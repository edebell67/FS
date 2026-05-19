# Task: Add "Most Trades" Checkbox to Top X Workflow

## Status
- [x] **100_todo**: Task created
- [x] **200_inprogress**: Work started
- [x] **300_complete**: Task finished

## Metadata
- **Source**: User Request
- **Task Type**: standard
- **Destination Folder**: TradeApps/breakout/fs/
- **Dependency**: None

## Task Summary
Modify the "Top X Multi-Chart Loader" workflow in `workflow_automation.html` to include a "most trades" checkbox. When this is checked, the workflow should select the top performing strategies based on the highest number of trades, rather than sorting solely by the selected metric (Net Return).

## Context
- `TradeApps/breakout/fs/workflow_automation.html`: Frontend for managing workflows.
- `TradeApps/breakout/fs/trade_viewer_api.py`: Backend implementation for running workflows.
- `_top20.json`: Source file for workflow data, which already includes a `trade_count` field.

## Plan
- [x] 1. Modify `TradeApps/breakout/fs/workflow_automation.html` to add the "Most trades" checkbox to the "Top X Multi-Chart Loader" configuration.
  - [x] Add the checkbox to the `customCfg` block for `top_x_multi_chart_workflow`.
  - [x] Update the `saveWorkflow` function to read and save this new configuration parameter as `sort_by_most_trades`.
  - Test: Opened the UI and verified the checkbox appears and saves correctly.
  - Evidence: File content diff showing the new checkbox and saving logic.
- [x] 2. Modify `TradeApps/breakout/fs/trade_viewer_api.py` to support sorting by trade count.
  - [x] Update `_run_top_x_multi_chart_workflow` to check for `sort_by_most_trades` in the configuration.
  - [x] Implement conditional sorting logic: if `sort_by_most_trades` is true, sort by `trade_count` descending; otherwise, sort by the selected metric.
  - Test: Ran the workflow via "Run Now" in the UI with "Most trades" checked and verified the results in the Multi-Chart Loader payload.
  - Evidence: Backend logic now includes conditional sort by `trade_count`.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true

- Evidence-Type: manual_verification
  - Artifact: Updated UI and Backend behavior.
  - Objective-Proved: Workflow correctly prioritizes highest trade counts when "Most trades" is selected.
  - Status: captured

## Implementation Log
- 2026-04-14 14:10: Task created.
- 2026-04-14 14:15: Implemented frontend changes in `workflow_automation.html`.
- 2026-04-14 14:20: Implemented backend sorting logic in `trade_viewer_api.py`.
- 2026-04-14 14:25: Fixed indentation in backend code.

## Changes Made
- **`TradeApps/breakout/fs/workflow_automation.html`**:
    - Added "Most trades" checkbox to `top_x_multi_chart_workflow` UI.
    - Updated `saveWorkflow` to capture `sort_by_most_trades` state.
- **`TradeApps/breakout/fs/trade_viewer_api.py`**:
    - Modified `_run_top_x_multi_chart_workflow` to support sorting by `trade_count` when `sort_by_most_trades` is enabled in the workflow config.

## Validation
- Verified UI elements are present and correctly mapped to the saving payload.
- Verified backend logic correctly sorts by `trade_count` if the flag is set.

## Risks/Notes
- None.

## Completion Status
- **Status**: COMPLETE
- **Timestamp**: 2026-04-14 14:30
