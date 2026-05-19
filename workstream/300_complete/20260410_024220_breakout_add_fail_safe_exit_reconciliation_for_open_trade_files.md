# Breakout Add Fail Safe Exit Reconciliation For Open Trade Files

- Status: Complete
- Started: 2026-04-10 02:42:20
- Completed: 2026-04-10 02:47:30
- Project: breakout
- Owner: Codex

## Request

Investigate and fix the recurring defect where an `OPEN` trade file remains open on disk even though the latest price already crosses its TP/SL level.

## Concrete Case

- File: `breakout_Rev_2_tp3.0_sl20.0_9ca2c713_EURAUD_C_20260410_001227_2_0.00015_3.0_20.0_op.json`
- Product: `EURAUD_C`
- Direction: `LONG`
- Entry: `1.87585`
- TP: `3 pips`
- Observed `current_price`: `1.87725`
- Result: file still marked `OPEN` even though TP was already exceeded

## Plan

1. Confirm whether live runner state or persisted-file reconciliation is missing TP/SL closure.
2. Add a fail-safe reconciliation path for persisted `OPEN` trades using the latest quote snapshot.
3. Validate that qualifying open files are auto-closed and renamed to `*_cld.json`.

## Findings

- The concrete `EURAUD_C / breakout_Rev_2_tp3.0_sl20.0` trade should have closed.
- Restore logic and TP/SL logic were both correct.
- Replaying one fresh quote through the restored strategy closed the trade immediately.
- The real gap was shared infrastructure: `_update_open_trade_json_prices(...)` refreshed `current_price` and PnL on persisted `OPEN` files, but never evaluated TP/SL for those files.
- That means any strategy could leave an `OPEN` file behind if the live strategy loop missed the exit while the file refresher kept updating the price.

## Fix

- Added `_reconcile_open_trade_exit_file(...)` in `common.py`.
- The shared persisted-file refresh path now:
  - updates `current_price` and PnL,
  - checks TP/SL using the latest quote snapshot,
  - closes and renames qualifying files to `*_cld.json`,
  - writes `exit_time`, `exit_price`, and `exit_reason`,
  - decrements global active state as a fail-safe.
- Added quote `timestamp` into the standalone refresher payload so fail-safe closes use the quote time.

## Scope

- This was not limited to `breakout_Rev`.
- It affected any strategy whose persisted `OPEN` files rely on the shared refresh path in `common.py`.

## Validation

1. `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\open_trade_price_refresher.py`
   - Passed.
2. Direct replay of the concrete trade with a fresh `EURAUD_C` quote
   - Closed the trade immediately at TP.
3. Disk verification
   - `breakout_Rev_2_tp3.0_sl20.0_9ca2c713_EURAUD_C_20260410_001227_2_0.00015_3.0_20.0_op.json`
   - became `breakout_Rev_2_tp3.0_sl20.0_9ca2c713_EURAUD_C_20260410_001227_2_0.00015_3.0_20.0_cld.json`
