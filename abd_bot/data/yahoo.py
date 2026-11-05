"""Indian stocks/indices (NSE/BSE) and forex/gold via Yahoo Finance: free, no API key.

Good for building and end-of-day work. Intraday it can lag a few minutes, so live NSE trading
should move to a broker feed (Kite, SmartAPI, Upstox, Dhan) — roadmap Phase 2.
"""

from __future__ import annotations

import logging
import time

import pandas as pd
import yfinance as yf

from ..models import Instrument, Market
from .base import OHLCV, DataError, clean

logging.getLogger("yfinance").setLevel(logging.CRITICAL)  # it logs every unknown symbol to stderr

_INTERVAL = {"5m": "5m", "15m": "15m", "1h": "60m", "1d": "1d", "1wk": "1wk"}

INDICES = {
    "NIFTY": ("^NSEI", "NIFTY 50"),
    "NIFTY50": ("^NSEI", "NIFTY 50"),
    "BANKNIFTY": ("^NSEBANK", "BANK NIFTY"),
    "NIFTYBANK": ("^NSEBANK", "BANK NIFTY"),
    "FINNIFTY": ("NIFTY_FIN_SERVICE.NS", "FIN NIFTY"),
    "SENSEX": ("^BSESN", "SENSEX"),
    "INDIAVIX": ("^INDIAVIX", "INDIA VIX"),
}

# Spot metals aren't on Yahoo; COMEX futures track XAU/USD and XAG/USD closely.
COMMODITIES = {
    "XAUUSD": ("GC=F", "GOLD (XAU/USD)"),
    "GOLD": ("GC=F", "GOLD (XAU/USD)"),
    "XAGUSD": ("SI=F", "SILVER (XAG/USD)"),
    "SILVER": ("SI=F", "SILVER (XAG/USD)"),
    "CRUDE": ("CL=F", "CRUDE OIL (WTI)"),
    "USOIL": ("CL=F", "CRUDE OIL (WTI)"),
}


def _download(symbol: str, timeframe: str, days: int) -> pd.DataFrame:
    end = pd.Timestamp.now(tz="UTC") + pd.Timedelta(days=1)
    start = end - pd.Timedelta(days=days + 1)
    for attempt in range(3):
        try:
            raw = yf.Ticker(symbol).history(
                start=start.date(),
                end=end.date(),
                interval=_INTERVAL[timeframe],
                auto_adjust=False,  # split-adjusted but not dividend-adjusted, like broker charts
                actions=False,
            )
            break
        except Exception as exc:  # yfinance raises assorted network / rate-limit errors
            if attempt == 2:
                raise DataError(f"Yahoo Finance se data nahi mila ({type(exc).__name__}). Thodi der baad try karo.") from exc
            time.sleep(1.5 * (attempt + 1))
    if raw.empty:
        return raw
    return raw.rename(columns=str.lower)[OHLCV]


class _Yahoo:
    source = "Yahoo Finance"

    def candles(self, inst: Instrument, timeframe: str, days: int) -> pd.DataFrame:
        df = _download(inst.symbol, timeframe, days)
        if df.empty:
            raise DataError(f"'{inst.name}' ka data nahi mila — symbol sahi hai? (delisted/rename ho sakta hai)")
        if timeframe in ("1d", "1wk") and pd.isna(df["close"].iloc[-1]):
            df = self._patch_last_close(inst, df)
        return clean(df)

    @staticmethod
    def _patch_last_close(inst: Instrument, df: pd.DataFrame) -> pd.DataFrame:
        """Yahoo sometimes leaves the newest daily/weekly close blank; take it from the 5m feed."""
        intraday = _download(inst.symbol, "5m", 5)
        if intraday.empty:
            return df
        intraday = intraday.dropna(subset=["close"])
        if intraday.empty or intraday.index[-1] < df.index[-1]:
            return df
        df = df.copy()
        df.loc[df.index[-1], "close"] = intraday["close"].iloc[-1]
        return df


class YahooStocks(_Yahoo):
    def resolve(self, query: str) -> Instrument:
        q = query.strip().upper().replace(" ", "")
        key = q.replace("-", "").replace("_", "")
        if key in INDICES:
            symbol, name = INDICES[key]
            exchange = "BSE" if symbol == "^BSESN" else "NSE"
            return Instrument(Market.STOCKS, symbol, name, exchange, "INR", has_volume=False, is_index=True)
        if not q.endswith((".NS", ".BO")):
            q += ".NS"
        exchange = "BSE" if q.endswith(".BO") else "NSE"
        return Instrument(Market.STOCKS, q, q.rsplit(".", 1)[0], exchange, "INR")


class YahooForex(_Yahoo):
    def resolve(self, query: str) -> Instrument:
        q = query.strip().upper().replace("/", "").replace(" ", "").removesuffix("=X")
        if q in COMMODITIES:
            symbol, name = COMMODITIES[q]
            return Instrument(Market.FOREX, symbol, name, "COMEX", "USD")
        if len(q) == 6 and q.isalpha():
            return Instrument(Market.FOREX, f"{q}=X", f"{q[:3]}/{q[3:]}", "FX", q[3:], has_volume=False)
        raise DataError(f"'{query}' samajh nahi aaya — pair aise likho: EURUSD, GBPJPY, USDINR (ya GOLD)")
