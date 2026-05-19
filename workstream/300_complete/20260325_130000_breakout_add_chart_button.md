# Task: Add Chart Button to Strategy Performance Table
**Status:** In 300_complete
**Created:** 2026-03-25 13:00
**Related Plan:** `C:\Users\edebe\eds\plans\20260325_1300_V20260325_1300_Add_Chart_Button_Strategy_Perf.md`

## Objective
The user has requested to include a new column inside the `strategy_performance.html` main data table. This column will contain a "Chart" button for each row. The goal is to easily send the summarized data of the selected row's strategy and product to the multi-charts view, using the exact same function and logic currently operating within the Top 20 screen modal.

## Action Items
To be executed upon user confirmation of the plan.
- [x] Implement UI layout changes to fit the new column in `strategy_performance.html`.
- [x] Inject the `sendSummarySelectionToMultiChart()` interactive button per row.
- [x] Update the system version in `constants.py`.
- [x] Conduct a local manual verification test.

## Execution Log
- **2026-03-25 13:00**: Task created in `100_todo`. Plan document generated for user review. Awaiting user confirmation to proceed.
- **2026-03-25 13:58**: Implementation complete. Task moved to `300_complete`.
