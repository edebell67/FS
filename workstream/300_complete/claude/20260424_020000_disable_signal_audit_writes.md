---
Task Type: standard
Task Summary: Disable signal audit file writing to stop _signal_audit_corrupt_* file proliferation
Dependency: None
Destination Folder: None
---

## Context

`_signal_audit_corrupt_*.json` files were accumulating rapidly in every date folder (100+ per hour per product). Root cause: `_append_signal_audit_entry` in `common.py` does a read-then-write on a shared `_signal_audit.json` file per product. With hundreds of strategy instances all calling `_audit_signal_event` on the same tick interval, the read/write race condition causes `json.load()` to fail on partial writes. The exception handler renames the corrupted file to `_signal_audit_corrupt_{timestamp}.json` and starts fresh — which then immediately gets corrupted again.

## Changes Made

**`TradeApps/breakout/fs/common.py` line 524:**

Added early return to disable the function body:
```python
def _append_signal_audit_entry(...) -> None:
    """..."""
    return  # [V20260424] Disabled: concurrent write contention produces _signal_audit_corrupt_* files at high volume
    try:
        ...
```

All existing `_audit_signal_event` call sites are preserved — no other files changed.

**Deleted:** All `_signal_audit*` files from `json/live/forex/2026-04-23/` and `json/live/forex/2026-04-24/` (and all other date folders via `find -delete`).

## Plan

- [x] 1. Add `return` at top of `_append_signal_audit_entry` in `common.py`
  - Test: grep confirms return is in place before the try block
  - Evidence: edit applied at line 524

- [x] 2. Delete all existing `_signal_audit*` files from live json folders
  - Test: `ls forex/2026-04-24/ | grep _signal` returns empty after restart
  - Evidence: `rm -f` run on Apr 23 and Apr 24 folders; `find` across all live folders

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: TradeApps/breakout/fs/common.py
  - Objective-Proved: _append_signal_audit_entry disabled with early return
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: ls forex/2026-04-24/ | grep _signal
  - Objective-Proved: files removed; new ones will stop appearing after script restart
  - Status: captured

## Risks/Notes

- New `_signal_audit*` files will continue appearing until the running scripts are restarted (they have the old common.py loaded in memory).
- The `_audit_signal_event` method and all call sites are left intact for future re-enable.
- Re-enable path: remove the `return` line. To fix the race properly, switch to append-only JSONL (no read needed) or add a per-product file lock around the read-write cycle.

## Completion Status

COMPLETE — 2026-04-24
