"""Web dashboard: a JSON API over the same engine, the static page, and the Telegram link flow."""

from __future__ import annotations

import asyncio
import logging
import secrets
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from telegram.error import Forbidden, InvalidToken, TelegramError

from ...config import Settings, load_settings
from ...data import DataError
from ...engine import analyze_cached
from ...models import Market, Style
from ...report import render
from ...serialize import report_to_dict
from ...store import LINK_TTL, Store
from ..telegram_bot import MAX_SYMBOL, QUICK_SYMBOLS, start_bot

STATIC = Path(__file__).parent / "static"
COOKIE = "abd_uid"
MARKET_LABELS = [(Market.STOCKS, "Indian stocks"), (Market.CRYPTO, "Crypto"), (Market.FOREX, "Forex & gold")]
log = logging.getLogger("abd.web")


class PlanRequest(BaseModel):
    style: Style
    market: Market
    symbol: str = Field(min_length=1, max_length=MAX_SYMBOL)


def create_app(settings: Settings | None = None, store: Store | None = None, start_telegram: bool = True) -> FastAPI:
    settings = settings or load_settings()
    store = store or Store(settings.db_path)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if start_telegram and settings.telegram_token:
            try:
                app.state.telegram = await start_bot(settings.telegram_token, store, settings.dashboard_url)
                log.info("Telegram bot @%s is listening", app.state.telegram.username)
            except InvalidToken:
                app.state.telegram_error = "Bot token galat hai. .env mein TELEGRAM_BOT_TOKEN BotFather se dobara copy karo."
            except TelegramError as exc:  # network down, Telegram unreachable, ...
                app.state.telegram_error = (
                    f"Telegram se connect nahi ho paya ({type(exc).__name__}). Internet check karke dashboard dobara chalao."
                )
            if app.state.telegram_error:
                log.warning("Telegram bot not started: %s", app.state.telegram_error)
        yield
        if app.state.telegram is not None:
            await app.state.telegram.stop()

    app = FastAPI(title="ABD Analyzer", lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)
    app.state.store = store
    app.state.telegram = None  # a RunningBot once polling
    app.state.telegram_error = None
    app.mount("/static", StaticFiles(directory=STATIC), name="static")

    def browser_id(request: Request, response: Response) -> str:
        """Each browser gets a random id cookie; that's what a Telegram chat is linked to (no login yet)."""
        uid = request.cookies.get(COOKIE, "")
        if not 16 <= len(uid) <= 64:
            uid = secrets.token_urlsafe(16)
            response.set_cookie(COOKIE, uid, max_age=365 * 86400, httponly=True, samesite="lax")
        return uid

    def from_dashboard(x_abd: str | None = Header(default=None)) -> None:
        # Another site can't add a custom header to a cross-origin request without CORS, which this app
        # never grants — so this header is the CSRF guard for the cookie-identified POSTs.
        if x_abd != "1":
            raise HTTPException(403, "Ye request dashboard se nahi aayi.")

    def telegram_state() -> dict:
        bot = app.state.telegram
        return {
            "configured": settings.telegram_token is not None,
            "running": bot is not None,
            "bot_username": bot.username if bot else None,
            "error": app.state.telegram_error,
        }

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(STATIC / "index.html")

    @app.get("/api/meta")
    def meta() -> dict:
        return {
            "styles": [{"value": s.value, "label": s.label} for s in Style],
            "markets": [{"value": m.value, "label": label} for m, label in MARKET_LABELS],
            "quick_symbols": {m.value: symbols for m, symbols in QUICK_SYMBOLS.items()},
        }

    @app.get("/api/plan")
    async def plan(style: Style, market: Market, symbol: str = Query(min_length=1, max_length=MAX_SYMBOL)) -> dict:
        try:
            report = await asyncio.to_thread(analyze_cached, style, market, symbol.strip())
        except DataError as exc:
            raise HTTPException(400, str(exc)) from exc
        return report_to_dict(report)

    @app.get("/api/telegram")
    def telegram_status(uid: str = Depends(browser_id)) -> dict:
        link = store.link_for(uid)
        return {**telegram_state(), "linked": link is not None, "chat_name": link.chat_name if link else None}

    @app.post("/api/telegram/link", dependencies=[Depends(from_dashboard)])
    def telegram_link(uid: str = Depends(browser_id)) -> dict:
        bot = app.state.telegram
        if bot is None:
            raise HTTPException(503, "Telegram bot abhi chal nahi raha. Setup ke steps dekho.")
        token = store.new_link_token(uid)
        return {"url": f"https://t.me/{bot.username}?start={token}", "expires_in": LINK_TTL}

    @app.post("/api/telegram/unlink", dependencies=[Depends(from_dashboard)])
    def telegram_unlink(uid: str = Depends(browser_id)) -> dict:
        store.unlink_user(uid)
        return {"linked": False}

    @app.post("/api/telegram/send", dependencies=[Depends(from_dashboard)])
    async def telegram_send(req: PlanRequest, uid: str = Depends(browser_id)) -> dict:
        bot, link = app.state.telegram, store.link_for(uid)
        if bot is None or link is None:
            raise HTTPException(409, "Pehle Telegram connect karo.")
        try:
            report = await asyncio.to_thread(analyze_cached, req.style, req.market, req.symbol.strip())
        except DataError as exc:
            raise HTTPException(400, str(exc)) from exc
        try:
            await bot.send(link.chat_id, render(report, compact=True))
        except Forbidden as exc:  # the user blocked or deleted the bot
            store.unlink_user(uid)
            raise HTTPException(409, "Bot Telegram mein block hai. Unblock karke dobara connect karo.") from exc
        except TelegramError as exc:
            raise HTTPException(502, f"Telegram par nahi bhej paya ({type(exc).__name__}). Thodi der baad try karo.") from exc
        return {"sent": True, "chat_name": link.chat_name}

    return app
