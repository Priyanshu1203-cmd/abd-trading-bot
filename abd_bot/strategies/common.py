"""Pieces every strategy shares: bias votes, risk rules and setup construction."""

from __future__ import annotations

from dataclasses import dataclass

from ..analysis import structure as st
from ..analysis.structure import Swing
from ..fmt import Fmt, zone_price
from ..models import Bias, Market, Setup, Sweep, Zone

SHORT_NOTE = {
    Market.STOCKS: "Overnight shorts need F&O (futures/options); in cash, treat this as an exit level",
    Market.CRYPTO: "Shorting needs futures/perpetuals — spot can't go short",
}


# --- bias ---------------------------------------------------------------------------------


@dataclass(frozen=True)
class Vote:
    score: int  # +1 bullish, -1 bearish, 0 neutral
    reason: str


def decide(votes: list[Vote]) -> tuple[Bias, int, list[str]]:
    score = sum(v.score for v in votes)
    bias = Bias.BULLISH if score >= 2 else Bias.BEARISH if score <= -2 else Bias.NEUTRAL
    arrow = {1: "▲", -1: "▼", 0: "•"}
    return bias, score, [f"{arrow[v.score]} {v.reason}" for v in votes]


def ma_vote(price: float, fast: float, slow: float, names: str) -> Vote:
    if price > fast > slow:
        return Vote(1, f"Price above {names}, aligned up")
    if price < fast < slow:
        return Vote(-1, f"Price below {names}, aligned down")
    return Vote(0, f"{names} mixed — no clean trend")


def level_vote(price: float, level: float, name: str, f: Fmt) -> Vote:
    if price > level:
        return Vote(1, f"Above {name} {f(level)}")
    if price < level:
        return Vote(-1, f"Below {name} {f(level)}")
    return Vote(0, f"Sitting on {name} {f(level)}")


def band_vote(price: float, top: float, bottom: float, name: str, f: Fmt) -> Vote:
    if price > top:
        return Vote(1, f"Above {name} ({f(bottom)} – {f(top)})")
    if price < bottom:
        return Vote(-1, f"Below {name} ({f(bottom)} – {f(top)})")
    return Vote(0, f"Inside {name} — indecision")


def rsi_vote(value: float, tf: str) -> Vote:
    if value >= 60:
        return Vote(1, f"{tf} RSI {value:.0f} — bullish momentum")
    if value <= 40:
        return Vote(-1, f"{tf} RSI {value:.0f} — bearish momentum")
    return Vote(0, f"{tf} RSI {value:.0f} — neutral")


def structure_vote(swings: list[Swing], close: float, tf: str, f: Fmt) -> Vote:
    direction = st.trend(swings)
    bos = st.break_of_structure(close, swings)
    broke = ""
    if bos:
        kind, swing = bos
        broke = f"closed {'above' if kind == 'bullish' else 'below'} swing {swing.kind} {f(swing.price)}"
    if direction == "up":
        if bos and bos[0] == "bearish":
            return Vote(0, f"{tf} structure was HH+HL but {broke} — change of character, careful")
        return Vote(1, f"{tf} structure: Higher High + Higher Low" + (f", {broke}" if bos else ""))
    if direction == "down":
        if bos and bos[0] == "bullish":
            return Vote(0, f"{tf} structure was LH+LL but {broke} — change of character, careful")
        return Vote(-1, f"{tf} structure: Lower High + Lower Low" + (f", {broke}" if bos else ""))
    if bos:
        return Vote(1 if bos[0] == "bullish" else -1, f"{tf} structure: range, but {broke}")
    return Vote(0, f"{tf} structure: range — no clear HH/HL or LH/LL")


def sweep_vote(sweeps: list[Sweep], f: Fmt) -> Vote | None:
    if not sweeps:
        return None
    last = sweeps[-1]
    if last.side == "sell":
        return Vote(1, f"Sell-side liquidity swept below {f(last.price)} and reclaimed — stop hunt")
    return Vote(-1, f"Buy-side liquidity swept above {f(last.price)} and rejected — stop hunt")


# --- setups -------------------------------------------------------------------------------


@dataclass(frozen=True)
class RiskRules:
    """Stop-distance limits for a style, in price units."""

    min_risk: float
    max_risk: float
    default_risk: float
    buffer: float  # entry/stop offset beyond a level, so a touch alone doesn't trigger

    @classmethod
    def from_atr(cls, atr: float, min_x: float, max_x: float, default_x: float, buffer_x: float) -> RiskRules:
        return cls(atr * min_x, atr * max_x, atr * default_x, atr * buffer_x)


def breakout(direction: str, trigger: Zone, zones: list[Zone], rules: RiskRules, confirm: str, f: Fmt) -> Setup:
    """Enter on a close through the trigger zone; the stop hides behind the nearest structure on the other side."""
    sign = 1 if direction == "long" else -1
    edge = trigger.high if sign > 0 else trigger.low
    entry = edge + sign * rules.buffer
    stop = _protective_stop(entry, sign, zones, rules)
    return Setup(
        direction=direction,
        name="Breakout Buy" if sign > 0 else "Breakdown Sell",
        trigger=f"{confirm} close {'above' if sign > 0 else 'below'} {f(edge)} ({' + '.join(trigger.labels)})",
        level=edge,
        entry=entry,
        stop=stop,
        targets=_targets(entry, sign, abs(entry - stop), zones),
    )


def retest(direction: str, zone: Zone, zones: list[Zone], rules: RiskRules, f: Fmt, name: str | None = None) -> Setup:
    """Buy a dip into support (or sell a rally into resistance); the stop sits just beyond the zone."""
    sign = 1 if direction == "long" else -1
    entry = zone.high if sign > 0 else zone.low
    far_edge = zone.low if sign > 0 else zone.high
    risk = min(max(abs(entry - far_edge) + rules.buffer, rules.min_risk), rules.max_risk)
    return Setup(
        direction=direction,
        name=name or ("Buy on Dip" if sign > 0 else "Sell on Rise"),
        trigger=f"Price {'dips into' if sign > 0 else 'rallies into'} {zone_price(zone, f)} ({' + '.join(zone.labels)}) and holds",
        level=entry,
        entry=entry,
        stop=entry - sign * risk,
        targets=_targets(entry, sign, risk, zones),
    )


def _protective_stop(entry: float, sign: int, zones: list[Zone], rules: RiskRules) -> float:
    # Far edge of the nearest zone behind the entry; if structure is too far, fall back to an ATR stop.
    if sign > 0:
        edges = sorted((z.low for z in zones if z.low < entry), reverse=True)
    else:
        edges = sorted(z.high for z in zones if z.high > entry)
    for edge in edges:
        stop = edge - sign * rules.buffer
        risk = abs(entry - stop)
        if risk < rules.min_risk:
            continue
        return stop if risk <= rules.max_risk else entry - sign * rules.default_risk
    return entry - sign * rules.default_risk


def _targets(entry: float, sign: int, risk: float, zones: list[Zone], count: int = 2) -> list[float]:
    # Near edge of each zone ahead — where opposing orders start — at least 1R away.
    edges = [z.low if sign > 0 else z.high for z in zones]
    ahead = sorted((e for e in edges if sign * (e - entry) >= risk), key=lambda e: sign * (e - entry))
    targets: list[float] = []
    for edge in ahead:
        if not targets or sign * (edge - targets[-1]) >= 0.5 * risk:
            targets.append(edge)
        if len(targets) == count:
            return targets
    while len(targets) < count:  # open sky: fall back to R-multiples
        targets.append(targets[-1] + sign * risk if targets else entry + sign * 1.5 * risk)
    return targets
