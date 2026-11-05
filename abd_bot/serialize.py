"""Report → JSON-ready dict for the dashboard: raw numbers for the chart plus the same formatted text the bot shows."""

from __future__ import annotations

import math

import pandas as pd

from . import fmt
from .fmt import Fmt
from .models import Pool, Report, Setup, Sweep, Zone
from .report.text import DISCLAIMER, render, stars

IST = "Asia/Kolkata"
CHART_BARS = {"5m": 400, "15m": 400, "1d": 300, "1wk": 260}
_EPOCH = pd.Timestamp("1970-01-01")


def report_to_dict(r: Report) -> dict:
    inst = r.instrument
    f = fmt.formatter(inst, r.price)
    by_date = r.timeframe in ("1d", "1wk")
    return {
        "instrument": {
            "name": inst.name,
            "symbol": inst.symbol,
            "exchange": inst.exchange,
            "market": inst.market.value,
            "currency": inst.currency,
            "sign": "" if inst.exchange == "FX" else fmt.CURRENCY_SIGN.get(inst.currency, ""),
            "decimals": fmt.decimals(inst, r.price),
            "has_volume": inst.has_volume,
        },
        "style": r.style.value,
        "style_label": r.style.label,
        "timeframe": r.timeframe,
        "price": r.price,
        "price_text": f(r.price),
        "change_pct": _num(r.change_pct),
        "change_basis": r.change_basis,
        "as_of_text": _when(r.as_of, by_date),
        "status": r.status,
        "live": r.status.startswith("LIVE"),
        "source": r.source,
        "bias": {
            "label": r.bias.value,
            "score": r.bias_score,
            "votes": len(r.bias_reasons),
            "reasons": [_reason(text) for text in r.bias_reasons],
        },
        "context": [{"title": _plain(title), "lines": lines} for title, lines in r.context],
        "resistance": [_zone(z, f) for z in r.resistance],
        "support": [_zone(z, f) for z in r.support],
        "at_price": [_zone(z, f) for z in r.at_price],
        "pivots": [{"name": name, "price": value, "text": f(value)} for name, value in r.pivots.items()],
        "buy_side": [_pool(p, f) for p in r.buy_side],
        "sell_side": [_pool(p, f) for p in r.sell_side],
        "sweeps": [_sweep(s, f, by_date) for s in r.sweeps],
        "setups": [_setup(s, r.price, f) for s in r.setups],
        "wait_zone": None
        if r.wait_zone is None
        else {"low": r.wait_zone[0], "high": r.wait_zone[1], "text": f"{f(r.wait_zone[0])} – {f(r.wait_zone[1])}"},
        "notes": r.notes,
        "disclaimer": DISCLAIMER.removeprefix("ℹ️ "),
        "candles": _candles(r),
        "text": render(r, compact=True),
    }


def _zone(z: Zone, f: Fmt) -> dict:
    return {"low": z.low, "high": z.high, "mid": z.mid, "text": fmt.zone_price(z, f), "labels": z.labels, "stars": stars(z)}


def _pool(p: Pool, f: Fmt) -> dict:
    return {"price": p.price, "text": f(p.price), "label": p.label}


def _sweep(s: Sweep, f: Fmt, by_date: bool) -> dict:
    return {"side": s.side, "price": s.price, "text": f(s.price), "label": s.label, "when": _when(s.time, by_date)}


def _setup(s: Setup, price: float, f: Fmt) -> dict:
    # a long trigger above price is a breakout, below it a dip to buy; mirrored for shorts
    if s.direction == "long":
        verb = "Buy above" if s.level > price else "Buy near"
    else:
        verb = "Sell below" if s.level < price else "Sell near"
    return {
        "direction": s.direction,
        "name": s.name,
        "verb": verb,
        "trigger": s.trigger,
        "primary": s.primary,
        "note": s.note,
        "level": s.level,
        "level_text": f(s.level),
        "entry": s.entry,
        "entry_text": f(s.entry),
        "stop": s.stop,
        "stop_text": f(s.stop),
        "targets": [{"price": t, "text": f(t)} for t in s.targets],
        "reward_risk": round(s.reward_risk, 1),
    }


def _reason(text: str) -> dict:
    mark, _, rest = text.partition(" ")
    return {"dir": {"▲": "up", "▼": "down"}.get(mark, "flat"), "text": rest}


def _plain(title: str) -> str:
    """Drop the emoji the text report leads with: '🧭 CPR' → 'CPR'."""
    head, _, rest = title.partition(" ")
    return rest if rest and not head.isalnum() else title


def _when(ts: pd.Timestamp, date_only: bool) -> str:
    local = ts.tz_convert(IST)
    return f"{local:%d %b %Y}" if date_only else f"{local:%d %b, %H:%M} IST"


def _num(value: float | None) -> float | None:
    return float(value) if value is not None and math.isfinite(value) else None


def _candles(r: Report) -> list[dict]:
    if r.candles is None or r.candles.empty:
        return []
    bars = r.candles.iloc[-CHART_BARS.get(r.timeframe, 300) :]
    if r.timeframe in ("1d", "1wk"):
        times: list = [ts.strftime("%Y-%m-%d") for ts in bars.index]
    else:
        # The chart library has no time zones, so it gets IST wall-clock time written as UTC seconds.
        local = bars.index.tz_convert(IST).tz_localize(None)
        times = [int(s) for s in (local - _EPOCH) // pd.Timedelta(seconds=1)]
    return [
        {"time": t, "open": float(o), "high": float(h), "low": float(lo), "close": float(c), "volume": _num(float(v)) or 0.0}
        for t, o, h, lo, c, v in zip(times, bars["open"], bars["high"], bars["low"], bars["close"], bars["volume"])
    ]
