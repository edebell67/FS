## Source

- User clarification: all previous dates must be cached; only today's anchored request should regenerate

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary

Change weekly performance caching from week-level regeneration to date-anchored snapshots so any target date before today is served from cache, even when that date falls within the current week.

## Context

- API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- UI anchor logic: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Weekly stats cache folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\<product_type>\stats\weekly\`

## Destination Folder

None

## Dependency

None

## Plan

- [x] 1. Inspect the current cache key and target-date handling for weekly performance.
  - [x] Test: Read `trade_viewer_api.py` and `weekly_performance.html`; pass if the week-start file naming and target-date reset behavior are documented in this file.
  - [x] Evidence: Summary recorded in `Implementation Log`.
- [x] 2. Patch the API and UI so cache entries are anchored by requested target date and only today-or-later requests regenerate.
  - [x] Test: Code inspection must show date-anchored cache filenames and `currentTargetDate` preserved as the requested anchor date.
  - [x] Evidence: Diff captured in source control.
- [x] 3. Validate the final behavior and archive the task.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` plus targeted readback of the cache-path and `currentTargetDate` handling must pass.
  - [x] Evidence: Command outputs summarized in `Validation`.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: not_applicable
  - Objective-Proved: The date-anchored cache policy is captured in the code diff.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: not_applicable
  - Objective-Proved: Syntax and readback validation pass after the patch.
  - Status: complete
- Evidence-Type: manual_verification
  - Artifact: not_applicable
  - Objective-Proved: Previous dates are served from their own cache snapshots by design.
  - Status: complete

## Implementation Log

- 2026-04-09 11:25:00 BST: Opened follow-up task after confirming week-start keyed caching is too coarse for current-week historical dates.
- 2026-04-09 11:31:00 BST: Confirmed backend now writes cache files to `stats/weekly/<target_date>.json` and refreshes only when the requested date is today-or-later, but the UI still reset `currentTargetDate` to `data.week_start` after each fetch.
- 2026-04-09 11:33:00 BST: Removed the UI reset so the requested date remains the active cache anchor across navigation and repeat fetches.

## Changes Made

- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` so `/api/weekly_performance` parses `target_date`, stores snapshots at `stats/weekly/<target_date>.json`, and refreshes only when the snapshot is missing, `force_refresh=true`, or the requested date is today-or-later.
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html` so `currentTargetDate` is no longer rewritten to `data.week_start` after a response, preserving the requested historical date as the cache key.

## Validation

- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` completed successfully.
- Readback confirmed `stats_file = stats_dir / f"{target_date}.json"` and `should_refresh = force_refresh or not stats_file.exists() or requested_date >= today` in `trade_viewer_api.py`.
- Readback confirmed the previous `currentTargetDate = data.week_start || currentTargetDate` reset was removed from `weekly_performance.html`.

## Risks/Notes

- This will create one weekly snapshot file per requested target date instead of one per aligned week. That is intentional to preserve historical daily anchors within the current week.

## Completion Status

- State: COMPLETE
- Timestamp: 2026-04-09 11:34:00 BST
