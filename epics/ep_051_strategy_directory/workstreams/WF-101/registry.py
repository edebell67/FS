# workstreams/WF-101/registry.py — Deterministic identity and definition utilities for the DNA registry.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: enforces normalized IDs, canonical definition hashing, and collision checks.

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Iterable

DNA_ID = re.compile(r"^DNA_[0-9]+$")


def normalize_strategy_id(source_model: str) -> str:
    normalized = source_model.strip().upper()
    if normalized.endswith(("_S", "_B")):
        normalized = normalized[:-2]
    if not DNA_ID.fullmatch(normalized):
        raise ValueError(f"invalid DNA model identifier: {source_model!r}")
    return normalized


def canonical_definition_json(definition: dict[str, Any]) -> str:
    return json.dumps(definition, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def definition_hash(definition: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_definition_json(definition).encode("utf-8")).hexdigest()


def validate_seed_records(records: Iterable[dict[str, Any]]) -> None:
    ids: dict[str, str] = {}
    hashes: dict[str, str] = {}
    aliases: dict[str, str] = {}
    count = 0
    for record in records:
        count += 1
        strategy_id = normalize_strategy_id(record["strategy_id"])
        expected_hash = definition_hash(record["definition"])
        if expected_hash != record["definition_hash"]:
            raise ValueError(f"definition hash mismatch for {strategy_id}")
        if strategy_id in ids:
            raise ValueError(f"duplicate canonical strategy ID: {strategy_id}")
        if expected_hash in hashes:
            raise ValueError(f"definition reused by {strategy_id} and {hashes[expected_hash]}")
        ids[strategy_id] = expected_hash
        hashes[expected_hash] = strategy_id
        for alias in record["source_aliases"]:
            if normalize_strategy_id(alias) != strategy_id:
                raise ValueError(f"alias {alias} does not normalize to {strategy_id}")
            if alias in aliases:
                raise ValueError(f"duplicate source alias: {alias}")
            aliases[alias] = strategy_id
    if not 300 <= count <= 500:
        raise ValueError(f"seed population must contain 300–500 strategies, found {count}")

