"""Shared types. Every layer speaks these: data → analysis → strategy → report → interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import pandas as pd


class Style(str, Enum):
    INTRADAY = "intraday"
    SWING = "swing"
    LONG_TERM = "longterm"

    @property
    def label(self) -> str:
        return {"intraday": "Intraday", "swing": "Swing", "longterm": "Long-term"}[self.value]


class Market(str, Enum):
    STOCKS = "stocks"  # Indian equities and indices (NSE/BSE)
    CRYPTO = "crypto"
    FOREX = "forex"  # currency pairs, plus gold/silver/crude which forex traders watch alongside

    @property
    def label(self) -> str:
        return {"stocks": "Indian Stocks", "crypto": "Crypto", "forex": "Forex"}[self.value]


class Bias(str, Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    NEUTRAL = "Neutral"


@dataclass(frozen=True)
class Instrument:
    market: Market
    symbol: str  # provider symbol: "RELIANCE.NS", "BTC/USDT", "EURUSD=X"
    name: str  # what the user sees: "RELIANCE", "BTC/USDT", "EUR/USD"
    exchange: str  # "NSE", "Binance", "FX", ...
    currency: str  # quote currency: "INR", "USDT", "USD", ...
    has_volume: bool = True  # indices and spot FX have no usable volume → no VWAP
    is_index: bool = False


@dataclass
class Level:
    """One price traders watch (PDH, a swing high, R1...). Weight = how much it matters."""

    price: float
    label: str
    weight: int = 1


@dataclass
class Zone:
    """Levels close enough to act as one area. More labels and weight = stronger confluence."""

    low: float
    high: float
    labels: list[str]
    weight: int

    @property
    def mid(self) -> float:
        return (self.low + self.high) / 2


@dataclass
class Pool:
    """Resting liquidity: stops parked above an obvious high (buy-side) or below a low (sell-side)."""

    side: str  # "buy" | "sell"
    price: float
    label: str
    weight: int = 1


@dataclass
class Sweep:
    """Price wicked through a pool and closed back — the stop hunt algos are known for."""

    side: str  # which pool got taken: "buy" | "sell"
    price: float
    label: str
    time: pd.Timestamp


@dataclass
class Setup:
    direction: str  # "long" | "short"
    name: str  # "Breakout Buy", "Buy on Dip", ...
    trigger: str  # the condition in words, e.g. "15m close above 1,318.90 (PDH)"
    level: float  # the price that defines the trigger: a breakout edge, or the zone edge for a dip/rally
    entry: float
    stop: float
    targets: list[float]
    primary: bool = False
    note: str | None = None

    @property
    def risk(self) -> float:
        return abs(self.entry - self.stop)

    @property
    def reward_risk(self) -> float:
        return abs(self.targets[0] - self.entry) / self.risk if self.risk else 0.0


@dataclass
class Report:
    instrument: Instrument
    style: Style
    timeframe: str
    price: float
    change_pct: float | None
    change_basis: str  # what change_pct is measured against: "1D", "1W"
    as_of: pd.Timestamp
    status: str  # "LIVE", "Market closed — plan for next session", ...
    source: str
    bias: Bias
    bias_score: int
    bias_reasons: list[str]
    context: list[tuple[str, list[str]]] = field(default_factory=list)  # (section title, lines)
    resistance: list[Zone] = field(default_factory=list)  # nearest first
    support: list[Zone] = field(default_factory=list)  # nearest first
    at_price: list[Zone] = field(default_factory=list)  # zones price is trading inside
    pivots: dict[str, float] = field(default_factory=dict)
    buy_side: list[Pool] = field(default_factory=list)  # nearest first
    sell_side: list[Pool] = field(default_factory=list)
    sweeps: list[Sweep] = field(default_factory=list)
    setups: list[Setup] = field(default_factory=list)
    wait_zone: tuple[float, float] | None = None
    notes: list[str] = field(default_factory=list)
    candles: pd.DataFrame | None = None  # the bars the plan was built from, for charts
