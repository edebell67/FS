Source: User request on 2026-04-28 to enable a Real-Time Stats filter for strategy groups with options `momentum`, `breakout`, `breakout_r`, `breakout_rev`, and `breakout_r_rev`.
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
Task Summary: Extend the Real-Time Stats mockup dashboard so users can switch the data source between momentum and the requested breakout strategy groups, while preserving the dashboard layout.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`, `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Plan:
- [x] 1. Add backend strategy-group filtering to the Real-Time Stats API.
- [x] 2. Add strategy-group filter controls to the dashboard UI.
- [x] 3. Verify the API/UI switch between the requested strategy groups correctly.
Evidence:
Objective-Delivery-Coverage: 100%
Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Mocked Flask test-client verification of `/api/realtime_stats` for `momentum`, `breakout`, `breakout_r`, `breakout_rev`, and `breakout_r_rev`
Results:
- [trade_viewer_api.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/trade_viewer_api.py) now accepts `strategy_group` and filters mutually exclusively across the requested families.
- [realtime_stats.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/realtime_stats.html) now exposes a strategy-group selector and keeps product filtering as a secondary filter.
- Mocked verification results:
  - `momentum` -> count `1`, net `10.0`
  - `breakout` -> count `1`, net `20.0`
  - `breakout_r` -> count `1`, net `-5.0`
  - `breakout_rev` -> count `1`, net `30.0`
  - `breakout_r_rev` -> count `1`, net `-12.0`
Execution Log:
- 2026-04-28 17:13:54: Follow-up task created in `workstream/200_inprogress`.
- 2026-04-28 17:16:00: Added backend `strategy_group` support for the Real-Time Stats dashboard API.
- 2026-04-28 17:18:00: Added a strategy-group selector to the dashboard UI and updated the live header text to reflect the active group.
- 2026-04-28 17:21:00: Fixed family-overlap bugs so `breakout`, `breakout_r`, `breakout_rev`, and `breakout_r_rev` are filtered mutually exclusively.
