"""EP051 liveness and readiness checks. Version 1.0.0 (2026-08-23)."""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]

def liveness() -> tuple[int, dict]:
    return 200, {"status": "ok", "service": "ep051-directory"}

def readiness(env: dict[str, str] | None = None) -> tuple[int, dict]:
    values = os.environ if env is None else env
    checks = {
        "manifest": (ROOT / "decomposition_manifest.json").is_file(),
        "directory_ui": (ROOT / "workstreams" / "WF-301" / "directory.html").is_file(),
        "broker_disabled": values.get("EP051_BROKER_PROFILE", "disabled") == "disabled",
    }
    snapshot = values.get("EP051_SNAPSHOT", "not-published")
    ok = all(checks.values())
    return (200 if ok else 503), {
        "status": "ready" if ok else "not_ready",
        "checks": checks,
        "snapshot": snapshot,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
