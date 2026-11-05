"""Crypto spot candles via ccxt: Binance first (deepest liquidity), Bybit/OKX as fallback. No API key needed."""

from __future__ import annotations

import threading

import ccxt
import pandas as pd

from ..models import Instrument, Market
from .base import OHLCV, DataError, clean

_TIMEFRAME = {"5m": "5m", "15m": "15m", "1h": "1h", "1d": "1d", "1wk": "1w"}
_QUOTES = ("USDT", "USDC", "FDUSD", "BTC", "ETH")  # suffixes we recognise in "BTCUSDT"-style input
_PAGE = 1000


class CryptoProvider:
    def __init__(self, exchanges: tuple[str, ...] = ("binance", "bybit", "okx")):
        self._names = exchanges
        self._ex: ccxt.Exchange | None = None
        self._lock = threading.RLock()  # ccxt's sync client isn't thread-safe, and web + bot share this provider

    @property
    def source(self) -> str:
        return self._ex.name if self._ex else "ccxt"

    def _exchange(self) -> ccxt.Exchange:
        with self._lock:
            return self._connect()

    def _connect(self) -> ccxt.Exchange:
        if self._ex is not None:
            return self._ex
        failures = []
        for name in self._names:
            config: dict = {"enableRateLimit": True, "timeout": 15_000}
            if name == "binance":
                config["options"] = {"fetchMarkets": {"types": ["spot"]}}  # skip futures metadata: ~2x faster
            exchange = getattr(ccxt, name)(config)
            try:
                exchange.load_markets()
            except ccxt.BaseError as exc:
                failures.append(f"{name}: {type(exc).__name__}")
                continue
            self._ex = exchange
            return exchange
        raise DataError("Crypto exchange se connect nahi ho paya (" + ", ".join(failures) + "). Internet check karo.")

    def resolve(self, query: str) -> Instrument:
        exchange = self._exchange()
        q = query.strip().upper().replace("-", "/").replace(" ", "")
        if "/" in q:
            candidates = [q]
        else:
            candidates = [f"{q[: -len(c)]}/{c}" for c in _QUOTES if q.endswith(c) and len(q) > len(c)]
            candidates.append(f"{q}/USDT")
        for symbol in candidates:
            market = exchange.markets.get(symbol)
            if market and market.get("spot"):
                return Instrument(Market.CRYPTO, symbol, symbol, exchange.name, market["quote"])
        raise DataError(f"'{query}' {exchange.name} par nahi mila — BTC, ETH, SOL ya BTCUSDT jaise likho.")

    def candles(self, inst: Instrument, timeframe: str, days: int) -> pd.DataFrame:
        exchange = self._exchange()
        tf = _TIMEFRAME[timeframe]
        step = exchange.parse_timeframe(tf) * 1000
        since = exchange.milliseconds() - days * 86_400_000
        rows: list[list] = []
        try:
            with self._lock:
                while True:
                    batch = exchange.fetch_ohlcv(inst.symbol, tf, since=since, limit=_PAGE)
                    if not batch:
                        break
                    rows += batch
                    following = batch[-1][0] + step
                    if following <= since or following > exchange.milliseconds():
                        break
                    since = following
        except ccxt.BaseError as exc:
            raise DataError(f"{exchange.name} se candles nahi aaye ({type(exc).__name__}). Thodi der baad try karo.") from exc
        if not rows:
            raise DataError(f"{inst.name} ka data nahi mila.")
        df = pd.DataFrame(rows, columns=["time", *OHLCV]).drop_duplicates("time")
        df = df.set_index(pd.to_datetime(df["time"], unit="ms", utc=True)).drop(columns="time")
        return clean(df)
