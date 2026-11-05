"""The one entry point every interface calls: (style, market, symbol) → Report."""

from __future__ import annotations

import threading
import time

import pandas as pd

from .data import provider_for
from .models import Market, Report, Style
from .strategies import intraday, positional

CACHE_SECONDS = 60.0
_CACHE_LIMIT = 256
_cache: dict[tuple[Style, Market, str], tuple[float, Report]] = {}
_cache_lock = threading.Lock()


def analyze(style: Style, market: Market, query: str, now: pd.Timestamp | None = None) -> Report:
    now = now if now is not None else pd.Timestamp.now(tz="UTC")
    provider = provider_for(market)
    inst = provider.resolve(query)
    if style is Style.INTRADAY:
        return intraday.analyze(inst, provider, now)
    return positional.analyze(inst, provider, style, now)


def analyze_cached(style: Style, market: Market, query: str) -> Report:
    """analyze(), reusing a plan made in the last minute — the dashboard and Telegram often ask twice."""
    key = (style, market, query.strip().upper())
    with _cache_lock:
        hit = _cache.get(key)
    if hit and time.monotonic() - hit[0] < CACHE_SECONDS:
        return hit[1]
    report = analyze(style, market, query)
    with _cache_lock:
        if len(_cache) >= _CACHE_LIMIT:
            _cache.clear()
        _cache[key] = (time.monotonic(), report)
    return report
