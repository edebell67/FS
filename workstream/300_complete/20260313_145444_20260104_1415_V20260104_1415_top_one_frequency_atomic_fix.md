# Plan: Atomic Persistence and Process Cleanup (V20260104_1415)

## 1. Objective
Fix the "continuous overwriting" issue where the frequency tally fails to accumulate counts correctly.

## 2. Root Cause Analysis
- Multiple background processes (running for 10h+) are competing for the same file.
- These processes lack the singleton lock and are stomp-writing over each other.

## 3. Plan of Approach
1.  **Atomic Save**: Modify `save_frequency` to use a temporary file + rename strategy to prevent corruption.
2.  **Singleton Enforcement**: The `LOCK_FILE` logic is already in the script, but needs a clean slate to be effective.
3.  **Process Purge**: Terminate all existing `top_one_frequency.py` instances.
4.  **Verification**: Confirm `_top_one_frequency.json` increments properly.

## 4. List of Changes
- [x] **top_one_frequency.py**: 
    - [x] Implement atomic `save_frequency`.
    - [x] Update `VERSION` to `V20260104_1415`.
- [x] **constants.py**:
    - [x] Update `VERSION` to `V20260104_1415`.

## 5. Execution
1. Update code.
2. **USER ACTION REQUIRED**: Please approve the `taskkill` or manually stop all terminal tabs running `top_one_frequency.py`.
3. Restart the script.
