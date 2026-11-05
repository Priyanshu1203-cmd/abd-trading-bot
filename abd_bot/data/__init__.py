"""Market data layer: one provider per market, all returning the same OHLCV frame."""

from functools import cache

from ..models import Market
from .base import DataError, DataProvider

__all__ = ["DataError", "DataProvider", "provider_for"]


@cache
def provider_for(market: Market) -> DataProvider:
    # Imported lazily: ccxt alone adds ~1s to startup, and each market needs only its own source.
    if market is Market.CRYPTO:
        from .crypto import CryptoProvider

        return CryptoProvider()
    from .yahoo import YahooForex, YahooStocks

    return YahooForex() if market is Market.FOREX else YahooStocks()
