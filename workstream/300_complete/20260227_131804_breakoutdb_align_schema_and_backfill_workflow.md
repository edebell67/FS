# Task: BreakoutDB align schema and backfill workflow (20260227_131804_breakoutdb_align_schema_and_backfill_workflow)

## Status
COMPLETE

## Source
- backlog: `workstream/000_backlog/20260227_131612_BreakoutDB_fs_to_db_full_parity_migration.md`
- project: `breakoutdb`

## Task Summary
Use `DB/backfill_trades.py` to define and validate required PostgreSQL schema/backfill behavior for DB runtime parity.

## Context
- target script: `TradeApps/breakout/DB/backfill_trades.py`
- database: PostgreSQL

## Objective
Ensure schema/table/index readiness and deterministic seed/backfill path for DB variant.

## Sub-tasks
- [x] Document required tables, keys, indexes, and constraints.
- [x] Update `backfill_trades.py` to match active DB model.
- [x] Execute backfill on test dataset.
- [x] Validate data integrity and idempotency expectations.

## Verification Test
1. Run backfill script against target PostgreSQL DB.
2. Validate row counts and key constraints.
3. Re-run backfill and verify expected idempotent behavior.

## Implementation Log
- `2026-02-27 13:18:04` Task created from BreakoutDB backlog decomposition.
- `2026-02-27 13:43:35` Updated `DB/backfill_trades.py` to load `.env` from DB root and default JSON base to `DB/json`.
- `2026-02-27 13:43:35` Added DB runbook and environment template to support deterministic backfill startup.
- `2026-02-27 15:22:25` Added `DB/.env` using existing PostgreSQL credentials and verified connectivity to `tradedb2`.
- `2026-02-27 15:22:25` Added `BACKFILL_RUN_ONCE` support in `DB/backfill_trades.py` and executed two one-pass backfill runs for `BACKFILL_DATES=2026-02-03`.

## Changes Made
- Updated: `TradeApps/breakout/DB/backfill_trades.py`
- Added: `TradeApps/breakout/DB/.env.example`
- Added: `TradeApps/breakout/DB/README_DB.md`
- Added: `TradeApps/breakout/DB/.env`

## Validation
- `python -m py_compile TradeApps/breakout/DB/backfill_trades.py` passed.
- `BACKFILL_RUN_ONCE=1 BACKFILL_DATES=2026-02-03 python TradeApps/breakout/DB/backfill_trades.py` run #1 passed (`Synced 5719 files`).
- Same command run #2 passed (`Synced 5719 files`).
- Row counts:
  - before: `trades=334659`, `daily_summary=69`
  - after: `trades=340378`, `daily_summary=69`
  - verification: `trades where run_mode='live' and entry_time::date='2026-02-03' = 5719`

## Risks/Notes
- Schema drift between environments can invalidate parity tests.

## Completion Status
- `COMPLETE` at `2026-02-27 15:22:25`
