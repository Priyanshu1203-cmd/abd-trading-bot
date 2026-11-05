# ABD Analyzer Bot

Personal-use market analysis bot for NSE stocks and indices, crypto and forex, with intraday, swing and long-term plans. `README.md` has the run commands, code structure and roadmap.

## Working with the user

- Reply in Hinglish: Hindi in Roman script (not Devanagari), with code, commands and trading terms in English.
- The user is a trader, not a programmer, and wants Claude to write all the code. Explain in plain terms.
- As of 2026-11-06 the project is in a discussion phase: the user said not to write more code for now. Don't change code until they ask.

## Decisions

- Personal use only (the user and a small group), not a public product. Login, subscriptions and public hosting are out of scope.
- SEBI Research Analyst rules don't bind personal use, but they return if plans are ever shared for money or made public.
- Order execution through a broker API falls under SEBI's retail algo rules even for personal use, and offshore forex brokers are illegal for Indian residents under FEMA. The bot stays analysis-first with if-then scenarios and a disclaimer; execution comes last, after paper trading.
- The GitHub repo is public so it clones without login, which makes anything committed public. Secrets such as the Telegram token and broker keys stay in `.env`, which git ignores.

## Current state

- Built: engine, terminal wizard, web dashboard, Telegram bot, and a dashboard flow that links a Telegram chat. 43 offline tests.
- The Telegram bot has never run with a real token. The user has to create one with @BotFather and put it in `.env`.
- There is no backtesting yet, so levels and triggers are unproven rules. Say so when discussing accuracy.
- Research from 2026-11-05: start with `reports/AI trading tools aur data timing.md`; the underlying notes are in `research_notes/AI trading tools aur data timing/`. Its plan is to fix data definitions first, then build a leak-free backtest with Indian costs and random baselines, then calibrated hit-rates and a shadow journal. New data comes after that, and LLM or ML last and only if useful.

## Inputs still needed from the user

- Exact trading rules: timeframe, opening-range minutes, entry, stop-loss and target rules, and what "algos" and buying/selling liquidity mean to them. These are currently guessed as Smart Money Concepts style stop pools and sweeps. Examples of real past trades are the easiest way to get them.
- What they trade: watchlist, cash or F&O, crypto exchange, forex pairs and platform.
- Broker for live NSE data, and the monthly data budget.
- Daily workflow: report times, alert types, how many people use it, laptop or always-on server.
- Feedback from using the dashboard during market hours.

## Known issues from the research (not fixed)

- NSE changed its close on 3 Aug 2026, according to secondary sources, so verify against the circulars. F&O stocks stop continuous trading at 15:15 and their official close comes from a closing auction, and the timings move again on 7 Dec 2026. `abd_bot/analysis/session.py` still treats 15:30 as the end of trading, so it shows LIVE during the auction, and `abd_bot/data/yahoo.py` can fill a blank daily close from the last 5m bar. Previous-day close, CPR and pivots can therefore be off.
- Yahoo's completed-day forex Close sits about one day behind: on EURUSD it is within 2 pips of that day's Open on about 45 of 50 days, and a median 18 pips from the day's last intraday close. Forex PDC, CPR and pivots are wrong as a result, while high and low are roughly fine.
- Forex previous-day levels also depend on the feed's day boundary, so they can differ from a broker's chart.
- Gold uses COMEX futures (`GC=F`), which are not spot XAU/USD, and Yahoo lists COMEX as 30 minutes delayed (about 10 minutes in one reading). Yahoo's daily rows follow the CME session while the bot uses the New York calendar day, so for about 6 hours a day its previous day is one session old.
- Signals, sweeps and the "closed above" text use the still-forming last candle, so they can fire before that candle closes.
- Swing points need future bars to confirm, so look-ahead has to be removed before any backtest.
- Sweep logic needs a random-level baseline. The tests found so far are not peer-reviewed and show no edge.
