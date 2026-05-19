# Task: Restrict Trade Bucket Splitting to Explicit Configuration

## 1. Understanding of Requirements
Modify the `Top X Multi-Chart Loader` workflow to ensure that strategy splitting (Net -> Buy/Sell) only occurs when explicitly configured via the `t_split_for_tb` flag. Prevent the transfer of single-row "Total Net" charts to Trade Buckets if splitting is disabled, even if it results in a minimum-row violation.

## 2. Plan of Approach
1.  **Modify `trade_viewer_api.py`**:
    *   Locate `_run_top_x_multi_chart_workflow`.
    *   Update the `should_split` boolean assignment to remove the `(len(pre_tb_family) == 1)` override.
    *   Remove the "emergency split" logic block that forces a split for single-row 'net' metrics.
2.  **Validation**:
    *   Run the workflow with `t_split_for_tb: false` on a single-product strategy and verify it fails to create a TB (reason: `min_rows_violation`).
    *   Run with `t_split_for_tb: true` and verify it successfully splits and transfers.

## 3. List of Changes
*   **`TradeApps/breakout/fs/trade_viewer_api.py`**:
    *   [ ] Refactor `should_split` assignment (approx. line 2240).
    *   [ ] Remove emergency split block (approx. line 2300).
    *   [ ] Update version and add datetimestamp comments.
*   **`TradeApps/breakout/fs/constants.py`**:
    *   [ ] Update version to `V20260413_1330`.
