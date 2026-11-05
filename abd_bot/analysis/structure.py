"""Market structure: swing points, trend (HH/HL vs LH/LL) and breaks of structure."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Swing:
    pos: int  # integer position in the frame it was found in
    time: pd.Timestamp
    price: float
    kind: str  # "high" | "low"


def find_swings(df: pd.DataFrame, k: int) -> list[Swing]:
    """Fractal swings: a high above the k bars before it and not exceeded by the k after (mirror for lows).

    The last k bars can't qualify yet — a swing is only known once price has moved away from it.
    """
    highs, lows = df["high"].to_numpy(), df["low"].to_numpy()
    swings = []
    for i in range(k, len(df) - k):
        if highs[i] > highs[i - k : i].max() and highs[i] >= highs[i + 1 : i + k + 1].max():
            swings.append(Swing(i, df.index[i], float(highs[i]), "high"))
        if lows[i] < lows[i - k : i].min() and lows[i] <= lows[i + 1 : i + k + 1].min():
            swings.append(Swing(i, df.index[i], float(lows[i]), "low"))
    return swings


def trend(swings: list[Swing]) -> str:
    """'up' = higher high + higher low, 'down' = lower high + lower low, otherwise 'range'."""
    highs = [s.price for s in swings if s.kind == "high"][-2:]
    lows = [s.price for s in swings if s.kind == "low"][-2:]
    if len(highs) < 2 or len(lows) < 2:
        return "range"
    higher_high, higher_low = highs[1] > highs[0], lows[1] > lows[0]
    if higher_high and higher_low:
        return "up"
    if not higher_high and not higher_low:
        return "down"
    return "range"


def break_of_structure(close: float, swings: list[Swing]) -> tuple[str, Swing] | None:
    """Has the latest close gone beyond the most recent swing high ('bullish') or swing low ('bearish')?"""
    last_high = next((s for s in reversed(swings) if s.kind == "high"), None)
    last_low = next((s for s in reversed(swings) if s.kind == "low"), None)
    if last_high and close > last_high.price:
        return "bullish", last_high
    if last_low and close < last_low.price:
        return "bearish", last_low
    return None
