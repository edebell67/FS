# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/check_drift.py — drift check between the live page and the Python engine, per function.
#
# VERSION HISTORY
# v2.0.0 · 2026-10-16 · Per-function drift: the page's current function bodies are hashed and compared with the hash each port was verified against; finds the map for the page's version (no more stale-map guesswork); reports new/removed functions and untested ports.
# v1.0.0 · 2026-10-16 · Initial version: page version vs engine port version, inventory-vs-map coverage, pending-count report; exits 1 on any drift or pending port work.
"""Usage: python check_drift.py [path-to-page.html]  (default: the live page under dashboards_and_uis/).
Exit codes: 0 = nothing drifted and nothing pending; 1 = drift (a verified port changed, new/removed functions, no map for this
page version) or pending port work. Drift lines start with 'DRIFT', pending with 'PENDING'."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import build_inventory  # noqa: E402

PAGE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "dashboards_and_uis" / "top10_5min_equity_curves.html"
inv = build_inventory.build(PAGE)
version = inv["summary"]["page_version"]
verified_engine = re.search(r'PORTED_FROM_PAGE_VERSION\s*=\s*"([^"]+)"', (ROOT / "engine" / "instance.py").read_text(encoding="utf-8")).group(1)

maps = {}
for p in ROOT.glob("engine_map*.json"):
    m = json.loads(p.read_text(encoding="utf-8"))
    maps[m["page_version"]] = (p, m)
print(f"page version        : {version}  ({inv['summary']['function_count']} functions)")
print(f"engine last verified: {verified_engine}")
if version not in maps:
    print(f"DRIFT: no engine map for page {version} (have {sorted(maps)}). Run: python tools/rebase_map.py <latest map> <its snapshot> <new snapshot>")
    sys.exit(1)
path, emap = maps[version]
print(f"map                 : {path.name}")

rows = {(r["name"], r["ordinal"]): r for r in emap["rows"]}
cur = {(f["name"], f["ordinal"]): f for f in inv["functions"]}
drift, pending = [], []
for k in cur.keys() - rows.keys():
    drift.append(f"new function in page, not in map: {k[0]}#{k[1]}")
for k in rows.keys() - cur.keys():
    drift.append(f"function removed from page: {k[0]}#{k[1]}")
for k, r in rows.items():
    f = cur.get(k)
    if not f:
        continue
    if r["status"] in ("ported", "ported_partial", "provisional"):
        if r["verified_body_sha256"] is None:
            drift.append(f"{k[0]}: ported but has no verified hash")
        elif f["body_sha256"] != r["verified_body_sha256"]:
            drift.append(f"{k[0]}: page body changed since the port was verified, re-verify {r['python_target']}")
        elif not r.get("differential_tested"):
            pending.append(f"{k[0]}: ported but NOT covered by the differential test (DOM-bound page function)")
    elif r["status"] == "pending":
        pending.append(f"{k[0]} [{r['category']}]")

for cat, d in sorted(emap["summary"].items()):
    print(f"  {cat:8s} {d}")
for d in drift:
    print("DRIFT  :", d)
print(f"PENDING: {len(pending)} items" + (" (first 12: " + "; ".join(pending[:12]) + ")" if pending else ""))
sys.exit(1 if drift or pending else 0)
