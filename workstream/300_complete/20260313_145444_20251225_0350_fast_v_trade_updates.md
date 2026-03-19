# Plan: Faster Price Updates for Virtual Trades

## 1. Requirement
The user reports "no price change" for V-Trades.
Root causes identified:
1.  Live price updates were inside `_manage_virtual_trades`, which only runs every 60 seconds.
2.  The update logic was conditional on `global_stats` being non-empty, which might not be true in fresh simulation runs.

## 2. Approach
I will separate the "Live Price Update" logic from the "Lifecycle Management" logic.

1.  **Create `_update_open_v_trades_prices(json_base_dir, latest_prices, config)`**:
    *   This function will scan for `OPEN` V-trades in the `virtual` directory.
    *   It will update `current_price` and recalculate PnL using `_calculate_v_trade_pnl`.
    *   It will write the updated JSON to disk.
    *   This function will be lightweight and focused only on updates.

2.  **Modify `common.py`**:
    *   Add the new function `_update_open_v_trades_prices` (reusing the logic I wrote in the previous step).
    *   Call `_update_open_v_trades_prices` inside the main `run_multiwindow` loop, every iteration (every `poll_interval` seconds, typically 10s), ensuring faster feedback.
    *   Remove the duplicate update logic from `_manage_virtual_trades` to keep concerns separated (Lifecycle vs. Real-time Updates).

## 3. Checklist
- [x] Implement `_update_open_v_trades_prices` in `common.py`.
- [x] Add call to `_update_open_v_trades_prices` in `run_multiwindow` (outside the 60s block).
- [x] Revert/Clean up the update logic inside `_manage_virtual_trades`.
- [x] Update `VERSION`.

## 4. Verification
- [x] Verify syntax.
- [x] User should see price changes within `poll_interval` (default 10s).
