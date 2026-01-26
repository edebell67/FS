# Gemini Coder - Plan for 03_str_topPerformerAtPriceSpread.py Enhancement

This document outlines the new trade triggering logic for `03_str_topPerformerAtPriceSpread.py`.

## 1. Understanding of Requirements

The primary function of `03_str_topPerformerAtPriceSpread.py` has been updated. Previously, it used a price-based condition to trigger trades. This has been replaced with a new condition, and the script now considers multiple top-performing models:

*   The script identifies the top `TOP_N_MODELS` (configurable, default 3) based on their `total_return`.
*   For each of these top model/signal pairs, a trade will be placed if there exists *any* open trade with an `alt_net_return` value less than a predefined threshold (`ALT_NET_RETURN_THRESHOLD`, default -100).
*   The `has_open_trade` function now includes a check for `trade.get('trade_reason') == SCRIPT_NAME`, ensuring that only trades originating from the same script are considered when determining if an open trade exists.

This means the script no longer considers `fx_midprice` or `avg_profitable_entry_price` for trade execution.

## 2. Implemented Changes

*   **`algo_viewer/strategy_library/03_str_topPerformerAtPriceSpread.py`**:
    *   **Added Constants**: `ALT_NET_RETURN_THRESHOLD: Final[int] = -100` and `TOP_N_MODELS: Final[int] = 3` were added to the configuration section.
    *   **Renamed and Modified `get_best_signal_and_price`**: This function was renamed to `get_top_n_signals_and_prices` and updated to return a list of the top `TOP_N_MODELS` signals, sorted by `total_return`.
    *   **Modified `main()` function**:
        *   The existing price-based trade evaluation `try...except` block was removed.
        *   The loop now iterates through the list of top N signals returned by `get_top_n_signals_and_prices`.
        *   For each model/signal pair, it performs the `has_open_trade` check.
        *   It then fetches all open trades for the current `model_name` and `signal` (without the `tradeable!=0` filter in the URL, as `alt_net_return` of all trades needs to be inspected).
        *   It iterates through these trades and checks if `trade.get('alt_net_return', 0) < ALT_NET_RETURN_THRESHOLD`.
        *   If the condition is met, `execute_trade(signal, current_price, model_name)` is called.
        *   Logging messages were adjusted to reflect the evaluation of multiple models and the new trade triggering criteria.
    *   **Modified `has_open_trade` function**: The `if` condition now includes `trade.get('trade_reason') == SCRIPT_NAME` to ensure that only trades originating from the same script are considered as existing open trades.
    *   **Modified `execute_trade` function**: The `trade_reason` in the `payload` was changed to `SCRIPT_NAME` to dynamically reflect the script's origin.

## 3. Verification

*   The script should now consider the top N models based on `total_return`.
*   Trades should only be placed if an open trade for that model/signal has an `alt_net_return` below the defined threshold.
*   The `has_open_trade` function should correctly identify existing trades from the same script.
*   The `trade_reason` for new trades should reflect the script's filename.