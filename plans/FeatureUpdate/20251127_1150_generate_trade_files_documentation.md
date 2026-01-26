# Documentation: generate_trade_files.py

**Location:** `C:\Users\edebe\eds\Trades\generate_RT\generate_trade_files.py`

## Overview
This script acts as the **bridge** between the internal logging system (`simple_trend_trader.py`) and the TWS execution system. It runs as an independent process that continuously monitors trade logs and converts them into execution orders for Interactive Brokers (TWS) based on specific configuration rules.

## Core Functionality

### 1. Monitoring (The Watchdog)
*   **Behavior:** Runs in an infinite loop (`while True`), scanning every **10 seconds**.
*   **Target:** Monitors the directory `C:\Users\edebe\eds\Trades\Trades\json_logs\open_trades\[TODAY_DATE]\`.
*   **Goal:** Detects any new `.json` log files created by the trading strategies.

### 2. Detection & Deduplication
*   Identifies new trade files that appear in the target folder.
*   Maintains a `processed_files.log` to ensure that each unique trade file is processed **exactly once**.

### 3. Filtering (The Gatekeeper)
*   **Config Source:** Reads `rt_trade_config.json` (shared with the Trade Monitor UI).
*   **Logic:** Checks the **Trade Title** of the new log file.
*   **Rule:** If the title is **NOT** present in the "Active RT Titles" list, the trade is **ignored**.
    *   *This allows selective "Go Live" capability, where only specific strategies execute real trades while others remain in simulation/logging mode.*

### 4. Transformation (The Translator)
*   Reads the trade details (Symbol, Position, etc.) from the source log.
*   **Dynamic Adjustments:**
    *   **Quantity:** Applies `trade_qty_percentage` from `config.json` (e.g., executing only 50% of the standard size).
    *   **Signal Flipping:** If `return_type` is set to `alt_net`, it flips the signal (BUY becomes SELL, and vice versa).

### 5. Execution (The Handoff)
*   **Output:** Generates a new JSON file in `C:\Users\edebe\eds\trades_rt2\order`.
*   **Content:** Contains TWS-compatible instructions (Symbol, Action, Quantity, OrderType, etc.).
*   **Downstream:** This folder is watched by the TWS Interface (e.g., `tws_price_gateway.py` or similar) which picks up these files and submits the actual orders to IB.

### 6. State Management
*   **Round-Turn Protection:** Tracks "Active TWS Trades" to prevent duplicate entries for the same strategy while a trade is already active.
*   **Lifecycle Tracking:** Monitors the `closed_trades` folder. When a trade is closed in the logs, it clears that title from its internal active list, allowing the strategy to trade again in the future.
