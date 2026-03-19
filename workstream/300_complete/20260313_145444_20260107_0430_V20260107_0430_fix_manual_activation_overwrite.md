# Plan: Fix Manual Activation Overwrite Bug

This document outlines the plan to fix a bug where manual strategy activations are being overwritten by the automatic activation process.

## 1. Requirement

The user has observed that manually activating a strategy via the UI does not persist. The `activations.json` file does not retain the `"manual": true` flag, and the UI becomes out of sync with the backend state.

The desired behavior is:
1.  Automated actions should **not** overwrite manually activated strategies.
2.  Automated activations should be added alongside existing manual activations.
3.  The `activations.json` file must be the single source of truth, and the UI must always reflect its contents.

## 2. Bug Analysis

The root cause is a flaw in the file-saving logic within `_perform_auto_activation_check()` in `common.py`.

1.  The function incorrectly calculates the updates to be saved. It calls `.update()` on the top-level activations object (`{'live': ..., 'sim': ...}`) instead of the `[run_mode]` sub-dictionary, corrupting the data structure in memory.
2.  It then calls `_save_activations()`, which has its own flawed logic. It expects a dictionary for a single mode but receives the corrupted top-level object, leading it to completely overwrite the correct data in `activations.json` with a malformed dictionary.

## 3. Plan of Approach

The fix involves refactoring the file-saving logic to be more robust and correct.

1.  **Refactor `_save_activations()`**: This function will be simplified to perform one task: accept a complete, well-formed activations object (`{'live': ..., 'sim': ...}`) and save it directly to `activations.json`. This makes its behavior safe and predictable.

2.  **Fix `_perform_auto_activation_check()`**: The end of this function, where updates are applied, will be rewritten to follow the correct procedure:
    a. Load the complete `all_activations` object from `activations.json`.
    b. Get the specific sub-dictionary for the current `run_mode` (e.g., `all_activations['live']`).
    c. Apply the calculated `updates` to this sub-dictionary. This correctly preserves all existing entries (including manual ones) that were not part of the update calculation.
    d. Call the newly refactored `_save_activations()` with the complete `all_activations` object to write the correct state back to the file.

3.  **Update Version**: The `VERSION` constant in `constants.py` will be updated to `V20260107_0430` to reflect this change.

## 4. List of Changes

*   **`tradepanel/breakout/common.py`**:
    *   **`_save_activations()`**:
        *   Change the function signature to accept a single `full_activations_data` dictionary.
        *   Remove all internal logic related to `run_mode`, sanitization, and dictionary merging.
        *   Replace the body with a simple `json.dump()` of the provided `full_activations_data` object to the `ACTIVATIONS_FILE`.
    *   **`_perform_auto_activation_check()`**:
        *   Replace the section that applies updates with the new, correct logic described in section 3.2 above.
*   **`tradepanel/breakout/constants.py`**:
    *   Update `VERSION` to `"V20260107_0430"`.
