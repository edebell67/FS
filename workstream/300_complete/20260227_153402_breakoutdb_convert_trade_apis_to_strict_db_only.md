# Task: BreakoutDB convert trade APIs to strict DB-only mode (20260227_153402_breakoutdb_convert_trade_apis_to_strict_db_only)

## Status
COMPLETE

## Source
- backlog: `workstream/000_backlog/20260227_153313_BreakoutDB_db_only_no_json_references.md`
- project: `breakoutdb`

## Description
Refactor DB runtime API endpoints so no route uses local JSON files as runtime data source.

## Objective
Ensure all trade/summary/activation/bucket endpoints resolve from PostgreSQL-backed services only.

## Sub-tasks
- [x] Audit runtime routes in `trade_viewer_api.py` and related APIs.
- [x] Replace remaining file-based path access with DB queries/services.
- [x] Preserve response schema contracts used by frontend pages.
- [x] Add endpoint-level fallback strategy that remains DB-only.

## Verification Test
1. API smoke: `/api/dates`, `/api/trades`, `/api/summary_net`, `/api/top_one`, `/api/activations`, `/api/trade_buckets`.
2. Confirm no runtime file reads from `DB/json`.
3. Validate error handling for missing DB rows without file fallback.

## Implementation Log
- `2026-02-27 15:39:01` Converted `/api/virtual_trades` from filesystem JSON scanning to PostgreSQL `virtual_trades` query.
- `2026-02-27 15:39:01` Added activation schema-compatibility logic for existing DB (`activations` table without `run_mode`/`activated_at`).
- `2026-02-27 15:39:01` Preserved `/api/trades` DB-only fallback behavior (`vw_trades_all` -> `trades`).

## Changes Made
- Updated `TradeApps/breakout/DB/trade_viewer_api.py`
  - DB-only virtual trades endpoint
  - portable activation load/save logic across schema variants
  - DB fallback query path retained for trade fetch

## Validation
- `python -m py_compile TradeApps/breakout/DB/trade_viewer_api.py` passed.
- API smoke via Flask test client:
  - `GET /api/activations?mode=live` -> `200`, `success=True`
  - `POST /api/activations/toggle` -> `200`, `success=True`
  - `GET /api/trades?mode=live&date=2026-02-03` -> `200`, `success=True`
  - `GET /api/virtual_trades?mode=live&date=2026-02-03&limit=20` -> `200`, `success=True`
  - `GET /api/dates?mode=live` -> `200`, `success=True`
  - `GET /api/trade_buckets?mode=live&date=2026-02-03` -> `200`, `success=True`

## Completion Status
COMPLETE
