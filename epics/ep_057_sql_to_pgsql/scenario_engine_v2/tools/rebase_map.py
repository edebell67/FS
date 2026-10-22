# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/rebase_map.py — carries the hand-reviewed engine map forward to a newer page snapshot, matching functions by name.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-16 · Initial version: name+ordinal matching, status carry-over, body-hash change detection for verified ports, new/removed reporting.
"""python rebase_map.py <old_map.json> <old_snapshot.html> <new_snapshot.html>  -> engine_map_<newver>.json (never overwrites).

For every function in the new page: carry category/status/python_target from the old map when the same name (and n-th declaration)
existed; classify new functions with map_rules; record body_sha256 (new page) and, for verified ports, verified_body_sha256 (the old
page's hash, i.e. what the differential test verified). Verified ports whose body changed are flagged, they must be re-verified."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_inventory  # noqa: E402
import map_rules  # noqa: E402

old_map, old_snap, new_snap = (Path(a) for a in sys.argv[1:4])
root = HERE.parent
old_inv, new_inv = build_inventory.build(old_snap), build_inventory.build(new_snap)
new_ver = new_inv["summary"]["page_version"]
out = root / f"engine_map_{new_ver}.json"
if out.exists():
    sys.exit(f"{out} exists; not overwriting")

old = json.loads(old_map.read_text(encoding="utf-8"))
old_rows = {}
for r in old["rows"]:  # old map rows are in page order; derive ordinals
    old_rows.setdefault(r["name"], []).append(r)
old_hash = {(f["name"], f["ordinal"]): f["body_sha256"] for f in old_inv["functions"]}

rows, changed, new_fns, carried = [], [], [], 0
seen = set()
for f in new_inv["functions"]:
    key = (f["name"], f["ordinal"])
    seen.add(key)
    prev = old_rows.get(f["name"], [])
    prev = prev[f["ordinal"] - 1] if len(prev) >= f["ordinal"] else None
    if prev:
        carried += 1
        cat, status, target = prev["category"], prev["status"], prev["python_target"]
    else:
        cat, status, target = map_rules.classify(f["name"], f["kind"])
        new_fns.append(f["name"])
    verified = status in ("ported", "ported_partial", "provisional")
    row = {"name": f["name"], "ordinal": f["ordinal"], "line": f["start_line"], "lines": f["lines"],
           "inventory_kind": f["kind"], "category": cat, "status": status, "python_target": target,
           "body_sha256": f["body_sha256"], "verified_body_sha256": old_hash.get(key) if (verified and prev) else None,
           "differential_tested": f["name"] in map_rules.PORTED and f["name"] not in map_rules.NOT_DIFF_TESTED}
    if verified and prev and row["verified_body_sha256"] != row["body_sha256"]:
        changed.append(f["name"])
    rows.append(row)
removed = [k for k in old_hash if k not in seen]
summary = {}
for r in rows:
    summary.setdefault(r["category"], {}).setdefault(r["status"], 0)
    summary[r["category"]][r["status"]] += 1
out.write_text(json.dumps({"page_version": new_ver, "rebased_from": old["page_version"], "summary": summary, "rows": rows}, indent=1), encoding="utf-8")
print(f"wrote {out.name}: {len(rows)} rows, {carried} carried, {len(new_fns)} new {new_fns[:8]}, {len(removed)} removed {removed[:8]}")
print(f"verified ports whose body CHANGED since verification: {changed or 'none'}")
print(json.dumps(summary))
