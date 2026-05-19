Source: User request on 2026-04-28 to modify Real-Time Stats so it filters and shows momentum strategy stats only.
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
  workflow_stage: todo
  depends_on: []
  feeds_into: []
Task Summary: Update the Real-Time Stats view and any supporting backend/query logic so the displayed stats are filtered to momentum strategies only.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_performance.html`, `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-28\`
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Plan:
- [x] 1. Identify the Real-Time Stats data source and current filtering behavior.
- [x] 2. Apply a momentum-only filter so Real-Time Stats includes only momentum strategy records.
- [x] 3. Verify the Real-Time Stats output shows momentum data and excludes non-momentum strategies.
Evidence:
Objective-Delivery-Coverage: 100%
Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Targeted Flask test-client verification against `/api/realtime_stats` using mocked momentum and non-momentum trade files in a workspace temp folder
Results:
- The Real-Time Stats page data source was confirmed to be `/api/realtime_stats` from [realtime_stats.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/realtime_stats.html).
- [trade_viewer_api.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/trade_viewer_api.py) now filters to strategy names beginning with `momentum` across `script_name`, `source_strategy`, `strategy_name`, and `app_name`.
- The API success payload bug was fixed by returning `True` instead of the invalid lowercase `true`.
- Mocked endpoint verification returned `STATUS 200`, `SUCCESS True`, `FILTER momentum_only`, and excluded the non-momentum sample from net totals.
Execution Log:
- 2026-04-28 16:10:59: Task created in `workstream/100_todo`.
- 2026-04-28 16:12:00: Confirmed the Real-Time Stats UI uses [realtime_stats.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/realtime_stats.html) and fetches `/api/realtime_stats`.
- 2026-04-28 16:16:00: Patched [trade_viewer_api.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/trade_viewer_api.py) so `/api/realtime_stats` scans momentum trades only and returns a valid success payload.
- 2026-04-28 16:17:00: Added an explicit “Momentum Strategies Only” label to [realtime_stats.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/realtime_stats.html).
- 2026-04-28 16:18:00: Verified the endpoint behavior with a mocked Flask request context and completed the task.
