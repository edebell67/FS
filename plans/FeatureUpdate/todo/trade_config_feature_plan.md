### Plan: Trade Configuration Management Feature

**Objective:** Overhaul the startup process of `simple_trend_trader.py` to use a `config_trade.json` file for saving, loading, and managing multiple trade strategy parameters.

**Part 1: Create the Plan Document**

*   `[ ]` Create a new document at `C:\Users\edebe\eds\plans\FeatureUpdate\trade_config_feature_plan.md` containing this checklist.

**Part 2: Implement Configuration File Management (`simple_trend_trader.py`)**

*   `[ ]` Define a new global constant for the path to `config_trade.json`.
*   `[ ]` Create a new helper function `load_trade_configs()` to read `config_trade.json` and return a dictionary of saved trade configurations. It will handle cases where the file doesn't exist.
*   `[ ]` Create a new helper function `save_trade_configs(configs)` to write the dictionary of trade configurations back to the `config_trade.json` file.

**Part 3: Overhaul the Script's Startup and UI (`simple_trend_trader.py`)**

*   `[ ]` Create a new primary function, `select_or_create_trade_config()`, that will replace the existing call to `get_user_inputs()` in the main simulation. This new function will perform the following:
    1.  Call `load_trade_configs()` to get all saved strategies.
    2.  Display a numbered list of saved `TRADE_TITLE`s to the user.
    3.  Provide an option for the user to "[N] Create a New Trade Strategy".
    4.  Prompt the user for their choice.
*   `[ ]` **Logic for "Select Existing Strategy":**
    *   If the user picks a number from the list, retrieve the corresponding parameters (`PRODUCT_SYMBOL`, `PRICE_CACHE_SIZE`, `BUFFER_X`, etc.).
    *   **Crucially, check if this trade is already active** by looking for a corresponding file in the `open_trades` directory.
    *   If the trade is active, print a message and exit the script gracefully.
    *   If the trade is *not* active, load the saved parameters into the script's global variables to be used for the run.
*   `[ ]` **Logic for "Create New Strategy":**
    *   If the user chooses to create a new one, call the original `get_user_inputs()` function to get the parameters interactively.
    *   After the new parameters are entered and a `TRADE_TITLE` is generated, add this new strategy configuration to the main dictionary of configs.
    *   Call `save_trade_configs()` to persist the newly created strategy to `config_trade.json`.
*   `[ ]` **Modify `run_trading_simulation()`:**
    *   Replace the original call to `get_user_inputs()` with a call to the new `select_or_create_trade_config()` function.
    *   The rest of the `run_trading_simulation` function will then proceed using the parameters selected or created by the user.
