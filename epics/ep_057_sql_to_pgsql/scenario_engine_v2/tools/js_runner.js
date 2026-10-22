// epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/js_runner.js — runs the page's real JS functions (extracted by inventory line range) in a Node VM.
process.on("unhandledRejection", e => { if (process.env.DIFF_JS_REJECTIONS) require("fs").appendFileSync(process.env.DIFF_JS_REJECTIONS, "UNHANDLED: " + (e && e.stack ? e.stack.split("\n").slice(0, 4).join(" | ") : e) + "\n"); });
//
// VERSION HISTORY
// v1.6.0 · 2026-10-17 · __imm (setImmediate) exposed so a stub can deliver each response as its own macrotask.
// v1.5.0 · 2026-10-17 · Async calls are awaited (the page's fetchers); URL / URLSearchParams available in the VM.
// v1.4.0 · 2026-10-17 · State defaults and stubs for the auto-top1 refresh and exact-search helpers.
// v1.3.0 · 2026-10-17 · State defaults and inert UI stubs so the small page helpers (clock, search terms, request options, step / seek, return type) can run.
// v1.2.1 · 2026-10-16 · A patch whose replacement is already in the page is skipped (the eligibility line was fixed in v2.65.31).
// v1.2.0 · 2026-10-16 · Assigned-rule support: per-case rule (__rule) and source-trade cache, getMaxFrames stub, and named source variants (e.g. the page as written vs with the one-line eligibility patch).
// v1.1.0 · 2026-10-16 · Datasets sent once and referenced by cases ($ds / $longest), so large parameter grids stay small.
// v1.0.0 · 2026-10-16 · Initial version: loads named functions from the page snapshot, applies per-case globals, returns JSON results.
// Usage: node js_runner.js <cases.json>
//   spec = {page, inventory, functions:[names], extra, datasets, variants:{name:[[old,new],...]}, cases:[{id, variant, globals, tradeCache, call, args}]}
'use strict';
const fs = require('fs');
const vm = require('vm');

const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const pageLines = fs.readFileSync(spec.page, 'utf8').split(/\r?\n/);
const inv = JSON.parse(fs.readFileSync(spec.inventory, 'utf8'));

const byName = new Map();
for (const f of inv.functions) byName.set(f.name, f); // later duplicate wins, like the page
let baseSrc = '';
for (const name of spec.functions) {
  const f = byName.get(name);
  if (!f) throw new Error('function not in inventory: ' + name);
  baseSrc += pageLines.slice(f.start_line - 1, f.end_line).join('\n') + '\n';
}

// Defaults copied from the page's top-level state declarations (lines 1639-1751 of v2.65.24).
const defaults = { currentReturnType: 'NET', baselineFrameIndex: 0, currentFrameIndex: -1, exitThreshold: 0,
  overlayTopX: 1, dailyTarget: 500, activePortfolioName: null, splitMode: 'ALL_NET', __rule: null, __maxFrames: 1,
  currentDate: '', currentProductType: 'forex', currentProduct: 'all', LIVE_DATE: '2099-01-01', PORTFOLIO_VIEW_REFRESH_MS: 300000,
  SCENARIOS_CATALOGUE: [], ALL_CRITERIA_DATA: {}, strategyCatalogue: [], portfolioModels: [], selectedTimeRankSelect: { value: '1' },
  portfolioScenarioConfigs: {}, portfolioCriteria: {}, currentCriteria: 'top_net', currentStrategyFamily: 'all', modelLimit: 10,
  minWinRate: 0, autoRefreshTop1Enabled: false, autoRefreshTop1Direction: 'top', autoRefreshTop1Rank: 1, availableDates: [],
  modelSearchInput: undefined, pointInTimeMode: false, pointInTimeModels: [], modelSearchLoadedModels: [], __candidates: [],
  autoRefreshTop1RequestAt: null, pendingExplicitTop1Time: null, selectedTimeExplicitRefresh: false, autoRefreshTop1NextMinute: null,
  autoRefreshTop1Minutes: 15, __head: null, __status: null, __sched: null, mainScenarioCriteria: 'top_net', visibleModels: new Set(), returnTypeNetBtn: {}, returnTypeAltBtn: {} };

function makeContext(patches) {
  let src = baseSrc;
  for (const [oldText, newText] of patches || []) {
    if (!src.includes(oldText)) {
      if (src.includes(newText)) continue; // already fixed in the page itself: nothing to patch
      throw new Error('patch target not found: ' + oldText.slice(0, 60));
    }
    src = src.replace(oldText, newText);
  }
  const ctx = vm.createContext({ console: process.env.DIFF_JS_REJECTIONS ? { log() {}, warn: (...a) => require("fs").appendFileSync(process.env.DIFF_JS_REJECTIONS, "WARN: " + a.map(x => (x && x.stack ? x.stack.split("\n").slice(0, 3).join(" | ") : String(x))).join(" ") + "\n"), error: (...a) => require("fs").appendFileSync(process.env.DIFF_JS_REJECTIONS, "ERR: " + a.join(" ") + "\n") } : console, Math, Number, String, Map, Set, Array, JSON, Infinity, Date, URL, URLSearchParams, __imm: setImmediate });
  Object.assign(ctx, defaults, { assignedOverlayTradeCache: new Map() });
  // Stubs for browser-only collaborators: the assigned rule is a per-case global, max frames is supplied by the case.
  vm.runInContext('const __noop = () => {}; var pauseReplay = __noop, updateScrubberUI = __noop, updateRibbon = __noop, renderCards = __noop, drawChart = __noop, schedulePointInTimeSelection = __noop, persistPortfolioViewConfig = __noop, syncSplitModeControls = __noop, updateScenarioUI = __noop, updateDateLabelAndTitle = __noop, saveCriteriaWorkspaces = __noop, getEligibleModels = () => []; var localStorage = { setItem: __noop, getItem: () => null }; var refreshLiveData = () => Promise.resolve(); '
    + 'function updateAutoRefreshTop1Status(m){ __status = m; } function pointInTimeAtReplayHead(){ return __head; } '
    + 'function scheduleAutomaticTop1Refresh(h){ __sched = h; } function getScenarioCandidates(){ return __candidates; } '
    + 'var window = { setTimeout: fn => fn() };', ctx);
  vm.runInContext('function activePortfolioOverlayRule(){return __rule;} function assignedPortfolioOverlayRule(){return __rule;} function getMaxFrames(){return __maxFrames;}', ctx);
  vm.runInContext(src, ctx, { filename: 'page_functions.js' });
  if (spec.extra) vm.runInContext(spec.extra, ctx);
  return ctx;
}
const contexts = new Map();
const ctxFor = name => {
  const key = name || 'asis';
  if (!contexts.has(key)) contexts.set(key, makeContext((spec.variants || {})[key]));
  return contexts.get(key);
};

// Datasets are sent once; cases reference them as {"$ds": name} (the models) or {"$longest": name} (their longest series).
const datasets = spec.datasets || {};
const longestOf = models => models.reduce((max, m) => (m.series.length > max.series.length ? m : max), models[0]).series;
const resolve = a => Array.isArray(a) ? a.map(resolve)
  : (a && typeof a === 'object' && a.$ds !== undefined) ? datasets[a.$ds]
  : (a && typeof a === 'object' && a.$longest !== undefined) ? longestOf(datasets[a.$longest]) : a;

const out = [];
(async () => {
for (const c of spec.cases) {
  const ctx = ctxFor(c.variant);
  Object.assign(ctx, defaults, c.globals || {});
  ctx.assignedOverlayTradeCache = new Map(Object.entries(c.tradeCache ? resolve(c.tradeCache) : {}));
  ctx.__args = resolve(c.args);
  try {
    const value = await vm.runInContext(`${c.call}(...__args)`, ctx);
    const res = JSON.stringify(value);
    out.push({ id: c.id, ok: true, result: JSON.parse(res === undefined ? 'null' : res) });
  } catch (e) {
    out.push({ id: c.id, ok: false, error: String(e && e.message || e) });
  }
}
process.stdout.write(JSON.stringify(out));
})();
