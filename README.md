# ABD Analyzer Bot

Ek hi bot jo **Intraday / Swing / Long-term** — teeno type ke traders ke liye **Indian Stocks (NSE), Crypto aur Forex**
ka analysis deta hai: bias, key levels, CPR/pivots, opening range, VWAP, buy-side/sell-side liquidity, stop-hunt
(sweep) aur **trigger points** (entry, stop-loss, targets).

Teen jagah se use kar sakte ho, teeno ek hi engine par chalte hain:
**web dashboard** (chart ke saath), **Telegram bot** (buttons wala), aur **terminal**.

## Chalana kaise hai

```bash
./setup.sh                 # ek baar: ~/.venvs/abd-bot mein Python env + libraries
./run.sh web               # dashboard: http://localhost:8000 (+ Telegram bot, agar .env mein token hai)
./run.sh                   # terminal wizard: trader type → market → symbol → plan
./run.sh --style intraday --market stocks --symbol RELIANCE
./run.sh bot               # sirf Telegram bot, dashboard ke bina
./run.sh test              # saare tests
```

`setup.sh` venv ko project ke bahar (`~/.venvs/abd-bot`) banata hai, kyunki original folder ke naam mein `:` tha aur
Python aise path mein venv nahi banata. Same WiFi wale phone par dashboard kholna ho to `./run.sh web --host 0.0.0.0`
chalao aur phone mein `http://<laptop-ka-IP>:8000` kholo.

## Naye PC par

Git aur Python 3.10 ya naya chahiye (test Python 3.14 par hua hai). Repo private hai, isliye pehle GitHub login karo.

```bash
gh auth login
gh repo clone Priyanshu1203-cmd/abd-trading-bot
cd abd-trading-bot
./setup.sh
./run.sh test
./run.sh web
```

Windows par `.sh` scripts nahi chalte. Wahan ye chalao (ye tarika abhi test nahi hua hai):

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m abd_bot web
```

`.env` aur `data/` git mein nahi jaate, isliye naye PC par `.env` dobara banana hoga aur Telegram dobara connect karna hoga.

## Telegram bot jodna (ek baar)

1. Telegram mein **@BotFather** kholo → `/newbot` → bot ka naam aur username do → wo ek **token** dega.
2. `.env.example` ko copy karke `.env` banao aur token likho: `TELEGRAM_BOT_TOKEN=...` (`.env` git mein nahi jaati).
3. `./run.sh web` dobara chalao. Dashboard ke upar **Telegram connect karo** → **Connect link banao** →
   Telegram khulega → **Start** dabao. Dashboard apne aap "Connected" dikhayega.
4. Ab har plan ke neeche **Ye plan Telegram par bhejo** button aata hai. Bot mein khud bhi `/menu` se wahi
   3 sawaal buttons se poochhe jaate hain.

Link kaise kaam karta hai: dashboard har browser ko ek random id (cookie) deta hai. "Connect" ek one-time token
banata hai (10 minute valid) jo `t.me/<bot>?start=<token>` link mein jaata hai; Start dabane par bot us chat ko
us browser se jod deta hai (`data/abd.sqlite3`). Telegram mein `/unlink` ya dashboard par "Disconnect karo" se hatao.

## Structure (layers)

```
Dashboard (web) ─┐
Telegram bot ────┼──► engine.analyze() ──► data/ ──► analysis/ ──► strategies/ ──► Report
Terminal (CLI) ──┘          (60 sec cache)                                            │
                                                     report/text.py (Telegram/CLI) ◄──┤
                                                     serialize.py (dashboard JSON) ◄──┘
```

```
abd_bot/
├── engine.py            (style, market, symbol) → Report; analyze_cached() dashboard/bot ke liye
├── models.py            Style, Market, Level, Zone, Pool, Sweep, Setup, Report
├── config.py            .env settings: TELEGRAM_BOT_TOKEN, DASHBOARD_URL
├── store.py             SQLite: dashboard browser ↔ Telegram chat link, one-time tokens
├── serialize.py         Report → JSON (chart candles + levels + formatted text)
├── fmt.py               ₹ lakh-grouping, decimals per instrument
├── data/                yahoo.py (NSE + forex/gold) · crypto.py (Binance → Bybit → OKX)
├── analysis/            indicators, levels (CPR/pivots/ORB), structure, zones, liquidity, session
├── strategies/          intraday.py · positional.py (swing = daily, long-term = weekly) · common.py
├── report/text.py       Report → emoji text (terminal + Telegram)
└── interfaces/
    ├── cli.py           wizard + `web` / `bot` launchers
    ├── telegram_bot.py  buttons wala wizard, /start <token> linking, /unlink
    └── web/             app.py (FastAPI API) + static/ (dashboard page, chart)
tests/                   synthetic data par offline tests (engine, API, bot helpers, store)
research_notes/          AI tools, data timing aur accuracy par research (Nov 2026)
```

## Bot kya padhta hai

| Aapki language | Code mein |
|---|---|
| Chart candles | `structure.py`: swing highs/lows, HH/HL trend, break of structure |
| Morning opening | `intraday.py`: gap-up/down, gap fill, Opening Range 09:15–09:30 (ORB) |
| Algos | `liquidity.py`: equal highs/lows ke paas stop-hunt / sweep detection, round numbers |
| Buying / selling liquidity | Buy-side = highs ke upar stops · Sell-side = lows ke neeche stops |
| Trigger points | `common.breakout`: "15m close above X" → entry, SL, T1/T2, R:R |
| Support / breakdown | `zones.py`: sab levels ka confluence; breakdown = support zone ke neeche close |

| Style | Candles | Main levels | Trigger confirm |
|---|---|---|---|
| Intraday | 5m (NSE), 15m (crypto/FX) | PDH/PDL, CPR, pivots, ORB, VWAP, day high/low, PWH/PWL | 15m close |
| Swing | Daily (~2 saal) | S/R zones, EMA20/50, 200 DMA, PWH/PWL, PMH/PML, 52W | Daily close |
| Long-term | Weekly (~20 saal) | S/R zones, EMA10/40W, 200 WMA, ATH, 52W, PYH/PYL | Weekly close |

## Roadmap

| Phase | Kya | Status |
|---|---|---|
| 0 | Analysis engine + CLI wizard, free data, tests | ✅ |
| 1 | Web dashboard (chart + plan) + Telegram bot (buttons) + dashboard se Telegram linking | ✅ |
| 2 | Live data: broker API (Kite/SmartAPI/Upstox/Dhan), Binance websocket; trigger hit hone par Telegram alert; 9:00 AM morning report | next |
| 3 | Option chain (OI, PCR, max pain) for NIFTY/BANKNIFTY, FVG/order blocks, volume profile, NIFTY 50 scanner | |
| 4 | Backtesting: har rule ka win-rate / R:R proof | |
| 5 | Login wale user accounts, internet par hosting, subscriptions | Plan mein nahi: bot personal use ke liye hai |
| 6 | (Optional) Auto-execution: pehle paper trading, risk limits, kill switch | |

## Dhyaan rakhne wali baatein

- **Data**: Yahoo Finance free hai par intraday mein kuch minute late ho sakta hai — live NSE ke liye Phase 2 mein broker feed.
- **Abhi login nahi hai**: dashboard browser-cookie se pehchaanta hai, isliye ise apne laptop/WiFi tak rakho. Internet par
  public host karne se pehle Phase 5 wala login zaroori hai.
- **Compliance (India)**: public ko "yahan kharido/becho" levels dena SEBI Research Analyst rules ke daayre mein aata hai;
  Indian residents ke liye offshore forex brokers (non-INR pairs) FEMA ke khilaf hain; auto-trading par SEBI ke retail
  algo rules lagte hain. Bot ko public karne se pehle SEBI-compliance expert se confirm karna.
- Har report mein disclaimer hai: ye educational analysis hai, investment advice nahi.

## Naya rule kaise jodna hai

1. Calculation `analysis/` mein (pure function, OHLCV in → number/levels out) + `tests/` mein test.
2. Strategy mein `Level(price, "Label", weight)` add karo — confluence aur triggers apne aap update hote hain.
3. Bias mein chahiye to `common.py` mein ek `Vote` function. Dashboard aur Telegram dono ko naya rule apne aap milta hai.
