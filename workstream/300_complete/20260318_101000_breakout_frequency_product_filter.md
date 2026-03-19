# 2026-03-18 10:10:00: breakout: Add Product Type Filter to Frequency Explorer

## Summary
Add a product type filter to the Frequency Explorer and ensure it fetches data from the correct subdirectories (`json/{runMode}/{product_type}/{date}/`).

## Objectives
- [x] Add `product_type` select UI to header.
- [x] Initialize and persist `productType` state.
- [x] Modify `fetchData()` to construct correct file paths.
- [x] Update version number in `Constants.py`.

## Progress Log
- 2026-03-18 10:10:00: Task created.
- 2026-03-18 10:10:00: Initial plan created.
- 2026-03-18 10:20:00: Implemented UI changes and path logic in `frequency_explorer.html`.
- 2026-03-18 10:25:00: Updated `Constants.py` to `V20260318_1010`.
- 2026-03-18 10:40:00: HOTFIX: Updated `trade_viewer_api.py` and `frequency_explorer.html` to resolve path resolution errors for missing product-specific dates. Implemented JSON response validation to prevent HTML parsing errors.
- 2026-03-18 10:42:00: Updated `Constants.py` to `V20260318_1015`.
