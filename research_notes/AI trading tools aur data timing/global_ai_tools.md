# Global AI-powered trading and market-analysis tools for retail traders: how they work, evidence, pricing, India/NSE fit (as of 5 Nov 2026)

How dates work in these notes: "fetched 5 Nov 2026" means the vendor's own page was read on that date. Third-party prices and features are marked "third-party" and should be treated as unverified. Several official pages (Danelfin, Kavout pricing, Liberated Stock Trader, the FXStreet TradingView press release) returned HTTP 403 or 404, so some facts rely on search snippets or secondary sources, and those are flagged. The personal bot is described from the assignment brief: a rule-based Python tool for NSE, Binance crypto and Yahoo forex that computes CPR, pivots, PDH/PDL, PWH/PWL, ORB, VWAP, swing S/R with confluence weights, liquidity pools, sweep detection, a vote-based bias score, and breakout and dip-buy setups. It sends output to a dashboard and Telegram, has no backtesting, and uses free, possibly delayed data.

## 1. Which tools matter most in 2026, and what is new in 2025–2026?

### Takeaway
The field has split into five groups:
- **Charting platforms adding LLM layers:** TradingView, with an AI Screener (Aug 2026) and AI Copilot (Oct 2026); TrendSpider; and LuxAlgo, which now runs its own platform.
- **Signal and scanner engines:** Trade Ideas Holly and Tickeron.
- **ML stock-rating services:** Danelfin and Kavout.
- **Broker-embedded pattern-recognition vendors:** Autochartist and Trading Central.
- **Natural-language and no-code automation:** Composer and Capitalise.ai, now part of Kraken.

On top of these, LLM assistants and broker "agentic" interfaces spread quickly in 2025–2026: Perplexity Finance India, Robinhood Cortex and Agentic Trading, Zerodha Kite MCP, Groww GR1 and FYERS–ChatGPT. For an NSE trader, only TradingView (and indicators running on it), Perplexity, the Indian-broker AI tools and general LLMs have real Indian-market coverage. Most US AI tools do not cover NSE.

### Cited Findings
**Charting platforms with new AI layers**
- TradingView's AI Screener turns a plain-language description into Stock Screener filters and columns. It is in public beta, works only in the Stock Screener, gives the best results in English, and the support page says it is "not supported on mobile devices" — [TradingView support: How to use the AI Screener](https://br.tradingview.com/support/solutions/43000785770/). A third-party guide says it checked the feature against TradingView's launch announcement on 18 Aug 2026 — [Pineify guide](https://pineify.app/tradingview-ai-screener); see also [FX News Group](https://fxnewsgroup.com/forex-news/platforms/tradingview-introduces-ai-screener/).
- TradingView's plan table (fetched 5 Nov 2026) lists monthly "AI screener requests" per plan: Basic gets preset requests only, Essential 100, Plus 150, Premium 250, Ultimate 500 — [TradingView pricing](https://www.tradingview.com/pricing/).
- TradingView announced "AI Copilot", an assistant that works directly on charts, in a press release dated 20 Oct 2026 (per the URL timestamp; the page returned 403) — [FXStreet press release](https://www.fxstreet.com/press-releases/tradingview-launches-ai-copilot-an-ai-assistant-that-works-directly-on-your-charts-202610201208). Feature details are in Section 2, from [TradingView support: Getting started with AI Copilot](https://in.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/).
- LuxAlgo is no longer only a TradingView-indicator vendor. Its pricing page (fetched 5 Nov 2026) describes:
  - its own browser charting platform, "Vela", covering stocks, ETFs, crypto, forex and commodities;
  - "PineTS", its open-source runtime for Pine Script;
  - order-flow trade and quote history;
  - a coding agent called "Quant" that "writes, tests, and runs indicators and strategies";
  - a new top tier, "AI Ultra", at $229.99/month billed monthly.

  Source: [LuxAlgo pricing (markdown)](https://www.luxalgo.com/pricing.md).
- All TrendSpider plans include "AI-Powered Backtesting", "Automated Trendlines & Fibs", "Chart Pattern Recognition", trading bots and Sidekick AI messages (fetched 5 Nov 2026) — [TrendSpider pricing](https://trendspider.com/pricing/). Its AI Strategy Lab trains machine-learning models — [TrendSpider AI Strategy Lab product page](https://trendspider.com/product/machine-learning-quant-trading-strategy-lab/).

**Broker-embedded analytics vendors**
- Trading Central launched FIBI, a generative-AI assistant built on its "proprietary natural language processing (NLP), language model (LM), and generative AI (GenAI) technologies", on 16 Sep 2025 — [FXStreet press release](https://www.fxstreet.com/press-releases/trading-central-launches-fibi-ai-powered-financial-assistant-live-across-research-tools-202509160742). It signed a partnership with Derayah Financial in Saudi Arabia in July 2026 — [Trading Central blog](https://www.tradingcentral.com/blog/trading-central-announces-partnership-with-derayah-financial-offering-ai-solutions-to-saudi-investors-for-the-first-time).
- oneZero acquired Autochartist. Competitor Acuity Trading has added chart-pattern detection, which Finance Magnates calls "table stakes for brokers" — [Finance Magnates](https://www.financemagnates.com/forex/products/acuity-catches-up-to-autochartist-as-chart-pattern-detection-becomes-table-stakes-for-brokers/).

**Natural-language and no-code automation**
- Kraken announced on 20 Aug 2025 that it had acquired Capitalise.ai, an Israeli no-code, natural-language trading-automation firm. The technology is to be rolled into Kraken Pro in phases — [Kraken/Payward press release](https://www.payward.com/press-release/kraken-acquires-capitalise-ai-trading-automation); [Finextra](https://www.finextra.com/newsarticle/46480/kraken-acquires-capitaliseai); [Crowdfund Insider](https://www.crowdfundinsider.com/2025/08/247795-kraken-announces-acquisition-of-israel-based-no-code-trading-automation-firm-capitalise-ai/).
- Composer offers "Trade with AI" on every plan (fetched 5 Nov 2026) — [Composer pricing](https://www.composer.trade/pricing). A Composer MCP server is also listed — [Glama MCP listing](https://glama.ai/mcp/servers/@invest-composer/composer-trade-mcp/tree/88e53a0f9e001a5e33ba953a24b9f971b88747a2).
- On 12 Aug 2026 Tickeron promoted "AI Trading Agents" built on its "Financial Learning Models (FLMs)" — [FinancialContent/PRLog release](https://www.financialcontent.com/article/prlog-2026-8-12-tickeron-highlights-ai-trading-agent-performance-across-multiple-market-sectors).

**LLM assistants and broker AI**
- Perplexity Finance added NSE and BSE data free for all users on 13 Aug 2025. It later added live earnings-call transcripts for Indian companies — [Outlook Business](https://www.outlookbusiness.com/deeptech/artificial-intelligence/perplexity-adds-live-transcripts-india-market-data-to-finance-dashboard-free-access-for-users); [Analytics India Magazine](https://analyticsindiamag.com/ai-news-updates/perplexity-finance-expands-to-indian-stock-markets).
- Robinhood:
  - Cortex, its AI research assistant, launched in March 2025 — [Benzinga](https://www.benzinga.com/25/03/44530226/robinhood-launches-ai-investment-tool-cortex-to-expand-market-analysis-access-a-premium-research-assistant-right-).
  - Cortex Digests reached the UK on 19 Aug 2025 and had been used by nearly 1 million customers — [Robinhood newsroom](https://robinhood.com/newsroom/digests-by-robinhood-cortex-uk/).
  - "Agentic Trading" (beta) launched on 27 May 2026 through Robinhood MCP servers — [Robinhood newsroom](https://robinhood.com/newsroom/robinhood-is-now-open-to-agents).
- Zerodha's hosted Kite MCP server at `https://mcp.kite.trade/mcp` connects a Kite account to assistants such as Claude, and to editors such as Cursor and Windsurf — [Zerodha TradingQnA announcement](https://tradingqna.com/t/introducing-kite-mcp-connect-your-kite-account-to-ai-assistants/181830).
- Groww unveiled GR1, an opt-in AI investing assistant, at Groww Next on 28 Feb 2026 — [Entrackr](https://entrackr.com/news/groww-showcases-ai-powered-investing-tools-at-groww-next-2026-11168623); [YourStory](https://yourstory.com/2026/02/groww-unveils-ai-enabled-platform-to-expand-investment-basket).
- FYERS announced what it calls India's first AI stock-market assistant integrated with ChatGPT (date not confirmed) — [Digital Terminal](https://digitalterminal.in/solutions/fyers-launches-indias-first-ai-stock-market-assistant-integrated-with-chatgpt).
- Kotak Neo became a TradingView broker partner in May 2026 (secondary source) — [Pulse](https://www.pulse.bot/banking/news/kotak-neo-joins-tradingview-as-broker-partner-3d26c8cc-65db-49bf-bbcb-538f6013d488/).

**Live-money LLM trading benchmark (new in 2025–2026)**
- Nof1's "Alpha Arena" gave each LLM $10,000 to trade live:
  - Season 1 ran in crypto, about 18 Oct to 3–4 Nov 2025 — [GN Crypto](https://www.gncrypto.news/news/qwen-wins-alpha-arena-season-1-with-22-percent-returns/).
  - Season 1.5 switched to US equities, with four simultaneous competitions over about two weeks — [Forklog](https://forklog.com/en/news/ai-model-grok-4-2-triumphs-in-trading-tournament).

### Inferences
- The biggest change in 2026 is that LLM assistants now sit inside the charting tool (TradingView Copilot, LuxAlgo Quant, TrendSpider Sidekick) and inside brokers (Robinhood, Kite MCP, Groww, FYERS). These assistants can draw levels, write scripts, build screens and place or stage orders on request. That overlaps directly with the bot's job of putting levels and setups on a dashboard.
- Most tools in the brief are built for US markets: Trade Ideas, TrendSpider, Danelfin, Kavout and Composer. Autochartist and Trading Central are sold through brokers, mainly FX/CFD brokers outside India. For NSE, the practical comparison set is TradingView (including LuxAlgo-style scripts and Copilot), Perplexity Finance, Indian-broker AI tools (Kite MCP, GR1, FYERS–ChatGPT) and general LLMs.

### Gaps
- I could not find official launch dates for LuxAlgo Vela, Quant or AI Ultra, so I don't know exactly when in 2025–2026 LuxAlgo moved to its own platform.
- I did not fetch the official FYERS or Upstox AI announcements. Upstox's "Algoverse, MCP AI" comes only from a listicle — [TaxGuru](https://taxguru.in/finance/top-ai-based-stock-brokers-india.html). I found no AI-assistant launch for Dhan or Angel One. The only Angel One item was internal use: support chatbots and multilingual AI podcasts — [NiftyTrader](https://www.niftytrader.in/markets/?p=19114).
- I could not verify any official OpenAI or Anthropic retail-trading product (for example, built-in real-time quotes in ChatGPT) from a primary source this session. See Section 2.

## 2. How each tool works: model, inputs, outputs, update frequency, validation, pricing, India/NSE coverage

### Takeaway
Almost none of these tools is "AI predicting price" end to end. They fall into four types:
- **Hand-written or algorithmic rules:** TradingView and LuxAlgo indicators, Capitalise.ai and Composer logic.
- **Statistical pattern recognition:** Autochartist, Trading Central, and TrendSpider's automated trendlines and patterns.
- **Statistical selection or ML ranking:** Holly's nightly backtest selection, Danelfin and Kavout scores, Tickeron FLMs, and TrendSpider's user-trained models.
- **LLM layers that translate language into these mechanics or summarize data:** TradingView Copilot and Screener, LuxAlgo Quant and Backtesting Assistant, Sidekick, FIBI, Composer "Trade with AI", Perplexity, Robinhood Cortex.

Backtesting is standard almost everywhere: TrendSpider on all plans, Composer's free tier, Trade Ideas OddsMaker in Premium, LuxAlgo's assistant. The bot has no backtesting at all.

### Cited Findings

#### TradingView (charting platform; AI Screener; AI Copilot; Pine Script ecosystem)
- **Pricing (official, fetched 5 Nov 2026, annual billing; shown in EUR, localized):** Basic €0; Essential €12.95/mo; Plus €29.95/mo; Premium €59.95/mo; Ultimate €199.95/mo — [TradingView pricing](https://www.tradingview.com/pricing/).
  - A third-party aggregator lists higher monthly-billing figures: Plus $34.95, Premium $69.95, Ultimate $199.95 — [PricingSaaS](https://pricingsaas.com/companies/tradingview).
- **Limits (official, fetched 5 Nov 2026), Basic / Essential / Plus / Premium / Ultimate:**
  - Indicators per chart: 2 / 5 / 10 / 25 / 50.
  - Price alerts: 3 / 20 / 100 / 400 / 1,000.
  - Technical alerts: 20 / 100 / 400 / 1,000 on the paid plans.
  - Historical bars: 5K / 10K / 10K / 20K / 40K.
  - Watchlist alerts: only on Premium (2) and Ultimate (15).

  Source: [TradingView pricing](https://www.tradingview.com/pricing/).
- **AI Copilot working model:** an LLM-style assistant in the Supercharts side panel. TradingView says it "sees what's on your chart" and claims "Every number in its answers is grounded in TradingView data." Source for this and the next five bullets: [TradingView support: AI Copilot](https://in.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/).
- **Copilot inputs:** quotes, indicators, financials, news, earnings, economic calendars, Screener data and country macro data.
- **Copilot outputs:**
  - Changes chart setup (symbols, timeframes, layouts, indicators) from text.
  - Draws support and resistance, chart patterns, and market structure, "including order blocks, fair value gaps, and BOS/CHoCH".
  - Covers multi-timeframe trend, key levels, RSI divergences and moving-average signals.
  - Runs natural-language screens across stocks, crypto, ETFs and bonds.
  - Writes, checks, applies and saves Pine Script, and reads strategy backtest results.
  - Creates single- or multi-condition alerts and watchlists.
- **Copilot access:** a separate monthly add-on for paid plans (Essential to Ultimate). It has a monthly usage limit "that most people won't reach" (no number given), and it is "not available in the mobile apps yet".
- **Copilot disclaimers:** "AI Copilot is an assistant, not an advisor"; "It can be wrong or use outdated information."
- **Update frequency:** charts and alerts run on streaming data where the user has real-time entitlement; Copilot answers on demand. This is inferred from the product description; there is no explicit latency spec.
- **Validation:** strategy backtesting in Pine. Copilot can "read strategy backtest results" — [TradingView support: AI Copilot](https://in.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/). TradingView also documents repainting rules and says scripts that leak future data through `lookahead` "will be moderated" — [Pine Script docs: Repainting](https://www.tradingview.com/pine-script-docs/concepts/repainting/).
- **India/NSE:**
  - Free users now reportedly see NSE prices about 15 minutes delayed, marked "D" — [Algotest blog](https://algotest.in/blog/tradingview-charts-showing-delayed-data/); [FYERS community](https://fyers.in/community/t/nse-data-delayed-on-tradingview-here-s-what-you-can-do/24313).
  - A TradingQnA thread notes that TradingView docs still describe real-time NSE data as the default for non-professionals, so sources conflict — [TradingQnA](https://tradingqna.com/t/why-is-no-one-talking-about-this-tradingview-data-delay/198284).
  - Real-time NSE is available via a paid data add-on or by linking a broker such as Dhan or FYERS — [Algotest blog](https://algotest.in/blog/tradingview-charts-showing-delayed-data/).
  - Kotak Neo became a TradingView broker partner in May 2026 — [Pulse](https://www.pulse.bot/banking/news/kotak-neo-joins-tradingview-as-broker-partner-3d26c8cc-65db-49bf-bbcb-538f6013d488/).

#### LuxAlgo (indicator vendor turned platform; SMC/price-action toolkits; LLM coding and backtest agents)
- **Pricing (official, fetched 5 Nov 2026, USD list):**

  | Plan | Monthly billing | Annual billing |
  |---|---|---|
  | Free | $0 | n/a |
  | Essential | $39.99/mo | $24.99/mo ($299.88/yr) |
  | Premium | $67.99/mo | $39.99/mo ($479.88/yr) |
  | Ultimate | $119.99/mo | $59.99/mo ($719.88/yr) |
  | AI Ultra | $229.99/mo | $119.99/mo ($1,439.88/yr) |

  Every plan has a 30-day money-back guarantee — [LuxAlgo pricing](https://www.luxalgo.com/pricing.md).
- **Limits (official, fetched 5 Nov 2026), Free / Essential / Premium / Ultimate / AI Ultra:**
  - Custom alerts: 5 / 50 / 100 / 200 / 500. Price alerts are unlimited on every plan.
  - Historical bars: 5K / 10K / 20K / 30K / 50K.
  - Order-flow lookback: 1 day / 30 days / 90 days / 1 year / full history.
  - Alerts go to email, push, Telegram, Discord or Slack. Webhooks to bots or brokers need a paid plan, and paid alerts can fire before the bar closes.

  Source: [LuxAlgo pricing](https://www.luxalgo.com/pricing.md).
- **Working model, indicators:** the Library of "800+ advanced tools" (Wyckoff, chart patterns, smart money concepts, volume, momentum, trend) is algorithmic, rule-based code, with versions for TradingView, MetaTrader, NinjaTrader and Thinkorswim — [LuxAlgo pricing](https://www.luxalgo.com/pricing.md). The public "Smart Money Concepts [LuxAlgo]" script has a "Bars Confirmation" setting that controls how many bars confirm equal highs and lows — [TradingView script page](https://tradingview.com/script/CnB3fSph-Smart-Money-Concepts-LuxAlgo).
- **Working model, AI:**
  - "Quant" is an LLM coding agent that writes, tests and runs indicators and strategies on the chart. It shares a usage pool with the Backtesting Assistant; usage refills every 5 hours and weekly on Fridays at 5 PM ET, and extra usage is sold in prepaid bundles — [LuxAlgo pricing](https://www.luxalgo.com/pricing.md).
  - The Backtesting Assistant is "a conversational AI leveraging a variety of state of the art large language models". It searches precomputed backtests of strategies built from LuxAlgo toolkits (Signals & Overlays, Price Action Concepts, Oscillator Matrix) — [LuxAlgo docs: AI Backtesting](https://docs.luxalgo.com/docs/ai-backtesting/introduction.md).
  - Strategy counts conflict: the docs claim backtest results for "over 10 million" strategies; a QuantVPS review cites about 6 million across 93 tickers — [QuantVPS review](https://www.quantvps.com/blog/luxalgo-review).
  - Access also conflicts: the docs say the assistant is only for Ultimate users, while the Nov 2026 pricing page says every plan, Free included, gets the usage pool.
- **Data (official):** Vela archives hold 8+ years of US equities (OHLCV, trades, L1 quotes), 16+ years of futures, 10+ years of crypto OHLCV, and 10+ years of forex OHLCV only. Live CME futures need a paid plan — [LuxAlgo pricing](https://www.luxalgo.com/pricing.md).
- **India/NSE:** LuxAlgo's NSE coverage on TradingView depends on TradingView's NSE data. The pricing page does not mention Indian equities in Vela.

#### TrendSpider (automated technical analysis, classical ML lab, LLM Sidekick, bots)
- **Pricing (official, fetched 5 Nov 2026, during an "Election Day" promotion):**
  - Listed "/month" prices: Standard $32.94, Premium $45.50, Enhanced $52.46, Advanced $74.90.
  - "Then" ranges go up to $75.65 (Standard), $126.65 (Premium), $169.15 (Enhanced) and $296.65 (Advanced) per month.
  - Discounts of "up to 65% off your first year" (Advanced) down to 39% (Standard); 7-day trial for $7; promo terms "final and non-refundable".
  - The page does not say which figures are monthly or annual billing.

  Source: [TrendSpider pricing](https://trendspider.com/pricing/).
- **Limits (official, fetched 5 Nov 2026), Standard / Premium / Enhanced / Advanced:**
  - Bots: 5 / 10 / 50 / 100.
  - Alerts: 10 / 50 / 100 / 400.
  - Backtest resolution and depth: 2-hour bars, 2K / 5-min, 10K / 1-min, 20K / 1-min, 30K.
  - Symbols per test: 50 / 150 / 250 / 510.
  - Sidekick AI: 25 messages/month on all plans. The page also says "10 free messages" elsewhere, which conflicts.
  - 5 free SignalStack automated orders per month.

  Source: [TrendSpider pricing](https://trendspider.com/pricing/).
- **Working model:**
  - (a) Algorithmic auto-detection of trendlines, Fibonacci levels and chart patterns. All plans include "Automated Trendlines & Fibs" and "Chart Pattern Recognition" — [TrendSpider pricing](https://trendspider.com/pricing/).
  - (b) User-trained classical ML in AI Strategy Lab, with four model types: Random Forest, Naive Bayes, KNN and logistic regression. The user picks inputs and a target, then clicks "Train" — [TrendSpider product page](https://trendspider.com/product/machine-learning-quant-trading-strategy-lab/); [PR Newswire launch](https://prnewswire.com/news-releases/trendspider-launches-ai-strategy-lab-to-empower-investors-to-build-custom-ai-powered-trading-models-with-ease-302306657.html).
  - (c) The Sidekick LLM assistant.
- **Validation:** all plans list backtesting, "Multi-symbol and Variance Testing" and "AI-Powered Backtesting" — [TrendSpider pricing](https://trendspider.com/pricing/). A vendor case study on SPY trained RSI-based KNN and Random Forest models and calls out-of-sample testing "the first step in validating an AI strategy". It reports a 119.4% return for the adjusted strategy; this is a vendor example, not independent — [TrendSpider blog](https://trendspider.com/blog/building-a-strategy-with-ai-strategy-lab/).
- **Data and update:**
  - US stocks and ETFs real-time, free for non-professionals; professionals pay $29/mo for NASDAQ.
  - Futures $7.50/mo; OPRA options $9.50/mo.
  - CBOE indexes delayed 10–15 minutes.
  - Forex and crypto have "Global" real-time feeds.
  - The page does not mention Indian or other international equities.

  Source: [TrendSpider pricing](https://trendspider.com/pricing/).

#### Trade Ideas (real-time US scanner; Holly AI)
- **Pricing (official, fetched 5 Nov 2026):**
  - TI Free: market dashboards with 15-minute delayed data.
  - TI Standard: $127/mo, or $89/mo billed annually ($1,068/yr).
  - TI Premium: $254/mo, or $178/mo billed annually ($2,136/yr).

  Source: [Trade Ideas pricing](https://www.trade-ideas.com/pricing/). An unnamed 2026 third-party review in the search results gives Standard at $118/mo and Premium at $228/mo or $2,268/yr, which conflicts with the official page. I could not tell which site it came from, so treat it as unverified; similar figures appear on affiliate and competitor sites such as [AlphaSignal](https://alphasignal-56o.pages.dev/blog/trade-ideas-standard-vs-premium/) and [Walnut Invest](https://walnutinvest.com/resources/trade-ideas-review) (Walnut is a competitor).
- **What each tier includes (official):**
  - Standard: real-time data, streaming alerts, Formula Editor, an "AI Assistant", paper trading, Brokerage Plus and broker API connections.
  - Premium adds: Holly AI buy/sell signals, OddsMaker backtesting, the Money Machine Simulator (which "currently places no live orders"), auto trading on your own strategies, and "Smart Risk Levels".

  Source: [Trade Ideas pricing](https://www.trade-ideas.com/pricing/).
- **Holly working model (official wording):** Holly "backtests her strategies nightly and selects the strongest for the next day" — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/). So Holly is a nightly statistical selection over a library of rule-based scan strategies, not a price-forecasting neural network (see Inferences).
- **Markets:** US exchanges (NYSE, NYSE Arca, NASDAQ, AMEX, Pink Sheets, OTCQB, BATS) plus Canada via TSX (limited). No other markets are listed — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/).

#### Tickeron (pattern recognition, "AI Robots" and "AI Trading Agents" built on proprietary FLMs)
- **Working model (vendor):** "Financial Learning Models (FLMs)" are trained on "patterns, indicators, and fundamental data" — [PR Newswire: Tickeron FLM platform](https://prnewswire.com/news-releases/tickeron-pioneers-the-flm-platform-for-producing-hundreds-of-ai-trading-bots-with-positive-alpha-302290913.html). The 2026 AI Trading Agents use FLMs that analyze market data, technical indicators and price behavior. Tickeron also offers an "Ask AI" research assistant — [FinancialContent, 12 Aug 2026](https://www.financialcontent.com/article/prlog-2026-8-12-tickeron-highlights-ai-trading-agent-performance-across-multiple-market-sectors).
- **Validation (vendor):** published agent figures "represent historical backtested or platform-reported strategy performance, depending on the individual Trading Agent, and are provided for informational purposes only" — [FinancialContent, 12 Aug 2026](https://www.financialcontent.com/article/prlog-2026-8-12-tickeron-highlights-ai-trading-agent-performance-across-multiple-market-sectors).
- **Pricing (third-party, unverified, conflicting):** an "AI Trading Robots & Real-Time Patterns" plan at $35/mo with a 14-day free trial — [Stork](https://www.stork.ai/en/tickeron). Another source gives about $65/mo for the AI Robots plan — [AlphaSignal comparison](https://alphasignal-56o.pages.dev/blog/tickeron-vs-trade-ideas/). Stork reports a Trustpilot score of 3.4/5 — [Stork](https://www.stork.ai/en/tickeron).
- **India/NSE:** no evidence of NSE coverage was found (see Gaps).

#### Danelfin (ML stock and ETF rating, 1–10 "AI Score")
- **Working model and outputs:** the AI Score (1–10) rates a stock's probability of beating the market over the next 3 months, with Technical, Fundamental and Sentiment subscores — [Danelfin: How it works (search snippet; page returned 403)](https://danelfin.com/how-it-works); [Danelfin support](https://support.danelfin.com/hc/en-us/articles/4404382038545).
- **Vendor validation (blog, 7 Jul 2025, new US model):**
  - AI Score 10 stocks: "+21.05% annualized alpha" vs the S&P 500, up from +15% under the previous model. AI Score 1: −33.28%.
  - Backtest window: 3 Jan 2017 to 1 Apr 2025.
  - Sample: 2,072 trading days × 5,616 stocks = 11,636,352 observations.
  - Method: average alpha after 3 months per AI Score, calculated daily.
  - Historical scores were recalculated for the new model.
  - No audit is mentioned. Disclaimer: "Backtested performance is not an indicator of future results."

  Source: [Danelfin blog](https://blog.danelfin.com/?p=4653).
- **Older vendor figure:** +14.69% annualized alpha for US AI Score 10 stocks "in the last 7 years" — [Danelfin support (search snippet)](https://support.danelfin.com/hc/en-us/articles/4404382344465-Are-AI-Scores-reliable-How-successful-were-AI-Scores-predictions-in-the-past).
- **Universe:** US-listed stocks, with separate models for ETFs and European stocks — [Danelfin blog](https://blog.danelfin.com/?p=4653). No India coverage was found.
- **Pricing:** the official pricing page returned 403. Third-party listings conflict, from about $17 to $79/mo, and one gives Pro at about $840/yr — [Walnut Invest](https://walnutinvest.com/resources/danelfin-review); [PriceMyAI](https://pricemyai.pages.dev/pricing/danelfin/). All unverified.

#### Kavout (ML "K Score" plus LLM research agents)
- **Official site disclaimer (fetched 5 Nov 2026):** "Real-time quotes and financial data are provided for U.S. stocks, ETFs, cryptocurrencies, and major forex pairs". Commodity futures and indices "may be delayed by approximately 15–20 minutes". "Past performance does not guarantee future results." The navigation lists "Investgpt", "Financial Agents" and "Smart Signals" — [Kavout](https://www.kavout.com/).
- **K Score (third-party, unverified):** an ML rating on a 1–9 scale that distills "200+ factors". The methodology is "not fully disclosed" — [Tooliverse](https://tooliverse.ai/tools/kavout); [Stork](https://www.stork.ai/ja/kavout).
- **Pricing (third-party, unverified):** a free tier with 10 research credits per month; Pro at about $16–$20/mo — [AIPicks 2026 review](https://aipicks.jp/mag/kavout-review-2026); [Stork](https://www.stork.ai/ja/kavout). The official /pricing URL returned 404.
- **India/NSE:** the official site does not mention it.

#### Autochartist (broker-distributed pattern-recognition engine)
- **Working model:** "pattern recognition engines that continuously monitor financial instruments". They detect:
  - chart patterns: triangles, wedges, head-and-shoulders, channels;
  - Fibonacci and harmonic patterns: Gartley, Butterfly;
  - "Key Levels", which are horizontal support and resistance.

  Each pattern carries quality scores for how evenly spaced its key points are and how clean it looks — [Spotware integration page](https://spotware.com/vi/integrations/autochartist); [CMC Markets](https://www.cmcmarkets.com/en-ie/trading-platform/mt4/autochartist); [Autochartist user manual (HotForex)](https://static.hotforex.com/assets/common/documents/manuals/Autochartist_User_Manual-SV.pdf); [EarnForex review](https://earnforex.com/guides/autochartist-review).
- **Outputs:** Key Levels come as "breakout signals and approaching signals". A volatility analysis helps place stop-loss and take-profit — same sources as above.
- **Distribution and price:** B2B. Brokers embed it in MT4, MT5 and cTrader, including Saxo, OANDA, Swissquote, Pepperstone, IC Markets and CMC; it is acquired by oneZero — [Finance Magnates](https://www.financemagnates.com/forex/products/acuity-catches-up-to-autochartist-as-chart-pattern-detection-becomes-table-stakes-for-brokers/); [IC Markets launch](https://financefeeds.com/pr/ic-markets-launches-autochartist-clients-mt4-mt5-ctrader/). Autochartist also sells brokers a product built on TradingView Advanced Charts — [TradingView blog](https://www.tradingview.com/blog/en/tradingview-advanced-charts-and-autochartist-broker-tools-39940).
- **India/NSE:** no Indian-broker partnership was found — [search result set incl. Saxo, IC Markets](https://www.financemagnates.com/forex/brokers/saxo-bank-integrates-trading-signals-capabilities-of-autochartist/).

#### Trading Central (broker-distributed research: pattern recognition, trade plans, FIBI LLM)
- **Working model:** Technical Insight is "US patented chart pattern recognition software to find, validate, and time trades". It identifies bullish or bearish "Technical Events®" by combining pattern recognition with a broad range of technical indicators — [Trading Central blog: Technical Insight Trader Edition](https://tradingcentral.com/blog/technical-insight-r-trader-edition-empower-investors-to-find-validate-and-time-their-trades); [Trading Central research products](https://www.tradingcentral.com/research-products).
- **Outputs:** "Technical Views" provides "concise, actionable trading plans with full position management". FIBI adds NLP and GenAI summaries — [Trading Central research products](https://www.tradingcentral.com/research-products); [FXStreet FIBI release](https://www.fxstreet.com/press-releases/trading-central-launches-fibi-ai-powered-financial-assistant-live-across-research-tools-202509160742).
- **Scale:** used by "1.3M investors across 40+ brokers" (vendor claim) — [Trading Central research products](https://www.tradingcentral.com/research-products).
- **Business model:** brokers pay to integrate it, so retail users get it free through a broker — [DayTrading.com](https://daytrading.com/trading-central). The industry awards it cites are not performance audits — [Trading Central awards](https://www.tradingcentral.com/awards/trading-central-for-best-ai-solution).
- **India/NSE:** the only India link found is an IIFL news page about Trading Central's awards. No partnership was confirmed — [IndiaInfoline](https://www.indiainfoline.com/news/business/trading-central-wins-at-the-technical-analyst-awards).

#### Composer (no-code rule-based "symphonies" with an LLM builder and automated execution, US only)
- **Pricing (official, fetched 5 Nov 2026):**
  - Starter $0: first automated strategy; unlimited no-code building and backtesting; "Trade with AI".
  - Advanced $10/mo: up to 5 automated strategies.
  - Pro $32/mo, or $384/yr: up to 500 strategies, API access, and "priority automated trade timing near market close".
  - Business: by call.

  Source: [Composer pricing](https://www.composer.trade/pricing).
- **Working model:** the AI "will assist you in creating a symphony based on common patterns from community-built symphonies", and the user reviews and confirms every symphony before it runs — [Composer help: What is Trade with AI?](https://help.composer.trade/article/254-what-is-trade-with-ai). The LLM drafts deterministic rules; it does not trade on its own judgment.
- **Custody and jurisdiction:** Composer Securities LLC (an SEC-registered broker-dealer, FINRA/SIPC member), with accounts carried by Alpaca Securities and Apex Clearing. "Not made in any jurisdiction where Composer Securities is not registered" — [Composer pricing](https://www.composer.trade/pricing).

#### Capitalise.ai (natural-language to rule automation, now Kraken)
- **Working model:** turns plain-language instructions into strategies that can be backtested and run automatically: "no-code trading strategy research, design, backtesting and automated execution across asset classes". Founded in 2015 and previously used by traditional brokers and exchanges — [Kraken/Payward press release](https://www.payward.com/press-release/kraken-acquires-capitalise-ai-trading-automation); [Pulse 2.0](https://pulse2.com/kraken-buying-no-code-trading-automation-company-capitalise-ai); [Finextra](https://www.finextra.com/newsarticle/46480/kraken-acquires-capitaliseai).
- **Status:** acquired by Kraken on 20 Aug 2025, with a phased integration into Kraken Pro. Kraken's stated goal is to cover digital and traditional asset classes — [Crowdfund Insider](https://www.crowdfundinsider.com/2025/08/247795-kraken-announces-acquisition-of-israel-based-no-code-trading-automation-firm-capitalise-ai/).

#### LLM assistants and broker-built AI
- **Perplexity Finance (India):** free live NSE and BSE prices, explanations of price moves, historical data downloads and earnings; later, live earnings-call transcripts for Indian companies — [Outlook Business](https://www.outlookbusiness.com/deeptech/artificial-intelligence/perplexity-adds-live-transcripts-india-market-data-to-finance-dashboard-free-access-for-users); [Marketcalls](https://www.marketcalls.in/perplexity/perplexity-finance-now-covers-indian-markets-why-traders-should-care.html). No measured data delay or full instrument-universe test has been published — [OneTradeJournal](https://onetradejournal.com/ai-trading/perplexity-finance-india).
- **Zerodha Kite MCP:** the hosted endpoint needs no install or API keys and "excludes potentially destructive trading operations". The self-hosted MIT-licensed build (GitHub `zerodha/kite-mcp-server`) lets agents fetch data, manage portfolios and execute trades — [LobeHub listing](https://lobehub.com/ja/mcp/zerodha-kite-mcp-server); [Zerodha TradingQnA](https://tradingqna.com/t/introducing-kite-mcp-connect-your-kite-account-to-ai-assistants/181830).
- **Groww GR1:** opt-in, focused on "personalized, guarded insights rather than autonomous trading", and built on MCP with user-specific data — [Entrackr](https://entrackr.com/news/groww-showcases-ai-powered-investing-tools-at-groww-next-2026-11168623); [NewsBytes](https://www.newsbytesapp.com/news/science/growws-new-agentic-ai-to-redefine-personal-investing-experience/tldr). The stance across Indian brokers is that AI "can analyse, summarise and personalise—but not decide" — [NiftyTrader](https://www.niftytrader.in/markets/?p=19114).
- **Robinhood:**
  - Axios describes Cortex as having access to real-time market data, analyst reports and research — [Axios, Dec 2025](https://www.axios.com/2025/12/17/ai-robinhood-stock-market). It launched for Gold subscribers — [Rallies.ai](https://rallies.ai/news/robinhood-unveils-cortex-ai-tool-for-gold-subscribers-to-boost-trading-volumes); [Benzinga](https://www.benzinga.com/25/03/44530226/robinhood-launches-ai-investment-tool-cortex-to-expand-market-analysis-access-a-premium-research-assistant-right-).
  - Agentic Trading (beta, 27 May 2026) runs third-party agents through MCP in a separate "agentic account", equities only. Robinhood says it does not control, supervise or audit third-party agents, and the customer bears the risk — [Robinhood newsroom](https://robinhood.com/newsroom/robinhood-is-now-open-to-agents); [InvestmentNews](https://www.investmentnews.com/fintech/robinhood-just-made-a-bold-move-into-ai-powered-trading-for-the-retail-market/266771); [Pulse 2.0](https://pulse2.com/robinhood-launches-agentic-trading-and-ai-credit-card/).
- **ChatGPT (general):** third-party 2026 guides say ChatGPT has no built-in live market feed and gets real-time data through plug-ins or connectors (for example, Benzinga via Firecrawl) — [Firecrawl](https://www.firecrawl.dev/articles/real-time-stock-news-chatgpt); [Dupple guide](https://dupple.com/learn/how-to-use-chatgpt-for-stock-trading). These are low-quality, non-primary sources.

### Inferences
Summary matrix, compiled from the cited findings above. Prices are as of 5 Nov 2026 unless marked.

| Tool | Working model | Main outputs | Update cadence | User-side validation | Price (dated) | NSE |
|---|---|---|---|---|---|---|
| TradingView + AI Copilot/Screener | Rules (Pine) + LLM agent over TradingView data | Charts, drawn S/R and structure, screens, alerts, Pine code | Streaming with entitlement; Copilot on demand | Strategy tester; Copilot reads results | €0–199.95/mo annual; Copilot add-on price not shown | Yes; free tier reportedly 15-min delayed |
| LuxAlgo | Rule-based indicators + LLM coding and backtest agents | Overlays, SMC levels, signals, alerts | Bar or tick (paid alerts can fire intrabar) | Search over precomputed backtests; Quant tests code | $0–229.99/mo | Via TradingView |
| TrendSpider | Algorithmic auto-TA + classical ML (RF/NB/KNN/LR) + LLM | Auto trendlines, Fibs, patterns, bots, alerts | Real-time US, FX, crypto | Backtests, multi-symbol, variance tests | ~$33–75/mo promo | Not listed |
| Trade Ideas Holly | Nightly backtest-based selection of rule strategies | Intraday entry/exit signals, scans | Real-time; strategy set changes nightly | OddsMaker (Premium) | $89–254/mo | No (US/Canada) |
| Tickeron | Proprietary ML ("FLMs") + pattern recognition | Robot or agent trades, pattern alerts | Intraday ("real-time patterns") | Vendor dashboards | $35–65/mo (unverified) | Not found |
| Danelfin | ML classifier/ranker, 3-month horizon | 1–10 score + subscores | Daily | Vendor backtest stats per score | Unverified | No |
| Kavout | ML ranking + LLM agents | 1–9 K Score, agent answers | Real-time quotes, US | None found | ~$16–20/mo (unverified) | No |
| Autochartist | Statistical pattern recognition | Patterns, key levels, volatility SL/TP | Continuous | Pattern quality scores | Free via broker | No Indian broker found |
| Trading Central | Patented pattern recognition + indicator events + trade plans + GenAI | Technical Events, trade plans, FIBI | Continuous | None public | Free via broker | No partnership confirmed |
| Composer | User rules + LLM drafting | Allocation strategies, auto-execution | Daily, near close | Unlimited backtests | $0 / $10 / $32/mo | No (US) |
| Capitalise.ai (Kraken) | NL-to-rules engine | Automated orders | Real-time rule monitoring | Backtesting | Not found | Unknown |
| Perplexity, ChatGPT, Claude, broker AI | LLM over retrieved data, optional broker MCP | Summaries, explanations, trades via MCP | On demand | None | Perplexity Finance free | Perplexity yes; Kite MCP yes |

- The bot's design (hand-written, deterministic rules over price data) belongs to the same family as TradingView and LuxAlgo indicators, Autochartist and Trading Central key levels, and Composer and Capitalise.ai rule engines. It is not in the ML family (Danelfin, Kavout, Tickeron, TrendSpider AI Strategy Lab), and it is not LLM-based.
- Holly's nightly "backtest and select the strongest" loop is a form of statistical model selection. It adapts over time, but it carries data-snooping risk (see Section 4).

### Gaps
- Underlying LLM vendors are not disclosed for TradingView AI Copilot, LuxAlgo Quant, Trading Central FIBI or Groww GR1. A third-party snippet said TrendSpider Sidekick uses Claude Sonnet; this was not verified in TrendSpider documentation.
- The price of the TradingView AI Copilot add-on, and the INR pricing for Indian users, were not found. The pricing page shows only localized annual prices, in EUR when fetched.
- Official prices for Danelfin (403), Kavout (404) and Tickeron were not retrieved. Third-party figures conflict.
- Composer's internal model (if/else logic trees with indicator conditions, rebalanced daily) is described from background knowledge plus the "near market close" wording. It was not fully re-verified this session.
- I don't know whether Capitalise.ai's features are now live in Kraken Pro, or whether they are available to Indian residents.
- Tickeron and Kavout NSE coverage was not confirmed either way. No source mentioned India.
- I did not verify, from a primary source this session, whether Trading Central "Analyst Views" or "Technical Views" are written by human analysts or generated automatically.

## 3. What independent evidence exists on accuracy and performance, as opposed to vendor claims?

### Takeaway
There are no independent audits of signal accuracy for any of the named retail tools. The performance figures (Danelfin +21.05% alpha, Holly about 68% win rate, Tickeron agent returns, the TrendSpider 119.4% case study) are vendor backtests or vendor-reported numbers. The independent evidence that does exist covers LLM trading in general. The academic StockBench benchmark finds that most LLM agents fail to beat buy-and-hold. Nof1's live Alpha Arena showed large dispersion and big losses for several frontier models. Regulators have focused on "AI washing" and AI-bot scams rather than auditing legitimate tools.

### Cited Findings
**Vendor claims, none audited**
- Danelfin: AI Score 10 has "+21.05% annualized alpha" in a backtest from 3 Jan 2017 to 1 Apr 2025, with historical scores "recalculated for the new model". No audit is mentioned, and the site states "Backtested performance is not an indicator of future results" — [Danelfin blog, 7 Jul 2025](https://blog.danelfin.com/?p=4653). An older support page gave +14.69% "in the last 7 years" — [Danelfin support](https://support.danelfin.com/hc/en-us/articles/4404382344465-Are-AI-Scores-reliable-How-successful-were-AI-Scores-predictions-in-the-past).
- Trade Ideas Holly:
  - The pricing page makes no performance claim and only says Holly re-selects strategies nightly from backtests — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/).
  - The roughly 68% win rate repeated in reviews comes from Trade Ideas' internal simulations and "has not been independently audited". User-forum anecdotes put live results at about 45–55%. The source is an affiliate-style site, so this is low reliability — [AlphaSignal Holly review](https://alphasignal-56o.pages.dev/blog/trade-ideas-holly-ai-review/).
  - No audited live track record was found.
- Tickeron: agent figures are "historical backtested or platform-reported", for "informational purposes only" — [FinancialContent, 12 Aug 2026](https://www.financialcontent.com/article/prlog-2026-8-12-tickeron-highlights-ai-trading-agent-performance-across-multiple-market-sectors).
- TrendSpider: the vendor blog reports a 119.4% return on an SPY RSI-model example — [TrendSpider blog](https://trendspider.com/blog/building-a-strategy-with-ai-strategy-lab/).
- Trading Central cites industry awards ("Best A.I. Solution"). These are awards, not audits — [Trading Central awards](https://www.tradingcentral.com/awards/trading-central-for-best-ai-solution).

**Independent and academic evidence on LLM trading**
- StockBench (arXiv 2510.02209; v1 2 Oct 2025, v2 2 Mar 2026): LLM agents received daily prices, fundamentals and news, and made buy/sell/hold decisions over multi-month windows. The abstract says "most models struggle to outperform the simple buy-and-hold baseline", though "some models demonstrate the potential to achieve higher returns and stronger risk management" — [arXiv](https://arxiv.org/abs/2510.02209). A Korean-language secondary summary said the opposite (that most agents beat the baseline); the primary abstract is authoritative — [Liner summary](https://liner.com/ko/review/stockbench-can-llm-agents-trade-stocks-profitably-in-realworld-markets).
- TradeTrap (arXiv, Dec 2025) concludes that autonomous trading agents "can be systematically misled at the system level" under perturbations (abstract only) — [arXiv 2512.02261](https://arxiv.org/abs/2512.02261v1).
- PHANTOM, a benchmark for hallucination detection in long-context financial QA (listed as Goldman Sachs, NeurIPS 2025), is listed but was not verified — [Awesome-LLM-Quant list](https://github.com/Tom-roujiang/Awesome-LLM-Quantitative-Trading-Papers).
- **Alpha Arena Season 1** (live crypto, $10,000 each, about 18 Oct to 3–4 Nov 2025):
  - Qwen 3 Max won with about +22%; DeepSeek V3.1 made about +4.89%.
  - One tally: Claude Sonnet 4.5 −30.8%, Grok 4 −45.3%, Gemini 2.5 Pro −56.7%, GPT-5 −62.7%.
  - Nof1 called the season exploratory, noting its short duration, modest capital and lack of statistical controls.

  Sources: [GN Crypto](https://www.gncrypto.news/news/qwen-wins-alpha-arena-season-1-with-22-percent-returns/); [Decrypt (mid-season)](https://decrypt.co/345006/ai-crypto-trading-showdown-deepseek-grok-winning-gemini-implodes); [Forklog: four of six models lose](https://forklog.com/en/four-out-of-six-ai-models-suffer-losses-in-trading-tournament/).
- **Alpha Arena Season 1.5** (US equities, about two weeks): the winner was reported as Grok 4.20, at about +12% average (+12.11%); GPT-5.1 was second and Gemini 3 third. Reported dollar figures conflict between outlets — [Forklog](https://forklog.com/en/news/ai-model-grok-4-2-triumphs-in-trading-tournament); [AIBase](https://www.aibase.com/news/23442); [Buildix blog (conflicting $ figure)](https://www.buildix.trade/blog/nof1-alpha-arena-lessons-ai-trading-byok-strategy-advisor-2026).

**Regulator actions and warnings**
- **SEC:**
  - The first "AI-washing" settlements came in March 2024 against advisers Delphia ($225,000) and Global Predictions ($175,000), for marketing AI capabilities they did not have — [Mondaq](https://webiis08.mondaq.com/canada/new-technology/1743326/ai-washing-the-new-greenwashing-how-the-secs-emerging-technologies-unit-is-rewriting-the-compliance-landscape).
  - Presto Automation followed on 14 Jan 2025, described as possibly the first AI-washing case against a public company. The SEC's 2026 examination priorities include the accuracy of firms' AI representations. A single secondary source reports three AI-claim actions between 26 Aug and 29 Sep 2026: alleged scams by Cryptoaiml and TSAI Pro, and a settled case against GenesisAI Corp. These were not verified against SEC releases — [TechJack Solutions](https://techjacksolutions.com/ai-brief/sec-ai-washing-enforcement-three-cases-2026/); [Promise Legal](https://blog.promise.legal/ai-washing-compliance-sec-ftc-state-enforcement/).
- **CFTC:** the January 2024 customer advisory "AI Won't Turn Trading Bots into Money Machines" warns against platforms that claim AI algorithms guarantee returns, and says AI cannot foresee sudden market changes — [CFTC release 8854-24](https://www.cftc.gov/PressRoom/PressReleases/8854-24); [Finextra](https://www.finextra.com/newsarticle/43602/cftc-cautions-against-ai-be-wary-of-the-hype).
- **FINRA, SEC and NASAA:** FINRA published "Artificial Intelligence (AI) and Investment Fraud", which covers deepfakes and scam tactics, and the SEC, NASAA and FINRA issued a joint AI investor alert — [Orrick InfoBytes](https://infobytes.orrick.com/2024-02-02/securities-regulators-issue-guidance-and-rfc-ai-trading-scams/); [NFA newsletter, Feb 2024](https://www.nfa.futures.org/investors/investor-newsletters/2024-february.html).
- **BaFin (Germany):** warned about networks of near-identical websites claiming AI automated trading with "self-learning trading bots that promise unrealistically high returns" — [Finance Magnates](https://www.financemagnates.com/forex/regulation/how-fraudsters-use-ai-to-lure-investors-bafin-exposes-the-scam).
- **SEBI (India):**
  - A June 2025 consultation, "Guidelines for Responsible Usage of AI/ML in Indian Securities Markets", proposes that firms using AI/ML for algo trading or advice must disclose this to clients, keep governance and monitoring in place, report accuracy, and retain inputs and outputs for at least 5 years. Comments were due 11 Jul 2025; whether it has been finalized is unclear — [Business Standard](https://www.business-standard.com/markets/news/sebi-proposes-ai-ml-guidelines-for-market-participants-125062001137_1.html); [Business Today](https://www.businesstoday.in/markets/story/sebi-releases-draft-guidelines-for-responsible-ai-use-in-markets-seeks-public-input-by-july-481229-2025-06-20); [Taxmann](https://www.taxmann.com/post/blog/sebi-proposes-ai-ml-governance-framework-for-securities-markets).
  - One report says registered advisers bear full responsibility for errors made by AI tools they use, and that SEBI's "Sudarshan" AI tool monitors online violations (low-quality source) — [Whalesbook](https://www.whalesbook.com/news/English/personal-finance/SEBI-Cracks-Down-on-Unregulated-Finfluencers-and-AI-Advice/69e604a8bca97ee10693e59f).

### Inferences
- For report purposes, every tool's accuracy should be rated "vendor-claimed, unaudited". The only third-party performance data is about general-purpose LLMs (StockBench, Alpha Arena). It points to poor or highly variable results when LLMs make the trading decisions themselves.
- Danelfin's +21% is a retroactive backtest of a model built in 2025, with history recalculated. Live, out-of-sample performance since then is the relevant number, and Danelfin has not published it (see Gaps).
- Regulators are targeting overclaiming and fraud, not legitimate tools. This means the absence of an enforcement action against a vendor says nothing about whether its signals work.

### Gaps
- I found no independent academic or audited study of Trade Ideas Holly, Tickeron, Danelfin, Kavout, Autochartist, Trading Central, LuxAlgo or TrendSpider signals. The Liberated Stock Trader lab tests of Tickeron and Trade Ideas exist, but the pages returned 403, so their results could not be read.
- I found no live, out-of-sample track record from Danelfin after 1 Apr 2025.
- I did not find an ESMA-specific warning on AI trading tools in this session.
- I did not retrieve the primary Nof1 leaderboard. Alpha Arena figures come from crypto and tech media and partly conflict.

## 4. Known weaknesses: overfitting, repainting, survivorship bias, LLM hallucination, delayed data

### Takeaway
The main failure modes are well documented:
- Indicators that "plot in the past", such as pivot, swing and SMC structure, or that use higher-timeframe lookahead, look far better on history than they did live.
- Systems that search millions of backtests, or re-optimize nightly, select for luck.
- LLM assistants can state wrong or stale numbers. Even TradingView's grounded Copilot carries an "it can be wrong or use outdated information" warning.
- Free data for Indian markets is often 15 minutes delayed, which breaks intraday ORB, VWAP and sweep logic.

The bot shares the repainting and pivot-confirmation risk and the delayed-data risk. It avoids LLM hallucination because it is deterministic.

### Cited Findings
**Repainting and future leak**
- TradingView defines repainting as "script behavior causing historical vs realtime calculations or plots to behave differently". Its causes include:
  - fluid realtime OHLC values before the bar closes;
  - `request.security()` with `lookahead_on` and no `[1]` offset, which "will return data from the future on historical bars, which is dangerously misleading";
  - pivot scripts that detect a pivot N bars later but draw it on the pivot bar;
  - `calc_on_every_tick` strategies whose live fills differ from the backtest.

  Fixes: use `barstate.isconfirmed` or `[1]`, apply a `[1]` offset with lookahead on HTF data, and plot pivots without an offset by default. TradingView notes that non-repainting methods "usually produce signals later" — [Pine Script docs: Repainting](https://www.tradingview.com/pine-script-docs/concepts/repainting/).
- LuxAlgo's "repaint-safe engineering" page: pivots are drawn 5 bars in the past, the default pivot length of 5 sets the confirmation delay, and swing pivots and similar structures should only be acted on or backtested after that delay has passed — [LuxAlgo Library: repaint-safe engineering](https://www.luxalgo.com/library/concept/repaint-safe-engineering.md); [LuxAlgo demo indicator](https://www.luxalgo.com/library/indicator/repaint-safe-engineering/).
- LuxAlgo's SMC script has a "Bars Confirmation" input for equal highs and lows — [TradingView script page](https://tradingview.com/script/CnB3fSph-Smart-Money-Concepts-LuxAlgo). Users on forums ask whether SMC labels repaint (anecdotal) — [useThinkScript thread](https://usethinkscript.com/threads/smart-money-concepts-smc-luxalgo-for-thinkorswim.19143/latest). A competitor's blog alleges frequent repaints; this is unverified and commercially biased — [Lunefi](https://lunefi.com/blog/best-luxalgo-alternatives-2026-tradingview-indicators).

**Overfitting and data-snooping exposure**
- LuxAlgo's Backtesting Assistant searches results across "over 10 million" strategies — [LuxAlgo docs](https://docs.luxalgo.com/docs/ai-backtesting/introduction.md).
- Holly "backtests her strategies nightly and selects the strongest for the next day" — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/).
- Danelfin recalculated historical scores for its new model — [Danelfin blog](https://blog.danelfin.com/?p=4653).
- TrendSpider's own guidance says the "first step in validating an AI strategy is to test it on out-of-sample data" — [TrendSpider blog](https://trendspider.com/blog/building-a-strategy-with-ai-strategy-lab/). TrendSpider also offers "Variance Testing" — [TrendSpider pricing](https://trendspider.com/pricing/).

**LLM hallucination and stale data**
- TradingView Copilot: "It can be wrong or use outdated information" — [TradingView support](https://in.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/).
- Most LLM agents fail to beat buy-and-hold in StockBench — [arXiv](https://arxiv.org/abs/2510.02209). Agents "can be systematically misled" in TradeTrap — [arXiv](https://arxiv.org/abs/2512.02261v1).
- Third-party guides say ChatGPT has no built-in live market feed without connectors — [Firecrawl](https://www.firecrawl.dev/articles/real-time-stock-news-chatgpt).
- No measured delay has been published for Perplexity Finance India — [OneTradeJournal](https://onetradejournal.com/ai-trading/perplexity-finance-india).

**Delayed data**
- TradingView free NSE data reportedly about 15 minutes delayed — [Algotest](https://algotest.in/blog/tradingview-charts-showing-delayed-data/).
- Trade Ideas Free tier: 15-minute delayed — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/).
- TrendSpider CBOE indexes: 10–15 minutes delayed — [TrendSpider pricing](https://trendspider.com/pricing/).
- Kavout futures and indices: about 15–20 minutes delayed — [Kavout](https://www.kavout.com/).

**Data lag rules in India (affects public sharing, not personal use)**
- SEBI's January 2025 finfluencer circular says unregistered educators may use only price data at least three months old, and may not use it to hint at future prices — [Business Today, 31 Jan 2025](https://businesstoday.in/markets/stocks/story/sebis-clampdown-on-finfluencers-cannot-use-live-stock-market-data-in-educational-content-462704-2025-01-31); [Business Standard](https://www.business-standard.com/markets/news/sebi-finfluencer-circular-live-stock-data-market-education-rules-125013000571_1.html).
- A January 2026 consultation proposed a 30-day lag instead. Adoption was not confirmed — [The Week, 7 Jan 2026](https://www.theweek.in/news/biz-tech/2026/01/07/sebi-mulls-30-day-lag-on-sharing-stock-market-data-for-investor-education-here-is-why.html).

**Automation rules in India**
- SEBI's retail algo framework (circular of 4 Feb 2025) applies to all brokers from 1 Apr 2026. Brokers that missed earlier milestones were barred from onboarding new retail API-algo clients from 5 Jan 2026 — [Business Standard](https://www.business-standard.com/markets/news/sebi-extends-retail-algo-trading-framework-rollout-to-2026-125093000956_1.html); [TaxScan](https://www.taxscan.in/top-stories/sebi-extends-timeline-for-retail-algo-trading-framework-full-implementation-from-apr-1-2026-1433982).
- API-based strategies are treated as algos and must be registered and routed through the broker. Secondary sources describe strategy IDs, static-IP whitelisting, 2FA and audit trails — [FYERS notice](https://fyers.in/notice-board/new-sebi-framework-for-retail-algo-trading-from-april-01-2026/); [5paisa](https://www.5paisa.com/news/sebi-tightens-algo-trading-rules-with-mandatory-2fa-and-audit-trails-from-april-1); [Sahi blog](https://www.sahi.com/blogs/sebi-algo-trading-rules-2026-what-every-retail-trader-must-know-before-april).

### Inferences
- **Pivot and SMC-style logic:** the bot's swing S/R, equal highs and lows, and "unswept swing high/low" liquidity pools all depend on swing pivots, which by definition are confirmed only N bars later. If a future backtest marks a pivot or sweep on the bar where it occurred, it will overstate performance. That is the exact pattern TradingView and LuxAlgo warn about. Sweep detection also needs a closed-bar rule (`isconfirmed`-style) to avoid intrabar flip-flopping.
- **Delayed data:** if the bot's NSE data is about 15 minutes delayed (as with free TradingView or other free sources), ORB breakouts, VWAP crosses and stop-hunt sweeps will often be flagged after the move. For live intraday use, this matters more than any modeling choice.
- **Survivorship bias:** this applies to any future NSE backtest run only on today's constituents, as well as to vendor stock-ranking backtests. Danelfin does not say whether its 5,616-stock universe includes delisted names.
- **Regulation:** a personal, signal-only bot that places no orders appears to fall outside SEBI's algo framework, which covers API orders, and outside the finfluencer data-lag rule, which covers public education content. This is an inference, not legal advice. Adding automated NSE order placement (for example, via self-hosted Kite MCP or the Kite API) would bring the April 2026 algo requirements into play.

### Gaps
- No primary-source study measured how often LLMs hallucinate price levels for specific tickers. PHANTOM is the closest listed benchmark and was not verified.
- No vendor in scope publicly documents survivorship-bias handling (point-in-time universes) for its backtests.
- I could not confirm whether the free TradingView NSE delay applies to all Indian users, nor when it started.

## 5. How does the personal rule-based bot compare: where is it already comparable, and what concrete features does it lack?

### Takeaway
On level computation and setup output (CPR, pivots, PDH/PDL, ORB, VWAP, swing S/R, liquidity, sweeps, entry/SL/T1/T2/R:R), the bot is already comparable to what TradingView and LuxAlgo indicators, Autochartist key levels and Trading Central trade plans deliver. It covers NSE, crypto and forex together, which most US AI tools do not, and it is deterministic, so it cannot hallucinate. What it lacks is the validation and data layer the leading tools sell:
- backtesting and out-of-sample or variance testing;
- historical hit-rate statistics per signal;
- licensed real-time data;
- pattern-recognition breadth;
- universe-wide scanning;
- fundamentals and news;
- a natural-language or LLM interface.

### Cited Findings
**Where the bot is already comparable**
- TradingView Copilot draws support and resistance and market structure ("order blocks, fair value gaps, and BOS/CHoCH") and sets alerts on them — [TradingView support](https://in.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/). The bot computes swing S/R, structure (HH/HL) and sweeps deterministically.
- LuxAlgo's SMC tools detect equal highs and lows with a "Bars Confirmation" setting — [TradingView script page](https://tradingview.com/script/CnB3fSph-Smart-Money-Concepts-LuxAlgo). This is analogous to the bot's equal-high/low liquidity pools.
- Autochartist "Key Levels" give breakout and approaching signals, plus a volatility analysis for SL/TP — [CMC Markets](https://www.cmcmarkets.com/en-ie/trading-platform/mt4/autochartist); [EarnForex](https://earnforex.com/guides/autochartist-review). Trading Central "Technical Views" give trading plans with position management — [Trading Central](https://www.tradingcentral.com/research-products). Trade Ideas Premium offers "Smart Risk Levels" — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/). The bot's breakout and dip-buy setups with entry, SL, two targets and R:R are the same kind of output.
- LuxAlgo delivers alerts to Telegram even on the Free plan — [LuxAlgo pricing](https://www.luxalgo.com/pricing.md). The bot's Telegram delivery is on par.
- On market coverage: Trade Ideas covers only US and Canada — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/). TrendSpider lists no Indian equities — [TrendSpider pricing](https://trendspider.com/pricing/). Kavout lists US stocks, ETFs, crypto and major FX — [Kavout](https://www.kavout.com/). Danelfin covers US, Europe and ETFs — [Danelfin blog](https://blog.danelfin.com/?p=4653). Composer is offered only where its US broker-dealer is registered — [Composer pricing](https://www.composer.trade/pricing).

**Concrete features the bot lacks, with the tools that have them**
- **Backtesting.** TrendSpider includes backtesting, multi-symbol and variance testing on all plans, with 1-minute resolution on its upper tiers — [TrendSpider pricing](https://trendspider.com/pricing/). Composer offers unlimited backtests on its free tier — [Composer pricing](https://www.composer.trade/pricing). Trade Ideas Premium has OddsMaker — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/). TradingView's Copilot reads strategy-tester results — [TradingView support](https://in.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/).
- **Per-signal historical statistics.** Danelfin publishes average 3-month alpha per score bucket, computed daily over 2017–2025 — [Danelfin blog](https://blog.danelfin.com/?p=4653). Holly re-ranks strategies nightly from backtests — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/).
- **ML models trained on indicator features.** TrendSpider AI Strategy Lab offers Random Forest, Naive Bayes, KNN and logistic regression, with out-of-sample checks — [TrendSpider product page](https://trendspider.com/product/machine-learning-quant-trading-strategy-lab/); [TrendSpider blog](https://trendspider.com/blog/building-a-strategy-with-ai-strategy-lab/).
- **Chart-pattern recognition beyond swing levels.** Autochartist and Trading Central detect triangles, wedges, head-and-shoulders, channels and harmonics, with quality scores; TrendSpider auto-draws trendlines and Fibs — [Spotware](https://spotware.com/vi/integrations/autochartist); [Trading Central](https://tradingcentral.com/blog/technical-insight-r-trader-edition-empower-investors-to-find-validate-and-time-their-trades); [TrendSpider pricing](https://trendspider.com/pricing/).
- **Fundamental, sentiment and news inputs.** Danelfin has Technical, Fundamental and Sentiment subscores — [Danelfin support](https://support.danelfin.com/hc/en-us/articles/4404382038545). Copilot covers financials, analyst estimates, news and macro — [TradingView support](https://in.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/). Perplexity Finance offers Indian earnings and live call transcripts — [Outlook Business](https://www.outlookbusiness.com/deeptech/artificial-intelligence/perplexity-adds-live-transcripts-india-market-data-to-finance-dashboard-free-access-for-users).
- **Natural-language querying and screening.** TradingView has its AI Screener and Copilot — [TradingView support](https://br.tradingview.com/support/solutions/43000785770/). Composer has Trade with AI — [Composer help](https://help.composer.trade/article/254-what-is-trade-with-ai). Kite MCP lets an LLM read a Zerodha account — [Zerodha TradingQnA](https://tradingqna.com/t/introducing-kite-mcp-connect-your-kite-account-to-ai-assistants/181830).
- **Licensed real-time data.** TradingView offers paid add-ons or broker-linked real-time NSE (Dhan, FYERS) — [Algotest](https://algotest.in/blog/tradingview-charts-showing-delayed-data/). Trade Ideas and TrendSpider stream US data in real time — [Trade Ideas pricing](https://www.trade-ideas.com/pricing/); [TrendSpider pricing](https://trendspider.com/pricing/).
- **Order-flow data.** LuxAlgo Vela has trades and L1 quotes with lookback by plan — [LuxAlgo pricing](https://www.luxalgo.com/pricing.md).
- **Execution and automation, with guardrails.** Options include TrendSpider bots with SignalStack orders, Composer auto-execution, Trade Ideas auto trading (Premium), Robinhood agentic accounts, and self-hosted Kite MCP order tools — [TrendSpider pricing](https://trendspider.com/pricing/); [Composer pricing](https://www.composer.trade/pricing); [Trade Ideas pricing](https://www.trade-ideas.com/pricing/); [Robinhood newsroom](https://robinhood.com/newsroom/robinhood-is-now-open-to-agents); [LobeHub Kite MCP](https://lobehub.com/ja/mcp/zerodha-kite-mcp-server). For NSE, SEBI's 1 Apr 2026 algo framework applies to API orders — [Business Standard](https://www.business-standard.com/markets/news/sebi-extends-retail-algo-trading-framework-rollout-to-2026-125093000956_1.html).
- **Pre-close alerts and multi-condition alerts.** LuxAlgo paid alerts can fire before the bar closes; TradingView Copilot sets multi-condition alerts — [LuxAlgo pricing](https://www.luxalgo.com/pricing.md); [TradingView support](https://in.tradingview.com/support/solutions/43000795131-getting-started-with-ai-copilot/).

### Inferences
- **Highest-value gap to close:** an event-driven backtester that uses only information available at signal time: pivots confirmed after N bars, sweeps judged on closed bars, HTF levels taken from the prior completed period. Pair it with per-setup statistics (win rate, average R, expectancy, MAE/MFE) by symbol, session and regime, and with walk-forward or out-of-sample splits. This is what TrendSpider, Trade Ideas and Danelfin sell as their credibility layer. It would also turn the bot's confluence weights and bias votes from hand-set into empirically calibrated.
- **Second gap:** data quality and timing. Getting real-time NSE through a broker API (Kite, Dhan or FYERS) instead of free or delayed feeds matters more for ORB, VWAP and sweep signals than adding any AI.
- **Optional third gap:** an LLM layer on top of the bot's deterministic outputs, for example a Telegram "explain this setup" or a natural-language screen. This mirrors TradingView Copilot and Kite MCP. Because the LLM would only narrate computed levels, it would keep the bot's no-hallucination property. Tools such as Copilot read levels from live platform data, while a general LLM asked "what is Nifty's support?" may invent them.
- **Where the bot is ahead:** for a multi-asset trader with NSE as the core market, the bot is already broader in coverage than Trade Ideas, TrendSpider, Danelfin, Kavout and Composer. Its CPR, ORB and liquidity-sweep stack is more NSE-intraday-specific than any off-the-shelf AI score. It is also free and reproducible. No vendor offers an audited edge that would clearly beat a well-backtested personal rule set.

### Gaps
- Without the bot's code and data, I cannot say whether its swing and sweep logic already avoids look-ahead and repainting.
- I found no tool that packages CPR, ORB and liquidity-sweep logic specifically for NSE with published hit rates, so there is no direct benchmark for the bot's specific signal set.
- INR pricing for TradingView paid plans and the Copilot add-on, and the cost of broker real-time data APIs in India (Kite, Dhan, FYERS), were not researched in this session.
