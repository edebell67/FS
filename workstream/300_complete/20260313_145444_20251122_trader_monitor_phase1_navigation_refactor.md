# Gemini Coder - Plan for `trade_monitor.py` Enhancements (Phase 1 & Navigation Refactor)

This document outlines the current state and the plan for integrating the SIM API feature's configuration management into `trade_monitor.py`, along with a refactor of the main navigation loop to handle dynamic page arguments.

## 1. Current Status (as of 2025-11-22)

*   **Typo Fix**: The typo `trade_title_title_raw` in `_extract_trade_info_from_filename` has been corrected to `trade_title_raw`.
*   **Global Navigation Prompts**: All `nav_options_str` and `q` handling in `view_rt_trade_selector`, `view_trade_names_summary`, `view_position_summary`, and `view_individual_trades` are correctly implemented, allowing for proper global navigation between pages.
*   **Main Configuration Functions**: New helper functions `_get_main_config_path()`, `load_main_config()`, and `save_main_config()` have been added to `trade_monitor.py` to manage a `config.json` file, primarily for the `trader_mode` setting.
*   **`view_rt_trade_selector` Update**: This function has been updated to load and display the current `trader_mode`, and provides a numbered option to toggle it between "live" and "sim", saving the change to `config.json`.

## 2. Phase 1: Configuration Management (SIM API Feature) - Next Steps

The next crucial step is to refactor the `main` function to dynamically handle the return values of view functions. This is necessary because some view functions (`view_rt_trade_selector`, `view_trade_names_summary`, `view_position_summary`, and `view_individual_trades`) now return a tuple containing both the next page identifier and a dictionary of arguments for that page.

### 2.1. Plan of Approach for `main` function Refactor

The `main` function will be updated to correctly interpret the new return format from the view functions.

1.  **Load `main_config`**: Load the main configuration at the beginning of the `main` loop to access `trader_mode`.
2.  **Display `trader_mode`**: Show the current `trader_mode` in the main menu header.
3.  **Handle Tuple Returns**: Modify the `elif` blocks for page navigation to unpack the `(next_page_id, page_args)` tuple.
4.  **Dynamic Function Calls**: When `next_page` is a callable (i.e., a function reference), call it with the `page_args`.
5.  **Break from loop**: The `main` loop should correctly break when `PAGE_QUIT` is returned.

### 2.2. List of Changes for `main` function

*   **`Trades/trade_monitor/trade_monitor.py`**:
    *   [ ] In `main()`:
        *   Load `main_config` using `load_main_config()` at the start.
        *   Display `current_trader_mode` in the main menu.
        *   Modify the `elif` blocks for `PAGE_OPEN_TRADES_SUMMARY`, `PAGE_CLOSED_TRADES_SUMMARY`, and `PAGE_RT_CONFIG` to correctly handle the tuple return from their respective view functions.
        *   Add `elif callable(current_page):` block to dynamically call view functions that return a function reference with `page_args`.
        *   Ensure the `while` loop correctly breaks on `PAGE_QUIT`.

This refactoring will make the navigation flow more robust and allow for passing dynamic data between different UI views.
