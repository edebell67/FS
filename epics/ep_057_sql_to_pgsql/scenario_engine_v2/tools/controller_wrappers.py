# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/controller_wrappers.py — generates the browser-side wrappers that delegate page controllers to the engine (engine/command.py).
#
# VERSION HISTORY
# v1.5.0 · 2026-10-18 · __engineSpawn: the page runs a spawn (fetch + resume stage) an engine answer asked for; the original-function fallbacks are gone except for live portfolios (activatePortfolio).
# v1.4.0 · 2026-10-18 · the staged shell is a reusable driver (__drive / __apply / __resume): started page promises keep a handle, a continuation can be attached to a handle and runs later as its own engine stage; fallback to the original function for what the engine refuses (live portfolios).
# v1.3.0 · 2026-10-18 · staged shells: Await.catch, args-bearing views (viewArgs), page flags, per-controller extra await targets (refreshLiveData's data layer).
# v1.1.0 · 2026-10-17 · stage 2 (no-fetch): applyChartLock, resetAutomaticRankSchedule; EXTRAS (prelude / range shell / conditional pause shell).
# v1.0.0 · 2026-10-17 · Initial version (stage 1: 8 controllers without network): state snapshot / apply code from page_state.FIELDS, __engineCommand, per-controller DOM shells copied from the original body and effect replay.
"""Used by tools/build_thin_page.py and by the differential test (tools/diff_page_js_vs_py.py with DIFF_WRAPPERS=1). The wrappers keep the original function names and signatures, so every caller in the page is unchanged.
For each controller: (1) snapshot the page state, (2) one /engine/call {fn:'command'}, (3) apply the returned state in place, (4) run the DOM shell the original function had (copied from its body), (5) replay the effects in order."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.page_state import FIELDS  # noqa: E402

# fields that are not page variables: how to read them (never written back)
DERIVED = {"pointInTimeHistoryPanelHidden": "Boolean(pointInTimeHistoryPanel && pointInTimeHistoryPanel.classList.contains('hidden'))"}
TIMER_FIELDS = {"replay_interval", "portfolio_refresh_timer"}   # real timer handles stay in the page; the engine only says when to start / stop them

# page function -> (engine method, parameter list as the page declares it, how the arguments are sent, DOM-shell regex or None, effect handlers)
CONTROLLERS = {
    "movePortfolio": ("move_portfolio", "name, offset", "[name, offset]", None, {}),
    "markPortfolioFixed": ("mark_portfolio_fixed", "name", "[name]", None, {}),
    "capturePortfolioScenario": ("capture_portfolio_scenario", "name, criteria = currentCriteria", "[name, criteria]", None, {}),
    "persistPortfolioViewConfig": ("persist_portfolio_view_config", "name = activePortfolioName", "arguments.length === 0 || arguments[0] === undefined ? [] : [name]", None, {}),
    "startReplay": ("start_replay", "", "[]", None, {"startPlaybackLoop": "startPlaybackLoop();"}),
    "pauseReplay": ("pause_replay", "", "[]", None, {}),
    "syncPortfolioViewRefresh": ("sync_portfolio_view_refresh", "", "[]", None, {}),
    "updateAutoRefreshTop1Status": ("update_auto_refresh_status", "message = ''", "[message]", None, {}),
    "applyChartLock": ("apply_chart_lock", "locked, persist = true", "[locked, persist]", None, {}),
    "resetAutomaticRankSchedule": ("reset_automatic_rank_schedule", "", "[]", None, {}),
    "uniquePortfolioName": ("unique_portfolio_name", "baseName", "[baseName]", None, {}),
    "currentPortfolioViewConfig": ("current_portfolio_view_config", "", "[]", None, {}),
    "applyPortfolioViewConfig": ("apply_portfolio_view_config", "config", "[config]", None, {}),
    "getMergedPortfolioModels": ("get_merged_portfolio_models", "", "[]", None, {}),
    "autoPinLivePortfolioStrategies": ("auto_pin_live_portfolio_strategies", "", "[]", None, {}),
    "schedulePointInTimeSelection": ("schedule_point_in_time_selection", "", "[]", None, {}),
    "scheduleAutomaticTop1Refresh": ("schedule_automatic_top1_refresh", "at", "[at]", None, {}),
    "applySelectedTime": ("apply_selected_time", "", "[]", None, {}),
    "triggerSelectedTimeRefresh": ("trigger_selected_time_refresh", "", "[]", None, {}),
    # staged: the page awaits a page async function between engine stages (engine/page.py STAGES)
    "removeModelFromPortfolio": ("remove_model_from_portfolio", "name, model", "[name, model]", None, {}),
    "addCatalogueModel": ("add_catalogue_model", "model", "[name, model]", None, {}),
    "moveModelBetweenPortfolios": ("move_model_between_portfolios", "sourceName, destinationName, model", "[sourceName, destinationName, model]", None, {}),
    "repopulateActivePortfolioFromCriteria": ("repopulate_active_portfolio_from_criteria", "", "[]", None, {}),
    "removePortfolios": ("remove_portfolios", "names", "[names]", None, {}),
    "switchDate": ("switch_date", "dateKey, { skipPortfolioLoad = false, refreshData = false } = {}", "[dateKey, skipPortfolioLoad, refreshData]", None, {}),
    "refreshActivePortfolioView": ("refresh_active_portfolio_view", "", "[]", None, {}),
    "refreshPointInTimeSelection": ("refresh_point_in_time_selection", "atOverride = null", "[atOverride]", None, {}),
    "refreshPointInTimeHistory": ("refresh_point_in_time_history", "", "[]", None, {}),
    "activatePortfolio": ("activate_portfolio", "name", "[name]", None, {}),
    "createSimilarPortfolio": ("create_similar_portfolio", "dimension", "[dimension]", None, {}),
    "setRankingCriteria": ("set_ranking_criteria", "criteria", "[criteria]", None, {}),
    "refreshLiveData": ("refresh_live_data", "targetDate = LIVE_DATE, { skipPortfolioRefresh = false } = {}", "[targetDate, skipPortfolioRefresh]", None, {}),
}
# per controller: prelude (page-only logic run before the call), range (first line regex, last line regex) = DOM shell block copied from the original, pause_if = state field that,
# when true after the call, also runs the original pauseReplay DOM lines
SWITCH_PRE = """    // page-only code of switchDate (the URL and the date pills): the engine asks for it by name
    globalThis.__switchDateUrl = dateKey => {
      const nextUrl = new URL(location.href);
      nextUrl.searchParams.set('date', dateKey);
      history.replaceState(null, '', nextUrl);
    };
    globalThis.__switchDatePills = () => {
      availableDates.forEach(d => {
        const tab = document.getElementById(`tab_${d.id}`);
        if (tab) {
          tab.className = `date-pill px-2.5 py-1 text-xs font-bold font-mono rounded ${
            d.id === currentDate ? 'bg-sky-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`;
          if (d.id === currentDate) tab.setAttribute('aria-current', 'date');
          else tab.removeAttribute('aria-current');
        }
      });
    };
"""
LIVE_TARGETS = '\n      fetchLiveDay: async (path) => {\n        const requestUrl = `${API_BASE}${path}`;\n        let res, payload;\n        const early = window.__ep057EarlyChartRequest;\n        if (early && !early.used && early.url === requestUrl) {\n          early.used = true;\n          const outcome = await early.request;\n          if (!outcome.error) {\n            res = outcome.response;\n            payload = outcome.payload;\n          }\n        }\n        if (!res) {\n          res = await fetch(requestUrl, { cache: \'no-store\' });\n          payload = await res.json();\n        }\n        if (!res.ok) throw new Error(payload.error || res.status);\n        __box.payload = payload;\n        return true;\n      },\n      applyLivePayload: (targetDate, requestedScenario, requestedProductType, requestedProduct, requestedStrategyFamily, requestedLimit, requestedCriteria, requestedReturnType) => {\n        const payload = __box.payload;\n        liveChartDataLoadedKeys.add(liveChartCacheKey(targetDate));\n        cacheLiveChartResponse(payload, targetDate, requestedScenario, requestedProductType, requestedProduct,\n          requestedStrategyFamily, requestedLimit, requestedCriteria, requestedReturnType);\n        if (productFilter) {\n          const products = Array.isArray(payload.products) ? payload.products : [];\n          productFilter.innerHTML = \'<option value="all">All</option>\' + products.map(product =>\n            `<option value="${product}">${product.toUpperCase()}</option>`\n          ).join(\'\');\n          if (!products.includes(currentProduct)) currentProduct = \'all\';\n          productFilter.value = currentProduct;\n        }\n        syncTpSlScenarios(Array.isArray(payload.tp_sl_scenarios) ? payload.tp_sl_scenarios : []);\n        Object.keys(payload).forEach(sc => {\n          if (!Array.isArray(payload[sc])) return;\n          ALL_CRITERIA_DATA[sc] ||= {};\n          ALL_CRITERIA_DATA[sc][targetDate] = payload[sc];\n        });\n        pendingFilterDataRefresh = false;\n        if (targetDate === LIVE_DATE) initialLiveDataAvailable = true;\n        updateStrategyFamilyOptions();\n        const t = new Date().toLocaleTimeString([], { hour: \'2-digit\', minute: \'2-digit\' });\n        setLiveBadge(targetDate === LIVE_DATE ? `Live · updated ${t}` : `${targetDate} · ${modelLimit} models`, \'ok\');\n      },\n      syncLivePortfolioScreenState: (targetDate) => syncLivePortfolioScreenState(targetDate),'
EXTRAS = {
    "refreshPointInTimeSelection": {"staged": True},
    "refreshPointInTimeHistory": {"staged": True},
    "activatePortfolio": {"staged": True, "fallback": True, "targets": " loadOverlayRuleLibrary: (...a) => loadOverlayRuleLibrary(...a), __attach: () => null,"},
    "createSimilarPortfolio": {"staged": True},
    "setRankingCriteria": {"staged": True},
    "removePortfolios": {"staged": True},
    "switchDate": {"staged": True, "pre": SWITCH_PRE},
    "refreshActivePortfolioView": {"staged": True, "prelude": "if (document.hidden) return;"},
    "refreshLiveData": {"staged": True, "locals": "      const __box = { payload: null };   // the live-day payload stays in the page: it is the page's data layer\n", "targets": LIVE_TARGETS},
    "removeModelFromPortfolio": {"staged": True},
    "addCatalogueModel": {"staged": True, "prelude": "const name = catalogPortfolioFilter.value; if (name && portfolios[name] && !portfolios[name].includes(model) && portfolios[name].length >= 10) alert(`${name} already contains the maximum of 10 strategies.`);"},
    "moveModelBetweenPortfolios": {"staged": True, "prelude": "if (sourceName && destinationName && sourceName !== destinationName && portfolios[sourceName]?.includes(model) && portfolios[destinationName] && !portfolios[destinationName].includes(model) && portfolios[destinationName].length >= 10) alert(`${destinationName} already contains the maximum of 10 strategies.`);"},
    "repopulateActivePortfolioFromCriteria": {"staged": True},
    "applyChartLock": {"prelude": "if (!locked && isLiveModePortfolio() && isLiveModeArmed()) locked = true;"},
}

COMMON_EFFECTS = {
    "savePortfolios": "savePortfolios();", "saveCriteriaWorkspaces": "saveCriteriaWorkspaces();", "renderPortfolioList": "renderPortfolioList();",
    "refreshPointInTimeHistory": "refreshPointInTimeHistory();", "renderPointInTimeHistory": "renderPointInTimeHistory();",
}
STORAGE = {"strategyDirectoryPortfolioViewV1": "JSON.stringify(portfolioViewConfigs)", "strategyDirectoryMainViewV1": "JSON.stringify(mainScenarioViewConfig)"}


def _snapshot_expr(js, kind):
    return {"val": js, "set": f"[...{js}].map(String).sort()", "oset": f"[...{js}]", "map": f"[...{js}.entries()]", "odict": f"Object.entries({js})",
            "valueobj": f"({js} ? {js}.value : null)", "textobj": f"({js} ? {js}.textContent : null)",
            "statusobj": f"({js} ? [{js}.textContent, {js}.className] : ['', ''])"}[kind]


def _apply_stmt(py, js, kind, decl):
    if kind == "val":
        if decl == "const":
            return f"if (ch('{py}')) __merge({js}, s.{py});"
        return f"if (ch('{py}')) {js} = __merge({js}, s.{py});"
    if kind in ("set", "oset"):
        return f"if (ch('{py}')) {{ {js}.clear(); s.{py}.forEach(x => {js}.add(x)); }}"
    if kind == "map":
        return f"if (ch('{py}')) {{ {js}.clear(); s.{py}.forEach(([k, v]) => {js}.set(k, v)); }}"
    if kind == "odict":
        return f"if (ch('{py}')) {{ Object.keys({js}).forEach(k => {{ delete {js}[k]; }}); s.{py}.forEach(([k, v]) => {{ {js}[k] = v; }}); }}"
    if kind == "valueobj":
        return f"if (ch('{py}') && {js}) {js}.value = s.{py};"
    if kind == "textobj":
        return f"if (ch('{py}') && {js}) {js}.textContent = s.{py};"
    return f"if (ch('{py}') && {js}) {{ {js}.textContent = s.{py}[0]; {js}.className = s.{py}[1]; }}"


def declarations(page_text: str, state_decls: dict) -> dict:
    """name -> let / const / var, also for names in a multi-variable declaration (the inventory only lists the first one)."""
    out = dict(state_decls)
    for _py, js, _k, _d in FIELDS:
        if js in out or js in DERIVED:
            continue
        m = re.search(r"^ {4,8}(let|const|var)\s[^;]*?\b" + re.escape(js) + r"\b\s*=", page_text, re.M)
        if m:
            out[js] = m.group(1)
    return out


def dom_elements() -> list:
    """Every element the engine writes to (engine/page.py: self.dom(\"name\", ...) calls and the lock-control loop)."""
    src = (Path(__file__).resolve().parent.parent / "engine" / "page.py").read_text(encoding="utf-8")
    names = set(re.findall(r'self.dom\("(\w+)"', src)) | set(re.findall(r'b = "(\w+)"', src))
    for tup in re.findall(r'for control in \(([^)]*)\)', src):
        names |= set(re.findall(r'"(\w+)"', tup))
    return sorted(names)


def helper_block(state_decls: dict) -> str:
    missing = [js for _py, js, _k, _d in FIELDS if js not in state_decls and js not in DERIVED]
    if missing:
        raise SystemExit(f"BUILD REFUSED: page state fields not declared at top level in the page: {missing}")
    dom_table = ", ".join(f"{n}: () => {n}" for n in dom_elements())
    snap = ", ".join(f"{py}: {DERIVED[js] if js in DERIVED else _snapshot_expr(js, kind)}" for py, js, kind, _d in FIELDS)
    apply = "\n      ".join(_apply_stmt(py, js, kind, state_decls[js]) for py, js, kind, _d in FIELDS if py not in TIMER_FIELDS and js not in DERIVED)
    return f"""    // ---- controllers run in the Python engine (engine/command.py): the page sends its state, applies the answer in place, then replays the effects in order ----
    function __engineSnapshot() {{ return {{ {snap} }}; }}
    function __merge(current, value) {{
      if (Array.isArray(current) && Array.isArray(value)) {{ current.length = 0; value.forEach(x => current.push(x)); return current; }}
      if (current && value && typeof current === 'object' && typeof value === 'object' && !Array.isArray(current) && !Array.isArray(value)) {{
        Object.keys(current).forEach(k => {{ if (!(k in value)) delete current[k]; }});
        Object.keys(value).forEach(k => {{ current[k] = value[k]; }});
        return current;
      }}
      return value;
    }}
    function __engineApplyState(s, sent) {{
      const ch = k => JSON.stringify(s[k]) !== JSON.stringify(sent[k]);
      {apply}
    }}
    function __engineCriteria() {{
      const key = isMetricAwareCriteria(currentCriteria) ? `${{currentCriteria}}_${{currentReturnType === 'ALT' ? 'alt' : 'net'}}` : currentCriteria;
      const out = {{}};
      [key, 'top_net'].forEach(k => {{ const bucket = ALL_CRITERIA_DATA[k] && ALL_CRITERIA_DATA[k][currentDate]; if (bucket) out[k] = {{ [currentDate]: bucket }}; }});
      return out;
    }}
    function __engineCommand(method, args, extra) {{
      const sent = __engineSnapshot();
      const res = __engine.call({{ fn: 'command', method, args, ...(extra || {{}}), state: sent, flags: {{ liveArmed: typeof isLiveModeArmed === 'function' && !!isLiveModeArmed() }}, criteriaData: __engineCriteria(), library: overlayRuleLibrary, hooks: globalThis.__engineHooks,
        scenarioNames: Object.fromEntries(SCENARIOS_CATALOGUE.map(item => [item.id, item.name])) }});
      if (!res.needsNetwork) {{ __engineApplyState(res.state, sent); (res.spawns || []).forEach(__engineSpawn); }}
      return res;
    }}
    // un-awaited page work an engine answer asked for: run the page's fetch, then resume the named engine stage on the page's current state
    function __engineSpawn(sp) {{
      Promise.resolve(__awaitTargets[sp.fn](...sp.args)).then(v => ({{ ok: v }}), e => ({{ error: String(e && e.message || e) }})).then(out => {{
        const r = __engineCommand(sp.method, null, {{ stage: sp.stage, ctx: sp.ctx, result: out }});
        __engineReplay(r.effects, {{}}, r.timers, r.viewArgs);
        (r.calls || []).forEach(([fn, a]) => globalThis[fn](...a));
      }}).catch(e => console.warn('engine continuation failed:', e));
    }}
    function __engineTimer(op) {{
      const timer = op.timer;
      const get = () => ({{ modelSearchTimer, pointInTimeDebounceTimer, replayInterval, portfolioViewRefreshTimer }})[timer];
      const put = v => {{ if (timer === 'modelSearchTimer') modelSearchTimer = v; else if (timer === 'pointInTimeDebounceTimer') pointInTimeDebounceTimer = v; else if (timer === 'replayInterval') replayInterval = v; else if (timer === 'portfolioViewRefreshTimer') portfolioViewRefreshTimer = v; else if (timer !== 'anonymousTimer') throw new Error('unknown engine timer: ' + timer); }};   // 'anonymousTimer': a one-shot the page never clears
      const interval = timer === 'replayInterval' || timer === 'portfolioViewRefreshTimer';
      if (op.op === 'clear') {{ if (interval) {{ clearInterval(get()); put(null); }} else clearTimeout(get()); return; }}
      if (interval) {{ if (timer === 'portfolioViewRefreshTimer' && location.protocol === 'file:') return; put(setInterval(globalThis.__engineTimerTargets[op.call], op.ms)); return; }}
      const run = () => globalThis.__engineTimerTargets[op.call](...op.args);
      put(setTimeout(run, op.ms));
    }}
    globalThis.__engineTimerTargets = {{ loadModelSearchFromDatabase: (...a) => loadModelSearchFromDatabase(...a), refreshPointInTimeSelection: (...a) => refreshPointInTimeSelection(...a), refreshActivePortfolioView: (...a) => refreshActivePortfolioView(...a), scheduleAutomaticTop1Refresh: (...a) => scheduleAutomaticTop1Refresh(...a) }};
    const __awaitTargets = {{ loadPortfolioData: (...a) => loadPortfolioData(...a), refreshLiveData: (date, skip) => skip === undefined ? refreshLiveData(date) : refreshLiveData(date, {{ skipPortfolioRefresh: !!skip }}), switchDate: (...a) => switchDate(...a),
      ensureHistoricalDataLoaded: (...a) => ensureHistoricalDataLoaded(...a), schedulePointInTimeSelection: (...a) => schedulePointInTimeSelection(...a), paintLiveChartCache: (...a) => paintLiveChartCache(...a), fetchPointInTime: async path => {{ const response = await fetch(`${{API_BASE}}${{path}}`, {{ cache: 'no-store' }}); const payload = await response.json(); return {{ status: response.status, payload }}; }},
      fetchPointInTimeHours: async path => {{ const response = await fetch(`${{API_BASE}}${{path}}`, {{ cache: 'no-store' }}); const payload = await response.json(); return {{ status: response.status, payload }}; }},
      activatePortfolio: (...a) => activatePortfolio(...a), applyPortfolioViewConfig: (...a) => applyPortfolioViewConfig(...a) }};   // page async functions an engine stage may ask the page to await
    const __domTargets = {{ {dom_table} }};
    function __engineDom(effect) {{
      const [, element, op, args] = effect;
      const target = __domTargets[element]();
      if (!target) return;
      if (op === 'set') target[args[0]] = args[1];
      else if (op === 'classList.add') target.classList.add(...args);
      else if (op === 'classList.remove') target.classList.remove(...args);
      else if (op === 'classList.toggle') target.classList.toggle(...args);
      else if (op === 'setAttribute') target.setAttribute(...args);
      else if (op === 'removeAttribute') target.removeAttribute(...args);
      else if (op === 'call') target[args[0]](...args.slice(1));
      else if (op === 'ensureOption') {{
        const hasProduct = [...target.options].some(option => option.value === args[0]);
        if (!hasProduct && args[0] !== 'all') {{ const option = document.createElement('option'); option.value = args[0]; option.textContent = args[0].toUpperCase(); target.appendChild(option); }}
      }} else throw new Error('unknown engine dom op: ' + op);
    }}
    function __engineReplay(effects, handlers, timers, viewArgs) {{
      effects.forEach((effect, at) => {{
        const name = effect[0];
        if (name === 'dom') {{ __engineDom(effect); return; }}
        if (name === 'setTimeout' || name === 'clearTimeout' || name === 'setInterval' || name === 'clearInterval') {{ (timers || []).filter(op => op.at === at).forEach(__engineTimer); return; }}   // named timers are re-created from `timers`
        if (name === 'view') {{ if (typeof globalThis[effect[1]] === 'function') globalThis[effect[1]](...((viewArgs && viewArgs[at]) || [])); return; }}
        if (name === 'localStorage.setItem') {{ const expr = {{{", ".join(f"'{k}': () => {v}" for k, v in STORAGE.items())}}}[effect[1]]; if (expr) localStorage.setItem(effect[1], expr()); return; }}
        if (handlers[name]) {{ handlers[name](effect); return; }}
        const common = {{{", ".join(f"'{k}': () => {{ {v} }}" for k, v in COMMON_EFFECTS.items())}}}[name];
        if (common) common(); else throw new Error('engine effect not handled by the page: ' + name);
      }});
    }}
"""


def _lines(body: str, rx: str):
    return [l.strip() for l in body.split("\n") if re.match(rx, l)]


PLAY_SHELL = r"^\s*(playIcon|playBtnText|playBtn)\b"


def wrapper(name: str, original_body: str, get_body=None) -> str:
    """get_body(name) -> the original source of another page function (needed for pause_if)."""
    method, params, argexpr, shell_re, effects = CONTROLLERS[name]
    ex = EXTRAS.get(name, {})
    shell = ""
    if shell_re:
        shell = "\n".join("      " + l for l in _lines(original_body, shell_re))
    if ex.get("range"):
        out, on = [], False
        for l in original_body.split("\n"):
            if re.match(ex["range"][0], l):
                on = True
            if on and not (ex.get("skip") and re.match(ex["skip"], l)):   # `skip`: view calls the engine's effects already replay
                out.append("      " + l.strip())
            if on and re.match(ex["range"][1], l):
                break
        shell = "\n".join(out)
    if ex.get("pause_if"):
        pause = "\n".join("        " + l for l in _lines(get_body("pauseReplay"), PLAY_SHELL))
        shell += f"\n      if ({ex['pause_if']}) {{\n{pause}\n      }}"
    flag = ""
    if ex.get("flag"):
        flag = f"      const __was = {ex['flag']};\n"
        shell = "      if (__was) {\n" + "\n".join("        " + l for l in _lines(original_body, ex["flag_shell"])) + "\n      }"
    prelude = f"      {ex['prelude']}\n" if ex.get("prelude") else ""
    handlers = ", ".join(f"'{k}': effect => {{ {v} }}" for k, v in effects.items())
    if ex.get("staged"):   # the page awaits between engine stages; each stage runs on the page's CURRENT state
        extra_targets = ex.get("targets", "")
        locals_ = ex.get("locals", "")
        pre = ex.get("pre", "")
        fb_fn, fb = "", f"throw new Error('engine stage for {method} needs the network');"
        if ex.get("fallback"):   # something the engine refuses (a live portfolio): the page runs its own copy of the original, whole
            fb_fn = original_body.replace(f"function {name}(", f"function __original_{name}(", 1) + "\n"
            fb = f"return __original_{name}.apply(this, arguments);"
        return (fb_fn + pre + f"    async function {name}({params}) {{\n{prelude}{locals_}      const __targets = {{ ...__awaitTargets,{extra_targets} }};\n"
                f"      const __handles = {{}};\n"
                f"      const __apply = r => {{\n"
                f"        __engineReplay(r.effects, {{ {handlers} }}, r.timers, r.viewArgs);\n"
                f"        (r.calls || []).forEach(([fn, a]) => globalThis[fn](...a));\n"
                f"      }};\n"
                f"      const __resume = (stage, ctx, result) => {{\n"
                f"        const r2 = __engineCommand('{method}', null, {{ stage, ctx, result }});\n"
                f"        if (r2.needsNetwork) throw new Error('engine stage for {method} needs the network');\n"
                f"        __apply(r2);\n"
                f"        return __drive(r2);\n"
                f"      }};\n"
                f"      const __drive = async res => {{\n"
                f"        while (res.await) {{\n"
                f"          const aw = res.await, ctxNow = res.ctx, stageNow = res.stage;\n"
                f"          let out;\n"
                f"          if (aw.attach) {{   // run a stage when a started page promise settles (a detached .then)\n"
                f"            __handles[aw.args[0]].then(v => __resume(aw.attach, ctxNow, {{ ok: v === undefined ? null : v }}), e => __resume(aw.attach, ctxNow, {{ error: String(e && e.message || e) }})).catch(e => console.warn('{method} continuation failed:', e));\n"
                f"            out = null;\n"
                f"          }} else if (aw.fire) {{   // start a page async function and carry on; keep the promise under a handle if asked\n"
                f"            const p = Promise.resolve(__targets[aw.fn](...aw.args));\n"
                f"            if (aw.handle) {{ __handles[aw.handle] = p; p.catch(() => {{}}); }} else p.catch(e => console.warn('Date refresh failed:', e));\n"
                f"            out = null;\n"
                f"          }} else if (aw.sync) out = __targets[aw.fn](...aw.args);\n"
                f"          else if (aw.catch) {{ try {{ out = {{ ok: await __targets[aw.fn](...aw.args) }}; }} catch (e) {{ out = {{ error: String(e && e.message || e) }}; }} }}\n"
                f"          else out = await __targets[aw.fn](...aw.args);\n"
                f"          if (stageNow === 'done') break;\n"
                f"          res = __engineCommand('{method}', null, {{ stage: stageNow, ctx: ctxNow, result: out === undefined ? null : out }});\n"
                f"          if (res.needsNetwork) throw new Error('engine stage for {method} needs the network');\n"
                f"          __apply(res);\n"
                f"        }}\n"
                f"        return res.ret;\n"
                f"      }};\n"
                f"      let res = __engineCommand('{method}', {argexpr});\n"
                f"      if (res.needsNetwork) {fb}\n"
                f"      __apply(res);\n"
                f"      return __drive(res);\n"
                f"    }}")
    shell_block = f"\n{shell}" if shell else ""
    asyncs = "async " if original_body.lstrip().startswith("async") else ""
    fallback_fn, fallback = "", ""
    if ex.get("fallback"):   # the controller may want the network: the engine then answers needsNetwork and the page runs its own copy of the original
        fallback_fn = original_body.replace(f"function {name}(", f"function __original_{name}(", 1) + "\n"
        fallback = f"\n      if (res.needsNetwork) return __original_{name}.apply(this, arguments);"
    return (fallback_fn + f"    {asyncs}function {name}({params}) {{\n{prelude}{flag}      const res = __engineCommand('{method}', {argexpr});{fallback}{shell_block}\n"
            f"      __engineReplay(res.effects, {{ {handlers} }}, res.timers);\n      return res.ret;\n    }}")
