# Plan: Fix Strategy Name Collision in State Persistence (2026-01-08)

This plan addresses the issue where strategies with similar names (e.g., `breakout` and `breakout_Rev`) incorrectly reference each other's trade files due to substring matching in the persistence logic.

## 1. Understanding of Requirements

*   **Issue**: `common.py` uses `self.script_name in fname` to identify trade files during state restoration (`_load_persisted_state`).
*   **Problem**: If one script name is a substring of another (e.g., `breakout` is in `breakout_Rev`), the shorter name will incorrectly "claim" the longer name's files.
*   **Goal**: Ensure each strategy only picks up its own files by using a more precise matching logic.

## 2. Plan of Approach

1.  **Refine `_load_persisted_state`**:
    *   Change the filename check from `self.script_name in fname` to a more robust prefix check.
    *   Since filenames start with `{script_name}_{product}_`, we can check `fname.startswith(f"{self.script_name}_{self.trade_product}_")`.
    *   Alternatively, split by underscore and check the first part(s). Given our current naming convention `{script_name}_{trade_product}_{direction.upper()}_{ts_str}_{params}.json`, the script name can contain underscores.
    *   The most reliable way is to check `fname.startswith(self.script_name + "_")` and ensure the rest of the metadata matches.

2.  **Update `_is_profitability_guard_passed`**:
    *   Review existing logic to ensure it doesn't suffer from the same flaw. It already has more advanced splitting logic but could be simplified.

3.  **Update Version**:
    *   Update `constants.py` to `V20260108_2330`.

## 3. List of Changes

*   **`common.py`**:
    *   [ ] In `_load_persisted_state`, change `self.script_name in fname` to `fname.startswith(self.script_name + "_")`.
    *   [ ] (Optional) Add a comment explaining the fix for version `V20260108_2330`.
*   **`constants.py`**:
    *   [ ] Update `VERSION` to `V20260108_2330`.

## 4. Verification Plan

*   **Success Criteria**: Running `breakout.py` should NOT pick up trade files belonging to `breakout_Rev`.
*   **Test**: Verify that the "RESTORE" logs only mention trades belonging to the specific script being run.
