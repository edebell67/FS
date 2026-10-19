# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/diff_page_js_vs_py.py — differential test of the page controller: the page's own state-changing functions (Node VM) vs engine/page.py, whole-state comparison.
#
# VERSION HISTORY
# v1.8.1 · 2026-10-18 · FAIL_PORTFOLIO_DAY switch (default on): the models harness, which shares this fixture server, turns the failing portfolio loads off so its own cases keep their strength.
# v1.8.0 · 2026-10-18 · add_catalogue_model cases pad the target portfolio to 9 / 10 strategies; refresh_active_portfolio_view_twice (two overlapping calls; wrapper mode only: the Python event-loop model cannot overlap one-go calls).
# v1.7.0 · 2026-10-18 · wrapper mode: the oracle is the ORIGINAL page's JS result (state, effects, fetches, return value), not the Python expectation: the wrapper runs on the real event loop, so a hop-count quirk of the Python event-loop model in a failure path must not decide it.
# v1.6.0 · 2026-10-18 · failing /api/portfolio_day (1 in 7 URLs); refresh_live_data_filter_change (one call, filter changed while in flight); frame / baseline at the boundary for refresh_live_data; extras (data-layer flags + criteria sizes) compared against the original in wrapper mode.
# v1.5.0 · 2026-10-18 · view calls record their arguments (vargs); in wrapper mode they are compared against the original page's (args-bearing views: setLiveBadge, cacheLiveChartResponse); engine-answer rounds 8 -> 30.
# v1.4.2 · 2026-10-18 · move_model_between_portfolios cases include a destination at / just under the ten-strategy limit.
# v1.3.0 · 2026-10-17 · refreshPointInTimeHistory direct group (hourly cohorts) with a response matrix; history state fields.
# v1.4.1 · 2026-10-18 · the Python expectation leaves out 'dom' effects (engine-emitted DOM writes; the JS stubs do not record DOM writes).
# v1.4.0 · 2026-10-17 · DIFF_WRAPPERS=1: run the engine-delegating controller wrappers (tools/controller_wrappers.py) instead of the originals; two passes (collect the requests, answer them with engine.rpc), compared with the Python expectation.
# v1.3.1 · 2026-10-17 · refresh_point_in_time_history_twice (overlapping hourly-cohort refreshes).
# v1.2.0 · 2026-10-17 · assignedPortfolioOverlayRule / activePortfolioOverlayRule direct groups; richer state (long names, 10+ members, live events, pinned / history maps, crypto, auto rank / minutes); refreshLiveData twice (stale response).
# v1.1.0 · 2026-10-17 · fetch stub delivers each response as its own macrotask (issue order); settle waits on macrotasks; opt-in visibleModels write trace (DIFF_DEBUG_ID).
# v1.0.0 · 2026-10-17 · Initial version: random page states -> run the page function and the Python method -> compare the full state (68 fields), recorded effects, requested URLs and return value.
"""Usage: python diff_page_js_vs_py.py [page.html] [--inventory inventory.json] [--methods a,b,c] [--cases N]
Each case: a random PageState + hooks (max frames, replay head, eligible models) + a fixture responder. The Python side runs first
against a recording transport; the recorded responses are then handed to the JS side, so a URL only one side requests shows up as a 404."""
import argparse
import copy
import hashlib
import json
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import data_client as dc  # noqa: E402
from engine import page_utils as pu  # noqa: E402
from engine.page import LivePortfolioRefused, Page  # noqa: E402
from engine.page_state import FIELDS, PageState, js_state_code  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("page", nargs="?", default=str(ROOT / "top10_5min_equity_curves_source_v2.65.34.html"))
ap.add_argument("--inventory", default=str(ROOT / "inventory_v2.65.34" / "inventory.json"))
ap.add_argument("--methods", default="")
ap.add_argument("--cases", type=int, default=150)
ns = ap.parse_args()
PAGE, INVENTORY = Path(ns.page), Path(ns.inventory)
API = "http://api"
TOL = 1e-9

PAGE_FUNCS = [
    "movePortfolio", "uniquePortfolioName", "markPortfolioFixed", "capturePortfolioScenario", "removeModelFromPortfolio", "removePortfolios",
    "deletePortfolio", "deleteSelectedPortfolios", "addCatalogueModel", "moveModelBetweenPortfolios", "getMergedPortfolioModels",
    "createSimilarPortfolio", "repopulateActivePortfolioFromCriteria", "livePortfolioModelsForDate", "autoPinLivePortfolioStrategies",
    "syncPortfolioViewRefresh", "refreshActivePortfolioView", "currentPortfolioViewConfig", "applyPortfolioViewConfig",
    "persistPortfolioViewConfig", "applyChartLock", "updateAutoRefreshTop1Status", "resetAutomaticRankSchedule", "scheduleAutomaticTop1Refresh",
    "schedulePointInTimeSelection", "applySelectedTime", "triggerSelectedTimeRefresh", "startReplay", "pauseReplay", "switchDate",
    "setRankingCriteria", "activatePortfolio", "assignedPortfolioOverlayRule", "activePortfolioOverlayRule",
    # dependencies, real
    "refreshLiveData", "fetchPortfolioData", "loadPortfolioData", "loadOverlayRuleLibrary", "ensureHistoricalDataLoaded", "syncTpSlScenarios",
    "rememberPortfolioView", "getLastPortfolioView", "getPersistedPortfolioViewCache", "refreshPointInTimeSelection",
    "finishAutomaticTop1Refresh", "retainSelectedTimeLeaders", "pointInTimeRequestOptions", "pointInTimeContextKey", "portfolioScenarioConfig",
    "selectedTimeRankCount", "clockMinutes", "replayClockTime", "nextAutomaticTop1Minute", "modelPointAtOrBeforeTime", "selectedTimeJoinAt",
    "selectedTimeModelEligibleAt", "timeOfDayMinutes", "isMetricAwareCriteria", "refreshPointInTimeHistory",
    "loadModelSearchFromDatabase", "loadDeepLinkModelsFromDatabase", "modelSearchTerms",
]

PAGE_EXTRA = js_state_code() + r"""
globalThis.API_BASE = 'http://api';
globalThis.location = { href: 'http://h/p/page.html', protocol: 'http:', origin: 'http://h' };
globalThis.history = { replaceState(){} };
var __fx = [], __calls = [], __timers = [], __vargs = [];
var __dom = [];
const __el = (name = '?') => new Proxy({ options: [] }, { get: (t, p) => p === 'classList' ? { add(...a){ __dom.push([name, 'classList.add', a]); }, remove(...a){ __dom.push([name, 'classList.remove', a]); }, toggle(...a){ __dom.push([name, 'classList.toggle', a]); }, contains(){ return false; } }
  : (p in t ? t[p] : (typeof p === 'string' && /^(setAttribute|removeAttribute|appendChild|addEventListener|focus|close|showModal)$/.test(p) ? (...a) => { __dom.push([name, p, a]); } : undefined)),
  set: (t, p, v) => { if (typeof p === 'string') __dom.push([name, p, v]); t[p] = v; return true; } });
globalThis.document = { getElementById: () => null, createElement: () => __el(), hidden: false };
['chartLockBtn','chartLockIcon','chartLockLabel','playBtn','stepBackBtn','stepFwdBtn','restartBtn','setBaseAtHeadBtn','resetBaselineBtn','scrubberTrack',
 'productTypeFilter','modelLimitFilter','winRateSlider','winRateValBadge','winRateDisplayBadge','productFilter','autoRefreshTop1Toggle','autoRefreshTop1Interval',
 'applySelectedTimeBtn','returnTypeNetBtn','returnTypeAltBtn','playIcon','playBtnText','catalogPortfolioFilter','portfolioList','similarStrategyModal',
 'modelSearchStatus'].forEach(n => { globalThis[n] = __el(n); });
['updateDateLabelAndTitle','updateScrubberUI','updateRibbon','renderCards','drawChart','updateScenarioUI','updatePointInTimeToggleUI','syncLiveAltReporting',
 'syncLiveModeUI','setupDateTabs','renderPortfolioTabs','syncAssignedOverlayRuleUI','updateStrategyFamilyOptions','syncSplitModeControls',
 'renderLivePortfolioTransition','renderPointInTimeHistory','setLiveBadge','cacheLiveChartResponse','scheduleLiveChartCacheFallback','persistPortfolioView',
 'updateChartLockControlState','populateCataloguePortfolioOptions','renderStrategyCatalogue','refreshLiveStoreUi'].forEach(n => { globalThis[n] = function(...a){ if (globalThis.__recordViews) { __fx.push(['view', n]); __vargs.push([n, JSON.stringify(a).replace(/Live · updated [^"]*/, 'Live · updated T')]); } }; });
globalThis.liveChartCacheKey = () => 'k';
globalThis.paintLiveChartCache = () => { if (globalThis.__recordViews) __fx.push(['view', 'paintLiveChartCache']); return false; };
globalThis.isLiveModePortfolio = () => false; globalThis.isLiveModeArmed = () => false;
globalThis.confirm = () => true; globalThis.alert = () => {};
globalThis.savePortfolios = () => { __fx.push(['savePortfolios']); };
globalThis.saveCriteriaWorkspaces = () => { __fx.push(['saveCriteriaWorkspaces']); };
globalThis.renderPortfolioList = () => { __fx.push(['renderPortfolioList']); };
globalThis.__realRefreshHistory = typeof refreshPointInTimeHistory === 'function' ? refreshPointInTimeHistory : null;
globalThis.__realHistory = (...a) => globalThis.__realRefreshHistory(...a);
globalThis.refreshPointInTimeHistory = () => { __fx.push(['refreshPointInTimeHistory']); };
globalThis.renderPointInTimeHistory = () => { __fx.push(['renderPointInTimeHistory']); };
globalThis.pointInTimeHistoryPanel = { classList: { contains: k => k === 'hidden' && globalThis.pointInTimeHistoryPanelHidden } };
globalThis.startPlaybackLoop = () => { __fx.push(['startPlaybackLoop']); globalThis.replayInterval = 1; };
globalThis.localStorage = { setItem: (k) => { __fx.push(['localStorage.setItem', k]); }, getItem: () => null };
globalThis.setTimeout = (fn, ms) => { __fx.push(['setTimeout', ms]); return 1; };
globalThis.clearTimeout = () => { __fx.push(['clearTimeout']); };
globalThis.setInterval = (fn, ms) => { __fx.push(['setInterval', ms]); return 1; };
globalThis.clearInterval = () => { __fx.push(['clearInterval']); };
globalThis.window = { setTimeout: (fn, ms) => { __fx.push(['setTimeout', ms]); return 1; } };
globalThis.getEligibleModels = () => globalThis.__elig;
globalThis.getScenarioCandidates = () => globalThis.__candidates;
globalThis.pointInTimeAtReplayHead = () => globalThis.__head;
var portfolioMergeSelection, portfolioMergeSelection2, PORTFOLIO_VIEW_CACHE = new Map(), PORTFOLIO_VIEW_REQUESTS = new Map(), PORTFOLIO_LAST_VIEW_CACHE = new Map(),
  PORTFOLIO_VIEW_CACHE_MAX = 32, PORTFOLIO_VIEW_CACHE_STORAGE_KEY = 'pv', persistedPortfolioViewCache = null, historicalCurveLoads = new Map(),
  TP_SL_SCENARIO_IDS = new Set(), liveChartDataLoadedKeys = new Set(), productFilterDummy = null, initialLiveDataAvailable = false, pendingFilterDataRefresh = false,
  overlayRuleLibrary = { rules: [], assignments: {} }, overlayRuleLibraryRequest = null, mainScenarioViewConfig = null, livePortfolioActiveModels = {},
  MOMENTUM_SCENARIO_IDS = new Set(['top3_momentum_net', 'top3_momentum_alt']), pointInTimeHistoryNearViewport = false, modelSearchTimer = null,
  pointInTimeDebounceTimer = null, deepLinkModel = '', portfolioViewRefreshTimer = null, pointInTimeRequestSequence = 0, selectedTimeInput = __el('selectedTimeInput'),
  pointInTimeStatus = { textContent: '', className: '' }, SCENARIOS_CATALOGUE = [], ALL_CRITERIA_DATA = {}, replayInterval = null,
  portfolioViewConfigs = {}, strategyCatalogue = [], similarStrategyPayload = null;
function __fetchStub(fx){ __calls = [];
  globalThis.fetch = async (url) => { const u = String(url); __calls.push(u); await new Promise(res => __imm(res)); const r = fx[u] || { status: 404, payload: { error: 'not found' } };
    return { ok: r.status >= 200 && r.status < 300, status: r.status, json: async () => r.payload }; }; }
globalThis.__engReq = []; globalThis.__engMode = 'off'; globalThis.__engResp = {};
globalThis.__engine = { call(req) { const key = JSON.stringify(req); __engReq.push(key);
  if (__engMode === 'collect') { const k = __engResp[key]; return k !== undefined && !k.startsWith('ERROR:') ? JSON.parse(k) : { ret: null, state: req.state, effects: [] }; }
  const t = __engResp[key]; if (t === undefined) throw new Error('no engine answer recorded for ' + req.method); if (t.startsWith('ERROR:')) throw new Error(t); return JSON.parse(t); } };
async function __page(fx, name, c, args){
  __fetchStub(fx); __fx = []; __dom = []; __vargs = []; globalThis.__recordViews = true; globalThis.__engReq = []; globalThis.__engMode = c.engMode || 'off'; globalThis.__engResp = c.engResp || {}; globalThis.__engineHooks = c.hooks;
  __ps_set(c.state);
  globalThis.portfolioViewConfigs = c.state.portfolio_view_configs; globalThis.livePortfolioStore = c.state.live_store;
  globalThis.__maxFrames = c.hooks.maxFrames; globalThis.__head = c.hooks.head; globalThis.__elig = c.hooks.eligible; globalThis.__candidates = c.hooks.candidates;
  globalThis.ALL_CRITERIA_DATA = c.criteria; globalThis.overlayRuleLibrary = c.library; globalThis.overlayRuleLibraryRequest = null;
  globalThis.PORTFOLIO_VIEW_CACHE = new Map(c.viewCache); globalThis.PORTFOLIO_VIEW_REQUESTS = new Map();
  globalThis.PORTFOLIO_LAST_VIEW_CACHE = new Map(c.lastView); globalThis.historicalCurveLoads = new Map(); globalThis.TP_SL_SCENARIO_IDS = new Set();
  globalThis.SCENARIOS_CATALOGUE = []; globalThis.pointInTimeRequestSequence = c.state.pit_request_sequence;
  globalThis.deepLinkModel = ''; globalThis.pendingFilterDataRefresh = false; liveChartDataLoadedKeys.clear(); globalThis.initialLiveDataAvailable = false;
  let ret;
  __dom = [];   // the writes made while the page set up its mirrored state are not part of the call
  let dbg = null;
  globalThis.__vlog = [];
  if (c.trace) { let __vm = globalThis.visibleModels; Object.defineProperty(globalThis, 'visibleModels', { configurable: true, get(){ return __vm; },
    set(v){ __vm = v; globalThis.__vlog.push([new Error().stack.split('\n').slice(2, 5).map(x => x.trim().slice(0, 70)), [...v]]); } }); }
  if (name === 'addCatalogueModel') { globalThis.catalogPortfolioFilter = { value: args[0] }; args = [args[1]]; }
  args = args.map(a => a === '__undef__' ? undefined : a);
  try {
    if (name === '__twiceLive') {
      const a = refreshLiveData(args[0]);
      if (args[2] === 'change_filter') globalThis.modelLimit = globalThis.modelLimit !== 20 ? 20 : 10;
      const b = refreshLiveData(args[1]);
      await a; await b;
    } else if (name === '__twiceView') {
      const a = refreshActivePortfolioView(); const b = refreshActivePortfolioView(); await a; await b;
    } else if (name === '__filterLive') {
      const a = refreshLiveData(args[0]); globalThis.modelLimit = globalThis.modelLimit !== 20 ? 20 : 10; await a;
    } else if (name === '__twiceHistory') {
      const a = __realRefreshHistory(); globalThis.pointInTimeHistoryKey = ''; const b = __realRefreshHistory();
      await a; await b;
    } else ret = await globalThis[name](...args);
  } catch (e) { ret = { error: true }; dbg = String(e && e.message || e); }
  for (let i = 0; i < 40; i++) await new Promise(res => __imm(res));
  const norm = e => [e[0], { models: e[1].models, cachedAt: Math.abs(e[1].cachedAt - Date.now()) < 120000 ? 'NOW' : e[1].cachedAt }];
  return { state: __ps_get(), effects: __fx, calls: __calls, dom: __dom, vargs: __vargs, extras: { loaded: [...liveChartDataLoadedKeys].sort(), initial: initialLiveDataAvailable, pending: pendingFilterDataRefresh,
    crit: Object.fromEntries(Object.entries(ALL_CRITERIA_DATA).map(([k, v]) => [k, Object.fromEntries(Object.entries(v).map(([d, l]) => [d, Array.isArray(l) ? l.length : null]))])) }, ret: ret === undefined ? null : ret, criteriaKeys: Object.keys(ALL_CRITERIA_DATA).sort(),
    library: overlayRuleLibrary, viewCache: [...PORTFOLIO_VIEW_CACHE.entries()].map(norm), _dbg: dbg, _vlog: c.trace ? globalThis.__vlog : null, _engReq: globalThis.__engReq };
}
"""

JS_NAME = {"move_portfolio": "movePortfolio", "unique_portfolio_name": "uniquePortfolioName", "mark_portfolio_fixed": "markPortfolioFixed",
           "capture_portfolio_scenario": "capturePortfolioScenario", "remove_model_from_portfolio": "removeModelFromPortfolio",
           "remove_portfolios": "removePortfolios", "delete_portfolio": "deletePortfolio", "delete_selected_portfolios": "deleteSelectedPortfolios",
           "add_catalogue_model": "addCatalogueModel", "move_model_between_portfolios": "moveModelBetweenPortfolios",
           "get_merged_portfolio_models": "getMergedPortfolioModels", "create_similar_portfolio": "createSimilarPortfolio",
           "repopulate_active_portfolio_from_criteria": "repopulateActivePortfolioFromCriteria",
           "live_portfolio_models_for_date": "livePortfolioModelsForDate", "auto_pin_live_portfolio_strategies": "autoPinLivePortfolioStrategies",
           "sync_portfolio_view_refresh": "syncPortfolioViewRefresh", "refresh_active_portfolio_view": "refreshActivePortfolioView",
           "current_portfolio_view_config": "currentPortfolioViewConfig", "apply_portfolio_view_config": "applyPortfolioViewConfig",
           "persist_portfolio_view_config": "persistPortfolioViewConfig", "apply_chart_lock": "applyChartLock",
           "reset_automatic_rank_schedule": "resetAutomaticRankSchedule", "schedule_automatic_top1_refresh": "scheduleAutomaticTop1Refresh",
           "schedule_point_in_time_selection": "schedulePointInTimeSelection", "apply_selected_time": "applySelectedTime",
           "trigger_selected_time_refresh": "triggerSelectedTimeRefresh", "start_replay": "startReplay", "pause_replay": "pauseReplay",
           "switch_date": "switchDate", "set_ranking_criteria": "setRankingCriteria", "activate_portfolio": "activatePortfolio",
           "refresh_live_data": "refreshLiveData", "refresh_point_in_time_selection": "refreshPointInTimeSelection",
           "load_portfolio_data": "loadPortfolioData", "refresh_live_data_twice": "__twiceLive", "refresh_live_data_filter_change": "__filterLive", "refresh_active_portfolio_view_twice": "__twiceView", "refresh_point_in_time_history_twice": "__twiceHistory", "update_auto_refresh_status": "updateAutoRefreshTop1Status",
           "refresh_point_in_time_history": "__realHistory", "load_model_search_from_database": "loadModelSearchFromDatabase",
           "load_deep_link_models_from_database": "loadDeepLinkModelsFromDatabase", "assigned_portfolio_overlay_rule": "assignedPortfolioOverlayRule", "active_portfolio_overlay_rule": "activePortfolioOverlayRule"}


RET_KEEP = {"assigned_portfolio_overlay_rule", "active_portfolio_overlay_rule", "move_portfolio", "unique_portfolio_name", "get_merged_portfolio_models", "live_portfolio_models_for_date",
            "current_portfolio_view_config", "load_portfolio_data"}


# ---------------------------------------------------------------------------------------------------------------- comparison
def diff(py, js, path=""):
    if isinstance(py, dict):
        if not isinstance(js, dict):
            return f"{path}: py dict vs js {type(js).__name__}"
        if set(py) != set(js):
            return f"{path}: keys differ py-only {sorted(set(py) - set(js))} js-only {sorted(set(js) - set(py))}"
        for k, v in py.items():
            d = diff(v, js[k], f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(py, list):
        if not isinstance(js, list) or len(py) != len(js):
            if path.endswith("effects") and isinstance(js, list):
                return f"{path}: py {json.dumps(py)[:260]} vs js {json.dumps(js)[:260]}"
            return f"{path}: length py {len(py) if isinstance(py, list) else py!r} vs js {len(js) if isinstance(js, list) else js!r}"
        for i, (a, b) in enumerate(zip(py, js)):
            d = diff(a, b, f"{path}[{i}]")
            if d:
                return d
        return None
    if isinstance(py, (int, float)) and isinstance(js, (int, float)) and not isinstance(py, bool) and not isinstance(js, bool):
        return None if abs(py - js) <= TOL else f"{path}: py {py} vs js {js}"
    return None if py == js else f"{path}: py {py!r} vs js {js!r}"


# ---------------------------------------------------------------------------------------------------------------- fixtures
def mk(i, n=3, product="gbp", start=0):
    return {"model": f"M{i}", "product": product, "strategy": "breakout", "color": f"#0000{i % 10}{i % 10}",
            "series": [{"time": f"{h + start:02d}:00", "net": float(i * (h + 1)), "buy": float(i), "sell": float(h)} for h in range(n)]}


FAIL_PORTFOLIO_DAY = True   # the page harness exercises failing portfolio loads; the models harness (which shares this server) switches it off


def responder(url: str):
    """Deterministic fake server keyed by URL (the same body for the same URL on both sides)."""
    from urllib.parse import parse_qs, urlparse
    u = urlparse(url)
    q = {k: v[0] for k, v in parse_qs(u.query).items()}
    seed = int(hashlib.md5(url.encode()).hexdigest()[:6], 16)
    if u.path.endswith("/api/live_day"):
        if seed % 6 == 0:
            return 500, {"error": "down"}   # some live-day requests fail: the page shows its offline badge
        scen = q.get("scenario", "top_net")
        return 200, {"products": ["gbp", "eur"], scen: [mk(1 + seed % 3), mk(5 + seed % 4)], "top_net": [mk(2)], "generated_at": "2026-10-14T12:00:00"}
    if u.path.endswith("/api/portfolio_day"):
        if FAIL_PORTFOLIO_DAY and seed % 7 == 0:
            return 500, {"error": "db down"}   # some portfolio loads fail: the controllers' catch paths
        ids = [m for m in q.get("models", "").split(",") if m]
        return 200, {"models": [mk(int(hashlib.md5(m.encode()).hexdigest()[:4], 16) % 90 + 1, start=seed % 3 * 2) | {"model": m} for m in ids], "generated_at": "2026-10-14T12:00:00"}
    if u.path.endswith("/api/overlay_rules"):
        return 200, {"rules": [{"id": "r1", "name": "R1", "config": {"interval_minutes": 30, "rules": [{"type": "ranked_top", "metric": "cum_net"}]}}],
                     "assignments": {"P1": "r1"}}
    if u.path.endswith("/api/point_in_time_scenario_hours"):
        pick = seed % 5
        if pick == 0:
            return 500, {}
        if pick == 1:
            return 400, {"error": "no hours"}
        if pick == 2:
            return 200, {"hours": "oops"}
        return 200, {"hours": [{"hour": f"{h:02d}:00", "models": [mk(1)]} for h in range(seed % 4)]}
    if u.path.endswith("/api/point_in_time_scenario"):
        return 200, {"models": [mk(1), mk(2), mk(3)], "at_time": q.get("at")}
    if "historical_curve_data" in u.path:
        return 200, {"top_net": [mk(7)]}
    return 404, {"error": "not found"}


class RecordingTransport:
    def __init__(self):
        self.calls, self.fx = [], {}

    def __call__(self, url):
        self.calls.append(url)
        st, body = responder(url)
        self.fx[url] = {"status": st, "payload": body}
        return st, body


# ---------------------------------------------------------------------------------------------------------------- random states
DATES = ["2026-10-13", "2026-10-14", "2026-10-15"]
CRITERIA = ["top_net", "top_alt_net", "top_win", "top1_at_time", "top3_momentum_net", "family_leaders", "top5_breakout", "top3_tp3_sl3"]


def rand_state(rng: random.Random) -> dict:
    n_port = rng.choice([0, 1, 2, 3, 4])
    names = rng.sample(["P1", "P2", "P3", "Alpha", "Beta", "X" * 32], n_port)
    portfolios = [[n, [f"M{rng.randint(1, 13)}" for _ in range(rng.choice([0, 1, 3, 9, 14, 16, 22]))]] for n in names]
    for pair in portfolios:
        pair[1] = list(dict.fromkeys(pair[1]))[:rng.choice([10, 10, 9, 11, 12])]
    active = rng.choice([None] + names)
    live = rng.choice(["2026-10-14", "2099-01-01"])
    date = rng.choice(DATES)
    st = PageState()
    st.update({
        "portfolios": dict((n, m) for n, m in portfolios), "active_portfolio": active, "current_date": date, "live_date": live,
        "current_criteria": rng.choice(CRITERIA), "return_type": rng.choice(["NET", "ALT"]), "product_type": rng.choice(["all", "forex"]),
        "product": rng.choice(["all", "gbp"]), "strategy_family": rng.choice(["all", "breakout"]), "model_limit": rng.choice([10, 20]),
        "min_win_rate": rng.choice([0, 5]), "split_mode": rng.choice(list(pu.SPLIT_MODES)), "chart_locked": rng.choice([False, True]),
        "use_assigned_rule": rng.choice([False, True]), "rank_select_value": rng.choice(["1", "3", "12"]),
        "selected_time_input": rng.choice(["", "10:00", "bad"]), "auto_direction_select": rng.choice(["top", "bottom"]),
        "auto_rank_select": rng.choice(["1", "2", "9"]), "auto_enabled": rng.choice([False, True]), "auto_direction": rng.choice(["top", "bottom"]),
        "auto_rank": rng.choice([1, 2]), "auto_minutes": rng.choice([5, 15, 30]), "auto_last_minute": rng.choice([None, 590, 610]),
        "auto_next_minute": rng.choice([None, 600, 615]), "auto_context": rng.choice(["", "x"]), "auto_request_at": rng.choice([None, None, "10:00"]),
        "pending_explicit_time": rng.choice([None, "10:00"]), "explicit_refresh": rng.choice([False, False, True]),
        "pit_mode": rng.choice([False, True]), "pit_models": rng.choice([None, [], [mk(1)]]), "pit_requested_key": rng.choice(["", "k"]),
        "pit_request_sequence": rng.randint(0, 3), "pit_history_key": rng.choice(["", "h"]), "pit_history_sequence": rng.randint(0, 3),
        "pit_timeline_models": rng.choice([[], [mk(2)]]), "pit_selection_preference": rng.choice([True, False]),
        "history_context": rng.choice(["", "ctx"]), "top1_prev_mode": rng.choice([None, True, False]), "search_loaded": rng.choice([[], [mk(4)]]),
        "search_sequence": rng.randint(0, 3), "deep_link_only": rng.choice([False, False, True]),
        "portfolio_models": rng.choice([[], [mk(1), mk(2)]]), "visible": set(rng.sample(["M1", "M2", "M3"], rng.randint(0, 3))),
        "selected_model_index": rng.randint(0, 2), "frame": rng.choice([-1, 0, 1, 2]), "baseline": rng.choice([0, 0, 1]),
        "is_playing": rng.choice([False, False, True]), "replay_interval": rng.choice([None, 1]), "date_switch_sequence": rng.randint(0, 3),
        "live_refresh_sequence": rng.randint(0, 3), "available_dates": [{"id": d, "label": d} for d in DATES],
        "main_criteria": rng.choice(["top_net", "top_win"]), "main_view_config": rng.choice([None, {"criteria": "top_win", "returnType": "ALT", "limit": 20}]),
        "model_search_input": rng.choice(["", "M1", "abcdefg", "abcde", "abcdef"]), "merge_selection": rng.sample(names, rng.randint(0, len(names))) + (["Ghost"] if rng.random() < 0.3 else []),
        "pit_status": ["", ""], "auto_status_text": "", "pit_history_near_viewport": rng.choice([True, True, False]), "pit_history_panel_hidden": rng.choice([False, False, True]),
        "pit_hours": rng.choice([[], [{"hour": "09:00"}]]), "pit_history_at": rng.choice(["", "09:00"]), "pit_history_status_text": rng.choice(["", "old"]), "live_refresh_in_flight": rng.random() < 0.2, "portfolio_refresh_timer": rng.choice([None, 1]),
    })
    for n in names:
        if rng.random() < 0.5:
            st.portfolio_criteria[n] = rng.choice(CRITERIA)
        if rng.random() < 0.4:
            st.portfolio_scenario_configs[n] = {"criteria": rng.choice(CRITERIA), "returnType": "NET", "productType": "all", "product": "all",
                                                 "strategyFamily": "all", "limit": 10, "minWinRate": 0}
        if rng.random() < 0.5:
            st.portfolio_view_configs[n] = {"date": rng.choice(DATES + ["2025-01-01"]), "replayHeadTime": rng.choice(["", "01:00", "00:30"]),
                                            "selectedAtTime": rng.choice(["", "09:30"]), "criteria": rng.choice(CRITERIA), "returnType": rng.choice(["NET", "ALT"]),
                                            "splitMode": rng.choice(list(pu.SPLIT_MODES) + ["x"]), "chartLocked": rng.choice([False, True, None]),
                                            "useAssignedOverlayRule": rng.choice([True, False, None]), "productType": rng.choice(["all", "forex", "crypto", "bogus"]), "autoAddEnabled": rng.choice([True, False]),
                                            "autoAddMinutes": rng.choice([1, 15, 7, 5, 30, 60, 120]), "autoAddRank": rng.choice([1, 2, 5, 6, 0, None]), "limit": rng.choice([10, 20, 30, 99]), "minWinRate": rng.choice([0, 50, 150])}
    st.live_store = {"events": [{"portfolio": rng.choice(["LIVE", "live", "LIVE_ALT", "P1", "Alpha"]), "switched_at": f"{rng.choice(DATES)}T{rng.choice(['09', '10', '11'])}:{rng.choice(['00', '30'])}:00",
                                 "from_model": rng.choice([None, "M1", "M2", " M3 "]), "to_model": rng.choice(["M4", "M2", "", None])} for _ in range(rng.choice([0, 3, 6]))],
                     "states": {"LIVE": {"active_model": rng.choice([None, "M7"]), "last_switch": rng.choice([None, {"switched_at": f"{rng.choice(DATES)}T10:00:00", "from_model": "M5", "to_model": "M6"}])}}}
    for k in range(rng.choice([0, 0, 2, 3])):
        st.pinned[f"M{k + 5}"] = mk(k + 5)
        st.history[f"M{k + 9}"] = {"model": f"M{k + 9}", "joined_at": "09:00", "color": "#abcdef"}
    st.similar_payload = {"groups": {"family": [{"model": f"M{i}"} for i in range(1, rng.choice([3, 13]))], "tp": [{"model": "M3"}] * rng.choice([0, 1])}, "reference": {"product": "gbp", "window": rng.choice([None, 5]), "tp": 3, "sl": 5}}
    return st.snapshot()


def rand_case(rng: random.Random, method: str):
    snap = rand_state(rng)
    st = PageState.from_snapshot(snap)
    ports = list(st.portfolios)
    pick = lambda: rng.choice(ports) if ports else "Nope"  # noqa: E731
    hooks = {"maxFrames": rng.choice([1, 3, 5]), "head": rng.choice([None, "10:05", "00:00", "11:00"]),
             "eligible": rng.choice([[], [mk(1), mk(2)]]), "candidates": [mk(i) for i in range(1, rng.choice([2, 12]))]}
    args = []
    if method == "move_portfolio":
        args = [pick(), rng.choice([-1, 1, 2, 0, "1", 1.5])]
    elif method == "unique_portfolio_name":
        args = [rng.choice(ports + ["New", "X" * 40, "Alpha"]) if ports else "New"]
        if rng.random() < 0.5 and ports:
            args = [ports[0]]
    elif method in ("mark_portfolio_fixed", "delete_portfolio", "activate_portfolio"):
        args = [pick() if rng.random() < 0.9 else None]
        if method == "activate_portfolio":
            args = [rng.choice([n for n in ports if n.upper() not in ("LIVE", "LIVE_ALT")] or ["Nope"])]
    elif method == "capture_portfolio_scenario":
        args = [pick()] + ([] if rng.random() < 0.5 else [rng.choice(CRITERIA)])
    elif method in ("remove_model_from_portfolio",):
        p = pick()
        args = [p, rng.choice((st.portfolios.get(p) or ["M1"]) + ["M9"])]
    elif method == "remove_portfolios":
        args = [rng.sample(ports, rng.randint(0, len(ports))) + (["Ghost"] if rng.random() < 0.2 else [])]
    elif method == "add_catalogue_model":
        args = [pick(), rng.choice(["M1", "M5", "M9"])]
        if len(ports) >= 1 and rng.random() < 0.4:   # the target portfolio at (or just under) the ten-strategy limit, without the model
            target = rng.choice(ports)
            table = {n: list(models) for n, models in snap["portfolios"]}
            table[target] = [f"Z{i}" for i in range(rng.choice([9, 10]))]
            snap["portfolios"] = [[n, table[n]] for n, _ in snap["portfolios"]]
            st = PageState.from_snapshot(snap)
            args = [target, rng.choice(["M1", "M5", "M9"])]
    elif method == "refresh_active_portfolio_view_twice":
        if ports:   # an active portfolio with members, viewed on the live date: otherwise the controller returns at once
            table = {n: list(models) for n, models in snap["portfolios"]}
            target = rng.choice(ports)
            table[target] = table[target] or ["M1", "M2"]
            snap["portfolios"] = [[n, table[n]] for n, _ in snap["portfolios"]]
            snap["active_portfolio"], snap["current_date"] = target, snap["live_date"]
            st = PageState.from_snapshot(snap)
        args = []
    elif method == "move_model_between_portfolios":
        a, b = pick(), pick()
        if len(ports) >= 2 and rng.random() < 0.4:   # a real move into a destination at (or just under) the ten-strategy limit
            a, b = rng.sample(ports, 2)
            table = {n: list(models) for n, models in snap["portfolios"]}   # the snapshot keeps portfolios as [name, models] pairs, in tab order
            if not table.get(a):
                table[a] = ["M1", "M2"]
            table[b] = [f"Z{i}" for i in range(rng.choice([9, 10]))]
            snap["portfolios"] = [[n, table[n]] for n, _ in snap["portfolios"]]
            st = PageState.from_snapshot(snap)
            args = [a, b, rng.choice(st.portfolios[a])]
        else:
            args = [a, b, rng.choice((st.portfolios.get(a) or ["M1"]) + ["M9"])]
    elif method == "create_similar_portfolio":
        args = [rng.choice(["family", "tp", "window", "bogus"])]
    elif method == "live_portfolio_models_for_date":
        args = [rng.choice(ports + ["live", "LIVE"]) if ports else "live", rng.choice(DATES), rng.choice([None, "M3"])]
    elif method == "apply_portfolio_view_config":
        args = [st.portfolio_view_configs.get(pick()) or rng.choice([None, {"criteria": "top_win"}, {"returnType": "ALT", "splitMode": "TRI_SPLIT", "limit": "20"}])]
    elif method == "persist_portfolio_view_config":
        args = [rng.choice(ports + [None]) if ports else None]
    elif method == "apply_chart_lock":
        args = [rng.choice([True, False]), rng.choice([True, False])]
    elif method == "schedule_automatic_top1_refresh":
        args = [rng.choice(["10:00", "10:05", "bad", "09:00", "11:30"])]
    elif method == "switch_date":
        args = [rng.choice(DATES + ["WEEK_OVERALL", "bad"]), {"skipPortfolioLoad": rng.choice([False, True]), "refreshData": rng.choice([False, True])}]
    elif method == "set_ranking_criteria":
        args = [rng.choice(CRITERIA + ["top_net"])]
    elif method == "refresh_live_data":
        args = [rng.choice(["__undef__", st.current_date, "2026-10-13"]), {"skipPortfolioRefresh": rng.choice([False, True])}]
    elif method == "refresh_point_in_time_history" and rng.random() < 0.3:
        probe = Page(PageState.from_snapshot(snap), dc.DataClient(None, API))
        snap["pit_history_key"] = pu.point_in_time_context_key(probe._opt_state())
        st = PageState.from_snapshot(snap)
    elif method == "assigned_portfolio_overlay_rule":
        args = rng.choice([[], [pick()], [None], ["Alpha"], ["P1"]])
    elif method == "update_auto_refresh_status":
        args = rng.choice([[], [""], ["Checking top #1 at 10:00"], ["On"]])
    elif method == "refresh_live_data_filter_change":
        args = [rng.choice([st.current_date, "2026-10-13"])]
    elif method == "refresh_live_data_twice":
        args = [st.current_date, rng.choice([st.current_date, "2026-10-13"]), rng.choice(["same", "change_filter"])]
    elif method == "refresh_point_in_time_selection":
        args = [rng.choice([None, "10:05", "11:00"])]
    elif method == "load_portfolio_data":
        args = [{"preferCache": rng.choice([True, False])}]
    elif method == "load_model_search_from_database":
        pool = ["M1", "M2", "abc.def", "X_9", "bad id", "a$b", "M1,M2", "M3;M4", "M5 M6", "", "  ", "M1,M1", "ZZ-1"]
        term = rng.choice(pool + [",".join(f"N{i}" for i in range(rng.choice([11, 20, 25])))])
        args = [term]
        # the search box usually still holds the term when the answer arrives; sometimes it was edited meanwhile
        snap["model_search_input"] = term if rng.random() < 0.8 else rng.choice(["", "other", term + "x"])
        snap["search_sequence"] = rng.choice([0, 3, 7])
        st = PageState.from_snapshot(snap)
    elif method == "load_deep_link_models_from_database":
        pool = ["M1", "M2", "abc.def", "bad id", "a$b", "M1", " M3 ", "", "ZZ-1"]
        ids = [rng.choice(pool) for _ in range(rng.choice([0, 1, 2, 4]))]
        if rng.random() < 0.15:
            ids = [f"D{i}" for i in range(rng.choice([10, 12, 15]))]
        args = [rng.choice([ids, ids, None])]
        snap["deep_link_only"] = rng.choice([True, False])
        st = PageState.from_snapshot(snap)
    if method in ("refresh_live_data", "refresh_live_data_twice", "refresh_live_data_filter_change"):   # the head / baseline exactly at the last frame
        if rng.random() < 0.4:
            snap["frame"] = hooks["maxFrames"] - 1
        if rng.random() < 0.3:
            snap["baseline"] = hooks["maxFrames"] - 1
    library = {"rules": [{"id": "r1", "name": "R1", "config": {"interval_minutes": 30, "rules": []}}], "assignments": rng.choice([{}, {"P1": "r1"}, {"Alpha": "r1"}])}
    view_cache = []
    for n in ports:
        if rng.random() < 0.5 and st.portfolios.get(n):
            k = f"{st.current_date}|{','.join(st.portfolios[n])}"
            view_cache.append([k, {"models": [mk(3)], "cachedAt": rng.choice([1.0, 1792233508000.0])}])
    last_view = [[f"{st.current_date}|{ports[0]}", {"modelKey": "old", "entry": {"models": [mk(8)], "cachedAt": 5.0}}]] if ports and rng.random() < 0.3 else []
    criteria = {"top_net": {st.current_date: [mk(1)]}} if rng.random() < 0.5 else {}
    return {"state": snap, "hooks": hooks, "library": library, "viewCache": view_cache, "lastView": last_view, "criteria": criteria}, args


# ---------------------------------------------------------------------------------------------------------------- python side
def to_py_args(method, args):
    if method == "switch_date":
        o = args[1]
        return [args[0]], {"skip_portfolio_load": o["skipPortfolioLoad"], "refresh_data": o["refreshData"]}
    if method == "refresh_live_data":
        return [None if args[0] == "__undef__" else args[0]], {"skip_portfolio_refresh": args[1]["skipPortfolioRefresh"]}
    if method == "load_portfolio_data":
        return [], {"prefer_cache": args[0]["preferCache"]}
    if method in ("refresh_live_data_twice", "refresh_point_in_time_history_twice"):
        return list(args), {}
    return list(args), {}


def run_twice_live(page, st, date_a, date_b, mode):
    """Two overlapping refreshLiveData calls (the second may change a filter in between): only the newest, still-matching response may apply."""
    first = page.begin_refresh_live_data(date_a)
    if mode == "change_filter":
        st.model_limit = 20 if st.model_limit != 20 else 10
    second = page.begin_refresh_live_data(date_b)
    page._await(first)
    page._await(second)
    page.settle()
    return None


def run_filter_live(page, st, date):
    """One refreshLiveData call whose filter changes while the request is in flight: its answer must be dropped."""
    first = page.begin_refresh_live_data(date)
    st.model_limit = 20 if st.model_limit != 20 else 10
    page._await(first)
    page.settle()
    return None


def run_twice_history(page, st):
    """Two overlapping hourly-cohort refreshes with the same context (the key was reset in between): only the newest response may apply."""
    first = page.begin_refresh_point_in_time_history()
    st.pit_history_key = ""
    second = page.begin_refresh_point_in_time_history()
    page._await(first)
    page._await(second)
    page.settle()
    return None


def run_python(method, case, args):
    tr = RecordingTransport()
    cl = dc.DataClient(tr, API, live_date=case["state"]["live_date"], base_href="http://h/p/page.html")
    cl.overlay_rule_library = copy.deepcopy(case["library"])
    cl.criteria_data = copy.deepcopy(case["criteria"])
    for k, v in case["viewCache"]:
        cl.portfolio_view_cache[k] = dict(v)
    for k, v in case["lastView"]:
        cl.last_view[k] = copy.deepcopy(v)
    st = PageState.from_snapshot(case["state"])
    h = case["hooks"]
    page = Page(st, cl, max_frames=lambda: h["maxFrames"], head_time=lambda: h["head"], eligible=lambda: h["eligible"], candidates=lambda: h["candidates"])
    pa, kw = to_py_args(method, args)
    dbg = None
    try:
        if method == "refresh_live_data_twice":
            ret = run_twice_live(page, st, *pa)
        elif method == "refresh_live_data_filter_change":
            ret = run_filter_live(page, st, *pa)
        elif method == "refresh_active_portfolio_view_twice":
            page.refresh_active_portfolio_view()   # not a model of the overlap (one-go cannot overlap): only wrapper mode runs this case, against the original page's JS
            ret = page.refresh_active_portfolio_view()
        elif method == "refresh_point_in_time_history_twice":
            ret = run_twice_history(page, st)
        else:
            ret = getattr(page, method)(*pa, **kw)
        page.settle()
    except LivePortfolioRefused:
        ret = {"error": True}
    except Exception as e:  # noqa: BLE001
        ret = {"error": True}
        dbg = f"{type(e).__name__}: {e}"
    if method not in RET_KEEP and not (isinstance(ret, dict) and ret.get("error") is True):
        ret = None
    out = {"state": st.snapshot(), "effects": [e for e in st.effects if e[0] != "dom"], "calls": tr.calls, "ret": ret if ret is not None else None,
           "criteriaKeys": sorted(cl.criteria_data), "library": cl.overlay_rule_library, "_dbg": dbg, "_vlog": None,
           "viewCache": [[k, {"models": v["models"], "cachedAt": "NOW" if abs(v["cachedAt"] - 1792233508000.0) < 0 else v["cachedAt"]}]
                         for k, v in cl.portfolio_view_cache.items()]}
    return out, tr.fx


# ---------------------------------------------------------------------------------------------------------------- main
def main():
    methods = [m for m in ns.methods.split(",") if m] or list(JS_NAME)
    if not os.environ.get("DIFF_WRAPPERS"):
        methods = [m for m in methods if m != "refresh_active_portfolio_view_twice"]   # wrapper mode only
    rng = random.Random(11)
    cases, expected = [], {}
    for method in methods:
        for _ in range(ns.cases):
            case, args = rand_case(rng, method)
            exp, fx = run_python(method, case, args)
            # the JS wrapper passes args exactly as the page function takes them
            cid = len(cases) + 1
            cases.append({"id": cid, "call": "__page", "args": [fx, JS_NAME[method], {**case, "trace": str(cid) == os.environ.get("DIFF_DEBUG_ID")}, args], "method": method})
            expected[cid] = (method, exp)
    extra = PAGE_EXTRA
    wrapped = bool(os.environ.get("DIFF_WRAPPERS"))
    if wrapped:   # run the engine-delegating wrappers instead of the original functions
        import build_inventory
        import controller_wrappers as cw
        inv_data = build_inventory.build(PAGE)
        decls = cw.declarations(PAGE.read_text(encoding="utf-8"), {st["name"]: st["decl"] for st in inv_data["state"]})
        fns = {f["name"]: f for f in inv_data["functions"]}
        lines = PAGE.read_text(encoding="utf-8").split("\n")
        def _body(n):
            return "\n".join(lines[fns[n]["start_line"] - 1:fns[n]["end_line"]])
        extra += "\n" + cw.helper_block(decls) + "\n".join(cw.wrapper(n, _body(n), _body) for n in cw.CONTROLLERS)
        py_to_js = {v: k for k, v in JS_NAME.items()}
        wrapped_methods = {cw.CONTROLLERS[n][0] for n in cw.CONTROLLERS}
        if "refresh_live_data" in wrapped_methods:   # two overlapping calls: the page's event loop interleaves the engine stages
            wrapped_methods.add("refresh_live_data_twice")
            wrapped_methods.add("refresh_live_data_filter_change")
        wrapped_methods.add("refresh_active_portfolio_view_twice")
        cases = [c for c in cases if c["method"] in wrapped_methods]
        expected = {cid: v for cid, v in expected.items() if v[0] in wrapped_methods}
    spec = {"page": str(PAGE), "inventory": str(INVENTORY), "functions": PAGE_FUNCS, "extra": extra, "cases": [{k: v for k, v in c.items() if k != "method"} for c in cases]}
    workers = max(1, min(int(os.environ.get("DIFF_WORKERS", "8")), len(cases)))

    def run_js(case_list):
        out_results = []
        with tempfile.TemporaryDirectory() as td:
            procs = []
            for k in range(workers):
                sp = Path(td) / f"c{k}.json"
                sp.write_text(json.dumps({**spec, "cases": case_list[k::workers]}), encoding="utf-8")
                procs.append(subprocess.Popen(["node", str(ROOT / "tools" / "js_runner.js"), str(sp)], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
            for pr in procs:
                out, err = pr.communicate(timeout=3600)
                if pr.returncode != 0:
                    print("NODE FAILED:", err.decode("utf-8", "replace")[-1500:])
                    sys.exit(2)
                out_results.extend(json.loads(out.decode("utf-8")))
        return out_results

    if wrapped:
        from engine import rpc as _rpc
        pending_cases = {c["id"]: c for c in spec["cases"]}
        for c in spec["cases"]:
            c["args"][2]["engMode"], c["args"][2]["engResp"] = "collect", {}
        for _round in range(30):   # a controller's later requests depend on earlier answers (the fallback path): collect until no new request appears
            collected = {r["id"]: r for r in run_js(list(pending_cases.values()))}
            pending_cases = {}
            for cid, c in {c["id"]: c for c in spec["cases"]}.items():
                r = collected.get(cid)
                if r is None:
                    continue
                answers = c["args"][2]["engResp"]
                new_keys = [k for k in ((r["result"].get("_engReq") or []) if r["ok"] else []) if k not in answers]
                for key in new_keys:
                    try:
                        answers[key] = json.dumps(_rpc.dispatch(json.loads(key)))
                    except Exception as e:  # noqa: BLE001
                        answers[key] = f"ERROR: {type(e).__name__}: {e}"
                if new_keys:
                    pending_cases[cid] = c
            if not pending_cases:
                break
        for c in spec["cases"]:
            c["args"][2]["engMode"] = "answer"
    results = run_js(spec["cases"])
    res = {r["id"]: r for r in results}
    orig_dom = {}
    orig_vargs = {}
    orig_extras = {}
    orig_res = {}
    if wrapped:   # the same cases through the ORIGINAL page functions: the DOM writes (and nothing else) the wrapper must reproduce
        ospec = {**spec, "extra": PAGE_EXTRA, "cases": [{**c, "args": [c["args"][0], c["args"][1], {**c["args"][2], "engMode": "off", "engResp": {}}, c["args"][3]]} for c in spec["cases"]]}
        spec_backup, spec = spec, ospec
        orig_run = run_js(ospec["cases"])
        orig_res = {r["id"]: r for r in orig_run}
        if os.environ.get("DIFF_DEBUG_ID") and int(os.environ["DIFF_DEBUG_ID"]) in orig_res:
            print("DEBUG ORIG:", json.dumps(orig_res[int(os.environ["DIFF_DEBUG_ID"])]))
        orig_dom = {r["id"]: (r["result"].get("dom") if r["ok"] else None) for r in orig_run}
        orig_vargs = {r["id"]: (r["result"].get("vargs") if r["ok"] else None) for r in orig_run}
        orig_extras = {r["id"]: (r["result"].get("extras") if r["ok"] else None) for r in orig_run}
        spec = spec_backup
    summary, fails = {}, {}
    for cid, (method, exp) in expected.items():
        r = res[cid]
        s = summary.setdefault(method, {"cases": 0, "pass": 0, "js_error": 0})
        s["cases"] += 1
        if os.environ.get("DIFF_DEBUG_ID") == str(cid):
            print("DEBUG JS:", json.dumps(r))
            print("DEBUG PY:", json.dumps(exp, default=str))
            Path(os.environ.get("DIFF_DEBUG_FILE", "debug_case.json")).write_text(json.dumps({"method": method, "case": cases[cid - 1]["args"][2], "args": cases[cid - 1]["args"][3]}), encoding="utf-8")
            print("DEBUG CASE:", json.dumps({"method": method, "args": cases[cid - 1]["args"][3], "hooks": cases[cid - 1]["args"][2]["hooks"], "state": {k: v for k, v in cases[cid - 1]["args"][2]["state"].items() if k in ("active_portfolio", "portfolios", "current_date", "live_date", "is_playing", "frame", "current_criteria", "pit_mode", "portfolio_models", "visible", "return_type", "product", "product_type", "strategy_family", "model_limit")}, "viewCache": cases[cid - 1]["args"][2]["viewCache"], "criteria": list(cases[cid - 1]["args"][2]["criteria"])}))
        if not r["ok"]:
            s["js_error"] += 1
            fails.setdefault(method, []).append(f"case {cid}: JS error {r['error']}")
            continue
        vlog = r["result"].pop("_vlog", None)
        if vlog:
            print("VLOG", json.dumps(vlog))
        exp.pop("_vlog", None)
        r["result"].pop("_engReq", None)
        dom_js = r["result"].pop("dom", None)
        vargs_js = r["result"].pop("vargs", None)
        extras_js = r["result"].pop("extras", None)
        dbg_js = r["result"].pop("_dbg", None)
        dbg_py = exp.pop("_dbg", None)
        if wrapped and orig_res.get(cid) and orig_res[cid]["ok"]:
            oc = {k: v for k, v in orig_res[cid]["result"].items() if k not in ("dom", "vargs", "extras", "_dbg", "_vlog", "_engReq")}
            d = diff(oc, r["result"])
        else:
            d = diff(exp, r["result"])
        if not d and wrapped and orig_dom.get(cid) is not None and dom_js != orig_dom[cid]:
            n = next((i for i, (x, y) in enumerate(zip(dom_js or [], orig_dom[cid])) if x != y), min(len(dom_js or []), len(orig_dom[cid])))
            d = f".dom[{n}]: original {json.dumps(orig_dom[cid][n:n + 1])[:200]} vs wrapper {json.dumps((dom_js or [])[n:n + 1])[:200]} (lengths {len(orig_dom[cid])}/{len(dom_js or [])})"
        if not d and wrapped and orig_vargs.get(cid) is not None and vargs_js != orig_vargs[cid]:
            n = next((i for i, (x, y) in enumerate(zip(vargs_js or [], orig_vargs[cid])) if x != y), min(len(vargs_js or []), len(orig_vargs[cid])))
            d = f".viewArgs[{n}]: original {json.dumps(orig_vargs[cid][n:n + 1])[:200]} vs wrapper {json.dumps((vargs_js or [])[n:n + 1])[:200]} (lengths {len(orig_vargs[cid])}/{len(vargs_js or [])})"
        if not d and wrapped and orig_extras.get(cid) is not None and extras_js != orig_extras[cid]:
            d = f".extras (data-layer flags / criteria sizes): original {json.dumps(orig_extras[cid])[:300]} vs wrapper {json.dumps(extras_js)[:300]}"
        if d and (dbg_js or dbg_py):
            d += f"   [js error: {dbg_js}] [py error: {dbg_py}]"
        if d:
            fails.setdefault(method, []).append(f"case {cid}: {d}")
        else:
            s["pass"] += 1
    for m, s in summary.items():
        print(f"{m:44s} cases={s['cases']:4d} pass={s['pass']:4d} fail={s['cases']-s['pass']-s['js_error']:4d} js_error={s['js_error']}")
        for f in fails.get(m, [])[: (1000 if os.environ.get("DIFF_ALL") else 2)]:
            print("     ", f[:300])
    sys.exit(0 if all(s["pass"] == s["cases"] for s in summary.values()) else 1)


if __name__ == "__main__":
    main()
