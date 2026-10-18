# epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/mutate_check.py — mutation check for the page controller (engine/page.py, page_state.py, rule_editor.py).
#
# VERSION HISTORY
# v1.7.0 · 2026-10-18 · runner 'stages' (tests/test_stages.py: the engine stages branch by branch).
# v1.6.0 · 2026-10-17 · runner 'wrap' (diff_page_js_vs_py with DIFF_WRAPPERS=1: the engine-delegating controller wrappers).
# v1.5.0 · 2026-10-17 · runner 'intel' (intelligence + watches tests).
# v1.4.0 · 2026-10-17 · runner 'thin' (rebuilds the engine-client page, then diff_thin_js_vs_py); fname may be relative to the package root (tools/…, runner/static/…).
# v1.3.1 · 2026-10-17 · a pytest run that ends in an ERROR (not a test failure) is a CRASH, not a kill: errors under parallel load had been counted as kills.
# v1.3.0 · 2026-10-17 · runner 'pytest' (mutants in runner/*.py are checked by the runner's own tests).
# v1.2.0 · 2026-10-17 · runner 'reports' (diff_reports_js_vs_py).
# v1.1.1 · 2026-10-17 · the temp copy includes the frozen page snapshot + inventory (the editor / models harnesses use them by default).
# v1.1.0 · 2026-10-17 · runner 'models' (diff_models_js_vs_py).
# v1.0.1 · 2026-10-17 · temp dir cleanup tolerates Windows file locks.
# v1.0.0 · 2026-10-17 · Initial version: each mutant changes ONE behaviour in a throwaway copy of engine/ + tools/; the matching differential run must report a failing group.
"""Usage: python tools/mutate_check.py [--only name,name] [--jobs N]. A mutant is KILLED if any group in its differential run fails, ALIVE if every group passes,
CRASH if the run produced no results (a crash is not counted as a kill). ALIVE mutants must be explained (equivalent) or the tests strengthened."""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

V2 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(V2 / "tools"))
from mutants_page import MUTANTS  # noqa: E402

PAGE = V2 / "top10_5min_equity_curves_source_v2.65.32.html"
INV = V2 / "inventory_v2.65.32" / "inventory.json"
CASES = os.environ.get("MUT_CASES", "60")


def run_one(m):
    name, fname, old, new, runner, methods = m[:6]
    count = m[6] if len(m) > 6 else 1
    folder = "runner" if runner == "pytest" else "engine"
    rel = Path(fname) if "/" in fname else Path(folder) / fname   # fname may be given relative to the package root
    src = (V2 / rel).read_text(encoding="utf-8")
    if src.count(old) != count:
        return name, f"BADPATTERN({src.count(old)})", ""
    td = tempfile.mkdtemp(prefix="mut_")
    try:
        d = Path(td)
        shutil.copytree(V2 / "engine", d / "engine", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(V2 / "tools", d / "tools", ignore=shutil.ignore_patterns("__pycache__"))
        if runner in ("pytest", "thin", "intel", "wrapjs", "stages"):
            shutil.copytree(V2 / "runner", d / "runner", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(V2 / "tests", d / "tests", ignore=shutil.ignore_patterns("__pycache__"))
        (d / rel).write_text(src.replace(old, new), encoding="utf-8")
        if runner == "thin":  # rebuild the engine-client page from the (possibly mutated) generator before comparing
            shutil.copy2(PAGE, d / PAGE.name)
            shutil.copytree(INV.parent, d / INV.parent.name, dirs_exist_ok=True)
            b = subprocess.run([sys.executable, str(d / "tools" / "build_thin_page.py"), str(d / PAGE.name)], capture_output=True, text=True, encoding="utf-8", cwd=str(V2),
                               env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            if b.returncode != 0:
                refused = "BUILD REFUSED" in (b.stdout + b.stderr)  # the generator's own consistency check caught it: that is a kill
                return name, ("KILLED" if refused else "CRASH"), "build refused: " + (b.stdout + b.stderr)[-160:].replace("\n", " ")
        shutil.copy2(PAGE, d / PAGE.name)
        shutil.copytree(INV.parent, d / INV.parent.name, dirs_exist_ok=True)
        if runner in ("page", "wrap"):
            cmd = [sys.executable, str(d / "tools" / "diff_page_js_vs_py.py"), str(PAGE), "--inventory", str(INV), "--cases", CASES, "--methods", methods]
        elif runner == "pytest":
            cmd = [sys.executable, "-m", "pytest", str(d / "tests" / "test_runner.py"), str(d / "tests" / "test_runner_server.py"), "-q", "-x", "-p", "no:cacheprovider"]
        elif runner == "stages":
            cmd = [sys.executable, "-m", "pytest", str(d / "tests" / "test_stages.py"), "-q", "-x", "-p", "no:cacheprovider"]
        elif runner == "wrapjs":
            cmd = [sys.executable, "-m", "pytest", str(d / "tests" / "test_controller_wrappers.py"), "-q", "-x", "-p", "no:cacheprovider"]
        elif runner == "reports":
            cmd = [sys.executable, str(d / "tools" / "diff_reports_js_vs_py.py"), "--cases", CASES]
        elif runner == "intel":
            cmd = [sys.executable, "-m", "pytest", str(d / "tests" / "test_intelligence.py"), str(d / "tests" / "test_runner_intel.py"), str(d / "tests" / "test_arena_provider.py"), "-q", "-x", "-p", "no:cacheprovider"]
        elif runner == "thin":
            cmd = [sys.executable, str(d / "tools" / "diff_thin_js_vs_py.py"), "--cases", CASES]
        elif runner == "dates":
            cmd = [sys.executable, str(d / "tools" / "diff_available_dates.py"), str(PAGE)]
        elif runner == "models":
            cmd = [sys.executable, str(d / "tools" / "diff_models_js_vs_py.py"), "--cases", CASES, "--methods", methods]
        else:
            cmd = [sys.executable, str(d / "tools" / "diff_rule_editor_js_vs_py.py"), "--cases", CASES, "--methods", methods]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=1800, cwd=str(V2),
                           env={**os.environ, "PYTHONIOENCODING": "utf-8", "DIFF_WORKERS": "4", **({"DIFF_WRAPPERS": "1"} if runner == "wrap" else {})})
        if runner in ("pytest", "intel", "wrapjs", "stages"):
            tail = r.stdout.strip().splitlines()[-1:] or [""]
            if r.returncode != 0 and not re.search(r"\d+ failed", r.stdout):
                tail = [r.stdout[-700:].replace("\n", " | ")]
            return name, ("ALIVE" if r.returncode == 0 else ("KILLED" if re.search(r"\d+ failed", r.stdout) else "CRASH")), tail[0][:100]
        rows = re.findall(r"^(\w+)\s+cases=\s*\d+ pass=\s*\d+ fail=\s*(\d+) js_error=(\d+)", r.stdout, re.M)
        if not rows:
            return name, "CRASH", (r.stdout + r.stderr)[-300:]
        failing = [row[0] for row in rows if int(row[1]) or int(row[2])]
        return name, ("KILLED" if failing else "ALIVE"), ",".join(failing)
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=3)
    ns = ap.parse_args()
    only = {x for x in ns.only.split(",") if x}
    todo = [m for m in MUTANTS if not only or m[0] in only]
    with ThreadPoolExecutor(ns.jobs) as ex:
        results = list(ex.map(run_one, todo))
    alive = 0
    for name, status, detail in results:
        print(f"{status:12s} {name:44s} {detail[:120]}")
        alive += status != "KILLED"
    print(f"\n{len(results) - alive}/{len(results)} killed; {alive} not killed")


if __name__ == "__main__":
    main()
