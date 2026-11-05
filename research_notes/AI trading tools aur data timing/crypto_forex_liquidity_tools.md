# Crypto & Forex Liquidity / Order-Flow Tools, Trading Bots, and India Legal Context (research notes, compiled 5 Nov 2026)

Legend used throughout: **[M]** = directly measured / exchange- or broker-reported data; **[E]** = estimated or modelled output; **[U]** = unverified, secondary-only, conflicting, or vendor claim. All dates are as reported by the cited source. Wording from sources is paraphrased unless marked as a quote.

## 1. Crypto liquidity / order-flow tools (CoinGlass, Hyblock, Bookmap, Kingfisher, TradingLite, Velo, Laevitas, exchange data): what is measured vs modelled, latency, pricing

### Takeaway
Only exchange-published series are measured: order-book depth (displayed limit orders), trades with taker side (the basis of CVD), open interest, funding, and realized liquidations. Even realized liquidations are only a lower bound on Binance, because its public feed pushes at most one liquidation per symbol per second. Every "liquidation heatmap / map / level" product (CoinGlass, Hyblock, Kingfisher) is a model. It projects hypothetical liquidation prices from open interest plus assumed leverage tiers, and the vendors themselves call the output an estimate or a relative intensity. None of them publishes a full formula.

### Cited Findings
**Exchange raw data (Binance, the bot's own data source)**
- [M] Binance USDⓈ-M liquidation stream (`<symbol>@forceOrder`, plus the all-market `!forceOrder@arr`). It updates every 1000 ms as a snapshot: for each symbol, only the most recent liquidation order in each 1-second window is pushed, and nothing is pushed if no liquidation happened. The payload carries symbol, side, original quantity, price, average price, order status and trade time. — [Binance docs: Liquidation Order Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams); [Binance docs: All Market Liquidation Order Streams](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/All-Market-Liquidation-Order-Streams)
- [M] Binance spot klines return 12 fields in this order: open time, open, high, low, close, volume, close time, quote-asset volume, number of trades (index 8), taker-buy base-asset volume (9), taker-buy quote-asset volume (10), ignore (11). The kline data source is listed as "Database". The order-book depth endpoint defaults to 100 levels with a maximum of 5000. Its request weight runs from 5 (1–100 levels) to 250 (1001–5000), and its data source is listed as "Memory". No latency figure is published for either endpoint. — [Binance Spot API: market-data endpoints](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints)
- [M]/[U] The 10–11 Oct 2025 crash was the largest liquidation event on record (~$19.1B per The Block). Afterwards, Hyperliquid co-founder Jeff Yan alleged that some centralized exchanges may undercount liquidations by up to 100× in volatile periods. He pointed to Binance's documented one-order-per-second feed and contrasted it with Hyperliquid's on-chain liquidations, which anyone can verify. The 100× figure is his allegation and has not been independently verified. — [The Block, 13 Oct 2025](https://www.theblock.co/post/374311); [ForkLog](https://forklog.com/en/hyperliquid-co-founder-says-cex-liquidation-totals-may-be-underreported-by-up-to-100x/); [FXStreet](https://www.fxstreet.com/cryptocurrencies/news/hyperliquid-founder-accuses-cexs-of-hiding-user-liquidation-data-202510130916)
- [U] CoinGlass reportedly also said that exchanges such as Binance may systematically underestimate liquidation volume during crashes. Only a secondary report was found. — [Coinspot](https://coinspot.io/hmwmh)
- [U] Reported 10–11 Oct 2025 figures differ by source and time window: about $19.25–19.5B total, about $16.7B of it longs, and about 1.6M accounts. One source names Hyperliquid as the largest venue (~$10.3B). Binance's post-mortem blamed a macro shock (the tariff announcement) rather than exchange failure. Binance's reimbursement totals are reported inconsistently ($283M vs $328M). — [Cointelegraph via TradingView](https://th.tradingview.com/news/cointelegraph:83d396b6a094b:0-19b-crypto-market-crash-was-it-leverage-china-tariffs-or-both); [AMBCrypto](https://ambcrypto.com/binance-says-macro-shock-not-exchange-failure-drove-octobers-19b-liquidation-cascade/); [Datawallet](https://www.datawallet.com/crypto/october-10-crypto-crash-explained); [Unhashed](https://unhashed.beehiiv.com/p/19b-crash-exposes-cex-transparency-gaps)

**CoinGlass [E] (heatmap / map); its realized-liquidation and OI series are [M] but inherit exchange gaps**
- CoinGlass's own guide says the heatmap computes *potential* liquidation levels from market volume, leverage usage and related data in each price range. CoinGlass calls the displayed values a relative-intensity indicator, meant to be compared against other levels rather than read as amounts. It says actual forced liquidations are often lower than the intensity shown, and that the tool predicts where liquidations might be triggered, not how many will occur or at what exact price. The colour scale runs from purple (low) to yellow (high). The idea that price is drawn toward "magnet" zones is presented as a trading heuristic. — [CoinGlass Learn: How to use Liquidation Heatmaps](https://coinglass.com/learn/how-to-use-liqmap-to-assist-trading-en)
- CoinGlass splits its products into a "Binance BTC/USDT Liquidation Map", an aggregated "Bitcoin Exchange Liquidation Map" and a separate "Hyperliquid Liquidation Map". The heatmap page offers "Model 1 / 2 / 3" tabs but does not define them on the page. A third-party API wrapper exposes model1–3 with windows from 12h to 3 months and returns cells of [time index, price index, liquidation value]. — [CoinGlass Liquidation Map](https://www.coinglass.com/pro/futures/LiquidationMap); [CoinGlass Liquidation Heatmap](https://www.coinglass.com/de/pro/futures/LiquidationHeatMapNew); [Apify wrapper (third-party)](https://apify.com/api_merge/coinglass-liquidation-heatmap.md)
- [U] Third-party explainers say exchanges do not publish each position's entry price or leverage. Heatmaps are therefore reconstructed from OI, funding, recent volume and an assumed leverage distribution, commonly 25× / 50× / 100× tiers. A generic formula (long liquidation ≈ entry × (1 − 1/leverage + maintenance margin)) circulates but is not confirmed as CoinGlass's. — [DEXTools 2026 guide](https://www.dextools.io/tutorials/how-to-read-liquidation-maps-in-crypto-guide-2026); [PCTechMag](https://pctechmag.com/?p=98148)
- API pricing:
  - Hobbyist $29/mo: 30 requests/min, personal use, update frequency ≤1 min.
  - Startup $79/mo: 80 requests/min.
  - Standard $299/mo: 300 requests/min, the first tier with commercial-use rights.
  - Professional $699/mo: 1,200 requests/min.
  - Enterprise: custom pricing.
  - ComparEdge reports a price cut on 28 Jun 2026 (Standard $379→$299, Professional $879→$699; last verified 8 Jul 2026).
  - Sources: [CoinGlass pricing](https://coinglass.com/pricing); [ComparEdge](https://comparedge.com/tools/coinglass/pricing)

**Hyblock Capital [E]**
- Hyblock calls its Liquidation Levels estimates and predictions of where large liquidations may occur. They are built from clusters of price points where high-leverage traders (100×, 50× and 25×, long and short) open positions.
  - Coverage: Binance USDT-M perpetuals (BTC, ETH, 70+ altcoins), BitMEX XBTUSD/ETHUSD, and Bybit BTCUSD/ETHUSD.
  - Position-size tiers vary by coin and exchange.
  - The tool shows only levels that price has not yet "hit".
  - Its cumulative delta is long levels minus short levels.
  - Hyblock publishes no formula, OI weighting, formal disclaimer or update frequency.
  - Source: [Hyblock Academy: Liquidation Levels](https://academy.hyblockcapital.com/tools/liquidation-levels)
- Hyblock's heatmap calculates levels from market data and a range of leverage amounts, then bins them into price buckets. Its Open Interest Heatmap is a separate tool. — [Hyblock Academy: Liquidation Heatmap](https://academy.hyblockcapital.com/tools/liquidation-levels-1); [Hyblock features](https://hyblockcapital.com/features)

**Kingfisher [E]**
- Kingfisher's liquidation maps are heatmap-style displays of the relative concentration of estimated liquidation clusters for each instrument. Access is credit-based (1 credit = one simple map), or a subscription/session gives unlimited pulls, and a free tier needs no card. GEX+ models where options dealers are forced to hedge (gamma exposure). Kingfisher's own content treats a negative-GEX zone near a liquidation cluster as a "squeeze" setup [U, vendor claim]. — [Kingfisher docs: Liquidation Maps](https://docs.thekingfisher.io/products/liquidations-maps); [Kingfisher getting-started guide (2026)](https://thekingfisher.io/en/blogs/kingfisher-getting-started); [Kingfisher: What is GEX](https://thekingfisher.io/en/blogs/what-is-gex)

**Bookmap [M] (visualises displayed limit-order depth and trades)**
- Bookmap plans (prices were matched to plans from the page layout):
  - Digital (free): real-time crypto from Binance, Bitfinex and 20+ more exchanges; US stocks and futures are delayed; 1 symbol at a time.
  - Global: $49/mo, $39/mo billed yearly, or $990 lifetime; 10 symbols.
  - Global Plus: $99/mo, $79/mo yearly, or $1,990 lifetime; 20 symbols.
  - Global Premium: $199/mo, $158/mo yearly, or $3,990 lifetime; adds the MBO bundle and SPX "Options Strike" gamma levels.
  - Non-crypto data is billed separately, e.g. the BookmapData CME bundle $79/mo (or $34 per exchange), Nasdaq TotalView $59/mo, and dxFeed or Rithmic ($40–101/mo).
  - Tools built on market-by-order data, such as the Stops & Icebergs Tracker, need an MBO feed (e.g. CME via BookmapData or Rithmic).
  - Source: [Bookmap pricing](https://bookmap.com/pricing)

**TradingLite [M] (order-book heatmap)**
- TradingLite is a browser-based crypto order-flow platform with a liquidity heatmap, footprint clusters, TPO, volume profile and its own LitScript language. Sources cite 200 to 500+ community indicators. Pricing conflicts: one source lists a Silver tier at $14.95/mo with a 14-day trial, another a free tier with paid plans from $24.99/mo. — [NexusFi](https://nexusfi.com/d/platforms/tradinglite/); [TradingToolsHub](https://tradingtoolshub.com/review/tradinglite/)

**Velo [M] (aggregated derivatives data)**
- A coin's funding on Velo is the OI-weighted average funding rate (per 8h or annualized) across all supported exchanges. OI can be shown in USD or coin terms, as candles or as bar-to-bar change. The docs include liquidation pages and a liquidation heatmap. A third party lists CVD charts [U]. A competitor says the Pro tier adds deeper history and the API [U]. No Pro price was found. — [Velo docs: Market page](https://velodata.gitbook.io/velo-data/market-page); [Velo docs: Chart page](https://velodata.gitbook.io/velo-data/chart-page/chart); [Sharpe comparison (competitor)](https://www.sharpe.ai/compare/sharpe-vs-velo)

**Laevitas [M market data + modelled Greeks / theoretical values]**
- Laevitas is a Swiss derivatives-analytics platform covering options, perpetuals and dated futures, with theoretical values, Greeks, a strategy builder, a REST API and an SDK. Its landing page lists a free plan with 1 week of history and Premium at $50 per seat per month. NexusFi adds Enterprise at $500/mo and Enterprise CME at $600/mo, and other third-party prices conflict. — [Laevitas landing page](https://laevitas-landing.pages.dev/); [NexusFi](https://nexusfi.com/d/data-providers/laevitas/)

### Inferences
- **Measured vs modelled map** (synthesised from the findings above):

| Data | Type | Example source/tool | Granularity / latency found |
|---|---|---|---|
| Order-book depth (displayed **limit** orders) | [M] | Binance depth REST (≤5000 levels); Bookmap / TradingLite heatmaps | Bookmap crypto "real-time"; Binance publishes no latency |
| Trades / taker side → bar delta & CVD | [M] | Binance klines fields 9–10; Velo CVD [U] | per bar (15m in the bot) |
| Open interest, funding | [M] exchange-reported (Velo aggregates OI-weighted) | Velo, CoinGlass | — |
| Realized liquidations | [M] but incomplete | Binance forceOrder | 1-s snapshots, at most one order per symbol per second |
| Liquidation heatmap / map / levels | [E] | CoinGlass, Hyblock, Kingfisher | CoinGlass API ≤1 min (Hobbyist) |
| On-chain perp positions / liquidations | [M] on-chain | Hyperliquid; CoinGlass Hyperliquid map | — |
| Options GEX | [E] (rests on assumptions about dealer positioning) | Kingfisher GEX+, Laevitas | — |

- **No CEX publishes stop orders.** Public CEX books show resting *limit* orders only. Untriggered stop orders and per-position liquidation prices are not published, which is why vendors must reconstruct heatmaps. "Stop" or "liquidation" liquidity on a CEX is therefore always inferred, both by vendors and by the user's bot. The exceptions are on-chain perpetuals such as Hyperliquid (public positions, which CoinGlass maps separately) and broker-level books in FX, such as OANDA (Section 3).
- **Heatmaps and the bot's pools are the same kind of data.** Both are [E]. Heatmaps anchor on measured OI changes plus leverage assumptions; the bot anchors on price structure alone (swings, equal highs/lows, PDH/PDL, weekly high/low). Neither observes real stop orders. A heatmap is not ground truth for validating the bot's pools.
- **Zero-cost upgrades for the bot (crypto):**
  - **CVD from data the bot already pulls.** Binance klines already contain taker-buy base volume. Bar delta = 2 × taker_buy_base − volume, and CVD is its cumulative sum. Caveat from prior knowledge, not verified this session: ccxt's unified `fetch_ohlcv` keeps only [t, o, h, l, c, v]. Keeping fields 8–10 needs ccxt's raw/implicit Binance kline method.
  - **Measured displayed liquidity.** A depth snapshot (≤5000 levels) gives measured displayed liquidity near a swing level.
  - **Liquidations.** Collecting liquidations needs a persistent websocket, and the feed undercounts by design.
  - **OI and funding.** Binance's public futures OI and funding endpoints exist (prior knowledge, not verified this session).

### Gaps
- What CoinGlass's Model 1/2/3 compute, and whether CoinGlass corrects realized-liquidation totals for Binance's 1-per-second throttle. No primary CoinGlass statement was found.
- Pricing for Hyblock, Kingfisher and Velo Pro was not found. TradingLite's official price is unresolved because the sources conflict.
- Bookmap's crypto feed latency, and whether it connects directly to each exchange. The pricing page points to a separate Crypto Guide, which was not read.
- No independent study was found that measures how well any liquidation heatmap predicts realized liquidations or price paths.

## 2. Crypto AI tools and bots (3Commas, Pionex, Cryptohopper, Token Metrics, Santiment, CryptoQuant, Glassnode): working model and known risks

### Takeaway
Most retail "bots" are deterministic execution engines: grid, infinity grid, DCA with safety orders, and signal-triggered bots. They trade through exchange API keys and do no market-structure analysis. "AI" ratings such as Token Metrics are proprietary composite scores with no published methodology. Data vendors (Santiment, CryptoQuant, Glassnode) sell measured on-chain, exchange-flow and social series plus derived ratios, with resolution and lag set by price tier. The best-documented operational risk is a third party holding users' API keys (3Commas, 2022). The US CFTC warns that "AI bot" marketing is a fraud vector.

### Cited Findings
**3Commas**
- **How the DCA bot works.** This comes from third-party guides and TradingView emulators; 3Commas's official docs were not retrieved.
  - The base order is the first entry.
  - Safety orders are placed at fixed % price deviations below entry (2% is suggested as a starting point).
  - "Volume scale" makes each safety order larger, and "step scale" widens the spacing between them.
  - Take-profit is a % above the *average* entry of the base and safety orders.
  - "Max safety orders" caps how many fill. A high volume multiplier makes later orders very large very quickly.
  - Sources: [Algorithmic Trading Guide: 3Commas chapter](https://trading-guide-1.gitbook.io/algorithmic-trading-guide-pro/3commas-guide); [TradingView 3Commas DCA backtester](https://www.tradingview.com/script/Txo3OEBa-3Commas-Bot-DCA-Backtester-Signals-FREE/)
- **API-key incident (2022).**
  - An attacker reportedly obtained about 100,000 API keys, published 10,000 of them and promised the rest.
  - User complaints began in October 2022. 3Commas at first called the reports "false rumours".
  - In December 2022, after a public warning from Binance's CZ, its CEO confirmed the leaked data was genuine.
  - The hacker claimed an employee sold the keys; 3Commas said its internal review found no evidence of that.
  - HAPI counted 24 confirmed victims with about $14.9M in losses by November.
  - The FBI joined the investigation on 29 Dec 2022.
  - The 100k total was never confirmed by 3Commas.
  - Sources: [Cointelegraph](https://regional-front.cointelegraph.com/news/3commas-ceo-confirms-api-key-leak-following-warning-from-cz); [ForkLog: HAPI analysis](https://forklog.com/en/api-key-leaks-and-exchange-inaction-a-hapi-analysis-of-the-3commas-incident/); [ForkLog: FBI probe](https://forklog.com/en/fbi-probes-3commas-api-key-leak-reports-say/); [SiliconANGLE, 29 Dec 2022](https://siliconangle.com/?p=602984); [Hackread](https://www.hackread.com/3commas-api-database-leak-anonymous-hacker/)
- [U] An affiliate-style comparison quotes pricing of about $37/mo, or $25/mo billed annually. — [AI Trading Ranked: 3Commas vs Pionex](https://ai-trading-ranked.pages.dev/posts/3commas-vs-pionex)

**Pionex**
- Pionex is an exchange with free built-in bots, so users pay only trading fees (0.05% is the figure sources consistently cite).
  - The grid bot buys low and sells high inside a set range.
  - Infinity Grid has no upper price limit and is set in percentages.
  - The DCA bot makes recurring buys.
  - Futures grids add leverage, and with it margin, funding and liquidation risk.
  - Grids fail when price leaves the range. A breakdown leaves the bot holding coins bought on the way down; a breakout sells the inventory early and misses the rally.
  - Sources: [Coin Bureau Pionex review (updated 19 Aug 2025)](https://coinbureau.com/review/pionex/); [Coin Bureau grid-bot guide](https://coinbureau.com/guides/how-to-copy-grid-bots-on-pionex); [Zignaly Pionex bot review](https://zignaly.com/crypto-trading/bots/pionex-bot-review); [DayTrading.com Pionex review](https://www.daytrading.com/pionex)

**Cryptohopper**
- Cryptohopper dropped its free "Pioneer" plan on 18 Jun 2026. Every bot now needs a paid plan, and new accounts get a 3-day Explorer trial. Explorer costs $29/mo ($24.16/mo billed yearly) before VAT. 2026 reviews show the service still active, and no acquisition or shutdown news was found. — [AirdropAlert review](https://airdropalert.com/blogs/cryptohopper-review/); [Altrady review (20 Apr 2026)](https://www.altrady.com/blog/crypto-bots/cryptohopper-review)

**Token Metrics [E] (proprietary)**
- Token Metrics gives each token two scores. The Trader Grade (0–100) covers short-term momentum and volatility and is updated hourly. The Investor Grade covers long-term fundamentals and is updated daily on the Advanced plan. Inputs are described as "80+ data points" (price action, volume, sentiment, on-chain and developer activity), with ML models that re-weight factors as conditions change. The sources are promotional blogs, and they disagree on update frequency and inputs. No official methodology, weights or out-of-sample validation was found. — [DEV Community (Token Metrics content)](https://dev.to/crypto-trader/inside-token-metrics-how-ai-grades-are-revolutionizing-crypto-investing-1lcc); [Kitemetric](https://kitemetric.com/blogs/built-for-retail-powered-by-quant-token-metrics-levels-the-playing-field)

**Santiment [M] social / on-chain counts + [E] sentiment classification**
- Metrics:
  - Social volume counts coin-specific mentions across 1,000+ crypto social channels.
  - Weighted sentiment is a sentiment balance weighted by social volume. It spikes when volume is high and messages are strongly positive, and dips when volume is high and messages are negative.
  - MVRV = market cap / realized cap.
  - Santiment claims extreme social-volume spikes during rallies often mark local tops [U, vendor claim].
  - Sources: [Santiment Academy: Weighted Sentiment](https://academy.santiment.net/metrics/sentiment-metrics/weighted-sentiment-metrics/); [Bitfinex blog (Santiment)](https://blog.bitfinex.com/?p=18786)
- Pricing (sources conflict):
  - The free tier has a 30-day lag on restricted data.
  - Sanbase Pro costs $49/mo or $529/yr, with a 14-day trial.
  - Sanbase Max costs $249/mo (as of 12 Jul 2026, per ComparEdge).
  - Holding 1,000 SAN tokens gives a 20% discount.
  - Signals are noisier for small-cap coins.
  - Sources: [Santiment pricing](https://app.santiment.net/pricing); [ComparEdge](https://comparedge.com/tools/santiment/pricing)

**CryptoQuant [M] exchange flows + derived ratios**
- The Estimated Leverage Ratio is an exchange's open interest divided by its coin reserve, used as a proxy for average leverage (BTC, ETH and XRP via the Data API). Exchange netflow is inflow minus outflow; a positive value means net deposits. — [CryptoQuant ELR chart](https://cryptoquant.com/asset/btc/chart/market-indicator/estimated-leverage-ratio); [CryptoQuant docs: ELR](https://docs.cryptoquant.com/data-guide/market/estimated-leverage-ratio.md); [CryptoQuant user guide: netflow](https://userguide.cryptoquant.com/cryptoquant-metrics/stablecoin/stablecoin-exchange-in-outflow-and-netflow)
- [U] A competitor blog that read CryptoQuant's pricing page in July 2026 says the free Basic plan offers charts at daily resolution with 3 years of history, and an API token needs one of two paid plans. — [Athenum blog (competitor)](https://athenum.mataroa.blog/blog/athenum-vs-cryptoquant-exchange-flows-or-live-cross-venue-derivatives/)

**Glassnode [M] on-chain**
- [U] Glassnode tiers (third-party sources, which conflict):
  - Standard (free): Tier-1 metrics at 24h resolution, 1 alert.
  - Advanced: $49/mo billed annually, or $99 month-to-month per ComparEdge, which also reports a rise from $39 on 5 Jun 2026. Adds Tier-2 metrics at up to 1h resolution and 10 alerts.
  - Professional: about $999/mo, with all tiers, 10-minute resolution and 500 alerts.
  - API access is priced separately, and CostBench shows the tier structure changing over time.
  - Sources: [Glassnode pricing](https://insights.glassnode.com/pricing); [ComparEdge](https://comparedge.com/tools/glassnode/pricing); [CostBench](https://costbench.com/software/onchain-analytics/glassnode)

**Regulatory warning**
- The CFTC customer advisory of 25 Jan 2024 (Release 8854-24) warns that fraudsters exploit AI hype to sell automated trading algorithms, signal strategies and crypto schemes promising unreasonably high or guaranteed returns. It states that AI cannot predict the future or sudden market changes. It cites the $1.7B Mirror Trading International Ponzi scheme, urges background checks on bot and signal sellers, and asks for fraud to be reported to the CFTC and the FBI. — [CFTC advisory: AI Won't Turn Trading Bots into Money Machines](https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/AITradingBots.html); [CFTC Release 8854-24](https://www.cftc.gov/PressRoom/PressReleases/8854-24)

### Inferences
- **Taxonomy compared with the user's bot.**
  - **Execution engines** (grid, DCA): they make no directional forecast, and their profit depends on the market regime (ranging vs trending). DCA safety orders add exposure as price falls, which makes them martingale-like.
  - **Signal / marketplace layers** (3Commas signal bots, Cryptohopper, MQL5-style copy trading): quality depends on unaudited providers.
  - **"AI" scores**: black boxes with no measured liquidity input.
  - **On-chain / flow vendors**: measured data, but at daily-to-10-minute resolution depending on price tier. That is too coarse for 15m sweep timing below the top paid tiers.
  - None of the bots reviewed advertises native use of order-book or liquidation data. This is based on the descriptions found and is not exhaustive.
- **API-key exposure.** The user's bot reads only public endpoints, so it carries no API-key risk until it places orders. Standard mitigations come from general best practice, not from the sources above: trade-only keys, withdrawals disabled, IP whitelisting, sub-accounts.
- Exchange-flow metrics (CryptoQuant, Glassnode) depend on attributing addresses to exchanges and entities, so they mix [M] chain data with [E] labelling. This is prior knowledge, not verified this session.

### Gaps
- Official 3Commas, Pionex and Cryptohopper documentation and pricing pages were not retrieved; the mechanics above come from third parties. Pionex's licensing status was not found.
- No Token Metrics methodology or audited track record was found.
- API-key incidents at other bot platforms in 2025–2026 were not searched.
- Glassnode's current official tier lineup is unresolved because the sources conflict.

## 3. Forex tools and bots (MT4/MT5 EAs, MQL5 Signals, Autochartist, Trading Central, Myfxbook, retail sentiment, OANDA order/position books): working model

### Takeaway
Spot FX trades OTC, with no consolidated order book or volume. The "measured" liquidity or positioning data available to retail traders is broker-client data, each from a biased sample:
- the OANDA Order and Position Book, the only source found that shows where retail **stop** orders sit, at 20-minute (5-minute for Elite) granularity;
- IG Client Sentiment;
- Myfxbook Community Outlook.

Broker-bundled analytics (Autochartist, Trading Central) and MT4/5 EAs or MQL5 Signals are pattern engines, rule engines or copy-trading. They fall in the same inferred category as the user's bot.

### Cited Findings
**OANDA Order Book / Position Book [M] (OANDA clients only)**
- The Order Book shows OANDA clients' pending buy and sell orders, limits and stops included, clustered by price. The Position Book shows open long and short positions (entry-price clustering, unrealized P&L). Both offer cumulative, non-cumulative and net views. Data is available in 20-minute intervals, or 5-minute for Elite Trader accounts. The article is dated 14 May 2025. — [OANDA: Order Book explained](https://www.oanda.com/us-en/skills-and-insights/education/platforms-and-tools/oanda-platforms/oanda-order-book-explained-how-to-track-client-orders-and-positions-live/)
- [U] Other OANDA pages conflict on timing. They say data refreshes every 30 minutes and charts show the last 24 hours. They also say the data covers OANDA Corporation clients plus some clients of other OANDA entities. The MT5 order-book indicator updates every 5 minutes for premium clients and every 15 minutes for others. These were search-snippet readings, so which page said what was not verified. — [OANDA BVI tool page](https://www.oanda.com/bvi-en/lab-education/tools/order-book-position-book-tool); [OANDA prop-trader tool page](https://proptrader.oanda.com/en/lab-education/tools/order-book-position-book-tool/)

**IG Client Sentiment [M] (IG clients)**
- IG Client Sentiment is built from live IG retail client positions. Each client counts as long or short regardless of position size. It shows the % net long or short and a long:short ratio (e.g. silver at 2.83:1 in April 2024). IG and DailyFX use it mainly as a contrarian indicator combined with trend (a strong uptrend plus extreme net-short positioning reads as bullish). They say it is not foolproof and can also signal trend continuation. — [DailyFX: Trading signals from IG Client Sentiment](https://dailyfx.com/education/market-sentiment/trading-signals-from-ig-client-sentiment.html); [IG: Trading on sentiment](https://ig.com/sg/trading-strategies/trading-on-sentiment--using-ig-client-sentiment-data-220930)

**Myfxbook Community Outlook [M] (self-selected sample)**
- Community Outlook shows the % long vs short across accounts that users have voluntarily connected (live or demo), so the sample is biased. It covers 70+ pairs and up to about 100,000 positions. Fields include position counts, lots and average entry prices. A scraper vendor says it refreshes about every 15 minutes. Whether the % is by trader count or by volume is unconfirmed. Contrarian thresholds (70–80% moderate, 80%+ strong) are informal heuristics. — [Apify scraper (third-party)](https://apify.com/xtracto/myfxbook-community-outlook); [MQL5 Market listing](https://www.mql5.com/de/market/product/80271); [Global Investing guide](https://globalinvesting.github.io/guide-market-sentiment.html)

**MetaTrader 4/5 Expert Advisors and the Strategy Tester**
- **OnTick events.** In testing, the EA's OnTick handler runs on every real or generated tick and receives time and bid/ask/last as it would live.
- **"Every tick based on real ticks" mode.** MT5's most accurate test mode uses the broker's tick history. Minutes missing from that history are filled with generated ticks.
- **Generated ticks.** These are built from M1 bars using reference points capped by the bar's tick volume and never more than 11.
- **Suggested workflow.** Optimise in faster modes (1-minute OHLC, open prices only), then confirm on real ticks.
- **History Quality.** Reports show the share of real ticks used. One author found 0% real ticks when the broker's history began after the test start [U, anecdotal].
- Sources: [MT5 Help: tick generation](https://www.metatrader5.com/en/terminal/help/algotrading/tick_generation); [MQL5 Book: tester ticks](https://mql5.com/en/book/automation/tester/tester_ticks); [MetaQuotes: Strategy Tester](https://metaquotes.net/en/metatrader5/algorithmic-trading/tester); [MQL5 article](https://www.mql5.com/en/articles/24562)

**MQL5 Signals (copy trading)**
- **What it is.** The service copies a provider account's trades into the subscriber's MT4/MT5 account automatically and in real time, configured from inside the platform with a linked MQL5.community account.
- **Fees.** The provider sets a fixed monthly fee, paid from the MQL5 account, a card or an e-wallet. MetaQuotes says it charges no commission on the subscriber's traded volume.
- **Provider commission [U].** Older (2011-era) rules quoted on the MQL5 forum say providers receive the fee minus a 20% service commission. The current percentage is unverified.
- **Disputes and limits.** The current month's fee can be refunded in a dispute, and one trading account can subscribe to only one signal.
- **Divergence.** Copied results can differ from the provider's, and MetaQuotes's blog lists checks to run before subscribing.
- Sources: [MetaQuotes: Trading Signals](https://metaquotes.net/en/services/trading-signals); [MT5 Help: Signals](https://www.metatrader5.com/en/terminal/help/signals.md); [MQL5 forum: becoming a Signals provider](https://Mql5.com/en/forum/9050); [MQL5 blog: why a signal may copy differently](https://www.mql5.com/en/blogs/post/775297)

**Autochartist [E] (pattern recognition)**
- Autochartist scans for chart patterns, Fibonacci patterns and key levels. It adds volatility analysis, price-range forecasts and performance statistics, and flags patterns as emerging or completed, with alerts. Brokers such as Swissquote, CMC Markets and HFM provide it free, usually once an account is opened. No independent accuracy data was found. — [CMC Markets](https://www.cmcmarkets.com/en-gb/platform/mt4/autochartist); [Swissquote](https://www.swissquote.com/en-row/private/trade/platforms/forex-cfds/autochartist); [HFM](https://www.hfmpro.com/sv/en/trading-tools/autochartist)

**Trading Central [E] (analyst + algorithm)**
- **Technical Views.** Automated pattern recognition proposes trading plans, and senior analysts validate them before publication.
  - Each view has a pivot: the support or resistance level at which Trading Central would flip its bias.
  - Each view also gives an alternative scenario if the pivot breaks.
  - Horizons are intraday, short-term (up to 3 weeks) and medium-term (up to 3 months).
  - The method combines chart analysis for direction and targets with indicators for timing.
- **Technical Insight.** This automated product has been on broker sites since 2003.
- **Cost.** It is free to traders; brokers pay a licence fee.
- No ML/"AI" internals were documented.
- Sources: [Trading Central: Technical analysis](https://tradingcentral.com/analysis/technical-analysis); [Trading Central: Getting started with Technical Views](https://tradingcentral.com/tutorials/getting-started-with-technical-views); [Titan FX user guide](https://titanfx.com/trading-central/technical-views-en-user-guide); [ForexBrokers.com](https://www.forexbrokers.com/guides/trading-central-brokers)

### Inferences
- **OANDA's book is the closest measured counterpart to the bot's pools.** Of the retail sources found, only the OANDA Order Book directly measures where *stop* orders rest. That is what the bot assumes sits beyond swing highs and lows. It covers one broker's clients and comes in 20-minute (5-minute Elite) snapshots. Even so, it could test whether the bot's EURUSD or XAUUSD pools line up with real retail stop clusters. Prior knowledge, not verified this session: OANDA's v20 REST API offers order-book and position-book endpoints to account holders.
- **Sentiment data answers a different question.** IG and Myfxbook positioning is measured, but it tells you crowd direction, not where liquidity sits by level. The exception is Myfxbook's average entry prices.
- **Vendor levels are the same category as the bot's.** Autochartist key levels and Trading Central pivots are the vendor equivalents of the bot's pivots, CPR and swing S/R, so they are inferred too. They are useful as an independent cross-check, not as liquidity data.
- **The bot's inputs carry no liquidity information.** Prior knowledge, unverified: Yahoo's `EURUSD=X` has no meaningful volume because spot FX is OTC. `GC=F` is a COMEX futures contract with exchange volume, but the bot uses only its OHLC.

### Gaps
- OANDA's refresh interval is unresolved (20 vs 30 minutes). Its API access rules and history depth were not verified.
- No official Myfxbook methodology page was found.
- The current MQL5 Signals commission is not confirmed (only the old 20% figure was found).
- Autochartist's scan frequency and hit rate are unknown.
- CFTC COT positioning and CME FX/gold futures depth data were not researched.
- Yahoo Finance delay for `GC=F` was not researched (presumably covered by the data-timing notes).

## 4. SMC/ICT "liquidity sweep" ideas vs measurable liquidity data; evidence on effectiveness

### Takeaway
Academic evidence built on real bank order data (Osler, NY Fed) supports part of the premise. Stop-loss orders do cluster just *beyond round numbers*, and reaching those clusters speeds up price moves for hours. However, the SMC/ICT claim that fading sweeps of swing or equal highs and lows gives a trading edge is not supported by the best available tests. Those tests are not peer-reviewed. One of them (August 2026) uses definitions almost identical to the user's bot and found sweep reversals occur *less* often than at random levels, with negative net expectancy.

### Cited Findings
- **Osler, NY Fed Staff Report 125 [M] (actual order data).** The study used about 9,700 stop-loss and take-profit orders at a large dealing bank (Sept 1999–Apr 2000). Take-profit orders cluster tightly at round numbers, while stop-loss orders sit just beyond them. Osler argues this explains why trends often reverse at support/resistance and move fast once those levels break. — [NY Fed SR125 (PDF)](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf)
- **Osler, NY Fed Staff Report 150.** Using minute-by-minute FX quotes, Osler found trends accelerate when rates reach levels where stop-losses cluster. The response to stop-loss orders is larger and longer-lasting than to take-profits. The effects are statistically significant for hours, not days, and the author notes the statistics cannot prove causation. — [NY Fed SR150](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr150.html)
- **eXpeed Research Lab (Tokyo), Aug 2026 [U]** (company research, not peer-reviewed, no named author, pre-registration not stated).
  - **Instruments and data:** EURUSD, GBPUSD, USDJPY, AUDUSD, XAUUSD and BTCUSD, using M1 bid data resampled to M15, Jan 2019–Aug 2026 (~7.6 years).
  - **Definitions:**
    - swing = 5-bar fractal;
    - equal high/low = 2+ swings within 3 pips (FX/XAU) or 0.05% (BTC) in a 24h lookback, plus PDH/PDL;
    - sweep = a wick beyond the level by 1 pip (FX), $0.10 or 20% of ATR(14) (XAU), or $10 or 20% of ATR (BTC);
    - reversal = a close back inside within 30 minutes.
  - **Null:** each real level keeps its timestamp but gets a random price at the same distance from market, repeated 50 times.
  - **Results vs random:**
    - Raw EURUSD reversal rates were about 75% (75.41% at swing highs, 75.37% at swing lows), yet all 18 instrument × category z-scores were *negative* vs random. EUR: swing −16.08, equal −10.29, PDH/PDL −5.14.
    - EURUSD overall: 75.10% observed vs 77.82% random (z = −21.02).
    - Kill zones: London 76.75% vs 79.57%; New York 79.24% vs 81.36%.
  - **P&L:** fading the sweep at EUR 1R gave a gross +0.032R but a net −0.194R after spreads. Net expectancy was negative for every instrument and R-multiple, about −0.10R to −0.25R per trade.
  - **Conclusion:** the authors report "no statistical or economic support for the core ICT claim".
  - **Stated limitations:** a loose reversal definition, non-independent events, fixed UTC kill zones, representative (not live) spreads, bid-only data, and confirmation-based entries.
  - Source: [eXpeed: ICT Buy-Side / Sell-Side Liquidity, an empirical test](https://www.expeed.co.jp/ict-buy-side-sell-side-liquidity-an-empirical-test/)
- [U] **StatOasis:** order blocks, FVGs, liquidity sweeps and OTE were coded as mechanical rules across 4 markets. None showed a statistically significant forward-return edge on SPY, and 0 of 648 backtests beat buy-and-hold. — [StatOasis](https://statoasis.com/overfit/research/ict-backtest-what-survives)
- [U] **IndicatorEdge:** 660,005 out-of-sample backtests across 903 assets. The SMC Liquidity Sweep signal had a median win rate of 71.2% but beat buy-and-hold in only 8% of assets. — [IndicatorEdge](https://indicatoredge.io/learn/smc-ict-strategy-backtest-evidence-win-rate)
- [U] **Positive claims rest on illustrative or tiny samples.** Backtrex's EURUSD example (38 trades, 57% win rate, PF 1.78) is labelled "Illustrative". BacktestingMax lists a gold sweep strategy with PF 1.90 from 49 trades. — [Backtrex](https://backtrex.com/en/blog/liquidity-sweep-smc-ict-trading-guide); [BacktestingMax](https://www.backtestingmax.com/strategy/ict-gold-a-liquidity-sweep-market-structure-shift-fair-value-GykYIUp2xmTxMnmBFO37)
- **Vendors' own framing is heuristic.** CoinGlass presents liquidation "magnet" zones as a trading heuristic, and Hyblock displays only levels price has not yet hit (unswept). Both are the vendor versions of "unswept liquidity". — [CoinGlass Learn](https://coinglass.com/learn/how-to-use-liqmap-to-assist-trading-en); [Hyblock Academy](https://academy.hyblockcapital.com/tools/liquidation-levels)

### Inferences
- **"Liquidity" in SMC/ICT language mixes three different things:**
  - (a) resting stop orders, which no CEX order book or spot-FX venue shows (except broker-level books such as OANDA);
  - (b) leverage liquidation prices, which are modelled, except on-chain venues like Hyperliquid;
  - (c) displayed limit orders, which are measured but can be cancelled or spoofed (prior knowledge).
  - The bot's pools are proxies for (a), and liquidation heatmaps are proxies for (b). Neither is measured.
- **The eXpeed test is close to a direct test of the bot's logic.** Its definitions (fractal swings, equal highs/lows within a few pips, PDH/PDL, wick-through-and-close-back) closely match the bot's sweep logic. A raw sweep-reversal rate around 75% is a base-rate artifact. The bot should compare its sweep outcomes against a randomized-level baseline and include spreads before treating "sweep" as a signal.
- **Where the levels probably are.** Osler's evidence points to stops clustering beyond **round numbers**, not specifically beyond swing points. Adding round-number levels (e.g. 00/50 in FX; round thousands in BTC) as candidate stop clusters, and testing them against the same null, is better grounded in evidence.
- **How measured data could confirm a sweep.**
  - Crypto: a wick through a level, plus a burst of `forceOrder` prints, plus a drop in OI and absorption visible in bar delta/CVD, would separate a real stop or liquidation flush from noise.
  - FX: the swept level would coincide with a stop cluster in the OANDA Order Book.
  - This is an untested hypothesis.

### Gaps
- No peer-reviewed study of ICT/SMC sweep rules specifically was found.
- No study tests whether CoinGlass, Hyblock or Kingfisher levels predict price paths or realized liquidations.
- The eXpeed results are unreplicated and the author is unidentified.
- Osler's data (1999–2000, one bank) predates algorithmic FX and crypto, so how well it carries over to today is unknown.

## 5. India context: offshore forex under FEMA / RBI Alert List, legal INR currency derivatives, crypto tax and FIU registration, crypto-futures availability

### Takeaway
For an Indian resident, offshore spot-FX/CFD trading (EURUSD, XAUUSD with foreign brokers) is not permitted under FEMA, and LRS cannot be used to send overseas margin. The RBI Alert List names 95 unauthorised entities, including eToro and Forex.com (as of 19 Nov 2025). The legal route is currency futures and options on SEBI-recognised exchanges, which are formally for hedging. On 10 Oct 2026 the RBI cut the no-documentation limit for these from $100M to $5M. Crypto is legal but heavily taxed: 30% plus 1% TDS, unchanged by Budget 2026-27 and renumbered under the Income-tax Act 2025 from 1 Apr 2026. Exchanges serving Indians must be FIU-IND registered; Binance was fined ₹18.82 crore and Bybit ₹9.27 crore before registering. Indian FIU-registered platforms offer INR-settled crypto futures, but crypto derivatives are not SEBI-regulated and their tax treatment is contested. Using analysis tools personally is not itself restricted; the legal exposure depends on where trades are executed and how they are funded.

### Cited Findings
**Offshore forex under FEMA**
- RBI regulations under FEMA 1999 do not permit residents to trade foreign exchange in domestic or overseas markets. The exception is currency futures and options on stock exchanges recognised by SEBI, subject to RBI conditions (2011 RBI circular). — [RBI circular (PDF)](https://website.rbi.org.in/documents/87730/39710850/APDR461711F.pdf)
- RBI FAQ:
  - Remittances for margins or margin calls to overseas exchanges or counterparties are not allowed under LRS. Asked whether a resident can remit margin under LRS for online forex trading, the FAQ answers no.
  - Forex dealing on unauthorised electronic trading platforms (ETPs) exposes residents to penal action under FEMA, and the PMLA 2002 also applies.
  - Source: [RBI FAQ: Foreign exchange transactions](https://website.rbi.org.in/documents/d/rbi/foreign-exchange-forex-transactions)
- RBI press release, Feb 2022: residents dealing in forex for purposes not permitted, or on ETPs RBI has not authorised, are liable to penal action under FEMA. Permitted transactions must use RBI-authorised ETPs or recognised exchanges. This release introduced the Alert List. — [RBI press release](https://website.rbi.org.in/web/rbi/-/press-releases/rbi-cautions-against-unauthorised-forex-trading-platforms-53216)
- **RBI Alert List.**
  - The 19 Nov 2025 update added 7 names (Starnet FX, CapPlace, Mirrox, Fusion Markets, Trive, NXG Markets, Nord FX), bringing the total to **95**.
  - The list includes eToro and Forex.com (per Gulf News).
  - Listed entities are neither Authorised Persons under FEMA nor authorised to run forex ETPs.
  - No RBI update dated 2026 was confirmed. One site's "January 2026" claim repeats the November additions.
  - Sources: [Gulf News](https://gulfnews.com/business/banking/etoro-forexcom-among-95-unauthorised-forex-platforms-in-india-flagged-by-rbi-1.500352489); [Moneylife](https://moneylife.in/article/unauthorised-forex-trading-platforms-rbi-adds-7-more-entities-to-its-alert-list/78900.html); [Upstox](https://upstox.com/news/personal-finance/trading/rbi-alert-list-updated-full-list-of-unauthorised-forex-trading-platforms-and-what-happens-if-you-use-them/article-184938); [RBI press release (Alert List update)](https://www.website.rbi.org.in/web/rbi/-/press-releases/rbi-updates-the-alert-list-of-unauthorised-forex-trading-platforms-2); [IndiaFXGuide (low reliability)](https://indiafxguide-com.pages.dev/artigos/rbi-alert-list-95-entities-january-2026-verification-framework-indian-retail-trader-due-diligence)
- [U] The ETP framework is now cited as the "Master Direction – Reserve Bank of India (Electronic Trading Platforms) Directions, 2025". This came from a search summary of Alert List coverage; the primary text was not read. — [Upstox](https://upstox.com/news/personal-finance/trading/rbi-alert-list-updated-full-list-of-unauthorised-forex-trading-platforms-and-what-happens-if-you-use-them/article-184938)

**Legal INR currency derivatives (NSE / BSE / MSEI)**
- The RBI framework for currency futures and exchange-traded options on recognised exchanges also covers cross-currency futures and options. — [RBI notification: introduction of cross-currency futures and options](https://website.rbi.org.in/web/rbi/-/notifications/guidelines-on-trading-of-currency-futures-and-exchange-traded-currency-options-in-recognized-stock-exchanges-introduction-of-cross-currency-futures-and-exchange-traded-option-contracts-10172)
- **2024 framework.** The January 2024 circular took effect after a deferral to 3 May 2024.
  - Rupee derivatives, OTC or exchange-traded, are allowed only to hedge FX risk.
  - Participants with a valid contracted underlying exposure could hold positions up to $100M equivalent, across all INR pairs and NSE, BSE and MSEI combined, without producing documentary evidence.
  - Exchanges must ensure a valid underlying exposure exists.
  - Sources: [RBI notification (ETCD revised guidelines)](https://website.rbi.org.in/web/rbi/-/notifications/risk-management-and-inter-bank-dealings-revised-guidelines-relating-to-participation-of-a-person-resident-in-india-and-foreign-portfolio-investor-fpi-in-the-exchange-traded-currency-derivatives-etcd-market-11222); [Business Standard, Apr 2024](https://www.business-standard.com/amp/economy/news/rbi-defers-implementing-currency-derivatives-regulations-till-may-3-124040401233_1.html)
- **10 Oct 2026 change.**
  - The RBI cut that limit from $100M to **$5M** equivalent, still across all INR pairs and exchanges combined (Master Direction para 3.4(i)).
  - It also cut the matching OTC hedging threshold (no proof of underlying needed) to $5M across Authorised Dealers.
  - It introduced a 20% "Foreign Exchange Risk Reserve" for specified contracts.
  - All of this comes from secondary reports; the RBI circular text was not retrieved.
  - Sources: [Moneylife, 12 Oct 2026](https://www.moneylife.in/article/rbi-tightens-forex-derivatives-rules-cuts-exposure-limit-to-us5mn-introduces-20-percentage-cash-reserve/81913.html); [CorpLaw Updates](https://www.corplawupdates.in/updates/rbi-forex-derivative-curbs-ferr-october-2026); [Free Press Journal](https://www.freepressjournal.in/business/rbi-tightens-forex-derivative-rules-cuts-exposure-limit-to-5-million-introduces-20-risk-reserve); [Kotak Neo](https://www.kotakneo.com/news/regulations/rbi-tightens-forex-derivative-rules-and-introduces-risk-reserve/)

**Crypto tax**
- Budget 2022 introduced a 30% tax on income from transferring virtual digital assets (VDAs). — [Business Standard, 1 Feb 2022](https://www.business-standard.com/amp/article/news-ani/india-introduces-crypto-tax-of-30-per-cent-122020100724_1.html)
- [U] **Income-tax Act 2025** (assent 21 Aug 2025; in force 1 Apr 2026; secondary sources only, so verify against the Gazette):
  - The 30% charge moved from s.115BBH to s.194 (Table, Sl. 4).
  - The 1% TDS moved from s.194S to s.393(1) (Table, Sl. 8(vi)).
  - The VDA definition is s.2(111) per one source and s.2(109) per another.
  - TDS rises to 20% if the payee gives no PAN (s.397(2)).
  - Budget 2026-27 (1 Feb 2026) kept the 30% and 1% rates. It added penalties for platforms that fail to file crypto-transaction statements under s.509.
  - TDS thresholds are described inconsistently (₹10,000 in one source).
  - Sources: [Patron Accounting](https://www.patronaccounting.com/blog/crypto-vda-taxation-income-tax-act-2025-rules); [TDSMAN (May 2026)](https://blog.tdsman.com/2026/05/tds-on-virtual-digital-assets-section-3931-194s/); [CAclubindia](https://www.caclubindia.com/news/tds-on-virtual-digital-assets-under-income-tax-act-2025-key-rules-rate-threshold-and-compliance-26748.asp); [Dalimss](https://dalimss.news/articles/india-crypto-tax-2026-30-percent-vda-1-percent-tds-new-income-tax-act); [Toolisky](https://toolisky.com/blog/vda-tax-under-the-new-income-tax-act)

**FIU-IND registration of exchanges**
- In December 2023, FIU-IND issued show-cause notices to nine offshore exchanges, Binance among them, for operating in India without registration. Their websites were blocked and their apps delisted. Offshore virtual-asset service providers must register with FIU-IND to serve Indian users. — [Moneylife](https://moneylife.in/article/binance-slapped-with-rs1882-crore-penalty-by-indias-fiu-for-not-following-pmla-regulations/74453.html)
- **Binance** was fined ₹18.82 crore (~$2.2M) by an FIU-IND order dated 19 Jun 2024 under s.13 PMLA. It registered and resumed operations, in August 2024 per one report. KuCoin was fined ₹34.5 lakh. — [Moneylife](https://moneylife.in/article/binance-slapped-with-rs1882-crore-penalty-by-indias-fiu-for-not-following-pmla-regulations/74453.html); [Entrackr](https://entrackr.com/2024/06/financial-intelligence-unit-imposes-rs-18-82-cr-penalty-on-binance); [CoinDesk](https://hotfix.coindesk.com/policy/2024/06/20/binance-fined-22-million-by-indias-financial-intelligence-unit); [Inc42](https://inc42.com/buzz/fiu-slaps-inr-9-3-cr-penalty-on-crypto-platform-bybit)
- **Bybit** was fined ₹9.27 crore on 31 Jan 2025 (PIB release) and its websites were blocked. It paid the fine and registered, announced 6 Feb 2025. A consumer guide says full service resumed in September 2025 [U]. — [Inc42](https://inc42.com/buzz/fiu-slaps-inr-9-3-cr-penalty-on-crypto-platform-bybit); [Cointelegraph](https://cointelegraph.com/news/bybit-registers-with-india-s-fiu-settles-for-monetary-fine); [CoinDesk](https://hotfix.coindesk.com/policy/2025/02/06/crypto-exchange-bybit-receives-india-clearance-after-settling-usd1m-fine); [Outlook Money](https://www.outlookmoney.com/invest/bybit-restores-complete-crypto-trading-services-in-india-amid-compliance-push); [KK Investing guide](https://kkinvesting.io/en/posts/bybit-exchange-guide-india/)
- [U] About 49 exchanges, Indian and foreign, are reported as FIU-registered as of early 2026 (aggregator source; no official FIU list was retrieved). — [Pulse](https://www.pulse.bot/crypto/news/indias-crypto-exchanges-reach-49-registered-marking-regulatory-shift-5b3bc7cb-3e7a-4406-b74c-184a0606b2f0)

**Crypto futures availability**
- Crypto futures are not expressly banned in India, but they are not regulated the way NSE/BSE derivatives are. Guides advise using FIU-registered, compliant platforms. — [CoinSwitch guide](https://coinswitch.co/switch/crypto-futures-derivatives/crypto-futures-legal-india/); [Mudrex guide](https://mudrex.com/learn/crypto-futures-trading-legal-india/)
- [U] Indian FIU-registered platforms offering crypto derivatives (mostly comparison or listicle sources):
  - **Delta Exchange India:** INR-settled futures and options; operated by Excelium Technologies Pvt Ltd; up to 100× on perpetuals.
  - **Pi42:** INR perpetual futures; founded by Nischal Shetty and Avinash Shekhar; claims up to 150×.
  - **CoinDCX:** INR-based futures; US-stock perpetual futures added 17 Feb 2026 (up to 20×).
  - **Mudrex:** INR- and USDT-margined futures.
  - Sources: [AlgoTest (2026)](https://algotest.in/blog/best-crypto-trading-app-in-india-2026-top-exchanges-compared.md); [CoinCodeCap](https://coincodecap.com/coindcx-vs-pi42-vs-delta-exchange); [CXO Digital Pulse: Pi42 launch](https://www.cxodigitalpulse.com/wazirx-founder-nischal-shetty-ex-zebpay-ceo-avinash-shekhar-launch-crypto-futures-exchange-pi42); [Analytics Insight (2026)](https://www.analyticsinsight.net/cryptocurrency-analytics-insight/10-best-fiu-registered-crypto-exchanges-in-india-2026-guide)
- [U] Pi42 claims its INR-settled derivatives fall outside the 30% VDA tax and 1% TDS. Some CAs agree, but the interpretation is unsettled. — [CoinCodeCap](https://coincodecap.com/coindcx-vs-pi42-vs-delta-exchange)
- [U] Among offshore FIU-registered exchanges, Bybit offers futures and options to Indian users after KYC, per a consumer guide. — [KK Investing guide](https://kkinvesting.io/en/posts/bybit-exchange-guide-india/)

### Inferences
- **Personal analysis is not the regulated act.** Downloading public Binance or Yahoo data and computing levels for personal use is not a FEMA "transaction". The legal exposure lies in how a signal is acted on.
  - For EURUSD/XAUUSD signals, the non-permitted route is an offshore CFD/FX broker funded via LRS, including the 95 Alert-List names.
  - The domestic route is NSE/BSE currency derivatives (INR pairs and the permitted cross-currency contracts), which are formally restricted to hedging, with the no-documentation ceiling now $5M.
  - Gold would go through domestic commodity-exchange contracts; this was not researched.
- **Crypto.** Acting on the bot's crypto output on FIU-registered exchanges is legal. Spot gains are taxed at a flat 30% with 1% TDS on transfers. INR-settled futures sit in a legal and tax grey zone. Offshore unregistered exchanges are blocked or penalised.
- **For the report:** frame the bot as an analysis tool. Put any execution component behind the jurisdiction constraints above.

### Gaps
- RBI's official Alert List PDF and any 2026 additions were not retrieved.
- The primary text of the 10 Oct 2026 RBI circular was not retrieved: circular number, effective date, how the 20% "risk reserve" works, and whether exchange-traded cross-currency (non-INR) pairs are affected.
- No official Gazette text of the Income-tax Act 2025 was read, and the section numbers conflict. Rules not verified this session:
  - whether VDA losses still cannot be set off (true under the 1961 Act, per prior knowledge);
  - the exact TDS thresholds;
  - GST on exchange fees.
- Whether Binance offers futures to Indian users is unverified; third-party sources conflict.
- Whether TDS applies to crypto futures on offshore exchanges is unresolved.
- The status of DeFi perpetuals (e.g. Hyperliquid) for Indian residents was not researched.
