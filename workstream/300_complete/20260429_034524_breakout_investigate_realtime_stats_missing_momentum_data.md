Source: User reported on 2026-04-29 that realtime_stats.html shows zero stats even though multiple momentum trade files now exist.
Task Type: standard
Task Attributes:
  recurring_task: false
  recurrence_type: scheduled
  recurrence_rule: None
  looping_task: false
  loop_until: manual_stop
  splittable_task: false
  split_output_type: files
  split_spawn_task: false
  split_failure_mode: fail_fast
  workflow_task: false
  workflow_name: ""
  workflow_stage: complete
  depends_on: []
  feeds_into: []
Task Summary: Investigate why realtime_stats.html is showing zero momentum stats despite live momentum trade files being present for 2026-04-29, and fix the data path if needed.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html, trade_viewer_api.py, realtime_stats_cache.json, and live trade/summary files under json\live\forex\2026-04-29.
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Plan:
- [x] 1. Compare live momentum trade files against today's _trades_summary.json and realtime_stats_cache.json.
- [x] 2. Identify where momentum trades are being excluded from the realtime stats pipeline.
- [x] 3. Implement and validate a fix so realtime_stats.html shows the momentum data.
Evidence:
Objective-Delivery-Coverage: 100%
Execution Log:
- 2026-04-29 03:45:24: Task created in workstream/200_inprogress.
- 2026-04-29 03:45:xx: Confirmed live folder `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-29` contained 27 momentum trade files while `_trades_summary.json` initially contained only 5 momentum rows.
- 2026-04-29 03:46:xx: Identified summary-stage dedupe bug in `summary_net_generator.py`: `_trade_dedupe_key(...)` prioritized `trade_id` ahead of `guid`, causing momentum trades with reused per-product trade_id values to collapse together.
- 2026-04-29 03:47:xx: Patched `summary_net_generator.py` to prefer `guid` and use a more specific fallback dedupe key.
- 2026-04-29 03:48:xx: Regenerated `2026-04-29` forex summary and confirmed `_trades_summary.json` momentum rows increased from 5 to 38.
- 2026-04-29 03:49:xx: Identified realtime windowing timezone bug in `trade_viewer_api.py`: persisted trade timestamps were UTC-naive while realtime window comparisons used local BST wall-clock time, making trades appear one hour older than reality.
- 2026-04-29 03:50:xx: Patched `_parse_iso_ts(...)` in `trade_viewer_api.py` to treat naive persisted timestamps as UTC and convert them to local wall-clock time before bucketing.
- 2026-04-29 03:51:xx: Rebuilt realtime cache directly and confirmed momentum counts updated to short-window values (`open_buy m5=8 m30=20`, `open_sell m5=2 m30=14`, `closed_buy m30=2`).
- 2026-04-29 03:52:xx: Found `localhost:5000` API was not running; started `trade_viewer_api.py` and verified live endpoint now returns corrected momentum counts.
Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- direct regeneration of `2026-04-29` forex `_trades_summary.json`
- direct rebuild of `realtime_stats_cache.json`
- live API check on `http://127.0.0.1:5000/api/realtime_stats?strategy_group=momentum`
Outcome:
- Realtime Stats now has the required momentum trades in its source summary and buckets them into the correct local-time windows.
- The original zero/near-zero display was caused by a combination of summary dedupe loss and a one-hour UTC-vs-BST windowing error.
