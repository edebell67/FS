Source: User reported on 2026-04-29 that /strategy_performance.html drill-down and send-to-chart displays do not match the selected strategy/trade context.
Task Type: investigation
Task Attributes:
  recurring_task: false
  recurrence_type: scheduled
  recurrence_rule: None
  looping_task: false
  loop_until: manual_stop
  splittable_task: false
  split_output_type: files
  split_spawn_task: false
  workflow_task: false
  workflow_name: ""
  workflow_stage: complete
Task Summary: Investigate mismatches in /strategy_performance.html where strategy drill-down trades and send-to-chart display do not match the selected strategy/performance row.
Context:
- Page: C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_performance.html
- API/server: C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
- Related generated data: C:\Users\edebe\eds\TradeApps\breakout\fs\json\live
- Process reference: C:\Users\edebe\eds\skills\workstream-task-lifecycle
Destination Folder: None
Dependency: None
Problem Statements:
- /strategy_performance.html drill down to trades is not matching the strategy row selected.
- /strategy_performance.html send to chart display is not matching the selected strategy/trade context.
Investigation Plan:
Plan:
- [ ] 1. Identify the UI handlers in strategy_performance.html for drill-down and send-to-chart actions.
  - Test: Search strategy_performance.html for drill-down/chart handlers and record handler names plus line references.
  - Evidence: planned
- [ ] 2. Trace the exact parameters sent from the selected strategy row to the backend/API or chart page.
  - Test: Capture request URL/body or JS routing payload for one selected strategy row and compare with visible selected row fields.
  - Evidence: planned
- [ ] 3. Identify the backend endpoints and data files used to populate drill-down trades.
  - Test: Search trade_viewer_api.py for the matching endpoints and record source JSON files used.
  - Evidence: planned
- [ ] 4. Compare selected strategy identifiers against trade file fields such as strategy_name, source_strategy, script_name, product, direction, and status.
  - Test: Inspect a concrete returned trade set and verify whether every trade matches the selected strategy key/product/direction/timeframe.
  - Evidence: planned
- [ ] 5. Reproduce the mismatch with a concrete selected strategy and captured request/response payloads.
  - Test: Run the page/API flow and record selected row, request payload, response count, and mismatching trade examples.
  - Evidence: planned
- [ ] 6. Determine whether mismatch comes from frontend parameter construction, backend filtering, stale cache/data, strategy-name normalization, or chart-page interpretation.
  - Test: Document root cause with exact file/line references and classify the required fix as a follow-up `_998_` task if implementation is needed.
  - Evidence: planned
Expected Deliverables:
- [ ] Root cause documented with file/line references.
- [ ] Concrete example showing selected strategy versus returned drill-down trades.
- [ ] Concrete example showing selected strategy/trade versus chart display target.
- [ ] Recommendation for implementation fix, including impacted files and validation steps.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: manual_verification
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_performance.html
  - Objective-Proved: User-visible page flow to be investigated.
  - Status: planned
- Evidence-Type: log_output
  - Artifact: not_applicable
  - Objective-Proved: Captured request/response evidence for mismatch reproduction.
  - Status: planned
- Evidence-Type: diff
  - Artifact: not_applicable
  - Objective-Proved: No implementation diff is expected unless converted to a `_998_` fix task.
  - Status: not_applicable
Execution Log:
- 2026-04-29 13:12: Task created in workstream/100_todo.
- 2026-04-29 13:16: Read C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md and confirmed investigative task filenames must include `_999_`.
- 2026-04-29 13:16: Renamed and moved task to workstream/100_backlog/20260429_131228_breakout_999_investigate_strategy_performance_drilldown_chart_mismatch.md.
- 2026-04-29 13:30: Reproduced drill-down mismatch with EURAUD_C / breakout_R / 4_tp20.0_sl3.0. The API returned 27 trades including breakout_Rev and breakout_R_Rev trades.
- 2026-04-29 13:30: Root cause identified: backend /api/trades indexed path and frontend drill-down filtering used prefix/substring matching, so breakout_R matched breakout_R_Rev.
- 2026-04-29 13:30: Created follow-up fix task C:\Users\edebe\eds\workstream\200_inprogress\20260429_133000_breakout_998_fix_strategy_performance_drilldown_chart_matching.md.
Implementation Log:
- 2026-04-29 13:16: Corrected lifecycle metadata to match the current workstream-task-lifecycle requirements.
Changes Made:
- Renamed lifecycle file to include `_999_`.
- Moved lifecycle file from workstream/100_todo to workstream/100_backlog.
- Added Destination Folder, Dependency, normalized Plan tests, Auto-Acceptance, and Evidence inventory.
Validation:
- Manual check: C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md states investigative task files must include `_999_`.
- Reproduction command: live /api/trades query for EURAUD_C, strategy=breakout_R, params=4_tp20.0_sl3.0 returned mixed app_name values before the fix.
Risks/Notes:
- This is an investigation task only. Any implementation fix identified by the investigation should be created as a separate `_998_` follow-up task.
Completion Status: Complete - root cause identified and `_998_` fix task created.
