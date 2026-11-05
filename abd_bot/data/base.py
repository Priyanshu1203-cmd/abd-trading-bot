"""Data-provider contract: every market source returns the same OHLCV frame shape."""

from __future__ import annotations

from typing import Protocol

import pandas as pd

from ..models import Instrument

OHLCV = ["open", "high", "low", "close", "volume"]


class DataError(Exception):
    """A problem worth showing the user as-is: unknown symbol, no data, network down."""


class DataProvider(Protocol):
    source: str

    def resolve(self, query: str) -> Instrument:
        """Turn what the user typed ("reliance", "btc", "eurusd") into an instrument."""
        ...

    def candles(self, inst: Instrument, timeframe: str, days: int) -> pd.DataFrame:
        """OHLCV for the last `days` calendar days: tz-aware index of bar open times, oldest first."""
        ...


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return df.dropna(subset=["open", "high", "low", "close"])
