# workstreams/WF-102/pipeline.py — Reference canonical ingestion with idempotency, role separation, watermarks, and quarantine.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: implements deterministic closed/open ingestion behavior for WF-102 validation.

from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

SOURCES = {"combined_trades_closed", "combined_trades_open"}
DNA_ID = re.compile(r"^DNA_[0-9]+$")


def _timestamp(value: Any) -> datetime:
    parsed = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def _strategy_id(model: Any) -> str:
    normalized = str(model).strip().upper()
    if normalized.endswith(("_S", "_B")):
        normalized = normalized[:-2]
    if not DNA_ID.fullmatch(normalized):
        raise ValueError("invalid DNA model")
    return normalized


def _decimal(value: Any) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError) as exc:
        raise ValueError("invalid decimal") from exc
    if not result.is_finite():
        raise ValueError("decimal must be finite")
    return result.quantize(Decimal("0.00000001"))


def _checksum(record: dict[str, Any]) -> str:
    body = json.dumps(record, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(body.encode()).hexdigest()


class CanonicalIngestion:
    def __init__(self) -> None:
        self.closed: dict[str, dict[str, Any]] = {}
        self.open: dict[str, dict[str, Any]] = {}
        self.watermarks: dict[str, tuple[datetime, str]] = {}
        self.quarantine: list[dict[str, Any]] = []
        self.runs: list[dict[str, Any]] = []

    def ingest(self, source: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
        if source not in SOURCES:
            raise ValueError("unsupported source")
        run = {"run_id": str(uuid.uuid4()), "source": source, "input": len(rows), "accepted": 0, "unchanged": 0, "quarantined": 0}
        target = self.closed if source.endswith("closed") else self.open
        newest = self.watermarks.get(source)
        for raw in rows:
            guid = str(raw.get("guid", "")).strip()
            try:
                if not guid:
                    raise ValueError("missing guid")
                canonical = self._canonicalize(source, raw)
                existing = target.get(guid)
                if existing:
                    if existing["source_checksum"] == canonical["source_checksum"]:
                        run["unchanged"] += 1
                        continue
                    if source.endswith("closed"):
                        raise ValueError("conflicting closed replay")
                target[guid] = canonical
                run["accepted"] += 1
                candidate = (canonical["source_updated_at"], guid)
                newest = max(newest, candidate) if newest else candidate
            except (ValueError, KeyError) as exc:
                self.quarantine.append({"source": source, "guid": guid or None, "reason": str(exc), "raw": raw, "run_id": run["run_id"], "replay_state": "pending"})
                run["quarantined"] += 1
        if newest:
            self.watermarks[source] = newest
        run["status"] = "passed"
        self.runs.append(run)
        return run

    def _canonicalize(self, source: str, raw: dict[str, Any]) -> dict[str, Any]:
        signal = str(raw["signal"]).strip().upper()
        if signal not in {"BUY", "SELL"}:
            raise ValueError("invalid signal")
        created_at = _timestamp(raw["created"])
        last_update = _timestamp(raw["last_update"])
        common = {"guid": str(raw["guid"]), "strategy_id": _strategy_id(raw["model"]), "source_model": str(raw["model"]), "signal": signal, "created_at": created_at}
        if source.endswith("closed"):
            exit_at = _timestamp(raw.get("g_close_time") or raw["last_update"])
            if exit_at < created_at:
                raise ValueError("exit precedes entry")
            net_return = _decimal(raw["net_return"])
            common.update({"exit_at": exit_at, "net_return": net_return, "outcome": "winner" if net_return > 0 else "loser" if net_return < 0 else "breakeven", "close_type": raw.get("close_type"), "source_updated_at": last_update})
        else:
            if last_update < created_at:
                raise ValueError("update precedes entry")
            common.update({"last_update": last_update, "unrealized_net_return": _decimal(raw["net_return"]) if raw.get("net_return") is not None else None, "source_updated_at": last_update})
        common["source_checksum"] = _checksum(raw)
        return common

