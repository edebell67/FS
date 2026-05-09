# Changelog

## V20251225_0255 (2025-12-25)
*   **Syntax Fix:** Corrected a `SyntaxError` in `common.py` (line 1714) caused by a malformed line continuation.
*   **Bug Fix (Price):** Fixed a critical bug in `_manage_virtual_trades` where the price of the last processed product was being incorrectly applied to all new virtual trades (e.g., EUR trades getting AUD/NZD prices). Resulting in `running_multiwindow` now passing a dictionary of all product prices.
*   **Bug Fix (Duplicates):** Implemented a safety check to abort the virtual trade scan cycle if file read errors occur, preventing the accidental creation of hundreds of duplicate "OPEN" trade files.
*   **Enhancement (Configurable Threshold):** Replaced the hardcoded `> 0` PnL threshold for virtual trade promotion with the configurable `profitability_guard.threshold_y` value from `config.json`.
*   **Bug Fix (Logic):** Corrected the initialization of `top_buy_pnl` and `top_sell_pnl` from `-1` to `-infinity` to ensure strategies with negative PnL (but above a negative threshold) are correctly identified.
*   **Bug Fix (Zero Price):** Moved the `_manage_virtual_trades` execution block in `run_multiwindow` to *after* the price update loop, ensuring new trades are created with valid `entry_price` and `current_price` instead of `0.0`.
