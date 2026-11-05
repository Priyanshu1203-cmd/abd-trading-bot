"""Classic reference levels: pivots, CPR, previous period high/low, opening range, round numbers."""

from __future__ import annotations

import math
from datetime import date

import pandas as pd

_AGG = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}


def floor_pivots(high: float, low: float, close: float) -> dict[str, float]:
    p = (high + low + close) / 3
    return {
        "S3": low - 2 * (high - p),
        "S2": p - (high - low),
        "S1": 2 * p - high,
        "P": p,
        "R1": 2 * p - low,
        "R2": p + (high - low),
        "R3": high + 2 * (p - low),
    }


def cpr(high: float, low: float, close: float) -> tuple[float, float, float]:
    """Central Pivot Range as (top, pivot, bottom)."""
    pivot = (high + low + close) / 3
    bc = (high + low) / 2
    tc = 2 * pivot - bc
    return max(tc, bc), pivot, min(tc, bc)


def cpr_width_pct(daily: pd.DataFrame) -> pd.Series:
    """Width (% of pivot) of the CPR each daily bar projects onto the session after it."""
    pivot = (daily["high"] + daily["low"] + daily["close"]) / 3
    bc = (daily["high"] + daily["low"]) / 2
    return 2 * (pivot - bc).abs() / pivot * 100


def cpr_relation(top: float, bottom: float, prev_top: float, prev_bottom: float) -> str:
    """Two-day CPR relationship — the CPR traders' read on where value is moving."""
    if bottom > prev_top:
        return "Higher value vs previous CPR → bullish"
    if top < prev_bottom:
        return "Lower value vs previous CPR → bearish"
    if top <= prev_top and bottom >= prev_bottom:
        return "Inside previous CPR → breakout day possible"
    if top >= prev_top and bottom <= prev_bottom:
        return "Engulfs previous CPR → sideways day likely"
    return f"Overlapping previous CPR → mild {'bullish' if top > prev_top else 'bearish'} drift"


def resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    return df.resample(rule).agg(_AGG).dropna(subset=["open"])


def prior_period(daily: pd.DataFrame, rule: str, session_date: date) -> tuple[pd.Series | None, pd.DataFrame]:
    """(last *completed* week/month/year bar before `session_date`, bars already inside the current one)."""
    buckets = resample(daily, rule)
    if buckets.empty:
        return None, daily.iloc[0:0]
    # Buckets are labelled by their last day (pandas 'W', 'ME', 'YE'), so a label on or after
    # the session date means that bucket is still running.
    if buckets.index[-1].date() >= session_date:
        if len(buckets) < 2:
            return None, daily
        return buckets.iloc[-2], daily[daily.index > buckets.index[-2]]
    return buckets.iloc[-1], daily.iloc[0:0]


def opening_range(bars: pd.DataFrame, open_time: pd.Timestamp, minutes: int) -> tuple[float, float] | None:
    window = bars[bars.index < open_time + pd.Timedelta(minutes=minutes)]
    if window.empty:
        return None
    return float(window["high"].max()), float(window["low"].min())


def nice_step(minimum: float) -> float:
    """Smallest 1 / 2 / 2.5 / 5 × 10ⁿ that is ≥ `minimum` — spacing for psychological round levels."""
    exp = math.floor(math.log10(minimum))
    for mult in (1, 2, 2.5, 5, 10):
        if mult * 10**exp >= minimum:
            return mult * 10**exp
    return 10 ** (exp + 1)


def round_levels(price: float, step: float, span: float) -> list[float]:
    first = math.ceil((price - span) / step) * step
    out = []
    level = first
    while level <= price + span:
        out.append(round(level, 10))
        level += step
    return out
