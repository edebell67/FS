# Breakout FS Migrate Remaining Generators To Product Type Layout

## Objective
Urgently migrate the remaining active FS generators/services so derived files are written to `json/{run_mode}/{product_type}/{date}` instead of the legacy `json/{run_mode}/{date}` path.

## Problem
- Raw trades are now being written under the new product-type structure.
- Some derived generators still write to the legacy day root.
- This leaves UI screens blank or inconsistent because `_summary_net.json`, `_top20.json`, `_top_one.json`, `_trades_summary.json`, and similar files are not guaranteed to exist in the same product-type folder as the raw trades.

## Scope
- Audit active services started by the FS runtime/verify launcher.
- Patch remaining generators to use the shared layout helpers.
- Stop legacy creation of `json/{run_mode}/{date}` by active generators.

## Priority Targets
- `summary_net_generator.py`
- `top_one_generator.py`
- `weighted_race.py`
- any other active generator/service in the verify launch set that still writes day-level outputs to the legacy path

## Plan
1. Identify every active writer still creating or targeting `json/{run_mode}/{date}`.
2. Patch each one to resolve day directories via the shared product-type layout helpers.
3. Verify that derived files land beside the raw trades under `json/{run_mode}/{product_type}/{date}`.
4. Confirm the legacy dated root is no longer recreated by active services.

## Validation
- Restart the FS sim process.
- Confirm `_summary_net.json`, `_top20.json`, `_top_one.json`, `_trades_summary.json`, and related outputs appear under the product-type folder.
- Confirm `json/{run_mode}/{date}` is not recreated by patched generators.

## Implementation
- Patched remaining active generator/services to stop assuming `json/{run_mode}/{date}` only:
  - `weighted_race.py`
  - `top_one_generator.py`
  - `dna_frequency_net.py`
  - `dna_frequency_alt.py`
  - `automated_strategy_picker.py`
  - `grid_live_monitor.py`
- Updated these modules to use the shared product-type-aware layout helpers or to enumerate product-type day folders from config.
- Validation passed:
  - `python -m py_compile` on patched Python modules
  - `pytest tests/test_breakout_fs_json_layout.py` -> `7 passed`

## Chronology
- 2026-03-14 21:32 Europe/London: Task created urgently after confirming raw trades were in `json/sim/forex/<date>` while some generators still recreated the legacy `json/sim/<date>` path.
- 2026-03-14 21:55 Europe/London: Patched remaining active generators/readers to write/read derived files from product-type day folders; local syntax/tests passed.
