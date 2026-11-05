'use strict';

// ABD Analyzer dashboard: asks the bot's three questions, draws the plan, and links Telegram.

const $ = (selector) => document.querySelector(selector);
const REFRESH_MS = 60_000; // live intraday plans refresh every minute (the server caches for the same time)
const LINK_POLL_MS = 2500;

const state = {
  meta: null,
  style: 'intraday',
  market: 'stocks',
  report: null,
  query: null, // the {style, market, symbol} the shown report was made for
  selected: 0,
  telegram: null,
  link: null, // {url, expiresAt} while waiting for the user to press Start in Telegram
  timers: { refresh: 0, linkPoll: 0, toast: 0 },
};

// --- small helpers ---------------------------------------------------------------------------

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value == null || value === false) continue;
    if (key === 'class') node.className = value;
    else if (key === 'text') node.textContent = value;
    else if (key.startsWith('on')) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value === true ? '' : value);
  }
  for (const child of children.flat()) {
    if (child == null || child === false) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

// replaceChildren() would print a skipped (null) child as the text "null"
function fill(node, ...children) {
  node.replaceChildren(...children.flat().filter((child) => child != null && child !== false));
}

const saved = {
  get(key) {
    try { return JSON.parse(localStorage.getItem(key)); } catch { return null; }
  },
  set(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private mode: just don't remember */ }
  },
};

async function request(path, options = {}) {
  const init = { credentials: 'same-origin', ...options };
  if (init.method === 'POST') {
    init.headers = { 'Content-Type': 'application/json', 'X-ABD': '1' };
    if (options.body !== undefined) init.body = JSON.stringify(options.body);
  }
  let response;
  try {
    response = await fetch(path, init);
  } catch {
    throw new Error('Dashboard server se connection nahi hua. Terminal mein ./run.sh web chal raha hai?');
  }
  let data = null;
  try { data = await response.json(); } catch { /* empty or non-JSON body */ }
  if (!response.ok) {
    const detail = data && data.detail;
    throw new Error(typeof detail === 'string' ? detail : `Server ne error diya (${response.status}).`);
  }
  return data;
}

function css(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function numberFormat(instrument) {
  const digits = instrument.decimals;
  return new Intl.NumberFormat(instrument.currency === 'INR' ? 'en-IN' : 'en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function showStatus(text, isError = false) {
  const node = $('#ask-status');
  node.textContent = text;
  node.classList.toggle('is-error', isError);
}

function toast(text, isError = false) {
  const node = $('#toast');
  node.textContent = text;
  node.classList.toggle('is-error', isError);
  node.classList.add('is-on');
  clearTimeout(state.timers.toast);
  state.timers.toast = setTimeout(() => node.classList.remove('is-on'), 3800);
}

// --- the three questions -----------------------------------------------------------------------

function buildQuestions() {
  segment($('#style-seg'), 'style', state.meta.styles, state.style, (value) => {
    state.style = value;
    runPlan();
  });
  segment($('#market-seg'), 'market', state.meta.markets, state.market, (value) => {
    state.market = value;
    buildQuick();
    $('#symbol').value = quickSymbols()[0] || '';
    runPlan();
  });
  buildQuick();
}

function segment(root, name, options, current, onChange) {
  root.replaceChildren(...options.flatMap((option) => {
    const id = `${name}-${option.value}`;
    return [
      el('input', { type: 'radio', name, id, value: option.value, checked: option.value === current, onchange: () => onChange(option.value) }),
      el('label', { for: id, text: option.label }),
    ];
  }));
}

function quickSymbols() {
  return state.meta.quick_symbols[state.market] || [];
}

function buildQuick() {
  const symbols = quickSymbols();
  $('#symbol').placeholder = symbols[0] || '';
  $('#quick').replaceChildren(
    el('span', { class: 'quick-label', text: 'Jaldi chuno:' }),
    ...symbols.map((symbol) => el('button', {
      type: 'button',
      class: 'chip',
      text: symbol,
      onclick: () => { $('#symbol').value = symbol; runPlan(); },
    })),
  );
}

// --- loading a plan -----------------------------------------------------------------------------

let ticket = 0;

async function runPlan({ quiet = false } = {}) {
  const symbol = $('#symbol').value.trim().toUpperCase();
  if (!symbol) {
    showStatus(`Symbol likho, jaise ${quickSymbols()[0] || 'RELIANCE'}.`, true);
    $('#symbol').focus();
    return;
  }
  const query = { style: state.style, market: state.market, symbol };
  saved.set('abd-last', query);
  const mine = ++ticket;
  clearTimeout(state.timers.refresh);
  $('#result').classList.add('is-loading'); // keep the old plan on screen, dimmed, until the new one lands
  if (!quiet) showStatus(`${symbol} ka ${styleLabel(query.style)} plan ban raha hai…`);
  try {
    const report = await request(`/api/plan?${new URLSearchParams(query)}`);
    if (mine !== ticket) return; // a newer request has taken over
    const sameSetups = quiet && state.report && state.report.setups.length === report.setups.length;
    state.report = report;
    state.query = query;
    state.selected = sameSetups ? state.selected : Math.max(0, report.setups.findIndex((s) => s.primary));
    render(report);
    showStatus('');
  } catch (error) {
    if (mine !== ticket) return;
    showStatus(error.message, true);
  } finally {
    if (mine === ticket) $('#result').classList.remove('is-loading');
  }
  scheduleRefresh();
}

function styleLabel(value) {
  const style = state.meta.styles.find((s) => s.value === value);
  return style ? style.label : value;
}

function scheduleRefresh() {
  clearTimeout(state.timers.refresh);
  const r = state.report;
  if (!r || !r.live || r.style !== 'intraday') return;
  state.timers.refresh = setTimeout(() => {
    if (document.visibilityState === 'visible') runPlan({ quiet: true });
    else scheduleRefresh();
  }, REFRESH_MS);
}

// --- rendering ---------------------------------------------------------------------------------

function render(r) {
  $('#result').hidden = false;
  renderHeadline(r);
  renderLadder(r);
  renderPlanActions();
  renderChart(r);
  renderBias(r);
  renderLevels(r);
  renderLiquidity(r);
  renderContext(r);
  renderFineprint(r);
}

function renderHeadline(r) {
  const change = r.change_pct;
  const direction = change > 0 ? 'up' : change < 0 ? 'down' : 'flat';
  $('#headline').replaceChildren(
    el('div', {},
      el('h1', { text: r.instrument.name }),
      el('p', { class: 'tags' },
        el('span', { text: r.instrument.exchange }),
        el('span', { text: r.style_label }),
        el('span', { text: `${r.timeframe} candles` }))),
    el('div', { class: 'headline-price' },
      el('p', { class: 'ltp', text: `${r.instrument.sign}${r.price_text}` }),
      change == null ? null : el('p', { class: `chg chg--${direction}` },
        el('span', { class: 'chg-mark', 'aria-hidden': 'true' }),
        `${change > 0 ? '+' : ''}${change.toFixed(2)}% (${r.change_basis})`)),
    el('p', { class: 'headline-meta' },
      el('span', { class: r.live ? 'status status--live' : 'status', text: r.status }),
      `Aakhri candle ${r.as_of_text}. Data: ${r.source}.`),
  );
}

function renderLadder(r) {
  const above = [];
  const below = [];
  r.setups.forEach((setup, index) => (setup.level > r.price ? above : below).push([setup, index]));
  const byPriceDesc = (a, b) => b[0].level - a[0].level;
  above.sort(byPriceDesc);
  below.sort(byPriceDesc);
  const middle = r.wait_zone ? waitBand(r) : ltpRung(r);
  const items = [...above.map(rung), middle, ...below.map(rung)];
  if (!r.setups.length) items.push(el('li', { class: 'ladder-empty', text: 'Abhi koi saaf trigger nahi bana. Neeche key levels dekho.' }));
  $('#ladder').replaceChildren(...items);
  requestAnimationFrame(() => requestAnimationFrame(() => placeLtp(r))); // let the marker travel from mid-band
}

function rung([setup, index]) {
  const selected = index === state.selected;
  const show = el('button', {
    type: 'button',
    class: 'quiet-link rung-show',
    'aria-pressed': String(selected),
    text: selected ? 'Chart par dikh raha hai' : 'Chart par dikhao',
    onclick: (event) => { event.stopPropagation(); select(index); },
  });
  return el('li', {
    class: `rung rung--${setup.direction}${selected ? ' is-selected' : ''}`,
    'data-index': index,
    onclick: () => select(index),
  },
    el('div', { class: 'rung-head' },
      el('span', { class: 'rung-name', text: setup.name }),
      setup.primary ? el('span', { class: 'badge', text: 'Bias ke saath' }) : null),
    el('p', { class: 'rung-price' }, el('span', { class: 'rung-verb', text: setup.verb }), el('strong', { text: setup.level_text })),
    el('p', { class: 'rung-when', text: setup.trigger }),
    el('dl', { class: 'rung-nums' },
      num('Entry', setup.entry_text), // risk on the first row, reward on the second
      num('SL', setup.stop_text),
      num('R:R', `1:${setup.reward_risk}`),
      ...setup.targets.map((target, i) => num(`T${i + 1}`, target.text))),
    setup.note ? el('p', { class: 'rung-note', text: setup.note }) : null,
    show);
}

function num(label, value) {
  return el('div', {}, el('dt', { text: label }), el('dd', { text: value }));
}

function waitBand(r) {
  return el('li', { class: 'wait' },
    el('p', { class: 'wait-title', text: 'Wait zone' }),
    el('p', { class: 'wait-range', text: r.wait_zone.text }),
    el('p', { class: 'wait-hint', text: 'Iske andar trade mat karo. Price ko side chunne do.' }),
    el('div', { class: 'ltp-mark', id: 'ltp-mark' },
      el('span', { class: 'ltp-dot', 'aria-hidden': 'true' }),
      el('span', { class: 'ltp-tag', text: `LTP ${r.price_text}` })));
}

function ltpRung(r) {
  const at = r.at_price.length ? `at ${r.at_price[0].labels.join(' + ')}` : null;
  return el('li', { class: 'ltp-rung' },
    el('span', { class: 'ltp-dot', 'aria-hidden': 'true' }),
    el('span', { class: 'ltp-label', text: 'LTP' }),
    el('strong', { text: `${r.instrument.sign}${r.price_text}` }),
    at ? el('span', { class: 'ltp-at', text: at }) : null);
}

function placeLtp(r) {
  const mark = $('#ltp-mark');
  if (!mark || !r.wait_zone) return;
  const { low, high } = r.wait_zone;
  const share = high > low ? (high - r.price) / (high - low) : 0.5;
  mark.style.setProperty('--pos', `${Math.min(88, Math.max(12, share * 100))}%`);
}

function select(index) {
  state.selected = index;
  document.querySelectorAll('.rung').forEach((node) => {
    const on = Number(node.dataset.index) === index;
    node.classList.toggle('is-selected', on);
    const button = node.querySelector('.rung-show');
    button.setAttribute('aria-pressed', String(on));
    button.textContent = on ? 'Chart par dikh raha hai' : 'Chart par dikhao';
  });
  if (state.report) {
    drawLines(state.report);
    renderLegend(state.report);
  }
}

function renderPlanActions() {
  const t = state.telegram;
  const root = $('#plan-actions');
  if (t && t.running && t.linked) {
    root.replaceChildren(el('button', { type: 'button', class: 'secondary', text: 'Ye plan Telegram par bhejo', onclick: sendToTelegram }));
  } else {
    root.replaceChildren(el('button', {
      type: 'button',
      class: 'quiet-link',
      text: 'Ye plan Telegram par paane ke liye connect karo',
      onclick: (event) => { event.stopPropagation(); openTelegramPanel(); },
    }));
  }
}

// --- chart ----------------------------------------------------------------------------------------

const chartState = { chart: null, candles: null, lines: [], format: null };

function renderChart(r) {
  const box = $('#chart');
  const LWC = window.LightweightCharts;
  if (chartState.chart) {
    chartState.chart.remove();
    chartState.chart = null;
  }
  if (!LWC) {
    box.replaceChildren(el('p', { class: 'chart-missing', text: 'Chart load nahi hua (internet check karo). Saare levels neeche table mein hain.' }));
    return;
  }
  box.replaceChildren();
  const intraday = !['1d', '1wk'].includes(r.timeframe);
  const format = numberFormat(r.instrument);
  const digits = r.instrument.decimals;
  const chart = LWC.createChart(box, {
    autoSize: true,
    layout: {
      background: { type: 'solid', color: css('--surface') },
      textColor: css('--ink-2'),
      fontFamily: getComputedStyle(document.body).fontFamily,
      fontSize: 12,
      panes: { separatorColor: css('--rule'), separatorHoverColor: css('--grid') },
    },
    grid: { vertLines: { color: css('--grid') }, horzLines: { color: css('--grid') } },
    rightPriceScale: { borderColor: css('--axis') },
    timeScale: { borderColor: css('--axis'), timeVisible: intraday, secondsVisible: false, rightOffset: 6 },
    crosshair: { mode: LWC.CrosshairMode.Normal },
  });
  const candles = chart.addSeries(LWC.CandlestickSeries, {
    upColor: css('--buy'),
    downColor: css('--sell'),
    wickUpColor: css('--buy'),
    wickDownColor: css('--sell'),
    borderVisible: false,
    priceLineColor: css('--ink'),
    priceFormat: { type: 'custom', minMove: 10 ** -digits, formatter: (price) => format.format(price) },
  });
  candles.setData(r.candles.map(({ time, open, high, low, close }) => ({ time, open, high, low, close })));
  if (r.instrument.has_volume && r.candles.some((bar) => bar.volume > 0)) {
    const volume = chart.addSeries(LWC.HistogramSeries, {
      color: css('--vol'),
      priceFormat: { type: 'volume' },
      priceLineVisible: false,
      lastValueVisible: false,
    }, 1); // its own pane under the price, never a second scale on the same plot
    volume.setData(r.candles.map((bar) => ({ time: bar.time, value: bar.volume })));
    const pane = chart.panes()[1];
    if (pane && pane.setHeight) pane.setHeight(76);
  }
  Object.assign(chartState, { chart, candles, lines: [], format });
  drawLines(r);
  renderLegend(r);
  const count = r.candles.length;
  chart.timeScale().setVisibleLogicalRange({ from: Math.max(0, count - (intraday ? 150 : 130)), to: count + 6 });
  chart.subscribeCrosshairMove((param) => showOhlc(r, param));
  showOhlc(r, null);
}

function drawLines(r) {
  const { candles, lines } = chartState;
  if (!candles) return;
  lines.splice(0).forEach((line) => candles.removePriceLine(line));
  const style = window.LightweightCharts.LineStyle;
  const add = (price, color, lineStyle, lineWidth, title, axisLabelVisible) => {
    lines.push(candles.createPriceLine({ price, color, lineStyle, lineWidth, title, axisLabelVisible }));
  };
  r.resistance.forEach((zone) => add(zone.mid, css('--sell-line'), style.Dotted, 1, zone.labels[0], false));
  r.support.forEach((zone) => add(zone.mid, css('--buy-line'), style.Dotted, 1, zone.labels[0], false));
  const setup = r.setups[state.selected];
  if (setup) {
    const side = css(setup.direction === 'long' ? '--buy' : '--sell');
    add(setup.level, side, style.Solid, 2, setup.verb, true);
    add(setup.stop, css('--ink-2'), style.Dashed, 1, 'SL', true);
    setup.targets.forEach((target, i) => add(target.price, side, style.Dotted, 1, `T${i + 1}`, true));
  }
}

function renderLegend(r) {
  const setup = r.setups[state.selected];
  const side = setup && setup.direction === 'long' ? 'buy' : 'sell';
  fill($('#legend'),
    setup ? swatch(side, 'solid', setup.verb) : null,
    setup ? swatch('ink', 'dashed', 'Stop-loss') : null,
    setup ? swatch(side, 'dotted', 'Target') : null,
    swatch('sell-faint', 'dotted', 'Resistance zone'),
    swatch('buy-faint', 'dotted', 'Support zone'),
  );
}

function swatch(color, lineStyle, label) {
  return el('li', {}, el('span', { class: `swatch swatch--${color} swatch--${lineStyle}`, 'aria-hidden': 'true' }), label);
}

function showOhlc(r, param) {
  let bar = param && param.seriesData ? param.seriesData.get(chartState.candles) : null;
  let time = param && param.time != null ? param.time : null;
  if (!bar) {
    bar = r.candles[r.candles.length - 1];
    time = bar ? bar.time : null;
  }
  if (!bar) return;
  const f = chartState.format;
  $('#ohlc').replaceChildren(
    el('span', { class: 'ohlc-time', text: timeText(time) }),
    ...[['O', bar.open], ['H', bar.high], ['L', bar.low], ['C', bar.close]].map(([label, value]) => el('span', {}, el('b', { text: label }), ` ${f.format(value)}`)),
  );
}

function timeText(time) {
  if (time == null) return '';
  if (typeof time === 'number') { // IST wall-clock written as UTC seconds by the server
    return new Date(time * 1000).toLocaleString('en-GB', { timeZone: 'UTC', day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
  }
  const date = typeof time === 'string' ? new Date(`${time}T00:00:00Z`) : new Date(Date.UTC(time.year, time.month - 1, time.day));
  return date.toLocaleDateString('en-GB', { timeZone: 'UTC', day: '2-digit', month: 'short', year: 'numeric' });
}

// --- the columns under the chart ------------------------------------------------------------

function renderBias(r) {
  const b = r.bias;
  const node = $('#bias');
  node.className = `bias bias--${b.label.toLowerCase()}`;
  node.replaceChildren(
    el('h2', { text: 'Bias' }),
    el('p', { class: 'bias-label' },
      el('span', { class: 'bias-mark', 'aria-hidden': 'true' }),
      b.label,
      el('span', { class: 'bias-score', text: `score ${b.score > 0 ? '+' : ''}${b.score} / ${b.votes}` })),
    el('ul', { class: 'reasons' }, b.reasons.map((reason) => el('li', { class: `reason reason--${reason.dir}`, text: reason.text }))),
  );
}

function renderLevels(r) {
  const row = (zone, kind) => el('tr', { class: `lv lv--${kind}` },
    el('td', { class: 'lv-price', text: zone.text }),
    el('td', { text: zone.labels.join(' + ') }),
    el('td', {}, meter(zone.stars)));
  const ltpLabel = r.at_price.length ? `LTP, at ${r.at_price[0].labels.join(' + ')}` : 'LTP';
  $('#levels').replaceChildren(
    el('thead', {}, el('tr', {},
      el('th', { scope: 'col', text: 'Price' }),
      el('th', { scope: 'col', text: 'Kya hai' }),
      el('th', { scope: 'col', text: 'Strength' }))),
    el('tbody', {},
      [...r.resistance].reverse().map((zone) => row(zone, 'res')),
      el('tr', { class: 'lv lv--ltp' }, el('td', { class: 'lv-price', text: r.price_text }), el('td', { text: ltpLabel }), el('td')),
      r.support.map((zone) => row(zone, 'sup'))),
  );
  $('#pivots').replaceChildren(...(r.pivots.length
    ? [el('b', { text: 'Pivots' }), ...r.pivots.map((p) => el('span', { text: `${p.name} ${p.text}` }))]
    : []));
}

function meter(filled) {
  return el('span', { class: 'meter', role: 'img', 'aria-label': `Strength ${filled} of 5` },
    ...Array.from({ length: 5 }, (_, i) => el('i', { class: i < filled ? 'on' : '' })));
}

function renderLiquidity(r) {
  const list = (pools) => (pools.length
    ? el('ul', { class: 'pool-list' }, pools.map((p) => el('li', {}, el('span', { class: 'pool-price', text: p.text }), p.label)))
    : el('p', { class: 'muted', text: 'Paas mein koi nahi.' }));
  const sweep = (s) => (s.side === 'buy'
    ? `${s.when}: ${s.text} (${s.label}) ke upar ke stops liye aur close wapas neeche aaya, bearish sign`
    : `${s.when}: ${s.text} (${s.label}) ke neeche ke stops liye aur close wapas upar aaya, bullish sign`);
  fill($('#liquidity'),
    el('h2', { text: 'Liquidity' }),
    el('h3', { text: 'Buy-side: highs ke upar stops' }), list(r.buy_side),
    el('h3', { text: 'Sell-side: lows ke neeche stops' }), list(r.sell_side),
    r.sweeps.length ? el('h3', { text: 'Haal ke sweeps (stop hunt)' }) : null,
    r.sweeps.length ? el('ul', { class: 'sweeps' }, r.sweeps.map((s) => el('li', { text: sweep(s) }))) : null,
  );
}

function renderContext(r) {
  $('#context').replaceChildren(...r.context.map((section) => el('div', { class: 'ctx' },
    el('h3', { text: section.title }),
    el('ul', {}, section.lines.map((line) => el('li', { text: line }))))));
}

function renderFineprint(r) {
  fill($('#fineprint'),
    r.notes.length ? el('ul', {}, r.notes.map((note) => el('li', { text: note }))) : null,
    el('p', { text: r.disclaimer }),
  );
}

// --- Telegram ----------------------------------------------------------------------------------

async function refreshTelegram() {
  try {
    state.telegram = await request('/api/telegram');
  } catch (error) {
    state.telegram = { configured: false, running: false, linked: false, error: error.message };
  }
  renderTelegram();
}

function renderTelegram() {
  const t = state.telegram || {};
  const chip = $('#tg-chip');
  chip.classList.toggle('is-linked', Boolean(t.linked));
  chip.replaceChildren('Telegram', el('span', { class: 'tg-chip-extra', text: t.linked ? `: ${t.chat_name}` : ' connect karo' }));
  chip.setAttribute('aria-label', t.linked ? `Telegram connected: ${t.chat_name}` : 'Telegram connect karo');
  $('#tg-panel').replaceChildren(el('div', { class: 'tg-box' }, ...telegramBody(t)));
  if (state.report) renderPlanActions();
}

function telegramBody(t) {
  if (!t.configured) {
    return [
      el('h2', { text: 'Telegram bot jodo' }),
      el('p', { text: 'Ek baar setup karo. Phir bot Telegram par wahi 3 sawaal buttons se poochhega, aur dashboard ka plan ek click mein wahan pahunchega.' }),
      el('ol', { class: 'tg-steps' },
        el('li', {}, 'Telegram mein ', el('code', { text: '@BotFather' }), ' kholo, ', el('code', { text: '/newbot' }), ' bhejo, naam aur username do.'),
        el('li', {}, 'Jo token mile, project folder ki ', el('code', { text: '.env' }), ' file mein likho: ', el('code', { text: 'TELEGRAM_BOT_TOKEN=aapka-token' })),
        el('li', {}, 'Terminal mein dashboard band karke dobara chalao: ', el('code', { text: './run.sh web' }))),
    ];
  }
  if (!t.running) {
    return [
      el('h2', { text: 'Telegram bot chal nahi raha' }),
      el('p', { text: t.error || 'Bot start nahi hua. Terminal ke messages dekho.' }),
    ];
  }
  if (t.linked) {
    return [
      el('h2', { text: `Connected: ${t.chat_name}` }),
      el('p', { text: `Plan @${t.bot_username} se aapke Telegram par aayenge.` }),
      el('div', { class: 'tg-actions' },
        el('button', { type: 'button', class: 'primary', text: 'Ye plan Telegram par bhejo', onclick: sendToTelegram, disabled: !state.report }),
        el('button', { type: 'button', class: 'quiet-link', text: 'Disconnect karo', onclick: disconnectTelegram })),
    ];
  }
  if (state.link) {
    return [
      el('h2', { text: 'Telegram mein Start dabao' }),
      el('p', { text: 'Neeche wala button Telegram kholega. Wahan Start dabate hi ye page apne aap connect ho jayega. Link 10 minute chalega.' }),
      el('div', { class: 'tg-actions' },
        el('a', { class: 'primary', href: state.link.url, target: '_blank', rel: 'noopener', text: `@${t.bot_username} kholo` }),
        el('span', { class: 'tg-wait' }, el('span', { class: 'pulse', 'aria-hidden': 'true' }), 'Start ka intezaar…')),
    ];
  }
  return [
    el('h2', { text: 'Telegram connect karo' }),
    el('p', { text: `Bot @${t.bot_username} taiyaar hai. Connect karne par dashboard ke plan seedha aapke Telegram par jayenge.` }),
    el('div', { class: 'tg-actions' }, el('button', { type: 'button', class: 'primary', text: 'Connect link banao', onclick: startLink })),
  ];
}

function toggleTelegramPanel() {
  if ($('#tg-panel').hidden) openTelegramPanel();
  else closeTelegramPanel();
}

function openTelegramPanel() {
  $('#tg-panel').hidden = false;
  $('#tg-chip').setAttribute('aria-expanded', 'true');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function closeTelegramPanel() {
  $('#tg-panel').hidden = true;
  $('#tg-chip').setAttribute('aria-expanded', 'false');
}

function closeTelegramPanelFromOutside(event) {
  const panel = $('#tg-panel');
  if (panel.hidden) return;
  if (event.type === 'keydown') {
    if (event.key !== 'Escape') return;
    closeTelegramPanel();
    $('#tg-chip').focus();
    return;
  }
  // composedPath is fixed at dispatch, so clicks on buttons the panel has since re-rendered still count as inside
  const path = event.composedPath();
  if (!path.includes(panel) && !path.includes($('#tg-chip'))) closeTelegramPanel();
}

async function startLink() {
  try {
    const { url, expires_in: seconds } = await request('/api/telegram/link', { method: 'POST' });
    state.link = { url, expiresAt: Date.now() + seconds * 1000 };
    renderTelegram();
    pollLink();
  } catch (error) {
    toast(error.message, true);
  }
}

function pollLink() {
  clearInterval(state.timers.linkPoll);
  state.timers.linkPoll = setInterval(async () => {
    if (!state.link || Date.now() > state.link.expiresAt) {
      clearInterval(state.timers.linkPoll);
      state.link = null;
      renderTelegram();
      return;
    }
    try {
      const t = await request('/api/telegram');
      if (!t.linked) return;
      clearInterval(state.timers.linkPoll);
      state.link = null;
      state.telegram = t;
      renderTelegram();
      toast(`Telegram connect ho gaya: ${t.chat_name}`);
    } catch (error) {
      console.warn('Telegram status check failed, retrying', error); // next tick tries again
    }
  }, LINK_POLL_MS);
}

async function sendToTelegram() {
  if (!state.query) return;
  try {
    const result = await request('/api/telegram/send', { method: 'POST', body: state.query });
    toast(`Telegram par bhej diya (${result.chat_name})`);
  } catch (error) {
    toast(error.message, true);
    refreshTelegram();
  }
}

async function disconnectTelegram() {
  try {
    await request('/api/telegram/unlink', { method: 'POST' });
    toast('Telegram disconnect ho gaya');
  } catch (error) {
    toast(error.message, true);
  }
  refreshTelegram();
}

// --- theme & start-up ------------------------------------------------------------------------------

function setupTheme() {
  $('#theme').addEventListener('click', () => {
    const current = document.documentElement.dataset.theme
      || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('abd-theme', next); } catch { /* not remembered */ }
    if (state.report) renderChart(state.report);
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (!document.documentElement.dataset.theme && state.report) renderChart(state.report);
  });
}

async function init() {
  setupTheme();
  $('#tg-chip').addEventListener('click', toggleTelegramPanel);
  document.addEventListener('click', closeTelegramPanelFromOutside);
  document.addEventListener('keydown', closeTelegramPanelFromOutside);
  $('#ask').addEventListener('submit', (event) => { event.preventDefault(); runPlan(); });
  try {
    state.meta = await request('/api/meta');
  } catch (error) {
    showStatus(error.message, true);
    return;
  }
  const last = saved.get('abd-last');
  const known = (list, value) => list.some((item) => item.value === value);
  if (last && known(state.meta.styles, last.style) && known(state.meta.markets, last.market)) {
    state.style = last.style;
    state.market = last.market;
  }
  buildQuestions();
  $('#symbol').value = (last && last.market === state.market && last.symbol) || quickSymbols()[0] || '';
  refreshTelegram();
  runPlan();
}

init();
