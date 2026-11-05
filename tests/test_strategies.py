"""End-to-end: synthetic candles → strategy → report → text, for every style and market."""

import pandas as pd
import pytest

from abd_bot.models import Instrument, Market, Report, Style
from abd_bot.report import render
from abd_bot.strategies import intraday, positional

from .conftest import IST, FakeProvider, daily_from, nse_5m, random_walk

NSE = Instrument(Market.STOCKS, "TEST.NS", "TEST", "NSE", "INR")
COIN = Instrument(Market.CRYPTO, "TEST/USDT", "TEST/USDT", "Binance", "USDT")
PAIR = Instrument(Market.FOREX, "EURUSD=X", "EUR/USD", "FX", "USD", has_volume=False)


def check(report: Report) -> str:
    """Invariants every plan must satisfy, whatever the market did."""
    for s in report.setups:
        sign = 1 if s.direction == "long" else -1
        assert sign * (s.entry - s.stop) > 0, s
        assert all(sign * (t - s.entry) >= s.risk * 0.999 for t in s.targets), s  # every target ≥ 1R
        assert sign * (s.targets[1] - s.targets[0]) > 0, s
    assert all(z.low > report.price for z in report.resistance)
    assert all(z.high < report.price for z in report.support)
    assert all(p.price > report.price for p in report.buy_side)
    assert all(p.price < report.price for p in report.sell_side)
    if report.wait_zone:
        assert report.wait_zone[0] < report.price < report.wait_zone[1]
    text = render(report)
    assert report.instrument.name in text and "not investment advice" in text
    return text


def nse_intraday(now: pd.Timestamp, seed: int = 1) -> FakeProvider:
    full = random_walk(nse_5m(120, "2026-11-04"), start=1300, vol=0.0015, seed=seed)
    seen = full[full.index <= now - pd.Timedelta(minutes=5)]  # only candles that exist at `now`
    return FakeProvider(NSE, {"5m": seen.iloc[-7 * 75 :], "1d": daily_from(seen, IST)})


def round_the_clock(inst: Instrument, tz: str, now: pd.Timestamp, volume: bool, seed: int = 2) -> FakeProvider:
    last_bar = (now.floor("15min") - pd.Timedelta(minutes=15)).tz_convert(tz)
    index = pd.date_range(end=last_bar, periods=200 * 96, freq="15min")
    full = random_walk(index, start=80_000 if volume else 1.12, vol=0.003, seed=seed, volume=volume)
    return FakeProvider(inst, {"15m": full.iloc[-7 * 96 :], "1d": daily_from(full, tz)})


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_nse_live_session_has_opening_range_and_vwap(seed):
    now = pd.Timestamp("2026-11-04 12:00", tz=IST)
    report = intraday.analyze(NSE, nse_intraday(now, seed), now)
    text = check(report)
    assert report.status == "LIVE"
    assert "Opening range 09:15–09:30" in text and "VWAP" in text
    assert report.setups and report.wait_zone


def test_nse_after_close_plans_next_session():
    now = pd.Timestamp("2026-11-04 18:00", tz=IST)
    report = intraday.analyze(NSE, nse_intraday(now), now)
    text = check(report)
    assert "closed" in report.status and "🌅 Opening" not in text
    assert any("next session" in note for note in report.notes)


def test_nse_pre_market_uses_yesterday_as_previous_day():
    now = pd.Timestamp("2026-11-05 08:00", tz=IST)
    provider = nse_intraday(now)
    report = intraday.analyze(NSE, provider, now)
    check(report)
    assert report.status.startswith("Pre-market")
    last_session = provider.frames["1d"].iloc[-1]
    assert report.pivots["P"] == pytest.approx((last_session.high + last_session.low + last_session.close) / 3)


def test_crypto_intraday_is_live_round_the_clock():
    now = pd.Timestamp("2026-11-08 03:00", tz="UTC")  # a Sunday
    report = intraday.analyze(COIN, round_the_clock(COIN, "UTC", now, volume=True), now)
    text = check(report)
    assert report.status == "LIVE (24×7)" and "Day Open" in text


def test_forex_intraday_skips_vwap_and_names_the_session():
    now = pd.Timestamp("2026-11-04 14:00", tz="UTC")
    report = intraday.analyze(PAIR, round_the_clock(PAIR, "Europe/London", now, volume=False), now)
    text = check(report)
    assert "VWAP" not in text.split("📝 Notes")[0]
    assert "London + New York overlap" in text


@pytest.mark.parametrize("style", [Style.SWING, Style.LONG_TERM])
@pytest.mark.parametrize("inst", [NSE, COIN])
@pytest.mark.parametrize("seed", [4, 5, 6])
def test_positional_plans(style, inst, seed):
    if style is Style.SWING:
        index = pd.bdate_range(end="2026-11-04", periods=560, tz=IST)
        frame = random_walk(index, start=1300, vol=0.015, seed=seed)
    else:
        index = pd.date_range(end="2026-11-02", periods=900, freq="W-MON", tz=IST)
        frame = random_walk(index, start=1300, vol=0.035, seed=seed)
    report = positional.analyze(inst, FakeProvider(inst, {"1d": frame, "1wk": frame}), style, pd.Timestamp.now(tz="UTC"))
    check(report)
    assert report.setups
    if style is Style.LONG_TERM:
        assert all(s.direction == "long" for s in report.setups)  # investors never get a short
    for s in report.setups:
        if s.direction == "short" and inst.market is Market.STOCKS:
            assert "F&O" in s.note
