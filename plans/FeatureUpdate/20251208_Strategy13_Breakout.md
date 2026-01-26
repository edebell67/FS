# Plan: Strategy 13 - Breakout

This document outlines the plan to implement `Strategy13`, a new strategy for `tradepanel` that replicates the logic from the standalone `breakout.py` script.

## 1. Goal

The objective is to create a new, fully integrated strategy within the `tradepanel` framework that executes a breakout trading strategy. The strategy should be configurable using existing UI elements.

## 2. Implementation Details

### File Creation
- A new file `s13.py` will be created in `C:\Users\edebe\eds\algo_viewer\tradepanel\strategies\`.
- No existing files will be modified. Therefore, no backups are required.

### Class Definition
- A new class, `Strategy13`, will be defined inheriting from `BaseStrategy`.
- It will be registered with the name "Strategy 13 - Breakout" using the `@BaseStrategy.register_strategy` decorator.

### Parameter Mapping (`__init__`)
The strategy will not have its own UI elements. Instead, it will derive its parameters from existing global configurations, as specified:

- **`window_size`**: The lookback window for detecting the breakout range.
  - **Source**: Reuses the `s09_lookback_var` UI setting.
  - **Example**: `self.window_size = int(self.config.get('s09_lookback_var', 5))`
- **`pip_buffer`**: The buffer added to the high/low of the range to confirm a breakout.
  - **Source**: Reuses the `trade_at_avg_price_avg_range_var` UI setting.
  - **Example**: `self.pip_buffer = float(self.config.get('trade_at_avg_price_avg_range_var', 0.00015))`

The following parameters from `breakout.py` will **not** be used or stored in `Strategy13`, as their functionality is handled globally by the `TradeManager`:
- `TP_PIPS` (Take Profit)
- `SL_PIPS` (Stop Loss)
- `COMMISSION_USD`
- `SPREAD_PIPS` 
- `PIP_VALUE`

### Core Logic (`evaluate`)
The `evaluate` method will contain the strategy's core logic and will be executed on each application tick:

1.  **Get Current Price**: Fetch the latest price for the configured product.
2.  **Check for Active Trades**: The strategy will check if it has any of its own trades currently active. It does this by filtering the active trades list for trades `triggered_by` "Strategy 13 - Breakout".
3.  **Entry Logic**:
    - This logic only runs if `Strategy13` has **no active trades**.
    - It checks if the price history has sufficient data (is the `deque` full?).
    - It finds the `max` and `min` of the recent price history.
    - If `current_price` breaks above `max_history + pip_buffer`, it executes a **BUY** trade.
    - If `current_price` breaks below `min_history - pip_buffer`, it executes a **SELL** trade.
4.  **Update Price History**: The `current_price` is added to the `price_history` `deque` for the next tick's evaluation.

### Trade Management
- **Entry**: `Strategy13` is responsible for trade entry only.
- **Exits (TP/SL)**: All exit logic is handled automatically by the `TradeManager` using the globally configured Stop Loss and Profit Target values. `Strategy13` will not contain any exit logic.
- **P&L Calculations**: Handled entirely by the `TradeManager`.

### JSON Definition
- A `get_definition_json()` method will be implemented to provide a clear, human-readable description of the strategy's rules and parameter mappings.
