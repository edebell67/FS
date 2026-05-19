# Breakout Hotfix API Side Open Trade Refresh Worker

## Objective
Add an immediate API-side fallback so open trade JSON files are refreshed continuously and on-read even when the live trading runtime misses periodic updates.

## Scope
- Update `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Refresh open trade files before serving trade data
- Add a background worker in the API process for ongoing refresh
- Reuse the open-trade reconciliation logic from `common.py`

## Validation
- Verify syntax
- Verify an existing `.op.json` file gets a fresh `last_updated` without relying on the trading loop

## Implemented
- Added an API-side `_refresh_open_trade_files(...)` fallback in `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Added `_open_trade_refresh_worker()` so the API process refreshes open trade files continuously
- Hooked refresh into `/api/trades` and `/api/trade_file` so reads force a fresh pass before serving data
- Reused the reconciliation logic from `common.py`

## Validation Result
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Result: passed

## Operational Note
- The API process on port `5000` must be restarted for this hotfix to take effect.
