## Gemini Coder - Plan for Adding S08S Debugging Logs

### 1. Understanding of Requirements

The user wants to add explicit logging to `Strategy08SR` (which inherits from `Strategy08S`) to understand why trades are not being executed, even when conditions appear to be met. The logs should be visible in the UI's "View Transcript" window.

### 2. Plan of Approach

1.  Increment the application version number in `constants.py`.
2.  Add `tradeflow.info` calls within the `evaluate` method of `s08s.py` to log key internal states and confirm execution flow.
3.  Save this plan to the specified directory.

### 3. List of Changes

*   **`tradepanel/constants.py`**:
    *   [x] Update `VERSION: Final[str] = "64.3.13"` to `"64.3.14"`.

*   **`tradepanel/strategies/s08s.py`**:
    *   [x] Add the following `tradeflow.info` call at the beginning of the `evaluate` method:

        ```python
        # 2025-07-30: NEXT_VERSION_NUMBER - Added for debugging trade execution flow
        tradeflow.info("s08s_evaluate_start", {
            "open_diff": tm.block0_buy_open_total_trades - tm.block0_sell_open_total_trades,
            "active_trades_count": len(tm.active_trades_list),
            "strategy_name": self.name,
            "entry_threshold": self.entry_threshold,
            "min_diff_threshold": self.min_diff_threshold,
            "range_type": self.range_type
        })
        # --- END ADDITION ---
        ```
    *   [x] Add the following `tradeflow.info` call inside the `if sell_criteria_met:` block, just before the `self.logger.info` line:

        ```python
        # 2025-07-30: NEXT_VERSION_NUMBER - Added for debugging trade execution flow
        tradeflow.info("s08s_sell_criteria_met_attempting_trade", {
            "open_diff": open_diff,
            "entry_threshold": self.entry_threshold,
            "min_diff_threshold": self.min_diff_threshold,
            "range_type": self.range_type,
            "strategy_name": self.name
        })
        # --- END ADDITION ---
        ```
