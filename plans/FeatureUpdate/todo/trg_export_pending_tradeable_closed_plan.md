# System-product-focused FX metadata (with leg helper)

## Summary
- Added `dbo.fn_expand_trade_legs` to split `_c`/`_s` products into individual legs, returning signal, symbol, and metadata resolved via `forex_products.system_product` first.
- Both export triggers now call this helper, so open/close exports emit one JSON per leg while preserving original attributes. `_c` keeps identical signals; `_s` flips the second leg.
- JSON payloads now show:
  * `GBPCAD_S` BUY → `{symbol:"GBP",..."action":"BUY"}` and `{symbol:"USD",..."currency":"CAD","action":"SELL"}`
  * CHF trades → `{symbol:"USD","currency":"CHF"}`
- `tradeable` flags still advance to 2 (open) and 4 (closed) after export; mirrored rows in `tbl_rt_trades` retain original `product` for traceability.

## Verification
- Ran labelled GUID harness; confirmed paired leg rows in `tbl_rt_trades` and JSON outputs.
- Checked `combined_trades_closed` to ensure all GUIDs moved to `tradeable = 4`.
