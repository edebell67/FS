# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/diff_models_js_vs_py.py — differential test of engine/replay_models.py: the page's getScenarioCandidates / getEligibleModels / getReplayTimelineModels / pointInTimeAtReplayHead / getMaxFrames (and localeCompare) vs Python.
#
# VERSION HISTORY
# v1.x · 2026-10-20 · COLORS shim (page v2.65.36 reads an undefined COLORS), searched-model cases with and without matches (page v2.65.36 getEligibleModels).
# v1.x · 2026-10-19 · queries with several spaces and a name-shaped query; half the cases have nothing loaded (page v2.65.35: spaces count as '_').
# v1.0.0 · 2026-10-17 · Initial version.
"""Usage: python diff_models_js_vs_py.py [--cases N] [--methods a,b]. Random page states over mixed-case ids, missing / null metrics and duplicate returns; compared: the returned model lists, the model-search status line, the whole state."""
import copy
import json
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_argv, sys.argv = sys.argv, ["x"]
sys.path.insert(0, str(ROOT / "tools"))
import diff_page_js_vs_py as dp  # noqa: E402
dp.FAIL_PORTFOLIO_DAY = False   # these cases were written against a fixture server whose portfolio loads always succeed
sys.argv = _argv
from engine import data_client as dc  # noqa: E402
from engine import replay_models as rm  # noqa: E402
from engine.page_state import PageState, js_state_code  # noqa: E402

METHODS = {"get_scenario_candidates": "getScenarioCandidates", "get_eligible_models": "getEligibleModels",
           "get_replay_timeline_models": "getReplayTimelineModels", "point_in_time_at_replay_head": "pointInTimeAtReplayHead",
           "get_max_frames": "getMaxFrames", "locale_compare": "__lc", "update_ribbon": "__ribbon"}
FUNCS = ["getScenarioCandidates", "getEligibleModels", "getReplayTimelineModels", "pointInTimeAtReplayHead", "getMaxFrames", "getMetricKeys",
         "getStrategyFamily", "modelSearchTerms", "isMetricAwareCriteria", "updateRibbon", "getBasePoint", "getReplayHeadPoint"]
EXTRA = js_state_code() + r"""
// the page (v2.65.36) reads a COLORS list it never defines; the harness defines the engine's fallback palette so the page function can run
globalThis.COLORS = ['#f59e0b', '#e879f9', '#34d399', '#fb7185', '#a78bfa', '#f97316', '#38bdf8', '#facc15', '#2dd4bf', '#c084fc'];
globalThis.productTypeFilter = { value: '' };
async function __models(fx, name, c) {
  __ps_set(c.state);
  globalThis.ALL_CRITERIA_DATA = c.criteria;
  let ret;
  try { ret = globalThis[name](); } catch (e) { ret = { error: true }; }
  return { state: __ps_get(), ret: ret === undefined ? null : ret };
}
const __node = (init) => { let t = init; return { get textContent(){ return t; }, set textContent(v){ t = (v === null || v === undefined) ? '' : String(v); },
  className: '', style: { backgroundColor: init } }; };
async function __ribbon(fx, name, c) {
  __ps_set(c.state);
  globalThis.ALL_CRITERIA_DATA = c.criteria; globalThis.SCENARIOS_CATALOGUE = c.catalogue;
  const R = c.ribbon;
  globalThis.ribbonModelName = __node(R.model_name); globalThis.ribbonProduct = __node(R.product); globalThis.ribbonStrategy = __node(R.strategy);
  globalThis.ribbonTotNet = __node(R.tot_net); globalThis.ribbonBuyNet = __node(R.buy_net); globalThis.ribbonSellNet = __node(R.sell_net);
  globalThis.totalNetLabel = __node(R.total_label); globalThis.buyNetLabel = __node(R.buy_label); globalThis.sellNetLabel = __node(R.sell_label);
  globalThis.indicatorBar = __node(R.indicator);
  ribbonTotNet.className = R.tot_class; ribbonBuyNet.className = R.buy_class; ribbonSellNet.className = R.sell_class;
  let err = false;
  try { updateRibbon(); } catch (e) { err = true; }
  return { state: __ps_get(), ret: err ? { error: true } : {
    model_name: ribbonModelName.textContent, product: ribbonProduct.textContent, strategy: ribbonStrategy.textContent, tot_net: ribbonTotNet.textContent,
    buy_net: ribbonBuyNet.textContent, sell_net: ribbonSellNet.textContent, tot_class: ribbonTotNet.className, buy_class: ribbonBuyNet.className,
    sell_class: ribbonSellNet.className, total_label: totalNetLabel.textContent, buy_label: buyNetLabel.textContent, sell_label: sellNetLabel.textContent,
    indicator: indicatorBar.style.backgroundColor } };
}
async function __lc(fx, name, c) { return { state: null, ret: c.pairs.map(p => Math.sign(p[0].localeCompare(p[1]))) }; }
"""
IDS = ["M1", "m2", "M10", "DNA_201700", "DNA_20170", "dna_201700", "breakout_R_1", "Breakout-2", "a b", "A_b", "a_B", "M-1", "M_1", "x.y", "Z9", "z9"]
STRATS = ["breakout", "breakout_R", "breakout_R_Rev", "breakout_Rev", "breakout_r_rev_5", "breakout_rev_2", "other", "", None]
NUMS = [0, 0.0, 1.0, 1.004, 1.006, 2.5, -0.005, 7.25, -3, None, "4.5", "x"]
CRIT = ["top_net", "top_win", "top5_breakout", "top3_tp3_sl3", "top3_momentum_net", "top1_at_time", "family_leaders", "NET_RETURN"]


def mkmodel(rng, mid=None):
    m = {"model": mid or rng.choice(IDS), "color": "#112233"}
    if rng.random() < 0.9:
        m["product"] = rng.choice(["gbp", "EUR", "gbp", "Eur"])
    if rng.random() < 0.8:
        m["product_type"] = rng.choice(["forex", "crypto", "Forex"])
    if rng.random() < 0.9:
        m["strategy"] = rng.choice(STRATS)
    for k in ("cum_net", "cum_alt_net"):
        if rng.random() < 0.8:
            m[k] = rng.choice(NUMS)
    for k in ("win_rate", "alt_win_rate"):
        if rng.random() < 0.7:
            m[k] = rng.choice([0, 10, 55, 80, None, 49.9, 50])
    n = rng.choice([0, 1, 3, 5])
    start = rng.choice([0, 0, 1, 2])
    m["series"] = [{"time": f"{h + start:02d}:00", "net": rng.choice([1.0, 2.0, 0.5, None]), "alt_net": rng.choice([1.0, -2.0, 0.5])} for h in range(n)]
    if rng.random() < 0.3:
        m["comparisonRole"] = rng.choice(["selected-time #1", "selected-time #12", "searched model", "x"])
    return m


def tied(rng, models):
    """Half the time give the models identical returns, so the tie-break (localeCompare on ids) decides the order."""
    if rng.random() < 0.5:
        v = rng.choice([1.0, 2.5, 0])
        for m in models:
            m["cum_net"] = m["cum_alt_net"] = v
    return models


def mklist(rng, lo=0, hi=5):
    return [mkmodel(rng) for _ in range(rng.randint(lo, hi))]


def make_case(rng, method):
    if method == "locale_compare":
        chars = "aAbBzZ09_-. xX,"
        pairs = [["".join(rng.choice(chars) for _ in range(rng.randint(0, 5))), "".join(rng.choice(chars) for _ in range(rng.randint(0, 5)))] for _ in range(40)]
        pairs += [["M1", "m2"], ["m1", "M1"], ["a", "A"], ["", "a"], ["a_", "ab"]]
        return {"pairs": pairs, "state": PageState().snapshot(), "criteria": {}}
    st = PageState()
    date = rng.choice(dp.DATES)
    crit = rng.choice(CRIT)
    ret = rng.choice(["NET", "ALT"])
    ptr = lambda: rng.choice([None, [], mklist(rng, 1, 4)])  # noqa: E731
    st.update({
        "current_date": date, "current_criteria": crit, "return_type": ret, "pit_mode": rng.random() < 0.35, "pit_models": ptr(),
        "deep_link_only": rng.random() < 0.15, "active_portfolio": rng.choice([None, None, "P1"]), "portfolio_models": tied(rng, mklist(rng, 2, 6)),
        "min_win_rate": rng.choice([0, 10, 50]), "product_type": rng.choice(["all", "forex", "crypto"]), "product": rng.choice(["all", "gbp", "eur"]),
        "strategy_family": rng.choice(["all", "breakout", "breakout_r", "unknown"]),
        "model_search_input": rng.choice(["", "", "m1", "M1", " dna_201700 ", "m1,dna_201700", "zzz", "m", "m1 m2 z9", "m1  m2", "m1_m2", "Breakout 4 TP20"]),   # v2.65.35: spaces count as '_'
        "search_loaded": rng.choice([[], mklist(rng, 0, 3)]), "scenario_removed": set(rng.sample(IDS, rng.randint(0, 3))), "frame": rng.choice([-1, 0, 1, 2, 9]),
        "pit_timeline_models": rng.choice([[], mklist(rng, 1, 3)]), "model_search_status": rng.choice(["", "old"]),
    })
    st.update({"baseline": rng.choice([0, 0, 1, 2, 4]), "split_mode": rng.choice(["ALL_NET", "TRI_SPLIT", "BUY_NET", "SELL_NET", "MULTI_SPLIT"]),
               "selected_model_index": rng.choice([0, 1, 2, 7, -1]), "visible": set(rng.sample(IDS, rng.randint(0, 8)))})
    pinned = {}
    for _ in range(rng.choice([0, 0, 1, 2])):
        pm = mkmodel(rng)
        pinned[pm["model"]] = pm
    st.pinned.update(pinned)
    if rng.random() < 0.3:  # plain active-portfolio listing with tied returns: the order is decided by localeCompare on the ids
        st.update({"active_portfolio": "P1", "pit_mode": False, "deep_link_only": False, "min_win_rate": 0, "product_type": "all", "product": "all",
                   "strategy_family": "all", "model_search_input": "", "portfolio_models": tied(rng, [mkmodel(rng) for _ in range(rng.randint(2, 6))])})
        for m in st.portfolio_models:
            m.pop("win_rate", None)
            m.pop("alt_win_rate", None)
        st.pinned.clear()
    if st.search_loaded and rng.random() < 0.5:
        st.model_search_input = rng.choice(st.search_loaded)["model"].lower()
    for m in st.search_loaded:   # a searched model without a colour takes the fallback palette (selected-time mode)
        if rng.random() < 0.4 and method == "get_eligible_models":   # only where the colour is read; the ribbon shim stores an undefined colour literally, which a real DOM ignores
            m.pop("color", None)
    normalized = re.sub(r"\s+", "_", str(st.model_search_input or "").strip().lower())   # what the page compares the resolved query with
    st.search_resolved_query = rng.choice([None, normalized, normalized, "another_query"])
    st.search_resolved_message = rng.choice(["", "No model ID or strategy name matches “x” for 2026-10-14", "No model data found for 2026-10-14: m1", "Database search failed: boom"])
    if st.active_portfolio:   # page v2.65.50: Find model is portfolio based: searched and pinned models must be members (ids in any case, sometimes none, sometimes the key is absent)
        pool = [m["model"] for m in st.search_loaded] + list(st.pinned) + [m["model"] for m in st.portfolio_models] + rng.sample(IDS, rng.randint(0, 3))
        members = [x.upper() if rng.random() < 0.3 else x for x in pool if rng.random() < 0.6]
        if rng.random() < 0.1:
            st.portfolios.pop("P1", None)
        else:
            st.portfolios["P1"] = members
    snap = st.snapshot()
    criteria = {}
    for key in {crit, f"{crit}_net", f"{crit}_alt", "top_net"}:
        if rng.random() < 0.7:
            criteria[key] = {date: rng.choice([[], mklist(rng, 1, 5)]), rng.choice(dp.DATES): mklist(rng, 0, 2)}
    ribbon = {k: rng.choice(["", "old"]) for k in rm._RIBBON_FIELDS}
    catalogue = [{"id": c, "name": rng.choice(["Name " + c, None])} if rng.random() < 0.6 else {"id": "zz"} for c in CRIT[:4]]
    return {"state": snap, "criteria": criteria, "ribbon": ribbon, "catalogue": catalogue}


def run_python(method, case):
    if method == "locale_compare":
        return {"state": None, "ret": [rm.locale_compare(a, b) for a, b in case["pairs"]]}
    cl = dc.DataClient(lambda url: (404, {}), "http://api")
    cl.criteria_data = copy.deepcopy(case["criteria"])
    st = PageState.from_snapshot(case["state"])
    try:
        if method == "update_ribbon":
            names = {c["id"]: c.get("name", rm._UNDEF) for c in case["catalogue"]}
            ret = rm.update_ribbon(st, cl, dict(case["ribbon"]), names)
        else:
            ret = getattr(rm, method)(st, cl)
    except Exception:  # noqa: BLE001
        ret = {"error": True}
    return {"state": st.snapshot(), "ret": ret}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=400)
    ap.add_argument("--methods", default="")
    ns = ap.parse_args()
    methods = [m for m in ns.methods.split(",") if m] or list(METHODS)
    rng = random.Random(21)
    cases, expected = [], {}
    for method in methods:
        for _ in range(ns.cases):
            case = make_case(rng, method)
            cid = len(cases) + 1
            cases.append({"id": cid, "call": {"locale_compare": "__lc", "update_ribbon": "__ribbon"}.get(method, "__models"), "args": [{}, METHODS[method], case]})
            expected[cid] = (method, run_python(method, case))
    spec = {"page": str(dp.PAGE), "inventory": str(dp.INVENTORY), "functions": FUNCS, "extra": EXTRA, "cases": cases}
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
        d = dp.diff(json.loads(json.dumps(exp, default=str)), r["result"])
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
