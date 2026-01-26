# Plan: Real-Time Trade Selection in Monitor

**Date:** 2025-11-21

This document outlines the plan to modify the `trade_monitor.py` script to allow user selection of active strategies for real-time (RT) trade generation, and to integrate this selection into the `generate_trade_files.py` script.

### 1. Understanding of Requirements

The goal is to enhance the existing `trade_monitor.py` script with a new feature that allows the user to select which "Trade Titles" are active for real-time (RT) trade generation.

1.  **New "RT Trade Selector" Page**: A new menu option will be added to the `trade_monitor.py` main menu. This page will display all unique `Trade Title`s found across both open and closed trades.
2.  **Selection Mechanism**: On this new page, each `Trade Title` will have a status (e.g., `[ACTIVE]` or `[INACTIVE]`). The user will be able to toggle the status of any trade title by selecting it.
3.  **Configuration File**: The list of "ACTIVE" trade titles will be saved to a persistent configuration file (`rt_trade_config.json`). This file will act as the "source of truth" for the trade generation script.
4.  **Integration with `generate_trade_files.py`**: The `generate_trade_files.py` script will be modified to read this new configuration file. It will then only generate TWS JSON files for open trades whose `Trade Title` is on the "ACTIVE" list in the configuration file.

This creates a complete workflow: the user can dynamically enable or disable strategies for real-time execution via the monitor, and the generator will respect those choices.

---

### 2. Detailed Implementation Checklist

This plan is broken into two main phases: modifying the UI (`trade_monitor.py`) and then updating the file generator (`generate_trade_files.py`).

**Phase 1: `trade_monitor.py` Enhancements**

*   [ ] **1.1. Create Configuration Helper Functions:**
    *   In `trade_monitor.py`, create a function `_get_rt_config_path()` to define the location of the new config file (e.g., in the same directory as the script, named `rt_trade_config.json`).
    *   Create `load_rt_config()`: Reads the JSON file and returns a `set` of active trade titles. Handles file-not-found errors by returning an empty set.
    *   Create `save_rt_config(active_titles)`: Takes a `set` of titles and writes it as a JSON list to the config file.

*   [ ] **1.2. Aggregate All Unique Trade Titles:**
    *   In the `TradeLogProcessor` class, create a new method `get_all_unique_trade_titles()`.
    *   This method will iterate through both `self.all_trades['open']` and `self.all_trades['closed']`.
    *   It will collect every unique `Extracted Trade Title` into a `set` to remove duplicates, and then return it as a sorted `list`.

*   [ ] **1.3. Implement the New UI Page (`view_rt_trade_selector`):**
    *   Create a new function `view_rt_trade_selector(processor)`.
    *   This function will contain a loop similar to the other `view_*` functions.
    *   Inside the loop, it will:
        *   Call `processor.get_all_unique_trade_titles()` to get the list of all possible titles.
        *   Call `load_rt_config()` to get the set of currently active titles.
        *   Print a formatted list to the screen, showing each title preceded by either `[ACTIVE]  ` or `[INACTIVE]` based on its presence in the active set.
        *   Prompt the user to "Enter a Trade Title to toggle its status (or 'b' to go back):".
        *   If a valid title is entered, add it to the active set if it's inactive, or remove it if it's active.
        *   After toggling, immediately call `save_rt_config()` to persist the change.
        *   The screen will then refresh to show the updated list.

*   [ ] **1.4. Integrate into the Main Menu:**
    *   In the `main()` function, add a new menu item: `4. Configure Real-Time (RT) Trades`.
    *   Wire this option to call the new `view_rt_trade_selector()` function.
    *   Adjust the other menu numbers accordingly.

**Phase 2: `generate_trade_files.py` Integration**

*   [ ] **2.1. Add Configuration Loading:**
    *   At the top of `generate_trade_files.py`, define the path to the same `rt_trade_config.json` file.
    *   Create a `load_rt_config()` function identical to the one in the monitor, which reads the file and returns a `set` of active titles.

*   [ ] **2.2. Implement Filtering Logic:**
    *   In the `main_loop()` function, call `load_rt_config()` at the *start* of each loop iteration. This ensures it always has the latest user selections.
    *   In the `process_source_file(filepath)` function, after loading the `source_data` from the JSON file:
        *   Extract the `Trade Title` from the `source_data`. 
        *   Add a check: `if trade_title not in active_titles:`.
        *   If the title is not in the active set, print a "Skipping inactive trade..." message and `return False` to prevent the TWS file from being generated.
---
### **Phase 3: UI Enhancements - Export to Excel & Universal Auto-Refresh**

This phase focuses on improving the user experience within the `trade_monitor.py` application by adding data export capabilities and making all data pages auto-refresh.

*   [ ] **3.1. Add New Dependencies:**
    *   The script will use the `pandas` and `openpyxl` libraries to create Excel files. A comment will be added indicating that the user needs to install them (e.g., `pip install pandas openpyxl`).

*   [ ] **3.2. Create Export Directory:**
    *   The `main()` function will be updated to automatically create an `exports` subdirectory in the same location as the script, ensuring a dedicated place for all exported files.

*   [ ] **3.3. Implement Core Export Functionality:**
    *   A new helper function, `export_to_excel(data, headers, view_name)`, will be created.
    *   **Function Logic**: This function will take the data currently displayed on the screen, convert it into a pandas DataFrame, generate a descriptive filename including the view name and a timestamp (e.g., `summary_by_title_20251121_150000.xlsx`), and save it as an `.xlsx` file in the `exports` directory.

*   [ ] **3.4. Integrate "Export" into all UI Views:**
    *   The user prompts in `view_trade_names_summary`, `view_position_summary`, and `view_individual_trades` will be updated to include an `'e' to export` option.
    *   An `elif` block will be added to each view's input handling to call the `export_to_excel` function with the currently displayed data when the user selects 'e'.

*   [ ] **3.5. Enable Auto-Refresh on "Closed" Trade Pages:**
    *   The logic in `view_trade_names_summary`, `view_position_summary`, and `view_individual_trades` will be refactored.
    *   The standard `input()` call currently used for the "closed" trade views will be replaced with the non-blocking `_get_input_with_timeout()` function that is already used for the "open" trade views.
    *   If the timeout occurs (the user does not enter any key), the script will automatically call `processor.reload_all_trades()` and refresh the current screen, creating a consistent auto-refresh experience across all pages.

*   [ ] **3.6. Implement Numbered Selection for "Trade Title Summary" Views:**
    *   In the `view_trade_names_summary` function, modify the display of `summary_data` to include a unique number (`No.`) next to each trade title.
    *   Update the `headers` list passed to `print_table` to include `'No.'`.
    *   Change the user prompt to ask for a number to select a trade title for details.
    *   Modify the input handling logic to parse the user's numeric input and map it to the corresponding `Trade Title` from the `summary_data` list.
---
### **Phase 4: Global "Go-To" Navigation**

This phase refactors the application's navigation to allow users to jump directly between primary pages using unique numeric identifiers, rather than navigating hierarchically.

*   [ ] **4.1. Define Page Navigation Constants:**
    *   At the top of `trade_monitor.py`, create constants for each primary page (e.g., `PAGE_MAIN_MENU = 0`, `PAGE_OPEN_TRADES_SUMMARY = 1`, `PAGE_CLOSED_TRADES_SUMMARY = 2`, `PAGE_RT_CONFIG = 3`).
    *   Create a dictionary mapping these constants to user-friendly page titles for display in prompts.

*   [ ] **4.2. Create a Central Navigation Router Function:**
    *   Implement `handle_navigation(choice, processor)`:
        *   Takes user input `choice` and `processor` object.
        *   If `choice` is a valid global navigation number, calls the corresponding `view_*` function and returns `True`.
        *   If `choice` is not a global navigation number, returns `False`.

*   [ ] **4.3. Refactor the Main Application Loop (`main` function):**
    *   Simplify the `main` loop to primarily act as a dispatcher.
    *   After displaying the main menu and getting `choice`, pass `choice` to `handle_navigation`.
    *   If `handle_navigation` returns `True`, continue the main loop. Otherwise, handle local `main` menu choices ('q', '3', '4').

*   [ ] **4.4. Update All View Functions (`view_*`):**
    *   In `view_trade_names_summary`, `view_position_summary`, `view_individual_trades`, and `view_rt_trade_selector`:
        *   Modify input prompts to include global navigation instructions (e.g., "Enter # for details, or jump to: [1] Open Summary, [2] Closed Summary, [3] RT Config, [0] Main Menu").
        *   In the input handling loop, first attempt to process the input via `handle_navigation`.
        *   If `handle_navigation` returns `True`, immediately `return` from the current view function to transfer control to the new page.
        *   If `handle_navigation` returns `False`, proceed with the local page's existing logic (drill-down, export, 'b', 'q').

*   [ ] **4.5. Standardize Return Values:**
    *   Ensure all `view_*` functions consistently return a value (e.g., `RETURN_TO_MAIN`, `QUIT_APP`, `None` for local action) that the calling loop can interpret.
    *   The new `handle_navigation` should also return the chosen page constant (or `None` if local action).