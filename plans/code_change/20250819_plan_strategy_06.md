# Plan for `06_str_topPerformerShortDuration_live.py`

This document outlines the plan to create the new trading strategy script.

## 1. Overall Goal

Create a new script, `06_str_topPerformerShortDuration_live.py`, based on the template from `05_str_topPerformerAgeEntryPrice_live.py`, but with a simplified trading criteria based on the duration of the most recent closed trade.

## 2. Granular Task List

### Phase 1: Setup and Configuration

*   [ ] **Create New File:** Copy `05_str_topPerformerAgeEntryPrice_live.py` to a new file named `06_str_topPerformerShortDuration_live.py`.
*   [ ] **Update Constants:**
    *   [ ] Change `SCRIPT_NAME` to `06_str_topPerformerShortDuration_live`.
    *   [ ] Add `DURATION_THRESHOLD_MINUTES: Final[int] = 10`.
    *   [ ] Remove `AGE_THRESHOLD_MINUTES` and `AVG_PRICE_WINDOW_HOURS` as they are no longer needed.

### Phase 2: Main Logic Implementation

*   [ ] **Restructure `main()` loop:** The main loop will be refactored to implement the new, simpler logic.
*   [ ] **Implement Core Logic - Step 1: Get Most Recent Close:**
    *   [ ] In the loop, call `get_closed_trades()`.
    *   [ ] Find the trade with the most recent `last_update` timestamp.
*   [ ] **Implement Core Logic - Step 2: Evaluate Trade Criteria:**
    *   [ ] Get the `signal` of the most recent closed trade.
    *   [ ] Get the `age` (duration) of the most recent closed trade from the `age` column in the data.
    *   [ ] **ASSUMPTION:** The "other filters" from the previous script (like checking the age of the close, calculating average prices from profitable trades, and comparing to live prices) are **no longer needed** and will be replaced entirely by this new, simpler duration-based logic.
*   [ ] **Implement Core Logic - Step 3: Buy Path:**
    *   [ ] If `signal == 'buy'` AND `age <= DURATION_THRESHOLD_MINUTES`:
        *   [ ] Call `execute_trade('buy', ...)`.
*   [ ] **Implement Core Logic - Step 4: Sell Path:**
    *   [ ] If `signal == 'sell'` AND `age <= DURATION_THRESHOLD_MINUTES`:
        *   [ ] Call `execute_trade('sell', ...)`.
*   [ ] **Add Logging:** Add detailed logging for the new evaluation process.

### Phase 3: Cleanup

*   [ ] **Remove Unused Functions/Logic:**
    *   [ ] Remove the code for fetching live prices (`get_live_prices()`).
    *   [ ] Remove the logic for calculating average entry prices and filtering by `alt_net_return`.
*   [ ] **Review and Finalize:** Read through the new script to ensure all parts work together and the logic is correctly implemented.
