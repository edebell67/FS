# Plan for `07_str_AvgPriceWithOffset_live.py`

This document outlines the plan to create a new trading strategy script based on the average entry price of recent, profitable open trades, with a price offset.

## 1. Overall Goal

Create a new script, `07_str_AvgPriceWithOffset_live.py`, using `05_str_topPerformerAgeEntryPrice_live.py` as a template. The new script will not depend on closed trades, but rather on the state of currently open trades.

## 2. Clarifications & Assumptions

*   **New File:** This plan assumes the creation of a new script, `07_...`, rather than modifying an existing one.
*   **Data Source:** The logic will use the `OPEN_TRADES_ENDPOINT` (`http://127.0.0.1:8000/api/vwCombined_trades_open`) to get the state of open trades.
*   **Time Window for Sells:** The buy criteria specifies a "most recent 2hr" window. For symmetry, the plan assumes this **same 2-hour window** applies to the sell criteria as well.
*   **"Other Filters":** The plan assumes that the core logic of evaluating a "most recent closed trade" is **replaced entirely** by this new logic of evaluating the average price of *all recent open trades* for the specified product.

## 3. Granular Task List

### Phase 1: Setup and Configuration

*   [ ] **Create New File:** Copy `05_str_topPerformerAgeEntryPrice_live.py` to a new file named `07_str_AvgPriceWithOffset_live.py`.
*   [ ] **Update Constants:**
    *   [ ] Add `OPEN_TRADES_ENDPOINT = "http://127.0.0.1:8000/api/vwCombined_trades_open"`.
    *   [ ] Add `PRICE_OFFSET: Final[float] = 0.0002`.
    *   [ ] Add `AVG_PRICE_WINDOW_HOURS: Final[int] = 2`.
    *   [ ] Remove `CLOSED_TRADES_ENDPOINT` and `AGE_THRESHOLD_MINUTES`.

### Phase 2: Data Fetching Functions

*   [ ] **Create `get_open_trades()` function:**
    *   [ ] This function will call the `OPEN_TRADES_ENDPOINT`.
    *   [ ] It will handle JSON parsing and error handling.
    *   [ ] It will return a list of open trade objects.
*   [ ] **Cleanup:** Remove the `get_closed_trades()` function.

### Phase 3: Main Logic Implementation

*   [ ] **Restructure `main()` loop:** The main loop will be completely refactored to implement the new logic.
*   [ ] **Implement Core Logic - Step 1: Get Open Trades & Prices:**
    *   [ ] In the loop, call `get_open_trades()`.
    *   [ ] Call `get_live_prices()`.
*   [ ] **Implement Core Logic - Step 2: Buy Path Evaluation:**
    *   [ ] Filter open trades to get all `buy` trades for the `PRODUCT_TO_TRADE` where `alt_net_return > 0` and the `entry_time` is within the last `AVG_PRICE_WINDOW_HOURS`.
    *   [ ] If any such trades exist, calculate the `avg(entry_price)` for this group.
    *   [ ] Calculate the `buy_target_price = avg(entry_price) - PRICE_OFFSET`.
    *   [ ] If the `current ask price` > `buy_target_price`, call `execute_trade('buy', ...)`.
*   [ ] **Implement Core Logic - Step 3: Sell Path Evaluation:**
    *   [ ] Filter open trades to get all `sell` trades for the `PRODUCT_TO_TRADE` where `alt_net_return > 0` and the `entry_time` is within the last `AVG_PRICE_WINDOW_HOURS`.
    *   [ ] If any such trades exist, calculate the `avg(entry_price)` for this group.
    *   [ ] Calculate the `sell_target_price = avg(entry_price) + PRICE_OFFSET`.
    *   [ ] If the `current bid price` < `sell_target_price`, call `execute_trade('sell', ...)`.
*   [ ] **Add Logging:** Add detailed logging for each step of the new evaluation process.

### Phase 4: Review

*   [ ] **Review and Finalize:** Read through the new script to ensure all parts work together and the logic is correctly implemented.
