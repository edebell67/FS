## Source

- User request: restrict weekly performance to top 200 strategies only

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary

Limit weekly performance results to the top 200 strategies while preserving existing ranking behavior.

## Context

- API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Aggregation logic may live under `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\`
- UI consumer: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`

## Destination Folder

None

## Dependency

None

## Plan

- [x] 1. Locate the weekly ranking/output path and identify the narrowest safe top-200 cutoff point.
  - [x] Test: Code inspection identifies where the weekly strategy list is sorted and returned.
  - [x] Evidence: Findings recorded in `Implementation Log`.
- [x] 2. Implement a top-200 cap in the weekly results path.
  - [x] Test: Code inspection shows the weekly payload is truncated to 200 ranked strategies.
  - [x] Evidence: Diff captured in source control.
- [x] 3. Validate the change and archive the task.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py` plus targeted readback must pass.
  - [x] Evidence: Validation summary recorded below.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: not_applicable
  - Objective-Proved: Weekly results are capped to 200 strategies in code.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: not_applicable
  - Objective-Proved: Syntax and readback validation pass.
  - Status: complete

## Implementation Log

- 2026-04-09 12:24:18 +01:00: Opened task to restrict weekly performance output to the top 200 ranked strategies only.
- 2026-04-09 12:26:00 +01:00: Located the weekly cutoff in `tools/aggregate_top_strategies.py`, where the already-sorted `final_list` is written to `top_strategies` in the cached weekly JSON.
- 2026-04-09 12:27:00 +01:00: Replaced the existing `[:1000]` write limit with a dedicated `WEEKLY_TOP_STRATEGY_LIMIT = 200` constant so the cap is explicit and applied after current ranking logic.

## Changes Made

- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py` to cap `top_strategies` at 200 items via `WEEKLY_TOP_STRATEGY_LIMIT`.

## Validation

- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py` completed successfully.
- Readback confirmed `WEEKLY_TOP_STRATEGY_LIMIT = 200` and `top_strategies: final_list[:WEEKLY_TOP_STRATEGY_LIMIT]`.

## Risks/Notes

- Cap should be applied after existing ranking logic so the current ordering semantics remain intact.

## Completion Status

- State: COMPLETE
- Timestamp: 2026-04-09 12:27:00 +01:00
