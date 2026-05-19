# Breakout Add Last Updated Field To Open Trade JSON After Current Price

## Objective
Add `last_updated: "yyyy-mm-dd hh:mm:ss"` immediately after `current_price` in open trade JSON payloads.

## Scope
- Update `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Cover normal open trade JSON saves
- Cover per-cycle open trade JSON price reconciliation
- Validate field placement and value format

## Clarification
- `last_updated` means the last time the trade's price-derived fields were refreshed.
- It should be written whenever `current_price`, `gross_pnl_pips`, `net_return`, or `alt_net` are recalculated for an open trade.
- It is not the generic file write time and not the trade entry time.

## Implemented
- Added `last_updated` to the normal open-trade JSON save path in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Added `last_updated` to the per-cycle open-trade JSON refresh path in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Enforced field ordering so `last_updated` is written immediately after `current_price`

## Validation
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Manually refreshed an existing open EUR file and confirmed:
  - `current_price`
  - `last_updated`
  - recalculated PnL fields
