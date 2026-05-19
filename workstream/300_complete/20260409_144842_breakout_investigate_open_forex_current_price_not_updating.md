# Breakout Investigate Open Forex Current Price Not Updating

## Objective
Determine why `current_price` in open forex trade JSON files is not updating to the current FX quote.

## Scope
- Inspect `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Inspect the forex tick processing path and JSON persistence path
- Confirm the concrete reason with code evidence

## Notes
- Triggered from live question comparing open trade JSON `current_price` vs `http://127.0.0.1:8002/api/vw_000_fx_quotes`

## Findings
- `current_price` in an open trade JSON is only refreshed when the owning strategy instance executes `display_open_trade_status(current_price)` in `common.py`, which then calls `_save_trade_json(current_price)`.
- That path only runs from `process_new_tick(...)` for the active processor handling that product/strategy instance.
- The specific file `breakout_R_2_tp20.0_sl5.0_866668bc_EUR_20260409_092111_2_0.00015_20.0_5.0_op.json` has `CreationTime` and `LastWriteTime` both at `2026-04-09 10:21:26`, proving it has not been touched since initial creation.
- Other `EUR` open files from the same day were updated later, for example multiple `*_EUR_20260409_120334_*_op.json` files have `LastWriteTime` around `2026-04-09 13:04:13/14`.
- Therefore the stale `current_price` is not caused by the FX endpoint itself. It is caused by that specific open file no longer being attached to an actively updating processor.

## Code Evidence
- `process_new_tick(...)` only persists open trade state via `display_open_trade_status(current_price)`:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- `display_open_trade_status(...)` calls `_save_trade_json(current_price)`
- `_save_trade_json(...)` writes `current_price` directly into the JSON

## Conclusion
The open trade file is orphaned/stale. Its `current_price` is frozen because the owning processor is not currently updating that JSON, even though live `EUR` quotes continue to move.

## Fix Implemented
- Added a per-poll reconciliation path in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` to refresh persisted `OPEN` trade JSON files from the shared live quote map, even if the original in-memory owner is no longer attached.
- Added `_calculate_open_trade_pnl(...)` to recompute `gross_pnl_pips`, `net_return`, `alt_net`, and `adhoc_cost_usd` consistently during reconciliation.
- Added `_update_open_trade_json_prices(...)` and invoked it from the main live loop before the existing per-cycle virtual trade price updater.

## Validation
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Result: passed
