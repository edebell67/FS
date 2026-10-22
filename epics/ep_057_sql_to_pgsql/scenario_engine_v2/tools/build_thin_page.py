# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/build_thin_page.py — builds the engine-client copy of the scenario page: the overlay / rotation engine is removed from the page and called in the Python engine.
#
# VERSION HISTORY
# v1.3.0 · 2026-10-17 · stage 1 controllers (8, no network) replaced by wrappers that delegate to the engine (tools/controller_wrappers.py).
# v1.2.0 · 2026-10-17 · --rebuild replaces an existing output only when that file is itself a generated page.
# v1.1.0 · 2026-10-17 · inlines runner/static/launch_panel.js after the main script (the 'Virtual race' button and panel).
# v1.0.0 · 2026-10-17 · Initial version: removes 12 functions (5 entry points become engine calls), inlines runner/static/engine_client.js and launch_panel.js, checks engine/rpc.py's global list against the page, never overwrites.
"""Usage: python build_thin_page.py [snapshot.html] [--inventory inventory.json] [--out top10_5min_equity_curves_engine_client_<version>.html]

The copy is generated, not hand-edited, so it can be rebuilt whenever the page moves to a new version. The build FAILS if (a) the output exists, (b) a function it must replace is missing
from the page, or (c) the globals a moved function reads no longer match engine/rpc.py GLOBALS (the page changed in a way the engine contract does not cover)."""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import build_inventory  # noqa: E402
import controller_wrappers as cw  # noqa: E402
from engine import rpc  # noqa: E402

ENTRY_POINTS = ["computeTradeOverlaySignals", "pairOverlayTrades", "computeSplitTargetSignal", "computeLeaderRotation", "computeMultiSplitRotation"]
# only reachable from the entry points above (checked below): the assigned-rule path
REMOVED = ["applyAssignedOverlayTradeResults", "assignedRuleTarget", "sourceTradeFlipResults", "overlayRuleCandidate", "overlayRuleMetricValue", "asOfCorrelation",
           "curvePointAtOrBefore"]
# kept in the page: it builds the key under which the data layer stores each model's source trades
KEPT_WITH_DATA_LAYER = ["assignedOverlayTradeCacheKey"]


def globals_object(names):
    return "{ " + ", ".join(names) + " }"


def stub_for(name: str) -> str:
    g = globals_object(rpc.GLOBALS[name])
    if name == "computeTradeOverlaySignals":
        return f"    function computeTradeOverlaySignals(seriesSlice, basePt) {{\n      return __engine.call({{ fn: 'computeTradeOverlaySignals', args: [seriesSlice, basePt], globals: {g} }});\n    }}"
    if name == "pairOverlayTrades":
        return "    function pairOverlayTrades(signals, seriesSlice, basePt) {\n      return __engine.call({ fn: 'pairOverlayTrades', args: [signals, seriesSlice, basePt], globals: {} });\n    }"
    if name == "computeSplitTargetSignal":
        return f"    function computeSplitTargetSignal(signals, seriesSlice, basePt) {{\n      return __engine.call({{ fn: 'computeSplitTargetSignal', args: [signals, seriesSlice, basePt], globals: {g} }});\n    }}"
    rotation_globals = globals_object(rpc.GLOBALS["computeLeaderRotation"])
    if name == "computeLeaderRotation":
        helper = f"""    // The overlay / rotation engine runs in the Python engine (engine/rpc.py): the page sends what it was called with, the globals the function reads, the assigned overlay rule
    // and the source-trade cache, and gets back exactly what the function returned (trades without their curveModel handle, which is re-attached here from the model id).
    function __engineRotationRequest(fn, models, second, upToIdx, replaySeries) {{
      const replayIndex = replaySeries ? models.findIndex(model => model.series === replaySeries) : -1;
      const rule = activePortfolioName ? activePortfolioOverlayRule() : null;
      return {{ fn, args: [models, second, upToIdx, replayIndex >= 0 ? null : (replaySeries ?? null)], replayIndex: replayIndex >= 0 ? replayIndex : null,
        globals: {rotation_globals}, rule,
        tradeCache: rule ? [...assignedOverlayTradeCache.entries()] : [],
        now: rule && currentDate === LIVE_DATE ? Date.now() : null, maxFrames: rule ? getMaxFrames() : null }};
    }}
    function __engineRelinkTrades(result, models) {{
      const byId = new Map(models.map(model => [model.model, model]));
      return {{ ...result, trades: result.trades.map(trade => ({{ ...trade, curveModel: byId.get(trade.model) }})) }};
    }}
"""
        return helper + "    function computeLeaderRotation(activeModels, metricKey, upToIdx, replaySeries = null) {\n" \
            "      return __engineRelinkTrades(__engine.call(__engineRotationRequest('computeLeaderRotation', activeModels, metricKey, upToIdx, replaySeries)), activeModels);\n    }"
    if name == "computeMultiSplitRotation":
        return "    function computeMultiSplitRotation(activeModels, keys, upToIdx, replaySeries = null) {\n" \
            "      return __engineRelinkTrades(__engine.call(__engineRotationRequest('computeMultiSplitRotation', activeModels, keys, upToIdx, replaySeries)), activeModels);\n    }"
    raise KeyError(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?", default=str(ROOT / "top10_5min_equity_curves_source_v2.65.56.html"))
    ap.add_argument("--inventory", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--rebuild", action="store_true", help="replace an existing output, but only if it is itself a generated engine-client page")
    ns = ap.parse_args()
    page = Path(ns.page)
    inv = build_inventory.build(page)
    version = inv["summary"]["page_version"]
    out = Path(ns.out) if ns.out else ROOT / f"top10_5min_equity_curves_engine_client_{version}.html"
    if out.exists():
        generated = "GENERATED by scenario_engine_v2/tools/build_thin_page.py" in out.read_text(encoding="utf-8")[:6000]
        if not (ns.rebuild and generated):
            sys.exit(f"{out} exists; not overwriting" + ("" if generated else " (and it is not a generated page, so --rebuild would refuse too)"))
    lines = page.read_text(encoding="utf-8").split("\n")
    fn = {f["name"]: f for f in inv["functions"]}
    state = {s["name"] for s in inv["state"]}
    problems = []
    for name in ENTRY_POINTS + REMOVED + KEPT_WITH_DATA_LAYER:
        if name not in fn:
            problems.append(f"function not in the page: {name}")
    if problems:
        sys.exit("; ".join(problems))

    def body(name):
        f = fn[name]
        return "\n".join(lines[f["start_line"] - 1:f["end_line"]])

    ident = re.compile(r"[A-Za-z_$][\w$]*")
    # (c) the globals each entry point reads must be exactly the contract's list
    for name in ENTRY_POINTS:
        text = re.sub(r"//.*|'[^'\n]*'|\"[^\"\n]*\"", "", body(name))
        reads = sorted((set(ident.findall(text)) & state) - {"assignedOverlayTradeCache", "PORTFOLIO_VIEW_REFRESH_MS"})
        contract = sorted(set(rpc.GLOBALS[name]) - {"currentDate", "currentFrameIndex", "currentReturnType", "currentProduct", "currentProductType", "LIVE_DATE"})
        extra = sorted(set(reads) - set(contract))
        if extra:
            problems.append(f"{name} reads globals the engine contract does not carry: {extra}")
    # (d) nothing outside the moved set may call a removed function
    callers = {}
    for other, f in fn.items():
        if other in ENTRY_POINTS + REMOVED:
            continue
        text = "\n".join(lines[f["start_line"] - 1:f["end_line"]])
        for r in REMOVED:
            if re.search(rf"\b{r}\s*\(", text):
                callers.setdefault(r, []).append(other)
    if callers:
        problems.append(f"removed functions are still called by page code: {callers}")
    if problems:
        sys.exit("BUILD REFUSED: " + " | ".join(problems))

    # build: replace from the bottom up so earlier line numbers stay valid
    edits = []
    for name in ENTRY_POINTS:
        edits.append((fn[name]["start_line"], fn[name]["end_line"], stub_for(name).split("\n")))
    for name in REMOVED:
        edits.append((fn[name]["start_line"], fn[name]["end_line"], []))
    decls = cw.declarations(page.read_text(encoding="utf-8"), {st["name"]: st["decl"] for st in inv["state"]})
    first = True
    for name in cw.CONTROLLERS:   # stage 1 controllers: delegated to the engine through __engineCommand
        if name not in fn:
            sys.exit(f"BUILD REFUSED: controller not in the page: {name}")
        new = (cw.helper_block(decls).split("\n") if first else []) + cw.wrapper(name, body(name), body).split("\n")
        first = False
        edits.append((fn[name]["start_line"], fn[name]["end_line"], new))
    for start, end, new in sorted(edits, key=lambda e: -e[0]):
        lines[start - 1:end] = new
    script_open = max(i for i, l in enumerate(lines) if l.strip() == "<script>")
    client = (ROOT / "runner" / "static" / "engine_client.js").read_text(encoding="utf-8").rstrip("\n").split("\n")
    lines[script_open:script_open] = ["  <script>"] + client + ["  </script>", ""]
    main_open = script_open + len(client) + 3
    main_end = next(i for i in range(main_open, len(lines)) if lines[i].strip() == "</script>")
    panel = (ROOT / "runner" / "static" / "launch_panel.js").read_text(encoding="utf-8").rstrip("\n").split("\n")
    lines[main_end + 1:main_end + 1] = ["  <script>"] + panel + ["  </script>"]   # after the main script, so the page's top-level variables are visible by name
    first_version = next(i for i, l in enumerate(lines) if re.match(r"^ \* v\d+\.\d+\.\d+ ·", l))
    lines.insert(first_version, f" * {version} (engine client) · 2026-10-17 · GENERATED by scenario_engine_v2/tools/build_thin_page.py: the overlay / rotation engine "
                                f"({', '.join(ENTRY_POINTS + REMOVED)}) is removed and called in the Python engine (/engine/call) through the inlined engine_client.js. Do not edit; rebuild.")
    out.write_text("\n".join(lines), encoding="utf-8")
    report = {"source": page.name, "version": version, "output": out.name, "entry_points_now_engine_calls": ENTRY_POINTS, "removed": REMOVED, "kept_with_data_layer": KEPT_WITH_DATA_LAYER, "inlined": ["runner/static/engine_client.js", "runner/static/launch_panel.js"], "controllers_delegated": list(cw.CONTROLLERS),
              "lines_before": inv["summary"]["main_script_lines"], "bytes": out.stat().st_size}
    out.with_suffix(".build.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
