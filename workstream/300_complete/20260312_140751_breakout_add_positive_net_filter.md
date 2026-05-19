# Task: Add Positive Net Filter to Top X Multi-Chart Loader Workflow

## 1. Understanding of Requirements
The user wants to ensure that the `top_x_multi_chart_workflow` only selects strategies that have a positive `total_net` (or positive value for the selected metric). This prevents strategies with losses or zero profit from being pushed to Multi-Charts or Trade Buckets via this automated workflow.

## 2. Plan of Approach
1. [x] Create a formal plan in `plans/`.
2. [x] Modify `_run_top_x_multi_chart_workflow` in `TradeApps/breakout/fs/trade_viewer_api.py` to include a check for `total_net > 0`.
3. [x] Update documentation in `.agent/workflows/top-x-multi-chart-loader.md` to reflect this new rule.
4. [x] Update `workflows.json` description/steps for the workflow.
5. [x] Increment version in `constants.py`.

## 3. Checklist of Changes
*   **`TradeApps/breakout/fs/trade_viewer_api.py`**:
    *   [x] Add `float(entry.get("total_net", 0.0) or 0.0) > 0` condition in the filtering loop of `_run_top_x_multi_chart_workflow`.
*   **`.agent/workflows/top-x-multi-chart-loader.md`**:
    *   [x] Add "Positive Net Filter" to the steps.
*   **`TradeApps/breakout/fs/workflows.json`**:
    *   [x] Update description/steps to mention positive net requirement.
*   **`TradeApps/breakout/fs/constants.py`**:
    *   [x] Update version to `V20260312_1410`.

## 4. Verification
*   [ ] Check that a strategy with zero or negative net is filtered out (simulate or check code logic).
