"""Liquidity: where stop orders cluster, and when price raids them.

Buy-side liquidity (BSL) = buy-stops of shorts and breakout buyers resting above unswept highs.
Sell-side liquidity (SSL) = sell-stops of longs resting below unswept lows.
Equal highs/lows are the most obvious clusters, which is why algos tend to run them first.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..models import Pool, Sweep
from .structure import Swing


def resting_pools(df: pd.DataFrame, swings: list[Swing], tol: float) -> tuple[list[Pool], list[Pool]]:
    """(buy_side, sell_side): swing highs/lows that no later bar has traded beyond."""
    highs, lows = df["high"].to_numpy(), df["low"].to_numpy()
    # most extreme price traded strictly *after* each bar
    later_high = np.append(np.maximum.accumulate(highs[::-1])[::-1][1:], -np.inf)
    later_low = np.append(np.minimum.accumulate(lows[::-1])[::-1][1:], np.inf)
    tops = [s.price for s in swings if s.kind == "high" and later_high[s.pos] <= s.price]
    bottoms = [s.price for s in swings if s.kind == "low" and later_low[s.pos] >= s.price]
    return _cluster(tops, "buy", tol), _cluster(bottoms, "sell", tol)


def _cluster(prices: list[float], side: str, tol: float) -> list[Pool]:
    groups: list[list[float]] = []
    for p in sorted(prices):
        if groups and p - groups[-1][0] <= tol:
            groups[-1].append(p)
        else:
            groups.append([p])
    kind = "highs" if side == "buy" else "lows"
    pools = []
    for g in groups:
        price = max(g) if side == "buy" else min(g)  # the stops sit beyond the most extreme one
        label = f"Equal {kind} ×{len(g)}" if len(g) > 1 else f"Swing {kind[:-1]}"
        pools.append(Pool(side, price, label, len(g)))
    return pools


def merge_pools(pools: list[Pool], tol: float) -> list[Pool]:
    """Combine same-side pools within `tol`, e.g. a PDH sitting on equal highs."""
    out: list[Pool] = []
    for pool in sorted(pools, key=lambda p: p.price):
        prev = out[-1] if out else None
        if prev and prev.side == pool.side and pool.price - prev.price <= tol:
            strong, weak = (prev, pool) if prev.weight >= pool.weight else (pool, prev)
            extreme = max(prev.price, pool.price) if pool.side == "buy" else min(prev.price, pool.price)
            out[-1] = Pool(pool.side, extreme, f"{strong.label} + {weak.label}", prev.weight + pool.weight)
        else:
            out.append(pool)
    return out


def find_sweeps(df: pd.DataFrame, candidates: list[Pool], window: int) -> list[Sweep]:
    """Raids inside the last `window` bars: a wick beyond a pool with no close beyond it since.

    `candidates` must be pools that were still untouched when the window began.
    """
    recent = df.iloc[-window:]
    sweeps = []
    for pool in candidates:
        if pool.side == "buy":
            pierced, closed_beyond = recent["high"] > pool.price, recent["close"] > pool.price
        else:
            pierced, closed_beyond = recent["low"] < pool.price, recent["close"] < pool.price
        if not pierced.any():
            continue
        first = pierced.idxmax()
        if not closed_beyond.loc[first:].any():
            sweeps.append(Sweep(pool.side, pool.price, pool.label, first))
    return sorted(sweeps, key=lambda s: s.time)
