## Source

- User request: stop regenerating non-changing historical weekly data and implement proper historical caching

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary

Update the weekly performance API so historical weeks are served from the persisted weekly stats cache instead of being regenerated on every request, while still allowing the current week to refresh because it can change.

## Context

- API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Weekly stats cache path: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\<product_type>\stats\weekly\`

## Destination Folder

None

## Dependency

None

## Plan

- [x] 1. Inspect the current weekly cache policy and define the correct historical/current-week refresh rule.
  - [x] Test: Read the `/api/weekly_performance` implementation; pass if the unconditional regeneration behavior and the replacement rule are documented in this file.
  - [x] Evidence: Confirmed the prior implementation hardcoded `is_recent = True`; replacement rule is now "refresh only when the week contains today, the cache file is missing, or `force_refresh` is explicitly requested."
- [x] 2. Patch the API so historical weeks use cached files and only current/incomplete weeks regenerate.
  - [x] Test: Code inspection must show the current refresh condition is based on the aligned week relative to today rather than a hardcoded `True`.
  - [x] Evidence: `get_weekly_performance()` now computes `week_contains_today` and `should_refresh`.
- [x] 3. Validate the new cache policy and archive the task.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` plus targeted readback of `get_weekly_performance()` must pass.
  - [x] Evidence: `py_compile` passed and readback confirmed `force_refresh`, `week_contains_today`, and `should_refresh`.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Objective-Proved: The cache-policy change is captured in the code diff.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` and targeted readback of `get_weekly_performance()`
  - Objective-Proved: Syntax and readback verification pass after the patch.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py:7208`
  - Objective-Proved: Historical weeks are served from cache by design.
  - Status: captured

## Implementation Log

- 2026-04-09 11:15:37 BST: Confirmed `/api/weekly_performance` currently sets `is_recent = True`, which forces regeneration for every week on every request.

## Changes Made

- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Added optional `force_refresh` query handling for `/api/weekly_performance`.
  - Replaced unconditional regeneration with:
    - refresh when the cache file is missing
    - refresh when the aligned week contains today
    - refresh only when `force_refresh` is explicitly requested
  - Historical weeks now read the persisted weekly stats file directly.

## Validation

- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Result: Passed with no syntax errors.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py | Select-Object -Skip 7204 -First 40`
  - Result: Confirmed `force_refresh`, `week_contains_today`, and `should_refresh` are present in `get_weekly_performance()`.

## Risks/Notes

- This change assumes historical weekly aggregates are immutable once the week has fully ended. If you sometimes backfill or repair historical data, a separate explicit refresh path may still be needed.

## Completion Status

- State: COMPLETE
- Timestamp: 2026-04-09 11:22:00 BST
