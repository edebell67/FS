# Gemini Coder - Plan for 01_str_topPerformerAtAvgPrice_sim.py Function

This document outlines the function and key characteristics of the new simulation strategy script: `01_str_topPerformerAtAvgPrice_sim.py`.

## 1. Purpose

`01_str_topPerformerAtAvgPrice_sim.py` is a new automated trade execution script designed for **simulated trading**. It will adapt the trade criteria from `01_str_topPerformerAtAvgPrice.py` to operate within a simulation environment, leveraging the structure and helper functions found in existing simulation scripts like `02_str_topPerformerCopy_sim.py`.

Its primary function is to:
*   Fetch model performance data.
*   Identify the best signal for the specified product (`gbp`).
*   Check if an open, tradeable trade for that model and signal (originating from this script) already exists.
*   If no such trade exists, evaluate if the `current_price` meets the `avg_profitable_entry_price` condition for the signal.
*   If conditions are met, execute a simulated trade.

## 2. Key Characteristics and Integrated Logic

*   **Base Logic**: Inherits the core trade evaluation logic (comparing `current_price` to `avg_profitable_entry_price`) from `01_str_topPerformerAtAvgPrice.py`.
*   **Simulation Environment**: Adapts to the simulation environment by using `tradedb_sim` and the `execute_trade_sim` endpoint, similar to `02_str_topPerformerCopy_sim.py`.
*   **Configuration**: Will include constants for API endpoints, database name, product to trade, log file, and poll interval.
*   **Dynamic Script Name**: `SCRIPT_NAME` will be dynamically derived and used in `trade_reason` for accurate trade tracking.
*   **Robust Data Fetching**: Utilizes a `fetch_data` helper function with recursive JSON decoding and error handling.
*   **Open Trade Check**: The `has_open_trade` function will ensure that duplicate trades for the same model and signal (from this script) are not opened.
*   **Trade Execution**: Uses `execute_trade_sim` for simulated trade placement.
*   **Logging**: Provides detailed logging for each cycle, including data fetching, signal evaluation, open trade checks, and trade execution outcomes.

## 3. Checklist of Tasks

*   [x] **Create Script File**: Copy `algo_viewer/strategy_library/01_str_topPerformerAtAvgPrice.py` to `algo_viewer/strategy_library/01_str_topPerformerAtAvgPrice_sim.py`.
*   [x] **Update Configuration Constants**:
    *   Modify `LOG_FILE` to `"01_str_topPerformerAtAvgPrice_sim.log"`.
    *   Add `BASE_URL = "http://127.0.0.1:8000/api"`.
    *   Add `DB_NAME = "tradedb_sim"`.
    *   Update `API_ENDPOINT` to `f"{BASE_URL}/vw_106_ModelPerformance_alt"`.
    *   Update `OPEN_TRADES_ENDPOINT` to `f"{BASE_URL}/vwCombined_trades_open"`.
    *   Add `EXECUTE_SIM_TRADE_ENDPOINT = f"{BASE_URL}/execute_trade_sim/"`.
    *   Remove `EXECUTE_TRADE_ENDPOINT` (or comment it out if not used).
    *   Add `POLL_INTERVAL_SEC = 10`.
    *   Remove `SIM_DB_SUFFIX` and `ALT_NET_RETURN_THRESHOLD` and `TOP_N_MODELS` if they exist from the original file (they are not needed for this specific strategy).
*   [x] **Update Imports**: Add `from typing import Any, Dict, Optional, Tuple, Final`.
*   [x] **Refactor `fetch_data`**:
    *   Change signature to `def fetch_data(url: str, *, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:`.
    *   Add `logging.debug(f"Fetching {url} with params={params}")`.
    *   Modify `requests.get(url)` to `requests.get(url, params=params, timeout=10)`.
    *   Update exception handling to `(requests.RequestException, json.JSONDecodeError) as exc:`.
*   [x] **Refactor `get_best_signal_and_price`**:
    *   Change signature to `def get_best_signal_and_price(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[float]]:`.
    *   Update `logging.info("Detected list of JSON strings, parsing each item...")` to `logging.info("Parsing list of JSON strings from signal list …")`.
    *   Remove `try...except` block as `fetch_data` handles it.
*   [x] **Refactor `has_open_trade`**:
    *   Change signature to `def has_open_trade(model_name: str, signal: str) -> bool:`.
    *   Add `logging.debug(f"has_open_trade called for Model='{model_name}', Signal='{signal}'")`.
    *   Modify `filtered_open_trades_url` to construct `params = {"db": DB_NAME, "model": model_name, "signal": signal, "tradeable": 1, "trade_reason": SCRIPT_NAME}`.
    *   Call `fetch_data` with `params`: `open_trades_data = fetch_data(OPEN_TRADES_ENDPOINT, params=params)`.
    *   Update `logging.warning("Open trades API response is missing the 'data' key or is empty.")` to `logging.warning("Open-trades response missing 'data'.")`.
    *   Update `logging.info("Detected list of JSON strings in open trades, parsing each item...")` to `logging.info("Parsing list of JSON strings in open trades …")`.
    *   Modify the loop condition to check `t.get("tradeable", 0) != 0` and `t.get("trade_reason") == SCRIPT_NAME`.
    *   Add detailed `logging.debug` statements for trade checking.
    *   Remove `try...except` block as `fetch_data` handles it.
*   [x] **Refactor `execute_trade`**:
    *   Rename function to `execute_trade_sim`.
    *   Change signature to `def execute_trade_sim(signal_type: str, price: float, model_name: str) -> None:`.
    *   Modify `payload` to include `"reason": SCRIPT_NAME` and `"price": price`.
    *   Modify `requests.post` call to `requests.post(EXECUTE_SIM_TRADE_ENDPOINT, params={"db": DB_NAME}, json=payload, timeout=10)`.
    *   Update `logging.info` message.
    *   Update exception handling to `requests.RequestException as exc:`.
*   [x] **Update `main` function**:
    *   Change `logging.info("Starting standalone trade executor...")` to `logging.info("Standalone trade executor started.")`.
    *   Change `logging.info("--- New Cycle ---")` to `logging.info("— New cycle —")`.
    *   Modify `model_data = fetch_data(API_ENDPOINT)` to `model_data = fetch_data(API_ENDPOINT, params={"db": DB_NAME})`.
    *   Update `best_signal_data, current_price = get_best_signal_and_price(model_data)`.
    *   Update `if not best_signal_data or current_price is None:` to `if not best or price is None:`.
    *   Update `logging.info("No valid signal or price found. Ending cycle.")` to `logging.info("No valid signal found; sleeping.")`.
    *   Update `time.sleep(10)` to `time.sleep(POLL_INTERVAL_SEC)`.
    *   Update `model_name = best_signal_data.get("model")` and `signal = best_signal_data.get("signal")` to use `best`.
    *   Update `logging.warning("Signal data is incomplete. Skipping. Data: %s", best_signal_data)` to `logging.warning("Signal data is incomplete. Skipping. Data: %s", best)`.
    *   Update `logging.info("--- Detailed Evaluation Log ---")` and subsequent `logging.info` lines for clarity.
    *   Update `execute_trade('sell', current_price_float, model_name)` to `execute_trade_sim('sell', price, model_name)`.
    *   Update `execute_trade('buy', current_price_float, model_name)` to `execute_trade_sim('buy', price, model_name)`.
    *   Remove the `try...except` block around price evaluation as `fetch_data` handles errors.
    *   Ensure `time.sleep(POLL_INTERVAL_SEC)` is used consistently.

    ```