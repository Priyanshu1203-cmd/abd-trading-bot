"""SQLite store for the dashboard ↔ Telegram link: one-time link tokens and linked chats."""

from __future__ import annotations

import secrets
import sqlite3
import threading
import time
from dataclasses import dataclass
from pathlib import Path

LINK_TTL = 600  # seconds a "connect Telegram" link stays valid


@dataclass(frozen=True)
class TelegramLink:
    chat_id: int
    chat_name: str


class Store:
    def __init__(self, path: Path | str):
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(path), check_same_thread=False)
        self._lock = threading.Lock()  # the web threads and the bot's event loop share one connection
        with self._lock, self._db:
            self._db.executescript(
                """
                CREATE TABLE IF NOT EXISTS link_tokens (
                    token      TEXT PRIMARY KEY,
                    user_id    TEXT NOT NULL,
                    expires_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS telegram_links (
                    user_id   TEXT PRIMARY KEY,  -- the dashboard browser
                    chat_id   INTEGER NOT NULL,  -- several browsers may share one chat
                    chat_name TEXT NOT NULL,
                    linked_at REAL NOT NULL
                );
                CREATE INDEX IF NOT EXISTS telegram_links_chat ON telegram_links (chat_id);
                """
            )

    def new_link_token(self, user_id: str, ttl: float = LINK_TTL) -> str:
        """A fresh token replaces the user's earlier ones; expired tokens are swept on the way."""
        token = secrets.token_urlsafe(16)  # 22 chars, inside Telegram's 64-char /start payload limit
        now = time.time()
        with self._lock, self._db:
            self._db.execute("DELETE FROM link_tokens WHERE expires_at < ? OR user_id = ?", (now, user_id))
            self._db.execute("INSERT INTO link_tokens VALUES (?, ?, ?)", (token, user_id, now + ttl))
        return token

    def redeem(self, token: str, chat_id: int, chat_name: str) -> str | None:
        """Link the chat to the token's dashboard user. A token works once; returns the user, or None."""
        now = time.time()
        with self._lock, self._db:
            row = self._db.execute("SELECT user_id, expires_at FROM link_tokens WHERE token = ?", (token,)).fetchone()
            if row is None:
                return None
            self._db.execute("DELETE FROM link_tokens WHERE token = ?", (token,))
            user_id, expires_at = row
            if expires_at < now:
                return None
            self._db.execute(
                "INSERT OR REPLACE INTO telegram_links VALUES (?, ?, ?, ?)", (user_id, chat_id, chat_name, now)
            )
        return user_id

    def link_for(self, user_id: str) -> TelegramLink | None:
        with self._lock:
            row = self._db.execute(
                "SELECT chat_id, chat_name FROM telegram_links WHERE user_id = ?", (user_id,)
            ).fetchone()
        return TelegramLink(*row) if row else None

    def unlink_user(self, user_id: str) -> bool:
        with self._lock, self._db:
            return self._db.execute("DELETE FROM telegram_links WHERE user_id = ?", (user_id,)).rowcount > 0

    def unlink_chat(self, chat_id: int) -> bool:
        with self._lock, self._db:
            return self._db.execute("DELETE FROM telegram_links WHERE chat_id = ?", (chat_id,)).rowcount > 0
