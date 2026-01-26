# Plan for `05_str_topPerformerAgeEntryPrice_live.py`

This document outlines the plan to create the new trading strategy script.

## 1. Overall Goal

Create a new script, `05_str_topPerformerAgeEntryPrice_live.py`, based on the template from `01_str_topPerformerAtAvgPrice_live.py`, but implementing a new set of trading criteria based on the age of recent trades and dynamically calculated average prices.

## 2. Granular Task List

### Phase 1: Setup and Configuration

*   [ ] **Create New File:** Copy `01_str_topPerformerAtAvgPrice_live.py` to a new file named `05_str_topPerformerAgeEntryPrice_live.py`.
*   [ ] **Update Constants:**
    *   [ ] Change `SCRIPT_NAME` to `05_str_topPerformerAgeEntryPrice_live`.
    *   [ ] Add `CLOSED_TRADES_ENDPOINT = "http://127.0.0.1:8000/api/trades_closed"`.
    *   [ ] Add `LIVE_PRICES_ENDPOINT = "http://127.0.0.1:8000/api/vw_000_forex_prices"`.
    *   [ ] Add `AGE_THRESHOLD_MINUTES = 30`.
    *   [ ] Add `AVG_PRICE_WINDOW_HOURS = 2`.

### Phase 2: Data Fetching Functions

*   [ ] **Create `get_closed_trades()` function:**
    *   [ ] This function will call the `CLOSED_TRADES_ENDPOINT`.
    *   [ ] It will handle JSON parsing and error handling.
    *   [ ] It will return a list of closed trade objects.
*   [ ] **Create `get_live_prices()` function:**
    *   [ ] This function will call the `LIVE_PRICES_ENDPOINT`.
    *   [ ] It will handle JSON parsing and error handling.
    *   [ ] It will return a dictionary containing `bid_price` and `ask_price`.

### Phase 3: Main Logic Implementation

*   [ ] **Restructure `main()` loop:** The main loop will be completely refactored to implement the new logic.
*   [ ] **Implement Core Logic - Step 1: Get Most Recent Close:**
    *   [ ] In the loop, call `get_closed_trades()`.
    *   [ ] Find the trade with the most recent `last_update` timestamp. This will be considered the "most recent closed trade".
*   [ ] **Implement Core Logic - Step 2: Check Age and Signal:**
    *   [ ] **Clarification on "Age":** The age of the most recent closed trade will be calculated as `datetime.now() - trade.last_update_datetime`. Your clarification ("time elaspsed between created and last_update") will be interpreted as the trade's *duration*, which is not used in the primary condition.
    *   [ ] Check if this age is less than `AGE_THRESHOLD_MINUTES`.
    *   [ ] If the age check passes, get the `signal` of this trade.
*   [ ] **Implement Core Logic - Step 3: Buy Path:**
    *   [ ] If `signal == 'buy'`:
        *   [ ] Filter the list of all closed trades to find `buy` trades closed within the last `AVG_PRICE_WINDOW_HOURS`.
        *   [ ] From that group, filter for trades where `alt_net_return > 0`.
        *   [ ] If any such trades exist, calculate the `avg(entry_price)` for this group.
        *   [ ] Call `get_live_prices()` to get the `latest_bid_price`.
        *   [ ] If `latest_bid_price > avg(entry_price)`, call `execute_trade('buy', ...)`.
*   [ ] **Implement Core Logic - Step 4: Sell Path:**
    *   [ ] If `signal == 'sell'`:
        *   [ ] Filter the list of all closed trades to find `sell` trades closed within the last `AVG_PRICE_WINDOW_HOURS`.
        *   [ ] From that group, filter for trades where `alt_net_return > 0`.
        *   [ ] If any such trades exist, calculate the `avg(entry_price)` for this group.
        *   [ ] Call `get_live_prices()` to get the `latest_ask_price`.
        *   [ ] If `latest_ask_price < avg(entry_price)`, call `execute_trade('sell', ...)`.
*   [ ] **Add Logging:** Add detailed logging for each step of the evaluation process.

### Phase 4: Cleanup

*   [ ] **Remove Unused Functions:** Delete the old `get_best_signal_and_price` function from the template, as it is no longer needed.
*   [ ] **Review and Finalize:** Read through the new script to ensure all parts work together and the logic is correctly implemented.
