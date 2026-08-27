"""Portable EP051 CI quality gates. Version 1.0.0 (2026-08-23)."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def run(label: str, command: list[str]) -> dict:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {"gate": label, "passed": result.returncode == 0,
            "output": (result.stdout + result.stderr)[-4000:]}

def main() -> int:
    manifest = json.loads((ROOT / "decomposition_manifest.json").read_text(encoding="utf-8"))
    structural = len(manifest["original_task_list"]) == 44 and all(
        Path(item["task_file"]).is_file() for item in manifest["original_task_list"])
    gates = [{"gate": "manifest_structure", "passed": structural, "output": "44 tasks and task paths"}]
    gates += [
        run("environment", [sys.executable, str(ROOT / "workstreams/EP051-INF-004/validate_environment.py")]),
        run("migrations", [sys.executable, str(ROOT / "solution/database/migrate.py")]),
        run("health", [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "solution/health"), "-p", "test_*.py"]),
    ]
    report = ROOT / "verification" / "ci_quality_report.json"
    report.write_text(json.dumps({"version": "1.0.0", "gates": gates}, indent=2), encoding="utf-8")
    for gate in gates: print(f"{'PASS' if gate['passed'] else 'FAIL'} {gate['gate']}")
    return 0 if all(g["passed"] for g in gates) else 1

if __name__ == "__main__": raise SystemExit(main())
