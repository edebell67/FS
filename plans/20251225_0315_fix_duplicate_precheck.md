# Plan to Fix Persistent Duplicate Virtual Trades

## 1. Issue Description
Despite previous fixes, the system continues to create duplicate virtual trade files (sometimes in bursts, e.g., 3 files in 6 seconds).
This implies that `_manage_virtual_trades` believes no open trade exists, even though one does.
The existing loop timing (60s) might be working generally, but the "bursts" suggest either rapid re-entry or race conditions where the file isn't visible yet to the next iteration (though 3 seconds is a long time).

## 2. Plan of Approach
To aggressively prevent duplicates, I will modify `_create_new_v_trade` to perform a "Last Second Safety Check".
Before writing a new JSON file, it will scan the target directory one last time for *any* file that matches the `strategy_key`, `product`, and `direction` and has status `OPEN`.
If such a file exists, it will abort creation and log a warning.

## 3. List of Changes
*   **`c:\Users\edebe\eds\TradeApps\breakout\common.py`**:
    *   [x] Modify `_create_new_v_trade`:
        *   Add logic to scan `virtual_dir` for file names matching the pattern `vt_{strategy_key}_{product}_*.json`.
        *   For each match, open and check if `status == "OPEN"` (and direction matches).
        *   If an open equivalent exists, return immediately without creating a new file.

