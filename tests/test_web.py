"""Dashboard API with the engine and Telegram swapped for fakes: no network, no bot token."""

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from abd_bot.config import Settings
from abd_bot.data import DataError
from abd_bot.interfaces.web import app as web
from abd_bot.strategies import intraday

from .conftest import IST
from .test_strategies import NSE, nse_intraday

POST = {"X-ABD": "1"}


class FakeBot:
    username = "abd_test_bot"

    def __init__(self):
        self.sent: list[tuple[int, str]] = []

    async def send(self, chat_id: int, text: str) -> None:
        self.sent.append((chat_id, text))

    async def stop(self) -> None:
        pass


@pytest.fixture
def api(tmp_path, monkeypatch):
    now = pd.Timestamp("2026-11-04 12:00", tz=IST)
    report = intraday.analyze(NSE, nse_intraday(now), now)

    def fake_analyze(style, market, symbol):
        if symbol == "NOPE":
            raise DataError("'NOPE' ka data nahi mila")
        return report

    monkeypatch.setattr(web, "analyze_cached", fake_analyze)
    app = web.create_app(Settings(None, tmp_path / "abd.sqlite3", None), start_telegram=False)
    with TestClient(app) as client:
        yield client, app


def test_page_and_meta_are_served(api):
    client, _ = api
    assert "ABD Analyzer" in client.get("/").text
    assert client.get("/static/app.js").status_code == 200
    meta = client.get("/api/meta").json()
    assert [s["value"] for s in meta["styles"]] == ["intraday", "swing", "longterm"]
    assert "NIFTY" in meta["quick_symbols"]["stocks"]


def test_plan_is_chartable_json(api):
    client, _ = api
    data = client.get("/api/plan", params={"style": "intraday", "market": "stocks", "symbol": "TEST"}).json()
    assert data["instrument"]["name"] == "TEST" and data["live"] is True
    bar = data["candles"][-1]
    assert set(bar) == {"time", "open", "high", "low", "close", "volume"} and isinstance(bar["time"], int)
    assert data["setups"] and {s["verb"] for s in data["setups"]} <= {"Buy above", "Sell below", "Buy near", "Sell near"}
    assert data["wait_zone"]["low"] < data["price"] < data["wait_zone"]["high"]
    assert data["text"].startswith("━")


def test_plan_errors_read_like_the_bot(api):
    client, _ = api
    bad = client.get("/api/plan", params={"style": "intraday", "market": "stocks", "symbol": "NOPE"})
    assert bad.status_code == 400 and "NOPE" in bad.json()["detail"]
    assert client.get("/api/plan", params={"style": "weekly", "market": "stocks", "symbol": "X"}).status_code == 422


def test_connect_send_and_disconnect_telegram(api):
    client, app = api
    status = client.get("/api/telegram").json()
    assert status["configured"] is False and status["linked"] is False
    assert client.post("/api/telegram/link", headers=POST).status_code == 503  # no bot running yet

    app.state.telegram = bot = FakeBot()
    assert client.post("/api/telegram/link").status_code == 403  # missing header: CSRF guard
    url = client.post("/api/telegram/link", headers=POST).json()["url"]
    assert url.startswith("https://t.me/abd_test_bot?start=")
    assert app.state.store.redeem(url.split("start=")[1], 777, "@trader")  # what /start <token> does

    assert client.get("/api/telegram").json()["chat_name"] == "@trader"
    plan = {"style": "intraday", "market": "stocks", "symbol": "TEST"}
    sent = client.post("/api/telegram/send", headers=POST, json=plan)
    assert sent.status_code == 200 and bot.sent[0][0] == 777 and "TEST" in bot.sent[0][1]

    client.post("/api/telegram/unlink", headers=POST)
    assert client.get("/api/telegram").json()["linked"] is False
    assert client.post("/api/telegram/send", headers=POST, json=plan).status_code == 409
