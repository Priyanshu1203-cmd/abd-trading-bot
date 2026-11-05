# Making a rule-based trading-levels bot measurably more accurate and trustworthy: validation methods and the evidence behind its techniques (NSE / Binance crypto / FX), as of 5 Nov 2026

Scope: a personal Python bot that computes PDH/PDL/PDC, CPR, floor pivots, 09:15-09:30 opening range, VWAP, fractal swing S/R zones (k bars each side, ATR-clustered, confluence-weighted), inferred liquidity pools and sweeps, a vote-based bias (EMA20/50, RSI 60/40, HH/HL, VWAP, CPR position), and 15-minute-close breakout setups with structure stops and zone targets of at least 1R. No backtest or live tracking exists yet.

Evidence grades used throughout: **[A]** peer-reviewed and replicated across markets or samples; **[B]** peer-reviewed single study, or a strong academic working paper; **[C]** unreviewed working paper or preprint, or a transparent practitioner replication; **[D]** vendor or marketing material, forum anecdote, or an untested convention. Where a figure comes from secondary coverage rather than the primary document, this is flagged inline.

## 1. What do academic and practitioner studies say about technical analysis in general and about the bot's specific techniques (ORB, intraday momentum, pivots/CPR, S/R and round numbers, VWAP, RSI/EMA rules, SMC/ICT liquidity sweeps), especially for NIFTY/BANKNIFTY, crypto and FX?

### Takeaway
The best-supported parts of the bot are time-of-day effects and intraday momentum (strong in US and developed markets and in Bitcoin, but untested on NIFTY), support/resistance near round numbers and stop-order clusters (FX order-book evidence), and slow trend-following on daily or weekly data. ORB and VWAP "edges" rest mainly on practitioner SSRN papers, and an independent 2026 replication found the ORB edge goes to about zero after realistic spread and slippage. Floor pivots and CPR have essentially no academic support. RSI 60/40 is folklore. SMC/ICT has no peer-reviewed test at all. Nothing in the literature validates these rules on NSE intraday data, and SEBI's loss studies (87.7-91% of individual F&O traders losing money in FY25-FY26) set a harsh prior that the bot must beat with its own out-of-sample evidence.

### Cited Findings

#### Technical analysis in general
- [A] Park & Irwin's survey (Journal of Economic Surveys 2007, 21(4):786-826): of 95 "modern" studies, 56 found technical trading profitable, 20 found negative results and 19 mixed. Early studies found profits in FX and futures but not in stocks. The authors flag data snooping, ex-post selection of rules, and difficulty estimating risk and transaction costs as major problems in the literature. — [IDEAS/RePEc](https://ideas.repec.org/a/bla/jecsur/v21y2007i4p786-826.html)
- [C] The 2004 working-paper version of that review reports that 30-40% of surveyed practitioners believe TA is an important driver of prices at horizons up to 6 months. — [AgEcon Search](https://ageconsearch.umn.edu/record/37487/files/AgMAS04_04.pdf)
- [B] Hsu, Taylor & Wang (Journal of International Economics 2016, 102:188-208) tested more than 21,000 rules on 30 developed and emerging currencies over 45 years of daily data, using a stepwise data-snooping test plus out-of-sample cross-validation. They found substantial predictability and excess profitability, which they attribute to temporarily not-fully-rational behaviour and market immaturity. — [EconPapers](https://econpapers.repec.org/RePEc:eee:inecon:v:102:y:2016:i:c:p:188-208)
- [C] A secondary summary of the same research reports that developed-market currency predictability ended by about 1996, while emerging currencies kept modest out-of-sample performance (not checked against the full text). — [CXO Advisory](https://cxoadvisory.com/technical-trading/updated-comprehensive-long-term-test-of-technical-currency-trading)
- [B] Hudson & Urquhart (Annals of Operations Research) tested about 15,000 rules from five classes on Bitcoin, Litecoin, Ethereum and Ripple. They found in-sample predictability and profitability in every class and coin, with significance surviving stationary-bootstrap p-values and multiple-hypothesis corrections, and breakeven costs well above typical crypto costs. However, **Bitcoin showed no out-of-sample predictability**, while the smaller coins still did. — [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1); [Reading repository](https://centaur.reading.ac.uk/85715)
- [A] Time-series momentum (Moskowitz, Ooi & Pedersen, JFE 2012, 104:228-250): an asset's own past excess return predicts its future return in all 58 liquid equity-index, currency, commodity and bond futures they studied. The effect persists about a year and then partially reverses. A diversified portfolio earned substantial abnormal returns and performed best in extreme markets. This is the strongest support for the bot's daily/weekly trend-bias logic. — [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:104:y:2012:i:2:p:228-250); [SSRN](https://papers.ssrn.com/abstract=2089463)

#### Intraday momentum and time-of-day
- [A] Gao, Han, Li & Zhou ("Intraday Momentum: The First Half-Hour Return Predicts the Last Half-Hour Return"), using SPY 1993-2013: the first half-hour return predicts the last half-hour return, with a predictive R² of 1.6% (2.6% after adding the 12th half-hour). The effect is stronger on volatile days, high-volume days, recession days and some macro-news days. Trading the last half-hour in the direction of the first earned 6.34% a year, gross of costs. — [Alpha Architect summary](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/); [working-paper PDF](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- [A] Li, Sakkas & Urquhart found significant first-half-hour to last-half-hour predictability in 12 of 16 developed markets, with the first half-hour measured from the prior close so that it includes overnight information. India was not in the sample. — [repository copy](https://nottingham-repository.worktribe.com/OutputFile/5273196) (via search summary)
- [A] Baltussen, Da, Lammers & Martens (JFE 2021, 142:377-403) studied more than 60 futures across equities, bonds and commodities, 1974-2020. The rest-of-day return predicts the last 30 minutes, and this reverses over the following days. The mechanism is hedging of short-gamma positions (option dealers, leveraged ETFs). Intraday momentum is much stronger on days with negative net gamma exposure and insignificant on positive-gamma days. — [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403); [authors' PDF](https://www3.nd.edu/~zda/intramom.pdf); [Alpha Architect](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/)
- [B] Bitcoin: Shen, Urquhart & Wang (Financial Review 2022) find first-half-hour to last-half-hour momentum on five exchanges (Bitfinex, Bitstamp, CEX.IO, Coinbase, Kraken), in and out of sample, driven by liquidity provision rather than late-informed trading. — [Reading repository](https://centaur.reading.ac.uk/100181)
- [B/C] Bitcoin shows significant negative first-order autocorrelation (mean reversion) at 1-, 2- and 4-hour horizons, with larger moves reversing more strongly. The authors attribute this to overreaction, excess volatility and cascading liquidations. — [LMU Munich repository](https://epub.ub.uni-muenchen.de/97651/)
- [B] "Turn-of-the-candle" effect (Heliyon 2023): Bitcoin's positive returns are concentrated in minutes 0, 15, 30 and 45 of each hour, and the effect persists out of sample. — [Northumbria research portal](https://researchportal.northumbria.ac.uk/en/publications/turn-of-the-candle-effect-in-bitcoin-returns/)
- [C] India: no NSE intraday-momentum study was found. A 2017 Nifty 50 intraday-pattern study reports an opening jump effect and a persistent end-of-session effect, with the first 20 minutes significant on all days of the week. — [Asian Journal of Management](https://indianjournals.com/article/ajm-8-3-082)

#### Opening range breakout (ORB)
- [B] Holmberg, Lönnbark & Lundström (Finance Research Letters 2013, 10(1):27-33) tested ORB on crude-oil futures. Returns were significantly above zero and the success rate was higher than a fair game. — [IDEAS](https://ideas.repec.org/a/eee/finlet/v10y2013i1p27-33.html)
- [C] Lundström's follow-up reports that average daily ORB returns differ by about 200 bp/day for crude oil and about 150 bp/day for S&P 500 futures between the highest and lowest volatility states. ORB profitability therefore depends heavily on the volatility regime. (Per search summary; full text not verified.) — [Umeå Economic Studies listing](https://econpapers.repec.org/RePEc:hhs:umnees:0948)
- [C] Zarattini, Barbon & Aziz (2024, SSRN 4729284 / Swiss Finance Institute RP 24-98) tested a 5-minute ORB restricted to "Stocks in Play", meaning stocks ranked by first-5-minute volume relative to their 14-day average. A top-20 portfolio reportedly returned more than 1,600% net, with a Sharpe ratio of 2.81 and 36% annualised alpha. — [IDEAS](https://ideas.repec.org/p/chf/rpseri/rp2498.html); [QuantConnect replication thread](https://quantconnect.com/forum/discussion/18444/Opening+Range+Breakout+for+Stocks+in+Play/p0/comment-37562)
- [C] The earlier Zarattini & Aziz (2023, SSRN 4416622) "Can Day Trading Really Be Profitable?" applied a 5-minute ORB to QQQ. — [CXO Advisory](https://www.cxoadvisory.com/individual-investing/intraday-trading-of-overactive-stocks-via-opening-range-breakout/)
- [C] Independent replication (T. Krueger, MQL5 blog, 25 Sept 2026) of the QQQ ORB rule (trade the first 5-minute candle's direction, stop at its far side, target 10R or the close) on NQ, SPX, Dow, DAX and FTSE CFDs, Jan 2015-Jun 2026:
  - **Gross result reproduced:** +0.05 to +0.13R per trade; NQ hit rate 23.2% vs the paper's 24%.
  - **Net result about zero:** after spread and slippage costing 6-12% of initial risk per trade, net expectancy was +0.002R for NQ and −0.04 to −0.08R for the other four markets.
  - **Weak years:** 2015-2017 were negative in every market.
  - **Costs in the paper:** commission only, no spread or slippage.
  - **Direction edge:** the first candle's direction beat a random-direction benchmark by +0.10 to +0.13R, about the size of trading costs.

  — [MQL5 blog](https://www.mql5.com/en/blogs/post/776235)

#### VWAP
- [C/D] Zarattini & Aziz (SSRN 4631351, Nov 2023), "VWAP: The Holy Grail for Day Trading Systems": go long above VWAP and short below it on QQQ, 2018 to Sept 2023. They report $25k growing to $192,656 (+671%), with 9.4% max drawdown and Sharpe 2.1, against buy-and-hold at +126%, 37% drawdown and Sharpe 0.7. The numbers circulate mainly through the authors' own trading-education material, and QuantConnect users posted a sceptical "not so fast" thread and reproductions. — [Concretum Group](https://concretumgroup.com/volume-weighted-average-price-vwap-the-holy-grail-for-day-trading-systems/); [Bear Bull Traders](https://bearbulltraders.com/?p=2606339); [QuantConnect thread](https://www.quantconnect.com/forum/discussion/16706/bear-bull-traders-039-paper-on-quot-the-holy-grail-quot-not-so-fast/)

#### Floor pivots and CPR
- [C] Public academic studies of pivot-point strategies are scarce; most backtests are proprietary or appear in blogs. (A 2013 paper in the *Journal of Theoretical and Applied Computer Science* is cited; its results were not retrieved.) — [QuantInsti](https://blog.quantinsti.com/pivot-point-strategy/)
- [C] Bulkowski's test on 1-minute intraday data found standard-formula floor pivots "worked" (price respected the level) 51-60% of the time, and Fibonacci pivots 28-36%. This measures whether price respected the level, not net profitability. — [ThePatternSite](https://thepatternsite.com/PivotPoints.html)
- No academic or rigorous practitioner test of CPR width, "narrow vs wide CPR", or two-day CPR relationships was found (see Gaps).

#### Support/resistance, round numbers and stop clusters ("liquidity pools")
- [A/B] Osler (Journal of Finance 2003, 58(5):1791-1819; FRBNY Staff Report 125) used about 9,700 stop-loss and take-profit orders at a large dealing bank (1 Sept 1999 to 11 Apr 2000; USD/JPY, GBP/USD, EUR/USD):
  - **Take-profit orders** cluster at round numbers, which explains why trends often reverse at S/R. They tend to reverse existing trends.
  - **Stop-loss orders** cluster just beyond round numbers, which explains why trends accelerate after a level breaks. They tend to propagate trends.

  — [NY Fed staff report](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf); [EconPapers (JF)](https://econpapers.repec.org/RePEc:bla:jfinan:v:58:y:2003:i:5:p:1791-1819)
- [C] Chung & Bellotti (arXiv 2101.07410, 2021):
  - **Reversals:** algorithmically discovered intraday S/R levels reverse price trends at statistically significant rates.
  - **Touch count:** a level that has seen more prior bounces is more likely to produce another bounce.
  - **Decay:** bounce probability falls as the level ages.
  - **Not noise:** the levels are not explained by AR(1) processes.
  - **Related work they cite:** Osler (2000), who found exchange-rate trends tend to stop at S/R levels, and Zapranis & Tsinaslanidis (2012), who found support levels interrupted trends better than resistance in US stocks but **did not beat buy-and-hold**.

  — [IDEAS (arXiv)](https://ideas.repec.org/p/arx/papers/2101.07410.html); [EconBiz record, Zapranis & Tsinaslanidis](https://www.econbiz.de/Record/identifying-and-evaluating-horizontal-support-and-resistance-levels-an-empirical-study-on-us-stock-markets/10010549298)

#### RSI / EMA rules
- [A] Trend persistence at the 12-month horizon is robust (time-series momentum above). — [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:104:y:2012:i:2:p:228-250)
- [B/C] Short-horizon technical rules have decayed in liquid markets: developed-currency rule predictability reportedly ended by about 1996, and Bitcoin rule predictability disappeared out of sample. — [CXO Advisory](https://cxoadvisory.com/technical-trading/updated-comprehensive-long-term-test-of-technical-currency-trading); [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1)
- No study testing an "RSI 60/40 range" regime or EMA20/50 alignment as an intraday bias filter was found (see Gaps).

#### SMC / ICT liquidity sweeps
- [D] No peer-reviewed empirical test of ICT/SMC concepts was found. One blog reports a Crossref search on 27 Sept 2026 that found none, and cites an unreviewed 2026 preprint concluding that ICT/SMC concepts do not work as literally taught. The preprint could not be located or verified. — [Thor Trade Copier blog](https://thortradecopier.com/blog/does-ict-smart-money-concepts-work)
- [D] A vendor backtest of a 5-year liquidity-sweep strategy on EURUSD and XAUUSD reports 1,247 trades, profit factor 1.68 and 53.2% win rate with a "kill-zone" time filter. It is commercial and unaudited. — [Backtrex](https://backtrex.com/en/blog/liquidity-sweep-strategy-backtest-results)
- [D] The usual definition of a liquidity sweep (price runs through a stop cluster and then reverses) is the core claim of the method, not an empirical result. — [LuxAlgo](https://www.luxalgo.com/library/concept/liquidity-sweep/)

#### Indian reality checks (regulator data and related)
- **SEBI FY25 F&O study:** 91% of individual traders lost money. Net losses were ₹1,05,603 crore, up from ₹74,812 crore in FY24 (top 13 brokers, about 96 lakh unique traders). — [Business Standard](https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html)
- **SEBI FY26 F&O study** (secondary coverage, Aug 2026):
  - 87.7% of individual traders lost money; aggregate losses ₹91,685 crore; average loss about ₹1.17 lakh.
  - Individuals paid about ₹25,000 crore in transaction costs.
  - Active individual traders fell from 98.1 lakh to 78.6 lakh.
  - 59% of index-options turnover happened on expiry day, and about 75% within one day of expiry.
  - Higher trading intensity relative to capital was linked to higher loss rates.
  - FY25 losses are restated at about ₹1.12 lakh crore.

  — [Open Magazine](https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26)
- **SEBI intraday equity-cash study** (released 24 Jul 2024, FY23 data):
  - 71% of individual intraday traders made net losses.
  - The loss rate was 80% among traders making more than 500 trades a year, and 76% among under-30s.
  - Loss-makers' trading costs equalled 57% of their trading losses; profit-makers' costs equalled 19% of their profits.

  — [SEBI press release](https://www.sebi.gov.in/media-and-notifications/press-releases/jul-2024/sebi-study-finds-that-7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses_84948.html)
- [B] Persistent day-trading skill is rare. Barber, Lee, Liu & Odean (Journal of Financial Markets 2014; Taiwan 1992-2006) document large cross-sectional differences in before- and after-fee returns. In their companion paper, day traders with prior profits are only 1.6% of all day traders but 12% of day-trading volume. — [paper PDF](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf); [companion PDF](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/day%20trading%20and%20learning%20110217.pdf)
- **Jane Street order (interim regulator allegation, not finally adjudicated):** SEBI's 3 July 2025 interim order alleged that Jane Street entities distorted BANKNIFTY on expiry days between Jan 2023 and Mar 2025. The alleged method was buying constituents and their futures aggressively in the morning while holding large options positions. ₹4,843.57 crore was impounded, and Jane Street disputes the findings. — [Moneylife explainer](https://moneylife.in/article/explainer-what-are-sebis-findings-on-jane-street-groups-market-manipulation/77594.html); [Tribune](https://www.tribuneindia.com/news/business/sebi-imposes-highest-ever-penalty-of-rs-4843-57-crore-on-jane-street-group-for-index-manipulation); [ECGI blog](https://www.ecgi.global/publications/blog/expiry-day-and-the-governance-of-algorithmic-trading-the-jane-street-episode)

### Inferences
- **Evidence grade by bot component** (synthesis of the findings above):

| Bot component | Best evidence | Grade | Markets covered | What it implies for the bot |
|---|---|---|---|---|
| Time-of-day / intraday momentum (first vs last half-hour) | Gao et al.; Li et al.; Baltussen et al. (JFE); Shen et al. (BTC) | A (US/developed), B (BTC), none for NSE | US, 12/16 developed, BTC | Test it directly on NIFTY/BANKNIFTY futures. It is a candidate *conditioning* feature, and the effect is small (R² about 1.6%). |
| Trend bias on daily/weekly bars (EMA alignment, HH/HL) | Time-series momentum (JFE) | A at 1-12 month horizons | 58 futures | Justified for swing/long-term versions. Intraday use of EMA20/50 is not directly supported. |
| S/R zones, touch counts, round numbers | Osler (JF), Chung & Bellotti (arXiv), Zapranis & Tsinaslanidis | A/B mechanism, C for level reactions | FX, US stocks, intraday series | Keep S/R zones, add round numbers as a level type, and use touch count and level age as features. Reactions are real but did not beat buy-and-hold in the stock study. |
| ORB 09:15-09:30 | Holmberg et al. (FRL, crude), Zarattini SSRN, Krueger replication | B/C; net edge on indices about zero after costs | Crude, US stocks/ETFs, index CFDs | Treat ORB as a volatility and participation context filter, not a standalone edge. It needs a volatility-state and relative-volume condition. |
| VWAP side | One practitioner SSRN paper plus sceptics | C/D | QQQ | Use as context, not a vote with proven weight. Test it. |
| Floor pivots / CPR | Bulkowski touch rates, blogs | C/D | US intraday | Unproven. Must beat PDH/PDL/PDC and random levels before it gets any weight. |
| RSI 60/40 | None found | D | n/a | Folklore until tested. |
| SMC/ICT sweeps | Vendor backtests only; Osler's stop-cluster theory is the closest academic anchor | D (B for the underlying mechanism) | FX/gold vendor tests | Reframe as a "stop-cluster" hypothesis and test both reversal and cascade outcomes. |

- **CPR width is a function of where yesterday closed, not of how wide yesterday's range was.** This follows algebraically from the standard definitions BC = (H+L)/2, P = (H+L+C)/3, TC = 2P − BC:
  - CPR width = |TC − BC| = |2C − H − L|/3 = (2/3)·|C − (H+L)/2|.
  - So width ranges from 0 (close exactly mid-range) to (H−L)/3 (close at the high or low).
  - A "narrow CPR" therefore means "yesterday closed near the middle of its range". A wide-range day that closes mid-range also gives a narrow CPR, so CPR width mixes range compression with close location.
  - Test the "narrow CPR → trending day" claim against two simpler baselines: previous-day range percentile (NR4/NR7-style) and close-location value. If CPR width adds nothing beyond them, drop it.
- **Floor pivots and CPR double-count PDH/PDL/PDC.** P, R1 = 2P − L, S1 = 2P − H and the CPR lines are all deterministic functions of yesterday's H, L and C. Counting "PDH plus R1 plus TC nearby" as three independent confluence votes overstates the evidence, so confluence weights must be fitted jointly (Section 3), not added by hand.
- **The five bias votes are highly collinear.** EMA20/50 alignment, RSI above or below 60/40, HH/HL structure, price vs VWAP and price vs CPR all measure recent direction. "5 of 5 votes" is closer to one piece of evidence than five. Use ablation tests to find which vote, if any, adds out-of-sample value.
- **Liquidity sweeps can be made testable.** Osler's order data predicts two outcomes when price pierces a level: reversal if take-profit liquidity dominates, and acceleration (a cascade) if stop-losses dominate. The bot's "wick through, close back inside" sweep rule is a testable conditional of this. Measure P(reversal of at least x ATR before continuation of y ATR | sweep) against the same statistic for random pierces of non-pool levels. Crypto liquidation cascades (Section 4) fit the cascade branch.
- **Opening range on NSE:** the evidence suggests ORB value comes from volatility state and participation (relative volume, "stocks in play") rather than from the breakout itself, and the remaining edge is about the size of costs. A 09:15-09:30 range breakout on NIFTY should be tested with explicit conditions: gap size, India VIX or ATR percentile, relative first-15-minute volume, and expiry or event day.
- **VWAP data caveats:**
  - NIFTY/BANKNIFTY spot indices have no traded volume of their own, so "index VWAP" has to be built from futures (or constituent) volume, with continuous-contract roll handling.
  - Spot FX is OTC with no consolidated volume, so FX VWAP depends on the broker's tick volume. It should get lower trust and be validated separately.
  - (Both points are reasoning, not sourced findings.)
- **Where an edge is plausible:** a durable edge is more likely from conditioning (time of day, volatility state, event and expiry regime, relative volume) plus disciplined execution and costs than from any single level type. The literature's surviving effects (intraday momentum, S/R order clustering, volatility dependence of ORB) are all conditional.
- **Expiry days need their own regime.** In India, expiry days concentrate most options turnover (59% of index-options turnover in FY26), and regulator allegations involve intentional index moves on BANKNIFTY expiry days. Level reactions there may differ systematically from normal days.

### Gaps
- No peer-reviewed or rigorous out-of-sample study of ORB, intraday momentum, pivots/CPR, VWAP or RSI/EMA rules on NIFTY/BANKNIFTY intraday data was found. The only NSE-specific intraday study retrieved (2017) covers time-of-day patterns, not strategies.
- No study of CPR width, two-day CPR relationships (higher/lower/overlapping/inside value), or "virgin CPR" was found. These remain practitioner lore (Frank Ochoa's "Pivot Boss" framework is the usual source, but it was not retrieved here).
- No evidence for the "RSI 60/40 range-shift" rule specifically.
- The 2026 SMC/ICT preprint mentioned by one blog could not be located, and Wen, Bouri, Xu & Zhao (2022, crypto intraday momentum vs reversal) was found only as a bibliographic record, so its results are unknown.
- Holmberg et al.'s sample period and cost treatment, and the sample period of Zarattini et al. (Stocks in Play), were not verified from full text.
- Whether the Gao et al. effect has decayed since publication was not checked.
- Round-number (psychological barrier) evidence for Indian indices or crypto was not searched.

## 2. What is best-practice backtesting for this bot (event-based trigger tests, walk-forward/out-of-sample, look-ahead and survivorship bias, realistic Indian costs, overfitting and multiple-testing controls)?

### Takeaway
Treat every trigger as an event with a triple-barrier outcome (target, stop or time-out, whichever comes first). Simulate it using only information timestamped before the decision, with fractal swings entering the level set only k bars after the pivot. Charge India's post-April-2026 costs: STT on futures is now 0.05% and on options 0.15% of premium. Judge results only out-of-sample, with explicit multiple-testing controls: the Deflated Sharpe Ratio, the Probability of Backtest Overfitting, and a t-statistic hurdle of about 3. NSE's market structure changed four times between Nov 2024 and Aug 2026: BANKNIFTY weekly options ended, expiry moved to Tuesday, STT rose, and a closing auction with a 3:40 pm derivatives close arrived. Intraday history must therefore be split into regimes, and daily "close" definitions must be pinned down.

### Cited Findings

#### Overfitting and multiple testing
- [B] Deflated Sharpe Ratio (Bailey & López de Prado, Journal of Portfolio Management 2014, 40(5):94-107): corrects the Sharpe ratio for selection bias from multiple testing and for non-normal returns. — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551)
- [B] Probability of Backtest Overfitting (Bailey, Borwein, López de Prado & Zhu, Journal of Computational Finance 20(4)): estimates the probability that the best in-sample configuration underperforms the median configuration out-of-sample, using combinatorially symmetric cross-validation (CSCV). — [SSRN 2326253](https://papers.ssrn.com/abstract=2326253)
- An R package `pbo` on CRAN implements CSCV and accepts metrics other than Sharpe. — [CRAN vignette](https://archive.linux.duke.edu/cran/web/packages/pbo/vignettes/pbo.html)
- [A] Harvey, Liu & Zhu (Review of Financial Studies 2016, 29(1):5-68): after accounting for hundreds of tested factors, a newly discovered factor needs a t-statistic above about 3.0, not 2.0. They argue most claimed findings in financial economics are likely false. — [NBER w20592](https://nber.org/papers/w20592)
- [B] Worked examples of data-snooping control in TA research:
  - Hudson & Urquhart compared each rule's p-value with 1,000 stationary-bootstrap p-values and applied multiple-hypothesis procedures. Bitcoin's in-sample edge still failed out of sample. — [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1)
  - Hsu et al. used a stepwise data-snooping test across 21,000+ rules. — [EconPapers](https://econpapers.repec.org/RePEc:eee:inecon:v:102:y:2016:i:c:p:188-208)

#### Event labeling and cross-validation for overlapping trades
- *Advances in Financial Machine Learning* (López de Prado, Wiley 2018) places triple-barrier labeling and meta-labeling in chapter 3, and purged K-fold cross-validation with an embargo in chapter 7. — [AFML table of contents](https://toc.uni.li/FLMF049641.pdf)
- **Triple-barrier labeling:** each event gets a profit-take barrier, a stop-loss barrier and a time limit. The label is whichever barrier is touched first, so a trade that would have been stopped out is a loss even if price later recovered. **Purging** removes training observations whose label windows overlap the test fold. An **embargo** of h bars follows each test set. (Secondary explainers; some quantitative claims on these sites, such as "naive k-fold overstates Sharpe by 10-30%", are unverified and not relied on here.) — [Purging & embargo explainer](https://5x5x5x5.github.io/quant-lessons/backtest/purging-embargo/); [LuxAlgo label-definition note](https://www.luxalgo.com/library/concept/label-definition-and-prediction-horizon.md)

#### Look-ahead and repainting
- Pivot and fractal functions need future bars to confirm a pivot. `ta.pivothigh(5,5)` can only confirm a pivot 5 bars after it happened, and drawing the label back on the pivot bar ("repainting by relocation") makes history look better than live trading. Acting only on confirmed data adds delay. — [CrossTrade blog](https://blog.crosstrade.io/pine-script-repainting/); [J. Rana, Pine repainting fix](https://jayadevrana.com/pine-script-repainting-fix/)
- TradingView defines repainting as script behaviour where historical and real-time calculations differ, a consequence of the difference between historical bars and real-time bar information. — [Pine Script docs (v5 mirror)](https://br.tradingview.com/pine-script-docs/en/v5/concepts/Repainting.html)
- TradingView: higher-timeframe requests with lookahead "peek into the future" and produce unrealistically good results. Lookahead is off by default, and offsetting the series by one bar (`[1]`) avoids the leak. — [TradingView support](https://tradingview.com/support/solutions/43000614705-strategy-produces-unrealistically-good-results-by-peeking-into-the-future)

#### NSE data-timing facts the backtest must encode (current as of Nov 2026)
- **Old closing price:** NSE's official equity closing price was the volume-weighted average of all trades in the last 30 minutes (3:00-3:30 pm). If a stock did not trade in that window, its last traded price was used. The official close therefore differs from the last traded price in a 15-minute candle. — [EquitiesIndia glossary](https://equitiesindia.com/glossary/closing-price-weighted-average); [Motilal Oswal](https://www.motilaloswal.com/learning-centre/2023/7/why-is-there-a-difference-between-the-ltp-and-closing-price-on-nse)
- **Closing Auction Session (CAS):** live from 3 August 2026 for F&O-eligible stocks. It replaces the 3:00-3:30 pm 30-minute VWAP with a single equilibrium price from a 20-minute auction phase. — [The TRADE](https://www.thetradenews.com/sebi-launches-new-equities-closing-auction/); [NSE circular](https://nsearchives.nseindia.com/content/circulars/CMTR75479.pdf)
- **New schedule (reported):** continuous trading in F&O stocks ends at 3:15 pm, the auction runs until 3:35 pm, and equity derivatives close at 3:40 pm. (Taken from search-summary text of the explainer.) — [Outlook Money explainer](https://www.outlookmoney.com/amp/story/invest/nse-extended-fo-timings-and-new-closing-auction-session-rules-explained)
- **Derivatives segment:** from 3 Aug 2026 the normal market closes at 3:40 pm, and the derivatives closing price is the VWAP of trades from 3:10 to 3:40 pm. The pre-open session is unchanged (9:00-9:08 am). — [Angel One](https://www.angelone.in/news/market-updates/nse-extends-equity-derivatives-trading-hours-till-3-40-pm-starting-august-3-2026-set-to-introduce-closing-auction-session-in-equity-cash-segment)
- **Expiry calendar (secondary broker sources, not SEBI circulars):** NSE derivative expiries moved to Tuesday from 1 Sept 2025, after SEBI asked exchanges in May 2025 to choose Tuesday or Thursday. NIFTY is the only NSE index with weekly options. BANKNIFTY weekly options were discontinued from Nov 2024 under SEBI's one-benchmark-per-exchange rule, leaving it monthly-only (last Tuesday). BSE's Sensex weekly expiry is Thursday. — [Angel One](https://www.angelone.in/news/market-updates/nifty-weekly-expiry-today-see-what-changed-on-sept-1-2025); [Zerodha support](https://support.zerodha.com/category/trading-and-markets/trading-faqs/f-otrading/articles/weekly-expiries-discontinued-for-certain-index-derivatives); [TradingQnA](https://tradingqna.com/t/sebi-confirms-derivatives-expiries-tuesday-for-nse-thursday-for-bse/183366)

#### Current Indian transaction costs (Zerodha schedule, read 5 Nov 2026)

| Charge | Equity intraday | Futures | Options |
|---|---|---|---|
| Brokerage | 0.03% or ₹20 per executed order, whichever is lower | 0.03% or ₹20 per order, whichever is lower | Flat ₹20 per order |
| STT | 0.025% on sell | 0.05% on sell | 0.15% of premium on sell; 0.15% of intrinsic value on exercise |
| NSE transaction charge | 0.00307% | 0.00183% | 0.03553% of premium |
| GST | 18% on (brokerage + SEBI fee + transaction charges) | same | same |
| SEBI fee | ₹10 per crore | ₹10 per crore | ₹10 per crore |
| Stamp duty | 0.003% on buy | 0.002% on buy | 0.003% on buy |

— [Zerodha charges](https://zerodha.com/charges)

- The Union Budget 2026 raised STT on futures to 0.05% (from 0.02%) and on options premium to 0.15% (from 0.1%), effective 1 April 2026. — [Business Today](https://www.businesstoday.in/markets/stocks/story/zerodha-doubling-fees-for-select-intraday-trades-who-will-be-impacted-522295-2026-03-25)
- From 1 April 2026, Zerodha charges ₹40 instead of ₹20 per order on intraday F&O trades the broker has to fund because of a cash shortfall, meaning trades placed without the 50% cash-collateral margin rule being met. — [Business Today](https://www.businesstoday.in/markets/stocks/story/zerodha-doubling-fees-for-select-intraday-trades-who-will-be-impacted-522295-2026-03-25)

#### Cost realism evidence
- In the 2026 ORB replication, spread and slippage alone consumed 6-12% of initial risk per trade and turned a reproducible gross edge into zero or negative net expectancy. — [MQL5 blog](https://www.mql5.com/en/blogs/post/776235)
- SEBI: intraday loss-makers' costs were 57% of their trading losses (FY23), and individual F&O traders paid about ₹25,000 crore in transaction costs in FY26. — [SEBI press release](https://www.sebi.gov.in/media-and-notifications/press-releases/jul-2024/sebi-study-finds-that-7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses_84948.html); [Open Magazine](https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26)

### Inferences
- **Bot-specific look-ahead checklist.** Each item below is a concrete leakage path in the described design.
  1. **Fractal swings (k bars each side).** A swing at bar t exists only from the close of bar t+k. Store `confirmed_at = t+k` and let only confirmed swings enter zones, pools, "unswept" status and equal-high/low detection. With k = 3 on 15-minute bars, a swing becomes usable 45 minutes later.
  2. **Zone clustering and strength.** Compute the ATR tolerance, touch counts and confluence weights using data up to the decision bar only. Re-clustering on the full history leaks future touches into the past.
  3. **Signals on bar close.** A 15-minute-close breakout is known only after that bar closes. Fill at the next bar's open (or the next tick) plus slippage, not at the signal bar's close. The 5-minute sweep bars must be aligned inside their 15-minute parent bar.
  4. **Same-bar ambiguity.** If stop and target both fall inside one 5- or 15-minute bar, count the stop as hit first, or resolve the order with 1-minute data. Optimistic resolution is a classic way intraday backtests overstate results.
  5. **Daily and weekly levels.** Use only completed prior sessions. On NSE, decide whether "previous close" means the official close (CAS price for F&O stocks since 3 Aug 2026; 30-minute VWAP before that; futures close = 3:10-3:40 pm VWAP) or the last traded price, and apply it consistently. Pivots and CPR computed from different "closes" give different levels.
  6. **Opening range.** It is known only after the 09:15-09:30 bar closes. Nothing before 09:30 may use it.
  7. **Rolling percentiles.** The CPR-width percentile and any "ATR percentile" must use a trailing window, never full-sample percentiles.
  8. **Higher-timeframe bias.** EMA, RSI and structure from a higher timeframe must use the last completed higher-timeframe bar (the `request.security` lookahead problem).
  9. **Day boundaries.** NSE runs on IST sessions, Binance on its daily-kline boundary (commonly 00:00 UTC; verify), and FX on the broker's or New York 17:00 rollover (verify). Daily pivots differ by convention, so fix one per market and record it.
  10. **Corporate actions and futures rolls.** Split or bonus adjustments change historical swing levels. Index-futures VWAP and levels need explicit roll rules on expiry days.
  11. **Survivorship.** Pick "large caps" using point-in-time NIFTY 50/100 membership, not today's list. For crypto, include coins Binance has since delisted if the universe is chosen by rank.
- **A simple leakage test.** For a random sample of timestamps t, recompute every feature and signal from data truncated at t and compare with the values from the full-history run. They must be identical. Any difference is look-ahead. This catches all of items 1-8 at once.
- **Event-study harness, one row per trigger.** Record:
  - Entry time and price, side, setup type and level type.
  - Stop and target in price and in R.
  - Barrier outcome (target-first, stop-first or time-out at session end or N bars), MFE/MAE in R, and time to outcome.
  - Net R after costs.
  - The full point-in-time feature vector.

  Then report hit rate with Wilson intervals, mean net R, profit factor and distribution tails by setup, level type, instrument, time-of-day bucket and regime.
- **Baselines that define "better than generic tools":**
  - (a) Random entries at the same time of day with identical stop and target geometry.
  - (b) Random or shifted levels drawn from the same distance-to-price distribution.
  - (c) Plain PDH/PDL/PDC levels only.
  - (d) Standard floor pivots from a generic charting tool.
  - (e) First-candle direction vs random direction (the Krueger-style benchmark).

  A level type or trigger earns weight only if it beats these out-of-sample, net of costs. The level-reaction test should mirror Chung & Bellotti's bounce probability vs a null model.
- **Worked cost examples** (current Zerodha rates, round trip, flat price, slippage excluded; my arithmetic):
  - **Equity intraday, ₹1,00,000 each way:** brokerage ₹40, STT ₹25, NSE ₹6.14, SEBI ₹0.20, GST ₹8.34, stamp ₹3. Total about ₹82.7, or 8.3 bp. At ₹5,00,000 the total is about ₹224.6 (4.5 bp), because brokerage is capped.
  - **Index futures, ₹10,00,000 notional each way:** brokerage ₹40, STT ₹500, NSE ₹36.6, SEBI ₹2, GST ₹14.15, stamp ₹20. Total about ₹612.8, or 6.1 bp. STT alone was ₹200 on this trade before 1 April 2026.
  - **Options, ₹10,000 premium each way:** total about ₹70.9, or 0.71% of premium. At ₹1,00,000 premium it is about ₹284, or 0.28%.
- **Costs as a fraction of R decide whether tight intraday stops are viable.**
  - With a futures stop 0.30% from entry, costs of about 0.061% are about 0.20R before slippage. With a 0.60% stop they are about 0.10R.
  - Breakeven hit rate is p* = (1 + c)/(1 + R_target), where c is round-trip cost in R. With c = 0.2: a 1R target needs 60%, 1.5R needs 48% and 2R needs 40%. With c = 0.1, a 1R target needs 55%.
  - This argues for (i) preferring targets of at least 1.5-2R, (ii) filtering out setups whose stop is under a few multiples of round-trip cost (Krueger filtered at risk of at least 2× cost), and (iii) charging slippage measured from your own fills.
- **Walk-forward with locked holdout and structural-break awareness.**
  - Roll train/test windows, for example 12 months train and 3 months test, choosing parameters only in-sample. Keep a final holdout untouched until the end; the post-CAS period from 3 Aug 2026 is a natural one.
  - Segment NSE history at Nov 2024 (SEBI F&O measures and the end of BANKNIFTY weeklies), 1 Sept 2025 (Tuesday expiry), 1 Apr 2026 (STT hike) and 3 Aug 2026 (CAS and the 3:40 pm derivatives close). Report metrics per segment, because a rule tuned on 2023 BANKNIFTY weekly-expiry dynamics may not transfer.
- **Multiple-testing accounting.** Log every configuration ever tried: k, ATR tolerance, ATR stop bounds, minimum R, vote thresholds, timeframe and instrument. Compute DSR using the number of trials and PBO via CSCV over the configuration grid, and require t of at least 3 before adopting a new filter. A rule that only "works" on one symbol or one parameter value should be presumed overfit.

### Gaps
- Specific references on anchored versus rolling walk-forward, and on López de Prado's combinatorial purged CV for backtest paths, were not retrieved. Only purged K-fold, embargo, CSCV/PBO and DSR were verified.
- How NIFTY 50 and BANKNIFTY spot values and closing values behave during the new 3:15-3:35 pm CAS window (static, indicative or auction-based) was not verified. Check NSE Indices methodology notes and your data vendor's 15-minute candles after 3 Aug 2026.
- A separate "September 7, 2026" phase was mentioned in one search summary without details. Angel One says pre-open is unchanged. Verify against NSE circulars.
- No measured slippage figures for NIFTY/BANKNIFTY futures or options at retail size were found. Binance fee tiers, funding costs, and FX broker spreads and swaps were not researched here.
- No source was found for point-in-time NSE index-constituent histories, needed to remove survivorship bias.
- The STT change was verified through Zerodha's live schedule and Business Today, not the Finance Act text itself.

## 3. How should forward testing work (paper-trading journal, hit rates per level type, calibrating confluence weights from data), and when does light machine learning (logistic regression, gradient boosting) help versus overfit?

### Takeaway
Run the bot in timestamped "shadow mode" with an append-only journal of every alert and its eventual triple-barrier outcome. Estimate hit rates per level type with confidence intervals, and replace hand-set confluence weights with a regularised logistic regression fitted walk-forward on event outcomes, checked for calibration. Gradient boosting or other ML should come in only as a meta-labeling filter or sizer on top of the rule-generated candidates, once there are thousands of labelled events and purged cross-validation. Below that, it is the most likely way to overfit.

### Cited Findings
- Meta-labeling separates the decision of *side* (the primary rule) from *whether to act and how much to size* (a secondary model). Joubert, "Meta-Labeling: Theory and Framework" (Journal of Financial Data Science, Summer 2022, 4(3):31-44), and Meyer, Barziy & Joubert, "Meta-Labeling: Calibration and Position Sizing" (JFDS, Spring 2023, 5(2):23-40), formalise this, including probability calibration for sizing. (Citation details via secondary listings; results not retrieved.) — [Hudson & Thames](https://hudsonthames.org/category/advances-in-financial-machine-learning/page/2/); [Meta-Labeling draft encyclopedia entry (mirror)](https://wikiless.lunar.icu/wiki/Draft:Meta-Labeling?lang=en)
- Triple-barrier labels (target-first, stop-first, time-out) and meta-labeling are in AFML chapter 3, and purged/embargoed CV in chapter 7. These are designed for exactly the overlapping, path-dependent labels a target/stop bot produces. — [AFML table of contents](https://toc.uni.li/FLMF049641.pdf); [purging & embargo explainer](https://5x5x5x5.github.io/quant-lessons/backtest/purging-embargo/)
- S/R levels with more prior bounces are more likely to bounce again, and bounce probability decays with level age. Touch count and age are therefore empirically motivated features for weighting zones. — [IDEAS (arXiv 2101.07410)](https://ideas.repec.org/p/arx/papers/2101.07410.html)
- [A] Multiple-testing hurdles (t > 3) and overfitting diagnostics (PBO, DSR) apply to ML feature and model searches just as to rule searches. — [NBER w20592](https://nber.org/papers/w20592); [SSRN 2326253](https://papers.ssrn.com/abstract=2326253); [SSRN 2460551](https://papers.ssrn.com/abstract=2460551)
- A random-direction benchmark showed that the first-candle signal's real edge (+0.10 to +0.13R) was only as large as costs. This is a practical template for judging whether a signal beats chance. — [MQL5 blog](https://www.mql5.com/en/blogs/post/776235)
- In-sample TA predictability can vanish out of sample even after bootstrap corrections (Bitcoin), which is why forward and out-of-sample checks are non-negotiable. — [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1)

### Inferences
- **Journal schema** (one immutable row per alert, written at alert time; outcome fields appended later):
  - **At alert time:** timestamp (exchange time zone), instrument, timeframe, setup type and side; trigger level and its type (PDH, CPR, pivot, OR high, swing zone, pool, round number); level age and touch count; confluence components; bias votes; CPR-width and ATR percentiles; gap; time-of-day bucket; expiry or event flag; India VIX or funding context; planned entry, stop and target, R multiple and estimated costs; bot version or git hash.
  - **Appended later:** fill price, slippage, barrier outcome, MFE/MAE in R, net R, and notes.
  - Hash each row, or store it append-only, so history cannot be edited in hindsight. This is the core of "trustworthy".
- **Sample sizes** (binomial arithmetic):
  - A hit rate near 50% has a 95% interval of about ±9.8 pp at n = 100, ±4.9 pp at n = 400 and ±3.1 pp at n = 1,000.
  - Distinguishing a 55% level type from a 50% one with 80% power needs about 1,565 events per group.
  - So per-level-type hit rates from a few weeks of paper trading are mostly noise. Pool across instruments within an asset class, and use the backtest event set for estimation and the forward test for confirmation.
- **Calibrating confluence weights.**
  - Fit an L2-regularised logistic regression of P(target before stop) on point-in-time features: level-type dummies, touch count, age, distance in ATR, time of day, regime flags, CPR/ATR percentiles and bias-vote components. Fit it walk-forward only.
  - Convert the coefficients into the "confluence score". Check calibration with reliability curves and the Brier score, and recalibrate (Platt or isotonic) if needed.
  - Show each alert's calibrated probability together with its uncertainty. A user can then compare the stated 58% against the realised hit rate of all alerts that said 58%. That is a measurable trust property generic tools lack.
- **When ML helps:**
  - There are at least a few thousand labelled events per asset class.
  - Features are point-in-time and tested for leakage.
  - Labels come from the triple barrier.
  - CV is purged and embargoed.
  - The model acts as a meta-label filter or sizer on rule candidates rather than generating trades.
  - The comparison baseline is the logistic model, and the improvement is judged on net expectancy and calibration out-of-sample, not on accuracy or AUC alone.
  - Shallow gradient-boosted trees with monotone constraints and early stopping are a reasonable step up from logistic regression.
- **When ML overfits:**
  - Only hundreds of events, with dozens of features.
  - Overlapping labels without purging.
  - Hyperparameters tuned on the test period.
  - Training across NSE structural breaks without regime features.
  - Repeated "peeking" at the holdout.
  - Any of these should trigger DSR and PBO checks, and a strong prior that the simpler model wins.
- **Forward-test protocol:**
  - Run at least about 3 months or about 300+ alerts per asset class in shadow mode before risking capital, then trade small size.
  - Compare live fill slippage and outcome distributions with the backtest's (for example with a KS test on R outcomes).
  - Pre-register kill-switch rules, such as pausing if rolling 100-trade expectancy falls below the backtest's 5th percentile.
  - Re-estimate weights on a fixed schedule, not after drawdowns.

### Gaps
- No empirical study was found that quantifies how far retail paper-trading results diverge from live results for intraday rule-based bots.
- The quantitative results of the meta-labeling papers (Joubert 2022; Meyer et al. 2023) were not retrieved, so their claimed improvements cannot be cited.
- No study was found on the minimum event counts at which gradient boosting beats logistic regression for TA-feature trade filtering. The thresholds above are reasoning, not citations.

## 4. Which extra data most improves intraday accuracy (India: option-chain OI and PCR, India VIX, FII/DII flows, GIFT Nifty, market breadth, event calendar including RBI policy, results and expiry days; crypto: funding, OI, liquidations; FX: session timing and economic calendar)?

### Takeaway
The best-evidenced additions are not new "levels" but **regime flags**: the scheduled-event calendar (macro releases for FX and crypto; expiry, RBI and results days for India) and **volatility state** (India VIX or ATR percentile). Intraday momentum and ORB effects are documented to be stronger on volatile and news days, and FX prices jump on announcement surprises. Option-dealer gamma has strong US evidence as a driver of end-of-day momentum but no Indian test. PCR, OI walls, FII/DII flows and GIFT Nifty have only weak, old or vendor evidence as intraday predictors. For crypto, order-flow imbalance and liquidation data look more informative at short horizons than funding or OI, though the evidence there is mostly blog-grade.

### Cited Findings

#### India
- **Event days:** intraday momentum is stronger on volatile, high-volume, recession and some macro-news days (US evidence). — [Alpha Architect summary of Gao et al.](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- **Volatility state:** ORB daily returns differ by about 150-200 bp/day between the highest and lowest volatility states (crude, S&P 500 futures; per search summary). — [Umeå Economic Studies listing](https://econpapers.repec.org/RePEc:hhs:umnees:0948)
- **Expiry concentration:** in FY26, 59% of index-options turnover took place on expiry day and about 75% within one day of expiry. — [Open Magazine](https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26)
- **Expiry calendar:** NIFTY weekly options expire on Tuesday (since 1 Sept 2025); BANKNIFTY is monthly-only. — [Angel One](https://www.angelone.in/news/market-updates/nifty-weekly-expiry-today-see-what-changed-on-sept-1-2025)
- **Expiry-day manipulation allegations:** SEBI's interim order on BANKNIFTY expiry days. — [Moneylife explainer](https://moneylife.in/article/explainer-what-are-sebis-findings-on-jane-street-groups-market-manipulation/77594.html)
- [A, US] **Dealer gamma:** end-of-day intraday momentum is much stronger on negative net-gamma days and insignificant on positive-gamma days. — [Alpha Architect](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/); [EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:142:y:2021:i:1:p:377-403)
- [C] **India VIX:**
  - Daily data from Mar 2009 to Nov 2011 show an inverse and asymmetric relationship between India VIX changes and Nifty moves. — [i-scholar (IJF)](https://mail.i-scholar.in/index.php/ijf/article/view/202319)
  - A later paper argues VIX estimates realised volatility better than traditional measures. — [Springer (DECISION)](https://springerlink.bibliotecabuap.elogim.com/content/pdf/10.1007/s40622-014-0070-0.pdf)
  - An emerging-markets comparison ranked GARCH first and India VIX second for forecasting. — [i-scholar (VBRVIM)](https://i-scholar.in/index.php/VBRVIM/article/download/64227/55068)
- [C] **Option OI:** an unreviewed study of Nifty near-month options (Jan 2014-Dec 2020, 1,728 observations) reports that the day's highest-OI strike has some ability to predict the next day's close. — [Scribd working paper](https://www.scribd.com/document/686192532/PCR)
- **PCR:** a frequency-domain causality study (Jena, Tiwari & Mitra, *Economies* 2019) compares PCR by volume and by OI in predicting market returns; its results were not retrieved. Practitioner sites mostly state PCR rules of thumb without testing them. — [MDPI](https://mdpi.com/2227-7099/7/1/24)
- [C] **FII flows:** studies of Indian daily data mostly find bidirectional or return-driven causality, consistent with FIIs feedback-trading on past returns. Any effect of FII trading on returns is very short-lived, and the samples are small and old. — [Emerald (2012)](https://www.emerald.com/insight/content/doi/10.1108/17554191211274794/full/html); [i-scholar (MERI)](https://i-scholar.in/index.php/MERI/article/view/182835)
- [D] **GIFT Nifty:** no rigorous study of its opening-gap accuracy was found. Vendor blogs claim it usually signals the opening direction, without data. Analysis must adjust for the GIFT premium and treat the July 2023 series break separately, and the size of the actual opening gap often differs from the implied gap. — [Belong blog (accuracy)](https://getbelong.com/blog/gift-nifty-as-an-early-indicator/); [Belong blog (historical data)](https://getbelong.com/blog/gift-nifty-historical-data/)

#### Crypto
- [D] **Order flow vs funding/OI:** a CryptoQuant-based 90-day analysis found daily BTC returns correlated 0.76 with net taker flow and 0.64 with the taker ratio, while open interest and funding showed almost no link to daily returns. It is a single window with no out-of-sample test. — [MEXC News](https://www.mexc.com/news/83641)
- [D] **October 2025 deleveraging:** open interest peaked at $54.7B before the collapse, and liquidation intensity (daily liquidations divided by OI) peaked at 4.82%. This describes the event; it is not a predictive test. — [Amberdata](https://blog.amberdata.io/leverage-liquidations-the-31b-deleveraging)
- [D] **OI/funding regimes:** a 2×2 classification of 2,522 days (Mar 2019-Feb 2026) found 43.3% of days had OI rising with positive funding and 9.0% had OI falling with negative funding ("capitulation"). It reports day counts, not forward returns. — [Axel Adler Jr.](https://axeladlerjr.com/bitcoin-open-interest-funding-rate/)
- [B/C] **Intraday structure:** Bitcoin mean-reverts at 1-4-hour horizons (attributed partly to cascading liquidations), shows first-half-hour to last-half-hour momentum, and has a 15-minute "turn-of-the-candle" return concentration. — [LMU repository](https://epub.ub.uni-muenchen.de/97651/); [Reading repository](https://centaur.reading.ac.uk/100181); [Northumbria](https://researchportal.northumbria.ac.uk/en/publications/turn-of-the-candle-effect-in-bitcoin-returns/)

#### FX
- [A] **Announcement effects** (Andersen, Bollerslev, Diebold & Vega, AER 2003, 93(1):38-62), six years of real-time quotes for the dollar against the mark, pound, yen, Swiss franc and euro:
  - Announcement surprises produce near-immediate jumps in exchange-rate conditional means.
  - Bad news has a larger effect than good news.
  - More timely releases matter most, including payrolls, durable goods and consumer confidence.
  - Volatility adjusts to news more gradually than the mean.

  — [NBER w8959](https://www.nber.org/system/files/working_papers/w8959/w8959.pdf); [EconPapers](https://econpapers.repec.org/RePEc:aea:aecrev:v:93:y:2003:i:1:p:38-62)
- [A/B] **Stop clusters around round numbers** make breaks of round levels prone to acceleration. Order-level data only (Osler). — [NY Fed SR125](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf)

### Inferences
- **Ranked additions, by expected value per unit of effort:**
  1. **Event and regime calendar flags.** Mark NSE expiry days (NIFTY Tuesday weekly; monthly last-Tuesday contracts; BSE Thursday Sensex), RBI policy days, Union Budget day, index heavyweights' results days, and US CPI/NFP/FOMC times for FX, crypto and the next-day NSE open. Use them as features, and as no-trade windows around scheduled releases for FX and crypto. This has the strongest evidence (AER announcement study, Gao et al. news-day effect, SEBI expiry concentration) and is cheap to build.
  2. **Volatility state.** Use the India VIX level and change percentiles plus the instrument's own ATR percentile, gating ORB and breakout setups and scaling stops and size. ORB profitability and intraday momentum are documented to depend on volatility.
  3. **Relative volume / "in play"** for single NSE stocks: first-15-minute volume relative to its 14-20-day average at the same time of day, and results-day flags. This is the condition behind the strongest ORB claims (graded C).
  4. **Futures-based VWAP and volume for indices**, plus the futures basis. This fixes a data problem rather than adding an alpha source.
  5. **Options positioning for NIFTY:** max-OI call and put strikes as candidate levels, and an approximate dealer-gamma sign if you can estimate it. Treat this as experimental: there is strong US mechanism evidence and only weak Indian evidence. Retail data cannot see dealer positions, so any GEX estimate rests on assumptions.
  6. **Crypto:** taker buy/sell imbalance (CVD) and liquidation feeds to confirm sweeps and cascades. Extreme funding and OI changes serve as context only, since their short-horizon predictive evidence is weak.
  7. **FII/DII flows and GIFT Nifty.** FII/DII provisional figures arrive after the cash session, so they are at most next-day bias inputs, and the literature points to feedback trading. GIFT Nifty is useful for estimating the opening gap (adjusted for premium), not for intraday direction. Both rank low. (Exact publication times should be verified.)
  8. **Market breadth** (advance/decline of NIFTY 50 constituents, share of constituents above VWAP). It is plausible as index-trend confirmation but has no evidence retrieved here. Test it as a feature rather than assuming it helps.
- **Test each data source the same way:** add it as a feature to the walk-forward logistic model from Section 3, and keep it only if out-of-sample net expectancy or calibration improves beyond the DSR/PBO-adjusted noise level.
- **Sessions for FX and crypto:** the London/New York overlap and fix windows are commonly cited by practitioners but were not evidenced here. Encode session as a time-of-day feature and let the event study decide.

### Gaps
- No rigorous, recent out-of-sample study was found showing that PCR, OI walls, India VIX, FII/DII flows or GIFT Nifty improve *intraday* NIFTY/BANKNIFTY direction forecasts. The Indian studies found are older, daily-frequency and partly unreviewed.
- No Indian dealer-gamma (GEX) study was found, despite India's options volumes. This is a natural research test for the bot.
- Market breadth, RBI policy-day effects and results-day effects on intraday level reactions were not researched here.
- Academic work on perpetual-futures funding-rate predictability (e.g. studies of perpetual futures fundamentals) was not retrieved. The crypto funding, OI and liquidation evidence above is blog-grade.
- FX session-timing studies (intraday volatility seasonality) were not retrieved. The release timetable for NSE FII/DII provisional data and GIFT Nifty session hours were not verified.

## 5. Which risk-management pieces matter as much as signal quality (position sizing, daily loss limits, maximum trades), and what is the evidence?

### Takeaway
The evidence is indirect but consistent:
- Losses and costs scale with trading frequency and intensity relative to capital.
- Traders who lose in the morning take more risk in the afternoon.
- Stop-losses only add value when returns trend (momentum) and subtract value under random-walk behaviour.
- Volatility-scaled exposure reduces tail risk and improves Sharpe for equity-type assets.

For this bot that means fixed-fractional risk per trade sized by stop distance, volatility scaling, a hard daily loss limit and trade cap, cost-aware trade filtering, and pre-registered kill-switches. These are cheap insurance even if the signal edge turns out smaller than hoped.

### Cited Findings
- [B] Coval & Shumway (Journal of Finance 2005, 60(1):1-34): CBOT proprietary traders with morning losses were about 15-16% more likely to take above-average afternoon risk than traders with morning gains. Losing traders bought at higher prices and sold at lower ones than before, with prices later reverting. — [IDEAS](https://ideas.repec.org/a/bla/jfinan/v60y2005i1p1-34.html)
- [B] Kaminski & Lo ("When Do Stop-Loss Rules Stop Losses?", Journal of Financial Markets 2014, 18:234-254): under a random walk, simple stop-loss rules reduce expected returns. With momentum, they can add value. Using monthly data from 1950 to 2004, certain stop-loss rules added 50-100 bp/month during stop-out periods. — [EconPapers](https://econpapers.repec.org/RePEc:eee:finmar:v:18:y:2014:i:c:p:234-254); [MIT DSpace](https://dspace.mit.edu/entities/publication/bb69ca4b-0cdc-487f-831d-63b2e84fafee)
- [B] Harvey et al., "The Impact of Volatility Targeting" (JPM 2018), 60+ assets:
  - Volatility targeting improves Sharpe ratios for risk assets (equities, credit) via the leverage effect. The effect is negligible for bonds, FX and commodities.
  - Across assets it consistently reduces the likelihood of extreme returns and the volatility of volatility.
  - A secondary example: US equity Sharpe rose from 0.40 to 0.48-0.51.

  — [Quantpedia](https://quantpedia.com/the-impact-of-volatility-targeting-on-equities-bonds-commodities-and-currencies)
- **Trading frequency and costs (SEBI):** among intraday traders making more than 500 trades a year, 80% were loss-makers, and loss-makers' costs equalled 57% of their losses (FY23). — [SEBI press release](https://www.sebi.gov.in/media-and-notifications/press-releases/jul-2024/sebi-study-finds-that-7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses_84948.html)
- **Trading intensity (SEBI FY26):** higher trading intensity relative to capital or portfolio size was associated with higher loss rates. — [Open Magazine](https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26)
- [C] **Low hit rates and losing streaks:** in the ORB replication, about a 20% hit rate combined with the paper's 4× leverage implies long losing streaks that a daily loss limit would not survive. The author reads the paper's 33% annual return as the same gross edge multiplied by leverage assumptions a retail account does not get. — [MQL5 blog](https://www.mql5.com/en/blogs/post/776235)
- [B] Few day traders are persistently profitable: those with prior profits are 1.6% of day traders. — [Barber et al. companion paper](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/day%20trading%20and%20learning%20110217.pdf)
- **Collateral rule cost:** Zerodha charges ₹40 instead of ₹20 per order on intraday F&O trades it must fund because the 50% cash-collateral rule is not met (from 1 Apr 2026). — [Business Today](https://www.businesstoday.in/markets/stocks/story/zerodha-doubling-fees-for-select-intraday-trades-who-will-be-impacted-522295-2026-03-25)

### Inferences

#### Risk rules suggested by the evidence (personal-use scale)
- **Position size from the stop, not from conviction.** Size = (fixed fraction of equity, e.g. 0.25-0.5% risk per trade) ÷ (stop distance + expected slippage), with a hard cap on leverage and notional. Optionally scale the risk fraction down when ATR or India VIX percentiles are high, in line with volatility-targeting evidence that tail risk falls. Any "confidence-based" sizing should use the calibrated probability from Section 3 with fractional, conservative multipliers, and only after calibration is shown to hold out-of-sample.
- **Daily loss limit and stop-after-losses rule** (for example, stop for the day at −2R or after 3 consecutive losses). The rationale is behavioural: morning losers take more afternoon risk (Coval & Shumway). For an automated bot this guards against regime days (event shocks, expiry squeezes) where the model is miscalibrated. The specific thresholds are judgement, not evidence.
- **Maximum trades per day and a minimum stop-to-cost ratio.** Frequency raises cost drag (SEBI: 80% loss-makers above 500 trades a year; costs 57% of losses). With c of about 0.1-0.2R per round trip on tight NSE futures stops, each extra marginal trade needs a high hit rate (Section 2). Cap trades per instrument per day, and reject setups whose stop is under about 2-3× round-trip cost.
- **Expect long losing streaks and size so they are survivable.** By the standard longest-run approximation, the expected longest losing streak over 250 trades is about 9-10 at a 40% hit rate and about 17-20 at a 20% hit rate. At 0.5% risk per trade, a 20-loss streak is about a 10% drawdown; at 2% risk it is about 33%.
- **Stops behind structure, but test them.** Kaminski & Lo imply stop-losses help only where returns trend at the trade's horizon. The bot's structure stops (bounded by ATR multiples) should be compared in the event study with time-based exits and wider ATR stops. The best stop rule may differ between breakout setups (momentum, where stops help) and mean-reversion setups such as sweep reversals.
- **Regime kill-switches:** no new trades in the final minutes before the 3:15 pm CAS cut-off for F&O stocks unless tested. Treat the new 3:15-3:40 pm window as a separate regime. Use reduced size or no trades on expiry days and around scheduled releases until the event study shows those regimes are profitable.
- **Operational risk:** keep the 50% cash-collateral ratio to avoid ₹40-per-order charges. Reconcile broker fills against the journal daily. Never let the bot place orders from unconfirmed (repainting) signals.

#### Consolidated prioritised action list (synthesis of all five sections)
1. **Make the engine leakage-proof and time-exact.** Add `confirmed_at` for swings, pools and equal highs/lows; closed-bar-only signals; point-in-time daily and weekly levels; one explicit "close" definition per market; and a session calendar that encodes NSE CAS (3:15/3:35), the 3:40 pm derivatives close, Tuesday expiries and holidays. Add the truncation-invariance unit test. *Why first:* every later number is meaningless if features peek into the future (Section 2).
2. **Build the triple-barrier event harness with full costs.** Use the current Zerodha/NSE charge table, measured slippage, Binance fees and funding, and FX spreads. Resolve same-bar ambiguity conservatively and fill at the next bar's open.
3. **Define null baselines and an ablation protocol.** Compare against random-time entries, random or shifted levels, plain PDH/PDL/PDC, generic floor pivots and random direction. "Better than generic tools" then means beating these net of costs, with confidence intervals.
4. **Ablate every component.** Test each level type (PDH/PDL, CPR, pivots, OR, swing zones, pools, round numbers) and each bias vote. Expect to drop or merge correlated ones: pivots and CPR versus PDH/PDL/PDC, and the five collinear bias votes.
5. **Walk-forward plus multiple-testing discipline.** Use a locked holdout (post-3 Aug 2026), log every configuration, report DSR and PBO, and require t of at least 3 for new filters. Segment NSE history at Nov 2024, Sept 2025, Apr 2026 and Aug 2026.
6. **Test the few literature-backed conditional effects on your own markets first.** These are: NIFTY/BANKNIFTY first-half-hour to last-half-hour momentum, with the end-of-day window redefined for CAS and the 3:40 pm close; ORB conditioned on volatility state and relative volume; S/R bounce probability against touch count and age; sweep reversal versus cascade; and BTC turn-of-candle and 1-4-hour mean reversion.
7. **Replace hand-set confluence weights with a calibrated, regularised logistic model** fitted walk-forward. Show calibrated probabilities with uncertainty on every alert, and publish reliability curves. This is the main measurable "trust" upgrade.
8. **Run shadow-mode forward tests with an immutable journal** (at least about 3 months or 300+ alerts per asset class). Compare live with backtest distributions, and keep pre-registered kill-switches.
9. **Add context data in evidence order:** event and expiry calendar flags, then volatility state (India VIX/ATR percentiles), then relative volume, then futures-based index VWAP, then experimental options-positioning features. For crypto, add order-flow and liquidation data; for FX, news blackout windows.
10. **Add ML only as a meta-labeling filter or sizer**, after there are thousands of labelled events, using purged and embargoed CV. Keep it only if out-of-sample net expectancy and calibration beat the logistic baseline after DSR/PBO checks.
11. **Hard-code the risk layer:** fixed-fractional sizing from the stop distance, volatility scaling, a daily loss limit, a consecutive-loss pause, a trades-per-day cap, a minimum stop-to-cost ratio, and expiry and event regime limits.
12. **Communicate evidence grades in the bot's output.** Label SMC/ICT-derived and CPR-derived signals as "unvalidated hypotheses" until the bot's own out-of-sample statistics support them. Never present backtest-only numbers as expected live performance.

### Gaps
- No direct evidence was found on the effectiveness of daily loss limits or maximum-trade caps for retail or automated intraday traders. The support is behavioural (Coval & Shumway) and regulator descriptive data (SEBI), not controlled tests.
- Kelly or fractional-Kelly sizing evidence, and drawdown-control studies specific to intraday strategies, were not researched here.
- Kaminski & Lo's empirical work uses monthly data. No study of stop-loss value at intraday horizons for NSE instruments was found.
- Prop-firm risk rules (daily drawdown limits) are widely used but were found only in vendor material, so they are not cited.
