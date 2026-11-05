"""Swing (daily candles) and long-term (weekly candles): trend, S/R zones, liquidity and entries."""

from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd

from .. import fmt
from ..analysis import indicators as ind
from ..analysis import levels as lv
from ..analysis import liquidity as liq
from ..analysis import structure as st
from ..analysis import zones as zn
from ..data import DataError, DataProvider
from ..fmt import Fmt
from ..models import Bias, Instrument, Level, Pool, Report, Setup, Style
from .common import (
    SHORT_NOTE,
    RiskRules,
    breakout,
    decide,
    level_vote,
    ma_vote,
    retest,
    rsi_vote,
    structure_vote,
    sweep_vote,
)

SWING_K = 3


@dataclass(frozen=True)
class Plan:
    timeframe: str
    days: int  # history to request
    fast: int  # EMA lengths for trend alignment
    slow: int
    trend: int  # SMA length of the long-term filter (200 DMA / 200 WMA)
    unit: str  # "D" | "W"
    confirm: str  # candle that must close beyond a trigger
    span_atr: float  # show levels within this many ATRs of price
    risk_atr: tuple[float, float, float, float]  # stop min / max / default distance, entry buffer
    sweep_bars: int
    periods: tuple[tuple[str, str, str], ...]  # (resample rule, high label, low label)


PLANS = {
    Style.SWING: Plan(
        "1d", 800, 20, 50, 200, "D", "Daily", 5.0, (0.75, 2.5, 1.5, 0.1), 5, (("W", "PWH", "PWL"), ("ME", "PMH", "PML"))
    ),
    Style.LONG_TERM: Plan(
        "1wk", 7300, 10, 40, 200, "W", "Weekly", 5.0, (0.75, 2.0, 1.25, 0.1), 4, (("ME", "PMH", "PML"), ("YE", "PYH", "PYL"))
    ),
}


def analyze(inst: Instrument, provider: DataProvider, style: Style, now: pd.Timestamp) -> Report:
    plan = PLANS[style]
    df = provider.candles(inst, plan.timeframe, plan.days)
    if len(df) < 60:
        raise DataError(f"{inst.name}: {style.label} analysis ke liye history kam hai (sirf {len(df)} candles).")
    close = df["close"]
    price = float(close.iloc[-1])
    f = fmt.formatter(inst, price)
    atr = float(ind.atr(df).iloc[-1])
    suffix = "W" if plan.unit == "W" else ""
    fast_name, slow_name = f"EMA{plan.fast}{suffix}", f"EMA{plan.slow}{suffix}"
    trend_name = "200 DMA" if plan.unit == "D" else "200 WMA"
    fast, slow = float(ind.ema(close, plan.fast).iloc[-1]), float(ind.ema(close, plan.slow).iloc[-1])
    trend_ma = float(ind.sma(close, plan.trend).iloc[-1])  # NaN with fewer than 200 candles
    swings = st.find_swings(df, SWING_K)

    # --- levels --------------------------------------------------------------------------
    levels = [Level(s.price, "S/R", 1) for s in swings]
    levels += [Level(fast, fast_name, 1), Level(slow, slow_name, 2)]
    if not math.isnan(trend_ma):
        levels.append(Level(trend_ma, trend_name, 2))
    periods = []
    for rule, high_label, low_label in plan.periods:
        prior, current = lv.prior_period(df, rule, df.index[-1].date())
        if prior is None:
            continue
        levels += [Level(float(prior["high"]), high_label, 2), Level(float(prior["low"]), low_label, 2)]
        periods.append((prior, current, high_label, low_label))
    year = df[df.index > df.index[-1] - pd.Timedelta(days=365)]
    high_52, low_52 = float(year["high"].max()), float(year["low"].min())
    levels += [Level(high_52, "52W High", 3), Level(low_52, "52W Low", 3)]
    ath = float(df["high"].max())
    if style is Style.LONG_TERM:
        levels.append(Level(ath, "ATH", 3))
    span = plan.span_atr * atr
    levels += [Level(p, "Round", 1) for p in lv.round_levels(price, lv.nice_step(1.5 * atr), span)]

    zones = zn.merge(levels, 0.3 * atr)
    above, below, at = zn.around(zones, price, span)

    # --- liquidity -----------------------------------------------------------------------
    eq_tol = 0.1 * atr
    buy_side, sell_side = liq.resting_pools(df, swings, eq_tol)
    for prior, current, high_label, low_label in periods:
        high_since = float(current["high"].max()) if not current.empty else float("-inf")
        low_since = float(current["low"].min()) if not current.empty else float("inf")
        if high_since < prior["high"]:
            buy_side.append(Pool("buy", float(prior["high"]), high_label, 2))
        if low_since > prior["low"]:
            sell_side.append(Pool("sell", float(prior["low"]), low_label, 2))
    buy_side.append(Pool("buy", high_52, "52W High", 3))
    sell_side.append(Pool("sell", low_52, "52W Low", 3))
    buy_side = [p for p in liq.merge_pools(buy_side, eq_tol) if 0 < p.price - price <= span][:3]
    sell_side = sorted(
        (p for p in liq.merge_pools(sell_side, eq_tol) if 0 < price - p.price <= span), key=lambda p: -p.price
    )[:3]

    base = df.iloc[: -plan.sweep_bars]
    base_buy, base_sell = liq.resting_pools(base, st.find_swings(base, SWING_K), eq_tol)
    sweeps = liq.find_sweeps(
        df, liq.merge_pools(base_buy, eq_tol) + liq.merge_pools(base_sell, eq_tol), plan.sweep_bars
    )

    # --- bias ----------------------------------------------------------------------------
    votes = [
        ma_vote(price, fast, slow, f"EMA{plan.fast}/{plan.slow}{suffix}"),
        structure_vote(swings, price, plan.confirm, f),
        rsi_vote(float(ind.rsi(close).iloc[-1]), plan.confirm),
    ]
    if not math.isnan(trend_ma):
        votes.append(level_vote(price, trend_ma, trend_name, f))
    if vote := sweep_vote(sweeps, f):
        votes.append(vote)
    bias, score, reasons = decide(votes)

    # --- entries -------------------------------------------------------------------------
    rules = RiskRules.from_atr(atr, *plan.risk_atr)
    # the nearest worthwhile zone on each side: support for dips/breakdowns, resistance for rallies/breakouts
    up, down = zn.pick(above, price, atr), zn.pick(below, price, atr)
    close_word = plan.confirm.lower()
    setups: list[Setup] = []
    notes: list[str] = []
    if style is Style.LONG_TERM:
        if down:
            setups.append(retest("long", down, zones, rules, f, name="Accumulate"))
        if up:
            setups.append(breakout("long", up, zones, rules, plan.confirm, f))
        if bias is Bias.BEARISH and up:
            notes.append(f"Weekly trend is down — wait for a weekly close above {f(up.high)} before accumulating.")
    elif bias is Bias.BULLISH:
        if down:
            setups.append(retest("long", down, zones, rules, f))
        if up:
            setups.append(breakout("long", up, zones, rules, plan.confirm, f))
        if down:
            notes.append(f"Bullish view fails on a {close_word} close below {f(down.low)}.")
    elif bias is Bias.BEARISH:
        if up:
            setups.append(retest("short", up, zones, rules, f))
        if down:
            setups.append(breakout("short", down, zones, rules, plan.confirm, f))
        if up:
            notes.append(f"Bearish view fails on a {close_word} close above {f(up.high)}.")
    else:
        if up:
            setups.append(breakout("long", up, zones, rules, plan.confirm, f))
        if down:
            setups.append(breakout("short", down, zones, rules, plan.confirm, f))
        if up and down:
            notes.append(f"No side favoured — wait for a {close_word} close above {f(up.high)} or below {f(down.low)}.")
    # investors don't short, so only a downtrend leaves them without a favourite; swing has none in a range
    no_favourite = Bias.BEARISH if style is Style.LONG_TERM else Bias.NEUTRAL
    if setups and bias is not no_favourite:
        setups[0].primary = True
    for setup in setups:
        if setup.direction == "short":
            setup.note = SHORT_NOTE.get(inst.market)

    # --- context -------------------------------------------------------------------------
    position = (price - low_52) / (high_52 - low_52) * 100 if high_52 > low_52 else 50.0
    trend_lines = [
        f"52W range {f(low_52)} – {f(high_52)} · price at {position:.0f}% of it · {(price / high_52 - 1) * 100:+.1f}% from the high",
        f"ATR(14) {f(atr)} ({atr / price * 100:.1f}%) — typical {'daily' if plan.unit == 'D' else 'weekly'} move",
    ]
    if not math.isnan(trend_ma):
        trend_lines.append(f"{trend_name} {f(trend_ma)} · price {(price / trend_ma - 1) * 100:+.1f}% away")
    context = [("📈 Trend & range", trend_lines)]
    if style is Style.LONG_TERM:
        context.append(("🏦 Investor view", _investor_lines(df, price, ath, f)))

    return Report(
        instrument=inst,
        style=style,
        timeframe=plan.timeframe,
        price=price,
        change_pct=(price / float(close.iloc[-2]) - 1) * 100,
        change_basis="1" + plan.unit,
        as_of=df.index[-1],
        status=f"{plan.confirm} candles",
        source=provider.source,
        bias=bias,
        bias_score=score,
        bias_reasons=reasons,
        context=context,
        resistance=above[:5],
        support=below[:5],
        at_price=at,
        buy_side=buy_side,
        sell_side=sell_side,
        sweeps=sweeps[-3:],
        setups=setups,
        notes=notes,
        candles=df,
    )


def _investor_lines(df: pd.DataFrame, price: float, ath: float, f: Fmt) -> list[str]:
    lines = [f"ATH {f(ath)} ({df['high'].idxmax():%b %Y}) · price {(price / ath - 1) * 100:+.1f}% from it"]
    returns = []
    for years in (1, 3, 5, 10):
        past = df[df.index <= df.index[-1] - pd.DateOffset(years=years)]
        if past.empty:
            continue
        growth = (price / float(past["close"].iloc[-1])) ** (1 / years) - 1
        returns.append(f"{years}Y {'' if years == 1 else 'CAGR '}{growth * 100:+.1f}%")
    if returns:
        lines.append("Returns: " + " · ".join(returns))
    lines.append(f"History used: since {df.index[0]:%b %Y}")
    return lines
