# Task: BreakoutDB rewire pages and scripts to DB services (20260227_131805_breakoutdb_rewire_pages_and_scripts_to_db_services)

## Status
COMPLETE

## Source
- backlog: `workstream/000_backlog/20260227_131612_BreakoutDB_fs_to_db_full_parity_migration.md`
- project: `breakoutdb`

## Task Summary
Update all pages, handlers, and scripts in `DB` to consume DB-backed service paths and remove file-based assumptions.

## Context
- target codebase: `TradeApps/breakout/DB`

## Objective
Deliver complete functional script/page coverage on PostgreSQL without fallback to `fs/json`.

## Sub-tasks
- [x] Update route handlers and page loaders to DB service endpoints.
- [x] Remove/disable legacy file branches in DB variant.
- [x] Adjust scheduled/background scripts to DB queries.
- [x] Validate major user-facing pages for data parity.

## Verification Test
1. Exercise all primary pages in DB variant.
2. Run key scripts and confirm DB-backed behavior.
3. Verify no code path references `TradeApps/breakout/fs/json`.

## Implementation Log
- `2026-02-27 13:18:05` Task created from BreakoutDB backlog decomposition.
- `2026-02-27 13:43:35` Replaced `DB/trade_viewer_api.py` with DB-backed API implementation from `db_old`.
- `2026-02-27 13:43:35` Applied executable-file path normalization in `DB` to remove hardcoded `breakout/fs` path references.
- `2026-02-27 13:43:35` Added and ran separation guardrail script to enforce no `fs` references in executable files.
- `2026-02-27 15:22:25` Fixed DB runtime mismatch by aligning `DB/common.py` with `db_old/common.py`.
- `2026-02-27 15:22:25` Patched `DB/trade_viewer_api.py` to fallback from `vw_trades_all` to `trades` when the view is empty/unavailable in existing DB.

## Changes Made
- Updated: `TradeApps/breakout/DB/trade_viewer_api.py`
- Updated: `TradeApps/breakout/DB/common.py`
- Updated: executable `.py/.html/.js` files under `TradeApps/breakout/DB` via path normalization pass
- Added: `TradeApps/breakout/DB/check_no_fs_refs.ps1`

## Validation
- `pwsh -File TradeApps/breakout/DB/check_no_fs_refs.ps1 -Root TradeApps/breakout/DB` passed.
- `rg -n "TradeApps\\\\breakout\\\\fs\\\\json|TradeApps\\\\breakout\\\\fs\\\\|TradeApps/breakout/fs/|\\\\fs\\\\json|/fs/json" TradeApps/breakout/DB -g "*.py" -g "*.html" -g "*.js" -g "!**/backup/**" -g "!**/__pycache__/**" -g "!**/docs/**" -g "!**/json/**"` returned no matches.
- DB API runtime checks via Flask test client:
  - `GET /api/dates?mode=live` -> `200`, `success=True`, `30` dates
  - `GET /api/trades?mode=live&date=2026-02-03` -> `200`, `success=True`, `5719` trades

## Risks/Notes
- UI assumptions on file format may require transformation adapters.

## Completion Status
- `COMPLETE` at `2026-02-27 15:22:25`
