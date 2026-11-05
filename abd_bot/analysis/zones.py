"""Confluence: merge nearby levels into zones, then split them around the current price."""

from __future__ import annotations

from ..models import Level, Zone


def merge(levels: list[Level], tol: float) -> list[Zone]:
    """Levels within `tol` of a group's first level join that group, so no zone is wider than `tol`."""
    zones: list[Zone] = []
    group: list[Level] = []
    for level in sorted(levels, key=lambda lv: lv.price):
        if group and level.price - group[0].price > tol:
            zones.append(_to_zone(group))
            group = []
        group.append(level)
    if group:
        zones.append(_to_zone(group))
    return zones


def _to_zone(group: list[Level]) -> Zone:
    count: dict[str, int] = {}
    weight: dict[str, int] = {}
    for lv in group:
        count[lv.label] = count.get(lv.label, 0) + 1
        weight[lv.label] = max(weight.get(lv.label, 0), lv.weight)
    names = sorted(count, key=lambda name: (-weight[name], -count[name]))
    labels = [f"{name}×{count[name]}" if count[name] > 1 else name for name in names]
    # Repeats count up to 3: six touches of a 5m swing shouldn't outrank PDH + R1.
    strength = sum(weight[name] * min(count[name], 3) for name in names)
    return Zone(min(lv.price for lv in group), max(lv.price for lv in group), labels, strength)


def around(zones: list[Zone], price: float, span: float) -> tuple[list[Zone], list[Zone], list[Zone]]:
    """(above, below, at): above/below are nearest first and within `span` of price."""
    above = sorted((z for z in zones if z.low > price and z.low - price <= span), key=lambda z: z.low)
    below = sorted((z for z in zones if z.high < price and price - z.high <= span), key=lambda z: -z.high)
    at = [z for z in zones if z.low <= price <= z.high]
    return above, below, at


def pick(zones: list[Zone], price: float, scale: float) -> Zone | None:
    """Best trigger among zones on one side of price: strength counts, but halves every `scale` of distance.

    Zones come nearest-first, so on a tie the nearer one wins.
    """
    if not zones:
        return None
    return max(zones, key=lambda z: z.weight / (1 + _distance(z, price) / scale))


def _distance(zone: Zone, price: float) -> float:
    if zone.low > price:
        return zone.low - price
    if zone.high < price:
        return price - zone.high
    return 0.0
