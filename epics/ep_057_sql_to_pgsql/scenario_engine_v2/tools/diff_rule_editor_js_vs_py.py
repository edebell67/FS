# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/diff_rule_editor_js_vs_py.py — differential test of the overlay-rule editor: the page's own functions (Node VM, DOM stub) vs engine/rule_editor.py.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: configFromOverlayEditor, beginEditNamedOverlayRule, cancelEditNamedOverlayRule, saveNamedOverlayRule, assignOverlayRule; whole-state + form + request comparison.
"""Usage: python diff_rule_editor_js_vs_py.py [--cases N] [--methods a,b]. Each case: random page state + random rule library + random form + a fake
server for POST / PUT (success, success without a rule, error with / without detail). Compared: all page state, recorded effects, the form, the requests made."""
import copy
import json
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_argv, sys.argv = sys.argv, ["x"]
sys.path.insert(0, str(ROOT / "tools"))
import diff_page_js_vs_py as dp  # noqa: E402
sys.argv = _argv
from engine import data_client as dc  # noqa: E402
from engine.page import Page  # noqa: E402
from engine.page_state import PageState  # noqa: E402
from engine.rule_editor import RuleForm  # noqa: E402

METHODS = {"config_from_overlay_editor": "configFromOverlayEditor", "begin_edit_named_overlay_rule": "beginEditNamedOverlayRule",
           "cancel_edit_named_overlay_rule": "cancelEditNamedOverlayRule", "save_named_overlay_rule": "saveNamedOverlayRule",
           "assign_overlay_rule": "assignOverlayRule"}
RULE_TYPES = ["ranked_top", "ranked_bottom", "group_ranked_top", "group_ranked_bottom", "higher_loss_rate", "ranked", "group_ranked", "higher_cum_net"]
ELIG = ["min_trades", "win_rate", "positive_net"]
EXTRA_FUNCS = ["configFromOverlayEditor", "beginEditNamedOverlayRule", "cancelEditNamedOverlayRule", "saveNamedOverlayRule", "assignOverlayRule"]

JS_WRAPPER = r"""
globalThis.drawChart = () => { __fx.push(['drawChart']); };
globalThis.syncAssignedOverlayRuleUI = () => { __fx.push(['syncAssignedOverlayRuleUI']); };
globalThis.CSS = { escape: s => String(s) };
async function __editor(fx, name, c, args) {
  __calls = []; __fx = [];
  globalThis.fetch = async (url, opts) => {
    const u = String(url); const key = opts && opts.method ? opts.method + ' ' + u + ' ' + opts.body : u; __calls.push(key);
    const r = fx[key] || { status: 404, payload: { error: 'not found' } };
    return { ok: r.status >= 200 && r.status < 300, status: r.status, json: async () => r.payload };
  };
  __ps_set(c.state);
  globalThis.overlayRuleLibrary = c.library; globalThis.overlayRuleLibraryRequest = null;
  globalThis.portfolioViewConfigs = c.state.portfolio_view_configs; globalThis.livePortfolioStore = c.state.live_store;
  globalThis.__maxFrames = c.hooks.maxFrames; globalThis.__head = c.hooks.head; globalThis.__elig = c.hooks.eligible; globalThis.__candidates = c.hooks.candidates;
  const f = c.form;
  const E = { liveRuleInterval: { value: f.interval }, liveRuleMetric: { value: f.metric }, liveRuleGroup: { value: f.group }, liveRuleTradeSide: { value: f.trade_side },
    namedRuleHoldRank: { value: f.hold_rank }, namedRuleExitThreshold: { value: f.exit_threshold },
    saveNamedOverlayRuleBtn: { textContent: f.save_text }, namedOverlayRuleStatus: { textContent: f.status },
    overlayRuleNameInput: { value: f.name_input }, overlayRuleNameStatus: { textContent: f.modal_status }, overlayRuleNameSave: { disabled: f.save_disabled },
    livePortfolioRulesPanel: { open: f.panel_open, scrollIntoView(){ __fx.push(['scrollIntoView']); } }, namedOverlayRuleEditor: { open: f.editor_open } };
  let hidden = f.cancel_hidden;
  E.cancelNamedOverlayRuleEditBtn = { classList: { add(k){ if (k === 'hidden') hidden = true; }, remove(k){ if (k === 'hidden') hidden = false; } } };
  const rc = f.rule_checks.map(x => ({ value: x.value, checked: x.checked })), ec = f.eligibility_checks.map(x => ({ value: x.value, checked: x.checked }));
  globalThis.document = { getElementById: id => E[id] || null, createElement: () => ({}), hidden: false,
    querySelectorAll: sel => sel === '.live-rule-check:checked' ? rc.filter(x => x.checked) : sel === '.live-rule-check' ? rc
      : sel === '.live-eligibility-check:checked' ? ec.filter(x => x.checked) : sel === '.live-eligibility-check' ? ec : [] };
  const selector = f.selector ? { disabled: f.selector.disabled, value: f.selector.value } : null;
  globalThis.portfolioList = { querySelector: () => selector };
  globalThis.overlayRuleLibraryModal = { close(){ __fx.push(['overlayRuleLibraryModal.close']); } };
  globalThis.overlayRuleNameModal = { close(){ __fx.push(['overlayRuleNameModal.close']); } };
  let ret;
  if (name === 'saveNamedOverlayRule') args = [{ preventDefault(){} }];
  try { ret = await globalThis[name](...args); } catch (e) { ret = { error: true, message: String(e && e.message || e) }; }
  for (let i = 0; i < 40; i++) await new Promise(res => __imm(res));
  const form = { interval: E.liveRuleInterval.value, metric: E.liveRuleMetric.value, group: E.liveRuleGroup.value, trade_side: E.liveRuleTradeSide.value,
    hold_rank: E.namedRuleHoldRank.value, exit_threshold: E.namedRuleExitThreshold.value, rule_checks: rc, eligibility_checks: ec,
    save_text: E.saveNamedOverlayRuleBtn.textContent, cancel_hidden: hidden, status: E.namedOverlayRuleStatus.textContent, name_input: E.overlayRuleNameInput.value,
    modal_status: E.overlayRuleNameStatus.textContent, save_disabled: E.overlayRuleNameSave.disabled, panel_open: E.livePortfolioRulesPanel.open,
    editor_open: E.namedOverlayRuleEditor.open, selector };
  return { state: __ps_get(), effects: __fx, calls: __calls, form, ret: ret === undefined ? null : ret, library: overlayRuleLibrary };
}
"""


def rand_config(rng):
    if rng.random() < 0.1:
        return rng.choice([None, {}])
    cfg = {}
    if rng.random() < 0.8:
        cfg["interval_minutes"] = rng.choice([0, 15, 30, 45, None])
    if rng.random() < 0.9:
        cfg["rules"] = rng.choice([None, [], [{"type": rng.choice(RULE_TYPES), "metric": rng.choice(["cum_net", "win_rate", "", None]), "group": rng.choice(["", "family:breakout", None])}
                                              for _ in range(rng.randint(1, 3))]])
    if rng.random() < 0.7:
        cfg["eligibility_filters"] = rng.choice([None, [], rng.sample(ELIG, rng.randint(0, 3))])
    if rng.random() < 0.7:
        cfg["trade_side"] = rng.choice(["both", "buy", "sell", "", None])
    if rng.random() < 0.7:
        cfg["hold_rank"] = rng.choice([0, 1, 2, 5, None])
    if rng.random() < 0.7:
        cfg["exit_threshold"] = rng.choice([0, -1.5, 2, None])
    return cfg


def rand_pending(rng):
    if rng.random() < 0.15:
        return rng.choice([None, 0])
    rules = [{"type": rng.choice(RULE_TYPES), "metric": "cum_net", "group": rng.choice(["", "family:breakout"])} for _ in range(rng.choice([0, 1, 2]))]
    return {"interval_minutes": 30, "rules": rules, "eligibility_filters": [], "trade_side": "both", "hold_rank": 1, "exit_threshold": 0}


def rand_form(rng):
    return {"interval": rng.choice(["30", "", "abc", "15.5", " 20 "]), "metric": rng.choice(["cum_net", "win_rate"]),
            "group": rng.choice(["", "  family:breakout  ", "fam"]), "trade_side": rng.choice(["both", "buy"]),
            "hold_rank": rng.choice(["", "0", "2", "abc", "1.5"]), "exit_threshold": rng.choice(["", "0", "-2", "x", "3.25"]),
            "rule_checks": [{"value": t, "checked": rng.random() < 0.4} for t in rng.sample(RULE_TYPES, rng.randint(1, len(RULE_TYPES)))],
            "eligibility_checks": [{"value": t, "checked": rng.random() < 0.4} for t in ELIG],
            "save_text": rng.choice(["Name and save rule", "Update x"]), "cancel_hidden": rng.choice([True, False]),
            "status": rng.choice(["", "old"]), "name_input": rng.choice(["", "  ", "My rule", " Spaced name "]), "modal_status": rng.choice(["", "old"]),
            "save_disabled": False, "panel_open": False, "editor_open": False,
            "selector": rng.choice([None, {"disabled": False, "value": "r1"}])}


def make_case(rng, method):
    snap = dp.rand_state(rng)
    st = PageState.from_snapshot(snap)
    ports = list(st.portfolios)
    rules = [{"id": f"r{i}", "name": rng.choice([f"Rule {i}", "Q&A rule", None]), "config": rand_config(rng)} for i in range(1, rng.randint(1, 4))]
    if rng.random() < 0.1:
        rules.append({"name": "no id", "config": {}})
    assign = rng.choice([{}, {"P1": "r1"}, {"Alpha": "r1", "P2": "r2"}, []])
    snap["editing_rule_id"] = rng.choice([None, "r1", "r2", "ghost"])
    snap["pending_rule_config"] = rand_pending(rng)
    snap["use_assigned_rule"] = rng.choice([False, True])
    hooks = {"maxFrames": 3, "head": rng.choice([None, "10:05"]), "eligible": [dp.mk(1)], "candidates": [dp.mk(i) for i in range(1, 4)]}
    case = {"state": snap, "hooks": hooks, "library": {"rules": rules, "assignments": assign}, "form": rand_form(rng), "viewCache": [], "lastView": [], "criteria": {},
            "writes": rng.choice(["ok", "ok", "norule", "nullrule", "err", "errplain"])}
    if method == "begin_edit_named_overlay_rule":
        args = [rng.choice([r.get("id") for r in rules] + ["nope", None])]
    elif method == "assign_overlay_rule":
        active = snap["active_portfolio"]
        args = [rng.choice(ports + ["P1", "Z q&"] + ([active] if active else [])), rng.choice(["r1", "r2", "", None, "rX"])]
    else:
        args = []
    return case, args


class RecordingWrites:
    def __init__(self, mode, case, shared):
        self.mode, self.case, self.shared, self.fx = mode, case, shared, {}

    def __call__(self, method, url, body):
        key = f"{method} {url} {json.dumps(body, separators=(',', ':'))}"
        self.shared.append(key)
        if self.mode == "ok":
            res = (200, {"rule": {"id": (body.get("config") and "r1") or "r1", "name": body.get("name", "n") if "name" in body else "n"}, "assignments": {}})
        elif self.mode == "norule":
            res = (200, {})
        elif self.mode == "nullrule":
            res = (200, {"rule": None})
        elif self.mode == "err":
            res = (400, {"detail": "bad request"})
        else:
            res = (500, {})
        self.fx[key] = {"status": res[0], "payload": res[1]}
        return res


def run_python(method, case, args):
    tr = dp.RecordingTransport()
    cl = dc.DataClient(tr, dp.API, live_date=case["state"]["live_date"], base_href="http://h/p/page.html")
    cl.overlay_rule_library = copy.deepcopy(case["library"])
    writes = RecordingWrites(case["writes"], case, tr.calls)
    cl.write_transport = writes
    st = PageState.from_snapshot(case["state"])
    h = case["hooks"]
    page = Page(st, cl, max_frames=lambda: h["maxFrames"], head_time=lambda: h["head"], eligible=lambda: h["eligible"], candidates=lambda: h["candidates"])
    form = RuleForm(**copy.deepcopy(case["form"]))
    page.rule_editor.form = form
    ret = None
    try:
        ret = getattr(page.rule_editor, method)(*args)
        page.settle()
    except Exception as e:  # noqa: BLE001
        ret = {"error": True, "message": str(e)}
    fx = {**tr.fx, **writes.fx}
    if isinstance(ret, dict) and "interval_minutes" in ret:
        ret = {k: (None if isinstance(v, float) and v != v else v) for k, v in ret.items()}
    return {"state": st.snapshot(), "effects": st.effects, "calls": tr.calls, "form": form.snapshot(),
            "ret": ret if method == "config_from_overlay_editor" or (isinstance(ret, dict) and ret.get("error")) else None,
            "library": cl.overlay_rule_library}, fx


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=300)
    ap.add_argument("--methods", default="")
    ns = ap.parse_args()
    methods = [m for m in ns.methods.split(",") if m] or list(METHODS)
    rng = random.Random(7)
    cases, expected = [], {}
    for method in methods:
        for _ in range(ns.cases):
            case, args = make_case(rng, method)
            exp, fx = run_python(method, case, args)
            cid = len(cases) + 1
            cases.append({"id": cid, "call": "__editor", "args": [fx, METHODS[method], case, args]})
            expected[cid] = (method, exp)
    spec = {"page": str(dp.PAGE), "inventory": str(dp.INVENTORY), "functions": dp.PAGE_FUNCS + EXTRA_FUNCS, "extra": dp.PAGE_EXTRA + JS_WRAPPER, "cases": cases}
    workers = max(1, min(int(os.environ.get("DIFF_WORKERS", "8")), len(cases)))
    results = []
    with tempfile.TemporaryDirectory() as td:
        procs = []
        for k in range(workers):
            sp = Path(td) / f"c{k}.json"
            sp.write_text(json.dumps({**spec, "cases": cases[k::workers]}), encoding="utf-8")
            procs.append(subprocess.Popen(["node", str(ROOT / "tools" / "js_runner.js"), str(sp)], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        for pr in procs:
            out, err = pr.communicate(timeout=3600)
            if pr.returncode != 0:
                print("NODE FAILED:", err.decode("utf-8", "replace")[-1500:])
                sys.exit(2)
            results.extend(json.loads(out.decode("utf-8")))
    res = {r["id"]: r for r in results}
    summary, fails = {}, {}
    for cid, (method, exp) in expected.items():
        r = res[cid]
        s = summary.setdefault(method, {"cases": 0, "pass": 0, "js_error": 0})
        s["cases"] += 1
        if os.environ.get("DIFF_DEBUG_ID") == str(cid):
            print("DEBUG JS:", json.dumps(r)[:3000])
            print("DEBUG PY:", json.dumps(exp, default=str)[:3000])
        if not r["ok"]:
            s["js_error"] += 1
            fails.setdefault(method, []).append(f"case {cid}: JS error {r['error']}")
            continue
        js = r["result"]
        if method != "config_from_overlay_editor" and not (isinstance(js["ret"], dict) and js["ret"].get("error")):
            js["ret"] = None
        d = dp.diff(exp, js)
        if d:
            fails.setdefault(method, []).append(f"case {cid}: {d}")
        else:
            s["pass"] += 1
    for m, s in summary.items():
        print(f"{m:34s} cases={s['cases']:4d} pass={s['pass']:4d} fail={s['cases'] - s['pass'] - s['js_error']:4d} js_error={s['js_error']}")
        for f in fails.get(m, [])[:6]:
            print("     ", f[:400])


if __name__ == "__main__":
    main()
