"""Telegram bot: the same three questions as the CLI and dashboard, asked with buttons.

`/start <token>` links this chat to a dashboard browser — the dashboard's "Connect" button hands out
that link — so plans can be sent here from the web.
"""

from __future__ import annotations

import asyncio
import logging
import time

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest, TelegramError
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

from ..data import DataError
from ..engine import analyze_cached
from ..models import Market, Style
from ..report import render
from ..store import Store

log = logging.getLogger("abd.telegram")

MESSAGE_LIMIT = 4000  # Telegram allows 4096 characters per message; keep a margin
COOLDOWN = 3.0  # seconds between plans per chat, so one chat can't hammer the data sources
MAX_SYMBOL = 30

STYLE_QUESTION = "Aap kis type ke trader ho?"
MARKET_QUESTION = "Kis market mein trade karna hai?"
SYMBOL_PROMPT = "Symbol chuno, ya type karo"
STYLES = [(Style.INTRADAY, "⚡ Intraday"), (Style.SWING, "📈 Swing"), (Style.LONG_TERM, "🏦 Long-term")]
MARKETS = [(Market.STOCKS, "🇮🇳 Indian Stocks"), (Market.CRYPTO, "₿ Crypto"), (Market.FOREX, "💱 Forex / Gold")]
QUICK_SYMBOLS = {
    Market.STOCKS: ["NIFTY", "BANKNIFTY", "RELIANCE", "HDFCBANK", "TCS", "SBIN"],
    Market.CRYPTO: ["BTC", "ETH", "SOL", "XRP", "BNB", "DOGE"],
    Market.FOREX: ["EURUSD", "GBPUSD", "USDJPY", "USDINR", "GOLD", "SILVER"],
}
COMMANDS = [
    BotCommand("menu", "Naya plan banao"),
    BotCommand("help", "Bot kaise use karein"),
    BotCommand("unlink", "Dashboard se link hatao"),
]
HELP = (
    "ABD Analyzer Bot\n\n"
    "/menu  naya plan: trader type → market → symbol\n"
    "/unlink  dashboard se link hatao\n"
    "/help  ye message\n\n"
    "Market chunne ke baad koi bhi symbol type kar sakte ho, jaise TCS, ETH ya GBPJPY."
)


# --- pure helpers (tested without Telegram) -------------------------------------------------


def parse_callback(data: str) -> tuple[str, Style | None, Market | None, str | None]:
    """'an:intraday:stocks:TCS' → ('an', Style.INTRADAY, Market.STOCKS, 'TCS'); anything malformed → 'menu'."""
    kind, _, rest = data.partition(":")
    parts = rest.split(":", 2) if rest else []
    need = {"st": 1, "mk": 2, "an": 3}.get(kind)
    if need is None or len(parts) != need:
        return "menu", None, None, None
    try:
        style = Style(parts[0])
        market = Market(parts[1]) if need >= 2 else None
    except ValueError:
        return "menu", None, None, None
    return kind, style, market, parts[2] if need == 3 else None


def style_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=f"st:{s.value}") for s, label in STYLES]])


def market_keyboard(style: Style) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(label, callback_data=f"mk:{style.value}:{m.value}")] for m, label in MARKETS]
    rows.append([InlineKeyboardButton("⬅️ Wapas", callback_data="menu")])
    return InlineKeyboardMarkup(rows)


def symbol_keyboard(style: Style, market: Market) -> InlineKeyboardMarkup:
    symbols = QUICK_SYMBOLS[market]
    rows = [
        [InlineKeyboardButton(sym, callback_data=f"an:{style.value}:{market.value}:{sym}") for sym in symbols[i : i + 3]]
        for i in range(0, len(symbols), 3)
    ]
    rows.append([InlineKeyboardButton("⬅️ Wapas", callback_data=f"st:{style.value}")])
    return InlineKeyboardMarkup(rows)


def report_keyboard(style: Style, market: Market, symbol: str, dashboard_url: str | None) -> InlineKeyboardMarkup:
    row = [
        InlineKeyboardButton("🔎 Naya symbol", callback_data=f"mk:{style.value}:{market.value}"),
        InlineKeyboardButton("🏠 Menu", callback_data="menu"),
    ]
    refresh = f"an:{style.value}:{market.value}:{symbol}"
    if len(refresh.encode()) <= 64:  # Telegram's limit for button data; odd typed symbols can exceed it
        row.insert(0, InlineKeyboardButton("🔄 Refresh", callback_data=refresh))
    rows = [row]
    if dashboard_url:  # Telegram rejects localhost URLs, so only a public address gets a button
        rows.append([InlineKeyboardButton("🌐 Dashboard kholo", url=dashboard_url)])
    return InlineKeyboardMarkup(rows)


def symbol_prompt(market: Market) -> str:
    return f"{SYMBOL_PROMPT} (jaise {', '.join(QUICK_SYMBOLS[market][:3])}):"


def start_reply(store: Store, payload: str | None, chat_id: int, chat_name: str) -> str:
    if payload:
        if store.redeem(payload, chat_id, chat_name):
            return f"✅ Dashboard se link ho gaya! Ab dashboard se plan seedha yahan aa sakta hai.\n\n{STYLE_QUESTION}"
        return (
            "⚠️ Ye link expire ho gaya ya pehle use ho chuka hai. Dashboard par Telegram connect karo "
            f"dabakar naya link lo.\n\n{STYLE_QUESTION}"
        )
    return f"Namaste 👋 Ye ABD Analyzer Bot hai: levels, liquidity aur trigger points, ek jagah.\n\n{STYLE_QUESTION}"


def split_message(text: str, limit: int = MESSAGE_LIMIT) -> list[str]:
    chunks, current = [], ""
    for line in text.splitlines(keepends=True):
        if current and len(current) + len(line) > limit:
            chunks.append(current)
            current = ""
        current += line
    if current:
        chunks.append(current)
    return chunks


def _is_wizard_step(text: str) -> bool:
    return text.endswith(STYLE_QUESTION) or text == MARKET_QUESTION or text.startswith(SYMBOL_PROMPT)


def _chat_name(update: Update) -> str:
    user = update.effective_user
    if user and user.username:
        return f"@{user.username}"
    if user:
        return user.full_name
    return update.effective_chat.title or str(update.effective_chat.id)


# --- handlers -------------------------------------------------------------------------------


async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    payload = context.args[0] if context.args else None
    text = start_reply(context.bot_data["store"], payload, update.effective_chat.id, _chat_name(update))
    await update.effective_message.reply_text(text, reply_markup=style_keyboard())


async def on_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(STYLE_QUESTION, reply_markup=style_keyboard())


async def on_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(HELP)


async def on_unlink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    removed = context.bot_data["store"].unlink_chat(update.effective_chat.id)
    await update.effective_message.reply_text(
        "Dashboard se link hata diya." if removed else "Ye chat kisi dashboard se linked nahi hai."
    )


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    kind, style, market, symbol = parse_callback(query.data or "")
    if kind == "an":
        await send_plan(context, query.message.chat_id, style, market, symbol)
        return
    if kind == "st":
        text, markup = MARKET_QUESTION, market_keyboard(style)
    elif kind == "mk":
        context.user_data["pending"] = (style.value, market.value)  # a typed symbol now means this pair
        text, markup = symbol_prompt(market), symbol_keyboard(style, market)
    else:
        text, markup = STYLE_QUESTION, style_keyboard()
    # Step through the wizard in place, but never overwrite a plan that has already been sent.
    if _is_wizard_step(query.message.text or ""):
        try:
            await query.edit_message_text(text, reply_markup=markup)
        except BadRequest as exc:
            if "not modified" not in str(exc):
                raise
    else:
        await query.message.reply_text(text, reply_markup=markup)


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pending = context.user_data.get("pending")
    symbol = (update.effective_message.text or "").strip()
    if not pending:
        await update.effective_message.reply_text(f"Pehle trader type chuno 👇\n\n{STYLE_QUESTION}", reply_markup=style_keyboard())
        return
    if len(symbol) > MAX_SYMBOL:
        await update.effective_message.reply_text("Symbol chhota likho, jaise TCS, BTC ya EURUSD.")
        return
    await send_plan(context, update.effective_chat.id, Style(pending[0]), Market(pending[1]), symbol)


async def send_plan(context: ContextTypes.DEFAULT_TYPE, chat_id: int, style: Style, market: Market, symbol: str) -> None:
    now = time.monotonic()
    if now - context.chat_data.get("last_plan_at", 0.0) < COOLDOWN:
        await context.bot.send_message(chat_id, "⏳ Thoda ruko, har 3 second mein ek plan banta hai.")
        return
    context.chat_data["last_plan_at"] = now
    waiting = await context.bot.send_message(chat_id, f"⏳ {symbol.upper()} ka {style.label} plan ban raha hai...")
    try:
        # the engine blocks on network I/O; off the event loop so the dashboard stays responsive
        report = await asyncio.to_thread(analyze_cached, style, market, symbol)
    except DataError as exc:
        await waiting.edit_text(f"❌ {exc}")
        return
    chunks = split_message(render(report, compact=True))
    await waiting.delete()
    keyboard = report_keyboard(style, market, symbol.upper(), context.bot_data.get("dashboard_url"))
    for i, chunk in enumerate(chunks):
        await context.bot.send_message(chat_id, chunk, reply_markup=keyboard if i == len(chunks) - 1 else None)


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.error("Telegram handler failed", exc_info=context.error)
    if isinstance(update, Update) and update.effective_chat:
        await context.bot.send_message(update.effective_chat.id, "⚠️ Kuch gadbad ho gayi. /menu se dobara try karo.")


# --- running ----------------------------------------------------------------------------------


def build_application(token: str, store: Store, dashboard_url: str | None = None) -> Application:
    app = Application.builder().token(token).build()
    app.bot_data.update(store=store, dashboard_url=dashboard_url)
    app.add_handler(CommandHandler("start", on_start))
    app.add_handler(CommandHandler(["menu", "plan"], on_menu))
    app.add_handler(CommandHandler("help", on_help))
    app.add_handler(CommandHandler("unlink", on_unlink))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(on_error)
    return app


async def _register_commands(app: Application) -> None:
    try:
        await app.bot.set_my_commands(COMMANDS)
    except TelegramError as exc:  # the menu is a nicety; the bot works without it
        log.warning("Could not set bot commands: %s", exc)


class RunningBot:
    """The bot polling inside the web server's event loop; the dashboard sends through it."""

    def __init__(self, app: Application):
        self._app = app

    @property
    def username(self) -> str:
        return self._app.bot.username

    async def send(self, chat_id: int, text: str) -> None:
        for chunk in split_message(text):
            await self._app.bot.send_message(chat_id, chunk)

    async def stop(self) -> None:
        await self._app.updater.stop()
        await self._app.stop()
        await self._app.shutdown()


async def start_bot(token: str, store: Store, dashboard_url: str | None = None) -> RunningBot:
    app = build_application(token, store, dashboard_url)
    await app.initialize()  # calls getMe, so a wrong token fails here
    await _register_commands(app)
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    return RunningBot(app)


def run_forever(token: str, store: Store, dashboard_url: str | None = None) -> None:
    """The bot on its own, without the dashboard (e.g. on a small always-on server). Stops on Ctrl+C."""

    async def main() -> None:
        bot = await start_bot(token, store, dashboard_url)  # same start-up path as the dashboard uses
        try:
            await asyncio.Event().wait()
        finally:
            await bot.stop()

    asyncio.run(main())
