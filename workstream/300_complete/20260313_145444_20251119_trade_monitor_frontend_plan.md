# Gemini Coder - Plan for Trade Monitor Front-end

This document outlines the plan to create a terminal-based front-end application for monitoring trade performance from JSON log files.

## 1. Understanding of Requirements

The user requires a "bare metal front end that has a terminal screen look and feel" to display trade data from JSON log files located in `@Trades\Trades\json_logs\open_trades\` and `@Trades\Trades\json_logs\closed_trades\`.

The application must:
1.  **List Trade Names:** Display a list of unique "Trade Title" values found in the JSON log files.
2.  **Summarize P&L:** For each unique trade name, show the total "Net P&L ($)" and "Alt Net ($)".
3.  **Group by Status:** Separate summaries into "Open Trades" and "Closed Trades" based on the presence of "Exit Time" (implied by file location: `open_trades` vs `closed_trades`).
4.  **Signal-based Summary (Position Summary):** Allow viewing summarized data (total Net P&L and Alt Net P&L) grouped by "Position" (e.g., BUY/SELL) for a selected trade name.
5.  **Drill-down Capability:** From the signal-based summary, enable drilling down to view individual trades that contribute to that summary item.

## 2. Refined Plan of Approach

The application will be a single Python script (`trade_monitor.py`) that uses standard console I/O for its interactive terminal interface.

### 2.1. `trade_monitor.py` (Main Application File)

This will be the entry point for the application, orchestrating data processing and UI.

### 2.2. `TradeLogProcessor` Class

This class will handle file system interaction, JSON parsing, and data aggregation.

*   **`__init__(self, log_directory)`**:
    *   Initializes with the base path to the `json_logs` directory (e.g., `@Trades\Trades\json_logs`).
    *   Internal storage for parsed trade data.
*   **`_load_trades(self, trade_type)`**:
    *   Takes `trade_type` (e.g., 'open', 'closed') as input.
    *   Scans the corresponding subdirectory (`open_trades` or `closed_trades`).
    *   Reads and parses all `*.json` files.
    *   Stores trade data, enhancing it with a `filename` and `trade_type` for later use.
*   **`load_all_trades(self)`**:
    *   Calls `_load_trades` for both 'open' and 'closed' types.
*   **`get_all_trades(self)`**:
    *   Returns all loaded trade data.
*   **`get_trade_names_summary(self, trade_type)`**:
    *   Takes `trade_type` ('open' or 'closed').
    *   Aggregates trades by 'Trade Title'.
    *   Calculates the sum of "Net P&L ($)" and "Alt Net ($)" for each unique trade title.
    *   Returns a list of dictionaries, each containing 'Trade Title', 'Total Net P&L ($)', and 'Total Alt Net ($)'.
*   **`get_position_summary(self, trade_name, trade_type)`**:
    *   Takes a specific `trade_name` and `trade_type`.
    *   Aggregates trades (filtered by `trade_name`) by 'Position' (BUY/SELL).
    *   Calculates the sum of "Net P&L ($)" and "Alt Net ($)" for each position.
    *   Returns a list of dictionaries, each containing 'Position', 'Total Net P&L ($)', and 'Total Alt Net ($)'.
*   **`get_individual_trades(self, trade_name, position, trade_type)`**:
    *   Takes `trade_name`, `position`, and `trade_type`.
    *   Returns a list of individual trade dictionaries matching these criteria.
*   **`_extract_trade_info_from_filename(self, filename)`**:
    *   Helper function to parse the `Trade Title` and `Trade No.` from filenames (e.g., `trade_AUD_TPUSD251_TLUSDneg65_period2_buffer0.0001_No1.json`).

### 2.3. Main Application Loop & UI Rendering

This part will be implemented directly within `trade_monitor.py`.

*   **Initialization**: Create an instance of `TradeLogProcessor`.
*   **Main Menu**: Present options to the user:
    *   "1. View Open Trades Summary"
    *   "2. View Closed Trades Summary"
    *   "q. Quit"
*   **Trade Name Summary View**:
    *   When '1' or '2' is selected, display the summary of trade names with their total P&L.
    *   Allow the user to select a `trade_name` for further detail.
*   **Position Summary View**:
    *   When a `trade_name` is selected, display the summary by 'Position' (BUY/SELL) for that trade.
    *   Allow the user to select a 'Position' for drilling down to individual trades.
*   **Individual Trades View**:
    *   When a 'Position' is selected, display a list of all individual trades matching the criteria.
    *   Provide an option to go back to the previous view.
*   **Console Output**: Use formatted `print()` statements to create a clean, readable terminal output with clear headings and tables.

## 3. List of Changes

*   **`trade_monitor.py`**:
    *   [ ] Create the `trade_monitor.py` file.
    *   [ ] Implement the `TradeLogProcessor` class including its methods.
    *   [ ] Implement the main interactive loop.
    *   [ ] Implement helper functions for UI rendering (e.g., `_print_table`, `_clear_screen`).
    *   [ ] Add necessary imports (`os`, `json`, `re`, `collections`).

## 4. Example Data Structure for Trade Summary

```json
[
    {
        "Trade Title": "AUD_TPUSD251_TLUSDneg65_period2_buffer0.0001",
        "Total Net P&L ($)": -265.0,
        "Total Alt Net ($)": 185.0
    },
    {
        "Trade Title": "EUR_TPUSD225_TLUSDneg66_period2_buffer0.0001",
        "Total Net P&L ($)": 80.0,
        "Total Alt Net ($)": -140.0
    }
]
```

## 5. Example Data Structure for Position Summary

```json
[
    {
        "Position": "SELL",
        "Total Net P&L ($)": -130.0,
        "Total Alt Net ($)": 90.0
    },
    {
        "Position": "BUY",
        "Total Net P&L ($)": -70.0,
        "Total Alt Net ($)": 50.0
    }
]
```
