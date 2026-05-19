Source: Follow-up fix from C:\Users\edebe\eds\workstream\200_inprogress\20260429_131228_breakout_999_investigate_strategy_performance_drilldown_chart_mismatch.md
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
  workflow_task: false
  workflow_name: ""
  workflow_stage: complete
Task Summary: Fix /strategy_performance.html drill-down and multi-chart handoff matching so selected strategy rows map to exact canonical strategy+parameter keys.
Context:
- C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_performance.html
- C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
- C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart.js
Destination Folder: None
Dependency: C:\Users\edebe\eds\workstream\200_inprogress\20260429_131228_breakout_999_investigate_strategy_performance_drilldown_chart_mismatch.md
Plan:
- [x] 1. Tighten backend /api/trades indexed strategy matching to exact canonical model keys.
  - Test: Query /api/trades for breakout_R + 4_tp20.0_sl3.0 + EURAUD_C and confirm returned app_name values are only breakout_R_4_tp20.0_sl3.0.
  - Evidence: Live API returned success=True, count=6, apps=['breakout_R_4_tp20.0_sl3.0'], bad=[].
- [x] 2. Tighten frontend drill-down filtering to exact canonical model keys so browser-side filtering cannot reintroduce prefix mismatches.
  - Test: Inspect strategy_performance.html matching logic and run a static syntax/check search for exact canonical matching helpers.
  - Evidence: strategy_performance.html now uses normalizeModel/buildModel exact comparisons and removes prefix startsWith matching for concrete strategy rows.
- [x] 3. Normalize Strategy Performance chart handoff to send base strategy plus parm_raw instead of relying on pre-concatenated inline keys.
  - Test: Verify generated payload can resolve to multi_chart processedSeries key strategy_params|product.
  - Evidence: _summary_net.json contains breakout_R_4_tp20.0_sl3.0 / EURAUD_C with 6 points; chart handoff now sends strategy=breakout_R, parm_raw=4_tp20.0_sl3.0 so multi_chart reconstructs the same key.
- [x] 4. Validate Python syntax and live API behavior.
  - Test: python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py and live HTTP /api/trades request.
  - Evidence: py_compile passed; live API returned exact app set after API restart.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py; live /api/trades query for EURAUD_C breakout_R 4_tp20.0_sl3.0
  - Objective-Proved: Backend exact matching no longer returns sibling strategy families.
  - Status: captured
- Evidence-Type: diff
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py and C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_performance.html
  - Objective-Proved: Code changes implement exact canonical matching and normalized chart handoff.
  - Status: captured
Implementation Log:
- 2026-04-29 13:30: Created `_998_` fix task after `_999_` investigation reproduced prefix matching defect.
- 2026-04-29 13:33: Updated /api/trades indexed and legacy paths to match exact canonical strategy+params keys.
- 2026-04-29 13:36: Updated strategy_performance.html drill-down browser filter to use exact canonical model matching.
- 2026-04-29 13:37: Updated Strategy Performance chart button to pass base strategy plus parm_raw for multi_chart reconstruction.
- 2026-04-29 13:43: Adjusted backend canonical key handling so app_name values that already contain params are not appended with signal labels from strategy fields.
- 2026-04-29 13:45: Restarted API on port 5000 and validated live endpoint behavior.
Changes Made:
- C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py: exact canonical model matching for /api/trades indexed and legacy paths.
- C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_performance.html: exact drill-down client filtering and normalized chart handoff payload.
Validation:
- python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py passed.
- Live API validation after restart: /api/trades?mode=live&date=2026-04-29&product_type=forex&product=EURAUD_C&strategy=breakout_R&params=4_tp20.0_sl3.0 returned count=6 and only app_name breakout_R_4_tp20.0_sl3.0.
- Chart handoff validation: _summary_net.json contains breakout_R_4_tp20.0_sl3.0 / EURAUD_C, matching the reconstructed multi_chart key from strategy=breakout_R plus parm_raw=4_tp20.0_sl3.0.
Risks/Notes:
- Drill-down summary bucket views that intentionally aggregate several strategies must still use category/member-key logic; exact matching applies to concrete strategy rows.
Completion Status: Complete.
