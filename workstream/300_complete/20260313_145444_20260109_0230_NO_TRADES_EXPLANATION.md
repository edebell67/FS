# Fix for Missing Base Trades
**Date**: 2026-01-09 02:35
**Version**: V20260109_0230

## Issue
User reported that base trade files were not being created. Logs showed strategies were being skipped with `[SKIPPING] ... is not active`.

## Root Cause
An explicit check in `BaseBreakoutStrategy.enter_trade` (in `common.py`) was returning early if the strategy was not active in 'net' or 'alt' mode. This prevented the creation of the base trade JSON file, which should exist regardless of execution status.

## Fix
Removed the blocking activation check from `enter_trade` in `common.py`.

### Flow Check
1. **Criteria Met**: `breakout.py` detects price breakout.
2. **Enter Trade**: Calls `enter_trade`.
3. **Activation Check (Removed)**: Previously blocked here. Now proceeds.
4. **Trade Obj Created**: Internal state updated, JSON file created.
5. **Handle Orders**: Calls `_handle_live_orders`.
   - Checks `activations.json`.
   - If not active, sends NO execution order (correct).
   - If active, sends execution order.

## Consequence
Base trades will now be created even for inactive strategies, allowing "shadow" tracking. These trades **will** count towards the `max_live_trades` limit.
