# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/diff_available_dates.py — differential test of availableDates: the page's own load-time expression (Node VM, fake clock) vs page_utils.available_dates.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: the page's IIFE is extracted from the frozen snapshot and run with a fixed `new Date()` for 400 instants (year / month / DST boundaries included).
"""Usage: python diff_available_dates.py [page.html] [--cases N]. The JS side evaluates the exact source text of `const availableDates = (() => {...})();`."""
import argparse
import json
import random
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import page_utils as pu  # noqa: E402

NODE_RUNNER = r"""
const vm = require('vm'); const fs = require('fs');
const { src, nows } = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));
const out = nows.map(ms => {
  const RealDate = Date;
  function FakeDate(...a) { return a.length === 0 ? new RealDate(ms) : new RealDate(...a); }
  FakeDate.prototype = RealDate.prototype; FakeDate.now = () => ms;
  const ctx = vm.createContext({ Date: FakeDate, String, JSON });
  return vm.runInContext(src + '; JSON.stringify(availableDates)', ctx);
});
console.log(JSON.stringify(out));
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?", default=str(ROOT / "top10_5min_equity_curves_source_v2.65.32.html"))
    ap.add_argument("--cases", type=int, default=400)
    ns = ap.parse_args()
    text = Path(ns.page).read_text(encoding="utf-8")
    m = re.search(r"const availableDates = \(\(\) => \{.*?\n    \}\)\(\);", text, re.S)
    assert m, "availableDates expression not found in the page"
    rng = random.Random(5)
    nows = [int(datetime(2026, 10, 17, 9, 0).timestamp() * 1000)]
    for y, mo, d in [(2026, 1, 3), (2026, 3, 1), (2026, 3, 29), (2026, 10, 25), (2026, 12, 31), (2027, 1, 1), (2028, 2, 29), (2028, 3, 1), (2026, 11, 2)]:
        for h in (0, 1, 11, 12, 13, 23):
            nows.append(int(datetime(y, mo, d, h, 30).timestamp() * 1000))
    while len(nows) < ns.cases:
        nows.append(int(datetime(2025, 1, 1).timestamp() * 1000) + rng.randrange(0, 3 * 365 * 24 * 3600) * 1000)
    tmp = Path(ROOT / "tools" / "_avail_cases.json")
    tmp.write_text(json.dumps({"src": m.group(0), "nows": nows}), encoding="utf-8")
    try:
        r = subprocess.run(["node", "-e", NODE_RUNNER, str(tmp)], capture_output=True, text=True, encoding="utf-8")
    finally:
        tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        print("NODE FAILED:", r.stderr[-1500:])
        sys.exit(2)
    js = [json.loads(x) for x in json.loads(r.stdout)]
    bad = []
    for ms, got in zip(nows, js):
        want = pu.available_dates(datetime.fromtimestamp(ms / 1000))
        if want != got:
            bad.append((datetime.fromtimestamp(ms / 1000).isoformat(), want, got))
    print(f"available_dates                    cases={len(nows):4d} pass={len(nows) - len(bad):4d} fail={len(bad):4d} js_error=0")
    for b in bad[:5]:
        print("     ", b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
