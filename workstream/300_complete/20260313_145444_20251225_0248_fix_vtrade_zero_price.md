# Plan to Fix Missing Prices in Virtual Trades

## 1. Issue Description
The user reported that new virtual trades are being created with `entry_price: 0.0`.
This is happening because `_manage_virtual_trades` is called at the *start* of the main loop in `run_multiwindow`, before the `latest_prices` dictionary has been populated with fresh data from `fetch_latest_quotes`.

## 2. Plan of Approach
I will move the `_manage_virtual_trades` execution block to the end of the `while True` loop, after the `latest_prices` dictionary has been updated with the latest market data.

## 3. List of Changes
*   **`c:\Users\edebe\eds\TradeApps\breakout\common.py`**:
    *   [x] In `run_multiwindow`:
        *   Move the `if time.time() - last_check_time > 60:` block (which calls `_manage_virtual_trades`) from the beginning of the loop to after the results processing section (i.e., after `latest_prices` is updated).
