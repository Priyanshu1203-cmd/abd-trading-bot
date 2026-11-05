"""Indicators in plain pandas — no TA-Lib, so it installs anywhere and every formula is visible."""

from __future__ import annotations

import pandas as pd


def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False, min_periods=length).mean()


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(length, min_periods=length).mean()


def rsi(close: pd.Series, length: int = 14) -> pd.Series:
    """Wilder's RSI."""
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    out = 100 - 100 / (1 + gain / loss)
    # only gains → 100; a perfectly flat stretch → 50
    return out.where(loss != 0, 100.0).where((gain != 0) | (loss != 0), 50.0)


def atr(df: pd.DataFrame, length: int = 14) -> pd.Series:
    """Wilder's Average True Range."""
    prev_close = df["close"].shift()
    true_range = pd.concat(
        [df["high"] - df["low"], (df["high"] - prev_close).abs(), (df["low"] - prev_close).abs()], axis=1
    ).max(axis=1)
    return true_range.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()


def vwap(bars: pd.DataFrame) -> pd.Series:
    """Session VWAP — pass the bars of one session only."""
    typical = (bars["high"] + bars["low"] + bars["close"]) / 3
    volume = bars["volume"].cumsum()
    return (typical * bars["volume"]).cumsum() / volume.where(volume > 0)
