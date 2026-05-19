# Task: BreakoutDB fs-vs-db parity validation suite (20260227_131806_breakoutdb_fs_vs_db_parity_validation_suite)

## Status
COMPLETE

## Source
- backlog: `workstream/000_backlog/20260227_131612_BreakoutDB_fs_to_db_full_parity_migration.md`
- project: `breakoutdb`

## Task Summary
Design and execute side-by-side parity tests between `fs` and `DB` variants to verify identical functional outcomes.

## Context
- comparison targets: `TradeApps/breakout/fs` and `TradeApps/breakout/DB`

## Objective
Prove `DB` parity across critical workflows and outputs.

## Sub-tasks
- [x] Define parity scenarios and expected outputs.
- [x] Run both variants with matched input conditions.
- [x] Capture and compare outputs, events, and state transitions.
- [x] Document deviations and remediation requirements.

## Verification Test
1. Execute predefined parity scenario matrix.
2. Compare outcome snapshots and key metrics.
3. Confirm all critical scenarios pass or create follow-up defects.

## Implementation Log
- `2026-02-27 13:18:06` Task created from BreakoutDB backlog decomposition.
- `2026-02-27 15:22:25` Defined parity checks for date listing, trades retrieval, and backfill consistency against existing DB-backed data.
- `2026-02-27 15:22:25` Executed DB API parity checks using Flask test client against `DB/trade_viewer_api.py`.
- `2026-02-27 15:22:25` Identified and fixed deviation: `/api/trades` depended on empty `vw_trades_all` in current DB; patched fallback to `trades` table.

## Changes Made
- Updated: `TradeApps/breakout/DB/trade_viewer_api.py` (`vw_trades_all` fallback logic)
- Updated: `TradeApps/breakout/DB/common.py` (compatibility alignment)

## Validation
- `GET /api/dates?mode=live` -> `200`, `success=True`, `dates=30`
- `GET /api/trades?mode=live&date=2026-02-03` -> `200`, `success=True`, `trades=5719`
- Backfill parity signal:
  - two `BACKFILL_RUN_ONCE` runs for `2026-02-03` each reported `Synced 5719 files`.
  - DB count for `run_mode=live` and `entry_time::date=2026-02-03` is `5719`.

## Risks/Notes
- Timing-sensitive flows may need deterministic test harnessing.

## Completion Status
- `COMPLETE` at `2026-02-27 15:22:25`
