# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/check_thin_boundary.py — what logic is still in the generated thin page, and is that exactly the documented boundary?
#
# VERSION HISTORY
# v1.0.0 · 2026-10-18 · Initial version: item 15's "no embedded engine" check.
"""Usage: python tools/check_thin_boundary.py [--json]. Exit 1 if the built page's boundary differs from the documented one.

The thin page is built from the source page by tools/build_thin_page.py. This tool parses BOTH with the inventory builder and compares function by function:
  * every controller delegated to the engine (tools/controller_wrappers.CONTROLLERS) must be a wrapper in the built page, and its original body must be gone;
  * the rule logic removed for the engine calls (build report 'removed' / 'entry_points_now_engine_calls') must be gone;
  * the only original-function copy kept for a fallback is activatePortfolio (a LIVE / LIVE_ALT tab places orders; the engine refuses it);
  * the ported controllers that stay in the page are exactly BOUNDARY below, each for a stated reason."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build_inventory  # noqa: E402
import controller_wrappers as cw  # noqa: E402

VERSION = "v2.65.34"
SOURCE = ROOT / f"top10_5min_equity_curves_source_{VERSION}.html"
BUILT = ROOT / f"top10_5min_equity_curves_engine_client_{VERSION}.html"

# ported (or portable) controllers that deliberately stay in the page, with the reason
BOUNDARY = {
    "loadPortfolioData": "data layer: HTTP + the page-owned portfolio view caches (the engine asks the page to await it)",
    "fetchPortfolioData": "data layer: HTTP + the page-owned caches and the in-flight request map",
    "ensureHistoricalDataLoaded": "data layer: optional static bundle fetch",
    "loadOverlayRuleLibrary": "data layer: rule library fetch",
    "deletePortfolio": "UI glue: a confirm() dialog, then removePortfolios (delegated)",
    "deleteSelectedPortfolios": "UI glue: a confirm() dialog, then removePortfolios (delegated)",
    "activePortfolioOverlayRule": "a lookup the redraw / rotation paths call per frame: a synchronous engine call each time would cost more than it saves",
    "assignedPortfolioOverlayRule": "as above",
    "loadModelSearchFromDatabase": "ported (engine stages, parity-tested) but not delegated: a synchronous engine call froze the page 0.6-0.8 s per call, against 18-40 ms for the page's own copy",
    "loadDeepLinkModelsFromDatabase": "as above",
    "livePortfolioModelsForDate": "a pure lookup on live-portfolio store data the page owns (live tabs place orders)",
}
FALLBACK_COPIES = {"activatePortfolio"}   # the original, kept only for LIVE / LIVE_ALT tabs


def _functions(path: Path) -> dict:
    inv = build_inventory.build(path)
    lines = path.read_text(encoding="utf-8").split("\n")
    out = {}
    for f in inv["functions"]:
        out[f["name"]] = "\n".join(lines[f["start_line"] - 1:f["end_line"]])
    return out


def analyse() -> dict:
    src, built = _functions(SOURCE), _functions(BUILT)
    report = json.loads(BUILT.with_suffix(".build.json").read_text(encoding="utf-8"))
    problems, delegated, kept_original = [], [], []
    norm = lambda t: re.sub(r"\s+", " ", t).strip()   # noqa: E731
    page_text = norm(BUILT.read_text(encoding="utf-8"))
    for name in cw.CONTROLLERS:
        body = built.get(name, "")
        if "__engineCommand(" not in body:
            problems.append(f"{name}: not a wrapper in the built page")
            continue
        delegated.append(name)
        original = norm(src[name])
        # the original text may legitimately survive ONLY as the fallback copy of an allowed function
        if original in page_text and name not in FALLBACK_COPIES:
            problems.append(f"{name}: its original body is still in the built page")
    for name in report["removed"] + report["entry_points_now_engine_calls"]:
        orig = norm(src[name])
        if orig in page_text:
            problems.append(f"{name}: rule logic that should have moved to the engine is still in the page")
    copies = set(re.findall(r"function __original_(\w+)\(", BUILT.read_text(encoding="utf-8")))
    if copies != FALLBACK_COPIES:
        problems.append(f"original-function fallback copies are {sorted(copies)}, documented {sorted(FALLBACK_COPIES)}")
    for name, reason in BOUNDARY.items():
        if name not in built:
            problems.append(f"{name}: documented as staying in the page but not in the built page")
        elif norm(built[name]) != norm(src[name]):
            problems.append(f"{name}: documented as unchanged in the page but it differs from the source")
        else:
            kept_original.append(name)
    return {"delegated": sorted(delegated), "kept_in_page": {n: BOUNDARY[n] for n in kept_original}, "fallback_copies": sorted(copies),
            "removed_to_engine_calls": report["removed"] + report["entry_points_now_engine_calls"], "problems": problems}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ns = ap.parse_args()
    r = analyse()
    if ns.json:
        print(json.dumps(r, indent=1))
    else:
        print(f"delegated to the engine: {len(r['delegated'])} controllers; rule logic moved to engine calls: {len(r['removed_to_engine_calls'])} functions")
        print(f"original-function copies kept for a fallback: {r['fallback_copies']}")
        print("controllers deliberately kept in the page:")
        for n, why in r["kept_in_page"].items():
            print(f"  {n}: {why}")
        print("PROBLEMS:" if r["problems"] else "boundary OK")
        for p in r["problems"]:
            print("  ", p)
    return 1 if r["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
