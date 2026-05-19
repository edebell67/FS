Source: User request on 2026-04-29 to review /realtime_stats.html and capture a requirement for 5-minute historical snapshots with forward/backward navigation.
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
Task Summary: Expand the Real-Time Stats data cache into persisted 5-minute snapshots and update realtime_stats.html so users can scroll backward and forward through historical dashboard context.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html, C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py, C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats_cache.json, and source summaries under json\live\<product_type>\<date>\_trades_summary.json.
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Requirement:
- Capture a dashboard snapshot every 5 minutes, using the same strategy group/product aggregation as the live Real-Time Stats view.
- Preserve enough historical snapshots to let users move backward and forward through prior 5-minute dashboard states.
- Add UI controls in /realtime_stats.html for previous snapshot, next snapshot, latest/live mode, and visible snapshot timestamp/context.
- Keep the current live auto-refresh behavior for latest mode while allowing historical mode to stay fixed on the selected snapshot.
- Expand the cache/data model rather than relying only on the current single realtime_stats_cache.json payload.
Plan:
- [x] 1. Review the existing realtime_stats.html fetch/render flow and trade_viewer_api.py cache builder to define the snapshot data contract.
- [x] 2. Add a persisted 5-minute snapshot store keyed by date, strategy_group, product, and snapshot timestamp.
- [x] 3. Update the cache refresh worker so every 5-minute boundary records a snapshot while still maintaining the latest payload.
- [x] 4. Add API support for listing available snapshots and fetching a specific snapshot or latest snapshot.
- [x] 5. Add dashboard controls for back/forward/latest and make historical mode render the selected snapshot without auto-jumping.
- [x] 6. Validate with generated sample snapshots and live API checks for momentum and all strategy groups.
Evidence:
Objective-Delivery-Coverage: 100%
Execution Log:
- 2026-04-29 10:09:23: Task created in workstream/100_todo.
- 2026-04-29 10:xx:xx: Moved task to workstream/200_inprogress and reviewed the existing realtime_stats.html single-payload render flow plus trade_viewer_api.py realtime cache builder.
- 2026-04-29 10:xx:xx: Added `realtime_stats_snapshots.json` as the persisted 5-minute snapshot store.
- 2026-04-29 10:xx:xx: Updated trade_viewer_api.py so forced cache refreshes record a 5-minute snapshot while preserving `realtime_stats_cache.json` as the latest payload.
- 2026-04-29 10:xx:xx: Added snapshot selection support to `/api/realtime_stats` via the `snapshot` query parameter, returning `snapshot_mode`, `snapshot_at`, and the available snapshot index.
- 2026-04-29 10:xx:xx: Added previous, next, and latest controls to realtime_stats.html and made auto-refresh apply only while viewing the latest snapshot.
- 2026-04-29 10:xx:xx: Restarted the local API and verified `localhost:5000` serves latest and historical snapshot payloads.
Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- direct forced cache refresh created `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats_snapshots.json`
- direct API helper check returned `latest` and `historical` payloads with rows
- live HTTP check confirmed `/api/realtime_stats?strategy_group=momentum` returns `snapshot_mode=latest` and a snapshot index
- live HTTP check confirmed `/api/realtime_stats?strategy_group=momentum&snapshot=<timestamp>` returns `snapshot_mode=historical`
- live page check confirmed realtime_stats.html includes `prevSnapshotBtn`, `nextSnapshotBtn`, `latestSnapshotBtn`, and `snapshotLabel`
Outcome:
- Real-Time Stats now captures persisted 5-minute dashboard snapshots and supports forward/backward navigation through the available snapshot history.
- Latest mode continues to auto-refresh; historical mode stays on the selected snapshot until the user navigates or returns to latest.
