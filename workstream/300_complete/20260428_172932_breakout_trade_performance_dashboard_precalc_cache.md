Source: User request on 2026-04-28 to implement a cache routine that precalculates the info required to populate the Trade Performance Dashboard and refreshes every 5 minutes.
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
  workflow_stage: in_progress
  depends_on: []
  feeds_into: []
Task Summary: Add a 5-minute precalculated cache for the Trade Performance Dashboard so it loads from prebuilt dashboard data instead of calculating on request, and ensure 5 min / 30 min sections populate reliably.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py, C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html, C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\_trades_summary.json
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\
Plan:
- [x] 1. Add a cache builder that precalculates Trade Performance Dashboard payloads.
- [x] 2. Refresh the cache every 5 minutes in the background and make /api/realtime_stats read from it.
- [x] 3. Verify the live endpoint returns quickly and 5 min / 30 min windows populate from cached data.
Evidence:
Objective-Delivery-Coverage: 100%
Execution Log:
- 2026-04-28 17:29:32: Task created in workstream/200_inprogress.
- 2026-04-28 18:xx:xx: Added realtime dashboard cache helpers in C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py to precompute dashboard payloads by strategy group, product, and time window from _trades_summary.json.
- 2026-04-28 18:xx:xx: Added file-backed cache output at C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats_cache.json and switched /api/realtime_stats to serve cached payloads instead of recalculating on request.
- 2026-04-28 18:xx:xx: Added background cache refresh worker with a 5 minute refresh interval so dashboard payloads are rebuilt automatically.
- 2026-04-28 19:18:00: Verified cache file exists and is populated. Observed size 930736 bytes and strategy groups breakout, breakout_r, breakout_r_rev, breakout_rev, momentum.
- 2026-04-28 19:xx:xx: Verified live API response from http://127.0.0.1:5000/api/realtime_stats?strategy_group=momentum returns success=True, filter=strategy_group, selected_group=momentum, and 4 dashboard windows from cache.
- 2026-04-28 19:xx:xx: Verified syntax with python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py.
Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- cache file check on `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats_cache.json`
- live endpoint check on `http://127.0.0.1:5000/api/realtime_stats?strategy_group=momentum`
Outcome:
- Trade Performance Dashboard data is now precalculated into a dedicated cache file.
- `/api/realtime_stats` now serves cached data rather than performing heavy request-time aggregation.
- A background worker refreshes the cache every 5 minutes.
- The live endpoint now returns promptly and exposes the expected 4 time windows needed by the dashboard, which addresses the missing and delayed 5 min / 30 min sections caused by slow on-demand computation.
