# 20251222_1600_V20251222_1600_Global_Top3_Strategy_Activation

## 1. Understanding of Requirements
The user requires a global limit of 3 total strategies active across *all* running scripts. The previous attempts to centralize this control were flawed. The goal is to enforce a single global limit for `auto_net_check` and `auto_alt_net_check` by modifying `common.py` such that a single instance of `_perform_auto_activation_check` (the one that acquires a lock) will decide the global state.

## 2. Plan of Approach

1.  **Modify `_perform_auto_activation_check` in `TradeApps/breakout/common.py`**:
    *   The `target_script_names` parameter will be removed. The function will operate on a global scale.
    *   It will scan *all* trade files (closed and open live trades) from the `json_base_dir` to get a comprehensive global picture of performance and open L-trades.
    *   It will identify all `protected_keys` (strategies with open L-trades) across *all* strategies.
    *   It will aggregate P&L and trade counts for *all* closed strategies.
    *   It will apply the "Top N" (currently 3) logic globally to select `final_net_keys` and `final_alt_keys` from *all* strategies.
    *   A file-based locking mechanism will be implemented to ensure atomicity and prevent race conditions when multiple strategy processes try to update `activations.json` simultaneously. Only the process that successfully acquires the lock will perform the update.

## 3. List of Changes

### `TradeApps/breakout/common.py` (MODIFY)
- [ ] **Modify `_perform_auto_activation_check` function**:
    - [ ] Remove `target_script_names` parameter.
    - [ ] Update logic to scan *all* open and closed trade files in `json_base_dir` (without filtering by `target_script_names`).
    - [ ] Implement a file-based locking mechanism (`ACTIVATIONS_LOCK_FILE`) around the entire update process of `activations.json`.
        -   Attempt to acquire lock.
        -   If lock acquired: Perform global calculation, update `activations.json`, release lock.
        -   If lock not acquired: Skip update for this cycle, print a message.
    - [ ] The `final_net_keys` and `final_alt_keys` sets will be derived from the global top N strategies.
    - [ ] The deactivation logic will be modified to deactivate any strategy not in the global `final_net_keys` or `final_alt_keys` (while respecting the master `auto_net/alt_check` flags).
    - [ ] Logging of activations/deactivations will remain.
- [ ] **Modify `run_multiwindow` function**:
    - [ ] Remove `unique_script_names` and `json_base_dir` parameters from the call to `_perform_auto_activation_check`.

### `TradeApps/breakout/constants.py`
- [ ] Update `VERSION` to `V20251222_1600`.

## 4. Verification Plan
- [ ] Start multiple strategy scripts concurrently.
- [ ] Observe `activations.json` to confirm that it strictly adheres to a maximum of 3 activated 'Net' strategies and 3 activated 'Alt' strategies (plus any protected ones).
- [ ] Verify that live trades are correctly generated for the top strategies and that the global `daily_target` limit is respected.
