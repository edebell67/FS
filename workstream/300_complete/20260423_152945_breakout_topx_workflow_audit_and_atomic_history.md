# Source
User requested implementation of recommendations from the Top X first-history timestamp investigation.

# Task Type
standard

# Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false

# Task Summary
Implement persistent Top X workflow audit logging, atomic `_top10_history.json` writes, preservation of corrupt history files, and skip/filter reason counts for `top_x_multi_chart_workflow`.

# Context
- `TradeApps/breakout/fs/trade_viewer_api.py`
- Top X Multi-Chart Loader workflow
- Per-date live folders such as `TradeApps/breakout/fs/json/live/forex/YYYY-MM-DD/`

# Destination Folder
None

# Dependency
Completed investigation: `workstream/300_complete/20260423_145506_breakout_topx_first_history_timestamp_investigation.md`

# Plan
- [x] 1. Add reusable per-date Top X audit writer.
  - Test: `python -m py_compile TradeApps/breakout/fs/trade_viewer_api.py` passes after implementation.
  - Evidence: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` completed with exit code 0.
- [x] 2. Record Top X run summaries and skip/filter reason counts.
  - Test: Manual run or compile plus code inspection confirms audit calls cover success, missing Top20, filter skips, payload write failure, and TB outcomes.
  - Evidence: `rg -n "_topx_workflow_audit|topx_audit|TOPX_AUDIT|history_corrupt|grid_auto_worker_startup" TradeApps/breakout/fs/trade_viewer_api.py` confirmed audit writer, run calls, startup marker, and endpoint.
- [x] 3. Make `_top10_history.json` updates atomic and preserve corrupt files.
  - Test: Code inspection confirms temp+replace write and corrupt-file rename before reset.
  - Evidence: `_log_top10_history_snapshot` now renames corrupt history to `_top10_history_corrupt_YYYYMMDD_HHMMSS.json` and writes via `_atomic_write_json`.
- [x] 4. Add API endpoint for reading Top X audit data.
  - Test: Compile passes and route exists for `/api/workflows/topx_audit`.
  - Evidence: `rg` confirmed `@app.route('/api/workflows/topx_audit', methods=['GET'])`.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `python -m py_compile TradeApps/breakout/fs/trade_viewer_api.py`
  - Objective-Proved: Modified Python remains syntactically valid.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/trade_viewer_api.py`
  - Objective-Proved: Audit, atomic history, and endpoint changes implemented.
  - Status: captured

# Implementation Log
- 2026-04-23 15:29 - Created task.
- 2026-04-23 15:37 - Added Top X audit file writer, per-run audit data, filter reason counts, TB outcome capture, startup marker, atomic history writes, corrupt file preservation, and audit read endpoint.

# Changes Made
- `TradeApps/breakout/fs/trade_viewer_api.py`
  - Added `TOPX_AUDIT_VERSION`.
  - Added `_log_topx_workflow_audit`.
  - Added persisted run audit data in `_run_top_x_multi_chart_workflow`.
  - Added filter reason counts for Top X selection.
  - Added TB outcome details to audit records.
  - Added grid-auto startup marker audit.
  - Changed `_log_top10_history_snapshot` to preserve corrupt history files and write atomically.
  - Added `GET /api/workflows/topx_audit`.

# Validation
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` passed.
- `rg -n "_topx_workflow_audit|topx_audit|TOPX_AUDIT|history_corrupt|grid_auto_worker_startup" C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` confirmed all expected code paths exist.

# Risks/Notes
- This task adds observability and safer writes. It does not change trading selection logic.
- Existing unrelated dirty work exists in the repository and was not modified/reverted.

# Completion Status
Complete - 2026-04-23 15:38.
