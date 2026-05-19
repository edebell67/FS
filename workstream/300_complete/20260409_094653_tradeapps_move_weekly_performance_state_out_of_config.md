## Source

- User request: reimplement the weekly performance auto-select persistence so it no longer uses `config.json`

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary

Move weekly performance auto-select state out of `TradeApps\breakout\fs\config.json` into a dedicated weekly-performance state store and API, remove the current config write path from `weekly_performance.html`, and prevent those UI-only keys from being persisted through `/api/config`.

## Context

- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Current config file: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`

## Destination Folder

None

## Dependency

None

## Plan

- [x] 1. Inspect the current weekly-performance save/load path and define a dedicated state file/API shape.
  - [x] Test: Read the relevant `weekly_performance.html` and `trade_viewer_api.py` sections; pass if the current `/api/config` dependency and replacement contract are documented in this file.
  - [x] Evidence: Confirmed the previous load/save path used `/api/config` for `auto_select_modes` and `auto_select_permitted_types`, and defined a replacement `weekly_performance_state.json` plus `/api/weekly_performance_state` API.
- [x] 2. Implement a dedicated weekly-performance state backend and remove auto-select persistence from `/api/config`.
  - [x] Test: Code inspection must show new dedicated state helpers/endpoints and no `/api/config` normalization for `auto_select_modes` or `auto_select_permitted_types`.
  - [x] Evidence: `trade_viewer_api.py` now defines `WEEKLY_PERFORMANCE_STATE_FILE`, state load/save helpers, `/api/weekly_performance_state` GET/POST routes, and strips auto-select keys from `/api/config` via `incoming.pop(...)`.
- [x] 3. Update `weekly_performance.html` to load/save through the dedicated weekly state API instead of `config.json`.
  - [x] Test: Code inspection must show `fetch('/api/weekly_performance_state')` load/save usage and no remaining auto-select POSTs to `/api/config`.
  - [x] Evidence: `weekly_performance.html` now loads from `/api/weekly_performance_state` and posts auto-select updates only to that endpoint.
- [x] 4. Validate the implementation and archive the task.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` plus targeted `rg` checks must pass.
  - [x] Evidence: `py_compile` passed; `rg` confirmed the frontend uses `/api/weekly_performance_state` and the backend exposes the dedicated state endpoint plus config-key filtering.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`, `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance_state.json`
  - Objective-Proved: Backend and frontend changes are captured in the repo diff.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` and targeted `rg`/`Select-String` readback
  - Objective-Proved: Syntax and targeted verification commands pass after the change.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html` and `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance_state.json`
  - Objective-Proved: Weekly performance state is isolated from `config.json` by design.
  - Status: captured

## Implementation Log

- 2026-04-09 09:46:53 BST: Created lifecycle task and re-read the required lifecycle skill.
- 2026-04-09 09:55:00 BST: Confirmed `weekly_performance.html` was still loading from and posting to `/api/config` for `auto_select_modes` and `auto_select_permitted_types`.
- 2026-04-09 10:00:00 BST: Added `weekly_performance_state.json` support and dedicated `/api/weekly_performance_state` GET/POST routes in `trade_viewer_api.py`.
- 2026-04-09 10:05:00 BST: Updated `/api/config` to discard incoming `auto_select_modes` and `auto_select_permitted_types` so UI-only state cannot re-enter `config.json`.
- 2026-04-09 10:08:00 BST: Switched `weekly_performance.html` to load/save auto-select state via `/api/weekly_performance_state`.
- 2026-04-09 10:10:00 BST: Added `weekly_performance_state.json` with empty defaults and completed targeted validation.

## Changes Made

- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Added `WEEKLY_PERFORMANCE_STATE_FILE`.
  - Added `_normalize_weekly_performance_state`, `_load_weekly_performance_state`, and `_save_weekly_performance_state`.
  - Added `/api/weekly_performance_state` GET/POST endpoints.
  - Updated `/api/config` POST to discard `auto_select_modes` and `auto_select_permitted_types`.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Replaced auto-select state load/save calls from `/api/config` with `/api/weekly_performance_state`.
  - Kept `vtrade_persistence_seconds` as a read-only value supplied through the dedicated weekly state endpoint.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance_state.json`
  - Added dedicated persisted dashboard state with default empty `auto_select_modes` and `auto_select_permitted_types`.

## Validation

- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Result: Passed with no syntax errors.
- `Get-Content -Raw C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance_state.json | ConvertFrom-Json | Out-Null`
  - Result: Passed and printed `state_json_ok`.
- `rg -n "/api/config|/api/weekly_performance_state|auto_select_modes|auto_select_permitted_types|vtrade_persistence_seconds" C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Result: `weekly_performance.html` now references `/api/weekly_performance_state` for auto-select load/save, and `trade_viewer_api.py` shows the new endpoint plus the `/api/config` filter.
- `Select-String -Path C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py -Pattern 'weekly_performance_state|incoming.pop\("auto_select_modes"|incoming.pop\("auto_select_permitted_types"'`
  - Result: Confirmed dedicated state helpers/routes and the config-input filtering lines are present.
- `git -C C:\Users\edebe\eds\TradeApps commit -m "Move weekly performance state out of config"`
  - Result: Succeeded with commit `71d3317530`.
- `git -C C:\Users\edebe\eds\TradeApps push origin master`
  - Result: Succeeded, updating `master` from `eb1df5b797` to `71d3317530`.

## Risks/Notes

- This change should isolate weekly dashboard UI state from shared runtime config, but any other pages still posting UI-only keys to `/api/config` would need separate cleanup.

## Completion Status

- State: COMPLETE
- Timestamp: 2026-04-09 10:10:00 BST
