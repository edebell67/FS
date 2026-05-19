# Documentation: Separation of Base Trade Creation and Live Execution
**Date**: 2026-01-09 03:48
**Version**: V20260109_0340

## Critical Logic Architecture
This document captures the specific logic separation implemented to ensure that "Base Trades" (shadow logs) are always created, while "Live Executions" (broker orders) are strictly limited.

**CRITICAL RULE**: Do not revert this separation. The `max_live_trades` guard MUST NOT exist in `enter_trade`.

### 1. Base Trade Creation (`enter_trade` in `common.py`)
*   **Purpose**: Records the signal, creates the JSON log file, and increments internal counters.
*   **Guard Status**: **UNRESTRICTED**.
    *   The `max_live_trades` check has been explicitly removed/commented out here.
    *   This ensures that every valid signal produces a timestamped JSON file (e.g., `breakout_...json`), allowing for verification and "shadow trading" analysis whatever the account state.

### 2. Live Execution (`_create_l_trade_order` in `common.py`)
*   **Purpose**: Creates the `..._open_tradeable.json` file which the broker portal picks up to execute the trade.
*   **Guard Status**: **RESTRICTED**.
    *   This function performs a strict check: `_get_total_open_live_trades() >= max_live_trades`.
    *   If the limit (e.g., 2) is reached, it returns `None` and logs `[GUARD] Max live trades ... reached`.
    *   This protects the real money account.

## Supporting Fixes (Dependencies)
The following fixes were also applied and must be retained for the system to function:
1.  **Strategy Name Persistence**: `_load_persisted_state` checks `startswith(f"{self.script_name}_{self.trade_product}_")` to prevent `breakout` from stealing `breakout_Rev` files.
2.  **Verify Algo Script**: `verify_algo_execution_and_restart_02.py` sets `cwd=os.path.dirname(__file__)` to ensure correct path resolution for child processes.

## Summary
*   **Files Created**: YES (Base Trade Files).
*   **Broker Executed**: ONLY if below limit (Live Trade Files).
