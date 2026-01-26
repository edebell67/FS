# Implementation Plan: Connect Filters to Trade Generation
**Date:** 2025-11-27
**Description:** Connected the Per-Title Trade Filter system to the TWS Trade Generation process (`generate_trade_files.py`).

## 1. Requirement Analysis
The user requested that the trade filter process (managed via `trade_monitor.py` and stored in `trade_filter_allocations.json`) be connected to the `generate_trade_files.py` script. 

**Core Problem:** 
Previously, the filter logic was only present in `simple_trend_trader.py`. If a trade was logged (either because the filter was disabled there or bypassed), `generate_trade_files.py` would blindly pick it up and send it to TWS for execution.

**Goal:** 
Establish `generate_trade_files.py` as the final "Gatekeeper". It must independently verify that a trade passes all assigned filters before generating a TWS order. This provides a robust safety layer: even if a trade appears in the logs, it won't be executed if it violates the filter rules.

## 2. Technical Challenges & Solutions

### Challenge 1: Path Dependency in `filters.py`
*   **Issue:** `filters.py` used relative paths (`Trades/json_logs/...`). When imported by `generate_trade_files.py` (which sits in `Trades/generate_RT/`), these relative paths would resolve incorrectly, causing the filter to fail finding historical data.
*   **Solution:** Modified `filters.py` to use **absolute paths** derived from `__file__`.
    ```python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OPEN_TRADES_FOLDER = os.path.join(BASE_DIR, "Trades", "json_logs", "open_trades")
    ```
    *Rationale:* This makes the `filters` module portable and safe to import from any subdirectory.

### Challenge 2: Importing Modules from Parent Directory
*   **Issue:** `generate_trade_files.py` is in a subdirectory (`generate_RT`) and needs to import `filters.py` from the parent (`Trades`) directory. Python does not allow this by default.
*   **Solution:** Used `sys.path.append` to add the parent directory to the search path.
    ```python
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import filters
    ```
    *Rationale:* While a package structure is cleaner, this script is often run standalone. Modifying `sys.path` is the most reliable way to ensure it finds its dependencies without requiring complex environment setup.

### Challenge 3: Accessing Filter Allocations
*   **Issue:** The mapping of "Which trade gets which filter" is stored in `trade_filter_allocations.json` in the parent directory.
*   **Solution:** Added logic to `generate_trade_files.py` to locate and read this JSON file directly.
    *   Defined `TRADE_FILTER_ALLOCATIONS_FILE` pointing to the parent directory.
    *   Implemented `load_trade_filter_allocations()` to parse it.

## 3. Implementation Details

### A. `Trades/filters.py`
*   **Change:** Updated `OPEN_TRADES_FOLDER` and `CLOSED_TRADES_FOLDER` to use `os.path.abspath`.

### B. `Trades/generate_RT/generate_trade_files.py`
*   **Imports:** Added `sys` and `filters`.
*   **Logic Injection:** Inside `process_source_file`, inserted the filter check immediately after the trade title validation.
    ```python
    # 20251127_01 - Apply Per-Title Filters
    if filters:
        allocations = load_trade_filter_allocations()
        title_filters = allocations.get(base_trade_title, [])
        if title_filters:
            if not filters.apply_filters(source_data, title_filters):
                print(f"Skipping trade due to active filter: {base_trade_title}")
                return False, True # Skip generation, but mark as processed
    ```

## 4. Resulting Workflow
1.  **Configuration**: User assigns filters (e.g., `prev_closed_same_signal_alt_net_negative`) to a trade title via the Trade Monitor UI.
2.  **Logging**: `simple_trend_trader.py` runs. It *may* or *may not* filter the trade log creation (depending on its own config).
3.  **Execution Gatekeeper**: `generate_trade_files.py` detects a new log file.
    *   It looks up the filters for that trade title.
    *   It re-runs the filter logic against the trade data.
    *   **If Filter Fails**: The TWS order is **BLOCKED**. The script logs "Skipping trade due to active filter".
    *   **If Filter Passes**: The TWS order is generated in `trades_rt2/order`.

## 5. Verification
*   **Import Test**: Verified `filters` can be imported from the subdirectory.
*   **Config Read**: Verified `generate_trade_files.py` can find and read `trade_filter_allocations.json`.
*   **Logic Check**: Confirmed that the `apply_filters` call is correctly placed to intercept the trade before the `json.dump` to the TWS folder.
