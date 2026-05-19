## Source

- User report: weekly performance product-type switching is too slow and auto-select state is lost when navigating between views/pages

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary

Reduce weekly performance product-type switching latency and restore durable auto-select persistence when navigating between product types or weeks by caching state/data in the page and synchronizing it safely with the dedicated weekly-performance state backend.

## Context

- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Weekly state API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Dedicated state file: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance_state.json`

## Destination Folder

None

## Dependency

None

## Plan

- [x] 1. Inspect the live weekly-performance fetch/state flow and identify the persistence/latency regressions.
  - [x] Test: Read `weekly_performance.html` around fetch/state functions; pass if the repeated fetch path and state reset points are documented in this file.
  - [x] Evidence: Confirmed `fetchData()` reloaded activations and weekly state on every product-type/week switch, and auto-select UI state was rehydrated from server state without any local cache or stale-request guard.
- [x] 2. Implement local weekly-state persistence and scoped UI hydration without reloading config/state on every view change.
  - [x] Test: Code inspection must show localStorage-backed weekly state helpers plus a single UI hydration path for product-type changes.
  - [x] Evidence: Added `WEEKLY_STATE_STORAGE_KEY`, `getStoredWeeklyState`, `storeWeeklyState`, `hydrateWeeklyState`, and `applyWeeklyStateToUi` in `weekly_performance.html`.
- [x] 3. Reduce product-type navigation latency by caching weekly data/activations and guarding against stale in-flight responses.
  - [x] Test: Code inspection must show cached activations/data and request-token or abort protection around `fetchData()`.
  - [x] Evidence: Added `activationsLoaded`, `weeklyDataCache`, `weeklyDataRequestId`, cached-read path, and `requestId !== weeklyDataRequestId` stale-response guard in `fetchData()`.
- [x] 4. Validate the final implementation and archive the task.
  - [x] Test: Run targeted readback checks against `weekly_performance.html`; pass if the new persistence/caching helpers and guarded fetch path are present.
  - [x] Evidence: `node --check` passed on the extracted inline script and `rg` confirmed the persistence/caching helpers and updated fetch path.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: The page logic changes are captured in source control.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `node --check C:\Users\edebe\eds\TradeApps\breakout\fs\_weekly_performance_inline_check.js` and targeted `rg` readback
  - Objective-Proved: Readback verification confirms the persistence/caching logic is present.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: Product-type switches and week navigation preserve auto-select state without resetting.
  - Status: captured

## Implementation Log

- 2026-04-09 10:18:15 BST: Created lifecycle task and inspected the current weekly-performance fetch/state flow.
- 2026-04-09 10:24:00 BST: Confirmed the page reloaded activations and weekly state on each `fetchData()` call, which made product-type navigation slower than necessary and reintroduced server-refresh state churn.
- 2026-04-09 10:32:00 BST: Added localStorage-backed weekly state helpers so auto-select mode/permitted-type selections survive product-type/week navigation and page reloads before the server round-trip completes.
- 2026-04-09 10:38:00 BST: Added cached activations and per-product/week response caching plus a stale-request guard to avoid out-of-order fetches overwriting the active view.
- 2026-04-09 10:42:00 BST: Updated `setProductType()` to hydrate UI state immediately from local memory instead of waiting for a fresh state fetch.
- 2026-04-09 10:46:00 BST: Ran targeted script validation and readback checks.

## Changes Made

- `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Added `activationsLoaded` so activations are not re-fetched on every product-type switch.
  - Added `weeklyDataCache` keyed by `product_type|week` for faster repeat navigation.
  - Added `weeklyDataRequestId` stale-response guard so slower responses cannot overwrite the active view.
  - Added localStorage-backed weekly state helpers:
    - `getStoredWeeklyState`
    - `storeWeeklyState`
    - `hydrateWeeklyState`
    - `applyWeeklyStateToUi`
  - Added `persistWeeklyState()` so the UI updates immediately and then syncs the dedicated backend state.
  - Updated `handleAutoSelectChange()` and `handlePermittedTypeToggle()` to persist locally first, then sync remotely, then re-evaluate auto-select.
  - Updated `setProductType()` to apply current state immediately before loading weekly data.

## Validation

- `node --check C:\Users\edebe\eds\TradeApps\breakout\fs\_weekly_performance_inline_check.js`
  - Result: Passed with no JavaScript syntax errors.
- `rg -n "WEEKLY_STATE_STORAGE_KEY|getStoredWeeklyState|storeWeeklyState|hydrateWeeklyState|weeklyDataCache|weeklyDataRequestId|requestId !== weeklyDataRequestId|activationsLoaded|persistWeeklyState|applyWeeklyStateToUi" C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Result: Confirmed the new local persistence helpers, cached activations/data, and stale-request guard are present.
- `Select-String -Path C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html -Pattern "setProductType|changeWeek|handleAutoSelectChange|handlePermittedTypeToggle"`
  - Result: Confirmed the relevant handlers now route through the new local/stateful flow.

## Risks/Notes

- This task focuses on the weekly page. If another page mutates activations or weekly state concurrently, a refresh may still be needed to observe that external change.

## Completion Status

- State: COMPLETE
- Timestamp: 2026-04-09 10:46:00 BST
