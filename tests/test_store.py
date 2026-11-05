from abd_bot.store import Store, TelegramLink


def test_link_token_works_once(tmp_path):
    store = Store(tmp_path / "abd.sqlite3")
    token = store.new_link_token("browser-1")
    assert store.redeem(token, 42, "@trader") == "browser-1"
    assert store.link_for("browser-1") == TelegramLink(42, "@trader")
    assert store.redeem(token, 99, "@someone-else") is None
    assert store.link_for("browser-1") == TelegramLink(42, "@trader")


def test_expired_and_replaced_tokens_are_refused():
    store = Store(":memory:")
    assert store.redeem(store.new_link_token("late", ttl=-1), 7, "@late") is None
    first = store.new_link_token("browser-1")
    second = store.new_link_token("browser-1")  # asking again invalidates the earlier link
    assert store.redeem(first, 1, "@a") is None
    assert store.redeem(second, 1, "@a") == "browser-1"


def test_unlink_from_either_side():
    store = Store(":memory:")
    for browser in ("laptop", "phone"):  # two browsers may share one chat
        store.redeem(store.new_link_token(browser), 5, "@me")
    assert store.unlink_user("laptop") and store.link_for("phone") is not None
    assert store.unlink_chat(5) and store.link_for("phone") is None
    assert not store.unlink_user("laptop")
