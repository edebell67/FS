# Task: Fix Top X Multi-Chart Loader product-type-aware source paths

## Summary
- Verify why `top_x_multi_chart_workflow` cannot load Top 20 data after the FS runtime moved to `json/<mode>/<product_type>/<date>/`.
- Update the workflow to read `_top20.json` and any supporting summary files from the correct product-type-aware day directories.
- Add regression coverage and validate the workflow behavior.

## Scope
- `TradeApps/breakout/fs/trade_viewer_api.py`
- `tests/test_breakout_fs_json_layout.py`

## Plan
- [x] Confirm the workflow is still reading the legacy flat path.
- [x] Refactor the workflow to use shared product-type-aware day-dir resolution.
- [x] Add a regression test covering product-type day folders.
- [x] Run targeted validation and record results.

## Log
- 2026-03-16 02:22:18 Created task from user request after verifying the Top X workflow was still attempting to read `BASE_PATH / mode / date / "_top20.json"` instead of the product-type-aware day folders.
- 2026-03-16 02:28:00 Updated `trade_viewer_api.py` so `_run_top_x_multi_chart_workflow()` reads `_top20.json` and `_summary_net.json` from `_iter_day_dirs_for(mode, date_str, product_type)` rather than the legacy flat path. Added optional workflow config support for `product_type` and switched scalper-ratio config lookup to the canonical `CONFIG_FILE`.
- 2026-03-16 02:29:00 Added regression coverage in `tests/test_breakout_fs_json_layout.py` to verify the Top X workflow reads only the selected product-type folder when both `crypto` and `forex` day folders exist.
- 2026-03-16 02:30:00 Validation:
  - `python -m py_compile TradeApps\breakout\fs\trade_viewer_api.py`
  - `pytest tests\test_breakout_fs_json_layout.py tests\test_breakout_fs_summary_product_type_filter.py`
  - Result: `10 passed in 0.72s`
