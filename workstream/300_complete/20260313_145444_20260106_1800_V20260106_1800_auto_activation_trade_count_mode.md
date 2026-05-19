# Plan: Add Configurable Trade Count Logic for Auto-Activation

This document outlines the plan to add a new configurable mode for strategy selection based on trade count.

## 1. Requirement

The user wants an alternative to the existing `min_auto_trades` criterion for selecting strategies for auto-activation. The new option should select the single strategy with the **maximum number of trades**, provided it also meets all other performance criteria (e.g., P&L > X). The user wants to be able to switch between the existing "minimum trades" mode and the new "maximum count" mode via a configuration setting.

## 2. Plan of Approach

### 2.1. New Configuration Setting

-   A new setting, `"auto_trade_count_mode"`, will be added to `config.json`.
-   This setting will have two possible values:
    -   `"min_trades"`: (Default) The existing behavior, where strategies must have a trade count greater than or equal to `min_auto_trades`.
    -   `"max_count"`: The new behavior, which selects the single strategy with the highest trade count from the pool of eligible candidates.

### 2.2. Code Implementation (`common.py`)

1.  **Update `_load_config()`**: The default configuration dictionary within this function will be updated to include `"auto_trade_count_mode": "min_trades"`.

2.  **Modify `_perform_auto_activation_check()`**: The core logic for candidate selection will be refactored. This will be done for both the "Net Activations" and "Alt Activations" sections of the function.

    -   The function will first load the new `auto_trade_count_mode` from the configuration.
    -   It will gather a list of `pre_candidates` by filtering all strategies based on the common performance criteria that apply in both modes (Total P&L, Win Rate, and Average Return).
    -   It will then create a `final_candidates` list based on the selected mode:
        -   **If mode is `"min_trades"`**: The `pre_candidates` list will be further filtered to include only those strategies where `total_count >= min_auto_trades`.
        -   **If mode is `"max_count"`**: The system will find the single strategy with the maximum `total_count` from the `pre_candidates` list. This single strategy will become the only member of the `final_candidates` list.
    -   The remainder of the function (sorting by P&L, selecting the top N, and checking against the API frequency map) will then operate on this `final_candidates` list.

## 3. List of Changes

*   **`tradepanel/breakout/common.py`**:
    *   **In `_load_config()`**:
        *   Add `"auto_trade_count_mode": "min_trades"` to the default dictionary.
    *   **In `_perform_auto_activation_check()`**:
        *   Load the `auto_trade_count_mode` value from the config.
        *   For both "Net" and "Alt" activation logic:
            *   Create a preliminary list of candidates that pass all criteria *except* the trade count check.
            *   Based on `auto_trade_count_mode`, apply a second filtering step to create the final list of candidates (either using `min_auto_trades` or finding the single strategy with the `max_count`).
            *   Ensure the candidate dictionaries include the `total_count` so it can be used for sorting in the "max_count" mode.
            *   Update the sorting logic for "max_count" mode to sort by `total_count` first, then `pnl`.

(Note: As per user feedback, the sorting for "max_count" mode will not be changed; the selection of the single max-count candidate is the primary mechanism.)
