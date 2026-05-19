# Implementation Plan: RT Trade Filter UI
**Version:** 20251127_01
**Date:** 2025-11-27
**Description:** Implementation of the User Interface for Per-Title Trade Filter Allocation in `trade_monitor.py`.

## 1. Requirement
Implement a UI in the Trade Monitor console application to allow users to assign specific trade filters (e.g., `prev_closed_same_signal_alt_net_negative`) to specific trade titles. This UI must interact with the backend logic implemented in `simple_trend_trader.py` via the `trade_filter_allocations.json` file.

## 2. Plan of Approach
1.  **Define UI Constants**: Add a new page ID (`PAGE_RT_TRADE_FILTER`) and update navigation maps (`PAGE_TITLES_MAP`, `MAIN_MENU_ORDER`, `GLOBAL_NAV_ORDER`) in `trade_monitor.py`.
2.  **Implement Helper Functions**: Create functions in `trade_monitor.py` to:
    *   Load/Save `trade_filter_allocations.json`.
    *   Get available filters from `config.json`.
3.  **Implement Page Logic**: Create `show_rt_trade_filter_page(processor)` to:
    *   Display a list of active trade titles.
    *   Allow selecting a title.
    *   Display available filters with checkboxes for the selected title.
    *   Provide commands to toggle filters, save changes, clear filters, and apply to all.
4.  **Integrate into Main Loop**: Update the `page_dispatch_map` and main loop in `trade_monitor.py` to route to the new page.
5.  **Update Version**: Update `VERSION` in `algo_viewer/tradepanel/constants.py`.

## 3. Checklist of Changes

### `Trades/trade_monitor/trade_monitor.py`
- [x] Added `PAGE_RT_TRADE_FILTER` constant (ID 7).
- [x] Updated `PAGE_TITLES_MAP` with "RT Trade Filter Management".
- [x] Added `PAGE_RT_TRADE_FILTER` to `MAIN_MENU_ORDER` and `GLOBAL_NAV_ORDER`.
- [x] Added helper functions:
    - [x] `_get_trade_filter_allocations_path()`
    - [x] `load_trade_filter_allocations()`
    - [x] `save_trade_filter_allocations()`
    - [x] `get_available_filters()`
- [x] Implemented `show_rt_trade_filter_page(processor)` function with full UI logic.
- [x] Added `PAGE_RT_TRADE_FILTER` to `page_dispatch_map`.
- [x] Updated main loop to pass `processor` to the new page.

### `algo_viewer/tradepanel/constants.py`
- [x] Updated `VERSION` to `20251127_01`.

## 4. Verification
- [x] Verify that the new page is accessible from the main menu.
- [x] Verify that trade titles are listed correctly.
- [x] Verify that filters can be toggled for a specific title.
- [x] Verify that "Save" writes to `trade_filter_allocations.json`.
- [x] Verify that "Apply to All" updates all titles in memory and saves.
- [x] Verify that "Clear" removes filters for the selected title.
- [x] Verify that navigation back to the main menu works.

## 5. Notes
- The UI uses a "Select Title -> Edit Filters" flow which is suitable for the console interface.
- Filters are loaded from `config.json` (`available_filters`), ensuring a single source of truth for filter definitions.
