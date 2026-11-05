from datetime import date

import numpy as np
import pandas as pd
import pytest

from abd_bot import fmt
from abd_bot.analysis import indicators as ind
from abd_bot.analysis import levels as lv
from abd_bot.analysis import liquidity as liq
from abd_bot.analysis import structure as st
from abd_bot.analysis import zones as zn
from abd_bot.models import Instrument, Level, Market

from .conftest import IST


def bars(highs, lows, closes=None, start="2026-11-02 09:15", freq="5min"):
    closes = closes if closes is not None else [(h + l) / 2 for h, l in zip(highs, lows)]
    index = pd.date_range(start, periods=len(highs), freq=freq, tz=IST)
    return pd.DataFrame(
        {"open": closes, "high": highs, "low": lows, "close": closes, "volume": 1000.0}, index=index
    )


# --- indicators ---------------------------------------------------------------------------


def test_rsi_extremes():
    rising = pd.Series(np.arange(1.0, 60.0))
    assert ind.rsi(rising).iloc[-1] == 100
    assert ind.rsi(rising[::-1].reset_index(drop=True)).iloc[-1] == pytest.approx(0)
    assert ind.rsi(pd.Series([5.0] * 40)).iloc[-1] == 50


def test_atr_of_constant_range():
    df = bars([102.0] * 40, [100.0] * 40)
    assert ind.atr(df).iloc[-1] == pytest.approx(2.0)


def test_vwap_weights_by_volume():
    df = bars([10.0, 20.0], [10.0, 20.0])
    df["volume"] = [3.0, 1.0]
    assert ind.vwap(df).iloc[-1] == pytest.approx((10 * 3 + 20 * 1) / 4)


# --- levels -------------------------------------------------------------------------------


def test_floor_pivots():
    piv = lv.floor_pivots(110, 90, 100)
    assert piv == pytest.approx({"S3": 70, "S2": 80, "S1": 90, "P": 100, "R1": 110, "R2": 120, "R3": 130})


def test_cpr_top_is_always_above_bottom():
    top, pivot, bottom = lv.cpr(120, 100, 115)
    assert (top, pivot, bottom) == pytest.approx((113.3333, 111.6667, 110.0), abs=1e-3)
    top, _, bottom = lv.cpr(120, 100, 101)  # close near the low flips TC/BC
    assert top > bottom


def test_cpr_relation():
    assert "bullish" in lv.cpr_relation(110, 108, 105, 103)
    assert "bearish" in lv.cpr_relation(100, 98, 105, 103)
    assert "Inside" in lv.cpr_relation(104.5, 103.5, 105, 103)


def test_prior_week_while_week_is_running():
    days = pd.bdate_range("2026-10-26", "2026-11-05", tz=IST)  # Mon 26 Oct … Thu 5 Nov
    daily = pd.DataFrame({"open": 1.0, "high": np.arange(len(days)) + 10.0, "low": 1.0, "close": 1.0,
                          "volume": 1.0}, index=days)
    prior, current = lv.prior_period(daily, "W", date(2026, 11, 5))
    assert prior["high"] == 14  # Fri 30 Oct was the 5th bar
    assert list(current.index.day) == [2, 3, 4, 5]
    prior, current = lv.prior_period(daily, "W", date(2026, 11, 9))  # next Monday: last week is complete
    assert prior["high"] == daily["high"].iloc[-1] and current.empty


def test_round_numbers():
    assert lv.nice_step(22.5) == 25
    assert lv.nice_step(1875) == 2000
    assert lv.nice_step(0.0045) == pytest.approx(0.005)
    assert lv.round_levels(1311, 25, 50) == [1275, 1300, 1325, 1350]


# --- structure, zones, liquidity --------------------------------------------------------------


def test_swings_and_trend():
    highs = [1, 2, 3, 6, 3, 2, 1, 2, 4, 8, 4, 3, 2, 3, 4]
    lows = [h - 1 for h in highs]
    lows[6], lows[12] = -5, -2  # two swing lows, the second one higher
    swings = st.find_swings(bars(highs, lows), k=2)
    assert [(s.kind, s.price) for s in swings if s.kind == "high"] == [("high", 6), ("high", 8)]
    assert [(s.kind, s.price) for s in swings if s.kind == "low"] == [("low", -5), ("low", -2)]
    assert st.trend(swings) == "up"


def test_merge_caps_repeats_and_pick_prefers_strength():
    levels = [Level(100.0, "PDH", 3), *[Level(100.0 + i / 10, "S/R") for i in range(6)], Level(103.0, "Round")]
    zones = zn.merge(levels, tol=1.0)
    assert zones[0].labels == ["PDH", "S/R×6"] and zones[0].weight == 6  # 3 + capped 3
    above, below, at = zn.around(zones, price=99.0, span=10)
    assert zn.pick(above, 99.0, scale=1.0) is zones[0]
    weak_near = zn.merge([Level(99.2, "Round"), Level(100.0, "PDH", 3)], tol=0.1)
    assert zn.pick(weak_near, 99.0, scale=1.0).labels == ["PDH"]


def test_equal_highs_pool_and_sweep():
    #             swing  …      equal high …     raid: wick 111, close 109.5
    highs = [100, 104, 110, 104, 100, 103, 110, 103, 100, 102, 111, 105]
    lows = [h - 2 for h in highs]
    closes = [h - 1 for h in highs]
    closes[10] = 109.5
    df = bars(highs, lows, closes)
    base = df.iloc[:-3]
    pools, _ = liq.resting_pools(base, st.find_swings(base, k=2), tol=0.5)
    assert [(p.price, p.label) for p in pools] == [(110, "Equal highs ×2")]
    sweeps = liq.find_sweeps(df, pools, window=3)
    assert len(sweeps) == 1 and sweeps[0].side == "buy" and sweeps[0].price == 110


def test_close_beyond_pool_is_a_breakout_not_a_sweep():
    highs = [100, 104, 110, 104, 100, 103, 112, 113]
    closes = [h - 1 for h in highs]
    df = bars(highs, [h - 2 for h in highs], closes)
    base = df.iloc[:-2]
    pools, _ = liq.resting_pools(base, st.find_swings(base, k=2), tol=0.5)
    assert liq.find_sweeps(df, pools, window=2) == []


# --- formatting ---------------------------------------------------------------------------


def test_indian_grouping_and_precision():
    inr = Instrument(Market.STOCKS, "X.NS", "X", "NSE", "INR")
    f = fmt.formatter(inr, 1311.0)
    assert f(1234567.891) == "12,34,567.89" and f(1311) == "1,311.00" and f(-5554005) == "-55,54,005.00"
    eurusd = Instrument(Market.FOREX, "EURUSD=X", "EUR/USD", "FX", "USD", has_volume=False)
    assert fmt.formatter(eurusd, 1.1244)(1.12444) == "1.1244"
    usdjpy = Instrument(Market.FOREX, "USDJPY=X", "USD/JPY", "FX", "JPY", has_volume=False)
    assert fmt.formatter(usdjpy, 150.12)(150.1234) == "150.123"
    btc = Instrument(Market.CRYPTO, "BTC/USDT", "BTC/USDT", "Binance", "USDT")
    assert fmt.formatter(btc, 80514.0)(80514.012) == "80,514.01"
