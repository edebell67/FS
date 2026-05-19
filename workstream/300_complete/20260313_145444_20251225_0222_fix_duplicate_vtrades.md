# Plan to Fix Duplicate Virtual Trade Creation

## 1. Issue Description
The user noticed an excessive number of "OPEN" virtual trade files being created in `C:\Users\edebe\eds\TradeApps\breakout\json\sim\2025-12-25\virtual`.
This suggests that the system is repeatedly creating new virtual trades instead of detecting and managing the existing open ones.
A likely cause is a race condition or logic flaw where:
1.  The system scans for open trades.
2.  It fails to find (or parse) the existing open trade correctly (perhaps due to file locking, read errors, or filtering logic).
3.  It assumes no trade is open.
4.  It creates a new one.
5.  This loop repeats every few seconds.

The `list_dir` output confirms hundreds of `vt_breakout_*` files created within minutes of each other, confirming the issue.

## 2. Plan of Approach
I will add safeguards to `_manage_virtual_trades` in `common.py`:
1.  **Robust Open Trade Detection**: Improve the scanning of open V-Trades. If a file read fails (e.g., due to race condition with writing), it should probably *skip* acting rather than assuming "no trade exists" and creating a duplicate.
2.  **Duplicate check**: Before calling `_create_new_v_trade`, explicit check if we *already* have an open trade for that exact strategy/product/direction in our `open_v_trades` list.
3.  **Logging**: Add more specific debug logs to see *why* it thinks it needs to create a new trade (e.g., "No open trade found for LONG").

## 3. List of Changes
*   **`c:\Users\edebe\eds\TradeApps\breakout\common.py`**:
    *   [ ] In `_manage_virtual_trades`:
        *   When iterating `open_v_trades` to find `open_buy_v_trade` and `open_sell_v_trade`:
            *   Ensure we are strictly matching.
        *   Before creating a NEW buy trade (`_create_new_v_trade`):
            *   Check again if `open_buy_v_trade` is truly None.
            *   Scan the `open_v_trades` list *one more time* for an open trade with the same product/direction to be absolutely sure.
    *   [ ] (Optional) Add a tiny sleep or retry mechanism when reading JSON files to avoid partial reads causing "empty" data which might lead to "no open trade found".

*   **Logic Refinement**:
    *   The current logic is: `open_buy_v_trade = next((t for t in open_v_trades if t.get('direction') == 'LONG'), None)`
    *   If `open_buy_v_trade` is found but `product` doesn't match `top_buy_product`, it closes the old one and opens a new one.  **This is correct.**
    *   If `open_buy_v_trade` matches `top_buy_product`, it prints "No change". **This is correct.**
    *   If `open_buy_v_trade` is `None`, it creates a new one. **This is where the bug likely is.**

    **Hypothesis**: `open_v_trades` is coming up empty even when files exist.
    *   Why? `json.load(f)` might be failing if the file is being written to? Or `data.get('status') == 'OPEN'` check is failing?
    *   Currently, the `except Exception` block in the file reading loop just prints a warning and *continues*. If *all* reads fail (or return non-OPEN status), `open_v_trades` is empty. The code then proceeds to create a new trade.
    *   **Fix**: If we encounter read errors, we should probably *abort the entire cycle* for safety, rather than assuming "0 open trades" and creating duplicates.

## 4. Revised Plan
1.  Modify the file reading loop: Track if *any* file read failed.
2.  If file reads failed, *return immediately* from `_manage_virtual_trades` to try again next tick. Do not proceed to creation logic. This prevents "phantom" creation when files are locked.
3.  Also, verify that `_create_new_v_trade` isn't being called unconditionally.

## 5. Steps
*   [x] Modify `_manage_virtual_trades` in `common.py` to track read errors.
*   [x] If errors occurred during scanning, log a warning and return.
*   [x] Review the "Reconcile" blocks to ensure they aren't logic-trapped into always creating.
