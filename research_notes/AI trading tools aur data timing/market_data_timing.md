# Market-data timing and accuracy for a personal trading-analysis bot: Indian stocks/indices, crypto, forex and gold (as of 5 November 2026)

*Research date: 2026-11-05. Web sources were accessed on 2026-11-05. "Own test" means a public, read-only API call made from this machine on 2026-11-05 at about 03:05 UTC (08:35 IST). Items marked **UNVERIFIED** come only from secondary or weak sources, or from search snippets of pages that could not be fetched.*

---

## 1. Yahoo Finance and yfinance: official delays, FX and COMEX sources, what yfinance is, rate limits, terms and data-quality problems

### Takeaway
Yahoo's own provider table lists NSE (`.NS`) as **real-time** and BSE (`.BO`) as **15 minutes delayed**. Both come from ICE Data Services. FX (`=X`) is listed as **real-time** (ICE), and COMEX futures, which include gold `GC=F`, are **30 minutes delayed**. NSE indices such as `^NSEI` are not listed at all. yfinance is an unofficial scraper of Yahoo endpoints, licensed for personal use only. It hits rate-limit blocks often and changes often (10 releases between April and November 2026). Its maintainers say that only US data "appears perfect". Treat Yahoo-derived NSE levels as near-real-time with no guarantee and possible gaps, FX as real-time indicative quotes, and gold as a 30-minute-delayed futures price that is not spot.

### Cited Findings
- Yahoo's "Exchanges and data providers" table rows say: "India | National Stock Exchange of India | .NS | Real-time | ICE Data Services" and "India | Bombay Stock Exchange | .BO | 15 min | ICE Data Services" — [Yahoo Help SLN2310](https://help.yahoo.com/kb/SLN2310.html)
- Same page: "Global | Currency Rates | =X | Real-time | ICE Data Services" — [Yahoo Help SLN2310](https://help.yahoo.com/kb/SLN2310.html)
- Same page, futures delays: CBOT (.CBT) 10 min, CME (.CME) 10 min, **COMEX (.CMX) 30 min**, NYMEX (.NYM) 30 min, all from ICE Data Services. A footnote says the market data "are the property of Chicago Mercantile Exchange Inc." — [Yahoo Help SLN2310](https://help.yahoo.com/kb/SLN2310.html)
- The page does not list Nifty 50 or any NSE index. It lists FTSE (15 min), Nikkei (30 min), Hang Seng (15 min), and MSCI/Dow Jones/S&P/Nasdaq (real-time). — [Yahoo Help SLN2310](https://help.yahoo.com/kb/SLN2310.html)
- Yahoo says "All data provided on Yahoo Finance is provided for informational purposes only" and is not intended for trading. It also says "You must not redistribute information displayed on or provided by Yahoo Finance." The page has no update date (only a 2025 copyright line). — [Yahoo Help SLN2310](https://help.yahoo.com/kb/SLN2310.html)
- yfinance says it is "not affiliated, endorsed, or vetted by Yahoo, Inc.", that it is an open-source tool using Yahoo's publicly available APIs, that it is meant for research/educational use, and that "the Yahoo! finance API is intended for personal use only." Users are pointed to Yahoo's terms of use for their rights to the data. — [yfinance GitHub README](https://github.com/ranaroussi/yfinance); [PyPI yfinance](https://pypi.org/project/yfinance/)
- yfinance README: "Prices are default adjusted for dividends (`auto_adjust=True`)." — [yfinance GitHub README](https://github.com/ranaroussi/yfinance)
- Latest version is **yfinance 1.8.0 (3 Nov 2026)**. Earlier releases: 1.7.0 (26 Aug 2026), 1.6.0 (13 Aug), 1.5.2 (23 Jul), 1.5.1 (28 Jun), 1.4.1 (28 May), 1.4.0 (23 May), 1.3.0 (16 Apr), 1.2.2 (13 Apr), 1.2.1 (7 Apr 2026). — [PyPI yfinance](https://pypi.org/project/yfinance/)
- The bot's `requirements.txt` pins only `yfinance>=0.2.54`, a 0.2.x-era floor. — local file `/Users/admin/ABD Trading Bot Crypto:forex:stocks/requirements.txt`
- Rate limiting: `YFRateLimitError` is raised when Yahoo's cookie/crumb request returns HTTP 429 or "Too Many Requests". The library defaults to a `curl_cffi` session that impersonates Chrome and rejects `requests_cache` sessions. — [third-party copy of yfinance `data.py`](https://generationalwealth.duckdns.org/venv/lib/python3.13/site-packages/yfinance/data.py) (mirror of library source, secondary)
- User reports: the rate-limit error appeared on 2025-04-29 and changing IP did not help ([issue #2422](https://github.com/ranaroussi/yfinance/issues/2422)). A 429 on `.info` persisted across 0.2.57–0.2.59 ([issue #2480](https://github.com/ranaroussi/yfinance/issues/2480)). A maintainer-style reply says blocks are usually temporary IP blocks after too many requests in a short time, and one user found that about 100 requests followed by a 30-second pause worked ([discussion #2431](https://github.com/ranaroussi/yfinance/discussions/2431)).
- **Own test (2026-11-05 03:05 UTC):** plain `curl` GETs to `https://query1.finance.yahoo.com/v8/finance/chart/<symbol>` for RELIANCE.NS, ^NSEI, EURUSD=X, GC=F and USDINR=X all returned **HTTP 429** with a 19-byte body. Yahoo rejects ordinary HTTP clients. yfinance works only because it impersonates a browser. I did not try to get around this. — [Yahoo chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/RELIANCE.NS)
- Intraday history limits: 1m data is limited to 7 days per request within the last 30 days. Intervals up to 90m (including 5m and 15m) are limited to 60 days. 60m/1h is limited to 730 days. — [yfinance wiki (mirror)](https://github-redirect.dependabot.com/ranaroussi/yfinance/wiki/Ticker); an error message confirming the 730-day limit appears in [issue #2451](https://github.com/ranaroussi/yfinance/issues/2451)
- yfinance's price-repair docs list known Yahoo defects: missing dividend adjustment, missing split adjustment, unexplained split-like adjustments, missing/corrupt rows or missing volume, 100x currency-unit errors, and several dividend errors (duplicates, wrong ex-date, wrong size). `repair=True` adds a `Repaired?` column. The author writes: "Only US market data appears perfect." Repair uses 1h data, which "cannot be fetched beyond 2 years". Dividend repair works only on 1d data. — [yfinance price repair docs](https://ranaroussi.github.io/yfinance/advanced/price_repair.html)
- Missing-data reports: Yahoo itself had missing data for all tickers in June 2024 ([issue #1962](https://github.com/ranaroussi/yfinance/issues/1962)). The last day of a requested range can be missing from output even though Yahoo has it ([issue #1906](https://www.github.com/ranaroussi/yfinance/issues/1906)). Yahoo can return nothing for specific timestamps, which wrappers fill with NaN ([YFinance.jl docs](https://github.com/eohne/YFinance.jl/blob/master/docs/src/Prices.md)). Open issues are titled "Inaccurate price data, NSE" (#2055) and "Incorrect market data for NSE segment" (#2022) (titles only seen) — [ecosyste.ms issue index](https://issues.ecosyste.ms/hosts/GitHub/repositories/ranaroussi%2Fyfinance/issues)
- Anecdotal: Yahoo's Indian closes have differed from broker/NSE closes. One answer suggests Yahoo may use BSE closes, and a 2014 CASTROLIND example showed 157.15 on Yahoo vs 156.39 elsewhere. The advice was to check NSE's site for official closes. — [TradingQnA: Google Finance vs Zerodha closes](https://tradingqna.com/t/why-is-there-a-difference-in-closing-prices-on-sites-like-google-finance-and-zerodha/9218); [TradingQnA: CASTROLIND](https://tradingqna.com/t/castrolind-chart-query/43902) (forum, old, weak)

### Inferences
- "Real-time" in Yahoo's table describes the quote feed. It is not a service guarantee for the 5m/15m bars that yfinance downloads. Those bars are built by Yahoo and can have gaps, as the issues above show. There is no SLA and no permitted commercial use.
- **Blank close on the newest NSE daily row.** Several causes fit what you saw. (a) During the session the current daily bar is still forming. (b) Since 3 Aug 2026, the official close of F&O stocks such as RELIANCE is set only by the closing auction (matching 15:30–15:35 IST until 6 Dec 2026, see Section 2). A fetch near or after 15:30 may see a placeholder, an LTP, or a value that is overwritten later. (c) Yahoo-side gaps. The bot should treat the newest daily row as provisional, drop NaN rows, and take the previous day's H/L/C from an official source (NSE bhavcopy or a broker's day candle) after the close.
- **Missing 5-minute bars.** Since 3 Aug 2026, F&O stocks have **no continuous trading from 15:15 to 15:30 IST** (call auction instead). The 15:15, 15:20 and 15:25 bars can therefore be empty or flat, followed by one auction print. RELIANCE is an F&O stock. This may explain some of the end-of-day gaps you saw. Gaps at other times point to Yahoo feed problems.
- With `auto_adjust=True` (the default), every OHLC value before an ex-dividend date is scaled down. On the morning after an ex-date, the "previous-day" H/L/C would be dividend-adjusted rather than the traded prices. Splits and bonuses do need adjusting, or levels are off by the split ratio. For pivots/CPR, use unadjusted prices and handle splits/bonuses explicitly (for example `auto_adjust=False` and check corporate actions). I did not verify how Yahoo's `Close` treats splits when `auto_adjust=False`.
- GC=F is a COMEX contract, so per Yahoo's table it is 30 minutes delayed. A "15-minute close confirmation" on GC=F therefore fires about 30 minutes or more after the real candle close, and it is on futures rather than spot (see Section 6).
- With 10 releases in 7 months and Yahoo returning 429s to non-browser clients, the bot should pin a recent yfinance (1.8.0), cache results, throttle, and keep a fallback source.

### Gaps
- Yahoo does not document how it builds NSE intraday bars. It also does not say whether its NSE daily close is the official close (VWAP or auction) or the last trade, or how it handles CAS auction prints. I could not test live because Yahoo returned HTTP 429, and getting around bot detection is out of scope.
- Delay and source for `^NSEI`, `^NSEBANK` and `^INDIAVIX` on Yahoo are not documented on the providers page.
- Yahoo's FX daily-candle boundary (London midnight, UTC midnight or New York 17:00) is not documented. No authoritative source was found.
- I found no official Yahoo statement of numeric rate limits. The limits are undocumented and enforced by IP blocks.

---

## 2. NSE data: who may redistribute real-time data, what brokers provide, session timings (2025–2026 changes) and how the official close is computed

### Takeaway
Real-time NSE data is licensed by NSE (through NSE Data & Analytics) to authorised vendors and trading members. A personal bot can get it legitimately through its own broker's API or from a licensed vendor. Most retail feeds are about 1-second snapshots, not every trade. Market structure changed a lot in 2025–2026:
- F&O futures pre-open started 8 Dec 2025.
- A **Closing Auction Session (CAS)** for F&O stocks started **3 Aug 2026**. Continuous trading in those stocks ends at **15:15**, and the official close is the **auction equilibrium price**.
- The equity pre-open was revised from 7 Sep 2026.
- CAS moves to **15:30–15:40 from 7 Dec 2026**.

Non-F&O stocks still close on the **VWAP of 15:00–15:30**. Neither the auction price nor the VWAP is the chart's last traded price. Previous-day close, CPR and pivots must use the official close.

### Cited Findings
**Licensing and feed types**
- NSE Data & Analytics offers real-time data at several levels. It publishes specs for a CM & CD multicast tick-by-tick feed delivered over a leased line, keeps a list of authorised real-time vendors, and offers a stock-wise CSV feed at set intervals. The listed tariff is ₹10,000/year for a single stock, with tariff PDFs dated 1 Apr 2025. **UNVERIFIED** detail: these points come from a search snippet because the NSE page timed out. — [NSE real-time data subscription](https://www.nseindia.com/static/market-data/real-time-data-subscription); [NSE Data & Analytics](https://nseindia.com/nsedataandanalytics)
- NSE still maintains its multicast tick-by-tick (MTBT) product. A 7 Oct 2025 circular added order-snapshot recovery over TCP/IP for the CM-segment MTBT broadcast. — [mirror of NSE circular 2025-10-07](https://rhnvrm.github.io/stock-market-circulars/circulars/nse/2025/nse-2025-10-07-4d5c0b5b03bd0047-market-data-introduction-of-order-snapshot-recovery-via-tcpip-for-mtbt-broadcast)
- A vendor blog says "almost all the data vendors (both domestic and international) get the same legacy netted consolidated 1-second snapshot data feed" — [Marketcalls](https://www.marketcalls.in/softwares/data-vendors-and-quality-of-datafeeds.html) (vendor/blogger, not NSE)
- Zerodha staff say Kite's WebSocket is a snapshot stream with about 1–2 ticks per second for liquid instruments, and no tick at all when a scrip has no trades in an interval (details in Section 3). — [Kite forum](https://kite.trade/forum/discussion/3574/is-the-websocket-data-sampled-by-1-sec)

**Session timings**
- F&O pre-open: NSE launched a call-auction pre-open for **current-month stock and index futures** on **8 Dec 2025**, running 09:00–09:15. Options, far-month and spread contracts are excluded. One source gives the order-entry window as 09:00–09:08 and another says it closes between 09:07 and 09:08. The basis is NSE circular NSE/FAOP/71092 dated 3 Nov 2025, following a SEBI circular of 29 May 2025. — [Business Standard](https://www.business-standard.com/markets/capital-market-news/nse-to-commence-pre-opening-session-in-f-o-segment-from-december-08-125110400728_1.html); [Tradejini](https://www.tradejini.com/blogs/nse-to-launch-preopen-session-for-futures-contracts-from-december-8-2025); [Angel One](https://www.angelone.in/news/market-updates/nse-to-start-pre-open-trade-in-equity-derivatives-from-december-8-2025)
- Revised equity pre-open, effective **7 Sep 2026**: 09:00–09:05 limit and market orders; 09:05–09:10 limit orders only, with random closure between 09:08 and 09:10; 09:10–09:12 matching and opening-price discovery; 09:12–09:15 transition to normal trading. — [TradingQnA (Zerodha community), 20 Jan 2026 post](https://tradingqna.com/t/sebi-introduces-closing-auction-session-cas-for-f-o-stocks-and-revises-pre-open-session/190558); the 7 Sep 2026 date is also in [Outlook Money](https://www.outlookmoney.com/invest/nse-extended-fo-timings-and-new-closing-auction-session-rules-explained)
- CAS legal basis: SEBI circular **HO/47/11/11(3)2025-MRD-POD2/I/2765/2026 dated 16 Jan 2026**, "Introduction of Closing Auction Session (CAS) in the Equity Cash Segment and certain modifications in the Pre-Open Auction Session" — [SEBI](https://www.sebi.gov.in/legal/circulars/jan-2026/introduction-of-closing-auction-session-cas-in-the-equity-cash-segment-and-certain-modifications-in-the-pre-open-auction-session_99122.html). NSE's operational SOP is circular CMTR73362 ([NSE PDF](https://nsearchives.nseindia.com/content/circulars/CMTR73362.pdf), referenced, but the fetch timed out).
- **CAS as run from 3 Aug 2026 to 6 Dec 2026** (phase 1 covers stocks with F&O contracts, about 200–300 names):
  - 15:00–15:15: VWAP window used for the reference price.
  - 15:15–15:20: reference price is set; no orders.
  - 15:20–15:25: limit and market orders.
  - 15:25–15:30: limit orders only; market orders cannot be modified; random closure 15:28–15:30.
  - 15:30–15:35: matching.
  - The close is the price that maximises matched volume, with tie-breaks on minimum unmatched quantity and then nearness to the reference price. If no equilibrium exists, the **reference price** is used. The reference price falls back to the day's LTP, then to the previous close.
  - "Regular cash market trading ends at 3:15 PM for F&O stocks"; F&O trades until **15:40**; the post-close session runs 15:50–16:00 at the closing price.
  - Sources: [TradingQnA](https://tradingqna.com/t/sebi-introduces-closing-auction-session-cas-for-f-o-stocks-and-revises-pre-open-session/190558); [Outlook Money](https://www.outlookmoney.com/invest/nse-extended-fo-timings-and-new-closing-auction-session-rules-explained); [Zerodha support](https://support.zerodha.com/category/trading-and-markets/trading-faqs/articles/ltp-doesnt-match-close)
- CAS details from Outlook Money: stop-loss, iceberg and IOC orders are blocked; unexecuted day limit orders within the band carry into the auction. Prices are held within a static **3% band** around an afternoon reference. If an index circuit breaker halts the market before the auction, the **close defaults to the 30-minute VWAP**. — [Outlook Money](https://www.outlookmoney.com/invest/nse-extended-fo-timings-and-new-closing-auction-session-rules-explained). **Conflict:** tick2trade says automatic carry-over of unexecuted orders into CAS takes effect only from **8 Feb 2027** — [tick2trade](https://www.tick2trade.com/blogs/sebi-revises-nse-closing-auction-session-rules)
- Non-F&O stocks: continuous trading runs until 15:30, and "the exchange calculates the closing price as a weighted average of the last 30 minutes of trading (3:00 PM to 3:30 PM)". For F&O stocks, "the closing price is determined during the Closing Auction Session (CAS)." — [Zerodha support](https://support.zerodha.com/category/trading-and-markets/trading-faqs/articles/ltp-doesnt-match-close)
- **Revision effective 7 Dec 2026**, by SEBI circular dated **15 Oct 2026** (No. HO/47/11/11(3)2025-MRD-POD2/I/23843/2026, "Review of certain aspects of the Closing Auction Session, market timings and settlement methodology for derivatives contracts"):
  - Continuous trading in CAS stocks runs to 15:30.
  - CAS runs 15:30–15:40: transition 15:30–15:31, market and limit orders 15:31–15:36, limit only 15:36–15:40, random closure 15:38–15:40.
  - Derivatives trade to **15:45**, except expiring index contracts, which stop at 15:30 on expiry day.
  - Stock and index derivatives expiry settlement goes back to the **30-minute VWAP of 15:00–15:30**.
  - Carry-over of unexecuted orders into CAS starts 8 Feb 2027.
  - Sources: [tick2trade](https://www.tick2trade.com/blogs/sebi-revises-nse-closing-auction-session-rules); [Outlook Business](https://www.outlookbusiness.com/markets/sebi-revises-closing-auction-session-rules-retains-30-minute-vwap-settlement-method); [Angel One](https://www.angelone.in/news/market-updates/sebi-revises-equity-market-closing-auction-rules-retains-30-minute-vwap-for-expiry); [Multibagg](https://www.multibagg.ai/market-pulse/articles/sebi-closing-auction-330-340-cmvkv5ufp00062ls0ytxwxery). All are secondary; the SEBI text itself was not fetched.
- Index close under CAS: the index close is computed after matching from constituents' official closing prices. Between 15:15 and the auction the index "can stay constant as trades are not continuously executed", and "3:15 pm is no longer the final fix." Over the first four sessions the average gap between the 15:15 level and the post-CAS close was about **0.42%**. Examples: 24,628 → 24,636 (8 points), 24,570 → 24,625 (55 points), and reported gaps of 184 points (3 Aug) and 155 points (4 Aug). — [Multibagg, 14 Aug 2026](https://www.multibagg.ai/market-pulse/articles/nifty-closing-price-cas-gap-cmsta63gb59h90zo5snn46x5n) (secondary, early-session data)
- Pre-CAS method and charts: NSE's close was "the Volume Weighted Average Price (VWAP) of all trades executed during the last 30 minutes", and "the close on the daily candle is updated using the close from NSE bhavcopy" (Zerodha). — [5paisa](https://forum.5paisa.com/portal/en/kb/articles/why-is-there-a-difference-between-the-ltp-and-closing-price-on-nse); [Upstox](https://upstox.com/learning-center/demat-account/difference-between-ltp-and-closing-price/article-1565/); [Zerodha support (search snippet)](https://support.zerodha.com/category/trading-and-markets/trading-faqs/general/articles/ltp-doesnt-match-close)

### Inferences
- **Effect on the bot's levels.** With prior-day H, L, C:
  - Pivot P = (H+L+C)/3, so a close error ΔC moves **P by ΔC/3**.
  - CPR bottom BC = (H+L)/2 does not move.
  - CPR top TC = 2P−BC moves by **2ΔC/3**.
  - R1 = 2P−L and S1 = 2P−H move by 2ΔC/3; R2/S2 move by ΔC/3.
  - Example from the early-CAS average: a 0.42% gap at NIFTY ≈ 24,600 is about 103 points. If the bot uses the 15:15 value or a chart's last bar instead of the official close, P is off by about 34 points and TC by about 69 points. That is large next to a typical CPR width.
- The auction trade can fall outside the 09:15–15:15 continuous range (it is bounded by a 3% band), so the official day **high/low** can also differ from what 5m bars show. This is not verified; check against the bhavcopy.
- Prior-day OHLC should come from the official close: NSE bhavcopy, or the broker's day candle and previous-close field. It should not come from the last 5m/15m bar, and it should not be computed before the auction close is published (about 15:35 until 6 Dec 2026; about 15:40 or later from 7 Dec 2026).
- Session times should be configuration, not hard-coded. 15:15 versus 15:30 as the end of continuous trading in F&O stocks changes again on 7 Dec 2026. F&O hours also change (15:40 now, 15:45 from 7 Dec, 15:30 for an expiring index contract).
- Opening range 09:15–09:30: the 09:15 open of pre-open stocks is the pre-open equilibrium price (matched 09:10–09:12 since 7 Sep 2026). The pre-open itself produces no 09:00–09:15 continuous bars.

### Gaps
- The official NSE CAS SOP (CMTR73362) and the SEBI 15 Oct 2026 circular text were not read directly. The NSE PDF timed out and SEBI's page body did not render, so all timings above are from consistent secondary sources.
- I could not confirm whether the 7 Sep 2026 pre-open revision also applies to the F&O futures pre-open (09:00–09:08 at launch).
- No NSE India redistribution fee schedule or delayed-data display policy was found. Search returned other exchanges called "NSE" (Nigeria, Kenya).
- Exact publication time of the official close and of the daily bhavcopy was not found.
- How Yahoo and other vendors represent the CAS print (one bar at 15:30? a separate auction bar?) is undocumented.

---

## 3. Indian broker APIs: WebSocket ticks, depth, historical candles, 2026 pricing and SEBI static-IP/algo rules

### Takeaway
Every major Indian broker streams real-time NSE data to its own clients over WebSocket, cheaply or for free:
- **Zerodha Kite Connect:** ₹500/month per API key, with data and history included.
- **Dhan Data API:** ₹499 + tax per month.
- **Upstox:** real-time feed stated free.
- **Fyers Standard:** free, but small limits.
- **ICICI Breeze:** free, including 1-second historical candles.

Standard depth is 5 levels, with 20/30/200 levels on premium tiers. Zerodha calls its feed snapshot-based (about 1–2 ticks/s). Dhan describes its feed as event-based tick-by-tick. Since **1 April 2026**, SEBI's retail-algo framework requires OAuth/2FA, a whitelisted static IP and an algo ID (generic below 10 orders/second) for **API order placement**. No fetched source says that market-data-only use needs a static IP.

### Cited Findings
**Zerodha Kite Connect**
- Paid Connect costs **₹500 per month per API key** and includes "live market data and historical data at no additional cost." The free Personal API covers orders, positions, holdings and funds, with no live or historical data. From **October 2026**, users generating at least ₹2,000 brokerage in a calendar month get 500 Developer Credits (₹500) that cover the next month's renewal. The page does not say whether GST is included. — [Zerodha support](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/historical-data-and-live-market-data-payment-plan)
- Zerodha stopped charging the ₹2,000 historical-data add-on from 8 Feb 2025. — [Kite forum](https://kite.trade/forum/discussion/14806/historical-data-is-now-free)
- WebSocket: `wss://ws.kite.trade`, up to **3,000 instruments per connection** and **3 connections per API key**. Modes are `ltp` (8-byte packet), `quote` (44 bytes) and `full` (184 bytes, with **5 bid + 5 ask** depth levels). The quote packet carries LTP, last qty, **average traded price**, day volume, OHLC, a Close field, last-trade time, OI and exchange timestamp. **Index packets have no volume, quantity or OI fields.** A 1-byte heartbeat is sent every couple of seconds when idle. Currency prices are divided by 10,000,000. — [Kite Connect WebSocket docs](https://kite.trade/docs/connect/v3/websocket/)
- Tick frequency: staff say the exchange streams "only one or two ticks a second" to internet clients. A scrip with no trades in an interval gets no tick. Kite charts and the WebSocket can show slightly different OHLC. Blocked client threads lose ticks for good. One user saw candle opens and closes arrive a couple of seconds late. — [Kite forum: sampled by 1 sec?](https://kite.trade/forum/discussion/3574/is-the-websocket-data-sampled-by-1-sec); [Kite forum: missing ticks](https://kite.trade/forum/discussion/comment/47013/); [Kite forum: ~500 tokens LTP](https://kite.trade/forum/discussion/comment/52020)
- Historical API: intervals minute, 3, 5, 10, 15, 30, 60 minute and day. `continuous=1` returns day candles only, for NFO/MCX futures. `oi=1` adds open interest. Expired contracts' tokens cannot otherwise be retrieved. — [Kite historical docs](https://kite.trade/docs/connect/v3/historical/)
- Rate limits: Quote 1 req/s; **Historical 3 req/s**; orders 10 req/s, 400/min and 5,000/day; HTTP 429 when exceeded. — [Kite exceptions/rate limits](https://kite.trade/docs/connect/v3/exceptions/)

**Upstox**
- Market Data Feed V3 modes: `ltpc` (LTP + close price), `option_greeks`, `full` (5-level depth + metadata + Greeks) and `full_d30` (30 levels, **Plus only**).
- Instrument limits (individual/combined): LTPC 5,000/2,000; Greeks 3,000/2,000; Full 2,000/1,500; Full D30 50/1,500.
- Connections: 2 (normal) or 5 (Plus). The feed is Protobuf, and no update frequency is stated.
- A `market_info` message includes `casMarketStatus` during the closing auction and `preOpenSessionStatus` during pre-open. Full mode carries CAS fields (iep, rp, ieq…). India VIX is available as `NSE_INDEX|India VIX`.
- Source: [Upstox V3 feed docs](https://upstox.com/developer/api-documentation/v3/get-market-data-feed/)
- Upstox staff: "Realtime market data over our web-sockets is completely free" ([Upstox community](https://community.upstox.com/t/i-just-wanted-to-clarify-websocket-is-free-of-cost-or-do-i-need-to-pay-for-it-for-real-time-data-if-any-charges-for-this-then-where-i-can-get-that-information-please-respond/8213)). The Trading API page shows ₹0, "Free access to trading & market data APIs" ([Upstox Trading API](https://upstox.com/trading-api/)). Order placement through the API was ₹10/order, extended to 31 Mar 2026 ([Upstox community](https://community.upstox.com/t/stay-ahead-of-the-curve-we-re-extending-10-order-api-pricing-till-march-2026/13277)).

**Dhan (DhanHQ)**
- Live feed at `wss://api-feed.dhan.co` with Ticker (LTP + last-trade time), Quote (adds ATP, volume, OHLC, buy/sell qty) and Full (adds OI and 5-level depth) modes. Previous close and OI come as separate packets.
- Limits: **5,000 instruments per connection**, 100 per subscribe message, **5 connections per user**.
- The docs say data is pushed as **"tick-by-tick, event-based"** updates. The server pings every 10 s and closes the connection after 40 s without a reply. Last-trade time is an epoch int32, so it has 1-second resolution.
- Source: [DhanHQ live market feed docs](https://dhanhq.co/docs/v2/live-market-feed/)
- The Data API costs **₹499 + applicable taxes per month**; the earlier "free if you trade enough" promotion has ended — [Dhan support](https://dhan.co/support/platforms/dhanhq-api/is-the-dhanhq-data-api-subscription-free-if-i-execute-a-minimum-number-of-trades-every-month/)
- Historical data: **last 5 years** of intraday OHLCV in 1, 5, 15, 25 and 60-minute candles ([Dhan support](https://dhan.co/support/platforms/dhanhq-api/what-timeframe-data-is-available-through-dhan-s-historical-data-apis/)). This covers active contracts only; expired futures are not available intraday ([Dhan support](https://dhan.co/support/platforms/dhanhq-api/how-can-i-retrieve-data-for-expired-futures-contracts-using-the-apis/)). Up to 100,000 Data API requests per day for historical data ([MadeForTrade announcement](https://madefortrade.in/t/enhanced-dhanhq-data-apis-with-more-data-and-higher-rate-limits/50328)).

**Fyers** (page last updated 14 Oct 2026)

| Item | Standard (free) | Prime |
|---|---|---|
| Data API rate limit | 5/s, 50/min, 5,000/day | 10/s, 500/min, 500,000/day |
| Daily history | 5 years | 25+ years |
| Intraday history | 1 year | 5+ years |
| Seconds data | none | last 30 days |
| Data WebSocket | 100 symbols | 5,000 symbols |
| Tick-by-tick socket | 1 symbol | 15 symbols |

Exceeding the per-minute limit more than 3 times in a day blocks the user for the rest of that day. The Prime price is not shown. — [Fyers plans & limits](https://fyers.in/api-docs/v3/getting-started/plans-and-limits/)

**ICICI Breeze**
- "absolutely free of cost", including historical data and live data over WebSockets. History can be fetched at 1-second and 1-minute intervals (`get_historical_data_v2`, `interval="1second"`). The FAQ says 3 years of F&O history, but the PyPI page says "10 years of historical market data including 1 sec OHLCV" — the two conflict. Orders require a registered static IP and are capped at 10 orders/s. — [ICICIdirect FAQ](https://icicidirect.com/faqs/f-and-o/what-is-trading-apis); [PyPI breeze-connect](https://pypi.org/project/breeze-connect/1.0.67/)

**Angel One SmartAPI**
- From 1 Apr 2026, "API order execution will only be accepted if it originates from your registered primary static IP". A secondary IP is allowed, and the IP can be changed at most once per calendar week. The threshold is 10 orders/s per exchange segment; above it, exchange registration is required. **Market and IOC orders are prohibited for algo trading.** The article does not mention market-data APIs. — [Angel One](https://oga-prod.angelone.in/news/market-updates/what-s-changing-in-angel-one-s-smartapi-access-from-april-1-2026)
- Users report a cap of **500 candles per `getCandleData` response**, so 1-minute history must be chunked, plus intermittent "exceeding access rate"/AB1021 throttling. An older answer allows 3 historical requests/s. — [SmartAPI forum: 500 records](https://smartapi.angelone.in/smartapi/forum/post/10902); [SmartAPI forum: access rate](https://smartapi.angelone.in/smartapi/forum/post/980) (user reports)

**SEBI retail-algo framework (all brokers)**
- Milestones:
  - 30 Nov 2025: exchanges register retail algo products.
  - 3 Jan 2026: broker mock session.
  - 5 Jan 2026: brokers that missed the deadlines are barred from onboarding new API clients.
  - **1 Apr 2026**: full enforcement.
  - Source: [Sahi blog](https://www.sahi.com/blogs/sebi-algo-trading-rules-2026-what-every-retail-trader-must-know-before-april) and [Strykex timeline](https://strykex.in/blogs/the-road-to-april-2026-a-timeline-of-sebis-retail-algo-framework). These are secondary blogs; the milestone dates came from a search summary, so which of the two states each date is **UNVERIFIED**. The extension to April 2026 is reported by [Outlook Business](https://www.outlookbusiness.com/amp/story/markets/sebi-extends-deadline-to-implement-retail-algo-trading-by-april-2026)
- Fyers: orders are accepted only from a registered App ID mapped to a whitelisted static IP — [Fyers notice](https://fyers.in/notice-board/new-sebi-framework-for-retail-algo-trading-from-april-01-2026/)
- Upstox: OAuth/2FA is required for all API sessions. A "Mandatory Static IP must be procured and whitelisted" for direct API users at both OPS tiers. At or below 10 OPS, orders get the generic algo ID 99999. The static IP can change once a week. Orders above 10 OPS are rejected unless registered. — [Upstox community guide](https://community.upstox.com/t/a-guide-for-our-api-algo-partners-and-clients/11826)

### Inferences
- For an analysis-only bot that places no orders, the cheapest legitimate way to get exact NSE data is your own broker's API:
  - Upstox, Fyers Standard or Breeze at ₹0.
  - Dhan at ₹499 + GST per month.
  - Kite at ₹500 per month.
  - Use the WebSocket for live LTP, the exchange-computed **average traded price** (day VWAP for stocks) and previous close.
  - Use day candles or historical candles for prior-day H/L/C.
- The broker's ATP field is the exchange's own day VWAP. Computing VWAP from 5m bars (typical price × bar volume) only approximates it.
- "Real-time" broker ticks are snapshots at about 1 s (Kite, by Zerodha's own account) or event-based (Dhan's claim). For 5m/15m candles and a 15-minute close confirmation, 1-second snapshots are enough. Intra-bar highs and lows can be missed by a few ticks (the Kite forum mentions candle-low misses).
- Static-IP rules are documented for **order execution**. If the bot later places orders, it needs a static IP (a VPS or ISP static IP) whitelisted with the broker, OAuth/2FA every day, and to stay under 10 orders/s.

### Gaps
- Angel One SmartAPI: WebSocket 2.0 modes, depth (5/20), token limits and current pricing could not be verified because the docs pages rendered empty. It is widely described as free, but no fetched source confirms this.
- Kite's per-request historical windows (for example the commonly cited 60 days for minute candles) are not on the official docs page. Kite's history start date is not stated.
- Fyers Prime price, Upstox Plus price and Upstox's tick update rate are not stated.
- Not researched: Groww, Kotak Neo, 5paisa, Shoonya/Finvasia, Alice Blue, Motilal Oswal APIs.
- No fetched source says whether market-data-only API calls require a static IP. Brokers' notices address orders.

---

## 4. Indices: NIFTY/BANKNIFTY spot has no volume (VWAP via futures) and India VIX availability

### Takeaway
Index spot values are calculated, not traded, so they carry no volume. Kite's index packet has no volume field. A VWAP for NIFTY or BANKNIFTY therefore has to be proxied, usually with the current-month index future. That future has a different session from the cash index (pre-open 09:00–09:15 since 8 Dec 2025; trading until 15:40 now and 15:45 from 7 Dec 2026) and trades at a premium or discount to spot. India VIX is available as an index feed from brokers, for example Upstox `NSE_INDEX|India VIX`.

### Cited Findings
- Kite index packets contain token, LTP, high, low, open, close, price change and exchange timestamp, with **no volume, quantity, buy/sell totals or OI** — [Kite WebSocket docs](https://kite.trade/docs/connect/v3/websocket/)
- Upstox lets you subscribe to index keys such as `NSE_INDEX|Nifty Bank`, but it is unclear whether the volume field is populated for indices. India VIX is available as `NSE_INDEX|India VIX`. — [Upstox V3 feed docs](https://upstox.com/developer/api-documentation/v3/get-market-data-feed/)
- F&O pre-open for current-month index and stock futures runs 09:00–09:15 from 8 Dec 2025 — [Business Standard](https://www.business-standard.com/markets/capital-market-news/nse-to-commence-pre-opening-session-in-f-o-segment-from-december-08-125110400728_1.html)
- Equity derivatives trade until 15:40 from 3 Aug 2026 ([Outlook Money](https://www.outlookmoney.com/invest/nse-extended-fo-timings-and-new-closing-auction-session-rules-explained)). From 7 Dec 2026 they trade until 15:45, except expiring index contracts, which stop at 15:30 on expiry day ([tick2trade](https://www.tick2trade.com/blogs/sebi-revises-nse-closing-auction-session-rules)).
- During CAS the index "can stay constant as trades are not continuously executed", and the official index close is computed after the auction — [Multibagg](https://www.multibagg.ai/market-pulse/articles/nifty-closing-price-cas-gap-cmsta63gb59h90zo5snn46x5n)
- Futures history limits:
  - Kite's `continuous=1` gives day candles only, and expired contract tokens cannot otherwise be retrieved ([Kite historical docs](https://kite.trade/docs/connect/v3/historical/)).
  - Dhan does not serve intraday data for expired futures ([Dhan support](https://dhan.co/support/platforms/dhanhq-api/how-can-i-retrieve-data-for-expired-futures-contracts-using-the-apis/)).
  - Fyers Standard allows 10 expired-F&O intraday requests per day ([Fyers plans](https://fyers.in/api-docs/v3/getting-started/plans-and-limits/)).

### Inferences
- A VWAP computed from Yahoo `^NSEI` bars is meaningless or approximated because there is no traded volume. Use near-month NIFTY/BANKNIFTY futures volume. Either compare the futures price with the futures VWAP, or shift the futures VWAP by the live basis (future − spot) before comparing it with spot levels.
- Futures sessions extend beyond the cash session: pre-open from 09:00 and trading to 15:40/15:45. A "session VWAP" must use one stated window, for example futures trades from 09:15 to 15:30 only, or levels will drift.
- Rolling to the next contract at monthly expiry causes a VWAP and volume discontinuity. Historical intraday futures data for expired months is hard to get from Kite and Dhan.
- Between 15:15 and about 15:35 (until 6 Dec 2026), index bars will look flat, followed by a jump to the official close. Triggers in that window on the spot index should be suppressed.

### Gaps
- What Yahoo reports in the volume field for `^NSEI`/`^NSEBANK`, and whether `^INDIAVIX` is real-time or delayed, could not be verified.
- No source was fetched on whether brokers' index ticks are refreshed every second or on each index computation.
- NIFTY/BANKNIFTY expiry calendars were not researched.

---

## 5. Crypto: Binance (and India-registered CoinDCX / Delta Exchange India) — REST vs WebSocket, kline update speed, UTC boundaries, in-progress candle, server time and rate limits, access from India

### Takeaway
Binance data is the exchange's own record, so it is exact for Binance prices:
- Trade and bookTicker streams are real-time.
- Kline streams push every **2 s** for 15m/1d candles (1 s for 1s candles), with an `x` flag when the candle is closed.
- Candles are **UTC-aligned by default**, so the "1d" candle runs **05:30–05:29:59 IST**. The REST `timeZone` parameter can realign them.
- REST `/klines` returns the **in-progress candle as the last row** (confirmed by own test).
- Limits are **6,000 request-weight per minute per IP**, and klines cost weight 2.

Binance registered with India's FIU in August 2024 and is accessible from India. CoinDCX and Delta Exchange India publish REST candle endpoints but little about limits.

### Cited Findings
- WebSocket kline stream `<symbol>@kline_<interval>`: "Update Speed" is **1000 ms for 1s and 2000 ms for other intervals**. The `x` field means "Is this kline closed?" and streams are UTC+0. Timezone-offset streams such as `@kline_1d@+08:00` open and close candles on offset boundaries, but `E/t/T` timestamps stay UTC. `@trade`, `@aggTrade` and `@bookTicker` are real-time. Partial depth comes in 5/10/20 levels at 100 ms or 1000 ms. — [Binance WebSocket streams](https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams)
- REST `GET /api/v3/klines` and `/uiKlines`: **weight 2**, data source "Database". The `timeZone` parameter defaults to 0 (UTC) and accepts −12:00 to +14:00; intervals are computed in that timezone, but `startTime/endTime` are always UTC. Limit defaults to 500, max 1000. "Klines are uniquely identified by their open time." `ticker/price` has weight 2 (single symbol) and is served from "Memory". `depth` weight is 5–250 depending on limit. — [Binance REST market-data endpoints](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints)
- Limits are per IP, not per API key. HTTP 429 means back off. HTTP 418 is an automated ban: "IP bans are tracked and scale in duration for repeat offenders, from 2 minutes to 3 days". Responses carry `Retry-After` and `X-MBX-USED-WEIGHT-*` headers. Signed requests need a timestamp in ms or µs; `recvWindow` defaults to 5000 ms (max 60000). `data-api.binance.vision` serves public market data only. — [Binance REST limits](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/limits)
- **Own test, `exchangeInfo` (2026-11-05):** REQUEST_WEIGHT **6000 per 1 minute**, RAW_REQUESTS 300,000 per 5 minutes, ORDERS 100 per 10 s and 200,000 per day; server timezone "UTC" — [data-api.binance.vision/api/v3/exchangeInfo?symbol=BTCUSDT](https://data-api.binance.vision/api/v3/exchangeInfo?symbol=BTCUSDT)
- **Own test, in-progress candle (03:05:42 UTC):** `klines?symbol=BTCUSDT&interval=15m&limit=2` returned 02:45–02:59:59.999 UTC (closed) and **03:00–03:14:59.999 UTC with a close time in the future**, i.e. still forming, with only 8,434 trades so far — [Binance klines](https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=2)
- **Own test, day-boundary effect.** BTCUSDT 1d for 4 Nov 2026:

  | Day definition | Window | O | H | L | C |
  |---|---|---|---|---|---|
  | UTC day | 00:00–23:59:59 UTC | 77,453.85 | 81,196.01 | 75,736.38 | **80,504.01** |
  | IST day (`timeZone=5:30`) | 18:30 UTC 3 Nov – 18:29:59 UTC 4 Nov | 77,670.03 | 81,196.01 | 75,736.38 | **80,600.01** |

  The previous-day close differs by **96.00 USDT (0.12%)** depending on the boundary. — [Binance klines (timeZone)](https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=2&timeZone=5:30)
- **Own test, clock sync:** `api.binance.com/api/v3/time` returned serverTime 1793847936658, against a local clock of …36061 before and …36697 after the request (round trip about 636 ms). The local clock agreed with Binance to within the round-trip uncertainty (about ±0.3 s). — [Binance /api/v3/time](https://api.binance.com/api/v3/time)
- Forum reports: the REST response's last candle can be open, and the WebSocket `x=true` marks the final update of a candle ([Binance dev forum: x field](https://dev.binance.vision/t/whats-the-meaning-of-x-i-e-closed-on-kline-stream/11686)). Right after a boundary, the new candle may be missing until its first trade, so a REST-only client "can not be sure what is in newest candle" ([Binance dev forum: kline generation](https://dev.binance.vision/t/new-candlestick-kline-generation-behavior/137)).
- India access: Binance registered with FIU-IND as a reporting entity in **August 2024** after a fine of about US$2.2 million (₹18.82 crore). Reports said its website and app became fully available in India. — [Business Today](https://www.businesstoday.in/technology/news/story/binance-achieves-legal-status-in-india-registers-with-financial-intelligence-unit-441692-2024-08-16); [Decrypt](https://decrypt.co/244850/binance-registers-with-indias-fiu-after-paying-2-25-million-fine)
- CoinDCX: public candles at `public.coindcx.com/market_data/candles`, with limit max 1000 and default 500 ([CoinDCX API help](https://coindcx.com/api/help/Market%20Data%20on%20CoinDCX%20API/Candles)). Streaming is Socket.IO at `stream.coindcx.com` ([APIs.io/API Evangelist listing](https://apis.apievangelist.com/store/streaming-api/), third-party). Rate limits are not published in the OpenAPI spec ([Jentic](https://jentic.com/apis/coindcx)).
- Delta Exchange India: `/v2/history/candles` on `https://api.india.delta.exchange`, up to 2,000 candles per request, start/end in Unix seconds. IP whitelisting is required for private calls, and no numeric rate limits are published. — [Delta Exchange help centre](https://www.delta.exchange/support/solutions/articles/80001174969-kickstarting-your-trading-journey-with-delta-india-apis); the 1,999-bar cap per request is from the third-party [StockSharp connector](https://www.nuget.org/packages/StockSharp.DeltaExchangeIndia)

### Inferences
- The bot's ccxt `fetch_ohlcv` (15m/1d/1w) gets exact Binance OHLCV. It must **drop the last row unless its close time is earlier than the Binance server time**, otherwise "confirm on 15-minute close" can fire on a half-formed candle.
- Better: subscribe to `@kline_15m` and act on `x=true`. Updates arrive every 2 s, so the confirmation lands about 0–2 s after the boundary. A REST poll should wait a buffer of 1–3 s after the boundary, then check the close time.
- "Previous-day" crypto levels must be defined explicitly as UTC day (Binance default, rolling over at 05:30 IST) or IST day (`timeZone=5:30`). The own test showed a 0.12% difference in prior close. CPR/pivots, and any weekly levels (Binance 1w candles start Monday 00:00 UTC, an inference not checked in docs), shift accordingly.
- At 15m/1d/1w polling for a few symbols, the bot uses a tiny fraction of the 6,000/min weight. Ban risk comes only from tight retry loops after 429s.
- Prices on India-registered INR venues (CoinDCX, Delta India) are different markets. Levels computed on Binance USDT pairs do not transfer exactly to them.

### Gaps
- No 2025–2026 source confirmed Binance's continued status for Indian users (KYC, INR rails) beyond the 2024 registration.
- CoinDCX and Delta India WebSocket channel specs, update speeds and numeric rate limits were not found in official docs.
- ccxt-specific handling (for example whether `fetch_ohlcv` filters the open candle) was not checked.

---

## 6. Forex and gold: no central exchange, vendor vs broker prices, daily candle boundaries, data sources (OANDA, Twelve Data, Massive/Polygon, Alpha Vantage, Finnhub, MT5) and XAU/USD spot vs COMEX GC futures

### Takeaway
Spot FX and spot gold trade over the counter with no consolidated tape. Every source (Yahoo/ICE, bank-feed vendors such as Massive, OANDA, MT5 brokers) publishes its **own** bid/ask or mid quotes, with no traded volume. Highs and lows differ slightly by source and spread. Daily candles depend on the provider's day boundary: OANDA defaults to **17:00 New York**, and others use GMT midnight or server time. "Exact" FX levels therefore mean "exact for one chosen provider and convention".

The bot's gold proxy **GC=F** is a different instrument: a COMEX futures contract, 30 minutes delayed on Yahoo, with a daily 17:00–18:00 ET halt. It trades at a basis (EFP) to London spot XAU/USD. That basis was about $40 and jumped to **>$100/oz in August 2025**. Indian residents also face RBI/FEMA restrictions on offshore forex platforms, which limits the "broker MT5 feed" route.

### Cited Findings
- **Massive (Currencies product):**
  - Basic costs $0, with 5 API calls/min, 2 years of history, **end-of-day** data and minute aggregates.
  - **Starter costs $49/month**, with unlimited calls, 10+ years of history, **real-time** data, second and minute aggregates and **WebSockets**.
  - Forex bars are built from **bid** prices. The `v` field is a quote count because "forex has no traded volume".
  - Source: **institutional bank feeds**; forex has no central exchange and no consolidated tape.
  - FX history starts 25 Sep 2009. Known gaps: C:XAUUSD missing Jul 2010–Jul 2013, and **sparse gold/silver quotes Jan 2021–Aug 2025**.
  - Source: [Massive Currencies](https://massive.com/currencies). The Massive pricing page lists Stocks Advanced at $199/month ([Massive pricing](https://massive.com/pricing)). It does not mention the Polygon.io name.
- **Twelve Data:**
  - Basic costs $0, with **8 API credits/min and 800/day**, described as "real-time" for US equities/ETFs, **forex and crypto**.
  - Grow $79/month, Pro $229/month (500+ WebSocket credits), Ultra $999/month.
  - The page's per-minute credit figures are inconsistent, and Indian exchanges are not mentioned.
  - Source: [Twelve Data pricing](https://twelvedata.com/pricing)
- **Alpha Vantage:** free tier of **25 requests/day**. Premium costs $49.99/month (75 req/min), $99.99 (150), $149.99 (300), $199.99 (600) and $249.99 (1,200). The page does not say whether FX intraday is premium-only. — [Alpha Vantage premium](https://www.alphavantage.co/premium/)
- **Finnhub:** the forex pricing page shows plans at $49.99 and $129.99 per month (billed quarterly). The tiers and the free-tier WebSocket scope could not be read. — [Finnhub forex pricing](https://www.finnhub.io/pricing-forex-api) (fragment only)
- **OANDA v20 candles:** `dailyAlignment` defaults to **17** (range 0–23), and `alignmentTimezone` defaults to **America/New_York**. Daily candles align to that hour, but times are returned in UTC. `includeFirst` supports polling from the last completed candle. — [async-v20 docs (annotations)](https://async-v20.readthedocs.io/en/latest/annotations.html); [async-v20 API](https://async-v20.readthedocs.io/en/latest/api.html); [OANDA v20 OpenAPI (docs.rs)](https://docs.rs/crate/oanda-v20-openapi/latest/source/docs/InstrumentApi.md). Secondary client docs; OANDA's own developer page returned 404.
- Day-boundary conventions differ by source:
  - OANDA daily bars run 5 pm to 5 pm New York ([QuantConnect forum](https://www.quantconnect.com/forum/discussion/4749)).
  - Broker day boundaries vary: "local time (with or without DST,) GMT/UTC, GMT+2, NY+7" ([MQL5 forum](https://www.mql5.com/en/forum/159190)).
  - Dukascopy users report conflicting answers: daily bars starting at 21:00/22:00 GMT, or anchored at GMT midnight ([Dukascopy forum](https://www.dukascopy.com/swiss/english/forex/jforex/forum/viewtopic.php?p=586)).
- OANDA's separate Exchange Rates API has no permanent free plan; it is a 7-day trial, then from **$450/month for 100,000 quotes** — [CurrencyFreaks blog](https://currencyfreaks.com/blog/Currency-Conversion-Api-Oanda-Pricing) (third-party)
- **India legal context:** RBI's Alert List of unauthorised forex platforms reached 95 entities with the 19 Nov 2025 update, which added Starnet FX, CapPlace, Mirrox, Fusion Markets, Trive, NXG Markets and Nord FX. Forex transactions on unauthorised platforms can lead to penal action under FEMA. — [Gulf News](https://gulfnews.com/business/banking/starnetfx-fusion-markets-among-7-new-unauthorised-forex-platforms-in-india-flagged-by-rbi-1.500352489); [Moneylife](https://moneylife.in/article/unauthorised-forex-trading-platforms-rbi-adds-7-more-entities-to-its-alert-list/78900.html); [RBI press release](https://www.website.rbi.org.in/web/rbi/-/press-releases/rbi-updates-the-alert-list-of-unauthorised-forex-trading-platforms-2)
- **Gold futures sessions:** CME lists GC on Globex "Sunday - Friday 6:00 p.m. - 5:00 p.m. (5:00 p.m. - 4:00 p.m. CT) with a 60-minute break each day beginning at 5:00 p.m." — [CME GC contract specs](https://cmegroup.com/trading/metals/precious/gold_contractSpecs_futures) (quoted from search snippet; the page itself timed out). Yahoo shows COMEX data **30 minutes delayed** — [Yahoo Help SLN2310](https://help.yahoo.com/kb/SLN2310.html)
- **Spot vs futures basis:** On 7–8 Aug 2025, the COMEX futures premium over London spot rose **above $100/oz from about $40/oz the week before**, after reports of US tariffs on 1 kg/100 oz bars. December futures (GCZ5) hit a record **$3,534**. Saxo's Ole Hansen called London spot XAU/USD the most reliable gauge and warned that futures moves were being driven by EFP changes. — [Saxo, 8 Aug 2025](https://www.home.saxo/pl-pl/content/articles/commodities/tariff-shock-sends-gold-futures-soaring--yet-spot-market-holds-the-real-signal-08082025)

### Inferences
- Yahoo `EURUSD=X`/`USDINR=X` "real-time (ICE)" values are indicative quotes from one aggregator, not a tradeable broker price, and their volume is zero or meaningless. Any "VWAP" on FX is at best tick-count-weighted (Massive's `vw` is an average bid), so VWAP is not a meaningful FX level.
- Prior-day H/L/C and pivots for FX change with the day boundary. NY-17:00 alignment (OANDA default, and most MT4/MT5 servers on GMT+2/+3) gives 5 daily bars per week. GMT-midnight alignment creates a short Sunday bar that becomes Monday's "previous day". This is a standard market convention, not separately verified here. The bot should use NY-17:00 (= 03:30 IST in winter and 02:30 IST during US daylight saving, by time-zone arithmetic) or document whichever convention it uses.
- **Gold:** CPR/pivots computed on GC=F differ from XAU/USD levels by the basis. In normal times that may be tens of dollars, but on 7–8 Aug 2025 it was over $100 (about 3% at about $3,500). Front-month roll jumps in a continuous `=F` series add more error, and the 30-minute delay pushes a 15-minute confirmation out by two or more candles. GC also halts 17:00–18:00 ET daily (03:30–04:30 IST in winter), while spot quotes continue to trade.
- To get **exact real-time spot FX/gold**, the realistic options for an India-based bot are:
  - Massive Currencies Starter at $49/month (but note its sparse gold history before Aug 2025).
  - Twelve Data's free tier (800 credits/day). This is enough for a handful of symbols on 15m polling if one time-series call costs 1 credit, which is unverified.
  - An OANDA or other broker API with its own bid/ask.
- Opening an offshore forex broker account to get an MT5 feed is legally risky for Indian residents (RBI Alert List/FEMA).
- Legal exact exchange data in India exists for **NSE currency derivatives (USDINR, EURINR…)** and **MCX gold (INR)** through Indian broker APIs. Kite's feed has a currency price divisor. These are different instruments, sessions and prices from EUR/USD spot or XAU/USD.

### Gaps
- Yahoo's FX/gold daily candle boundary and the exact ICE FX methodology (indicative composite or which contributors) are not documented.
- Not found: OANDA v20 trading API pricing/eligibility for Indian residents, Finnhub free-tier forex WebSocket scope, Twelve Data's forex source and latency, and Alpha Vantage's FX intraday tier.
- Current (November 2026) COMEX–London basis level not found.
- CME real-time data licensing cost for GC via a vendor not researched.
- Whether Massive's gold quotes are now dense (after Aug 2025) is not confirmed beyond its own gap note.

---

## 7. General: candle-close timing, clock sync (NTP) and how each delay or approximation becomes an error in levels and triggers

### Takeaway
Most "wrong level" errors come from **definitions**, not latency:
- which "close" is used: LTP, 30-minute VWAP or auction price;
- where the day starts: UTC, IST or NY 17:00;
- which instrument is used: spot, futures or index;
- whether the newest candle is complete.

Latency matters for **triggers**. A 15-minute close confirmation arrives at candle close plus source delay (0 s for Binance and broker feeds; 30 min for Yahoo COMEX; 15 min for Yahoo BSE), plus polling interval, plus finalisation lag (Binance kline push up to 2 s; Kite ticks about 1 s). Clock skew moves the bot's own candle boundaries.

### Cited Findings
- Binance kline streams update every 2000 ms (1000 ms for 1s klines), and `x` marks a closed kline — [Binance WebSocket streams](https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams)
- Binance REST returns the open (in-progress) candle as the last row (own test, Section 5). A new candle may not exist until the first trade after the boundary. — [Binance klines](https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=2); [Binance dev forum](https://dev.binance.vision/t/new-candlestick-kline-generation-behavior/137)
- Binance signed requests require a timestamp, `recvWindow` defaults to 5,000 ms, and the server time endpoint lets a client measure its offset. The own test found a local clock within about ±0.3 s of Binance. — [Binance REST limits](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/limits); [Binance /api/v3/time](https://api.binance.com/api/v3/time)
- Kite: candles can be built from the first, last, high and low ticks in each interval. Ticks are roughly 1 per second for liquid scrips and none when a scrip has no trades. Opens and closes were seen arriving a couple of seconds late. Kite packets include an exchange timestamp. — [Kite forum](https://kite.trade/forum/discussion/3574/is-the-websocket-data-sampled-by-1-sec); [Kite WebSocket docs](https://kite.trade/docs/connect/v3/websocket/)
- Dhan's last-trade time is a 32-bit epoch (1-second resolution) — [DhanHQ live feed](https://dhanhq.co/docs/v2/live-market-feed/)
- Delays published by Yahoo: NSE real-time, BSE 15 min, FX real-time, CME/CBOT 10 min, COMEX/NYMEX 30 min — [Yahoo Help SLN2310](https://help.yahoo.com/kb/SLN2310.html)

### Inferences
**Error budget per current input:**

| Input the bot uses today | Timing class (stated) | What is approximated | Typical effect on levels/triggers |
|---|---|---|---|
| RELIANCE.NS etc. via yfinance 5m | "Real-time" (Yahoo/ICE), unofficial, no SLA | Missing bars (incl. 15:15–15:30 CAS gap for F&O stocks), provisional/NaN latest daily row, possible non-official close, dividend-adjusted history by default | Prior-day C error moves P by ΔC/3 and TC/R1/S1 by 2ΔC/3. Opening range 09:15–09:30 is fine if bars exist. VWAP from 5m bars only approximates exchange ATP. |
| ^NSEI / ^NSEBANK via yfinance | Not listed on Yahoo's delay table | No volume, so no true VWAP. Flat 15:15–~15:35 then jump to official close (since 3 Aug 2026) | Early-CAS average gap of about 0.42% (~100 NIFTY points) between 15:15 and official close shifts P about 34 points and TC about 69 points if the wrong close is used. |
| EURUSD=X, USDINR=X 15m | "Real-time" (ICE), indicative | Provider-specific quotes, no volume, unknown day boundary | Prior-day H/L/C can differ by boundary (NY 17:00 vs midnight) and by provider/spread. Pivots differ accordingly. |
| GC=F as XAU/USD | **30-min delayed** COMEX futures | Different instrument (basis/EFP), roll jumps, daily 17:00–18:00 ET halt | All levels offset by the basis (tens of $, >$100 on 7–8 Aug 2025). 15m confirmations arrive 2+ candles late. |
| Binance klines via ccxt | Exchange real-time (exact for Binance) | Last REST row is in-progress; UTC day boundary | A trigger on an unclosed candle is a false confirmation. Prior-day close differed by 96 USDT (0.12%) between UTC-day and IST-day in the own test. |

**Rules that follow:**
- Confirm on candle close only when the source marks the candle closed (Binance `x=true`) or when `close_time < exchange_server_time`.
- Wait a small buffer (1–3 s) after the boundary before polling.
- Never compute prior-day levels before the official close is published. For NSE that is after CAS matching: about 15:35 IST until 6 Dec 2026, about 15:40+ from 7 Dec 2026.
- Keep the host clock NTP-synced. Periodically log the offset against Binance `/api/v3/time` (or broker exchange timestamps) and alert if it exceeds, say, 500 ms.
- Build candles on exchange timestamps, not on local receive time.

**What "exact real-time" costs per market (Nov 2026):**

| Market | What exact real-time needs | Cost |
|---|---|---|
| NSE stocks, indices, futures, India VIX | Own broker API | Upstox / Fyers Standard / Breeze ₹0 (stated); Dhan ₹499 + tax/month; Zerodha Kite ₹500/month (credit-renewed if ≥₹2,000 brokerage/month from Oct 2026) |
| Crypto | Binance public API | Free; 6,000 weight/min/IP |
| Spot FX/gold | One chosen provider, used consistently | Massive Starter $49/month; Twelve Data free (800 credits/day) to $79–$229/month; Alpha Vantage $49.99+/month |
| India-legal exchange FX/gold | NSE currency futures and MCX gold via an Indian broker API | Same broker API cost as NSE |
| COMEX GC real-time | Licensed CME vendor | Not researched |

### Gaps
- No authoritative NTP guidance was fetched. The clock advice above is an engineering inference, supported only by the own Binance offset test.
- I found no source quantifying how often Yahoo NSE 5m bars are missing, or comparing Yahoo against bhavcopy closes after CAS.
- Weekly-candle start conventions (Binance 1w, FX weekly) were not verified in docs.
