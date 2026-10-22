# Version history:
# 2026-08-23 v1.0.0 Codex - Atomic promotion, rollback, and monotonicity tests.

from __future__ import annotations

from copy import deepcopy
import pytest

from app.repository import MemoryRepository
from app.contracts import snapshot_hash
from sync.export_snapshot import build_snapshot


def test_promote_atomically_changes_current_and_retains_previous(
    strategy_items, snapshot_kwargs
):
    repository = MemoryRepository()
    first = build_snapshot(strategy_items, **snapshot_kwargs)
    repository.promote(first)

    later_kwargs = {"source_watermark": "2026-01-01T00:00:00Z"}
    changed_items = deepcopy(strategy_items)
    changed_items[0]["total_net_return"] = 21.5
    second = build_snapshot(changed_items, **later_kwargs)
    repository.promote(second)

    assert repository.current_snapshot().snapshot_id == second.snapshot_id
    assert first.snapshot_id in repository.snapshots
    assert second.snapshot_id in repository.snapshots

    repository.rollback(first.snapshot_id)
    assert repository.current_snapshot().snapshot_id == first.snapshot_id


def test_failed_promotion_leaves_current_pointer_unchanged(
    strategy_items, snapshot_kwargs
):
    repository = MemoryRepository()
    valid = build_snapshot(strategy_items, **snapshot_kwargs)
    repository.promote(valid)
    invalid = valid.model_copy(deep=True)
    invalid.items[0].total_net_return = 999

    with pytest.raises(Exception):
        repository.promote(invalid)
    assert repository.current_snapshot().snapshot_id == valid.snapshot_id


def test_unknown_rollback_does_not_change_current(strategy_items, snapshot_kwargs):
    repository = MemoryRepository()
    current = build_snapshot(strategy_items, **snapshot_kwargs)
    repository.promote(current)
    with pytest.raises(KeyError):
        repository.rollback("missing")
    assert repository.current_snapshot().snapshot_id == current.snapshot_id


def test_snapshot_id_is_immutable(strategy_items,snapshot_kwargs):
    repository=MemoryRepository();first=build_snapshot(strategy_items,**snapshot_kwargs);repository.promote(first)
    changed=first.model_copy(deep=True);changed.items[0].total_net_return+=1;changed.sha256=snapshot_hash(changed.items)
    with pytest.raises(ValueError,match="different evidence"):repository.promote(changed)
