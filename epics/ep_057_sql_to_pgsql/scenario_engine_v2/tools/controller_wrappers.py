# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/controller_wrappers.py — generates the browser-side wrappers that delegate page controllers to the engine (engine/command.py).
#
# VERSION HISTORY
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
    "startReplay": ("start_replay", "", "[]", r"^\s*(playIcon|playBtnText|playBtn)\b", {"startPlaybackLoop": "startPlaybackLoop();"}),
    "pauseReplay": ("pause_replay", "", "[]", r"^\s*(playIcon|playBtnText|playBtn)\b",
                    {"clearInterval": "if (replayInterval) { clearInterval(replayInterval); replayInterval = null; }"}),
    "syncPortfolioViewRefresh": ("sync_portfolio_view_refresh", "", "[]", None,
                                 {"clearInterval": "if (portfolioViewRefreshTimer !== null) { clearInterval(portfolioViewRefreshTimer); portfolioViewRefreshTimer = null; }",
                                  "setInterval": "if (location.protocol !== 'file:') portfolioViewRefreshTimer = setInterval(refreshActivePortfolioView, effect[1]);"}),
    "updateAutoRefreshTop1Status": ("update_auto_refresh_status", "message = ''", "[message]", None, {}),

}
# NOT yet delegated (timer effects carry no callback identity; needs engine-named timers):
#     "applyChartLock": ("apply_chart_lock", "locked, persist = true", "[locked, persist]", None, {}),
#     "resetAutomaticRankSchedule": ("reset_automatic_rank_schedule", "", "[]", None, {}),
# per controller: prelude (page-only logic run before the call), range (first line regex, last line regex) = DOM shell block copied from the original, pause_if = state field that,
# when true after the call, also runs the original pauseReplay DOM lines
EXTRAS = {
    "resetAutomaticRankSchedule": {"flag": "autoRefreshTop1RequestAt !== null", "flag_shell": r"^\s*applySelectedTimeBtn\?\."},
    "applyChartLock": {"prelude": "if (!locked && isLiveModePortfolio() && isLiveModeArmed()) locked = true;", "range": (r"^\s*chartLockBtn\.setAttribute", r"^\s*scrubberTrack\.title"),
                       "pause_if": "chartLocked"},
}

COMMON_EFFECTS = {
    "savePortfolios": "savePortfolios();", "saveCriteriaWorkspaces": "saveCriteriaWorkspaces();", "renderPortfolioList": "renderPortfolioList();",
    "refreshPointInTimeHistory": "refreshPointInTimeHistory();",
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


def helper_block(state_decls: dict) -> str:
    missing = [js for _py, js, _k, _d in FIELDS if js not in state_decls and js not in DERIVED]
    if missing:
        raise SystemExit(f"BUILD REFUSED: page state fields not declared at top level in the page: {missing}")
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
    function __engineCommand(method, args) {{
      const sent = __engineSnapshot();
      const res = __engine.call({{ fn: 'command', method, args, state: sent, criteriaData: __engineCriteria(), library: overlayRuleLibrary, hooks: globalThis.__engineHooks,
        scenarioNames: Object.fromEntries(SCENARIOS_CATALOGUE.map(item => [item.id, item.name])) }});
      __engineApplyState(res.state, sent);
      return res;
    }}
    function __engineReplay(effects, handlers) {{
      effects.forEach(effect => {{
        const name = effect[0];
        if (name === 'view') {{ if (typeof globalThis[effect[1]] === 'function') globalThis[effect[1]](); return; }}
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
            if on:
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
    shell_block = f"\n{shell}" if shell else ""
    asyncs = "async " if original_body.lstrip().startswith("async") else ""
    return (f"    {asyncs}function {name}({params}) {{\n{prelude}{flag}      const res = __engineCommand('{method}', {argexpr});{shell_block}\n"
            f"      __engineReplay(res.effects, {{ {handlers} }});\n      return res.ret;\n    }}")
