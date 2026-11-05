# Indian (NSE/BSE) AI, Analytics and Algo Tools: How They Work, Data Timing, Pricing, SEBI Status (research date 5 Nov 2026)

Source tags: [official] = the vendor's, regulator's or exchange's own page; [broker] = a broker's own notice or help page; [media] = news outlet; [competitor] = published by a rival product (AlgoTest, Strike, Tapetide and OptionX all sell competing tools, so their comparisons are self-interested); [secondary] = blog, aggregator or forum; [UNVERIFIED] = a single weak source, or sources that conflict. "Checked DD Mon YYYY" means the citing page says it verified the fact on that date. "Fetched 5 Nov 2026" means I loaded the page that day. Every price is in INR.

## 1. Options analytics (Sensibull, Opstra, Quantsapp and others): what they compute, from what data, how real-time, pricing

### Takeaway
Indian options tools compute the same core outputs: an option chain with OI and OI change, PCR, max pain ("option pain"), IV and IV charts, Greeks, OI build-up classification, and multi-leg strategy payoff. They build these from NSE/BSE F&O quotes that arrive through broker or vendor feeds. Where they differ is data freshness (live for paid or broker-linked users; 3–15 minutes or EOD on free tiers), backtesting depth, and broker lock-in. Sensibull is free for Zerodha clients, Opstra's terminal is for Definedge clients, and Dhan Options Trader is free for Dhan clients. Late-2026 list prices run from ₹0 (broker-funded) to about ₹800/month (Sensibull for other brokers) and ₹1,300/month plus GST (Opstra). Quantsapp quotes ₹3,250–₹8,000/month, and its figures conflict across sources.

### Cited Findings
#### Sensibull
- Sensibull's help page says it is "100% free for Zerodha users". Users of other brokers get a Free plan (basic option chain, verified P&L, daily market analysis, positions page) or a Pro plan (Easy Options, Strategy Builder, live options charts, open-interest analysis, IV chart). Prices are shown only in the user's profile "plans" tab. The article was last updated 23 Jul 2026 — [Sensibull help, official](https://sensibull.freshdesk.com/support/solutions/articles/43000586718-what-are-the-charges-of-sensibull-)
- Zerodha's free access is broker-funded and dates from a Zerodha announcement of 24 Jul 2023. For other brokers, the Sensibull homepage shows ₹800/month (1-month plan) and ₹640/month (6-month plan). Documented features are multi-leg construction, payoff diagrams, scenario analysis and Greeks. A Sensibull help article (modified 1 Jan 2024) says there is no historical backtesting and no options simulator. Whether the data is real-time or delayed was "not established". Checked 14 Oct 2026 — [OneTradeJournal comparison, secondary](https://onetradejournal.com/platforms/options-analytics-tools-compared)
- The Sensibull homepage says long-term paid plans are available only to Angel One, Upstox and Google users. Checked 14 Oct 2026 — [OneTradeJournal, secondary](https://onetradejournal.com/platforms/sensibull-free-with-which-broker)
- Older prices, likely outdated: Pro at ₹800 + 18% GST for 1 month and ₹3,840 + GST for 6 months (undated 5paisa help article) — [5paisa, broker](https://forum.5paisa.com/portal/en/kb/articles/what-are-the-subscription-and-brokerage-charges-for-sensibull); ₹1,300/month (undated) — [Fintrakk, secondary](https://app.fintrakk.com/article/is-sensibull-pro-worth-it-good-option-trading)
- AlgoTest's 2026 review describes a free plan with 8 features and Pro at ₹0/month with 25+ features for Zerodha users — [AlgoTest, competitor](https://algotest.in/blog/sensibull-review-2026-features-pricing-and-who-its-for/)

#### Opstra (Definedge)
- Pricing on the public analytics site is ₹1,300/month + 18% GST, ₹6,000 for 6 months + GST, and ₹11,000/year + GST (₹12,980 in total). A separate brokerage-linked terminal costs ₹799/month or ₹7,999/year. It is for Definedge demat holders only, and the fee comes back as a wallet credit usable against brokerage. Public pricing lists EOD IV and an EOD options backtest; live and intraday features are on paid tiers. Opstra describes free chain and dashboard data as updating every 15 minutes. Its FAQ describes 1-minute data with a calculation delay, and OI updating every 3 minutes. BSE F&O and MCX data are available only on the Definedge terminal. Checked 14 Oct 2026 — [OneTradeJournal, secondary](https://onetradejournal.com/platforms/options-analytics-tools-compared)
- A 2026 review lists the features as strategy builder and payoff, Greeks, IV and volatility-surface charts, OI analytics, an options simulator, and backtesting with data from 2016. Full Pro access needs a Definedge account, and the reviewer calls the UI dated — [Strike review, competitor](https://www.strike.money/reviews/definedge-opstra)

#### Quantsapp
- On its official page (fetched 5 Nov 2026; page undated), Basic is "free forever" with 28 tools. Pro costs ₹3,250/month and adds 53 premium analytics plus 1 option algorithm. Pro+ costs ₹6,500/month and adds 14 advanced tradeable analytics plus 33 order and trade-book analytics. The yearly option shows "save 20%", and subscriptions are non-refundable. Features listed:
  - live Greeks, OI, and OI build-up tools (Built-up Scrip, Built-up Breadth, Built-up Sector, Option Built Up)
  - "Option Pain" (max pain), PCR (Pro and Pro+), IV, and Price-OI Percentile (premium)
  - Strategy Builder with payoff (Strategy Chart is premium) and Options Architect
  - FNO Scanner, plus custom and real-time alerts
  - backtesting and a Strategy Optimizer (Pro and Pro+)
  - multi-broker execution (Aliceblue, Choice, Dhan, Fyers, Motilal, Nuvama, Upstox, Zerodha, 5paisa)

  "Real Time Data and Updates" is ticked for all three plans. Quantsapp calls itself "an analytics and decision-support platform, not a broker", and says its expert trade alerts are "Managed by SEBI RAs" — [Quantsapp, official](https://new.quantsapp.com/)
- Conflicting prices: PRO at ₹4,000/month or ₹19,999/year, and PRO+ at ₹8,000/month or ₹39,999/year, described by the provider as tax-inclusive. Checked 14 Oct 2026 — [OneTradeJournal, secondary](https://onetradejournal.com/platforms/options-analytics-tools-compared). An April 2024 page cited different tiers again — [Fintrakk, secondary](https://forum.fintrakk.com/t/is-quantsapp-options-analytics-platform-free-to-use-what-are-its-pricing-plans/1177)
- One low-quality review claims the free tier has 15-minute-delayed OI, and that real-time OI, flow, alerts (OI breakouts, PCR breaches, IV-percentile thresholds) and multi-expiry analysis need a ₹999/month Premium plan. This contradicts the official "real-time on all plans" claim — [bankniftyoptions review, secondary, UNVERIFIED](https://bankniftyoptions-com.pages.dev/artigos/quantsapp-banknifty-review)
- Quantsapp's video library explains its Price-OI Percentile logic: a price move backed by an OI increase has a better chance of sustaining when the price percentile is above 80 — [Quantsapp video library, official](https://web.quantsapp.com/video-library/price-oi-percentile/ILHCJH4L)

#### Others
- Dhan Options Trader has a strategy builder with current and expiry payoff lines, IV adjustment, strategy Greeks and saved-strategy comparison. All features cost ₹0 for Dhan users. Checked 14 Oct 2026 — [OneTradeJournal, secondary](https://onetradejournal.com/platforms/options-analytics-tools-compared). The app listing describes "Quant Mode" for multi-leg strategies, Greeks tuning, and backtesting on NIFTY, BANKNIFTY, FINNIFTY and SENSEX. Dhan's DEXT engine runs Iceberg+, Super Orders and Quant Mode — [App Store listing, official](https://apps.apple.com/us/app/id1601444691)
- Zerodha Kite's native option chain shows OI, IV measures and Greeks, with basket orders, margin and position tracking. It is not documented as a payoff builder. Checked 14 Oct 2026 — [OneTradeJournal, secondary](https://onetradejournal.com/platforms/options-analytics-tools-compared)
- AlgoTest claims more than 7.5 years of historical data for options backtesting. It covers Nifty, Bank Nifty, FinNifty, MidcapNifty, Sensex and Bankex, supports multi-leg structures (straddles, strangles, iron flies, condors), and lets users add slippage and brokerage — [AlgoTest vs Sensibull, vendor](https://algotest.in/blog/algotest-vs-sensibull.md); [AlgoTest backtesting roundup, vendor](https://algotest.in/blog/best-backtesting-software-for-options-trading-in-india/)
- NiftyTrader runs an options screener that filters F&O stocks by IV, OI and volume — [NiftyTrader](https://www.niftytrader.in/options-screener)

### Inferences
- All these tools take the same input: per-strike F&O quotes (LTP, bid/ask, volume, OI) from the exchange via a broker or vendor feed. The derived numbers are computed server-side. IV comes from inverting an option-pricing model, Greeks follow from it, PCR is put OI divided by call OI, and max pain is the strike where option writers pay out least. These are standard definitions; no tool documents its exact model.
- "Real-time" is not tick-level for OI: Opstra's own FAQ says OI updates every 3 minutes. For OI-based signals, a 1–3 minute refresh is the realistic best case even on paid tiers.
- What the bot lacks here: it has no option-chain input at all. So it has no OI or OI change, PCR, max pain, IV or IV percentile, Greeks, OI build-up classification, straddle or premium charts, multi-leg payoff or strategy builder, and no options backtesting.

### Gaps
- Sensibull's data source and latency are not documented anywhere I found.
- I could not confirm which tools offer IV Percentile (IVP) or IV Rank; the OneTradeJournal comparison says IVP was not documented for any tool it checked.
- A competitor comparison (data "as of February 2026") quoted Opstra at ₹999/month + GST with a 7-day trial. I could not pin that figure to a specific page, so I left it out.
- Quantsapp's price conflict (₹3,250 vs ₹4,000/month for Pro) is unresolved. ₹3,250 + 18% GST ≈ ₹3,835, so the official figure may exclude tax — that is an inference.
- I did not check SEBI registration status for Sensibull or Opstra/Definedge (Definedge Securities is described only as the execution broker).

## 2. Scanners and research (Chartink, StockEdge, Trendlyne, Screener.in, MarketsMojo, Tijori, others): working model, data timing, pricing

### Takeaway
These products fall into three groups:
- **Rule-based screeners**, where the user writes boolean conditions over indicators or fundamentals: Chartink, Screener.in's query screens, StockEdge scans, Trendlyne screeners.
- **Proprietary composite scores** with undisclosed weights: Trendlyne DVM, MarketsMojo's Mojo Score, Tickertape scorecards, Moneycontrol "MC Insights".
- **LLM add-ons arriving in 2025–26**: Screener AI credits, Trendlyne AI credits and an MCP connector, StockEdge "Stock AI", Chartink's plain-language-to-filter input.

Timing is mostly EOD or daily for scores and fundamentals. Trendlyne's StratQ uses 15-minute data. Chartink is about 5 minutes delayed free and near real-time (about 1 minute) on Premium. Annual prices range from about ₹1,500 to ₹12,000.

### Cited Findings
#### Chartink (rule-based technical scanner)
- Scans use a rule-based filter builder (for example, "Close > 500") with no scripting language. Technical and fundamental filters can be combined, and plain-language input is converted into filters (marketed as "AI-powered").
- **Free:** scans and charts delayed about 5 minutes, timeframes of 5 minutes or longer, no custom alerts.
- **Premium:** near-real-time 1-minute updates, 1/2/3-minute timeframes, SMS, email and webhook alerts, private scans and dashboards. Trades are executed through a third-party tool (AlgoTest), not Chartink.
- Prices: about ₹780/month or ₹8,500/year.

Review updated 14 Jan 2026 and revised 28 Apr 2026 — [Strike review, competitor](https://www.strike.money/reviews/chartink)
- Premium costs ₹780 for 30 days, ₹2,220 for 90 days or ₹8,500 for 365 days, inclusive of all taxes. It includes real-time scans, 1–3 minute timeframes, private scans and SMS/email/webhook alerts; the free tier is delayed. Checked 24 Oct 2026 — [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india). The same ₹780/₹2,220/₹8,500 figures appear in a check dated 14 Oct 2026 — [OneTradeJournal, secondary](https://onetradejournal.com/platforms/options-analytics-tools-compared)

#### StockEdge (Kredent; ready-made and custom scans)
- **Premium:** ₹399/month, or ₹1,499/year with a coupon (list price about ₹250/month). Includes 500+ ready-made scans, 20 combination scans, sector rotation, IPO analysis and CSV downloads.
- **Pro:** ₹1,499/month or ₹5,999/year. Adds 50 custom scans, chart patterns and industry rotation.
- **Club:** ₹2,499/month or ₹11,994/year. Adds "Stock AI", SEBI-registered research ideas and analyst access.

Checked 25 Oct 2026 — [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india)
- StockEdge's own premium page has shown ₹399/month (auto-renew) and ₹2,989/year with a promo code; I don't know when that page was captured — [StockEdge, official](https://stockedge.com/premium). The three paid plans are Premium, Pro and Club — [StockEdge FAQ, official](https://stockedge.com/faq/plans-payments/plans). Plans are not refunded once bought — [StockEdge FAQ, official](https://stockedge.com/faq/plans-payments/pricing). The free tier covers news, FII data and watchlists; scans and indicator charts are paid — [Tapetide StockEdge review, competitor](https://tapetide.com/compare/stockedge-review)

#### Trendlyne (proprietary DVM scores plus screeners)
- DVM stands for Durability, Valuation and Momentum, each scored 0–100. Above 55 is "good" and 35–55 is "neutral/medium". Momentum is recalculated daily from more than 30 technical indicators. Valuation uses current P/E, P/BV and price. Durability reflects financial consistency. The weights are not published — [Trendlyne help, official](https://help.trendlyne.com/support/solutions/articles/84000384325-what-does-the-stock-overview-in-the-trendlyne-app-mean-); [Trendlyne help, stock report structure, official](https://help.trendlyne.com/support/solutions/articles/84000396565-how-is-the-stock-report-structured-). Screener parameters that use DVM scores are for subscribers only — [Trendlyne screener page, official](https://trendlyne.com/fundamentals/screen/4807/highest-returns-top-dvm-performers-for-all-stocks-subscription)
- Plans, checked 24 Oct 2026 — [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india):
  - **GuruQ:** ₹390/month or ₹2,990/year (₹1,890 with coupon). 1,758 screener parameters, Forecaster estimates, 200 backtests a year, AI credits, daily technicals.
  - **StratQ:** annual only, ₹9,900 (₹5,900 with coupon). 3,512 parameters, 1,200 backtests, Excel Connect, 20 AI credits, intraday technicals from 15-minute data.
  - **PRO / PRO PLUS:** ₹1,500 / ₹2,000 a month, or ₹8,900 / ₹11,900 a year. Both add US stocks; PLUS also adds F&O "SmartOptions".
  - **Trendlyne MCP connector:** a separate product, Pro ₹299/month and Max ₹499/month.

#### Screener.in (fundamental query-language screener)
- Premium is ₹4,999/year including GST, with no monthly plan. It adds higher alert limits, quick ratios, downloads, custom ratios and ₹500 of "Screener AI" credits. Checked 24 Oct 2026 — [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india). The free account covers query screens and 10 alerts. A full refund is available within 48 hours, and there is no free trial — [Tapetide Screener review, competitor](https://tapetide.com/compare/screener-in-review)

#### MarketsMojo (proprietary "Mojo Score" plus advisory)
- The marketsmojo.motilaloswal.com domain lists the entity as "MOJO Markets Private Limited (Research Entity)" with SEBI RA No. INH000021942 — [MarketsMojo page, official](https://marketsmojo.motilaloswal.com/stocks-analysis/getstocksbyname?n=X). An aggregator says the RA registration has perpetual validity from 18 Jul 2025 — [ESI, secondary](https://esi.in/finance/investments/sebi/research-analysts/mojo-markets-private-limited/). The site reportedly also shows "SEBI Registered Investment Advisor Registration No: INA000012528 (Non – Ind)" — [Tapetide MarketsMojo review, competitor](https://tapetide.com/compare/marketsmojo-review)
- The Mojo Score is a quantitative Buy/Hold/Sell call with "no target price or time frame" — [Tapetide MarketsMojo review, competitor](https://tapetide.com/compare/marketsmojo-review). The app listing describes it as a 100-point rating covering fundamentals, valuation, technicals and earnings quality — [MarketsMojo app listing, secondary](https://mwm.ai/apps/marketsmojo-stock-research/1192962208). MojoOne Expert costs ₹9,999 on a 14-month offer and includes recommendations, model portfolios and trading calls. Checked 24 Oct 2026 — [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india)

#### Tijori Finance (sector-specific operational data)
- Paid: ₹330/month or ₹3,500/year, covering historical operational metrics, custom screener queries and data downloads. Checked 24 Oct 2026 — [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india). The free plan allows 1 portfolio account and 1 watchlist — [Tijori features page, official](https://tijorifinance.com/features/?r=forbidden). Premium adds market share, revenue mix, raw-material data and 1,000+ operational metrics (Nov 2025 review) — [Finology Ticker review, secondary](https://ticker.finology.in/discover/solutions/tijori-finance-review). Zerodha's Z-Connect blog carries "New on Tijori" product updates — [Z-Connect](https://zerodha.com/z-connect/business-updates/new-on-tijori)

#### Others (prices checked 24 Oct 2026) — [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india)
- **Tickertape Pro:** ₹399/month or ₹2,999/year (offer). Analyst ratings, forecasts, scorecards, red flags, 100+ metrics, 69 premium filters.
- **Moneycontrol PRO:** ₹99/month or ₹499/year with coupons, plus 18% GST. Scanners, SWOT and proprietary "MC Insights".
- **Moneycontrol Super PRO:** ₹499/month or ₹2,499/year with coupons. Adds trading calls, daily chart patterns and "AI WhatsApp alerts".
- **Value Research Stock Advisor:** ₹9,990/year.
- **Finology ONE:** ₹299/month.

### Inferences
- **Rule-based screens** (Chartink, Screener.in, StockEdge, Trendlyne) are transparent and reproducible. You see exactly the conditions that fired.
- **Proprietary scores** (DVM, Mojo Score, MC Insights) are rules or weightings that aren't published. None of the sources describes them as machine-learning price forecasts. "AI" in this group in 2025–26 means LLM credits for Q&A or natural-language screen building, not ML signals.
- **Data timing:**
  - Fundamental scores update after quarterly filings.
  - Momentum and technical scores are recomputed daily (Trendlyne) or from 15-minute bars (StratQ).
  - Intraday technical scanning is live only on Chartink Premium (about 1 minute), and about 5 minutes delayed on its free tier.
- **What the bot lacks:**
  - universe-wide scanning across all NSE stocks
  - fundamentals or composite quality and valuation scores
  - scan backtesting (Trendlyne gives 200–1,200 backtests a year)
  - sector or industry rotation views, chart-pattern recognition, and FII/deals data feeds (StockEdge)
  - webhook alerts that can chain to an execution platform (Chartink to AlgoTest)

### Gaps
- No source states Screener.in's data refresh schedule (EOD vs intraday price updates), nor whether StockEdge scans use EOD or intraday data.
- Trendlyne's exact DVM formula and weights, and MarketsMojo's scoring weights, are not public.
- I found no source on whether MarketsMojo is now owned by or partnered with Motilal Oswal. The motilaloswal.com subdomain suggests some link, but that is unverified.
- Who holds the SEBI RA registration behind StockEdge Club's "SEBI-registered research ideas" was not checked.
- A search snippet attributed a ₹399/month / ₹1,499/year price to Chartink. It matches StockEdge's figures exactly, so I treated it as a mix-up and disregarded it.

## 3. No-code algo and backtest platforms (Streak, Tradetron, AlgoTest, others): strategy definition, backtesting, execution, data, limits

### Takeaway
- **Strategy definition:** condition blocks (indicator crossovers, time windows, P&L-based exits). Option-focused tools add multi-leg legs with per-leg stop-loss and target.
- **Backtesting:** runs on the vendor's historical candles. AlgoTest claims 7.5+ years of index-options history with slippage settings.
- **Execution:** through broker APIs, from the vendor's servers.
- **Pricing models:**
  - Streak has been free for Zerodha clients since 17 Jan 2024.
  - Tradetron charges by number of live strategies: ₹300–₹2,500/month for retail, up to ₹15,000.
  - AlgoTest sells credits (₹499–₹5,999 packs) plus a ₹1,299 Signals plan.

From 1 Apr 2026, third-party platforms can place orders only if the exchanges have empanelled them as algo providers. Empanelment status is self-reported (AlgoTest) or unverified (Tradetron).

### Cited Findings
- **Streak, status:** Zerodha's post of 17 Jan 2024 is titled "Zerodha users now have unlimited access to Streak". Users can run scanners, place direct orders, backtest strategies and virtually deploy strategies in live markets — [Z-Connect, official](https://zerodha.com/z-connect/updates/zerodha-users-now-have-unlimited-access-to-streak). Streak's help page describes it as free exclusively for Zerodha users, but the page did not render when I fetched it on 5 Nov 2026 — [Streak help, official](https://help.streak.tech/subscription)
- **Streak, conflicting price data:** AlgoTest's comparison (published 3 May 2026, updated 3 Jun 2026; prices "as of April 2026") still lists Streak at about ₹500 (Basic), ₹900 (Premium) and ₹1,400 (Ultimate) a month with a 7-day trial, and says it is primarily Zerodha with limited multi-broker support. This is probably outdated — [AlgoTest, competitor](https://algotest.in/blog/algo-trading-software-price/). Older plan limits were 50 backtests/day, 50 scans/day and 5 live deployments at a time (2021) — [Chittorgarh, secondary](https://chittorgarh.com/article/zerodha-streak-review-algo-trading-for-retail/516). Streak is described as a no-code, indicator-based builder and backtester that works only with Zerodha accounts — [AlgoTest vs Streak, competitor](https://algotest.in/blog/algotest-vs-streak/)
- **Tradetron (April 2026 prices):** prices "as of April 2026" — [AlgoTest, competitor](https://algotest.in/blog/algo-trading-software-price/)

  | Plan | Price/month | Limits |
  |---|---|---|
  | Free | ₹0 | paper trading only, 1 live-paper deployment, 10 private strategies |
  | Starter | ₹300 | 1 live strategy |
  | Retail | ₹1,200 | 5 live strategies + 2 stockbags |
  | Retail+ | ₹2,500 | 12 live strategies + 4 stockbags |
  | Advanced | up to ₹15,000 | — |

  Quarterly billing saves 7% and annual saves 17%. Strategies are built in a no-code visual builder, and a marketplace sells strategies from other users and from SEBI-registered analysts. Tradetron's help centre says MCX and other exchange sets have their own plan tiers — [Tradetron help, official](https://help.tradetron.tech/en/article/tradetron-pricing-plans-upgrade-refund-policy-7oisc0/)
- **AlgoTest (April 2026):** "as of April 2026" — [AlgoTest, vendor](https://algotest.in/blog/algo-trading-software-price/)
  - **Free tier:** 25 backtests a week, which do not expire ("not a trial").
  - **Credit packs:** Starter ₹499 (500 credits), Explorer ₹999 (1,100), Pro ₹2,499 (3,000), Premier ₹5,999 (7,500). Credits do not expire.
  - **Deployment:** 100 credits per strategy per 28-day cycle. Forward testing costs 50 credits.
  - **Signals Plan:** ₹1,299 for 28 days, with unlimited live trades and up to 100 concurrent executions.
  - **Execution:** 40+ brokers, including Zerodha, Angel One, Fyers and Dhan.
- **AlgoTest, other claims:** more than 7.5 years of historical options data, multi-leg backtests, and slippage and brokerage settings — [AlgoTest vs Sensibull, vendor](https://algotest.in/blog/algotest-vs-sensibull.md). AlgoTest says it is empanelled with NSE and BSE — [AlgoTest blog, vendor, UNVERIFIED](https://algotest.in/blog/is-sebi-banning-algo-trading-in-india/)
- **Others (April 2026):** prices and features "as of April 2026" — [AlgoTest, competitor](https://algotest.in/blog/algo-trading-software-price/)
  - **AlgoBulls:** from ₹1,180/month; no-code, Python, and "AI-assisted strategy generation".
  - **uTrade Algos:** about ₹999/month; "AI-based building"; works with Share India only.
  - **QuantMan:** Basic ₹1,300/month, Premium ₹3,300/month; 80+ indicators, straddle and iron-condor templates.
- **Broker-hosted automation:** FYERS says "FYERS Automate" on FYERS Web runs inside FYERS infrastructure and complies with the 1 Apr 2026 framework. Its notice of 10 Mar 2026 also says third-party platforms "must be empanelled and hosted within the broker's infrastructure" to keep placing orders — [FYERS notice, broker](https://fyers.in/notice-board/new-sebi-framework-for-retail-algo-trading-from-april-01-2026)
- **Empanelment:** NSE has an "Empanelled Algo Providers" page that references circulars of 22 Jul 2025 and 19 Sep 2025. The page timed out when fetched on 5 Nov 2026, so I could not read the provider names — [NSE, official](https://www.nseindia.com/static/trade/empanelled-algo-providers-exchange). The only claim that Tradetron is NSE-empanelled comes from a Reddit snapshot of 6 Apr 2026 — [Reddit snapshot, UNVERIFIED](https://reddit.sentinel-team.org/posts/1sdp51g/snapshots/2026-04-06T18%3A21%3A45.259237Z)

### Inferences
- **Data used:** backtests run on the vendor's stored historical OHLC candles (index options for AlgoTest; mostly equity and indicator data for Streak). Live runs use broker market data and order APIs.
- **Limits:**
  - plan caps on live strategies or credits
  - backtests at candle resolution, so fills inside a candle are assumed and slippage is a user parameter
  - after 1 Apr 2026, dependence on the platform's empanelment and broker hosting (FYERS notice)
- **What the bot lacks:**
  - a backtesting engine and statistics for its own setups (win rate, expectancy, drawdown of breakout and dip-buy signals)
  - forward or paper testing
  - broker order execution with per-leg stop-loss and target management
  - multi-leg options strategies
  - a webhook-to-order pipeline (Chartink/TradingView to AlgoTest/Tradetron)
  - a strategy marketplace

### Gaps
- AlgoTest's backtest granularity (1-minute or not) and its exact start date are not stated; 7.5+ years implies roughly 2019.
- Streak's current (2026) limits for Zerodha users are not confirmed, nor whether live deployments still need the user to confirm orders. I also don't know whether Streak or Tradetron are exchange-empanelled.
- I could not fetch Tradetron's official price page (tradetron.tech/plans returned 404), so its prices come only from a competitor.
- I found no independent data on live-trading performance or failure rates for any platform.

## 4. Broker-built AI and analytics (Zerodha, Angel One, Dhan, Upstox, Groww, Fyers): what is genuinely AI/ML and what is rules

### Takeaway
LLM-based features you can actually use exist at three brokers:
- Angel One's "Ask Angel" conversational assistant
- Groww's "GR 1" assistant (beta, opt-in, announced Mar 2026)
- Fyers' FIA screener builder (Apr 2025) and FIA GPT (2025)

On top of that, seven of eight large brokers have official MCP servers (checked 13 Oct 2026) that expose account data to external LLMs. Only some of those servers can place orders: Dhan, Groww and 5paisa can; Zerodha can set GTT orders only; Upstox, FYERS and Kotak Neo are read-only. The analytics proper (option chains, OI, Greeks, scanners, ARQ Prime stock picks) are rule-based or quantitative. None is documented as ML price prediction.

### Cited Findings
#### Zerodha
- **Kite MCP:** launched 20 May 2025, free. It works with Claude Desktop, Cursor, Windsurf and VS Code Copilot, and Zerodha credentials never pass through the AI (Kite 2FA flow). The post says operations are "read-only, except GTT orders". A Zerodha staff comment in Nov 2025 lists 22 tools, including place, modify and cancel order, which contradicts that — [Z-Connect, official](https://zerodha.com/z-connect/featured/connect-your-zerodha-account-to-ai-assistants-with-kite-mcp)
- **Kite MCP, hosting:** hosted at mcp.kite.trade. The open-source zerodha/kite-mcp-server includes order tools for people who self-host it with their own API keys. Checked 13 Oct 2026 — [OneTradeJournal MCP review, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers)
- **Kite Connect API pricing:** order-placement and account APIs have been free since March 2025. Data APIs (real-time and historical) were cut from ₹2,000 to ₹500/month from 6 May 2025 — [Z-Connect, 6 May 2025, official](https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework); [Kite forum, official](https://kite.trade/forum/discussion/comment/49590). A forum user (not Zerodha staff) says "Personal" apps cost nothing — UNVERIFIED.
- **Analytics stack:** Zerodha's analytics are partner-built and broker-funded. Sensibull has been free since 24 Jul 2023 and Streak since 17 Jan 2024 (see sections 1 and 3). The native Kite option chain shows OI, IV and Greeks — [OneTradeJournal, secondary](https://onetradejournal.com/platforms/options-analytics-tools-compared)

#### Angel One
- **ARQ Prime:** search summaries of Angel One pages describe ARQ Prime as a *rule-based* investment engine. It recommends up to 15 stocks and suggests portfolio rebalancing, and grew out of the original "ARQ". Angel One's own article was titled "Angel Broking's machine learning engine is like having Iron Man's Jarvis by your side". When I fetched them on 5 Nov 2026, that article and a related one both returned HTTP 410 (Gone). Whether ARQ Prime is still current, and whether it is really ML or rules, is UNVERIFIED — [Angel One ARQ article (removed)](https://www.angelone.in/news/market-updates/angel-brokings-machine-learning-engine-is-like-having-iron-mans-jarvis-by-your-side); [Angel One investment-tech page (removed)](https://www.angelone.in/news/personal-finance/pushing-the-boundaries-of-investment-technology)
- **"Ask Angel":** an in-app conversational AI assistant for customer service, IPO discovery, stock analysis and general Q&A. Angel One's investor presentation calls it "captively developed", built on a hybrid of open-source and enterprise models with guardrails. Company-reported figures are over 90% answer accuracy and over 80% of users resolving queries through it — [Angel One investor presentation, official](https://w3assets.angelone.in/wp-content/uploads/pdf/1768485285003-Investor-Presentation-Final.pdf). Ask Angel is also listed inside the "OneHelp" support hub — [Angel One, official](https://angelone.in/news/introducing-onehelp-your-new-go-to-resource-for-effortless-support)
- A Reuters item says the AI assistant rolled out "in April" (year not stated) and had over 1.1 million user clicks — [Reuters item on Zerodha's ANGELONE quote page, media](https://www.zerodha.com/markets/stocks/NSE/ANGELONE/). A Sep 2026 interview says the company is "actively exploring AI" for personalisation — [YourStory, media](https://yourstory.com/2026/09/pits-walkie-talkies-ai-angel-one-founder-dinesh-thakkar-30-year-old-stock-broking-stellar-growth)
- Angel One has no official MCP server; only community-built ones exist. Checked 13 Oct 2026 — [OneTradeJournal MCP review, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers)

#### Dhan
- **ScanX:** a separate research platform at scanx.trade, with some premium features reserved for Dhan users. A forum reply (date unclear) says it has not been inside the Dhan app since 2024 — [MadeForTrade forum, secondary](https://madefortrade.in/t/scanx-in-dhan-application/46204)
- **Options Trader:** Quant Mode, Greeks and backtests, free for Dhan users (see section 1).
- **Official MCP:** at mcp.dhan.co. It reads funds, holdings, positions, order and trade books and historical candles, and can place, modify and cancel orders. Live quotes and option chains need the paid Data API, ₹499 + taxes/month. Checked 13 Oct 2026 — [OneTradeJournal MCP review, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers)

#### Upstox
- The official MCP at mcp.upstox.com is read-only (holdings, orders, positions, mutual funds, funds, profile); the page says "You cannot place orders, modify positions, or execute trades". A separate "Agent Skill", dated 6 Jun 2026, can place, modify and cancel orders, including GTTs. Checked 13 Oct 2026 — [OneTradeJournal MCP review, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers)

#### Groww
- **GR 1:** an AI investing assistant that "reads markets, tracks news sentiment" and gives portfolio-personalised insights. It is in beta and opt-in, and was unveiled at Groww Next 2026 in Bengaluru (article dated 2 Mar 2026). The same event added a high-frequency trading mode, a physical trading keyboard, and F&O risk alerts and trading locks — [Entrackr, media](https://entrackr.com/news/groww-showcases-ai-powered-investing-tools-at-groww-next-2026-11168623)
- **Groww MCP:** at mcp.groww.in, dated 4 Aug 2025. It reads holdings, positions, P&L and chart data, and can place buy, limit and stop-loss orders; sell orders need DDPI. Checked 13 Oct 2026 — [OneTradeJournal MCP review, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers); [Groww engineering blog, official](https://tech.groww.in/building-groww-mcp-a-technical-deep-dive-into-ai-powered-portfolio-intelligence-beea42be67f1)

#### Fyers
- **FIA (FYERS Intelligent Assistant):** a natural-language screener builder over price, volume and OI data, in beta on FYERS Web. The PTI press release is dated 7 Apr 2025 — [Tribune/PTI, media](https://www.tribuneindia.com/news/business/fyers-launches-fia-indias-first-ai-powered-screener-creator-for-traders)
- **FIA GPT:** a free custom GPT in OpenAI's GPT store (launched in 2025; exact date not found) — [SME Street, media](https://smestreet.in/technology/fyers-launches-fia-gpt-indias-first-ai-analyst-for-traders-9666659); [FYERS support, broker](https://support.fyers.in/portal/en/kb/articles/how-is-fia-gpt-different-from-a-regular-chatbot); [FYERS 2025 year review, broker](https://fyers.in/community/blogs-gdppin8d/post/fyers-2025-a-year-of-building-for-serious-traders-oexZi4iLhXxvLYh). One report says it does analysis only and does not execute trades — [Exchange4media, media](https://www.exchange4media.com/digital-news/fyers-launches-ai-stock-market-assistant-integrated-with-openais-chatgpt-146447.html)
- **FIA MCP:** at mcp.fyers.in, dated 7 Nov 2025 (help article updated 18 Dec 2025). It reads funds, holdings, positions, orders, GTTs, the trade book, the option chain and historical data, and can create watchlists and price alerts. It cannot place, modify or cancel orders. Checked 13 Oct 2026 — [OneTradeJournal MCP review, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers)

#### Others
- **Kotak Neo MCP:** read-only (holdings, books, positions, live prices, research), no extra cost.
- **5paisa MCP:** runs locally from GitHub, dated 17 Jun 2025. It can place orders.

Both checked 13 Oct 2026 — [OneTradeJournal MCP review, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers)

### Inferences
- **Genuinely AI (LLM):** Ask Angel, GR 1, FIA and FIA GPT, Chartink's plain-language filter input, and the MCP servers, which turn broker APIs into tools an LLM can call.
- **Rules or quant:** option-chain analytics, OI and Greeks, scanners, ARQ Prime stock selection (described as rule-based despite the "ML" label), and risk alerts and locks.
- No broker documents an ML model that predicts prices.
- For the bot, the MCP route is a ready-made way to connect broker data, positions and (at Dhan or Groww) orders to an LLM. Any API order placement is still bound by the static-IP and other rules in section 6.
- **What the bot lacks:**
  - a natural-language query layer ("show NSE stocks with long build-up and price above VWAP")
  - news and sentiment ingestion (GR 1)
  - portfolio and position awareness from a live broker account
  - option-chain data, which comes free with Dhan's Data API (₹499/month) or the Fyers MCP

### Gaps
- I found no confirmed AI features inside the Dhan or Upstox apps (beyond the MCP and Agent Skill). A 2025 roundup claiming Dhan has "AI-powered stock ideas" was unreliable and left out.
- I did not research Zerodha's in-app "Nudges" or any other risk prompts.
- ARQ Prime's current product status, pricing and method could not be confirmed, because its pages have been removed.
- The exact launch dates of Ask Angel and FIA GPT are not confirmed.

## 5. AI advisory apps (Liquide, Univest and similar): working model and SEBI RA/IA registration

### Takeaway
"AI advisory" apps in India operate under a SEBI Research Analyst (RA) licence, sometimes with an IA or broker licence alongside. They put an LLM or quant front end on recommendations that their RA staff supervise. Liquide (RA INH000009816) and MarketsMojo (RA INH000021942, IA INA000012528) have clearly stated numbers. Univest's broker licence (INZ000317437) is clear, but its RA number conflicts between listings. Since 16 Dec 2024, SEBI's RA rules require RAs to disclose how much they use AI, and they stay fully responsible for AI-generated output.

### Cited Findings
- **Liquide:** Liquide Solutions Pvt Ltd holds SEBI RA INH000009816 (corporate, perpetual validity) and BSE enlistment ID 5582. It calls LiMo the "world's first AI-powered & expert-supervised research assistant", claiming 20 million+ queries and 5 million+ reports. Trade ideas (intraday, short-term, long-term) are "curated by SEBI-registered experts", with automated BUY/SELL alerts. "Wealth Baskets" use "quant and AI strategies", with a claimed $13.5 million+ AUM across 6 baskets. Fetched 5 Nov 2026; no pricing shown — [Liquide, official](https://liquide.life/)
- The Liquide app listing describes LiMo as giving real-time Buy/Sell/Hold suggestions, with trades placed through the user's own broker — [App Store, official](https://apps.apple.com/us/app/liquide-life/id1624726081). A competitor criticises Liquide's vague "accuracy" claims — [AlgoTest, competitor](https://algotest.in/blog/ra-algos-vs-liquide)
- **Univest:** Univest Stock Broking Pvt Ltd is a SEBI stock broker, INZ000317437, on NSE, BSE and MCX. Products are Univest Pro (analyst recommendations for stocks, F&O and commodities), screeners, "Shark Portfolios" and unspecified "AI-powered portfolio insights". No RA number is listed there — [univest.in/llms.txt, official](https://univest.in/llms.txt). App listings say RA services come from subsidiary Uniresearch India Pvt Ltd, but give two different RA numbers, INH000013776 and INH000015339 — [App Store India listing, official](https://apps.apple.com/in/app/id6443753518) (UNVERIFIED which is current)
- **MarketsMojo:** RA INH000021942 and IA INA000012528; the Mojo Score is a quantitative Buy/Hold/Sell call (see section 2).
- **Quantsapp:** its trade alerts are "Managed by SEBI RAs", while Quantsapp itself claims no registration — [Quantsapp, official](https://new.quantsapp.com/)
- **StockEdge Club:** includes "SEBI-registered research ideas". **Moneycontrol Super PRO:** includes trading calls and "AI WhatsApp alerts". Checked 24–25 Oct 2026 — [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india)
- **SEBI AI-disclosure rule:** the SEBI (Research Analysts) (Third Amendment) Regulations, 2024, notified 16 Dec 2024, add Regulation 19(vii). RAs must disclose "the extent of use of Artificial Intelligence tools in providing research services". RAs and IAs are "solely responsible" for client-data security and for advice based on AI output — [SCC Online, secondary](https://www.scconline.com/blog/post/2024/12/19/sebi-research-analyst-third-amendment-regulations-2024/); [Daily Pioneer, media](https://www.dailypioneer.com/2024/business/investment-advisers--research-analysts--should-disclose-ai-tool-usage-to-clients--sebi.html). The disclosure is made along with the terms and conditions of service. A Feb 2025 source says existing clients had to be covered by 30 Apr 2025 — [AZB & Partners, secondary](https://www.azbpartners.com/?p=86104)
- **Black-box algos:** providers of black-box algos (logic not disclosed) must register as RAs and keep a detailed research report for each algo. Any logic change means registering a fresh algo with a new report — [MediaNama on the 4 Feb 2025 circular, media](https://www.medianama.com/2025/02/223-sebi-proposes-framework-retail-investors-algo-trading/). An RA who wants to deploy a black-box algo must also become an empanelled algo provider — [Shoonya blog, broker](https://blog.shoonya.com/sebi-algo-trading-rules/)
- **Tradetron marketplace:** includes strategies from SEBI-registered analysts — [AlgoTest, competitor](https://algotest.in/blog/algo-trading-software-price/)

### Inferences
- **Working model:** human RAs produce or approve calls (entry, target, stop). The "AI" is a chat interface, a personalisation layer, or quant screens over those calls. Users execute through their own broker.
- These apps sell opaque recommendations. The user's bot is the opposite: transparent and rule-based, for personal use only. That makes it neither an RA service nor a black-box algo, as long as it isn't offered to others (see section 6).

### Gaps
- I could not access SEBI's intermediary database to confirm INH000009816, INH000021942, INA000012528 or Univest's RA number.
- Pricing for Liquide and Univest was not shown on their sites.
- Other AI advisory apps (for example Jarvis Invest, Equentis/Research & Ranking) and their registrations were not researched.
- I did not check whether SEBI's 2025 consultation on AI/ML guidelines for regulated entities has been finalised.

## 6. SEBI rules: (a) personal, non-public use of analysis tools; (b) API-based algo trading by an individual (Feb 2025 framework, later updates, status in late 2026)

### Takeaway
(a) **Personal analysis.** Running analysis tools or a self-built analysis bot for your own trading needs no SEBI registration. The RA definition (as amended Dec 2024) covers only people who provide research services "for consideration", and consideration includes indirect or non-cash benefit. Sharing signals publicly or for any benefit moves into RA or finfluencer territory. "Educational" content must use price data at least 3 months old (Jan 2025 circular); a Jan 2026 consultation proposes 30 days.

(b) **API algo trading.** SEBI's 4 Feb 2025 retail algo circular has been fully in force for all brokers since 1 Apr 2026, after two deferrals: 1 Aug 2025, then 1 Oct 2025, then a glide path. For an individual's own bot, the rules are:
- orders only from a broker-whitelisted static IP (1 primary + 1 optional backup, changeable once a week, shareable only with spouse, dependent children and dependent parents)
- a daily 2FA login, with no persistent refresh tokens
- at most 10 orders per second per exchange per segment unless the algo is registered with the exchange
- orders tagged by the broker with an exchange algo ID
- market orders converted to price-protected orders (at FYERS)
- the algo may be used only by you and your family, never offered to others

Read-only data access (market-data WebSocket, positions) needs no static IP at Zerodha.

### Cited Findings
#### (a) Personal / non-public use
- After the Dec 2024 amendment, a research analyst is someone who, "for consideration, is engaged in the business of providing research services". "Consideration" means "any form of economic benefit including non-cash benefit, received or receivable, directly or indirectly... whether from client or otherwise". Services provided without any direct or indirect consideration can be offered without registration. A SEBI FAQ treats research bundled with other services, such as brokerage, as "research for consideration" — [Mondaq, secondary](https://www.mondaq.com/india/securities/1574012/navigating-the-updated-regulatory-framework-for-investment-advisers-and-research-analysts); [Lakshmikumaran & Sridharan on SEBI FAQs 2025, secondary](https://lakshmisri.com/insights/articles/key-clarifications-under-the-sebi-issued-faqs-2025)
- SEBI's 29 Jan 2025 circular says people offering market education may use only price data at least 3 months old, and may not use stock names, codes or recent prices in any way that implies advice — [Business Standard, media](https://www.business-standard.com/markets/news/sebi-finfluencer-circular-live-stock-data-market-education-rules-125013000571_1.html). A consultation paper of 6 Jan 2026 proposes cutting the lag to 30 days (comments were due 27 Jan 2026). It is not confirmed as final — [Moneylife, media](https://moneylife.in/article/sebi-plans-30day-pricedata-lag-to-curb-misuse-by-market-educators/79450.html)
- Under the Feb 2025 framework, retail investors who build their own algos may use them "for personal and family investments but cannot offer them to other investors" — [MediaNama, media](https://www.medianama.com/2025/02/223-sebi-proposes-framework-retail-investors-algo-trading/)
- **Yahoo Finance timing:** Yahoo's help page lists NSE (.NS) as "Real-time" (provider ICE Data Services). Another version of the page adds that NSE quotes are real-time "for all users who have signed in". BSE (.BO) is 15 minutes delayed — [Yahoo help, official](https://help.yahoo.com/kb/SLN2310.html). By contrast, Microsoft Excel's stock data lists NSE at a 5-minute delay — [Microsoft support, official](https://support.microsoft.com/en-us/Excel/about-the-stocks-financial-data-sources)

#### (b) API algo trading — framework text and timeline
- The circular is SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013, dated 4 Feb 2025, "Safer participation of retail investors in Algorithmic trading" — [SEBI, official](https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html). The body text could not be extracted, so the provisions below come from coverage of it.
- Main provisions — [MediaNama, 5 Feb 2025, media](https://www.medianama.com/2025/02/223-sebi-proposes-framework-retail-investors-algo-trading/):
  - the broker is the principal and algo providers (fintechs, vendors) are its agents
  - exchanges empanel algo providers
  - access only through a "unique vendor client-specific API key" plus a broker-verified static IP
  - brokers must block open APIs, prefer OAuth and use two-step verification
  - orders above an OPS threshold count as algo orders
  - every API order is tagged with an exchange-issued unique identifier, and exchanges can "kill switch" an algo ID
  - white-box (logic disclosed) vs black-box algos (RA registration needed)
  - original effective date 1 Aug 2025
- NSE's implementation standards (reported 6 May 2025):
  - individuals may automate "up to 10 orders per second (per segment per exchange) without registration"; above that, the algo must be registered with the exchange
  - algos from algo providers and from brokers need exchange registration at any rate
  - order tagging: broker algos carry an exchange-specific algo ID, provider algos a unique cross-broker ID, and client algos a generic ID if unregistered (10 OPS or less) or a unique ID if registered (more than 10)
  - OAuth/2FA, password expiry and no open APIs apply to all categories
  - brokers are fully liable for every order

  [Z-Connect, 6 May 2025, broker](https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework); [Business Standard, 6 May 2025, media](https://www.business-standard.com/markets/capital-market-news/nse-lays-down-new-ground-rules-for-retail-algo-trading-to-boost-safety-and-compliance-125050600690_1.html)
- Zerodha staff comments on that post (May 2025 to Mar 2026), all [broker] — [Z-Connect comments](https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework):
  - limits apply per API key, and only one API key per user can run an unregistered algo below 10 OPS
  - static IP is needed only for order placement, and family members can share it
  - a backup IP is recommended; IPv6 is allowed; the IP need not be in India; 127.0.0.1 does not qualify
  - users of vendor platforms don't need their own static IP, because the vendor connects with its own
  - Zerodha's 3,000 orders/day cap is an internal Zerodha limit
  - a clause about hosting on broker cloud "will be revised out"
- NSE issued detailed operational modalities in July 2025, under the headline "NSE issues retail algo trading rulebook, mandates strategy registration" (23 Jul 2025). The article body returned HTTP 403, so the details are not verified — [Business Standard, media](https://www.business-standard.com/markets/news/nse-unveils-guidelines-for-retail-algo-trading-effective-august-1-125072301458_1.html)
- **Extension circular:** SEBI's circular of 30 Sep 2025 (SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/132) replaced the single deadline with a glide path. Brokers that were ready could go live from 1 Oct 2025. Brokers had to take part in at least one mock trading session by 3 Jan 2026, and those missing milestones were barred from onboarding new retail API-algo clients from 5 Jan 2026. The framework applies to all stock brokers from 1 Apr 2026. The date had already moved from Aug 2025 to 1 Oct 2025 before this — [Business Standard, 30 Sep 2025, media](https://www.business-standard.com/markets/news/sebi-extends-retail-algo-trading-framework-rollout-to-2026-125093000956_1.html); [Taxscan, secondary](https://www.taxscan.in/top-stories/sebi-extends-timeline-for-retail-algo-trading-framework-full-implementation-from-apr-1-2026-1433982); [IANS, media](https://ianslive.in/sebi-pushes-back-retail-algo-trading-framework-sets-phased-rollout-till-april-2026--20250930211310)
- Secondary summaries add a 31 Oct 2025 milestone for brokers to apply to register at least one retail algo product — [Sahi blog, secondary](https://www.sahi.com/blogs/sebi-algo-trading-rules-2026-what-every-retail-trader-must-know-before-april); [AlgoBulls blog, secondary](https://algobulls.com/blog/industry-insights-and-updates/sebi-new-algotrading-regulations-for-retail-investors-2026). Mint reported that brokers struggled to meet the deadline and that SEBI had to extend it twice — [Mint via Magzter, media](https://www.magzter.com/nb/stories/newspaper/Mint-Hyderabad/BROKERS-STRUGGLE-TO-MEET-SEBI-DEADLINE-ON-RETAIL-ALGO-TRADING)

#### (b) Status as of late 2026, from broker documentation
- **Zerodha (current support page):** "effective 1 April 2026, you must have a static IP for API-based order placement". The market-data WebSocket and other APIs such as orderbook and positions work from any IP. You need at least 1 primary IP and may add up to 2. Exchange rules allow one IP change per calendar week. Immediate family (spouse, dependent children, dependent parents) can share the IP through a single developer account, with separate apps and all client IDs added. Users must confirm the IPs "will be used exclusively by me and/or my immediate family". Static IPs can come from an ISP, cloud or VPS provider — [Zerodha support, broker](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/static-ip)
- **FYERS (notice of 10 Mar 2026, effective 1 Apr 2026):** "Orders will only be accepted from a registered App ID mapped to a whitelisted static IP address". 2FA is required once every trading day, and "continuous refresh-token sessions will no longer be supported". The limit is 10 orders per second at most. Market orders are "automatically converted to MPP (Market Price Protection) orders". Third-party platforms must be empanelled and hosted inside the broker's infrastructure. The old and new frameworks ran in parallel until 31 Mar 2026 — [FYERS notice, broker](https://fyers.in/notice-board/new-sebi-framework-for-retail-algo-trading-from-april-01-2026); [FYERS support, broker](https://support.fyers.in/portal/en/kb/articles/what-are-the-new-sebi-rules-for-retail-algo-trading-from-april-01-2026)
- **Conflict on sub-10 OPS registration:** secondary 2026 guides disagree. Some say no formal exchange registration is needed below 10 OPS, others say a generic algo ID registration is mandatory, and others that it is "tracked and tagged" only — [Liquide blog, secondary](https://blog.liquide.life/sebi-algo-trading-regulations-2026/); [AlgoBulls, secondary](https://algobulls.com/blog/industry-insights-and-updates/sebi-new-algotrading-regulations-for-retail-investors-2026); [Alphaquark, secondary](https://alphaquark.in/blog/sebi-retail-algo-trading-rules-2026-guide); [Flattrade Kosh, broker](https://flattrade.in/kosh/understanding-nses-guidelines-for-client-generated-algos-what-retail-investors-need-to-know/). Zerodha's own wording is that you can automate up to 10 OPS "without registration", with orders carrying a generic ID — [Z-Connect, broker](https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework)

### Inferences
- **The bot as it stands** (Yahoo data, then dashboard and Telegram alerts, no order placement) is outside the algo framework, because the framework governs API order flow. It needs no static IP or algo ID, and personal use needs no RA registration.
  - The line is crossed if signals go to other people for any direct or indirect benefit (paid Telegram group, ads, referral links). That would need RA registration.
  - Even free public posting of recent-price "setups" is risky under the finfluencer and education rules.
- **If the bot adds broker order placement:**
  - create a broker API app (Zerodha's order APIs are free) and whitelist a static IP from a VPS or cloud host (backup IP optional, changes limited to weekly)
  - re-authenticate with 2FA every trading day, because unattended refresh-token sessions are gone (at FYERS)
  - stay far below 10 OPS, which is trivial for a setups-based bot
  - prefer limit orders, since market orders become MPP orders at FYERS
  - accept that orders carry a generic algo ID and fall under broker RMS and exchange kill-switch controls
  - use it only for yourself and your family
- **Live NSE data instead of Yahoo:** the cheapest official options found are Kite Connect data at ₹500/month (data endpoints are not IP-restricted) and the Dhan Data API at ₹499/month + taxes (includes option chains).
- **Yahoo timing:** Yahoo's "real-time NSE" statement covers its website for signed-in users. Whether the unofficial yfinance download endpoints are equally live is not documented. Treat intraday Yahoo bars (ORB, VWAP) as possibly lagged until you test them against a broker feed.

### Gaps
- I could not extract the full text of the SEBI 4 Feb 2025 circular or NSE's July 2025 operational modalities (403 and empty fetches). The exact "family" wording comes from Zerodha's support page, not the circular.
- I found no SEBI or NSE amendment after 1 Apr 2026 (for example, a revised OPS threshold or a self-service registration process for client algos). That does not prove none exists.
- One secondary blog claims retail algo servers must be in India. I could not trace it to a primary source, and Zerodha staff said in May 2025 that the IP need not be in India.
- I could not read NSE's licensing rules for redistributing 15-minute-delayed data (the [NSE tariff PDF](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Download15mindelayeddatatariff.pdf) timed out). These would matter if the dashboard or Telegram bot ever shows NSE prices to others.
- Out of scope and not researched: RBI/FEMA rules on retail forex (offshore brokers) and Indian crypto tax/TDS. Both matter because the bot also covers forex and crypto.

## 7. Indian intraday concepts these tools emphasise (OI build-up, PCR, India VIX, FII/DII, GIFT Nifty, expiry-day behaviour)

### Takeaway
Indian tools centre on derivatives-flow signals:
- OI build-up (price change crossed with OI change), PCR and max pain from the option chain
- India VIX (30-day implied volatility from NIFTY options)
- provisional FII/DII cash flows published after the close
- GIFT Nifty (about 21 hours of trading at NSE IX) as the pre-market cue

Expiry structure has changed sharply since late 2024. There is now one weekly index expiry per exchange: Nifty on Tuesday since 1 Sep 2025, Sensex on Thursday. Short options pay extra margin on expiry day, and an F&O futures pre-open session (9:00–9:15) has run since 8 Dec 2025. In 2026 SEBI kept weekly expiries but flagged problems with expiry-day weekly options.

### Cited Findings
- **OI build-up and PCR:**
  - Quantsapp has Built-up Scrip, Breadth, Sector and Option Built Up tools, PCR on Pro and Pro+, and "Option Pain" (max pain) — [Quantsapp, official](https://new.quantsapp.com/)
  - Fyers' FIA builds screens from price, volume and OI (Apr 2025) — [Tribune/PTI, media](https://www.tribuneindia.com/news/business/fyers-launches-fia-indias-first-ai-powered-screener-creator-for-traders)
  - One review says Quantsapp alerts cover OI breakouts, PCR breaches and IV-percentile thresholds — [bankniftyoptions review, UNVERIFIED](https://bankniftyoptions-com.pages.dev/artigos/quantsapp-banknifty-review)
- **India VIX:**
  - NSE computes it from the NIFTY options order book. It reflects expected volatility over the next 30 calendar days, using the CBOE method adapted to near and next month, with time to expiry measured in minutes. Each contract is weighted in proportion to its bid-ask spread and inversely to its strike — [NSE launch release via Business Standard (2010), media](https://www.business-standard.com/amp/article/press-releases/nse-announces-the-launch-of-india-vix-110071900094_1.html)
  - The inputs are the best bid and ask quotes of out-of-the-money near- and next-month NIFTY options. The forward index comes from the NIFTY futures price — [NSE white-paper copy on Kite forum, secondary](https://kite.trade/forum/uploads/editor/70/vxgewoop7qn5.pdf)
- **FII/DII:** NSE publishes provisional FII/DII trading data after each session and calls it "provisional and subject to change" pending custodial confirmation. Final FPI figures are on NSDL — [NSE FII/DII report, official](https://www.nseindia.com/reports/fii-dii). FII data is in StockEdge's free tier and in Tapetide's free tier — [Tapetide StockEdge review, competitor](https://tapetide.com/compare/stockedge-review); [Tapetide price table, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india)
- **GIFT Nifty:** it trades for about 21 hours in two sessions, against NSE cash hours of 9:15–15:30 IST. Session times conflict between sources:
  - Kotak: Session 1, 6:30 am–3:40 pm IST — [Kotak Securities, broker](https://www.kotaksecurities.com/indices/global-indices/sgx-niftysgx-nifty)
  - Bajaj: 6:15 am–2:45 am IST with a 25-minute break — [Bajaj Broking, broker](https://www.bajajbroking.in/blog/what-is-gift-nifty)
  - [NiftyTrader explainer, secondary](https://www.niftytrader.in/markets/gift-nifty-explained-market-open-impact/)
- **SEBI F&O package (circular of 1 Oct 2024, SEBI/HO/MRD/TPD-1/P/CIR/2024/132):**
  - index contract value raised to ₹15 lakh or more (from 20 Nov 2024)
  - one weekly index expiry per exchange (20 Nov 2024)
  - extra 2% ELM on short index options on expiry day (20 Nov 2024)
  - option premium collected upfront from buyers (1 Feb 2025)
  - calendar-spread margin benefit removed on expiry day
  - intraday monitoring of position limits

  Dates vary slightly between sources — [Zerodha Z-Connect, broker](https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing); [Business Standard, 1 Oct 2024, media](https://www.business-standard.com/amp/markets/news/sebi-announces-six-key-changes-to-curb-speculation-in-derivatives-trading-124100101316_1.html)
- **Expiry days:** a SEBI circular of May 2025 limits each exchange's equity-derivative expiries to Tuesday or Thursday. NSE moved its expiries to Tuesday from 1 Sep 2025 (first Tuesday expiry on 2 Sep 2025), and BSE Sensex moved to Thursday — [Business Standard, 28 Aug 2025, media](https://www.business-standard.com/markets/news/nse-bids-adieu-to-thursday-expiry-as-dates-swap-come-into-effect-explained-125082800635_1.html); [Angel One, broker](https://www.angelone.in/news/market-updates/nifty-weekly-expiry-today-see-what-changed-on-sept-1-2025). Only Nifty (NSE) and Sensex (BSE) keep weekly options; Bank Nifty, FinNifty and Midcap Nifty are monthly only — [OneTradeJournal, secondary](https://onetradejournal.com/learn/weekly-vs-monthly-expiry)
- **SEBI stance on weekly expiries:**
  - Aug 2025: the SEBI chief called reports of a weekly-expiry ban "speculative" — [Business Standard, 6 Aug 2025, media](https://www.business-standard.com/markets/news/sebi-chief-refutes-ban-on-weekly-expiries-calls-reports-speculative-125080601594_1.html)
  - Jul 2025: a Mint report listed a move to fortnightly expiry among options under study — [Angel One news, broker](https://www.angelone.in/news/market-updates/sebi-may-shift-to-fortnightly-expiry-to-curb-index-options-activity-report)
  - Early 2026: Chairman Tuhin Kanta Pandey said SEBI is not considering new F&O curbs and will keep the status quo on weekly expiries (month per search summary: Feb 2026) — [5paisa, broker](https://www.5paisa.com/news/big-relief-for-fo-traders-sebi-not-considering-new-curbs-says-chief-tuhin-kanta-pandey)
  - Mar 2026: Pandey said "We did identify problems in options, specifically weekly index options on the expiry day" — [ANI, 2 Mar 2026, media](https://aniweb.voxturr.us/news/business/sebi-uses-data-warnings-and-targeted-measures-to-curb-retail-losses-in-fampo-chairman-pandey20260302090003)
- **F&O pre-open session:** live from 8 Dec 2025, 9:00–9:15 am. Orders can be placed, changed or cancelled until about 9:07–9:08. It covers current-month stock and index futures (next-month in the last 5 trading days before expiry); options are not covered. Basis: SEBI circular of 29 May 2025 and NSE circular NSE/FAOP/71092 of 3 Nov 2025 (as cited) — [Business Standard, 4 Nov 2025, media](https://www.business-standard.com/markets/capital-market-news/nse-to-commence-pre-opening-session-in-f-o-segment-from-december-08-125110400728_1.html); [5paisa, broker](https://www.5paisa.com/news/nse-fo-pre-open-session-begins-today-aims-to-improve-price-discovery-and-reduce-volatility); [Jainam, broker](https://www.jainam.in/blog/nse-pre-open-session-fo-segment/)

### Inferences
- The usual OI build-up taxonomy is a standard convention; no source here defines it:

  | Price | OI | Label |
  |---|---|---|
  | up | up | long build-up |
  | down | up | short build-up |
  | up | down | short covering |
  | down | down | long unwinding |

  Tools apply it per stock-futures contract or per strike. Because OI refreshes only every few minutes (section 1), it is a slower signal than price or VWAP.
- **Expiry calendar:** Nifty expires on Tuesday (weekly and monthly), Sensex on Thursday, and other indices monthly only. Expiry-day effects (gamma, pinning near max pain, extra margin on shorts) now land on Tuesdays for NSE. A bot that flags breakout or dip-buy setups on NIFTY should know the calendar.
- **Pre-market cues** Indian tools emphasise: the GIFT Nifty gap versus the previous Nifty close, the previous day's provisional FII/DII flows, India VIX level and change, and the pre-open equilibrium price (cash 9:00–9:08; futures since Dec 2025).
- **What the bot lacks:**
  - India VIX as a regime or volatility filter
  - FII/DII and participant data
  - a GIFT Nifty pre-market gap estimate
  - expiry-calendar awareness and expiry-day rules
  - futures OI build-up for stock and index futures
  - pre-open session data
  - PCR and max-pain context for index levels

  The bot's CPR, pivots, ORB and VWAP logic would sit next to these cues in Indian practice; the tools covered treat OI and VIX as primary.

### Gaps
- No source gave an exact publication time for NSE's provisional FII/DII data. Participant-wise OI (FII/Pro/Client) was not researched.
- GIFT Nifty session times conflict; I did not fetch the NSE IX contract specifications.
- I did not source SEBI's July 2025 Jane Street interim order on expiry-day index manipulation, which is often cited as context for expiry-day behaviour.
- India VIX parameters (30% spread filter, cubic-spline interpolation) come from secondary copies of the NSE white paper.

## 8. Concrete features the personal bot lacks, compared with these Indian tools

### Takeaway
The bot's level-based price-action engine (CPR, pivots, PDH/PDL and PWH/PWL, ORB, VWAP, confluence S/R, liquidity pools, sweeps, bias score, setups with R:R) covers ground the Indian tools mostly don't document. No tool reviewed here advertises liquidity-pool or stop-hunt detection. Its gaps fall into five areas:
- derivatives data (option chain, OI, IV, Greeks, PCR, max pain, futures OI build-up)
- validation (backtesting, forward testing)
- data quality and timing (Yahoo vs licensed broker feeds)
- market-context feeds (India VIX, FII/DII, GIFT Nifty, expiry calendar, pre-open)
- execution and compliance plumbing (broker API, static IP, daily 2FA, order tagging)

### Cited Findings
- **Option chain and analytics:** OI and OI build-up, PCR, max pain, IV, Greeks, strategy payoff — Quantsapp (fetched 5 Nov 2026) — [Quantsapp, official](https://new.quantsapp.com/); Sensibull Pro: OI analysis, IV chart, Strategy Builder, live options charts (updated 23 Jul 2026) — [Sensibull help, official](https://sensibull.freshdesk.com/support/solutions/articles/43000586718-what-are-the-charges-of-sensibull-)
- **Backtesting:** options backtests with 7.5+ years of history, slippage and brokerage (AlgoTest) — [AlgoTest, vendor](https://algotest.in/blog/algotest-vs-sensibull.md); 200–1,200 screener backtests a year (Trendlyne GuruQ/StratQ, checked 24 Oct 2026) — [Tapetide, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india); Streak backtests and virtual deployment (free for Zerodha users since 17 Jan 2024) — [Z-Connect, official](https://zerodha.com/z-connect/updates/zerodha-users-now-have-unlimited-access-to-streak)
- **Forward or paper testing:** AlgoTest forward test at 50 credits and Tradetron's free paper tier (as of Apr 2026) — [AlgoTest, competitor](https://algotest.in/blog/algo-trading-software-price/)
- **Universe-wide intraday scanning with webhooks:** Chartink Premium, about 1-minute data, 1–3 minute timeframes, webhook alerts (2026) — [Strike, competitor](https://www.strike.money/reviews/chartink)
- **Licensed live data feeds:** Kite Connect data API at ₹500/month (from 6 May 2025) — [Z-Connect, broker](https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework); Dhan Data API at ₹499/month including option chains (checked 13 Oct 2026) — [OneTradeJournal, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers)
- **LLM and natural-language layers:**
  - FIA natural-language screens over price, volume and OI (Apr 2025) — [Tribune/PTI, media](https://www.tribuneindia.com/news/business/fyers-launches-fia-indias-first-ai-powered-screener-creator-for-traders)
  - GR 1 news sentiment (Mar 2026) — [Entrackr, media](https://entrackr.com/news/groww-showcases-ai-powered-investing-tools-at-groww-next-2026-11168623)
  - broker MCP servers (Oct 2026) — [OneTradeJournal, secondary](https://onetradejournal.com/ai-trading/indian-broker-mcp-servers)
- **Fundamentals and composite scores:** DVM scores (daily momentum from 30+ indicators) — [Trendlyne help, official](https://help.trendlyne.com/support/solutions/articles/84000384325-what-does-the-stock-overview-in-the-trendlyne-app-mean-); Mojo Score, Screener.in queries and Tijori operational metrics (Oct 2026) — [Tapetide, competitor](https://tapetide.com/compare/stock-research-subscription-prices-india)
- **Market-context feeds:**
  - India VIX — [NSE via Business Standard, media](https://www.business-standard.com/amp/article/press-releases/nse-announces-the-launch-of-india-vix-110071900094_1.html)
  - FII/DII provisional data — [NSE, official](https://www.nseindia.com/reports/fii-dii)
  - F&O pre-open session (from 8 Dec 2025) — [Business Standard, media](https://www.business-standard.com/markets/capital-market-news/nse-to-commence-pre-opening-session-in-f-o-segment-from-december-08-125110400728_1.html)
  - Tuesday Nifty expiry (from 1 Sep 2025) — [Business Standard, media](https://www.business-standard.com/markets/news/nse-bids-adieu-to-thursday-expiry-as-dates-swap-come-into-effect-explained-125082800635_1.html)
- **Compliance-ready execution:** static-IP whitelisting, daily 2FA, 10 OPS limit and MPP conversion (from 1 Apr 2026) — [FYERS notice, broker](https://fyers.in/notice-board/new-sebi-framework-for-retail-algo-trading-from-april-01-2026); [Zerodha support, broker](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/static-ip)

### Inferences
- **Highest-value additions for an NSE intraday bot** (my ordering):
  1. a licensed live feed (₹500/month) to replace Yahoo for ORB and VWAP accuracy
  2. a backtest and forward-test harness for its own setups
  3. India VIX and expiry-calendar filters
  4. option-chain OI, PCR and max pain for NIFTY levels
  5. FII/DII and GIFT Nifty pre-market context
- **Where the bot is ahead:** none of the reviewed Indian tools documents liquidity-pool, equal-highs/lows or sweep detection, or a multi-factor bias score with explicit R:R setups. That is an absence of evidence, not proof.

### Gaps
- I found no head-to-head accuracy or performance data for any Indian tool's signals, so this comparison is by features only.
