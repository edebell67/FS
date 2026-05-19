# Plan: Fix Trade Activation and Block Reasons

This document outlines the plan to fix the trade activation logic and ensure block reasons are correctly persisted to trade JSON files.

## 1. Understanding of Requirements

*   **Activation Mismatch**: The backend is checking for activation keys like `script_name_buy_net`, while `activations.json` (and the frontend) uses keys that include additional parameter strings, e.g., `script_name_window_buffer_tp_sl_buy_net`.
*   **Missing Block Reasons**: Although logic was added to capture `trade_block_reason`, it is currently not being included in the dictionary saved to disk in `_save_trade_json`.

## 2. Plan of Approach

1.  **Update `_is_active` in `common.py`**:
    *   Modify the key construction to include the strategy parameters (`window_size`, `pip_buffer`, `tp_pips`, `sl_pips`).
    *   This will ensure the backend correctly identifies active strategies from `activations.json`.
2.  **Update `_save_trade_json` in `common.py`**:
    *   Explicitly add `trade_block_reason` to the `trade_data` dictionary before it is saved to a file.
    *   This will allow the user to see why a trade was blocked (e.g., activation failure or guard failure) directly in the trade JSON or viewer.
3.  **Update Version**:
    *   Update `VERSION` in `constants.py` to `V20251231_1000`.

## 3. List of Changes

### `common.py`

*   [ ] In `BaseBreakoutStrategy._is_active()`:
    *   Construct the key as:
        ```python
        key = f"{self.script_name}_{self.window_size}_{self.pip_buffer}_{self.tp_pips}_{self.sl_pips}_{direction.lower()}_{mode.lower()}"
        ```
*   [ ] In `BaseBreakoutStrategy._save_trade_json()`:
    *   Add `trade_block_reason` to the `trade_data` dictionary:
        ```python
        if 'trade_block_reason' in self.open_trade:
            trade_data['trade_block_reason'] = self.open_trade['trade_block_reason']
        ```

### `constants.py`

*   [ ] Update `VERSION` to `V20251231_1000`.

## 4. Verification

*   Restart strategy scripts.
*   Monitor new trades to confirm `is_live_trade` becomes `true` when active in `activations.json`.
*   If a trade is blocked, verify the reason is present in the trade JSON.
