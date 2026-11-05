"""Intraday plan: previous-day levels, CPR, pivots, opening range, VWAP and intraday liquidity → trigger points."""

from __future__ import annotations

import pandas as pd

from .. import fmt
from ..analysis import indicators as ind
from ..analysis import levels as lv
from ..analysis import liquidity as liq
from ..analysis import structure as st
from ..analysis import zones as zn
from ..analysis.session import IST, NSE_OPEN, day_context, fx_sessions
from ..data import DataError, DataProvider
from ..fmt import Fmt
from ..models import Bias, Instrument, Level, Market, Pool, Report, Style
from .common import (
    SHORT_NOTE,
    RiskRules,
    band_vote,
    breakout,
    decide,
    level_vote,
    ma_vote,
    rsi_vote,
    structure_vote,
    sweep_vote,
)

TIMEFRAME = {Market.STOCKS: "5m", Market.CRYPTO: "15m", Market.FOREX: "15m"}
CONFIRM = "15m"  # every trigger waits for a 15-minute candle close
OPENING_RANGE_MINUTES = 15
SWING_K = 3
SWEEP_BARS = 12
RISK_ATR = (0.15, 0.6, 0.3, 0.02)  # stop min / max / default distance and entry buffer, in daily ATRs
PICK_ATR = 0.25  # a trigger zone's strength halves every quarter daily-ATR away from price


def analyze(inst: Instrument, provider: DataProvider, now: pd.Timestamp) -> Report:
    tf = TIMEFRAME[inst.market]
    intraday = provider.candles(inst, tf, days=7)
    daily = provider.candles(inst, "1d", days=200)
    ctx = day_context(inst.market, intraday, daily, now)
    done = ctx.completed
    if len(done) < 22 or len(intraday) < 60:
        raise DataError(f"{inst.name}: intraday plan ke liye history kam hai.")

    prev = done.iloc[-1]
    ph, pl, pc = float(prev["high"]), float(prev["low"]), float(prev["close"])
    datr = float(ind.atr(done).iloc[-1])
    price = float(intraday["close"].iloc[-1])
    f = fmt.formatter(inst, price)
    bars = ctx.day_bars
    tol = 0.1 * datr

    # --- reference levels ----------------------------------------------------------------
    levels = [Level(ph, "PDH", 3), Level(pl, "PDL", 3), Level(pc, "PDC", 1)]
    top, pivot, bottom = lv.cpr(ph, pl, pc)
    if top - bottom <= tol:
        levels.append(Level(pivot, "CPR", 3))
    else:
        levels += [Level(top, "CPR TC", 2), Level(bottom, "CPR BC", 2)]
    piv = lv.floor_pivots(ph, pl, pc)
    levels += [Level(piv["R1"], "R1", 2), Level(piv["S1"], "S1", 2), Level(piv["R2"], "R2", 1), Level(piv["S2"], "S2", 1)]
    prior_week, this_week = lv.prior_period(done, "W", ctx.session_date)
    if prior_week is not None:
        levels += [Level(float(prior_week["high"]), "PWH", 3), Level(float(prior_week["low"]), "PWL", 3)]

    day_high = float(bars["high"].max()) if not bars.empty else float("-inf")
    day_low = float(bars["low"].min()) if not bars.empty else float("inf")
    opening_range = None
    vwap = None
    if not bars.empty:  # only non-empty while the session is live
        levels += [Level(day_high, "Day High", 2), Level(day_low, "Day Low", 2)]
        if inst.market is Market.STOCKS:
            open_at = pd.Timestamp.combine(ctx.session_date, NSE_OPEN).tz_localize(IST)
            if now >= open_at + pd.Timedelta(minutes=OPENING_RANGE_MINUTES):
                opening_range = lv.opening_range(bars, open_at, OPENING_RANGE_MINUTES)
            if opening_range:
                levels += [Level(opening_range[0], "ORB High", 3), Level(opening_range[1], "ORB Low", 3)]
        else:
            levels.append(Level(float(bars["open"].iloc[0]), "Day Open", 2))
        if inst.has_volume and bars["volume"].sum() > 0:
            vwap = float(ind.vwap(bars).iloc[-1])
            levels.append(Level(vwap, "VWAP", 2))

    swings = st.find_swings(intraday, SWING_K)
    levels += [Level(s.price, "S/R", 1) for s in swings]
    levels += [Level(p, "Round", 1) for p in lv.round_levels(price, lv.nice_step(0.75 * datr), 2 * datr)]

    zones = zn.merge(levels, tol)
    above, below, at = zn.around(zones, price, 1.5 * datr)

    # --- liquidity -----------------------------------------------------------------------
    eq_tol = 0.05 * datr
    buy_side, sell_side = liq.resting_pools(intraday, swings, eq_tol)
    if day_high < ph:
        buy_side.append(Pool("buy", ph, "PDH", 3))
    if day_low > pl:
        sell_side.append(Pool("sell", pl, "PDL", 3))
    if prior_week is not None:
        week_high = max(day_high, float(this_week["high"].max()) if not this_week.empty else float("-inf"))
        week_low = min(day_low, float(this_week["low"].min()) if not this_week.empty else float("inf"))
        if week_high < prior_week["high"]:
            buy_side.append(Pool("buy", float(prior_week["high"]), "PWH", 3))
        if week_low > prior_week["low"]:
            sell_side.append(Pool("sell", float(prior_week["low"]), "PWL", 3))
    reach = 2 * datr
    buy_side = [p for p in liq.merge_pools(buy_side, eq_tol) if 0 < p.price - price <= reach][:3]
    sell_side = sorted(
        (p for p in liq.merge_pools(sell_side, eq_tol) if 0 < price - p.price <= reach), key=lambda p: -p.price
    )[:3]

    # pools that were still untouched when the sweep window opened
    base = intraday.iloc[:-SWEEP_BARS]
    base_buy, base_sell = liq.resting_pools(base, st.find_swings(base, SWING_K), eq_tol)
    if ctx.live:
        early = bars[bars.index < intraday.index[-SWEEP_BARS]]
        if early.empty or early["high"].max() < ph:
            base_buy.append(Pool("buy", ph, "PDH", 3))
        if early.empty or early["low"].min() > pl:
            base_sell.append(Pool("sell", pl, "PDL", 3))
    sweeps = liq.find_sweeps(
        intraday, liq.merge_pools(base_buy, eq_tol) + liq.merge_pools(base_sell, eq_tol), SWEEP_BARS
    )

    # --- bias ----------------------------------------------------------------------------
    close = intraday["close"]
    votes = [
        ma_vote(price, float(ind.ema(close, 20).iloc[-1]), float(ind.ema(close, 50).iloc[-1]), f"EMA20/50 ({tf})"),
        structure_vote(swings, price, tf, f),
        rsi_vote(float(ind.rsi(close).iloc[-1]), tf),
        band_vote(price, top, bottom, "CPR", f),
    ]
    if vwap is not None:
        votes.append(level_vote(price, vwap, "VWAP", f))
    if vote := sweep_vote(sweeps, f):
        votes.append(vote)
    bias, score, reasons = decide(votes)

    # --- trigger points ------------------------------------------------------------------
    rules = RiskRules.from_atr(datr, *RISK_ATR)
    # Triggers sit outside the zone price is trading in; that zone is part of the wait area.
    up, down = zn.pick(above, price, PICK_ATR * datr), zn.pick(below, price, PICK_ATR * datr)
    setups = []
    if up:
        setups.append(breakout("long", up, zones, rules, CONFIRM, f))
    if down:
        short = breakout("short", down, zones, rules, CONFIRM, f)
        if inst.market is Market.CRYPTO:
            short.note = SHORT_NOTE[Market.CRYPTO]
        setups.append(short)
    for setup in setups:
        setup.primary = (setup.direction == "long" and bias is Bias.BULLISH) or (
            setup.direction == "short" and bias is Bias.BEARISH
        )

    # --- context -------------------------------------------------------------------------
    context = []
    if inst.market is Market.STOCKS and not bars.empty:
        context.append(("🌅 Opening", _opening_lines(bars, pc, price, opening_range, f)))
    context.append(("🧭 CPR", _cpr_lines(done, top, pivot, bottom, f)))
    if not bars.empty:
        context.append(("📅 Today", [f"Open {f(float(bars['open'].iloc[0]))} · High {f(day_high)} · Low {f(day_low)}"]))
    else:
        context.append(("📅 Last session", [f"Open {f(float(prev['open']))} · High {f(ph)} · Low {f(pl)} · Close {f(pc)}"]))
    if inst.market is Market.FOREX:
        context.append(("🌍 Session", [fx_sessions(now)]))

    notes = []
    if not ctx.live:
        notes.append("These levels are for the next session; Opening Range and VWAP appear once it opens.")
    if inst.market is not Market.CRYPTO:
        notes.append("Yahoo data can lag a few minutes — confirm levels on your broker chart before acting.")
    if inst.is_index:
        notes.append("An index has no volume, so no VWAP — use the index futures chart for VWAP.")
    elif not inst.has_volume:
        notes.append("Spot FX has no central volume, so VWAP isn't used.")
    if inst.market is Market.CRYPTO:
        notes.append("Crypto day starts 05:30 IST (00:00 UTC) — PDH/PDL/CPR use that day.")

    change = (price / pc - 1) * 100 if ctx.live else (pc / float(done["close"].iloc[-2]) - 1) * 100
    return Report(
        instrument=inst,
        style=Style.INTRADAY,
        timeframe=tf,
        price=price,
        change_pct=change,
        change_basis="1D",
        as_of=intraday.index[-1],
        status=ctx.status,
        source=provider.source,
        bias=bias,
        bias_score=score,
        bias_reasons=reasons,
        context=context,
        resistance=above[:4],
        support=below[:4],
        at_price=at,
        pivots={k: piv[k] for k in ("S2", "S1", "P", "R1", "R2")},
        buy_side=buy_side,
        sell_side=sell_side,
        sweeps=sweeps[-3:],
        setups=setups,
        wait_zone=(down.low, up.high) if up and down else None,
        notes=notes,
        candles=intraday,
    )


def _opening_lines(bars: pd.DataFrame, pdc: float, price: float, opening_range: tuple[float, float] | None, f: Fmt) -> list[str]:
    day_open = float(bars["open"].iloc[0])
    gap = (day_open / pdc - 1) * 100
    if abs(gap) < 0.1:
        lines = [f"Flat open at {f(day_open)} (PDC {f(pdc)})"]
    else:
        filled = bars["low"].min() <= pdc if gap > 0 else bars["high"].max() >= pdc
        kind = "Gap-up" if gap > 0 else "Gap-down"
        lines = [f"{kind} {gap:+.2f}% (Open {f(day_open)} vs PDC {f(pdc)}) — {'gap filled' if filled else 'gap not filled yet'}"]
    if opening_range is None:
        lines.append("Opening range (09:15–09:30) still forming")
    else:
        high, low = opening_range
        if price > high:
            where = "above it → upside breakout"
        elif price < low:
            where = "below it → downside breakdown"
        else:
            where = "inside it → wait for a break"
        lines.append(f"Opening range 09:15–09:30: {f(low)} – {f(high)} · price {where}")
    return lines


def _cpr_lines(done: pd.DataFrame, top: float, pivot: float, bottom: float, f: Fmt) -> list[str]:
    widths = lv.cpr_width_pct(done)
    width = float(widths.iloc[-1])
    rank = float((widths.iloc[-21:-1] < width).mean())
    kind = "narrow" if rank <= 0.3 else "wide" if rank >= 0.7 else "normal"
    hint = {
        "narrow": "trending / breakout day likely",
        "wide": "sideways / range day likely",
        "normal": "no strong edge from width",
    }[kind]
    before = done.iloc[-2]
    prev_top, _, prev_bottom = lv.cpr(float(before["high"]), float(before["low"]), float(before["close"]))
    return [
        f"TC {f(top)} · P {f(pivot)} · BC {f(bottom)}",
        f"Width {width:.2f}% — {kind} vs last 20 sessions → {hint}",
        lv.cpr_relation(top, bottom, prev_top, prev_bottom),
    ]
