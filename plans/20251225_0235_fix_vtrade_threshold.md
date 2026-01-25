# Plan to Replace Hardcoded PnL Threshold with Config Value

## 1. Issue Description
The user identified that the PnL threshold for creating virtual trades in `_manage_virtual_trades` is currently hardcoded to `> 0`.
This should instead use the `profitability_guard.threshold_y` value from `config.json`, consistent with other parts of the application.

## 2. Plan of Approach
I will modify `_manage_virtual_trades` in `common.py` to:
1.  Read `profitability_guard` -> `threshold_y` from the loaded config.
2.  Replace the hardcoded `> 0` checks for both BUY and SELL reconciliation blocks with `> guard_threshold_y`.

## 3. List of Changes
*   **`c:\Users\edebe\eds\TradeApps\breakout\common.py`**:
    *   [x] In `_manage_virtual_trades`:
        *   Extract `guard_threshold_y` from `config` (defaulting to 0.0 if not found).
        *   Update the condition `if top_buy_product and top_buy_pnl > 0:` to `if top_buy_product and top_buy_pnl > guard_threshold_y:`.
        *   Update the condition `if top_sell_product and top_sell_pnl > 0:` to `if top_sell_product and top_sell_pnl > guard_threshold_y:`.
        *   Update debug logs to reflect the actual threshold used.
