# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/diff_js_vs_py.py — differential test: the page's real JS functions (Node) vs the Python engine, on real API data.
#
# VERSION HISTORY
# v1.21.0 · 2026-10-17 · main() runs only when executed as a script, so the data / rule fixtures can be imported (tools/diff_thin_js_vs_py.py).
# v1.20.1 · 2026-10-17 · __pload captures portfolioModels at request time (mid); fetch cases without a portfolio name.
# v1.20.0 · 2026-10-17 · data_portfolio uses the page's real rememberPortfolioView / getLastPortfolioView (in-memory last-view cache), with last-view seeds and the cache in the compared state.
# v1.19.0 · 2026-10-17 · data_pitsel: mid-request status capture, boundary frame, explicit refresh pending at another time, identical-request early return, removed history entries, palette-coloured leaders, leaders with own join / selection times, empty series; 1,400 sampled combinations. (Added after 16 of 64 mutants survived.)
# v1.18.3 · 2026-10-17 · Removed the no-op refreshPointInTimeSelection stub that shadowed the real page function.
# v1.18.2 · 2026-10-17 · DIFF_DEBUG_ID=<case id> prints one case's JS and Python results.
# v1.18.1 · 2026-10-17 · __elig (state) no longer collides with the __eligible wrapper function.
# v1.18.0 · 2026-10-17 · data_pitsel: the page's refreshPointInTimeSelection vs selected_time.refresh_point_in_time_selection (640 sampled combinations of mode, payload, rank settings, history, pinned / searched models, criteria, portfolio, frame, plus early exits).
# v1.17.2 · 2026-10-17 · Data cases run first: their 'now'-relative fixture timestamps went stale (>2 min) during the ~20 min of rule cases in full runs, producing false cachedAt mismatches.
# v1.17.1 · 2026-10-17 · Renamed the rule-library wrapper (__rulelib): it shadowed the overlay-signals wrapper __overlay.
# v1.17.0 · 2026-10-17 · Data groups compare key sets both ways; special-character inputs; per-batch generated_at; reordered search responses; stale cached trades; failing loads are results, not crashes. (Added after the first mutation run left 11 data-client mutants alive.)
# v1.16.1 · 2026-10-17 · Dropped the model-key-with-empty-id case from the fetch group (it trips the page's switched-away guard, which the sequential client does not model).
# v1.16.0 · 2026-10-17 · data_* groups: DataClient vs the page's refreshLiveData / fetchPortfolioData / loadPortfolioData / loadModelSearchFromDatabase / loadDeepLinkModelsFromDatabase / loadStrategyCatalogue / loadOverlayRuleLibrary / ensureAssignedOverlayTradeData / ensureHistoricalDataLoaded on a recording fetch stub.
# v1.15.0 · 2026-10-17 · utils_auto (finishAutomaticTop1Refresh state machine) and utils_search (getExactSearchModel) groups.
# v1.14.2 · 2026-10-17 · Strengthened helper tests after mutation testing showed 6 alive mutants (top3_ prefix ids, model_limit below the rank count, retain: joined_at precedence, colours in use by history-only models, palette wrap, empty selectedAtEntries).
# v1.14.1 · 2026-10-17 · --utils-only (no API calls) for fast mutation checks of the small helpers.
# v1.14.0 · 2026-10-17 · utils_* groups: clock / search / rule summary / request options / retainSelectedTimeLeaders / tradeDateRange / step / seek / split / return-type helpers vs the page JS (always run; fast).
# v1.13.0 · 2026-10-16 · Node cases run on parallel workers (DIFF_WORKERS) with a 2 h timeout; the single 10-minute subprocess timed out on the full grid.
# v1.12.0 · 2026-10-16 · rule_as_written runs only while the page still has the buggy eligibility line (fixed in v2.65.31); the patched-page oracle becomes a no-op on a fixed page.
# v1.11.0 · 2026-10-16 · engine_rule group (Engine class with an assigned rule vs the patched page JS); --skip-rules for the fast tier.
# v1.10.0 · 2026-10-16 · Noisy correlated / anti-correlated copies (graded correlations) and mid-day open source trades, after round 2 showed the 0.5 / -0.5 thresholds and the latest-head rule were still unexercised.
# v1.9.0 · 2026-10-16 · Dense synthetic source trades (closes inside snapshot minutes, open trades), head-frame variants and a partial-cache group, added after the second mutation run showed boundary / latest-head / loading branches were not exercised.
# v1.8.0 · 2026-10-16 · Synthetic-data rule groups (rule_syn_*): mirrored negatively correlated models and mixed strategy families, so the similar / opposite / family-prefix branches are exercised (the first mutation run showed real data never reached them).
# v1.7.0 · 2026-10-16 · --only-rules: run only the assigned-rule groups for the named rules (fast, targeted mutation checks).
# v1.6.0 · 2026-10-16 · Assigned overlay-rule groups (7 rules x leader/multi-split x baseline x NET/ALT x head, loading-cache, as-written page) with source trades from /api/model_trades; patched-page oracle.
# v1.5.0 · 2026-10-16 · Adds engine_rotation and engine_overlay groups: the Engine class (not just core functions) against the page JS.
# v1.4.0 · 2026-10-16 · Proper argument parsing (--base value was being read as the page path); --inventory to test any page snapshot.
# v1.3.0 · 2026-10-16 · Adds extended rotation grid (rank hold 1-3, NET/ALT, selected-time late-joining models); datasets sent once.
# v1.2.0 · 2026-10-16 · Passes the longest series as replay_series to the Python rotation functions (as the page does).
# v1.1.0 · 2026-10-16 · Adds --breakdown (pass/fail by baseline, exit threshold, target, replay head for the rotation groups).
# v1.0.1 · 2026-10-16 · Decode Node output as UTF-8 (cp1252 default garbled the middle dot and caused false text mismatches).
# v1.0.0 · 2026-10-16 · Initial version: metric keys, overlay signals/trades/target, leader rotation, multi-split rotation over 3 dates x top-10 models x parameter grid.
"""Usage: python diff_js_vs_py.py [page_snapshot.html] [--base http://127.0.0.1:8765]. Exit 1 if any case differs.
Every key present in the Python output must equal the JS value; JS-only keys are reported (information, not failure)."""
import copy
from collections import OrderedDict
from datetime import datetime
import os
import random
import json
import subprocess
import sys
import tempfile
import urllib.request
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import Engine, EngineSpec  # noqa: E402
from engine import core_ported as core  # noqa: E402
from engine.core_ported import RuleContext  # noqa: E402
from engine import page_utils as pu  # noqa: E402
from engine import data_client as dc  # noqa: E402
from engine import selected_time as stm  # noqa: E402

import argparse  # noqa: E402

_ap = argparse.ArgumentParser()
_ap.add_argument("page", nargs="?", default=str(ROOT / "top10_5min_equity_curves_source_v2.65.24.html"))
_ap.add_argument("--inventory", default=str(ROOT / "inventory" / "inventory.json"), help="inventory.json built from the same page file")
_ap.add_argument("--base", default="http://127.0.0.1:8765")
_ap.add_argument("--breakdown", action="store_true")
_ap.add_argument("--utils-only", action="store_true", help="only the small-helper groups (no API calls; seconds)")
_ap.add_argument("--skip-rules", action="store_true", help="skip every assigned-rule group (fast tier; the rule groups take ~30 min)")
_ap.add_argument("--only-rules", default="", help="comma list of RULES keys: run ONLY the assigned-rule groups for these rules (fast mutation checks)")
_ns = _ap.parse_args()
PAGE, INVENTORY, BASE = Path(_ns.page), Path(_ns.inventory), _ns.base
_ONLY_RULES = set(x for x in _ns.only_rules.split(",") if x) or None
DATES = ["2026-10-14", "2026-10-13", "2026-10-12"]
TOL = 1e-9


def get(path):
    return json.load(urllib.request.urlopen(BASE + path, timeout=90))


def load_models(date):
    pit = get(f"/api/point_in_time_scenario?date={date}&at=23%3A55&scenario=top_net&return_type=NET&product_type=forex"
              "&product=all&strategy_family=all&limit=10&min_win_rate=0&rank_direction=top")
    ids = [m["model"] for m in pit["models"]][:10]
    return get(f"/api/portfolio_day?models={','.join(ids)}&date={date}")["models"]


def mapped(model, rt):
    return core.mapped_series(model, rt)


JS_EXTRA = """
function __overlay(series){ const base=getBasePoint(series); const s=computeTradeOverlaySignals(series, base);
  const t=pairOverlayTrades(s, series, base); const g=computeSplitTargetSignal(s, series, base); return {signals:s, trades:t, target:g}; }
function __strip(r){ return {signals:r.signals, trades:r.trades.map(t=>{const {curveModel, ...x}=t; return x;}), threshold:r.threshold, targetSignal:r.targetSignal}; }
function __leader(models, mk, up, rs){ return __strip(computeLeaderRotation(models, mk, up, rs)); }
function __multi(models, up, rs){ return __strip(computeMultiSplitRotation(models, getMetricKeys(), up, rs)); }
function __keys(){ return getMetricKeys(); }
function __step(delta){ step(delta); return currentFrameIndex; }
function __seek(pct){ seekToPct(pct); return currentFrameIndex; }
function __split(mode){ setSplitMode(mode); return splitMode; }
function __retype(type){ setReturnType(type); return { currentReturnType, currentCriteria }; }
function __pit(){ return pointInTimeRequestOptions(); }
function __pitkey(){ return pointInTimeContextKey(); }
function __eligible(model, point){ return selectedTimePointEligible(model, point); }
function __retain(pinned, search, history, leaders, at){ globalThis.pinnedComparisonModels = new Map(pinned.map(m => [m.model, m]));
  globalThis.modelSearchLoadedModels = search; globalThis.selectedTimeLeaderHistory = new Map(history);
  retainSelectedTimeLeaders(leaders, at); return [...selectedTimeLeaderHistory.entries()]; }
function __short(id){ return shortStrategyDescription(id); }
function __rank(){ return selectedTimeRankCount(); }
function __finish(at, message){ globalThis.__status = null; globalThis.__sched = null;
  finishAutomaticTop1Refresh(...(message === undefined ? [at] : [at, message]));
  return { status: __status, sched: __sched, requestAt: autoRefreshTop1RequestAt, pending: pendingExplicitTop1Time,
           explicit: selectedTimeExplicitRefresh, nextMinute: autoRefreshTop1NextMinute }; }
function __exact(){ return getExactSearchModel(); }
// ---- data layer: the page's own fetchers run against a recording fetch() stub ----
globalThis.API_BASE = 'http://api';
globalThis.location = { href: 'http://h/p/page.html', protocol: 'http:', origin: 'http://h' };
var liveRefreshSequence = 0, liveChartDataLoadedKeys = new Set(), productFilter = { innerHTML: '', value: '' }, TP_SL_SCENARIO_IDS = new Set(),
  initialLiveDataAvailable = false, pendingFilterDataRefresh = false, isPlaying = false, __badge = null, __calls = [],
  PORTFOLIO_VIEW_CACHE = new Map(), PORTFOLIO_VIEW_REQUESTS = new Map(), PORTFOLIO_VIEW_CACHE_MAX = 32, portfolios = {},
  modelSearchRequestSequence = 0, modelSearchStatus = { textContent: '' }, scenarioRemovedModels = new Set(), selectedModelIndex = 0,
  pinnedComparisonModels = new Map(), deepLinkModelsOnly = false, strategyCatalogueDate = null,
  strategyCatalogueResults = { innerHTML: '', textContent: '' }, overlayRuleLibrary = { rules: [], assignments: {} }, overlayRuleLibraryRequest = null,
  assignedOverlayTradeRequests = new Map(), historicalCurveLoads = new Map();
function setLiveBadge(t, k){ __badge = [t, k]; } function liveChartCacheKey(){ return 'k'; } function cacheLiveChartResponse(){}
function updateStrategyFamilyOptions(){} function syncLivePortfolioScreenState(){ return false; } function isLiveModeArmed(){ return false; }
function persistPortfolioView(){} function autoPinLivePortfolioStrategies(){}
var PORTFOLIO_LAST_VIEW_CACHE = new Map(), PORTFOLIO_VIEW_CACHE_STORAGE_KEY = 'pv', persistedPortfolioViewCache = null;
function renderStrategyCatalogue(){} function renderPortfolioList(){}
function __fetchStub(fx){ __calls = [];
  globalThis.fetch = async (url) => { const u = String(url); __calls.push(u);
    try { globalThis.__mid = [pointInTimeStatus.textContent, pointInTimeStatus.className]; } catch (e) {}
    try { if (globalThis.__midPM === undefined || globalThis.__midPM === null) globalThis.__midPM = JSON.parse(JSON.stringify(portfolioModels)); } catch (e) {} const r = fx[u] || { status: 404, payload: { error: 'not found' } };
    return { ok: r.status >= 200 && r.status < 300, status: r.status, json: async () => r.payload }; }; }
var __timers = [];
function __lv(){ return [...PORTFOLIO_LAST_VIEW_CACHE.entries()].map(([k, v]) => [k, { modelKey: v.modelKey, entry: { models: v.entry.models, cachedAt: Math.abs(v.entry.cachedAt - Date.now()) < 120000 ? 'NOW' : v.entry.cachedAt } }]); }
async function __drain(){ for (let i = 0; i < 60; i++) await null; while (__timers.length) { __timers.shift()(); for (let i = 0; i < 60; i++) await null; } }
function __norm(entries){ return entries.map(([k, v]) => [k, { models: v.models, cachedAt: Math.abs(v.cachedAt - Date.now()) < 120000 ? 'NOW' : v.cachedAt }]); }
async function __live(fx, targetDate){ __fetchStub(fx); globalThis.ALL_CRITERIA_DATA = {}; TP_SL_SCENARIO_IDS.clear(); __badge = null;
  await refreshLiveData(targetDate); return { calls: __calls, criteria: ALL_CRITERIA_DATA, product: currentProduct, tpSl: [...TP_SL_SCENARIO_IDS], badge: __badge && __badge[1] === 'err' ? __badge : null }; }
async function __pfetch(fx, key, date, modelKey, background, seed, pname){ __fetchStub(fx); PORTFOLIO_VIEW_CACHE = new Map(seed || []); PORTFOLIO_VIEW_REQUESTS = new Map(); PORTFOLIO_LAST_VIEW_CACHE = new Map();
  portfolios = { P: modelKey.split(',').filter(Boolean) }; activePortfolioName = 'P'; currentDate = date;
  __timers = []; window.setTimeout = fn => { __timers.push(fn); };
  try { await fetchPortfolioData(key, date, modelKey, pname === undefined ? 'P' : pname, background); await __drain(); } catch (e) { window.setTimeout = fn => fn(); return { calls: __calls, error: String(e.message) }; }
  window.setTimeout = fn => fn(); return { calls: __calls, cache: __norm([...PORTFOLIO_VIEW_CACHE.entries()]), lastView: __lv() }; }
async function __pload(fx, models, date, preferCache, seed, lastSeed){ __fetchStub(fx); globalThis.__midPM = null; PORTFOLIO_VIEW_CACHE = new Map(seed || []); PORTFOLIO_VIEW_REQUESTS = new Map(); PORTFOLIO_LAST_VIEW_CACHE = new Map((lastSeed || []).map(([k, v]) => [k, { modelKey: v.modelKey, entry: v.entry }]));
  portfolios = { P: models }; activePortfolioName = 'P'; currentDate = date; portfolioModels = [];
  __timers = []; window.setTimeout = fn => { __timers.push(fn); };
  let r; try { r = await loadPortfolioData({ preferCache }); await __drain(); } catch (e) { window.setTimeout = fn => fn(); return { calls: __calls, error: String(e.message) }; }
  window.setTimeout = fn => fn(); return { calls: __calls, cache: __norm([...PORTFOLIO_VIEW_CACHE.entries()]), lastView: __lv(), models: portfolioModels, fetched: r, mid: __midPM }; }
async function __search(fx, term, date){ __fetchStub(fx); currentDate = date; modelSearchLoadedModels = []; modelSearchStatus.textContent = '';
  modelSearchInput = { value: term === null ? '' : term }; modelSearchRequestSequence = 0; pointInTimeMode = false;
  await loadModelSearchFromDatabase(term); return { calls: __calls, loaded: modelSearchLoadedModels, status: modelSearchStatus.textContent }; }
async function __deeplink(fx, ids, date, only){ __fetchStub(fx); currentDate = date; pinnedComparisonModels = new Map(); modelSearchStatus.textContent = '';
  deepLinkModelsOnly = only; pointInTimeMode = false; await loadDeepLinkModelsFromDatabase(ids);
  return { calls: __calls, pinned: [...pinnedComparisonModels.entries()], status: modelSearchStatus.textContent }; }
async function __catalog(fx, date, seedCat, seedDate){ __fetchStub(fx); currentDate = date; strategyCatalogue = seedCat; strategyCatalogueDate = seedDate;
  strategyCatalogueResults = { innerHTML: '', textContent: '' }; await loadStrategyCatalogue();
  return { calls: __calls, catalogue: strategyCatalogue, date: strategyCatalogueDate, text: strategyCatalogueResults.textContent }; }
var pointInTimeRequestSequence = 0, __elig = [], autoRefreshTop1DirectionSelect = { value: 'top' }, autoRefreshTop1RankSelect = { value: '1' },
  selectedTimeInput = { value: '' }, applySelectedTimeBtn = null, pointInTimeStatus = { textContent: '', className: '' }, pointInTimeHistoryAt = '',
  selectedTimeLeaderHistory = new Map(), selectedTimeLeaderHistoryContext = '', pointInTimeTimelineModels = [], pointInTimeModels = [];
function getEligibleModels(){ return __elig; } function updatePointInTimeToggleUI(){} function renderPointInTimeHistory(){}
async function __pitsel(fx, c, atOverride){
  __fetchStub(fx);
  pointInTimeMode = c.mode; currentDate = c.date; currentCriteria = c.criteria; activePortfolioName = c.active;
  portfolioScenarioConfigs = c.configs; portfolioCriteria = c.pcrit; currentReturnType = c.rt; currentProductType = c.ptype; currentProduct = c.product;
  currentStrategyFamily = c.fam; modelLimit = c.limit; minWinRate = c.mwr; selectedTimeRankSelect = { value: c.rankValue };
  autoRefreshTop1DirectionSelect = { value: c.autoDir }; autoRefreshTop1RankSelect = { value: c.autoRankValue };
  autoRefreshTop1Enabled = c.autoEnabled; autoRefreshTop1RequestAt = c.reqAt; pendingExplicitTop1Time = c.pending;
  selectedTimeExplicitRefresh = c.explicit; autoRefreshTop1NextMinute = c.nextMinute; autoRefreshTop1Minutes = c.interval;
  pointInTimeModels = c.models; pointInTimeTimelineModels = c.timeline; pointInTimeRequestedKey = c.requestedKey; pointInTimeRequestSequence = 0;
  pinnedComparisonModels = new Map(c.pinned); modelSearchLoadedModels = c.search; selectedTimeLeaderHistory = new Map(c.history);
  selectedTimeLeaderHistoryContext = c.historyContext; scenarioRemovedModels = new Set(c.removed);
  SCENARIOS_CATALOGUE = c.names.map(([id, name]) => ({ id, name }));
  pointInTimeStatus = { textContent: '', className: '' }; selectedTimeInput = { value: '' }; selectedModelIndex = 0; visibleModels = new Set();
  pointInTimeHistoryAt = ''; currentFrameIndex = c.frame; globalThis.__maxFrames = c.maxFrames; globalThis.__head = c.head; __elig = c.eligible;
  globalThis.__status = null; globalThis.__sched = null; globalThis.__mid = null;
  await refreshPointInTimeSelection(atOverride);
  return { calls: __calls, models: pointInTimeModels, timeline: pointInTimeTimelineModels, requestedKey: pointInTimeRequestedKey,
    history: [...selectedTimeLeaderHistory.entries()], historyContext: selectedTimeLeaderHistoryContext, removed: [...scenarioRemovedModels].sort(),
    status: pointInTimeStatus.textContent, statusClass: pointInTimeStatus.className, historyAt: pointInTimeHistoryAt,
    visible: [...visibleModels].map(String).sort(), frame: currentFrameIndex, reqAt: autoRefreshTop1RequestAt, pending: pendingExplicitTop1Time,
    explicit: selectedTimeExplicitRefresh, nextMinute: autoRefreshTop1NextMinute, autoStatus: __status, sched: __sched,
    input: selectedTimeInput.value, selIdx: selectedModelIndex, mid: __mid }; }
async function __rulelib(fx, seed){ __fetchStub(fx); overlayRuleLibrary = seed; overlayRuleLibraryRequest = null; await loadOverlayRuleLibrary(); return { calls: __calls, library: overlayRuleLibrary }; }
async function __trades(fx, models, date, ptype, product, seed){ __fetchStub(fx); currentDate = date; currentProductType = ptype; currentProduct = product; activePortfolioName = null;
  assignedOverlayTradeCache = new Map(seed || []); assignedOverlayTradeRequests = new Map(); await ensureAssignedOverlayTradeData(models.map(m => ({ model: m })));
  return { calls: __calls, cache: [...assignedOverlayTradeCache.entries()].map(([k, v]) => [k, { rows: v.rows, cachedAt: Math.abs(v.cachedAt - Date.now()) < 120000 ? 'NOW' : v.cachedAt }]) }; }
async function __hist(fx, dateKey, buckets){ __fetchStub(fx); globalThis.ALL_CRITERIA_DATA = buckets; historicalCurveLoads = new Map();
  try { await ensureHistoricalDataLoaded(dateKey); } catch (e) { return { calls: __calls, error: String(e.message), criteria: ALL_CRITERIA_DATA }; }
  return { calls: __calls, criteria: ALL_CRITERIA_DATA }; }
"""
FUNCS = ["rememberPortfolioView", "getLastPortfolioView", "getPersistedPortfolioViewCache", "refreshPointInTimeSelection", "refreshLiveData", "fetchPortfolioData", "loadPortfolioData", "loadModelSearchFromDatabase", "loadDeepLinkModelsFromDatabase",
         "loadStrategyCatalogue", "loadOverlayRuleLibrary", "ensureAssignedOverlayTradeData", "ensureHistoricalDataLoaded", "syncTpSlScenarios",
         "finishAutomaticTop1Refresh", "getExactSearchModel", "clockMinutes", "replayClockTime", "nextAutomaticTop1Minute", "selectedTimePointEligible", "modelSearchTerms",
         "overlayRuleSummary", "isMetricAwareCriteria", "shortStrategyDescription", "getSelectedTimeNoteEntries", "selectedTimeRankCount",
         "portfolioScenarioConfig", "pointInTimeRequestOptions", "pointInTimeContextKey", "retainSelectedTimeLeaders", "tradeDateRange",
         "step", "seekToPct", "setSplitMode", "setReturnType", "overlayRuleMetricValue", "overlayRuleCandidate", "asOfCorrelation", "timeOfDayMinutes", "curvePointAtOrBefore",
         "sourceTradeFlipResults", "assignedOverlayTradeCacheKey", "applyAssignedOverlayTradeResults", "assignedRuleTarget",
         "getStrategyFamily", "getMetricKeys", "getBasePoint", "getReplayHeadPoint", "computeTradeOverlaySignals", "pairOverlayTrades",
         "computeSplitTargetSignal", "modelPointAtOrBeforeTime", "selectedTimeJoinAt", "selectedTimeModelEligibleAt",
         "applyAssignedOverlayTradeResults", "assignedRuleTarget", "computeLeaderRotation", "computeMultiSplitRotation"]


PAGE_TEXT = PAGE.read_text(encoding="utf-8").replace("\r\n", "\n")
ELIGIBLE_OLD = "if (config.trade_side === 'sell' && item.side && item.side !== 'sell') return false;\n        return false;"
ELIGIBLE_NEW = "if (config.trade_side === 'sell' && item.side && item.side !== 'sell') return false;\n        return true;"
RULES = {
    "top30": {"interval_minutes": 30, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
              "rules": [{"type": "ranked_top", "metric": "cum_net"}]},
    "bottom15": {"interval_minutes": 15, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                 "rules": [{"type": "ranked_bottom", "metric": "cum_net"}]},
    "group_buy": {"interval_minutes": 60, "hold_rank": 1, "trade_side": "buy", "eligibility_filters": ["cum_net_positive"],
                  "rules": [{"type": "group_ranked_top", "group": "family:breakout", "metric": "net"},
                            {"type": "ranked_top", "metric": "cum_net"}]},
    "similar": {"interval_minutes": 30, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                "rules": [{"type": "similar_higher_net"}, {"type": "ranked_top", "metric": "cum_net"}]},
    "opposite": {"interval_minutes": 30, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                 "rules": [{"type": "opposite_top", "metric": "cum_net"}, {"type": "ranked_top", "metric": "cum_net"}]},
    "winrate": {"interval_minutes": 45, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                "rules": [{"type": "better_win_rate"}, {"type": "ranked_top", "metric": "cum_net"}]},
    "sell_alt": {"interval_minutes": 30, "hold_rank": 2, "exit_threshold": 25, "trade_side": "sell",
                 "eligibility_filters": ["cum_alt_net_positive"], "rules": [{"type": "ranked_top", "metric": "cum_alt_net"}]},
}


RULES_SYN = {  # need synthetic data: negatively correlated curves and mixed strategy families
    "similar_hi": {"interval_minutes": 15, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                   "rules": [{"type": "similar_higher_net"}, {"type": "ranked_bottom", "metric": "cum_net"}]},
    "similar_lo": {"interval_minutes": 15, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                   "rules": [{"type": "similar_lower_net"}, {"type": "ranked_top", "metric": "cum_net"}]},
    "opposite_top": {"interval_minutes": 15, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                     "rules": [{"type": "opposite_top", "metric": "cum_net"}, {"type": "ranked_top", "metric": "cum_net"}]},
    "opposite_bot": {"interval_minutes": 15, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                     "rules": [{"type": "opposite_bottom", "metric": "cum_net"}, {"type": "ranked_top", "metric": "cum_net"}]},
    "family_prefix": {"interval_minutes": 15, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                      "rules": [{"type": "group_ranked_top", "group": "family:breakout", "metric": "net"}]},
    "family_bottom": {"interval_minutes": 15, "hold_rank": 1, "trade_side": "both", "eligibility_filters": [],
                      "rules": [{"type": "group_ranked_bottom", "group": "family:breakout", "metric": "net"}]},
}


def make_rows(model, date):
    """Dense synthetic source trades in the API's row format. Many closes land inside a snapshot minute (so exit-minute
    boundaries matter), the last two rows are still open, and signals alternate buy/sell. Deterministic per model."""
    rng = random.Random(f"{model['model']}|{date}")
    times = [pt["time"] for pt in model["series"]]
    rows = []

    def stamp(t, sec):
        return f"{date} {t[:5]}:{sec:02d}"

    def plus(t, minutes):
        h, m = int(t[:2]), int(t[3:5])
        total = min(23 * 60 + 59, h * 60 + m + minutes)
        return f"{total // 60:02d}:{total % 60:02d}"

    for i in range(0, max(1, len(times) - 3), 2):
        t0 = times[i]
        dur = rng.choice([0, 5, 10, 15, 25, 40, 70])
        t1 = times[min(len(times) - 1, i + dur // 5)] if rng.random() < 0.6 else plus(t0, dur)
        rows.append({"status": "closed", "opened": stamp(t0, rng.choice([0, 12, 30, 47])), "last_update": stamp(t1, rng.choice([0, 20, 33, 59])),
                     "signal": rng.choice(["buy", "sell"]), "net_return": round(rng.uniform(-60, 80), 2),
                     "alt_net_return": round(rng.uniform(-60, 80), 2), "strategy": model.get("strategy"), "product": model.get("product")})
    for j in range(10, max(11, len(times) - 3), 25):  # open trades that stopped updating mid-day
        rows.append({"status": "open", "opened": stamp(times[j], 5), "last_update": stamp(times[min(len(times) - 1, j + 3)], 40),
                     "signal": rng.choice(["buy", "sell"]), "net_return": round(rng.uniform(-40, 60), 2),
                     "alt_net_return": round(rng.uniform(-40, 60), 2), "strategy": model.get("strategy"), "product": model.get("product")})
    for t0 in times[-3:-1]:
        rows.append({"status": "open", "opened": stamp(t0, 5), "last_update": stamp(times[-1], 40), "signal": rng.choice(["buy", "sell"]),
                     "net_return": round(rng.uniform(-40, 60), 2), "alt_net_return": round(rng.uniform(-40, 60), 2),
                     "strategy": model.get("strategy"), "product": model.get("product")})
    return rows


def synth(models):
    """Real curves plus (a) strategy families cycled through breakout / breakout_r / breakout_rev / breakout_r_rev / other and
    (b) three mirrored models whose curves are the negation of real ones (guaranteed strongly negative correlation)."""
    ms = copy.deepcopy(models)
    fam = ["breakout", "breakout_r", "breakout_rev", "breakout_r_rev", "other"]
    for i, m in enumerate(ms):
        m["strategy"] = fam[i % len(fam)]
    for k, src in enumerate(models[:3]):
        mir = copy.deepcopy(src)
        mir["model"], mir["strategy"] = f"MIR_{k}", fam[(k + 1) % len(fam)]
        for key in ("cum_net", "buy_net", "sell_net", "cum_alt_net", "buy_alt_net", "sell_alt_net"):
            if mir.get(key) is not None:
                mir[key] = -mir[key]
        for pt in mir["series"]:
            for key in ("net", "buy", "sell", "alt_net", "alt_buy", "alt_sell"):
                if pt.get(key) is not None:
                    pt[key] = -pt[key]
        ms.append(mir)
    noise = random.Random("noise")
    keys6 = ("net", "buy", "sell", "alt_net", "alt_buy", "alt_sell")
    for k, src in enumerate(models[:3]):
        for sign, tag in ((1, "NZP"), (-1, "NZN")):
            nm = copy.deepcopy(src)
            nm["model"], nm["strategy"] = f"{tag}_{k}", fam[(k + 2) % len(fam)]
            level = 0.6 + 0.7 * k
            for key in keys6:
                vals = [pt.get(key) or 0 for pt in src["series"]]
                incs = [b - a for a, b in zip(vals, vals[1:])] or [1]
                std = (sum(i * i for i in incs) / len(incs)) ** 0.5 or 1.0
                walk = 0.0
                for j, pt in enumerate(nm["series"]):
                    walk += noise.gauss(0, level * std)
                    pt[key] = round(sign * vals[j] + walk, 2)
            last = nm["series"][-1]
            nm.update(cum_net=last["net"], buy_net=last["buy"], sell_net=last["sell"], cum_alt_net=last["alt_net"],
                      buy_alt_net=last["alt_buy"], sell_alt_net=last["alt_sell"])
            ms.append(nm)
    return ms


STRICT = False  # data_* groups compare key sets both ways (the default only checks the Python keys against JS)


def diff(py, js, path="", extra=None):
    """First difference of every Python key against JS, or None."""
    if isinstance(py, dict):
        if not isinstance(js, dict):
            return f"{path}: py dict vs js {type(js).__name__}"
        if STRICT and set(py) != set(js):
            return f"{path}: keys differ, py-only {sorted(set(py) - set(js))} js-only {sorted(set(js) - set(py))}"
        for k, v in py.items():
            if k not in js:
                return f"{path}.{k}: missing in JS"
            d = diff(v, js[k], f"{path}.{k}", extra)
            if d:
                return d
        if extra is not None:
            extra.update(set(js) - set(py))
        return None
    if isinstance(py, list):
        if not isinstance(js, list) or len(py) != len(js):
            return f"{path}: length py {len(py)} vs js {len(js) if isinstance(js, list) else js!r}"
        for i, (a, b) in enumerate(zip(py, js)):
            d = diff(a, b, f"{path}[{i}]", extra)
            if d:
                return d
        return None
    if isinstance(py, (int, float)) and isinstance(js, (int, float)) and not isinstance(py, bool):
        return None if abs(py - js) <= TOL else f"{path}: py {py} vs js {js}"
    return None if py == js else f"{path}: py {py!r} vs js {js!r}"


def main():
    data = {} if _ns.utils_only else {d: load_models(d) for d in DATES}
    rule_data = {} if _ns.skip_rules else data
    datasets = dict(data)
    for d, ms in data.items():  # variant where models 1 and 2 are selected-time ranks that join late
        sel = copy.deepcopy(ms)
        for i, joined in ((1, "10:00"), (2, "18:30")):
            if i < len(sel):
                sel[i]["comparisonRole"] = f"selected-time #{i}"
                sel[i]["joined_at"] = joined
        datasets[d + "|sel"] = sel
    cases, py_out = [], {}
    cid = 0

    def add(group, call, globals_, a, py, variant=None, trade_cache=None):
        nonlocal cid
        cid += 1
        if _ONLY_RULES is not None and not group.startswith("rule_"):
            return
        case = {"id": cid, "globals": globals_, "call": call, "args": a}
        if variant:
            case["variant"] = variant
        if trade_cache:
            case["tradeCache"] = trade_cache
        cases.append(case)
        py_out[cid] = (group, py)

    add("metric_keys", "__keys", {"currentReturnType": "NET"}, [], core.metric_keys("NET"))
    add("metric_keys", "__keys", {"currentReturnType": "ALT"}, [], core.metric_keys("ALT"))

    for date, models in data.items():
        for m, rt, bi, et in product(models, ("NET", "ALT"), (0, 40), (0.0, 25.0, 100.0)):
            ser = mapped(m, rt)
            base = core.base_point(ser, bi)
            sig = core.overlay_signals(ser, base, et)
            trades = core.pair_overlay_trades(sig, ser, base)
            tgt = core.split_target_signal(sig, ser, base, 500.0)
            add("overlay", "__overlay", {"baselineFrameIndex": bi, "exitThreshold": et, "dailyTarget": 500}, [ser],
                {"signals": sig, "trades": trades, "target": tgt})
        longest = max(models, key=lambda x: len(x["series"]))["series"]
        n = len(longest)
        # plain grid: default rank hold 1, NET, no selected-time models
        for bi, et, dt, up in product((0, 40), (0.0, 25.0, 100.0), (500.0, 0.0), (n - 1, 150)):
            keys = core.metric_keys("NET")
            g = {"baselineFrameIndex": bi, "exitThreshold": et, "dailyTarget": dt}
            add("leader_rotation", "__leader", g, [{"$ds": date}, "net", up, {"$longest": date}],
                core.leader_rotation(models, "net", up, baseline_index=bi, exit_threshold=et, daily_target=dt, replay_series=longest))
            add("multi_split_rotation", "__multi", g, [{"$ds": date}, up, {"$longest": date}],
                core.multi_split_rotation(models, keys, up, baseline_index=bi, exit_threshold=et, daily_target=dt, replay_series=longest))
        # extended grid: rank hold 1-3, NET/ALT, and with/without selected-time (late-joining) models
        for variant, bi, et, up, hold, rt in product(("", "|sel"), (0, 40), (0.0, 25.0), (n - 1, 150), (1, 2, 3), ("NET", "ALT")):
            ds = date + variant
            keys = core.metric_keys(rt)
            g = {"baselineFrameIndex": bi, "exitThreshold": et, "dailyTarget": 500, "overlayTopX": hold, "currentReturnType": rt}
            add("leader_rotation_ext", "__leader", g, [{"$ds": ds}, keys["netKey"], up, {"$longest": date}],
                core.leader_rotation(datasets[ds], keys["netKey"], up, baseline_index=bi, exit_threshold=et, daily_target=500.0,
                                     replay_series=longest, hold_rank=hold))
            add("multi_split_rotation_ext", "__multi", g, [{"$ds": ds}, up, {"$longest": date}],
                core.multi_split_rotation(datasets[ds], keys, up, baseline_index=bi, exit_threshold=et, daily_target=500.0,
                                          replay_series=longest, hold_rank=hold))

    # Engine class vs page JS: the same spec through Engine.rotation / Engine.overlay (eligible list, replay series, baseline,
    # head and thresholds all chosen by the Engine itself); the page JS gets exactly the inputs the Engine derived.
    for date, models in data.items():
        for rt in ("NET", "ALT"):
            elig = Engine(EngineSpec(date=date, return_type=rt)).load_models(models).eligible()
            ds = f"{date}|elig|{rt}"
            datasets[ds] = elig
            keys = core.metric_keys(rt)
            n_e = max(len(m["series"]) for m in elig)
            for bi, et, hold, fr, kind in product((0, 40), (0.0, 25.0), (1, 2), (-1, 150), ("leader", "multi_split")):
                eng = Engine(EngineSpec(date=date, return_type=rt, baseline_index=bi, exit_threshold=et, hold_rank=hold,
                                        frame_index=fr)).load_models(models)
                up = n_e - 1 if fr < 0 else min(fr, n_e - 1)
                g = {"baselineFrameIndex": bi, "exitThreshold": et, "dailyTarget": 500, "overlayTopX": hold, "currentReturnType": rt}
                if kind == "leader":
                    add("engine_rotation", "__leader", g, [{"$ds": ds}, keys["netKey"], up, {"$longest": ds}], eng.rotation("leader"))
                else:
                    add("engine_rotation", "__multi", g, [{"$ds": ds}, up, {"$longest": ds}], eng.rotation("multi_split"))
            for m in elig:
                for bi, et, fr in product((0, 40), (0.0, 25.0), (-1, 150)):
                    eng = Engine(EngineSpec(date=date, return_type=rt, baseline_index=bi, exit_threshold=et,
                                            frame_index=fr)).load_models(models)
                    out = eng.overlay(m["model"])
                    ser = core.mapped_series(m, rt)
                    part = ser[: (len(ser) - 1 if fr < 0 else min(fr, len(ser) - 1)) + 1]
                    add("engine_overlay", "__overlay", {"baselineFrameIndex": bi, "exitThreshold": et, "dailyTarget": 500}, [part],
                        {"signals": out["signals"], "trades": out["trades"], "target": out["targetSignal"]})

    # Assigned overlay-rule path. Oracle = the page's JS with the one-line eligibility patch ("patched"); the page as written
    # ("asis") is compared with eligible_fallthrough=False. Source trades come from /api/model_trades for the same models/day.
    for date, models in rule_data.items():
        cache = {}
        for m in models:
            rows = get(f"/api/model_trades?model={m['model']}&from={date}&to={date}&product_type=forex&product=all").get("trades") or []
            cache[f"{date}|forex|all|{m['model']}"] = {"rows": rows, "cachedAt": 0}
        datasets[date + "|trades"] = cache
        longest = max(models, key=lambda x: len(x["series"]))["series"]
        n = len(longest)
        max_frames = n
        for rname, cfg, kind, bi, rt, fr in product(RULES, [None], ("leader", "multi_split"), (0, 40), ("NET", "ALT"), (-1, 150)):
            if _ONLY_RULES is not None and rname not in _ONLY_RULES:
                continue
            cfg = RULES[rname]
            rule = {"id": rname, "name": rname, "config": cfg}
            keys = core.metric_keys(rt)
            up = n - 1 if fr < 0 else 150
            ctx = RuleContext(trade_cache=cache, current_date=date, live_date="2099-01-01", current_frame_index=fr,
                              max_frames=max_frames, return_type=rt, eligible_fallthrough=True)
            g = {"baselineFrameIndex": bi, "exitThreshold": 0, "dailyTarget": 500, "currentReturnType": rt, "currentDate": date,
                 "currentFrameIndex": fr, "activePortfolioName": "P", "__rule": rule, "__maxFrames": max_frames, "overlayTopX": 1}
            common = dict(baseline_index=bi, exit_threshold=0.0, daily_target=500.0, replay_series=longest, hold_rank=1,
                          overlay_rule=rule, rule_context=ctx)
            if kind == "leader":
                add("rule_leader", "__leader", g, [{"$ds": date}, keys["netKey"], up, {"$longest": date}],
                    core.leader_rotation(models, keys["netKey"], up, **common), "patched", {"$ds": date + "|trades"})
            else:
                add("rule_multi_split", "__multi", g, [{"$ds": date}, up, {"$longest": date}],
                    core.multi_split_rotation(models, keys, up, **common), "patched", {"$ds": date + "|trades"})
        # cache empty -> 'loading' results (no daily-target signal)
        for kind in ("leader", "multi_split"):
            rule = {"id": "top30", "name": "top30", "config": RULES["top30"]}
            keys = core.metric_keys("NET")
            ctx = RuleContext(trade_cache={}, current_date=date, live_date="2099-01-01", max_frames=max_frames)
            g = {"baselineFrameIndex": 0, "exitThreshold": 0, "dailyTarget": 500, "currentDate": date,
                 "activePortfolioName": "P", "__rule": rule, "__maxFrames": max_frames}
            common = dict(baseline_index=0, replay_series=longest, overlay_rule=rule, rule_context=ctx)
            if kind == "leader":
                add("rule_loading", "__leader", g, [{"$ds": date}, "net", n - 1, {"$longest": date}],
                    core.leader_rotation(models, "net", n - 1, **common), "patched")
            else:
                add("rule_loading", "__multi", g, [{"$ds": date}, n - 1, {"$longest": date}],
                    core.multi_split_rotation(models, keys, n - 1, **common), "patched")
        # page as written: the eligibility filter rejects everything, so a rule selects nothing (only while the page still has that line)
        for kind, rname in product(("leader", "multi_split"), ("top30", "group_buy") if ELIGIBLE_OLD in PAGE_TEXT else ()):
            rule = {"id": rname, "name": rname, "config": RULES[rname]}
            keys = core.metric_keys("NET")
            ctx = RuleContext(trade_cache=cache, current_date=date, live_date="2099-01-01", max_frames=max_frames,
                              eligible_fallthrough=False)
            g = {"baselineFrameIndex": 0, "exitThreshold": 0, "dailyTarget": 500, "currentDate": date,
                 "activePortfolioName": "P", "__rule": rule, "__maxFrames": max_frames}
            common = dict(baseline_index=0, replay_series=longest, overlay_rule=rule, rule_context=ctx)
            if kind == "leader":
                add("rule_as_written", "__leader", g, [{"$ds": date}, "net", n - 1, {"$longest": date}],
                    core.leader_rotation(models, "net", n - 1, **common), "asis", {"$ds": date + "|trades"})
            else:
                add("rule_as_written", "__multi", g, [{"$ds": date}, n - 1, {"$longest": date}],
                    core.multi_split_rotation(models, keys, n - 1, **common), "asis", {"$ds": date + "|trades"})

    # Assigned rules on synthetic data (negatively correlated mirrors, mixed families) so the similar / opposite / family branches fire.
    for date, models in rule_data.items():
        syn = synth(models)
        datasets[date + "|syn"] = syn
        cache = {f"{date}|forex|all|{m['model']}": {"rows": make_rows(m, date), "cachedAt": 0} for m in syn}
        datasets[date + "|syn|trades"] = cache
        longest = max(syn, key=lambda x: len(x["series"]))["series"]
        n = len(longest)
        for rname, kind, bi, rt, fr in product(RULES_SYN, ("leader", "multi_split"), (0, 40), ("NET", "ALT"), (-1, 150)):
            if _ONLY_RULES is not None and rname not in _ONLY_RULES:
                continue
            if fr != -1 and rname not in ("opposite_top", "family_prefix", "similar_hi"):
                continue
            up = n - 1 if fr < 0 else 150
            rule = {"id": rname, "name": rname, "config": RULES_SYN[rname]}
            keys = core.metric_keys(rt)
            ctx = RuleContext(trade_cache=cache, current_date=date, live_date="2099-01-01", current_frame_index=fr,
                              max_frames=n, return_type=rt, eligible_fallthrough=True)
            g = {"baselineFrameIndex": bi, "exitThreshold": 0, "dailyTarget": 500, "currentReturnType": rt, "currentDate": date,
                 "currentFrameIndex": fr, "activePortfolioName": "P", "__rule": rule, "__maxFrames": n, "overlayTopX": 1}
            common = dict(baseline_index=bi, exit_threshold=0.0, daily_target=500.0, replay_series=longest, hold_rank=1,
                          overlay_rule=rule, rule_context=ctx)
            if kind == "leader":
                add("rule_syn_leader", "__leader", g, [{"$ds": date + "|syn"}, keys["netKey"], up, {"$longest": date + "|syn"}],
                    core.leader_rotation(syn, keys["netKey"], up, **common), "patched", {"$ds": date + "|syn|trades"})
            else:
                add("rule_syn_multi_split", "__multi", g, [{"$ds": date + "|syn"}, up, {"$longest": date + "|syn"}],
                    core.multi_split_rotation(syn, keys, up, **common), "patched", {"$ds": date + "|syn|trades"})

    for date, models in rule_data.items():
        syn = datasets[date + "|syn"]
        full = datasets[date + "|syn|trades"]
        partial = {k: v for i, (k, v) in enumerate(full.items()) if i % 2 == 0}
        datasets[date + "|syn|partial"] = partial
        n = max(len(m["series"]) for m in syn)
        longest = max(syn, key=lambda x: len(x["series"]))["series"]
        for rname, kind in product(("top30", "bottom15"), ("leader", "multi_split")):
            if _ONLY_RULES is not None and rname not in _ONLY_RULES:
                continue
            rule = {"id": rname, "name": rname, "config": RULES[rname]}
            keys = core.metric_keys("NET")
            ctx = RuleContext(trade_cache=partial, current_date=date, live_date="2099-01-01", max_frames=n)
            g = {"baselineFrameIndex": 0, "exitThreshold": 0, "dailyTarget": 1, "currentDate": date,
                 "activePortfolioName": "P", "__rule": rule, "__maxFrames": n}
            common = dict(baseline_index=0, daily_target=1.0, replay_series=longest, overlay_rule=rule, rule_context=ctx)
            if kind == "leader":
                add("rule_partial_cache", "__leader", g, [{"$ds": date + "|syn"}, "net", n - 1, {"$longest": date + "|syn"}],
                    core.leader_rotation(syn, "net", n - 1, **common), "patched", {"$ds": date + "|syn|partial"})
            else:
                add("rule_partial_cache", "__multi", g, [{"$ds": date + "|syn"}, n - 1, {"$longest": date + "|syn"}],
                    core.multi_split_rotation(syn, keys, n - 1, **common), "patched", {"$ds": date + "|syn|partial"})

    # Engine class with an assigned rule: the Engine derives eligible list, replay series, max frames and RuleContext itself.
    for date, models in rule_data.items():
        cache = datasets[date + "|trades"]
        for rname, kind, rt in product(("top30", "group_buy"), ("leader", "multi_split"), ("NET", "ALT")):
            if _ONLY_RULES is not None and rname not in _ONLY_RULES:
                continue
            rule = {"id": rname, "name": rname, "config": RULES[rname]}
            keys = core.metric_keys(rt)
            eng = (Engine(EngineSpec(date=date, product_type="forex", return_type=rt, overlay_rule=rule, live_date="2099-01-01"))
                   .load_models(models).load_trade_cache(cache))
            elig = eng.eligible()
            ds = f"{date}|elig|{rt}"
            n_e = max(len(m["series"]) for m in elig)
            g = {"baselineFrameIndex": 0, "exitThreshold": 0, "dailyTarget": 500, "currentReturnType": rt, "currentDate": date,
                 "currentFrameIndex": -1, "activePortfolioName": "P", "__rule": rule, "__maxFrames": n_e, "overlayTopX": 1}
            if kind == "leader":
                add("engine_rule", "__leader", g, [{"$ds": ds}, keys["netKey"], n_e - 1, {"$longest": ds}],
                    eng.rotation("leader"), "patched", {"$ds": date + "|trades"})
            else:
                add("engine_rule", "__multi", g, [{"$ds": ds}, n_e - 1, {"$longest": ds}],
                    eng.rotation("multi_split"), "patched", {"$ds": date + "|trades"})

    # ---- small pure helpers (fast; no API data) ----
    for v in ("00:00", "23:59", "24:00", "12:60", "9:05", "12:05:00", "", None, "ab:cd", "07:5", " 07:05", "07:05\n"):
        add("utils_clock", "clockMinutes", {}, [v], pu.clock_minutes(v))
    for v in (0, 59, 60, 1439, 1440, 1500, -1, -61, 12.7, "90", "x", None, 3200, -1440, -1441, 86399.9):
        add("utils_clock", "replayClockTime", {}, [v], pu.replay_clock_time(v))
    for minute, interval, inc in product((0, 1, 29, 30, 31, 59, 60, 1439, -5, "15", 7.9), (1, 5, 15, 30, 60, 0, "x", 7.9, -3), (True, False, None)):
        args = [minute, interval] if inc is None else [minute, interval, inc]
        add("utils_clock", "nextAutomaticTop1Minute", {}, args, pu.next_automatic_top1_minute(minute, interval, True if inc is None else inc))
    for model in ({}, {"comparisonRole": "selected-time #1", "joined_at": "10:00"}, {"comparisonRole": "selected-time #2", "selectedAt": "18:30"},
                  {"comparisonRole": "other", "joined_at": "10:00"}):
        for point in ({"time": "09:55"}, {"time": "10:00"}, {"time": "18:35"}, {}, None):
            add("utils_clock", "__eligible", {}, [model, point], pu.selected_time_point_eligible(model, point, core.selected_time_join_at(model)))
    for v in ("", "a", "a b", "a,b;c  d", " a , a ,b ", "DNA_1,dna_1", None, "x;;y,,z", "\t a\nb "):
        add("utils_text", "modelSearchTerms", {}, [v], pu.model_search_terms(v))
    for rule in [None, {"name": "x", "config": None}] + [{"name": k, "config": c} for k, c in {**RULES, **RULES_SYN}.items()] + \
            [{"name": "d", "config": {"rules": [{"type": "bogus"}, {"type": "group_ranked"}], "interval_minutes": 0, "hold_rank": 3, "trade_side": "sell"}}]:
        add("utils_text", "overlayRuleSummary", {}, [rule], pu.overlay_rule_summary(rule))
    for c in ("top_net", "family_leaders", "top5_breakout", "top5_x", "top3_tp3_sl3", "top3_tp", "top_alt_net", "", "top1_at_time", "top3_x", "top3_", "top5", "top5_"):
        add("utils_text", "isMetricAwareCriteria", {}, [c], pu.is_metric_aware_criteria(c))
    cat = [{"model": "A", "strategy": "breakout_R_Rev_1"}, {"model": "B", "strategy": "BREAKOUT_Rev_2"}, {"model": "C", "strategy": "breakout_x"},
           {"model": "D", "strategy": "R_Rev_3"}, {"model": "E", "strategy": "other"}, {"model": "F", "strategy": None}]
    pm = [{"model": "G", "strategy": "breakout_Rev_9"}, {"model": "A", "strategy": "ignored"}]
    for mid in ("A", "B", "C", "D", "E", "F", "G", "Z"):
        add("utils_text", "__short", {"strategyCatalogue": cat, "portfolioModels": pm}, [mid], pu.short_strategy_description(mid, cat, pm))
    for model in ({"selectedAtEntries": [{"time": "10:00", "rank": 2}]}, {"selectedAtEntries": []}, {"comparisonRole": "selected-time #3", "selectedAtTimes": ["10:00", "11:00"]},
                  {"selectedRank": 4, "selectedAt": "12:00"}, {"selectedAtTimes": ["9:00"]}, {}, {"comparisonRole": "x", "selectedAt": ""}):
        add("utils_text", "getSelectedTimeNoteEntries", {}, [model], pu.selected_time_note_entries(model))
    for v in ("1", "5", "10", "11", "0", "abc", "", None, "3.5", 2, "-4"):
        add("utils_text", "__rank", {"selectedTimeRankSelect": {"value": v}}, [], pu.selected_time_rank_count(v))
    cfg = {"P1": {"criteria": "top1_at_time", "returnType": "ALT", "productType": "forex", "product": "gbp", "strategyFamily": "breakout", "limit": 20, "minWinRate": 5},
           "P2": {"criteria": "top_win"}, "P3": {"returnType": "NET", "limit": 0, "minWinRate": 0}}
    for active, crit, rt, cur_crit, rank, mwr, en, ml in product((None, "P1", "P2", "P3", "P9"), ({"P1": "top_alt_net"}, {}), ("NET", "ALT"),
                                                                  ("top_net", "top1_at_time", "top_win"), ("3", "12", "5"), (0, 7.5), (False, True), (10, 2)):
        state = {"active_portfolio": active, "portfolio_scenario_configs": cfg, "portfolio_criteria": crit, "current_criteria": cur_crit,
                 "current_return_type": rt, "current_product_type": "forex", "current_product": "all", "current_strategy_family": "all",
                 "model_limit": ml, "min_win_rate": mwr, "rank_select_value": rank, "current_date": "2026-10-14",
                 "auto_refresh_enabled": en, "auto_refresh_direction": "bottom", "auto_refresh_rank": 2}
        g = {"activePortfolioName": active, "portfolioScenarioConfigs": cfg, "portfolioCriteria": crit, "currentCriteria": cur_crit,
             "currentReturnType": rt, "modelLimit": ml, "minWinRate": mwr, "selectedTimeRankSelect": {"value": rank}, "currentDate": "2026-10-14",
             "autoRefreshTop1Enabled": en, "autoRefreshTop1Direction": "bottom", "autoRefreshTop1Rank": 2}
        add("utils_state", "__pit", g, [], pu.point_in_time_request_options(state))
        add("utils_state", "__pitkey", g, [], pu.point_in_time_context_key(state))
    leaders_a = [{"model": "M1", "series": [{"time": "10:00"}], "selectedRank": 2}, {"model": "M2", "series": [{"time": "10:00"}], "joined_at": "09:00"},
                 {"model": "M3", "series": []}, {"model": "M4", "series": [{"time": "10:00"}], "color": "#111"}]
    hist0 = [["M1", {"model": "M1", "color": "#f59e0b", "selectedAtTimes": ["09:00"], "selectedRank": 3, "joined_at": "09:00"}],
             ["M2", {"model": "M2", "color": "", "selectedAtEntries": [{"time": "08:00", "rank": 1}], "joined_at": ""}]]
    leaders_b = [{"model": "M2", "series": [{"time": "10:00"}]}, {"model": "M4", "series": [{"time": "10:00"}], "joined_at": "08:00"},
                 {"model": "M5", "series": [{"time": "10:00"}]}, {"model": "M7", "series": [{"time": "10:00"}], "selectedRank": "3"}]
    hist1 = [["M9", {"model": "M9", "color": "#F59E0B"}],
             ["M4", {"model": "M4", "joined_at": "07:00", "selectedAtTimes": ["07:00"], "selectedRank": 1, "color": "#111111"}],
             ["M5", {"model": "M5", "selectedAtEntries": [], "selectedAtTimes": ["06:00"], "selectedRank": 4}]]
    hist_pal = [[f"H{i}", {"model": f"H{i}", "color": f"#00000{i}"}] for i in range(3)]
    pinned7 = [{"model": f"X{i}", "color": c.upper()} for i, c in enumerate(pu.HISTORY_PALETTE)]
    for pinned, search, hist, leaders, at in product(([], [{"model": "P", "color": "#A78BFA"}], pinned7), ([], [{"model": "S", "color": "#34d399"}]),
                                                     ([], hist0, hist1, hist_pal), (leaders_a, leaders_b, leaders_a[:1], []), ("10:05", "", None)):
        h = {k: copy.deepcopy(v) for k, v in hist}
        pu.retain_selected_time_leaders(h, pinned, search, leaders, at)
        add("utils_state", "__retain", {}, [pinned, search, hist, leaders, at], [[k, v] for k, v in h.items()])
    ids_a = ["WEEK_OVERALL", "2026-09-16", "2026-09-17", "2026-09-18", "2026-09-19", "2026-10-14"]
    for cd, ids in product(("WEEK_OVERALL", "2026-10-14"), (ids_a, ["WEEK_OVERALL"], ["2026-12-01"], [])):
        add("utils_state", "tradeDateRange", {"currentDate": cd, "availableDates": [{"id": i} for i in ids]}, [], pu.trade_date_range(cd, ids))
    for cur, delta, mx in product((-1, 0, 5, 149, 334), (-1, 1, 10, -400), (1, 335)):
        add("utils_frames", "__step", {"currentFrameIndex": cur, "__maxFrames": mx}, [delta], pu.frame_after_step(cur, delta, mx))
    for pct, mx in product((0, 0.25, 0.5, 0.333, 0.75, 1, 1.2, -0.1, 0.0015), (1, 2, 335, 450)):
        add("utils_frames", "__seek", {"__maxFrames": mx}, [pct], pu.frame_for_pct(pct, mx))
    for mode in ("ALL_NET", "BUY_NET", "SELL_NET", "TRI_SPLIT", "MULTI_SPLIT", "BOGUS", "", None, "all_net"):
        add("utils_frames", "__split", {"splitMode": "ALL_NET"}, [mode], mode if pu.valid_split_mode(mode) else "ALL_NET")
    for cur_t, crit, new_t in product(("NET", "ALT"), ("top_net", "top_alt_net", "top_win", "top3_tp3_sl3"), ("NET", "ALT")):
        add("utils_frames", "__retype", {"currentReturnType": cur_t, "currentCriteria": crit, "LIVE_DATE": ""}, [new_t],
            pu.swap_scenario_for_return_type(cur_t, crit, new_t))

    # ---- auto-top1 refresh state machine and exact model search ----
    for req, at, pend, expl, nxt, ival, en, head, msg in product((None, "10:00", "10:05"), ("10:00", "10:05", "bad", None), (None, "10:00"),
                                                                  (False, True), (None, 600), (15, 30), (False, True), (None, "10:05", ""),
                                                                  (None, "", "Added 2")):
        st = pu.AutoTop1State(request_at=req, pending_explicit_time=pend, explicit_refresh=expl, next_minute=nxt, interval_minutes=ival, enabled=en)
        out = pu.finish_automatic_top1_refresh(st, at, msg or "", head)
        g = {"autoRefreshTop1RequestAt": req, "pendingExplicitTop1Time": pend, "selectedTimeExplicitRefresh": expl,
             "autoRefreshTop1NextMinute": nxt, "autoRefreshTop1Minutes": ival, "autoRefreshTop1Enabled": en, "__head": head}
        add("utils_auto", "__finish", g, [at] if msg is None else [at, msg], out)
    pool = [{"model": "DNA_1"}, {"model": "dna_2"}, {"model": "Other"}, {"model": None}]
    loaded = [{"model": "DNA_9", "src": "loaded"}, {"model": "dna_1", "src": "loaded"}]
    for text, ld, av, mode in product(("", "dna_1", "DNA_1", " DNA_2 ", "DNA_1,DNA_2", "DNA_9", "other", "zzz", None, "dna_1;"),
                                       ([], loaded), (pool, []), ("scenario", "portfolio", "pit")):
        g = {"modelSearchInput": {"value": text}, "modelSearchLoadedModels": ld, "__candidates": av if mode == "scenario" else [],
             "activePortfolioName": "P" if mode == "portfolio" else None, "portfolioModels": av if mode == "portfolio" else [],
             "pointInTimeMode": mode == "pit", "pointInTimeModels": av if mode == "pit" else []}
        add("utils_search", "__exact", g, [], pu.exact_search_model(text, ld, av))

    # ---- data layer: DataClient vs the page's own fetchers, both fed the same fixture responses ----
    class FakeTransport:
        def __init__(self, fx):
            self.fx, self.calls = fx, []

        probe = None
        mid = None

        def __call__(self, url):
            self.calls.append(url)
            if self.probe and self.mid is None:  # the first request's moment (the portfolio group reads it once)
                self.mid = list(self.probe())
            r = self.fx.get(url)
            return (r["status"], r["payload"]) if r else (404, {"error": "not found"})

    def fx_of(*pairs):
        return {u: {"status": s, "payload": p} for u, s, p in pairs}

    API = "http://api"
    def lvn(cl):
        return [[k, {"modelKey": v["modelKey"], "entry": {"models": v["entry"]["models"], "cachedAt": "NOW" if abs(v["entry"]["cachedAt"] - datetime.now().timestamp() * 1000) < 120000 else v["entry"]["cachedAt"]}}] for k, v in cl.last_view.items()]

    def mi(m):
        return int(m[1:]) if m[1:].isdigit() else sum(map(ord, m))

    def mk(i, n=2):
        return {"model": f"DNA_{i}", "product": "gbp", "series": [{"time": f"{h:02d}:00", "net": float(i * h)} for h in range(n)]}

    live_payload = {"products": ["eurusd", "gbp"], "tp_sl_scenarios": [{"id": "top3_tp3_sl5", "tp": 3, "sl": 5}, {"id": "top3_tp3_sl3", "tp": 3, "sl": 3}, {"id": "top3_tp_sl", "tp": 0, "sl": 0},
                                                                     {"id": "top3_tp10_sl3", "tp": 10, "sl": 3}, {"id": "bad_id", "tp": 1, "sl": 1}, None],
                    "top_net": [mk(1), mk(2)], "top_alt_net": [mk(3)], "family_leaders_net": [mk(4)], "top3_tp3_sl3_net": [mk(5)],
                    "note": "ignored (not an array)", "generated_at": "2026-10-14T12:00:00"}
    for (tdate, ptype, prod, fam, lim, crit, rt, status, payload) in product(
            ("2026-10-14",), ("all", "forex"), ("all", "gbp", "zzz"), ("all", "breakout"), (10, 5),
            ("top_net", "top1_at_time", "family_leaders", "top5_breakout", "top3_tp3_sl3"), ("NET", "ALT"),
            (200, 500), (live_payload,)):
        cl = dc.DataClient(None, API, live_date="2099-01-01")
        url = cl.live_day_url(tdate, ptype, prod, fam, lim, crit, rt)
        if status == 500 and (ptype, prod, fam, lim, rt) != ("all", "all", "all", 10, "NET"):
            continue  # one failure case per criteria is enough
        fx = fx_of((url, status, live_payload if status == 200 else {"error": "boom"}))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API, live_date="2099-01-01")
        cl.current_product = prod
        res = cl.refresh_live_data(tdate, product_type=ptype, product=prod, strategy_family=fam, limit=lim, criteria=crit, return_type=rt)
        g = {"currentProductType": ptype, "currentProduct": prod, "currentStrategyFamily": fam, "modelLimit": lim, "currentCriteria": crit,
             "currentReturnType": rt, "currentDate": "", "LIVE_DATE": "2099-01-01"}
        add("data_live", "__live", g, [fx, tdate], {"calls": tr.calls, "criteria": cl.criteria_data, "product": cl.current_product,
                                                       "tpSl": res.get("tp_sl_ids", []), "badge": list(cl.live_badge) if cl.live_badge else None})

    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    ids25 = [f"M{i}" for i in range(25)]
    for ids, bg, gen, status_b, date, live, fail_at in product((["A", "B"], ids25, ids25[:10], ids25[:11], []), (False, True),
                                                                ("2020-01-01T00:00:00", now_iso, None), (200, 500), ("2026-10-14",),
                                                                ("2099-01-01", "2026-10-14"), ("last", "first")):
        key = ",".join(ids)
        if not ids and not bg:
            pass
        cache_key = f"{date}|{key}"
        batches = [[x for x in ids if x][i:i + 10] for i in range(0, len([x for x in ids if x]), 10)]
        pairs = []
        for gi, b in enumerate(batches):
            q = {"date": date, "models": ",".join(b)}
            if bg:
                q["refresh"] = "1"
            u = f"{API}/api/portfolio_day?{dc.url_search_params(q)}"
            st = status_b if gi == (len(batches) - 1 if fail_at == "last" else 0) else 200
            gen_i = (gen if gi % 2 == 0 or not gen else gen.replace("2020", "2019").replace(now_iso[:4], str(int(now_iso[:4]) - 1)))
            pairs.append((u, st, {"models": [mk(mi(m)) for m in b], **({"generated_at": gen_i} if gen else {})} if st == 200 else {"detail": "bad"}))
        # background refresh request for the stale / live case (second call) shares the fixture shape with refresh=1
        if not bg and date == live:
            for gi, b in enumerate(batches):
                u = f"{API}/api/portfolio_day?{dc.url_search_params({'date': date, 'models': ','.join(b), 'refresh': '1'})}"
                pairs.append((u, 200, {"models": [mk(mi(m)) for m in b], **({"generated_at": gen} if gen else {})}))
        fx = fx_of(*pairs)
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API, live_date=live)
        try:
            cl.fetch_portfolio_data(cache_key, date, key, bg, "P")
            exp = {"calls": tr.calls, "cache": [[k, {"models": v["models"], "cachedAt": "NOW" if abs(v["cachedAt"] - datetime.now().timestamp() * 1000) < 120000 else v["cachedAt"]}]
                                               for k, v in cl.portfolio_view_cache.items()], "lastView": lvn(cl)}
        except dc.FetchError as e:
            exp = {"calls": tr.calls, "error": str(e)}
        add("data_portfolio", "__pfetch", {"LIVE_DATE": live}, [fx, cache_key, date, key, bg, None], exp)

    for pname in (None, ""):
        key, date = "A,B", "2026-10-14"
        cache_key = f"{date}|{key}"
        fx = fx_of((f"{API}/api/portfolio_day?{dc.url_search_params({'date': date, 'models': key})}", 200, {"models": [mk(1), mk(2)], "generated_at": "2020-01-01T00:00:00"}))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API, live_date="")
        cl.fetch_portfolio_data(cache_key, date, key, False, pname)
        add("data_portfolio", "__pfetch", {"LIVE_DATE": ""}, [fx, cache_key, date, key, False, None, pname],
            {"calls": tr.calls, "cache": [[k, {"models": v["models"], "cachedAt": v["cachedAt"]}] for k, v in cl.portfolio_view_cache.items()], "lastView": lvn(cl)})
    for n_seed in (30, 31, 32, 33):
        seed = [[f"old{i}", {"models": [mk(i)], "cachedAt": 1.0}] for i in range(n_seed)]
        key, date = "A,B", "2026-10-14"
        cache_key = f"{date}|{key}"
        fx = fx_of((f"{API}/api/portfolio_day?{dc.url_search_params({'date': date, 'models': key})}", 200, {"models": [mk(1), mk(2)], "generated_at": "2020-01-01T00:00:00"}))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API, live_date="")
        for k, v in seed:
            cl.portfolio_view_cache[k] = dict(v)
        cl.fetch_portfolio_data(cache_key, date, key, False, "P")
        add("data_portfolio", "__pfetch", {"LIVE_DATE": ""}, [fx, cache_key, date, key, False, seed],
            {"calls": tr.calls, "cache": [[k, {"models": v["models"], "cachedAt": v["cachedAt"]}] for k, v in cl.portfolio_view_cache.items()], "lastView": lvn(cl)})
    for models, prefer, seeded, date, live, gen, last_seeded in product((["A", "B"], [], ids25[:12]), (True, False), (False, True), ("2026-10-14", "bad-date"),
                                                           ("2099-01-01", "2026-10-14"), ("2020-01-01T00:00:00", now_iso), ("none", "models", "empty")):
        key = ",".join(models)
        cache_key = f"{date}|{key}"
        batches = [models[i:i + 10] for i in range(0, len(models), 10)]
        pairs = []
        for bgf in (False, True):
            for b in batches:
                q = {"date": date, "models": ",".join(b)}
                if bgf:
                    q["refresh"] = "1"
                pairs.append((f"{API}/api/portfolio_day?{dc.url_search_params(q)}", 200,
                              {"models": [mk(mi(m)) for m in b], "generated_at": gen}))
        fx = fx_of(*pairs)
        seed = ([["other|key", {"models": [mk(98)], "cachedAt": 1.0}], [cache_key, {"models": [mk(99)], "cachedAt": datetime.fromisoformat(gen).timestamp() * 1000}],
                 ["third|key", {"models": [mk(97)], "cachedAt": 1.0}]] if seeded else [])
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API, live_date=live)
        tr.probe = lambda cl=cl: (copy.deepcopy(cl.portfolio_models),)
        for k, v in seed:
            cl.portfolio_view_cache[k] = dict(v)
        last_seed = [] if last_seeded == "none" else [[f"{date}|P", {"modelKey": "old", "entry": {"models": ([mk(55)] if last_seeded == "models" else []), "cachedAt": 5.0}}]]
        for k, v in last_seed:
            cl.last_view[k] = copy.deepcopy(v)
        try:
            r = cl.load_portfolio_data(models, date, prefer, "P")
            exp = {"calls": tr.calls, "cache": [[k, {"models": v["models"], "cachedAt": "NOW" if abs(v["cachedAt"] - datetime.now().timestamp() * 1000) < 120000 else v["cachedAt"]}]
                                                 for k, v in cl.portfolio_view_cache.items()],
                   "lastView": lvn(cl), "models": r["models"], "fetched": r["fetched"], "mid": (tr.mid[0] if tr.mid else None)}
        except dc.FetchError as e:
            exp = {"calls": tr.calls, "error": str(e)}
        add("data_portfolio", "__pload", {"LIVE_DATE": live}, [fx, models, date, prefer, seed, last_seed], exp)

    def pd_url(models, date):
        return f"{API}/api/portfolio_day?{dc.url_search_params({'models': ','.join(models), 'date': date})}"

    found = {m: {"model": m, "color": None if i % 2 else "#123456", "series": [{"time": "10:00"}]} for i, m in enumerate(["DNA_1", "dna_2", "DNA_3", "X_4"])}
    for term, date, st in product(("DNA_1", "A.B-c_d", "dna_1, DNA_2", "DNA_1 dna_9", "zz", "bad id!", "", None, " DNA_1;DNA_3 ", ",".join(f"DNA_{i}" for i in range(12))),
                                  ("2026-10-14", "nope"), (200, 500)):
        req = pu.model_search_terms(term)
        batches = [req[i:i + 10] for i in range(0, len(req), 10)]
        pairs = [(pd_url(b, date), st if bi == 0 else 200, {"models": [found[m] for m in reversed(list(found)) if m.lower() in {x.lower() for x in b}]} if st == 200 else {"error": "boom"})
                 for bi, b in enumerate(batches)]
        fx = fx_of(*pairs)
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API)
        cl.load_model_search(term, date)
        add("data_search", "__search", {}, [fx, term, date], {"calls": tr.calls, "loaded": cl.model_search_loaded, "status": cl.model_search_status})

    for ids, date, only, st in product((["DNA_1", "DNA_1", " dna_2 "], ["DNA_1", "nope!", ""], [], [f"DNA_{i}" for i in range(14)], ["X_4", "DNA_9"]),
                                       ("2026-10-14", "nope"), (False, True), (200, 500)):
        clean = []
        for raw in ids:
            s = str(raw).strip()
            if dc.MODEL_ID_RE.fullmatch(s) and s not in clean:
                clean.append(s)
        clean = clean[:10]
        fx = fx_of((pd_url(clean, date), st, {"models": [found.get(m, found.get(m.lower())) for m in clean if m in found or m.lower() in found] + [{"model": ""}]} if st == 200 else {"detail": "bad"}))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API)
        cl.load_deep_link_models(ids, date, only)
        add("data_search", "__deeplink", {}, [fx, ids, date, only], {"calls": tr.calls, "pinned": [[k, v] for k, v in cl.pinned.items()], "status": cl.deep_link_status})

    odd = "g b~*!'()x&=%+ü/"
    for crit, rt in (("top_net", "NET"), ("top1_at_time", "ALT")):
        cl = dc.DataClient(None, API, live_date="2099-01-01")
        url = cl.live_day_url("2026-10-14", odd, odd, odd, 10, crit, rt)
        fx = fx_of((url, 200, {"products": [odd], "top_net": [mk(1)]}))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API, live_date="2099-01-01")
        cl.current_product = odd
        res = cl.refresh_live_data("2026-10-14", product_type=odd, product=odd, strategy_family=odd, limit=10, criteria=crit, return_type=rt)
        g = {"currentProductType": odd, "currentProduct": odd, "currentStrategyFamily": odd, "modelLimit": 10, "currentCriteria": crit,
             "currentReturnType": rt, "currentDate": "", "LIVE_DATE": "2099-01-01"}
        add("data_live", "__live", g, [fx, "2026-10-14"], {"calls": tr.calls, "criteria": cl.criteria_data, "product": cl.current_product,
                                                            "tpSl": res.get("tp_sl_ids", []), "badge": None})
    odd_date, odd_key = "2026 10~14*(x)!&+", "A B,C~D,E*F,G'H!,I(J),K+L&M=N%O"
    odd_ids = odd_key.split(",")
    fx = fx_of((f"{API}/api/portfolio_day?{dc.url_search_params({'date': odd_date, 'models': ','.join(odd_ids)})}", 200, {"models": [mk(1)], "generated_at": "2020-01-01T00:00:00"}))
    tr = FakeTransport(fx)
    cl = dc.DataClient(tr, API, live_date="")
    cl.fetch_portfolio_data(f"{odd_date}|{odd_key}", odd_date, odd_key, False, "P")
    add("data_portfolio", "__pfetch", {"LIVE_DATE": ""}, [fx, f"{odd_date}|{odd_key}", odd_date, odd_key, False, None],
        {"calls": tr.calls, "cache": [[k, {"models": v["models"], "cachedAt": v["cachedAt"]}] for k, v in cl.portfolio_view_cache.items()], "lastView": lvn(cl)})
    odd_models = ["A B~*!'()", "ü", "x/y&z"]
    fx = fx_of(*[(f"{API}/api/model_trades?model={dc.encode_uri_component(m)}&from=2026-10-14&to=2026-10-14&product_type={dc.encode_uri_component('forex x')}&product={dc.encode_uri_component('all&b')}",
                  200, {"trades": [{"opened": "x"}]}) for m in odd_models])
    tr = FakeTransport(fx)
    cl = dc.DataClient(tr, API, live_date="2099-01-01")
    cl.ensure_trade_data(odd_models, "2026-10-14", "forex x", "all&b")
    add("data_trades", "__trades", {"LIVE_DATE": "2099-01-01"}, [fx, odd_models, "2026-10-14", "forex x", "all&b", []],
        {"calls": tr.calls, "cache": [[k, {"rows": v["rows"], "cachedAt": "NOW"}] for k, v in cl.trade_cache.items()]})
    odd_cat_date = "2026 10/14~*!'()&="
    fx = fx_of((f"{API}/api/strategy_catalog?date={dc.encode_uri_component(odd_cat_date)}", 200, {"models": [{"model": "A"}]}))
    tr = FakeTransport(fx)
    cl = dc.DataClient(tr, API)
    cl.load_strategy_catalogue(odd_cat_date)
    add("data_catalog", "__catalog", {}, [fx, odd_cat_date, [], None],
        {"calls": tr.calls, "catalogue": cl.strategy_catalogue, "date": cl.strategy_catalogue_date, "text": cl.strategy_catalogue_status})

    cat = {"models": [{"model": "A", "strategy": "breakout_x"}, {"model": "B"}]}
    for date, st, seed_cat, seed_date in product(("2026-10-14",), (200, 500, 404), ([], [{"model": "OLD"}]), (None, "2026-10-14", "2026-10-13")):
        fx = fx_of((f"{API}/api/strategy_catalog?date={dc.encode_uri_component(date)}", st, cat if st == 200 else {"error": "nope"}))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API)
        cl.strategy_catalogue, cl.strategy_catalogue_date = list(seed_cat), seed_date
        cl.load_strategy_catalogue(date)
        add("data_catalog", "__catalog", {}, [fx, date, seed_cat, seed_date],
            {"calls": tr.calls, "catalogue": cl.strategy_catalogue, "date": cl.strategy_catalogue_date, "text": cl.strategy_catalogue_status})
    for st, payload, seed in product((200, 500), ({"rules": [{"id": "r"}], "assignments": {"P": "r"}}, {"rules": "x", "assignments": []}, {}),
                                     ({"rules": [], "assignments": {}}, {"rules": [{"id": "old"}], "assignments": {"Q": "old"}})):
        fx = fx_of((f"{API}/api/overlay_rules", st, payload))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API)
        cl.overlay_rule_library = copy.deepcopy(seed)
        cl.load_overlay_rule_library()
        add("data_catalog", "__rulelib", {}, [fx, seed], {"calls": tr.calls, "library": cl.overlay_rule_library})

    trades_payload = {"trades": [{"opened": "2026-10-14 10:00:00", "net_return": 5.0}]}
    for models, date, live, seeded, st in product((["A", "B"], ["C d"]), ("2026-10-14", "bad"), ("2099-01-01", "2026-10-14"), (False, True, "stale"), (200, 500)):
        pairs = [(f"{API}/api/model_trades?model={dc.encode_uri_component(m)}&from={date}&to={date}&product_type=forex&product=all", st,
                  trades_payload if st == 200 else {"error": "x"}) for m in models]
        fx = fx_of(*pairs)
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API, live_date=live)
        seed = []
        if seeded:
            seed = [[f"{date}|forex|all|{models[0]}", {"rows": [{"old": 1}], "cachedAt": 1.0 if seeded == "stale" else datetime.now().timestamp() * 1000}]]
            for k, v in seed:
                cl.trade_cache[k] = dict(v)
        cl.ensure_trade_data(models, date, "forex", "all")
        add("data_trades", "__trades", {"LIVE_DATE": live}, [fx, models, date, "forex", "all", seed],
            {"calls": tr.calls, "cache": [[k, {"rows": v["rows"], "cachedAt": "NOW" if abs(v["cachedAt"] - datetime.now().timestamp() * 1000) < 120000 else v["cachedAt"]}]
                                           for k, v in cl.trade_cache.items()]})
    daily = {"top_net": [mk(1)], "top_alt_net": [mk(2)]}
    for dkey, buckets, st, live in product(("2026-10-14", "WEEK_OVERALL", "bad", "2026-10-15"), ({}, {"top_net": {"2026-10-14": [mk(7)]}}, {"top_net": {"2026-10-14": []}}),
                                           (200, 404), ("2099-01-01", "2026-10-14")):
        fx = fx_of((f"http://h/p/historical_curve_data/{dc.encode_uri_component(dkey)}.json", st, daily if st == 200 else {"error": "x"}))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API, live_date=live, base_href="http://h/p/page.html")
        cl.criteria_data = copy.deepcopy(buckets)
        try:
            cl.ensure_historical_data(dkey)
            exp = {"calls": tr.calls, "criteria": cl.criteria_data}
        except dc.FetchError as e:
            exp = {"calls": tr.calls, "error": str(e), "criteria": cl.criteria_data}
        add("data_trades", "__hist", {"LIVE_DATE": live}, [fx, dkey, buckets], exp)

    # ---- selected-time cohort: the page's own refreshPointInTimeSelection vs selected_time.refresh_point_in_time_selection ----
    rng = random.Random(7)

    def rmod(i, series=True, color="auto"):
        return {"model": f"R{i}", "product": "gbp", "color": (f"#aabb0{i}" if color == "auto" else color),
                "series": [{"time": "10:00", "net": float(i)}, {"time": "10:05", "net": float(i + 1)}] if series else []}

    ranked5 = [rmod(i) for i in range(1, 6)]
    ranked_mixed = [rmod(1, color=None), rmod(2, series=False), rmod(3), rmod(4, color=None), rmod(5)]
    ranked_pal = [rmod(1, color="#a78bfa"), rmod(2, color="#f59e0b"), rmod(3, color="#34d399")]
    ranked_meta = [{**rmod(1), "joined_at": "07:00", "selectedAtTimes": ["x1"], "selectedAtEntries": [{"time": "x1", "rank": 4}], "selectedRank": 3}, rmod(2), rmod(3)]
    ranked_empty = [rmod(i, series=False) for i in (1, 2, 3)]
    payloads = {
        "A": (200, {"models": ranked5, "at_time": "10:00"}), "B": (200, {"models": ranked5}), "C": (200, {"models": "x", "at_time": "10:00"}),
        "D": (200, {"models": [], "at_time": "10:00"}), "E": (500, {"error": "boom"}), "F": (500, {}), "G": (200, {"models": ranked_mixed, "at_time": "11:30"}), "H": (200, {"models": ranked_empty, "at_time": "10:00"}),
        "P": (200, {"models": ranked_pal, "at_time": "10:00"}), "Q": (200, {"models": ranked_meta, "at_time": "10:00"}),
    }
    ctx_ok = "2026-10-14|top_net|forex|all|all|NET"
    hist_rec = {"model": "R1", "color": "#f59e0b", "selectedAt": "09:00", "selectedAtTimes": ["09:00"], "joined_at": "09:00",
                "selectedAtEntries": [{"time": "09:00", "rank": 2}], "selectedRank": 2, "series": rmod(1)["series"]}
    hist_other = {"model": "R9", "color": "#38bdf8", "selectedAt": "08:00", "selectedAtTimes": ["08:00", "08:30"], "joined_at": "08:00",
                  "selectedAtEntries": [{"time": "08:00", "rank": 1}, {"time": "08:30", "rank": 1}], "selectedRank": 1, "series": rmod(9)["series"]}
    histories = {"none": ([], ""), "same": ([["R1", hist_rec], ["R9", hist_other]], ctx_ok), "other_ctx": ([["R1", hist_rec]], "stale|ctx")}
    pinned_sets = {"none": [], "pin": [["R2", {**rmod(2), "color": "#123456", "comparisonRole": "pinned comparison"}], ["Z9", {**rmod(9), "model": "Z9", "color": "#654321"}]]}
    searches = {"none": [], "one": [{**rmod(3), "model": "S1", "color": "#e879f9"}, {**rmod(4), "color": "#00ff00"}]}
    initial_models = {"none": [], "two": [{**rmod(7), "comparisonRole": "x"}, rmod(8)]}
    timelines = {"none": [], "two": [rmod(1)]}
    configs = {"P1": {"criteria": "top_net", "returnType": "NET", "productType": "forex", "product": "all", "strategyFamily": "all", "limit": 4, "minWinRate": 0}}
    modes = {"plain": (None, False, None), "explicit": (None, True, "10:05"), "auto": ("10:05", False, None), "explicit_other": (None, True, "09:00")}
    dims = [list(x) for x in (modes, payloads, ("1", "3", "12"), ("2", None, "9"), ("top", "bottom", "x"), histories, pinned_sets, searches, initial_models,
                        ("top_net", "top1_at_time"), (None, "P1"), (-1, 5, 334), (None, "11:00"), ("none", "hist"), ("", "same"))]
    grid = [tuple(rng.choice(dm) for dm in dims) for _ in range(1400)]
    for mode, pay, rank_v, auto_rank, auto_dir, hist_name, pin_name, search_name, init_name, crit, active, frame, at_ov, rem, reqkey in grid[:1400]:
        req_at, expl, pending = modes[mode]
        at = at_ov or "10:05"
        if mode == "auto" and at_ov:
            req_at = at_ov
        if mode == "explicit" and at_ov:
            pending = at_ov
        hist, hist_ctx = histories[hist_name]
        status, body = payloads[pay]
        opt_state = {"active_portfolio": active, "portfolio_scenario_configs": configs, "portfolio_criteria": {"P1": "top_net"}, "current_criteria": crit,
                     "current_return_type": "NET", "current_product_type": "forex", "current_product": "all", "current_strategy_family": "all",
                     "model_limit": 10, "min_win_rate": 0, "rank_select_value": rank_v}
        opts = pu.point_in_time_request_options(opt_state)
        ad = ("bottom" if auto_dir == "bottom" else "top") if mode == "auto" else None
        arn = pu._number(auto_rank)
        ar = max(1, min(5, 1 if (arn != arn or arn == 0) else arn))
        url = dc.DataClient(None, API).point_in_time_url("2026-10-14", at, opts, ad, ar if mode == "auto" else None)
        fx = fx_of((url, status, body))
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API)
        pit_probe = {}
        tr.probe = lambda: (pit_probe["st"].status, pit_probe["st"].status_class)
        st = stm.SelectedTimeState(point_in_time_mode=True, current_date="2026-10-14", current_criteria=crit, active_portfolio=active,
                                   auto=pu.AutoTop1State(request_at=req_at, pending_explicit_time=pending, explicit_refresh=expl, next_minute=None,
                                                         interval_minutes=15, enabled=True),
                                   auto_direction=auto_dir, auto_rank_value=auto_rank, models=copy.deepcopy(initial_models[init_name]),
                                   timeline_models=copy.deepcopy(timelines[init_name]), requested_key="", pinned=OrderedDict((k, copy.deepcopy(v)) for k, v in pinned_sets[pin_name]),
                                   search_loaded=copy.deepcopy(searches[search_name]),
                                   history=OrderedDict((k, copy.deepcopy(v)) for k, v in hist), history_context=hist_ctx,
                                   scenario_removed=({"R2"} if (init_name == "two" and pin_name == "none") else set()) | ({"R1", "R9"} if rem == "hist" else set()),
                                   scenario_names={"top_net": "Top 10 Net Return", "top1_at_time": "Top 1 at time"}, frame_index=frame)
        eligible = [rmod(1), rmod(2)] if frame == -1 else []
        init_removed = sorted(st.scenario_removed)
        if reqkey == "same":  # an identical request is skipped (the key of the request about to be made is already recorded)
            st.requested_key = "|".join(pu.js_str(p) for p in [st.current_date, at, opts["scenario"], opts["return_type"], opts["product_type"], opts["product"],
                                                              opts["strategy_family"], opts["limit"], opts["min_win_rate"], st.active_portfolio or "scenario",
                                                              (ad or "top") if mode == "auto" else "", ar if mode == "auto" else ""])
        pit_probe["st"] = st
        init = {"mode": True, "date": "2026-10-14", "criteria": crit, "active": active, "configs": configs, "pcrit": {"P1": "top_net"}, "rt": "NET",
                "ptype": "forex", "product": "all", "fam": "all", "limit": 10, "mwr": 0, "rankValue": rank_v, "autoDir": auto_dir, "autoRankValue": auto_rank,
                "autoEnabled": True, "reqAt": req_at, "pending": pending, "explicit": expl, "nextMinute": None, "interval": 15,
                "models": st.models, "timeline": copy.deepcopy(timelines[init_name]), "requestedKey": st.requested_key, "pinned": [[k, v] for k, v in st.pinned.items()], "search": st.search_loaded,
                "history": [[k, v] for k, v in st.history.items()], "historyContext": hist_ctx, "removed": init_removed,
                "names": [["top_net", "Top 10 Net Return"], ["top1_at_time", "Top 1 at time"]], "frame": frame, "maxFrames": 335, "head": "10:05", "eligible": eligible}
        init = copy.deepcopy(init)
        stm.refresh_point_in_time_selection(st, cl, opt_state, head_time="10:05", max_frames=335, eligible_models=eligible, at_override=at_ov)
        add("data_pitsel", "__pitsel", {}, [fx, init, at_ov],
            {"calls": tr.calls, "models": st.models, "timeline": st.timeline_models, "requestedKey": st.requested_key,
             "history": [[k, v] for k, v in st.history.items()], "historyContext": st.history_context, "removed": sorted(st.scenario_removed),
             "status": st.status, "statusClass": st.status_class, "historyAt": st.history_at, "visible": sorted(str(x) for x in st.visible),
             "frame": st.frame_index, "reqAt": st.auto.request_at, "pending": st.auto.pending_explicit_time, "explicit": st.auto.explicit_refresh,
             "nextMinute": st.auto.next_minute, "autoStatus": st.auto_status, "sched": st.sched,
             "input": st.selected_time_input or "", "selIdx": st.selected_model_index, "mid": tr.mid})
    # early exits: not in point-in-time mode, bad date, nothing to look up
    for mode_f, date_f, head_f in ((False, "2026-10-14", "10:05"), (True, "nope", "10:05"), (True, "2026-10-14", None)):
        fx = fx_of()
        tr = FakeTransport(fx)
        cl = dc.DataClient(tr, API)
        st = stm.SelectedTimeState(point_in_time_mode=mode_f, current_date=date_f)
        init = {"mode": mode_f, "date": date_f, "criteria": "top_net", "active": None, "configs": configs, "pcrit": {}, "rt": "NET", "ptype": "forex",
                "product": "all", "fam": "all", "limit": 10, "mwr": 0, "rankValue": "1", "autoDir": "top", "autoRankValue": "1", "autoEnabled": True,
                "reqAt": None, "pending": None, "explicit": False, "nextMinute": None, "interval": 15, "models": [], "timeline": [], "requestedKey": "",
                "pinned": [], "search": [], "history": [], "historyContext": "", "removed": [], "names": [], "frame": -1, "maxFrames": 335, "head": head_f, "eligible": []}
        stm.refresh_point_in_time_selection(st, cl, {"current_criteria": "top_net", "current_return_type": "NET", "current_product_type": "forex",
                                                      "current_product": "all", "current_strategy_family": "all", "model_limit": 10, "min_win_rate": 0},
                                            head_time=head_f, max_frames=335, eligible_models=[])
        add("data_pitsel", "__pitsel", {}, [fx, init, None],
            {"calls": tr.calls, "models": [], "timeline": [], "requestedKey": "", "history": [], "historyContext": "", "removed": [], "status": "",
             "statusClass": "", "historyAt": "", "visible": [], "frame": -1, "reqAt": None, "pending": None, "explicit": False, "nextMinute": None,
             "autoStatus": None, "sched": None, "input": "", "selIdx": 0, "mid": None})

    spec = {"page": str(PAGE), "inventory": str(INVENTORY), "functions": FUNCS, "cases": cases,
            "datasets": datasets, "extra": JS_EXTRA, "variants": {"patched": [[ELIGIBLE_OLD, ELIGIBLE_NEW]], "asis": []}}
    # The JS cases are independent: spread them over parallel Node workers (DIFF_WORKERS, default 8).
    workers = max(1, min(int(os.environ.get("DIFF_WORKERS", "8")), len(cases)))
    js_results = []
    with tempfile.TemporaryDirectory() as td:
        procs = []
        # Data cases carry timestamps relative to 'now' (cache freshness): run them first, a few seconds after they were built,
        # not after the ~20 minutes the heavy rule cases take.
        ordered = sorted(cases, key=lambda c: 0 if py_out[c["id"]][0].startswith("data_") else 1)
        for k in range(workers):
            chunk = ordered[k::workers]
            sp = Path(td) / f"cases{k}.json"
            sp.write_text(json.dumps({**spec, "cases": chunk}), encoding="utf-8")
            procs.append(subprocess.Popen(["node", str(ROOT / "tools" / "js_runner.js"), str(sp)],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        for pr in procs:
            out, err = pr.communicate(timeout=7200)
            if pr.returncode != 0:
                print("NODE FAILED:", err.decode("utf-8", "replace")[-1500:])
                sys.exit(2)
            js_results.extend(json.loads(out.decode("utf-8")))
    js_res = {r["id"]: r for r in js_results}

    summary, failures, extra_keys = {}, {}, {}
    for cid_, (group, py) in py_out.items():
        s = summary.setdefault(group, {"cases": 0, "pass": 0, "js_error": 0})
        s["cases"] += 1
        r = js_res[cid_]
        if not r["ok"]:
            s["js_error"] += 1
            failures.setdefault(group, []).append(f"case {cid_}: JS error {r['error']}")
            continue
        if os.environ.get("DIFF_DEBUG_ID") == str(cid_):
            print("DEBUG JS:", json.dumps(r)[:2500])
            print("DEBUG PY:", json.dumps(py, default=str)[:2500])
        ek = extra_keys.setdefault(group, set())
        global STRICT
        STRICT = group.startswith("data_")
        d = diff(py, r["result"], "", ek)
        if d:
            failures.setdefault(group, []).append(f"case {cid_}: {d}")
        else:
            s["pass"] += 1

    stats = {}
    for cid_, (group, py) in py_out.items():
        if group.startswith("rule_") and isinstance(py, dict):
            st = stats.setdefault(group, {"with_trades": 0, "with_source_trades": 0, "with_T": 0, "loading": 0, "trades": 0})
            st["trades"] += len(py["trades"])
            st["with_trades"] += bool(py["trades"])
            st["with_source_trades"] += any((t.get("actualTradeCount") or 0) > 0 for t in py["trades"])
            st["with_T"] += py["targetSignal"] is not None
            st["loading"] += any(t.get("resultSource") == "loading" for t in py["trades"])
    for g, s in summary.items():
        print(f"{g:22s} cases={s['cases']:4d} pass={s['pass']:4d} fail={s['cases']-s['pass']-s['js_error']:4d} js_error={s['js_error']}")
        for f in failures.get(g, [])[:3]:
            print("     ", f[:260])
        if extra_keys.get(g):
            print("      JS-only keys:", sorted(extra_keys[g]))
    for g, st in stats.items():
        print(f"  coverage {g}: {st}")
    if _ns.breakdown:
        from collections import Counter
        meta = {c["id"]: c for c in cases}
        for g in ("leader_rotation", "multi_split_rotation"):  # plain grid only
            cnt = Counter()
            for cid_, (group, py) in py_out.items():
                if group != g:
                    continue
                c = meta[cid_]
                gl = c["globals"]
                up = c["args"][2] if g == "leader_rotation" else c["args"][1]
                ok = js_res[cid_]["ok"] and diff(py, js_res[cid_]["result"]) is None
                cnt[(f"base={gl['baselineFrameIndex']}", f"exit={gl['exitThreshold']}", f"target={gl['dailyTarget']}", f"up={up}", "PASS" if ok else "FAIL")] += 1
            print(g)
            for k, v in sorted(cnt.items()):
                print("   ", *k, v)
    out = ROOT / "tests" / "diff_results_20261016.json"
    if not out.exists():
        out.write_text(json.dumps({"page": str(PAGE), "summary": summary,
                                   "failures": {g: f[:20] for g, f in failures.items()},
                                   "js_only_keys": {g: sorted(k) for g, k in extra_keys.items()}}, indent=1), encoding="utf-8")
    sys.exit(0 if all(s["pass"] == s["cases"] for s in summary.values()) else 1)


if __name__ == "__main__":
    main()
