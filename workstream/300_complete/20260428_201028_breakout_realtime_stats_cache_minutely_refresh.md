Source: User request on 2026-04-28 to change the Trade Performance Dashboard cache refresh from every 5 minutes to every 1 minute.
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
Task Summary: Reduce the realtime stats cache refresh interval from 300 seconds to 60 seconds so the Trade Performance Dashboard updates minutely.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Plan:
- [x] 1. Update the realtime stats cache refresh interval constant from 300 seconds to 60 seconds.
- [x] 2. Verify the stale check and background worker continue to use the shared refresh constant.
- [x] 3. Validate the updated setting in code and close the lifecycle task.
Evidence:
Objective-Delivery-Coverage: 100%
Execution Log:
- 2026-04-28 20:10:28: Task created in workstream/100_todo.
- 2026-04-28 20:1x:xx: Updated `REALTIME_STATS_CACHE_REFRESH_SECONDS` in C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py from `300` to `60`.
- 2026-04-28 20:1x:xx: Verified the stale cache check still uses `REALTIME_STATS_CACHE_REFRESH_SECONDS`.
- 2026-04-28 20:1x:xx: Verified the realtime cache background worker sleep loop still uses `REALTIME_STATS_CACHE_REFRESH_SECONDS`.
- 2026-04-28 20:1x:xx: Verified syntax with `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`.
Validation:
- `rg -n "REALTIME_STATS_CACHE_REFRESH_SECONDS" C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
Outcome:
- The Trade Performance Dashboard cache is now configured to refresh every 60 seconds instead of every 300 seconds, and both cache staleness detection and background refresh scheduling continue to use the same shared interval constant.
