# Breakout FS Restore Screen Reads From Product Type Day Folders

## Objective
Urgently restore FS screen functionality so read views operate correctly from `json/{run_mode}/{product_type}/{date}` instead of implicitly depending on the legacy day-root layout.

## Problem
- The new runtime folder structure is present and receiving trades.
- Screens such as `strategy_performance.html` still appear blank or incomplete because their data dependencies are not consistently resolved from the product-type folder.
- The read path for screens depends on both raw trades and derived day-level files, and both need to align to the selected product-type structure.

## Scope
- Audit the screen/API chain for:
  - `strategy_performance.html`
  - other immediate FS read views relying on `_summary_net.json`, `_top20.json`, `_top_one.json`, `_trades_summary.json`
- Ensure active APIs read from product-type day folders correctly.
- Restore visible screen behavior once the derived files are available under the new structure.

## Plan
1. Trace the exact API dependencies for `strategy_performance.html` and identify which files are missing or still resolved from legacy assumptions.
2. Patch any remaining API read paths that still implicitly depend on `json/{run_mode}/{date}`.
3. Validate the full screen path against an actual populated folder like `json/sim/forex/<date>`.
4. Confirm the screen renders without needing the legacy dated root to exist.

## Validation
- Open `strategy_performance.html` against a populated product-type day folder.
- Confirm the main stats table, top20 modal, drilldown, and related reads work without `json/{run_mode}/{date}` present.
- Confirm no blank-screen dependency remains on the legacy layout.

## Implementation
- Added explicit `product_type` selection to `strategy_performance.html`.
- Wired the page to load product types from config and include the selected `product_type` in:
  - `/api/stats_summary`
  - `/api/top20`
  - `/api/trades`
  - `/api/trade_file`
  - `/api/bias_from_summary`
- Updated `trade_viewer_api.py` endpoints to accept `product_type` and resolve only the selected product-type day folder when provided.
- Local validation passed:
  - `python -m py_compile` on patched API/generator modules
  - `pytest tests/test_breakout_fs_json_layout.py` -> `7 passed`

## Chronology
- 2026-03-14 21:32 Europe/London: Task created urgently after deletion of the legacy `json/sim/<date>` folder caused `strategy_performance.html` to appear blank even though raw trades existed in `json/sim/forex/<date>`.
- 2026-03-14 21:55 Europe/London: Added product-type selector plumbing for strategy performance and patched supporting APIs to read the selected product-type folder.
