# Breakout FS Apply Product Type To Multi Charts Trade Bucket Live Trades

## Metadata
- Project: breakout
- Task: apply product type selection to remaining product-data screens
- Status: Complete
- Owner: Codex
- Started: 2026-03-15 13:24:20

## Request
Extend product type awareness to additional screens where product data is viewed so they resolve and display data from the correct product-type folder instead of relying on legacy mode/date-only behavior.

Target screens:
- `multi_chart.html` / `multi_chart.js`
- `trade_bucket.html`
- `live_trades.html`

## Plan
1. Inspect each target screen and its API calls to identify where `product_type` is currently missing from requests or routing.
2. Update UI state and request builders so each screen can select, persist, and pass `product_type`.
3. Update backend/API resolution paths as needed so each screen reads from the correct `json/<mode>/<product_type>/<date>` outputs.
4. Add focused regression or smoke coverage for each affected screen path.
5. Validate manually and with targeted automated checks, then document any restart/reload requirements.

## Execution Log
### 2026-03-15 13:24:20
- Created lifecycle record for extending product type support to multi charts, trade bucket, and live trades screens.

### 2026-03-15 13:49:00
- Updated `TradeApps/breakout/fs/multi_chart.html` and `TradeApps/breakout/fs/multi_chart.js` to add product type selection and pass `product_type` through summary, frequency, trade, and trade-bucket requests and links.
- Updated `TradeApps/breakout/fs/trade_bucket.html` to add product type selection, persist it from query/config, and include it in trade bucket, trade, and trade file requests.
- Updated `TradeApps/breakout/fs/live_trades.html` to add product type selection, fetch `_live_trades.json` through `/api/trade_file` with `product_type`, and preserve product type in cross-screen links.
- Updated `TradeApps/breakout/fs/trade_viewer_api.py` so `_trade_buckets.json` is resolved under the selected product-type day folder and trade-bucket CRUD routes accept `product_type`.
- Added backend regression coverage in `tests/test_breakout_fs_json_layout.py` for product-type-aware trade bucket path resolution.
- Restarted `trade_viewer_api.py` so the new backend routing and path resolution are active.

## Validation
```powershell
python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
pytest C:\Users\edebe\eds\tests\test_breakout_fs_summary_product_type_filter.py C:\Users\edebe\eds\tests\test_breakout_fs_json_layout.py
```

## Result
- `python -m py_compile` passed for `trade_viewer_api.py` and `summary_net_generator.py`.
- `pytest` passed: `9 passed in 0.88s`.
- `trade_viewer_api.py` was restarted successfully and is listening again on port `5000`.
- Product type support is now applied across multi charts, trade bucket, and live trades screens, including product-type-aware trade bucket storage.
