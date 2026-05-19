Source: User report on 2026-04-28 that in `strategy_performance.html`, `momentum_s_0_tp5.0_sl7.0` drills down to 1 short trade and 8 long trades, but it should drill down only to short trades.
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
  workflow_stage: backlog
  depends_on: []
  feeds_into: []
Task Summary: Investigate why `strategy_performance.html` drill-down for `momentum_s_0_tp5.0_sl7.0` is including long trades, determine whether the issue is in summary generation, API shaping, or frontend filtering, and define the fix required so sell-prefixed momentum strategies drill down only to sell/short trades.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_performance.html`, `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\`
Destination Folder: None
Dependency: None
Plan:
- [x] 1. Trace the data flow for `strategy_performance.html` drill-down from source JSON / API payload to frontend filtering.
  - [x] Test: Inspect the frontend click/drill-down logic and the backend/API fields used for strategy and direction filtering.
  - Evidence: The direct table rows at [strategy_performance.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/strategy_performance.html:3026) call `showDrillDown(product, strategy, parm_raw, direction)` with an explicit strategy and direction. The summary/hierarchy rows at [strategy_performance.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/strategy_performance.html:5940) and [strategy_performance.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/strategy_performance.html:6028) call `showDrillDown(..., 'all', parm_raw, direction)` and therefore build context from parameter groups rather than exact strategy keys. The backend matcher in [trade_viewer_api.py](/C:/Users/edebe/eds/TradeApps/breakout/fs/trade_viewer_api.py:3924) is direction-aware when given an exact strategy.
- [x] 2. Verify whether momentum trade files and summary records encode the buy/sell-specific strategy names consistently.
  - [x] Test: Compare representative `momentum_b_*` and `momentum_s_*` trade artifacts and any summary rows used by the page.
  - Evidence: Existing momentum trade artifacts were being migrated to buy/sell-specific names, but the summary drill-down path still groups by `parm_raw` / parameter context instead of exact `script_name`, so both sides can enter the candidate pool if they share the same TP/SL parameter family.
- [x] 3. Determine the exact root cause of the mixed-direction drill-down and define the code change required to enforce direction-correct drill-down behavior.
  - [x] Test: Produce a documented conclusion with file/line references and the required fix scope.
  - Evidence: Root cause is frontend drill-down pooling logic in [strategy_performance.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/strategy_performance.html:3328) when invoked from summary/hierarchy entry points that pass `appName='all'`. Required fix scope: summary/hierarchy drill-down should pass or preserve the exact strategy key (`momentum_s_0_tp5.0_sl7.0`) instead of only `parm_raw`, or the pool filter must additionally constrain by exact strategy-side prefix before rendering.
Evidence:
Objective-Delivery-Coverage: 100%
- Confirmed the mismatch is not caused by the backend exact matcher path
- Confirmed the summary/hierarchy frontend path broadens the drill-down pool across shared parameter groups
- Identified the concrete fix boundary in `strategy_performance.html`
Execution Log:
- 2026-04-28 14:12:26: Investigative backlog task created in `workstream/100_todo`.
- 2026-04-28 14:13:00: Task moved to `workstream/200_inprogress`.
- 2026-04-28 14:16:00: Traced `showDrillDown(...)` calls from main table, hierarchy rows, and leaderboard rows.
- 2026-04-28 14:18:00: Confirmed backend direction matcher is strict, but summary/hierarchy drill-down requests use broader parameter-group inputs.
- 2026-04-28 14:20:00: Concluded the mixed long/short drill-down arises from frontend pool construction, not from the backend exact trade matcher.
