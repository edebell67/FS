# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/diff_thin_js_vs_py.py — the engine-client copy behaves like the original page: the page's own overlay / rotation functions vs the copy's engine-call stubs (Node) answered by engine/rpc.py.
#
# VERSION HISTORY
# v1.1.0 · 2026-10-17 · live-date staleness (frozen clock), product-specific cache keys, engine errors surfaced as failures.
# v1.0.0 · 2026-10-17 · Initial version: overlay signals, daily-target signal, leader / multi-split rotation (generic and assigned-rule paths) on real and synthetic data; three passes (collect requests, answer them in Python, compare).
"""Usage: python tools/diff_thin_js_vs_py.py [--cases N]. For every case the ORIGINAL function (from the frozen page snapshot) and the thin page's STUB (built by tools/build_thin_page.py) run on the same inputs.
Pass 1 records the requests the stub makes; Python answers each with engine.rpc.dispatch; pass 2 runs both sides and compares the results (the request construction, the engine's answer and the
re-attached curveModel handles are all covered)."""
import argparse
import copy
import json
import random
import subprocess
import sys
import tempfile
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_argv, sys.argv = sys.argv, ["x", str(ROOT / "top10_5min_equity_curves_source_v2.65.32.html"), "--inventory", str(ROOT / "inventory_v2.65.32" / "inventory.json"), "--skip-rules"]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))
import diff_js_vs_py as dj  # noqa: E402
import build_inventory  # noqa: E402
sys.argv = _argv
from engine import core_ported as core  # noqa: E402
from engine import rpc  # noqa: E402
from engine.rpc import RpcError  # noqa: E402,F401
from runner.server import _clean  # noqa: E402

NOW = 1_800_000_000_000
PAGE = ROOT / "top10_5min_equity_curves_source_v2.65.32.html"
INVENTORY = ROOT / "inventory_v2.65.32" / "inventory.json"
ORIG_FUNCTIONS = ["computeTradeOverlaySignals", "pairOverlayTrades", "computeSplitTargetSignal", "computeLeaderRotation", "computeMultiSplitRotation",
                  "applyAssignedOverlayTradeResults", "assignedRuleTarget", "sourceTradeFlipResults", "overlayRuleCandidate", "overlayRuleMetricValue",
                  "asOfCorrelation", "curvePointAtOrBefore", "assignedOverlayTradeCacheKey", "getBasePoint", "getStrategyFamily", "modelPointAtOrBeforeTime",
                  "selectedTimeModelEligibleAt", "selectedTimeJoinAt", "timeOfDayMinutes", "getMetricKeys"]
THIN_FUNCTIONS = ["computeTradeOverlaySignals", "pairOverlayTrades", "computeSplitTargetSignal", "__engineRotationRequest", "__engineRelinkTrades", "computeLeaderRotation", "computeMultiSplitRotation"]


def thin_page() -> Path:
    built = sorted(ROOT.glob("top10_5min_equity_curves_engine_client_v*.html"))
    if not built:
        sys.exit("no engine-client page built: python tools/build_thin_page.py")
    return built[-1]


def make_cases(models_by_date, rng, limit):
    cases = []

    def add(fn, dataset, args, g, rule=None, cache=None, max_frames=None):
        cases.append({"id": len(cases) + 1, "fn": fn, "dataset": dataset, "args": args, "globals": g, "rule": rule, "cache": cache, "maxFrames": max_frames})

    for date, models in models_by_date.items():
        longest = max(models, key=lambda m: len(m["series"]))["series"]
        n = len(longest)
        real_date = date.split("|")[0]
        cache = {}
        for m in models:
            cache[f"{real_date}|forex|all|{m['model']}"] = {"rows": dj.make_rows(m, real_date), "cachedAt": 0}
        entries = [[k, v] for k, v in cache.items()]
        # overlay signals / daily target / paired trades on single models
        for m, rt, bi, et in product(models[:4], ("NET", "ALT"), (0, 40), (0.0, 25.0, 100.0)):
            ser = core.mapped_series(m, rt)
            base = core.base_point(ser, bi)
            sig = core.overlay_signals(ser, base, et)
            g = {"baselineFrameIndex": bi, "exitThreshold": et, "dailyTarget": 500, "currentReturnType": rt}
            add("computeTradeOverlaySignals", None, [ser, base], g)
            for dt in (500, 0, 150):
                add("computeSplitTargetSignal", None, [sig, ser, base], {**g, "dailyTarget": dt})
            add("pairOverlayTrades", None, [sig, ser, base], g)
        # generic rotations (no assigned rule)
        for kind, rt, bi, et, hold, up, dt in product(("leader", "multi"), ("NET", "ALT"), (0, 40), (0.0, 25.0), (1, 2, 3), (n - 1, 150), (500, 0, 250)):
            keys = core.metric_keys(rt)
            g = {"baselineFrameIndex": bi, "exitThreshold": et, "dailyTarget": dt, "overlayTopX": hold, "currentReturnType": rt, "currentDate": real_date,
                 "currentFrameIndex": up, "activePortfolioName": None}
            if kind == "leader":
                add("computeLeaderRotation", date, [{"$ds": 1}, keys["netKey"], up, {"$longest": 1}], g)
            else:
                add("computeMultiSplitRotation", date, [{"$ds": 1}, keys, up, {"$longest": 1}], g)
        # assigned overlay-rule path
        for rname, kind, rt, bi in product(list(dj.RULES), ("leader", "multi"), ("NET", "ALT"), (0, 40)):
            rule = {"id": rname, "name": rname, "config": dj.RULES[rname]}
            keys = core.metric_keys(rt)
            up = n - 1
            g = {"baselineFrameIndex": bi, "exitThreshold": 0, "dailyTarget": 500, "overlayTopX": 1, "currentReturnType": rt, "currentDate": real_date,
                 "currentFrameIndex": -1, "activePortfolioName": "P", "currentProductType": "forex", "currentProduct": "all", "LIVE_DATE": "2099-01-01"}
            fn = "computeLeaderRotation" if kind == "leader" else "computeMultiSplitRotation"
            add(fn, date, [{"$ds": 1}, keys["netKey"] if kind == "leader" else keys, up, {"$longest": 1}], g, rule=rule, cache=entries, max_frames=n)
        # live date: the source-trade cache goes stale after 5 minutes (fresh / stale entries), and a product-specific cache key
        for rname, kind, age in product(("top30", "sell_alt"), ("leader", "multi"), (1000, 400000)):
            rule = {"id": rname, "name": rname, "config": dj.RULES[rname]}
            keys = core.metric_keys("NET")
            fresh = [[k, {**v, "cachedAt": NOW - age}] for k, v in entries]
            g = {"baselineFrameIndex": 0, "exitThreshold": 0, "dailyTarget": 500, "overlayTopX": 1, "currentReturnType": "NET", "currentDate": real_date,
                 "currentFrameIndex": 150, "activePortfolioName": "P", "currentProductType": "forex", "currentProduct": "all", "LIVE_DATE": real_date}
            fn = "computeLeaderRotation" if kind == "leader" else "computeMultiSplitRotation"
            add(fn, date, [{"$ds": 1}, keys["netKey"] if kind == "leader" else keys, 150, {"$longest": 1}], g, rule=rule, cache=fresh, max_frames=n)
        gbp = [[k.replace("|forex|all|", "|forex|gbp|"), v] for k, v in entries]
        for kind in ("leader", "multi"):
            rule = {"id": "top30", "name": "top30", "config": dj.RULES["top30"]}
            keys = core.metric_keys("NET")
            g = {"baselineFrameIndex": 0, "exitThreshold": 0, "dailyTarget": 500, "overlayTopX": 1, "currentReturnType": "NET", "currentDate": real_date,
                 "currentFrameIndex": -1, "activePortfolioName": "P", "currentProductType": "forex", "currentProduct": "gbp", "LIVE_DATE": "2099-01-01"}
            fn = "computeLeaderRotation" if kind == "leader" else "computeMultiSplitRotation"
            add(fn, date, [{"$ds": 1}, keys["netKey"] if kind == "leader" else keys, n - 1, {"$longest": 1}], g, rule=rule, cache=gbp, max_frames=n)
    rng.shuffle(cases)
    cases = cases[:limit]
    for i, c in enumerate(cases):
        c["id"] = i + 1
    return cases


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=400)
    ns = ap.parse_args()
    rng = random.Random(9)
    models_by_date = {d: dj.load_models(d) for d in dj.DATES}
    # a synthetic day too: mixed strategy families and mirrored models, so the similar / opposite / family rule branches fire
    models_by_date["2026-10-14|syn"] = dj.synth(models_by_date["2026-10-14"])
    cases = make_cases(models_by_date, rng, ns.cases)
    datasets = {}
    for c in cases:
        if c["dataset"]:
            key = c["dataset"]
            datasets[key] = models_by_date[key] if key in models_by_date else models_by_date[key.split("|")[0]]
            c["dataset"] = key
    for c in cases:  # `$ds` placeholders carry the dataset name
        if c["dataset"]:
            c["args"] = [{"$ds": c["dataset"]} if isinstance(a, dict) and "$ds" in a else ({"$longest": c["dataset"]} if isinstance(a, dict) and "$longest" in a else a) for a in c["args"]]
    thin = thin_page()
    thin_inv = build_inventory.build(thin)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "thin_inventory.json").write_text(json.dumps(thin_inv), encoding="utf-8")
        spec = {"page": str(PAGE), "inventory": str(INVENTORY), "thinPage": str(thin), "thinInventory": str(td / "thin_inventory.json"), "origFunctions": ORIG_FUNCTIONS,
                "thinFunctions": THIN_FUNCTIONS, "datasets": datasets, "cases": cases, "now": NOW}

        def run(mode, responses=None):
            (td / "spec.json").write_text(json.dumps({**spec, "mode": mode, "responses": responses or {}}), encoding="utf-8")
            r = subprocess.run(["node", str(ROOT / "tools" / "thin_runner.js"), str(td / "spec.json"), str(td / f"out_{mode}.json")], capture_output=True, text=True, encoding="utf-8", timeout=3000)
            if r.returncode != 0:
                print("NODE FAILED:", r.stderr[-1500:])
                sys.exit(2)
            return json.loads((td / f"out_{mode}.json").read_text(encoding="utf-8"))

        collected = run("collect")
        responses = {}
        errors = {}
        for row in collected:
            if row.get("error"):
                errors[row["id"]] = row["error"]
                continue
            for key in row["requests"]:
                if key not in responses:
                    try:
                        responses[key] = json.dumps(_clean(rpc.dispatch(json.loads(key))))
                    except Exception as e:  # noqa: BLE001 - what the service answers with 422; the page throws it
                        responses[key] = f"ERROR: {type(e).__name__}: {e}"
        answered = run("answer", responses)
    by_fn, fails = {}, {}
    for row, case in zip(answered, cases):
        s = by_fn.setdefault(case["fn"], {"cases": 0, "pass": 0, "err": 0})
        s["cases"] += 1
        if row.get("error"):
            s["err"] += 1
            fails.setdefault(case["fn"], []).append(f"case {row['id']}: error {row['error']}")
            continue
        norm = lambda x: json.loads(json.dumps(x))  # noqa: E731
        d = dj.diff(norm(row["thin"]), norm(row["orig"]))
        if d or not row.get("thinLinked"):
            fails.setdefault(case["fn"], []).append(f"case {row['id']}: {d or 'trades not re-linked to their models'}")
        else:
            s["pass"] += 1
    for fn, s in by_fn.items():
        print(f"{fn:34s} cases={s['cases']:4d} pass={s['pass']:4d} fail={s['cases'] - s['pass'] - s['err']:4d} js_error={s['err']}")
        for f in fails.get(fn, [])[:5]:
            print("     ", f[:300])


if __name__ == "__main__":
    main()
