# Gemini Coder - Plan for 04_str_topPerformerByCount_sim.py Function

This document outlines the function and key characteristics of the new simulation strategy script: `04_str_topPerformerByCount_sim.py`.

## 1. Purpose

`04_str_topPerformerByCount_sim.py` is a new automated trade execution script designed for **simulated trading**. It will leverage the existing simulation structure (from `01_str_topPerformerAtAvgPrice_sim.py`) and implement a new trade criteria based on the profitability count and sum of `alt_net_return` from recently closed trades.

Its primary function is to:
*   Fetch recently closed trades from the API.
*   Analyze these trades to determine profitable buy and sell counts and their respective `alt_net_return` sums.
*   Apply specific buy/sell criteria based on these counts and sums.
*   Execute simulated trades if criteria are met, respecting existing open trade checks.

## 2. Key Characteristics and Integrated Logic

*   **Base Structure**: Will be copied from `01_str_topPerformerAtAvgPrice_sim.py` to ensure consistency with the simulation environment setup, logging, and helper functions (`fetch_data`, `has_open_trade`, `execute_trade_sim`).
*   **Configuration**:
    *   `LOG_FILE`: Specific log file for this strategy.
    *   `CLOSED_TRADES_ENDPOINT`: API endpoint for closed trades.
    *   `RECENT_TRADES_LIMIT`: Configurable variable for the number of most recently created closed trades to fetch (default: 50).
*   **Trade Criteria**:
    *   **Open Trades Check**: Will use the existing `has_open_trade` function.
    *   **Data Processing**: A new function will be introduced to fetch and process closed trades, calculating `buy_profit_count`, `sell_profit_count`, `sum_buy_alt_net_return`, and `sum_sell_alt_net_return`, along with the latest profitable buy and sell trades.
    *   **Buy Criteria**: `buy_profit_count > sell_profit_count` AND `sum_buy_alt_net_return > sum_sell_alt_net_return`.
    *   **Sell Criteria**: `buy_profit_count < sell_profit_count` AND `sum_buy_alt_net_return < sum_sell_alt_net_return`.
*   **Trade Execution**: Uses the existing `execute_trade_sim` function, using the `model`, `signal`, and `live_forex_price`.
*   **Logging**: Detailed logging for data fetching, trade analysis, and decision-making.

## 3. Checklist of Tasks

*   [x] **Create Script File**: Copy `algo_viewer/strategy_library/01_str_topPerformerAtAvgPrice_sim.py` to `algo_viewer/strategy_library/04_str_topPerformerByCount_sim.py`.
*   [x] **Update Configuration Constants**:
    *   Modify `LOG_FILE` to `"04_str_topPerformerByCount_sim.log"`.
    *   Add `CLOSED_TRADES_ENDPOINT = f"{BASE_URL}/vwCombined_trades_closed"`.
    *   Add `RECENT_TRADES_LIMIT: Final[int] = 50`.
    *   Remove `API_ENDPOINT` (as we will not be using `vw_106_ModelPerformance_alt` for this strategy).
*   [x] **Remove Unused Functions**:
    *   Remove `get_best_signal_and_price` function.
*   [x] **Implement `analyze_closed_trades` Function**:
    *   Create a new function `analyze_closed_trades(limit: int) -> Tuple[int, int, float, float, Optional[Dict[str, Any]], Optional[Dict[str, Any]]]`. 
    *   This function will:
        *   Fetch data from `CLOSED_TRADES_ENDPOINT` with `limit`, `db=DB_NAME`, `product=PRODUCT_TO_TRADE`, **and sorted by `timestamp` in descending order**.
        *   **Add logging to print the raw `closed_trades_data` received from the API.**
        *   Initialize `buy_profit_count`, `sell_profit_count`, `sum_buy_alt_net_return`, `sum_sell_alt_net_return` to 0.
        *   Initialize `latest_profitable_buy_trade` and `latest_profitable_sell_trade` to `None`.
        *   Iterate through the fetched trades (which are already sorted by creation time, newest first, due to the API endpoint).
        *   For each trade:
            *   **Add logging to print the `model`, `signal`, `alt_net_return`, and `timestamp` of each trade as it's being processed.**
            *   Check if `alt_net_return > 0`.
            *   If profitable:
                *   If `trade.get('signal') == 'buy'`: increment `buy_profit_count`, add `alt_net_return` to `sum_buy_alt_net_return`. If `latest_profitable_buy_trade` is `None`, set it to the current `trade`.
                *   **Add logging to indicate when `latest_profitable_buy_trade` is set.**
                *   If `trade.get('signal') == 'sell'`: increment `sell_profit_count`, add `alt_net_return` to `sum_sell_alt_net_return`. If `latest_profitable_sell_trade` is `None`, set it to the current `trade`.
                *   **Add logging to indicate when `latest_profitable_sell_trade` is set.**
        *   Return the four calculated values, plus `latest_profitable_buy_trade` and `latest_profitable_sell_trade`.
*   [x] **Implement `clean_recently_placed_trades` Function**:
    *   Create a new function `clean_recently_placed_trades(recently_placed_trades: set) -> None`.
    *   This function will:
        *   Iterate through `recently_placed_trades`.
        *   For each `(model, signal)` pair, check if it's still an open trade in the API (using `OPEN_TRADES_ENDPOINT` and `fetch_data`).
        *   If not found as open, remove it from `recently_placed_trades`.
*   [x] **Update `main` Function Logic**:
    *   Initialize `recently_placed_trades = set()` to store `(model_name, signal)` of trades placed in the current session.
    *   Call `clean_recently_placed_trades(recently_placed_trades)` at the beginning of each cycle.
    *   Fetch `live_forex_price` from `FOREX_PRICES_ENDPOINT` by looking up `code` and calculating mid-price from `bid` and `ask`.
    *   Call `analyze_closed_trades(RECENT_TRADES_LIMIT)` to get all six return values.
    *   **Buy Criteria**:
        *   `if buy_profit_count > sell_profit_count and sum_buy_alt_net_return > sum_sell_alt_net_return:`
        *   Inside the `if` block:
            *   Check `if latest_profitable_buy_trade:`.
            *   Set `model_name = latest_profitable_buy_trade.get('model')`.
            *   Call `execute_trade_sim('buy', model_name, live_forex_price)`.
            *   Add `(model_name, signal)` to `recently_placed_trades` after successful execution.
            *   Add logging for the selected trade details.
    *   **Sell Criteria**:
        *   `elif buy_profit_count < sell_profit_count and sum_buy_alt_net_return < sum_sell_alt_net_return:`
        *   Inside the `elif` block:
            *   Check `if latest_profitable_sell_trade:`.
            *   Set `model_name = latest_profitable_sell_trade.get('model')`.
            *   Call `execute_trade_sim('sell', model_name, live_forex_price)`.
            *   Add `(model_name, signal)` to `recently_placed_trades` after successful execution.
            *   Add logging for the selected trade details.
    *   Ensure `has_open_trade` is still used before executing any trade. This will now use the `model_name` derived from the latest trade.
    *   Adjust logging messages to reflect the new criteria.
    *   Ensure `time.sleep(POLL_INTERVAL_SEC)` is used consistently.
*   [x] **Modify `has_open_trade` function**:
    *   Add `recently_placed_trades: set` as a parameter.
    *   Before making the API call to `vwCombined_trades_open`, check if `(model_name, signal)` exists in `recently_placed_trades`. If it does, immediately return `True`.
