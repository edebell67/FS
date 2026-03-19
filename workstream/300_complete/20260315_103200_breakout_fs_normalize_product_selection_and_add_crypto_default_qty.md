# Breakout FS Normalize Product Selection And Add Crypto Default Qty

## Metadata
- Project: breakout
- Task: normalize product selection in config UI and add crypto default quantity
- Status: In Progress
- Owner: Codex
- Started: 2026-03-15 10:32:00

## Request
- Ensure configured products such as `BTC` appear correctly selected in the FS config UI.
- Add a crypto-specific default trade volume setting so crypto orders do not reuse the forex quantity default.

## Plan
1. Normalize `trade_products` values consistently in the config UI and save path.
2. Add a config field for crypto-specific quantity percent.
3. Route order quantity calculation through a shared helper that switches by mapped product type.
4. Validate JSON/syntax and record the outcome.

## Execution Log
### 2026-03-15 10:32:00
- Created lifecycle record.
- Investigating config UI case-normalization and quantity calculation call sites.

### 2026-03-15 10:41:00
- Updated `TradeApps/breakout/fs/trade_viewer.html` so `trade_products` render/save in uppercase and `product_types` render/save in lowercase. This fixes checkbox selection drift caused by mixed-case saved values.
- Added `Crypto Trade Qty %` to the config modal.
- Updated `TradeApps/breakout/fs/common.py` and `TradeApps/breakout/fs/trade_viewer_api.py` to calculate order quantity by mapped product type, using `crypto_trade_qty_percent` for crypto products and `trade_qty_percent` otherwise.
- Updated `TradeApps/breakout/fs/config.json` to include:
  - `crypto_trade_qty_percent`
  - `BTC` in `trade_products`
  - normalized uppercase product codes
  - `crypto` and `metals` in `product_types`

## Validation
```powershell
Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\config.json | ConvertFrom-Json | Out-Null
python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
Select-String -Path C:\Users\edebe\eds\TradeApps\breakout\fs\config.json -Pattern 'crypto_trade_qty_percent|\"BTC\"|\"product_types\"'
```

## Current Status
- Code/config changes are implemented and validated locally.
- Manual UI/runtime verification is still required before moving this task to `300_complete`.
