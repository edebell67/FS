# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/build_engine_map.py — builds a first engine map for a page snapshot (use rebase_map.py to carry a reviewed map forward instead).
#
# VERSION HISTORY
# v2.0.0 · 2026-10-16 · Uses map_rules + build_inventory (same rows as rebase_map, incl. ordinal and body hashes); writes engine_map_<version>.json and never overwrites.
# v1.1.0 · 2026-10-16 · Marks the verified ports; rotation functions are ported_partial (overlay-rule path missing).
# v1.0.0 · 2026-10-16 · Initial version: rule-based categories (compute/state/data/live/view/split) over inventory.json; marks the 11 already-ported functions.
"""python build_engine_map.py <page_snapshot.html>   Every ported/provisional row gets verified_body_sha256 = its current body hash,
so only run this on a snapshot the differential test has just passed against."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_inventory  # noqa: E402
import map_rules  # noqa: E402

inv = build_inventory.build(Path(sys.argv[1]))
ver = inv["summary"]["page_version"]
out = HERE.parent / f"engine_map_{ver}.json"
if out.exists():
    sys.exit(f"{out} exists; not overwriting")
rows = []
for f in inv["functions"]:
    cat, status, target = map_rules.classify(f["name"], f["kind"])
    verified = status in ("ported", "ported_partial", "provisional")
    rows.append({"name": f["name"], "ordinal": f["ordinal"], "line": f["start_line"], "lines": f["lines"],
                 "inventory_kind": f["kind"], "category": cat, "status": status, "python_target": target,
                 "body_sha256": f["body_sha256"], "verified_body_sha256": f["body_sha256"] if verified else None,
                 "differential_tested": f["name"] in map_rules.PORTED and f["name"] not in map_rules.NOT_DIFF_TESTED})
summary = {}
for r in rows:
    summary.setdefault(r["category"], {}).setdefault(r["status"], 0)
    summary[r["category"]][r["status"]] += 1
out.write_text(json.dumps({"page_version": ver, "summary": summary, "rows": rows}, indent=1), encoding="utf-8")
print(out.name, json.dumps(summary))
