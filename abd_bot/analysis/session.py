"""Which session is the plan for? Market hours and live/closed logic for intraday plans.

Most intraday bugs are "wrong day" bugs, so all of that reasoning lives here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time, timedelta

import pandas as pd

from ..models import Market

IST = "Asia/Kolkata"
NSE_OPEN, NSE_CLOSE = time(9, 15), time(15, 30)
_STALE = pd.Timedelta(minutes=45)  # FX/crypto: no new candle for this long → market is shut
_FX_SESSIONS = (  # (name, timezone, local open hour, local close hour)
    ("Sydney", "Australia/Sydney", 7, 16),
    ("Tokyo", "Asia/Tokyo", 9, 18),
    ("London", "Europe/London", 8, 17),
    ("New York", "America/New_York", 8, 17),
)


@dataclass
class DayContext:
    live: bool
    session_date: date  # the session the plan is for: today when live, else the next trading day
    day_bars: pd.DataFrame  # intraday bars of the running session; empty when not live
    completed: pd.DataFrame  # daily bars of finished sessions only
    status: str


def day_context(market: Market, intraday: pd.DataFrame, daily: pd.DataFrame, now: pd.Timestamp) -> DayContext:
    if market is Market.STOCKS:
        tz = IST
    elif market is Market.CRYPTO:
        tz = "UTC"  # exchange days roll at 00:00 UTC = 05:30 IST
    else:
        tz = daily.index.tz  # Yahoo FX days follow London, COMEX metals New York
    intraday, daily, local_now = intraday.tz_convert(tz), daily.tz_convert(tz), now.tz_convert(tz)
    last_date = intraday.index[-1].date()
    bars = intraday[intraday.index.date == last_date]

    if market is Market.STOCKS:
        in_hours = local_now.weekday() < 5 and NSE_OPEN <= local_now.time() < NSE_CLOSE
        live = in_hours and last_date == local_now.date()
        if live:
            status = "LIVE"
        elif in_hours:
            status = "Market open — today's candles not in feed yet, using last session"
        elif local_now.weekday() < 5 and local_now.time() < NSE_OPEN:
            status = "Pre-market — plan for today's session"
        else:
            status = "Market closed — plan for next session"
    else:
        live = local_now - intraday.index[-1] < _STALE
        if live:
            status = "LIVE (24×7)" if market is Market.CRYPTO else "LIVE"
        else:
            status = "Market closed — plan for next session"

    if live:
        return DayContext(True, last_date, bars, daily[daily.index.date < last_date], status)

    completed = daily[daily.index.date <= last_date]
    if completed.empty or completed.index[-1].date() != last_date:
        # the feed has no daily bar for the last session yet: build it from its intraday candles
        completed = pd.concat([completed, _as_daily_bar(bars, last_date, tz)])
    return DayContext(False, _next_weekday(last_date), bars.iloc[0:0], completed, status)


def fx_sessions(now: pd.Timestamp) -> str:
    active = []
    for name, tz, start, end in _FX_SESSIONS:
        local = now.tz_convert(tz)
        if local.weekday() < 5 and start <= local.hour < end:
            active.append(name)
    if not active:
        return "No major session open — thin liquidity, fake moves common"
    if "London" in active and "New York" in active:
        return "London + New York overlap — highest liquidity of the day"
    return "Active: " + " + ".join(active)


def _as_daily_bar(bars: pd.DataFrame, day: date, tz) -> pd.DataFrame:
    row = {
        "open": bars["open"].iloc[0],
        "high": bars["high"].max(),
        "low": bars["low"].min(),
        "close": bars["close"].iloc[-1],
        "volume": bars["volume"].sum(),
    }
    return pd.DataFrame([row], index=pd.DatetimeIndex([pd.Timestamp(day).tz_localize(tz)]))


def _next_weekday(day: date) -> date:
    day += timedelta(days=1)
    while day.weekday() >= 5:
        day += timedelta(days=1)
    return day
