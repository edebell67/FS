Source: Direct user request in this session.

Task Summary: Ensure FS trade drilldowns, especially Trade Bucket strategy drilldowns, can still access closed trades after `.cld` auto-archive moves them under `archive/<HHMMSS>`.

Context:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`

Plan:
- [x] 1. Identify the FS backend drilldown endpoints that currently scan only the active day folder.
  - [x] Test: Review `trade_viewer_api.py` endpoints used by drilldowns; pass if the non-archive-aware paths are identified.
  - [x] Evidence: Confirmed `/api/trades` used `trade_dir.glob(...)` against the top-level day folder only, and `/api/trade_file` only checked direct day/virtual paths plus non-archived directory search by ID.
- [x] 2. Implement archive-aware closed-trade discovery for FS drilldown APIs without breaking open-trade behavior.
  - [x] Test: Update the relevant FS file-discovery helpers/endpoints so closed-trade lookups include `archive/<HHMMSS>` files.
  - [x] Evidence: Added `_iter_trade_json_files(...)` in `trade_viewer_api.py`; `/api/trades` now includes archived closed files recursively while keeping open trades top-level only, `/api/trade_file` can resolve archived closed trades by filename or trade ID, and `promotion_blocks` uses the same archive-aware discovery path.
- [x] 3. Validate that archived closed trades remain accessible through drilldown-oriented FS APIs.
  - [x] Test: Run targeted syntax checks and a focused fixture verification covering archived closed trade retrieval.
  - [x] Evidence: `python -m py_compile` passed for `trade_viewer_api.py`, and repo-local fixture `workstream\verification\fs_trade_drilldown_archive_fixture` returned both top-level and archived closed trades through `/api/trades` and resolved the archived trade through `/api/trade_file`.

Implementation Log:
- 2026-03-13 10:56 Europe/London: Created bugfix task for FS drilldown retrieval of archived closed trades after auto-archive.
- 2026-03-13 10:57 Europe/London: Traced the drilldown failure to `trade_viewer_api.py`, where `/api/trades` and `/api/trade_file` only scanned the active top-level day folder.
- 2026-03-13 10:59 Europe/London: Added a shared file iterator that includes archived closed trades recursively while preserving current top-level-only behavior for open trades.
- 2026-03-13 11:00 Europe/London: Updated `/api/trades`, `/api/trade_file`, and `promotion_blocks` to use archive-aware closed-trade discovery.
- 2026-03-13 11:01 Europe/London: Validated the fix with syntax checks and a repo-local Flask fixture covering archived closed-trade drilldown retrieval.

Changes Made:
- Updated `TradeApps\breakout\fs\trade_viewer_api.py`:
  - Added `_iter_trade_json_files(day_dir, include_archived_closed, product_hint)`.
  - Updated `/api/trades` to include archived `*_cl.json` and `*_cld.json` files from `archive/<HHMMSS>/`.
  - Updated `/api/trade_file` to resolve archived closed trades by filename or trade ID.
  - Updated `promotion_blocks` to include archived closed trades consistently.

Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Result: Passed with no output.
- Repo-local functional verification in `workstream\verification\fs_trade_drilldown_archive_fixture`
  - Result: `/api/trades` returned both trade IDs `[101, 202]`, where `202` existed only under `archive/<HHMMSS>/`; `/api/trade_file?trade_id=202` also resolved successfully. Final assertion output: `fs_trade_drilldown_archive_test=ok`.

Risks/Notes:
- The fix preserves top-level-only scanning for open trades and excludes underscore metadata files from archive-aware discovery.
- This resolves the backend retrieval gap for archived closed trades in drilldown-oriented APIs; frontend drilldown logic can continue using `/api/trades` and `/api/trade_file` without archive-specific changes.

Completion Status:
- Complete - 2026-03-13 11:01 Europe/London
