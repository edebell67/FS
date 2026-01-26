# Strategy 01: Top Performer - Implementation Plan

**Date:** 2025-08-06

This document outlines the creation and logic of the trading strategy script, `01_str_topPerformer.py`.

## 1. Requirements

The goal was to create a standalone Python script that continuously checks for trading opportunities based on model performance data and executes trades if specific conditions are met. The script needed to:

1.  Create a new folder `strategy_library` within `\algo_viewer` to house the program.
2.  Fetch model performance data from a specific API endpoint.
3.  Identify the best-performing model and signal for the 'gbp' product.
4.  Check for any existing open trades for the *same model and signal* to avoid duplication.
5.  Execute a trade by calling a stored procedure via a new FastAPI endpoint, passing a specific `trade_reason`.
6.  Log all actions for monitoring.

## 2. Implementation Details

### Endpoints Used

*   **Model Performance Data:** `http://127.0.0.1:8000/api/vw_106_ModelPerformance_alt`
*   **Open Trades Check:** `http://127.0.0.1:8000/api/vwCombined_trades_open`
*   **Trade Execution:** `http://127.0.0.1:8000/api/execute_trade/`

### Core Logic

The script operates in an infinite loop with the following steps in each cycle:

1.  **Fetch Best Signal**: It calls the model performance endpoint and selects the signal for the `gbp` product that has the highest `total_return`.

2.  **Pre-Trade Check**: Before proceeding, it calls the open trades endpoint to verify that there are no existing trades where:
    *   `model` matches the best signal's model.
    *   `signal` matches the best signal's signal (e.g., 'buy' or 'sell').
    *   `tradeable` is not equal to 0.
    *   If a matching active trade exists, the script logs this and skips the current cycle.

3.  **Trade Execution Logic**: If no active trade is found, it proceeds to check the price conditions:
    *   For a **'sell'** signal: A trade is triggered if `fx_midprice < avg_profitable_entry_price`.
    *   For a **'buy'** signal: A trade is triggered if `fx_midprice > avg_profitable_entry_price`.

4.  **Trade Execution**: The `execute_trade` function calls the `/api/execute_trade/` endpoint on the FastAPI server, sending the `model`, `signal`, and a hardcoded `trade_reason` of `'python_TopPerformer'` in a POST request. The FastAPI server then executes the `dbo.sp_001_copy_trade_as_tradeable` stored procedure with the provided parameters.

5.  **Logging**: All steps, decisions, and errors are logged to both the console and a file named `01_str_topPerformer.log`.

## 3. Files Modified

*   `C:\Users\edebe\eds\algo_viewer\strategy_library\01_str_topPerformer.py`: Main application logic.
*   `C:\Users\edebe\eds\api_server_sql\main.py`: FastAPI server, updated with the new trade execution endpoint.

## 4. Revisions and Bug Fixes (2025-08-06)

Following the initial implementation, several enhancements and bug fixes were made:

*   **Enhanced Logging**: The script's logging was significantly improved to provide a detailed, step-by-step breakdown of each trade evaluation. This includes logging the specific data points being compared (model, signal, prices) and a clear outcome message stating whether a trade was generated or skipped, and why.

*   **`AttributeError` Resolution**: The script initially failed with an `AttributeError: 'str' object has no attribute 'get'`. This was caused by the API returning JSON data that was nested or "double-encoded". The issue was resolved by updating both the `get_best_signal_and_price` and `has_open_trade` functions to correctly parse the nested data structure from their respective API endpoints.

*   **Database Execution Error**: A "500 Internal Server Error" occurred because the `model` ID was being sent as a string to a stored procedure that expected an integer. This was fixed by adding a type conversion in the FastAPI server to ensure the data type was correct before the database call.

*   **API and Trade Check Enhancements (2025-08-07)**:
    *   **FastAPI Server Filtering**: The FastAPI server (`api_server_sql/main.py`) was modified to allow filtering of the `/api/{view_name}` endpoint (specifically used for `vwCombined_trades_open`) by `model`, `signal`, and `tradeable != 0` via URL query parameters. This significantly reduces the data transferred and processed.
    *   **Script Optimization**: The `has_open_trade` function in `01_str_topPerformerAtAvgPrice.py` was updated to utilize these new filtered API calls, passing `model_name`, `signal`, and `tradeable!=0` as query parameters to the `OPEN_TRADES_ENDPOINT`. The client-side `tradeable != 0` check was retained for robustness.
    *   **Trade Origin Check**: The `has_open_trade` function was further refined to include a check for `trade.get('trade_reason') == SCRIPT_NAME`, ensuring that only trades originating from the same script are considered when determining if an open trade exists.
