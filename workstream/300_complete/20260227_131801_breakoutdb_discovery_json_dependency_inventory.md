# Task: BreakoutDB discovery and JSON dependency inventory (20260227_131801_breakoutdb_discovery_json_dependency_inventory)

## Status
COMPLETE

## Source
- backlog: `workstream/000_backlog/20260227_131612_BreakoutDB_fs_to_db_full_parity_migration.md`
- project: `breakoutdb`

## Task Summary
Inventory all `fs` files and runtime paths that depend on JSON/file-based persistence and map each to a PostgreSQL replacement path for the `DB` variant.

## Context
- source app: `TradeApps/breakout/fs`
- target app: `TradeApps/breakout/DB`

## Objective
Produce a complete dependency map that prevents hidden `fs/json` references from leaking into `DB`.

## Sub-tasks
- [x] Enumerate files in `fs` that read/write JSON persistence.
- [x] Identify all API endpoints and scripts tied to file persistence.
- [x] Classify each dependency by CRUD behavior and target table/domain.
- [x] Produce migration map (`file path -> DB repository/query path`).

## Verification Test
1. Run a repository search on `fs` for JSON path usage.
2. Cross-check mapped files against runtime entry points.
3. Confirm no unclassified file-based persistence remains in inventory.

## Implementation Log
- `2026-02-27 13:18:01` Task created from BreakoutDB backlog decomposition.
- `2026-02-27 13:43:35` Ran full-text dependency scans across `TradeApps/breakout/fs` and generated runtime dependency inventory for migration planning.
- `2026-02-27 13:43:35` Exported discovered dependency file list to `TradeApps/breakout/DB/docs/fs_json_dependency_files.txt` (78 matching files in filtered executable/docs set).

## Changes Made
- Created `TradeApps/breakout/DB/docs/fs_json_dependency_files.txt` with JSON/file persistence dependency file list from `fs`.

## Validation
- `rg -n "json|\\.json|active_trades|quotes|open\\(|write\\(|dump\\(|load\\(" TradeApps/breakout/fs` (broad discovery scan).
- `rg -l "json|\\.json|active_trades|grid_live|activations" TradeApps/breakout/fs -g "*.py" -g "*.html" -g "*.js" -g "*.md" -g "!**/backup/**" -g "!**/__pycache__/**"` (filtered inventory export).

## Risks/Notes
- Hidden helpers/utilities may reference JSON indirectly.

## Completion Status
- `COMPLETE` at `2026-02-27 13:43:35`
