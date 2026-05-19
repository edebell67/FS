# Gemini Coder - Plan for Multi-Product Support in Breakout Strategy

This document outlines the plan to modify the breakout trading system to support multiple trade products specified in `config.json`.

## 1. Understanding of Requirements

The current breakout trading system in `breakout.py` (located in `C:\Users\edebe\eds\TradeApps\breakout`) is designed to run for a single trade product. The user wants to extend this functionality to support multiple products, where the list of products is defined in `config.json` (located in `C:\Users\edebe\eds\TradeApps\breakout`).

## 2. Plan of Approach

The core modification will involve changing how `trade_product` is handled. Instead of a single string, it will become a list of strings. The `run_multiwindow` function (in `C:\Users\edebe\eds\TradeApps\breakout\common.py`) will be updated to iterate through this list of products, effectively running a separate set of strategy processors for each product.

## 3. List of Changes

*   **`C:\Users\edebe\eds\TradeApps\breakout\common.py`**:
    *   **[ ] Update `_load_config()`**: Modify the default `config.json` dictionary in the `except` block of the `_load_config` function to include a new key `"trade_products": ["gbp"]`. This ensures a default multi-product setup if `config.json` is missing. **(Note: My previous inspection showed this might already be present in your `common.py`. I will verify again before attempting this change.)**
    *   **[ ] Modify Global Constants**:
        *   Change the constant `DEFAULT_TRADE_PRODUCT` to `DEFAULT_TRADE_PRODUCTS`.
        *   Load `DEFAULT_TRADE_PRODUCTS` as a list from `CONFIG.get('trade_products', ['gbp'])`.
        *   Implement logic to override this list with products specified in the `BREAKOUT_TRADE_PRODUCT` environment variable (comma-separated), if present.
    *   **[ ] Modify `run_multiwindow()` function signature**:
        *   Change the `trade_product: str` parameter to `trade_products: List[str]`.
    *   **[ ] Implement Product Iteration in `run_multiwindow()`**:
        *   Introduce an outer loop that iterates over each `product` in the `trade_products` list.
        *   Inside this loop, the existing logic for iterating over `WINDOW_SIZES` and instantiating `strategy_cls` will remain, but `product` will be passed as the `trade_product` argument to the `strategy_cls` constructor.
    *   **[ ] Update Print Statements in `run_multiwindow()`**: Adjust print statements to reflect that the strategy is running for a specific `product`.
    *   **[ ] Modify `fetch_latest_quotes()`**: Ensure this function correctly handles fetching quotes for a single `trade_product` as it will be called for each product within the iteration. (No direct change needed in signature, as it already accepts `trade_product: str`).

*   **`C:\Users\edebe\eds\TradeApps\breakout\breakout.py`**:
    *   **[ ] Modify `parse_args()`**: Remove the `--trade-product` command-line argument definition, as product selection will now be managed via `config.json` and `DEFAULT_TRADE_PRODUCTS` from `common.py`.
    *   **[ ] Update `if __name__ == '__main__':` block**:
        *   Change the call to `run_multiwindow()` to pass `DEFAULT_TRADE_PRODUCTS` (the new list constant from `common.py`) instead of `args.trade_product`.

## 4. Verification

*   Run the `breakout.py` script.
*   Verify that the console output shows strategies being initialized and running for all products specified in `config.json` (or the default `gbp` if no config).
*   Check the generated trade JSON files to ensure they are created correctly for each product.

## 5. Versioning (Important Note)

*   I will **not** assign a version number. Please explicitly tell me if a `Constants.py` file or similar mechanism for versioning exists and its location, and how you would like me to update it. Otherwise, this item will remain pending.
