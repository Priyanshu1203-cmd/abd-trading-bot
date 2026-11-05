"""Runtime settings: environment variables, optionally from a .env file in the project folder."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    telegram_token: str | None  # from @BotFather; without it the dashboard runs and Telegram stays off
    db_path: Path  # dashboard ↔ Telegram links
    dashboard_url: str | None  # public dashboard address, if any, for an "open dashboard" button in Telegram


def load_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env")
    return Settings(
        telegram_token=os.environ.get("TELEGRAM_BOT_TOKEN", "").strip() or None,
        db_path=Path(os.environ.get("ABD_DB_PATH", "") or PROJECT_ROOT / "data" / "abd.sqlite3"),
        dashboard_url=os.environ.get("DASHBOARD_URL", "").strip() or None,
    )
