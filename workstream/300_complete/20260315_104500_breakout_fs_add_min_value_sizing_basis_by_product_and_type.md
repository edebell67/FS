# Breakout FS Add Min Value Sizing Basis By Product And Type

## Metadata
- Project: breakout
- Task: add min value sizing basis by product and product type
- Status: In Progress
- Owner: Codex
- Started: 2026-03-15 10:45:00

## Request
Replace the crude crypto quantity-percent override with a configurable minimum-value sizing basis:
- a shared default can apply to forex
- product types can have their own default min value
- individual products can override that default

## Plan
1. Add config fields for default min value, min value by product type, and min value by product.
2. Route order-quantity calculation through the new min-value basis with legacy fallback.
3. Update the config UI to edit the new fields cleanly.
4. Validate JSON parsing and Python syntax after the change.

## Execution Log
### 2026-03-15 10:45:00
- Created lifecycle record.
- Implementing min-value sizing as the new primary sizing basis, with legacy percent-based fallback for older configs.

### 2026-03-15 10:53:00
- Added config fields in `TradeApps/breakout/fs/config.json`:
  - `default_min_value`
  - `min_value_by_product_type`
  - `min_value_by_product`
- Updated `TradeApps/breakout/fs/common.py` so order quantity now prefers:
  1. `min_value_by_product[PRODUCT]`
  2. `min_value_by_product_type[product_type]`
  3. `default_min_value`
  4. legacy percent-based sizing fallback
- Updated `TradeApps/breakout/fs/trade_viewer_api.py` to apply the same sizing basis for API-generated close orders and to normalize the new config structures on save.
- Updated `TradeApps/breakout/fs/trade_viewer.html` config UI:
  - `Default Min Value` field
  - `Min Value By Product Type (JSON)`
  - `Min Value By Product (JSON)`
- Seeded config defaults with:
  - forex = 10
  - crypto = 1
  - metals = 10

## Validation
```powershell
Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\config.json | ConvertFrom-Json | Out-Null
python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
Select-String -Path C:\Users\edebe\eds\TradeApps\breakout\fs\config.json -Pattern 'default_min_value|min_value_by_product_type|min_value_by_product'
```

## Current Status
- Implemented and validated locally.
- Manual verification is still required in the config UI and a live/sim order payload before completion.
