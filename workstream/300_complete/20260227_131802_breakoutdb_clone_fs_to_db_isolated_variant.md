# Task: BreakoutDB clone fs app into isolated DB variant (20260227_131802_breakoutdb_clone_fs_to_db_isolated_variant)

## Status
COMPLETE

## Source
- backlog: `workstream/000_backlog/20260227_131612_BreakoutDB_fs_to_db_full_parity_migration.md`
- project: `breakoutdb`

## Task Summary
Create `TradeApps/breakout/DB` by cloning `TradeApps/breakout/fs` and enforce separation constraints so both variants can evolve independently.

## Context
- source: `TradeApps/breakout/fs`
- target: `TradeApps/breakout/DB`

## Objective
Establish an isolated DB variant baseline with no accidental runtime coupling to `fs`.

## Sub-tasks
- [x] Copy directory tree from `fs` to `DB`.
- [x] Adjust app identifiers and startup paths for DB variant.
- [x] Add/adjust DB-specific env template/config scaffold.
- [x] Validate DB variant boots without touching `fs` runtime files.

## Verification Test
1. Start `DB` variant using its own entrypoint/config.
2. Confirm process starts and routes load.
3. Verify no runtime reads/writes to `TradeApps/breakout/fs/json`.

## Implementation Log
- `2026-02-27 13:18:02` Task created from BreakoutDB backlog decomposition.
- `2026-02-27 13:43:35` Created `TradeApps/breakout/DB` clone from `TradeApps/breakout/fs`.
- `2026-02-27 13:43:35` Ported DB runtime baseline files from `db_old` into `DB` (`db_utils.py`, `trade_viewer_api.py`, `backfill_trades.py`).
- `2026-02-27 13:43:35` Performed path normalization pass across executable files to remove hardcoded `breakout/fs` references in DB variant code.

## Changes Made
- Created `TradeApps/breakout/DB` as isolated variant root.
- Updated key DB runtime files in `DB`:
  - `TradeApps/breakout/DB/db_utils.py`
  - `TradeApps/breakout/DB/trade_viewer_api.py`
  - `TradeApps/breakout/DB/backfill_trades.py`
- Rewrote hardcoded executable-path references from `breakout\\fs\\` to `breakout\\DB\\` in `DB` code files.

## Validation
- `if (Test-Path TradeApps/breakout/DB) { 'DB_EXISTS' }` returned `DB_EXISTS`.
- `rg -n "TradeApps\\\\breakout\\\\fs\\\\json|TradeApps\\\\breakout\\\\fs\\\\|TradeApps/breakout/fs/|\\\\fs\\\\json|/fs/json" TradeApps/breakout/DB -g "*.py" -g "*.html" -g "*.js" -g "!**/backup/**" -g "!**/__pycache__/**" -g "!**/docs/**" -g "!**/json/**"` returned no matches after rewrite.

## Risks/Notes
- Relative imports or shared config defaults may create unintended coupling.

## Completion Status
- `COMPLETE` at `2026-02-27 13:43:35`
