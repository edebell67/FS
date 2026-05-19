# Weekly Performance Full-Week Navigation Layout

## Source
User request during conversation 1dc8e4c5-47c8-4ca9-9bc9-8cb42900b7de

## Task Summary
Update the Weekly Performance layout so it always displays one complete working week at a time using fixed weekday columns ordered `Mon -> Sun`. Update backward and forward navigation so each action moves exactly one full week and always renders the target week in full.

## Requirements
1. Display exactly one full calendar week at a time.
   - Columns must be fixed to `Mon`, `Tue`, `Wed`, `Thu`, `Fri`, `Sat`, `Sun` in that order.
   - The visible week must align to a complete Monday-through-Sunday range.
2. Adjust the displayed data window to the aligned week.
   - If the current selected date range is partial or offset, normalize it to the containing Monday-through-Sunday week.
   - Header and date labels must reflect the full aligned week.
3. Change backward navigation behavior.
   - Moving backward must shift the view by exactly one full week.
   - The resulting view must show the previous Monday-through-Sunday period in full.
4. Change forward navigation behavior.
   - Moving forward must shift the view by exactly one full week.
   - The resulting view must show the next Monday-through-Sunday period in full.
5. Preserve table behavior for ranking and totals.
   - Strategy ranking, totals, and trade counts must continue to work against the displayed week only.

## Context
- Weekly Performance page shown at `localhost:5000/weekly_performance.html`
- Likely related frontend and/or backing logic under the breakout app that builds weekly columns, labels, and previous/next week navigation

## Dependency
Dependency: None

## Plan

- [x] 1. Locate the Weekly Performance page implementation and identify where weekday columns and date-range navigation are generated.
  - [x] Test: Confirm the relevant HTML/JS/Python files responsible for column labels and previous/next week actions.
  - Evidence: `TradeApps/breakout/fs/weekly_performance.html` handles fetch/render/navigation, `TradeApps/breakout/fs/trade_viewer_api.py` exposes `/api/weekly_performance`, and `TradeApps/breakout/fs/tools/aggregate_top_strategies.py` builds the weekly date window and aggregated columns.

- [x] 2. Update week-range normalization logic to anchor every rendered view to a full Monday-through-Sunday week.
  - [x] Test: Load a known partial or offset range and verify it snaps to the containing full week.
  - Evidence: `python -m pytest tests\test_breakout_weekly_performance.py -q` passed, including `test_get_week_bounds_aligns_to_monday_sunday`; Flask test-client check for `target_date=2026-03-26` returned `week_start=2026-03-23` and `week_end=2026-03-29`.

- [x] 3. Update the table column generation to render fixed weekday order `Mon -> Sun`.
  - [x] Test: Verify seven weekday columns appear in the correct order for multiple weeks.
  - Evidence: Aggregator now emits `dates_included` as seven ascending dates with `date_labels` from `Mon` through `Sun`; regression test `test_aggregate_for_product_type_outputs_full_monday_to_sunday_week` verified `Mon 03-23` through `Sun 03-29`.

- [x] 4. Update previous/next navigation so each action advances or rewinds by exactly seven days from the aligned week boundary.
  - [x] Test: Click backward and forward repeatedly and verify each rendered week is complete and contiguous.
  - Evidence: `weekly_performance.html` now advances from `currentData.week_start` rather than an arbitrary selected date; API caches by aligned `week_start` filename so adjacent requests always resolve to contiguous Monday-through-Sunday ranges.

- [x] 5. Validate totals and trade counts against the displayed week and move the task to completion once verified.
  - [x] Test: Manual verification in the Weekly Performance page and any available regression checks.
  - Evidence: `test_aggregate_for_product_type_outputs_full_monday_to_sunday_week` verified totals/trade counts only include the aligned week and exclude out-of-week trades; live API check returned a valid full-week payload for `forex`. UI verification request is still pending before final closure.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: manual_verification
  - Artifact: Weekly Performance UI showing full Monday-through-Sunday columns and week-by-week navigation.
  - Objective-Proved: Layout and navigation match the requested weekly behavior.
  - Status: planned

- Evidence-Type: test_output
  - Artifact: `python -m pytest tests\test_breakout_weekly_performance.py -q` → `3 passed in 1.61s`
  - Objective-Proved: Week alignment, fixed seven-day payload generation, and aligned API response behavior are covered by regression tests.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: Flask test-client request to `/api/weekly_performance?product_type=forex&target_date=2026-03-26` returned HTTP `200`, `week_start=2026-03-23`, `week_end=2026-03-29`, `first_label=Mon 03-23`, `last_label=Sun 03-29`.
  - Objective-Proved: The live API payload now normalizes an offset target date to a full Monday-through-Sunday week with fixed weekday ordering.
  - Status: captured

- Evidence-Type: diff
  - Artifact: Updated `TradeApps/breakout/fs/tools/aggregate_top_strategies.py`, `TradeApps/breakout/fs/trade_viewer_api.py`, `TradeApps/breakout/fs/weekly_performance.html`, and added `tests/test_breakout_weekly_performance.py`.
  - Objective-Proved: Backend aggregation, API week resolution, frontend rendering/navigation, and regression coverage were all updated together.
  - Status: captured

## Implementation Log
- 2026-03-28 16:34 — Task created from the request to enforce full-week `Mon -> Sun` layout and whole-week navigation in Weekly Performance.
- 2026-03-28 17:03 — Moved from `workstream/100_todo` to `workstream/200_inprogress/codex` on user instruction.
- 2026-03-28 17:10 — Confirmed the active implementation path: frontend page `TradeApps/breakout/fs/weekly_performance.html`, backend API `TradeApps/breakout/fs/trade_viewer_api.py`, and aggregation logic `TradeApps/breakout/fs/tools/aggregate_top_strategies.py`.
- 2026-03-28 17:18 — Replaced trailing-trading-day aggregation with a true Monday-through-Sunday calendar-week payload, including explicit `week_start`, `week_end`, and fixed `date_labels`.
- 2026-03-28 17:20 — Updated `/api/weekly_performance` to align incoming `target_date` values to the containing week and cache weekly payloads by aligned Monday date.
- 2026-03-28 17:21 — Updated `weekly_performance.html` to render the backend weekday labels and navigate by `currentData.week_start` in exact seven-day increments.
- 2026-03-28 17:23 — Added regression tests for week alignment, full-week payload shape, and aligned API behavior; verified with `pytest` and a live Flask test-client request.

## Changes Made
- `TradeApps/breakout/fs/tools/aggregate_top_strategies.py`
  - Added helpers to align any requested date to the containing Monday-through-Sunday week.
  - Changed weekly aggregation to always emit seven ordered dates and weekday labels.
  - Preserved totals/trade counts strictly within the displayed week.
- `TradeApps/breakout/fs/trade_viewer_api.py`
  - Updated `/api/weekly_performance` to normalize `target_date` to the aligned week before generating or reading cache files.
  - Changed weekly cache naming to use the aligned Monday date for deterministic previous/next navigation.
- `TradeApps/breakout/fs/weekly_performance.html`
  - Updated header rendering to use backend-supplied `date_labels`.
  - Changed week navigation to move from the aligned week start, guaranteeing whole-week jumps.
- `tests/test_breakout_weekly_performance.py`
  - Added regression coverage for week-bound alignment, full seven-day payload generation, and aligned API output.

## Validation
- 2026-03-28 17:10 — Discovery validation: inspected the Weekly Performance page, API route, and aggregation utility to confirm where week range generation and navigation are implemented.
- 2026-03-28 17:22 — `python -m py_compile TradeApps\breakout\fs\tools\aggregate_top_strategies.py TradeApps\breakout\fs\trade_viewer_api.py` → passed.
- 2026-03-28 17:22 — `python -m pytest tests\test_breakout_weekly_performance.py -q` → passed (`3 passed in 1.61s`).
- 2026-03-28 17:23 — Flask test-client check:
  - Request: `/api/weekly_performance?product_type=forex&target_date=2026-03-26`
  - Result: HTTP `200`, `week_start=2026-03-23`, `week_end=2026-03-29`, `dates_included=[2026-03-23..2026-03-29]`, `first_label=Mon 03-23`, `last_label=Sun 03-29`.
- 2026-03-28 17:24 — User verification requested: confirm in `localhost:5000/weekly_performance.html` that:
  - columns are fixed `Mon -> Sun`,
  - the header range always shows one complete Monday-through-Sunday week,
  - previous/next arrows move exactly one week at a time,
  - totals and trade counts match the displayed week only.

## Risks/Notes
- Technical validation is complete, but this is a user-visible screen change, so final closure still depends on browser verification against the live page.
- Existing weekly cache files named by non-aligned dates remain on disk; the updated route now reads and writes aligned Monday-based weekly cache files.

## Completion Status
- Awaiting user verification — 2026-03-28 17:24
