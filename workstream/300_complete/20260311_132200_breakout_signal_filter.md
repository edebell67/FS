# Task: Add Signal Filter to Trade Drilldown

## Status: TODO
- Created: 2026-03-11 13:22
- Requirement: Add a signal filter (All/Long/Short) to the Trade Drilldown screen with "All" as default.

## Plan Summary
1.  Add Signal Filter dropdown to `multi_chart.html`.
2.  Add filter state and logic to `multi_chart.js`.
3.  Ensure default is "All" and it resets when opening a new drilldown.
4.  Update version to `V20260311_1330` in `constants.py`. (Completed)

## TODO List
- [x] Create detailed implementation plan in `/plans/`.
- [x] Add Signal Filter HTML to `multi_chart.html`.
- [x] Add event listener and state to `multi_chart.js`.
- [x] Update `renderDrilldownTable` to filter by signal.
- [x] Verify functionality.
- [x] Update version in `constants.py`.

## Completion Summary
- Successfully added Signal Filter (All/Long/Short) to the Trade Drilldown modal.
- Fixed accidental truncation in `multi_chart.html` during the process.
- Verified all modal sections (Drilldown, Transfer, Batch Create) are intact.
- Version updated to V20260311_1330.
