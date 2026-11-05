from abd_bot.interfaces import telegram_bot as tg
from abd_bot.models import Market, Style
from abd_bot.store import Store


def test_parse_callback():
    assert tg.parse_callback("an:intraday:stocks:TCS") == ("an", Style.INTRADAY, Market.STOCKS, "TCS")
    assert tg.parse_callback("an:swing:crypto:BTC:USDT") == ("an", Style.SWING, Market.CRYPTO, "BTC:USDT")
    assert tg.parse_callback("mk:longterm:forex") == ("mk", Style.LONG_TERM, Market.FOREX, None)
    for broken in ("st:weekly", "an:intraday:stocks", "mk:intraday", "zz:1", "", "menu"):
        assert tg.parse_callback(broken)[0] == "menu"


def test_every_button_fits_telegram_limits():
    keyboards = [tg.style_keyboard()]
    for style in Style:
        keyboards.append(tg.market_keyboard(style))
        for market in Market:
            keyboards.append(tg.symbol_keyboard(style, market))
            keyboards.append(tg.report_keyboard(style, market, "X" * tg.MAX_SYMBOL, None))
            keyboards.append(tg.report_keyboard(style, market, "स" * tg.MAX_SYMBOL, None))  # 3 bytes per char
    for keyboard in keyboards:
        for row in keyboard.inline_keyboard:
            for button in row:
                assert button.callback_data is None or len(button.callback_data.encode()) <= 64


def test_start_with_token_links_the_chat(tmp_path):
    store = Store(tmp_path / "abd.sqlite3")
    token = store.new_link_token("browser-1")
    assert "link ho gaya" in tg.start_reply(store, token, 5, "@me")
    assert store.link_for("browser-1").chat_id == 5
    assert "expire" in tg.start_reply(store, token, 5, "@me")  # second use
    assert tg.start_reply(store, None, 5, "@me").startswith("Namaste")


def test_split_message_keeps_every_line():
    text = "\n".join(f"line {i} " + "x" * 50 for i in range(200))
    chunks = tg.split_message(text, limit=500)
    assert all(len(chunk) <= 500 for chunk in chunks)
    assert "".join(chunks) == text
