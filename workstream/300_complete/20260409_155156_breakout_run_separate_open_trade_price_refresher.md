# Breakout Run Separate Open Trade Price Refresher

## Objective
Run a separate price update routine alongside the main breakout process so open `.op.json` files continue receiving fresh `current_price`, `last_updated`, and recalculated PnL fields.

## Scope
- Add a standalone refresher script under `C:\Users\edebe\eds\TradeApps\breakout\fs`
- Reuse the existing open-trade reconciliation logic in `common.py`
- Start the refresher as a separate process
- Validate that an existing open `.op.json` file is refreshed by the standalone routine

## Implemented
- Added standalone script:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\open_trade_price_refresher.py`
- The script:
  - discovers products with `OPEN` trade files for the day
  - fetches live quotes via `common.fetch_latest_quotes(...)`
  - refreshes `.op.json` files via `common._update_open_trade_json_prices(...)`
  - supports `--once`, `--interval`, `--mode`, `--date`, and optional `--products`

## Validation
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\open_trade_price_refresher.py`
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\open_trade_price_refresher.py --once`
- Verified refreshed file:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-09\breakout_R_4_tp20.0_sl5.0_643fed38_CHF_20260409_075007_4_0.00015_20.0_5.0_op.json`
  - `last_updated` moved to `2026-04-09 16:05:33`
