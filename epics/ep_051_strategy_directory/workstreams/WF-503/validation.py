"""Portfolio validation gates. Versions: 1.1.0 (2026-08-23) UTC-aware timestamp validation; 1.0.0 initial."""
from __future__ import annotations
from datetime import datetime, timezone


def _aware(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def validate_run(run: dict) -> dict:
    failures = []
    train_end = _aware(run["train_end"])
    holdout_start = _aware(run["holdout_start"])
    universe_as_of = _aware(run["universe_as_of"])
    if train_end >= holdout_start:
        failures.append("TEMPORAL_LEAKAGE")
    if universe_as_of > train_end:
        failures.append("SURVIVORSHIP_RISK")
    required_regimes = set(run["required_regimes"])
    if not required_regimes.issubset(run["regime_results"]):
        failures.append("REGIME_COVERAGE")
    if not {"equal_weight", "simple_selection"}.issubset(run["benchmarks"]):
        failures.append("BASELINE_MISSING")
    if not run.get("risk_disclosures"):
        failures.append("RISKS_MISSING")
    if not run.get("sensitivity_runs"):
        failures.append("SENSITIVITY_MISSING")
    return {"approved": not failures, "failures": failures, "decision": "PROMOTE" if not failures else "HOLD"}
