"""Price formatting shared by strategies (trigger text) and reports."""

from __future__ import annotations

import math
from collections.abc import Callable

from .models import Instrument, Zone

Fmt = Callable[[float], str]

CURRENCY_SIGN = {"INR": "₹", "USD": "$", "USDT": "$", "USDC": "$", "FDUSD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}


def formatter(inst: Instrument, ref_price: float) -> Fmt:
    """One precision for every price in a report, picked from the instrument's current price."""
    places = decimals(inst, ref_price)
    if inst.currency == "INR":
        return lambda value: _indian(value, places)
    return lambda value: f"{value:,.{places}f}"


def zone_price(zone: Zone, f: Fmt) -> str:
    low, high = f(zone.low), f(zone.high)
    return low if low == high else f"{low} – {high}"


def decimals(inst: Instrument, ref: float) -> int:
    if not math.isfinite(ref) or ref <= 0:
        return 2
    places = max(2, 4 - math.floor(math.log10(ref)))  # 80,000 → 2 · 2.31 → 4 · 0.18 → 5
    if inst.exchange == "FX":  # pairs quote in pips: 1.1244 · 150.123 · 94.748
        places = max(places, 3)
    return min(places, 8)


def _indian(value: float, places: int) -> str:
    """1234567.5 → '12,34,567.50' (lakh/crore grouping)."""
    whole, _, frac = f"{abs(value):.{places}f}".partition(".")
    if len(whole) > 3:
        head, groups = whole[:-3], [whole[-3:]]
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        whole = ",".join([head, *groups])
    return ("-" if value < 0 else "") + whole + (f".{frac}" if frac else "")
