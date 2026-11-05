"""Terminal version of the bot's conversation: trader type → market → symbol → plan.

Also the launcher: `web` starts the dashboard (plus the Telegram bot), `bot` runs the bot alone.
"""

from __future__ import annotations

import argparse
import logging

from ..data import DataError
from ..engine import analyze
from ..models import Market, Style
from ..report import render

BANNER = """
╔══════════════════════════════════════╗
║        ABD Analyzer Bot  v0.1        ║
║   Stocks (NSE) · Crypto · Forex      ║
╚══════════════════════════════════════╝"""

STYLES = [
    (Style.INTRADAY, "Intraday trader      (aaj ke levels, ORB, VWAP, triggers)"),
    (Style.SWING, "Swing trader         (kuch din se hafte — daily chart)"),
    (Style.LONG_TERM, "Long-term investor   (mahine se saal — weekly chart)"),
]
MARKETS = [
    (Market.STOCKS, "Indian Stocks / Index (NSE)"),
    (Market.CRYPTO, "Crypto"),
    (Market.FOREX, "Forex / Gold"),
]
EXAMPLES = {
    Market.STOCKS: "NIFTY, BANKNIFTY, RELIANCE, HDFCBANK, TCS, SBIN",
    Market.CRYPTO: "BTC, ETH, SOL, XRP, BNB",
    Market.FOREX: "EURUSD, GBPUSD, USDJPY, USDINR, GOLD",
}


def choose(question: str, options: list) -> object:
    print(f"\n{question}")
    for i, (_, label) in enumerate(options, 1):
        print(f"  {i}) {label}")
    while True:
        raw = input("👉 Number chuno: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1][0]
        print(f"  ⚠ 1 se {len(options)} ke beech ka number likho")


def run_once(style: Style, market: Market, symbol: str) -> bool:
    print(f"\n⏳ {symbol.upper()} ka {style.label} analysis ho raha hai...")
    try:
        report = analyze(style, market, symbol)
    except DataError as exc:
        print(f"❌ {exc}")
        return False
    print(render(report))
    return True


def wizard() -> None:
    print(BANNER)
    style = choose("Aap kis type ke trader ho?", STYLES)
    market = choose("Kis market mein trade karna hai?", MARKETS)
    while True:
        print(f"\nSymbol batao — jaise {EXAMPLES[market]}")
        symbol = input("👉 Symbol ('m' = menu, 'q' = exit): ").strip()
        if symbol.lower() in {"q", "quit", "exit"}:
            print("Bye 👋")
            return
        if symbol.lower() == "m":
            style = choose("Aap kis type ke trader ho?", STYLES)
            market = choose("Kis market mein trade karna hai?", MARKETS)
            continue
        if symbol:
            run_once(style, market, symbol)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="abd-bot", description="ABD Analyzer Bot — intraday / swing / long-term levels for NSE, crypto and forex"
    )
    parser.add_argument("--style", choices=[s.value for s in Style], help="intraday | swing | longterm")
    parser.add_argument("--market", choices=[m.value for m in Market], help="stocks | crypto | forex")
    parser.add_argument("--symbol", "-s", help="e.g. RELIANCE, NIFTY, BTC, EURUSD")
    commands = parser.add_subparsers(dest="command", metavar="{web,bot}")
    web = commands.add_parser("web", help="dashboard kholo (.env mein token ho to Telegram bot bhi)")
    web.add_argument("--host", default="127.0.0.1", help="0.0.0.0 = same WiFi ke phone se bhi khulega")
    web.add_argument("--port", type=int, default=8000)
    web.add_argument("--no-telegram", action="store_true", help="Telegram bot start mat karo")
    commands.add_parser("bot", help="sirf Telegram bot, dashboard ke bina")
    args = parser.parse_args(argv)

    if args.command == "web":
        return serve_web(args.host, args.port, telegram=not args.no_telegram)
    if args.command == "bot":
        return run_bot()
    if args.style or args.market or args.symbol:
        if not (args.style and args.market and args.symbol):
            parser.error("--style, --market aur --symbol teeno do (ya kuch mat do, wizard khulega)")
        return 0 if run_once(Style(args.style), Market(args.market), args.symbol) else 1
    try:
        wizard()
    except (KeyboardInterrupt, EOFError):
        print("\nBye 👋")
    return 0


def serve_web(host: str, port: int, telegram: bool) -> int:
    import uvicorn

    from .web.app import create_app

    _configure_logging()
    shown = "localhost" if host in ("127.0.0.1", "0.0.0.0") else host
    print(f"🌐 Dashboard: http://{shown}:{port}   (band karne ke liye Ctrl+C)")
    uvicorn.run(create_app(start_telegram=telegram), host=host, port=port, log_level="warning")
    return 0


def run_bot() -> int:
    from telegram.error import InvalidToken

    from ..config import load_settings
    from ..store import Store
    from .telegram_bot import run_forever

    settings = load_settings()
    if not settings.telegram_token:
        print("❌ .env mein TELEGRAM_BOT_TOKEN nahi mila — README ka 'Telegram bot' section dekho.")
        return 1
    _configure_logging()
    print("🤖 Telegram bot start ho raha hai   (band karne ke liye Ctrl+C)")
    try:
        run_forever(settings.telegram_token, Store(settings.db_path), settings.dashboard_url)
    except InvalidToken:
        print("❌ Bot token galat hai — BotFather se dobara copy karke .env mein daalo.")
        return 1
    except KeyboardInterrupt:
        print("\nBot band ho gaya 👋")
    return 0


def _configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    logging.getLogger("httpx").setLevel(logging.WARNING)  # its INFO lines put the bot token (in the URL) on screen
