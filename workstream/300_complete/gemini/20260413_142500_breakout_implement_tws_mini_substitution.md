# Task: Implement Mini-Product Substitution for TWS Trading

## 1. Understanding of Requirements
Implement a symbolic substitution layer at the point of trade execution. If a product is configured for "mini" trading, the symbol sent to Interactive Brokers (TWS) should be replaced with its micro/mini equivalent (e.g., ES -> MES). This should be driven by configuration and apply specifically to the execution phase.

## 2. Plan of Approach
1.  **Update Configuration (`TradeApps/breakout/fs/config.json`)**:
    *   [x] Add `trade_mini_config` containing `enabled_products` (list) and `symbol_map` (mapping).
2.  **Modify Execution Engine (`algo_forex/tws_monitor_and_trade2.py`)**:
    *   [x] Load the mini configuration from `config.json`.
    *   [x] In `process_trade_file`, check the incoming trade symbol.
    *   [x] If the product is enabled for mini trading, swap the `symbol` in the trade dictionary with the mapped value.
3.  **Validation**:
    *   [x] Create a test "tradeable" JSON for `ES`.
    *   [x] Run the monitor in dry-run mode (or with logging) and verify that the `Contract.symbol` is set to `MES`.

## 3. List of Changes
*   **`TradeApps/breakout/fs/config.json`**:
    *   [x] Add `trade_mini_config` structure.
*   **`algo_forex/tws_monitor_and_trade2.py`**:
    *   [x] Implement config loading.
    *   [x] Implement symbol substitution logic in `process_trade_file`.        
    *   [x] Add descriptive logging for the substitution.
*   **`TradeApps/breakout/fs/constants.py`**:
    *   [x] Update version to `V20260413_1425`.
