# workstreams/WF-103/reconciliation.py — Fail-closed source/canonical reconciliation for publish gates.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: validates counts, P&L precision, required fields, duplicates, freshness, and backfill equivalence.

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

TOLERANCE = Decimal("0.00000001")
REQUIRED = {"guid", "strategy_id", "signal", "created_at", "exit_at", "net_return", "source_checksum"}


def reconcile(source_rows: list[dict[str, Any]], canonical_rows: list[dict[str, Any]], *, quarantined: int = 0, now: datetime | None = None, source_watermark: datetime | None = None) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    expected = len(source_rows) - quarantined
    checks.append(check("accepted_count", expected == len(canonical_rows), expected, len(canonical_rows)))
    source_total = sum((Decimal(str(r["net_return"])) for r in source_rows if r.get("valid", True)), Decimal("0"))
    canonical_total = sum((Decimal(str(r["net_return"])) for r in canonical_rows), Decimal("0"))
    checks.append(check("net_return_total", abs(source_total - canonical_total) <= TOLERANCE, str(source_total), str(canonical_total)))
    ids = [r.get("guid") for r in canonical_rows]
    checks.append(check("duplicate_guid", len(ids) == len(set(ids)), 0, len(ids) - len(set(ids))))
    missing = sum(1 for row in canonical_rows if REQUIRED - set(row) or any(row.get(field) is None for field in REQUIRED))
    checks.append(check("required_fields", missing == 0, 0, missing))
    impossible = sum(1 for row in canonical_rows if row["exit_at"] < row["created_at"])
    checks.append(check("exit_order", impossible == 0, 0, impossible))
    if source_watermark:
        age = (now or datetime.now(timezone.utc)) - source_watermark
        checks.append(check("closed_freshness", age <= timedelta(hours=1), "<=1:00:00", str(age)))
    return {"publish_allowed": all(item["passed"] for item in checks), "checks": checks}


def compare_backfill(incremental: list[dict[str, Any]], backfill: list[dict[str, Any]]) -> dict[str, Any]:
    def signature(rows: list[dict[str, Any]]) -> list[tuple[Any, ...]]:
        return sorted((r["guid"], str(r["net_return"]), r["source_checksum"]) for r in rows)
    passed = signature(incremental) == signature(backfill)
    return check("backfill_equivalence", passed, signature(incremental), signature(backfill))


def check(rule: str, passed: bool, expected: Any, observed: Any) -> dict[str, Any]:
    return {"rule": rule, "passed": passed, "severity": "blocking", "expected": expected, "observed": observed}

