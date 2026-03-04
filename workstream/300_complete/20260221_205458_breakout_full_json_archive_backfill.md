# Task Documentation: Breakout Full JSON Archive Backfill

## Metadata
- Timestamp: 2026-02-21 20:54:58
- Project: breakout
- Unique Task: full_json_archive_backfill
- Primary File Updated: `TradeApps/breakout/fs/backfill_trades.py`
- Requested Outcome: Capture all relevant JSON files in database with explicit exclusions and keep existing structured ingestion.

## Lifecycle Log
- Created in `workstream/100_todo`.
- Moved to `workstream/200_inprogress` while implementation was in progress.
- Moved to `workstream/300_complete` after implementation + syntax validation completed.

## Problem Statement
Existing backfill logic only persisted selected JSON data into domain tables (`trades`, `daily_summary`, `grid_snapshots`).
This left operational files uncaptured from:
- `fs/*.json` (except `grid_live.json`)
- `fs/json/live/*.json`, `fs/json/sim/*.json` (e.g. `_targeted_strategies.json`)
- `fs/json/strategy_profile/*.json`

## Solution Implemented
Implemented a full-fidelity archive lane in `backfill_trades.py` that runs alongside existing ingestion:

1. Added archive table bootstrap
- Function: `ensure_archive_table(cursor)`
- Creates `fs_json_archive` with:
  - `file_path`, `file_name`, `file_group`, `run_mode`, `file_date`
  - `content_hash` (SHA-256)
  - `json_data` (JSONB)
  - `ingest_status`, `error`, `captured_at`
- Adds uniqueness guard: `UNIQUE (file_path, content_hash)`
- Adds helper index: `(file_group, file_date)`

2. Added discovery functions
- `discover_structured_files()`:
  - Daily date-folders only (`live/sim/YYYY-MM-DD`) for existing structured processing.
- `discover_archive_files()`:
  - `fs/*.json`
  - `fs/json/*.json`
  - `fs/json/live/*.json`
  - `fs/json/sim/*.json`
  - `fs/json/strategy_profile/**/*.json`
  - Daily date folders `live/sim/YYYY-MM-DD/**/*.json`

3. Added classification and metadata extraction
- `classify_file(file_path)` sets:
  - `file_group` in `{fs_root, json_root, mode_root, strategy_profile, daily, other}`
  - `run_mode` (`live`/`sim` where applicable)
  - `file_date` when a `YYYY-MM-DD` path segment exists.

4. Added archive write path
- `archive_json_file(cursor, file_path)`:
  - Excludes files by configurable list.
  - Reads file and computes SHA-256 hash.
  - Parses JSON when possible.
  - Writes row to `fs_json_archive`.
  - Uses `ON CONFLICT (file_path, content_hash) DO NOTHING` for idempotency.
  - Records failed parse/read attempts as `ingest_status='failed'`.

5. Added configurable exclusion control
- `ARCHIVE_EXCLUDE_FILES` from env var, defaulting to:
  - `config copy.json`

6. Integrated with `main()` loop
- Archive scan runs every loop before structured upserts.
- Existing structured ingestion remains active:
  - `process_trade_file`
  - `process_summary_file`
  - `process_grid_history`
  - `process_grid_latest`
- Added per-loop archive metrics log:
  - scanned, inserted, unchanged, excluded, failed, structured_skipped.

## Validation
- Command run:
  - `python -m py_compile TradeApps/breakout/fs/backfill_trades.py`
- Result:
  - Passed (no syntax errors).

## Operational Notes
- `_targeted_strategies.json` is now archived by default (mode-root discovery).
- `config copy.json` is excluded by default but can be overridden with `ARCHIVE_EXCLUDE_FILES`.
- Structured analytics tables still operate exactly as before; archive adds recovery/completeness coverage.

## Suggested Follow-ups
1. Add a reconciliation SQL/report for filesystem-vs-archive completeness by group/date.
2. Add optional max-file-size guardrail if archive volume grows significantly.
3. Optionally add `--once` loop mode for controlled runs.

## Additional Deliverable: Reusable Skill
Created reusable skill:
- Path: `skills/workstream-task-lifecycle/SKILL.md`
- Purpose: enforce creation and movement of task docs across `100_todo -> 200_inprogress -> 300_complete`.
- Added metadata file: `skills/workstream-task-lifecycle/agents/openai.yaml`
- Validation command: `quick_validate.py skills/workstream-task-lifecycle`
- Validation result: `Skill is valid!`
