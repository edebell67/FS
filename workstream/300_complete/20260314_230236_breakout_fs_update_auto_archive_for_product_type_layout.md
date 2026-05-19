# Breakout FS Update Auto Archive For Product Type Layout

## Objective
Update the FS auto-archive functionality so it operates correctly against the new `json/{run_mode}/{product_type}/{date}` structure instead of the legacy `json/{run_mode}/{date}` layout.

## Prior Understanding
Reviewed the completed prior tasks:
- [20260313_042243_breakout_fs_apply_auto_archiver.md](/C:/Users/edebe/eds/workstream/300_complete/20260313_042243_breakout_fs_apply_auto_archiver.md)
- [20260313_042937_breakout_fs_preserve_summary_net_history_pre_autoarchive.md](/C:/Users/edebe/eds/workstream/300_complete/20260313_042937_breakout_fs_preserve_summary_net_history_pre_autoarchive.md)

Those tasks established:
- `_perform_cld_auto_archive(config)` in `fs/common.py`
- threshold-based `.cld` auto-archive using `auto_archive_threshold`
- `_summary_net.json` preservation before archive
- fallback/restore behavior for preserved summary history

However, that implementation was originally scoped around `json/<run_mode>/<date>` and now needs a product-type-aware review/update.

## Problem
- FS runtime has moved toward `json/{run_mode}/{product_type}/{date}`.
- Auto-archive must now archive `.cld` files inside the correct product-type day folder(s).
- `_summary_net.json` preservation must happen in the correct product-type path.
- Any remaining archive detection, watcher, or validation logic must stop assuming a single day root directly under `run_mode`.

## Scope
- Review and update `fs/common.py` auto-archive behavior for product-type day folders.
- Review and update `fs/archive_cld.py` watcher behavior.
- Confirm `_summary_net_pre_auto_archive.json` preservation/restore still works when product types are in play.
- Verify that auto-archive does not silently skip valid product-type folders or recreate legacy assumptions.

## Plan
1. Re-read the existing FS auto-archive implementation and identify every place that still assumes `json/{run_mode}/{date}`.
2. Update the auto-archive path resolution so it scans or targets `json/{run_mode}/{product_type}/{date}` correctly.
3. Validate that summary preservation and restore behavior remains correct per product type.
4. Run targeted verification with a repo-local fixture under the new folder structure.
5. Confirm the live FS runtime and optional standalone watcher both honor the product-type-aware archive path.

## Validation
- Python syntax checks for changed FS archive modules.
- Targeted fixture using `json/{run_mode}/{product_type}/{date}` with:
  - top-level `*_cld.json`
  - `_summary_net.json`
  - threshold trigger
- Pass criteria:
  - archive fires in the correct product-type folder
  - preserved summary copies are created in the correct product-type path
  - summary restore path still works after archive

## Implementation
- Reviewed the prior completed FS auto-archive and summary-preservation tasks and confirmed the current code had already been partially updated to enumerate product-type day folders via shared layout helpers.
- Tightened the archive documentation/comments in `TradeApps/breakout/fs/common.py` so the product-type-aware path is explicit.
- Added focused regression coverage in `tests/test_breakout_fs_auto_archive_product_type.py` to validate:
  - `.cld` auto-archive against `json/{run_mode}/{product_type}/{date}`
  - preservation of `_summary_net_pre_auto_archive.json` in the product-type folder
  - no dependence on recreating the legacy `json/{run_mode}/{date}` day root
- Cleaned `utcnow()` deprecation usage in the auto-archive path to `datetime.now(timezone.utc)`.

## Validation Results
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py C:\Users\edebe\eds\TradeApps\breakout\fs\archive_cld.py C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`
  - Result: Passed.
- `pytest C:\Users\edebe\eds\tests\test_breakout_fs_auto_archive_product_type.py C:\Users\edebe\eds\tests\test_breakout_fs_json_layout.py`
  - Result: `8 passed in 3.10s`

## Chronology
- 2026-03-14 23:02 Europe/London: Task created after reviewing the previous completed FS auto-archive tasks and identifying that they were implemented against the pre-product-type structure.
- 2026-03-14 23:10 Europe/London: Re-read the current archive implementation and confirmed it already enumerates product-type day folders through shared layout helpers.
- 2026-03-14 23:16 Europe/London: Added a focused product-type auto-archive regression test and validated preservation behavior under `json/{run_mode}/{product_type}/{date}`.
- 2026-03-14 23:18 Europe/London: Removed `utcnow()` deprecation usage from the auto-archive path and re-ran syntax/tests successfully.
