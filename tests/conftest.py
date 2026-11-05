"""Synthetic markets so the whole pipeline runs offline and deterministically."""

from __future__ import annotations

import numpy as np
import pandas as pd

from abd_bot.analysis.levels import resample
from abd_bot.models import Instrument

IST = "Asia/Kolkata"


def random_walk(index: pd.DatetimeIndex, start: float = 1000.0, vol: float = 0.002, seed: int = 0,
                volume: bool = True) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = start * np.exp(np.cumsum(rng.normal(0, vol, len(index))))
    open_ = np.concatenate([[start], close[:-1]])
    wick = np.abs(rng.normal(0, vol, len(index))) * close
    return pd.DataFrame(
        {
            "open": open_,
            "high": np.maximum(open_, close) + wick,
            "low": np.minimum(open_, close) - wick,
            "close": close,
            "volume": rng.integers(1_000, 5_000, len(index)).astype(float) if volume else np.zeros(len(index)),
        },
        index=index,
    )


def nse_5m(days: int, last_day: str) -> pd.DatetimeIndex:
    """5-minute bar open times, 09:15–15:25 IST, for `days` weekdays ending on `last_day`."""
    sessions = pd.bdate_range(end=last_day, periods=days, tz=IST)
    offsets = pd.to_timedelta(np.arange(75) * 5 + 9 * 60 + 15, unit="min")
    return pd.DatetimeIndex([day + offset for day in sessions for offset in offsets])


def daily_from(intraday: pd.DataFrame, tz: str) -> pd.DataFrame:
    return resample(intraday.tz_convert(tz), "D")


class FakeProvider:
    source = "Synthetic"

    def __init__(self, inst: Instrument, frames: dict[str, pd.DataFrame]):
        self.inst, self.frames = inst, frames

    def resolve(self, query: str) -> Instrument:
        return self.inst

    def candles(self, inst: Instrument, timeframe: str, days: int) -> pd.DataFrame:
        return self.frames[timeframe]
