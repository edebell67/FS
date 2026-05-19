Source: User request on 2026-04-28 to add an 'all' option to the strategy group filter in /realtime_stats.html.
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
Task Summary: Add an `all` option to the Real-Time Stats strategy group filter so the dashboard can show combined data across all supported strategy groups.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html and C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Plan:
- [x] 1. Update the strategy group options to include an `all` selection in the dashboard UI and API.
- [x] 2. Make the realtime stats aggregation support combined results across all strategy groups when `all` is selected.
- [x] 3. Verify the filter renders and returns valid combined dashboard data.
Evidence:
Objective-Delivery-Coverage: 100%
Execution Log:
- 2026-04-28 21:52:52: Task created in workstream/100_todo.
- 2026-04-28 22:xx:xx: Moved task to workstream/200_inprogress and updated `trade_viewer_api.py` to add an `all` strategy group option.
- 2026-04-28 22:xx:xx: Added cached combined-payload support for `all` by merging the per-group realtime dashboard payloads rather than recalculating from raw trades.
- 2026-04-28 22:xx:xx: Updated `realtime_stats.html` to show the `all` option in the filter and adjusted the dashboard labels/subline/footer for combined strategy-group mode.
- 2026-04-28 22:xx:xx: Added a classifier guard so concrete trades continue to classify into their real family instead of matching `all` first.
- 2026-04-28 22:xx:xx: Verified syntax with `python -m py_compile` and verified offline combined payload shape returned `selected_group=all`, `rows=4`, `windows=4`, and summary keys for all windows.
Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Offline combined payload check via imported `trade_viewer_api.py`
- Targeted file checks in `realtime_stats.html` for the `all` option and combined-mode labels
Outcome:
- The Real-Time Stats strategy group filter now supports an `all` selection, and the API can return a combined dashboard view across all supported strategy groups using cached data.
