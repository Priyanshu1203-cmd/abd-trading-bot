"""Report → plain text with emoji. The same text works in the terminal today and in Telegram later."""

from __future__ import annotations

import pandas as pd

from .. import fmt
from ..fmt import Fmt
from ..models import Bias, Report, Zone

IST = "Asia/Kolkata"
RULE, SHORT_RULE = "━" * 38, "━" * 18
DISCLAIMER = "ℹ️ Educational market analysis, not investment advice. Use your own judgement and always a stop-loss."
_BIAS_ICON = {Bias.BULLISH: "🟢", Bias.BEARISH: "🔴", Bias.NEUTRAL: "🟡"}


def render(r: Report, compact: bool = False) -> str:
    """`compact` drops the column padding and long rules: phones show Telegram text in a proportional font."""
    f = fmt.formatter(r.instrument, r.price)
    rule = SHORT_RULE if compact else RULE
    # an FX rate is a ratio, not a price in one currency, so it gets no sign
    sign = "" if r.instrument.exchange == "FX" else fmt.CURRENCY_SIGN.get(r.instrument.currency, "")
    daily_bars = r.timeframe in ("1d", "1wk")
    change = f"  {r.change_pct:+.2f}% ({r.change_basis})" if r.change_pct is not None else ""
    out = [
        rule,
        f"📊 {r.instrument.name} · {r.instrument.exchange} · {r.style.label} ({r.timeframe})",
        f"💰 {sign}{f(r.price)}{change}",
        f"🕒 {_when(r.as_of, daily_bars)} · {r.status} · {r.source}",
        "",
        f"{_BIAS_ICON[r.bias]} Bias: {r.bias.value.upper()} (score {r.bias_score:+d}/{len(r.bias_reasons)})",
        *[f"   {reason}" for reason in r.bias_reasons],
    ]
    for title, lines in r.context:
        out += ["", title, *[f"   • {line}" for line in lines]]

    out += ["", "📍 Key Levels  (★ = confluence strength)"]
    out += [f"   🔺 {_ladder(z, f, compact)}" for z in reversed(r.resistance)]
    here = f"  ← at {' + '.join(r.at_price[0].labels)}" if r.at_price else ""
    out.append(f"   ▶  {f(r.price)}  LTP{here}")
    out += [f"   🔻 {_ladder(z, f, compact)}" for z in r.support]
    if r.pivots:
        out.append("   Pivots: " + " · ".join(f"{name} {f(value)}" for name, value in r.pivots.items()))

    if r.buy_side or r.sell_side or r.sweeps:
        out += ["", "💧 Liquidity"]
        if r.buy_side:
            out.append("   Buy-side (stops above highs):  " + " · ".join(f"{f(p.price)} {p.label}" for p in r.buy_side))
        if r.sell_side:
            out.append("   Sell-side (stops below lows):  " + " · ".join(f"{f(p.price)} {p.label}" for p in r.sell_side))
        for s in r.sweeps:
            where, read = ("above", "bearish") if s.side == "buy" else ("below", "bullish")
            out.append(
                f"   ⚡ {_when(s.time, daily_bars)}: {s.side}-side swept {where} {f(s.price)} ({s.label}),"
                f" closed back → {read} sign"
            )

    if r.setups:
        out += ["", "🎯 Trigger Points"]
        for s in r.setups:
            tag = "✅ PRIMARY · " if s.primary else ""
            icon = "🟢" if s.direction == "long" else "🔴"
            targets = " · ".join(f"T{i} {f(t)}" for i, t in enumerate(s.targets, 1))
            out += [
                f"   {tag}{icon} {s.name}",
                f"      When:  {s.trigger}",
                f"      Entry {f(s.entry)} · SL {f(s.stop)} · R:R 1:{s.reward_risk:.1f}",
                f"      Targets {targets}",
            ]
            if s.note:
                out.append(f"      ⚠ {s.note}")
        if r.wait_zone:
            low, high = r.wait_zone
            out.append(f"   ⏸ Wait zone {f(low)} – {f(high)}: no trade inside, let price pick a side")

    if r.notes:
        out += ["", "📝 Notes", *[f"   • {note}" for note in r.notes]]
    out += ["", DISCLAIMER, rule]
    return "\n".join(out)


def stars(z: Zone) -> int:
    """Confluence strength on a 1–5 scale."""
    return min(5, (z.weight + 1) // 2)


def _ladder(z: Zone, f: Fmt, compact: bool) -> str:
    marks = "★" * stars(z)
    if compact:
        return f"{fmt.zone_price(z, f)}  {marks}  {' + '.join(z.labels)}"
    return f"{fmt.zone_price(z, f):<24}{marks:<6}{' + '.join(z.labels)}"


def _when(ts: pd.Timestamp, date_only: bool) -> str:
    local = ts.tz_convert(IST)
    return f"{local:%d %b %Y}" if date_only else f"{local:%d %b %Y, %H:%M} IST"
