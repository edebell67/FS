# Version history:
# 2026-08-23 v1.0.0 Codex - Determinism and validation tests for aggregate snapshots.

from __future__ import annotations

from copy import deepcopy

import pytest

from pydantic import ValidationError

from app.contracts import Snapshot,Strategy, snapshot_hash
from sync.export_snapshot import build_snapshot


def test_snapshot_hash_and_payload_are_deterministic(strategy_items, snapshot_kwargs):
    first = build_snapshot(strategy_items, **snapshot_kwargs)
    second = build_snapshot(list(reversed(deepcopy(strategy_items))), **snapshot_kwargs)

    assert first.sha256 == second.sha256
    assert first.snapshot_id == second.snapshot_id
    assert first.item_count == 2
    assert [row.strategy_id for row in first.items] == [
        "DNA_102001",
        "DNA_102002",
    ]
    first.verified()


@pytest.mark.parametrize("invalid_id", ["DNA_102001_B", "DNA_102001_S", "NON_DNA_1", ""])
def test_validation_rejects_noncanonical_strategy_ids(
    strategy_items, snapshot_kwargs, invalid_id
):
    items = deepcopy(strategy_items)
    items[0]["strategy_id"] = invalid_id
    with pytest.raises(ValidationError):
        build_snapshot(items, **snapshot_kwargs)


def test_validation_rejects_tampering_and_count_mismatch(strategy_items, snapshot_kwargs):
    payload = build_snapshot(strategy_items, **snapshot_kwargs)
    tampered = payload.model_copy(deep=True)
    tampered.items[0].total_net_return = 999
    with pytest.raises(ValueError):
        tampered.verified()

    wrong_count = payload.model_copy(update={"item_count": payload.item_count + 1})
    with pytest.raises(ValueError):
        wrong_count.verified()


def test_hash_ignores_input_order(strategy_items):
    assert snapshot_hash(strategy_items) == snapshot_hash(list(reversed(strategy_items)))


def test_snapshot_rejects_nonfinite_evidence(strategy_items):
    items=deepcopy(strategy_items);items[0]["total_net_return"]=float("nan")
    with pytest.raises(ValidationError):Strategy.model_validate(items[0])
