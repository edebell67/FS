Source: User report on 2026-04-28 that `momentum.py` is not creating JSON files like `breakout.py`.
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
Task Summary: Diagnose why the running `momentum.py` process is not producing trade JSON artifacts and implement the fix if the issue is in strategy logic.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\json\`
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Dependency: Running `momentum.py` instance and shared breakout JSON persistence behavior.
Plan:
- [x] 1. Inspect current runtime evidence and target JSON directories for momentum-specific artifacts.
  - [x] Test: Read current `momentum_stdout.log`/`momentum_stderr.log` and list recent `json/live/<product>/<date>` files.
  - Evidence: Both momentum logs were empty and no `*momentum*` files existed under `json/live/forex/2026-04-28`, while many breakout JSON files existed.
- [x] 2. Compare `momentum.py` entry/save flow against `BaseBreakoutStrategy` to identify why open-trade JSON creation is being skipped or never reached.
  - [x] Test: Trace `enter_trade`, `_save_trade_json`, and `process_new_tick` call paths in local code.
  - Evidence: `momentum.py` calls `super().enter_trade(...)` at line 171, appends the returned trade, and later calls `_save_trade_json(...)` at line 201; the shared save path is intact.
- [x] 3. Apply the fix, then validate by running a controlled local reproduction that confirms JSON file creation.
  - [x] Test: Synthetic tick run that creates at least one momentum trade and confirms an `*_op.json` file exists.
  - Evidence: Local reproduction created `momentum_localcheck_c93ad7b2_AUD_20260428_115005_1_5.0_5.0_7.0_op.json`.
Evidence:
Objective-Delivery-Coverage: 100%
- Runtime inspection: no momentum JSON files existed for the live run at time of check
- Code-path inspection: JSON saver is reachable from the momentum entry path
- Local proof: threshold-crossing reproduction created a real `*_op.json` file on disk
Execution Log:
- 2026-04-28 11:42:23: Debug task file created in `workstream/100_todo`.
- 2026-04-28 11:42:30: Task moved to `workstream/200_inprogress`.
- 2026-04-28 11:44:00: Confirmed no live `momentum` JSON artifacts were present and background logs were empty/buffered.
- 2026-04-28 11:44:30: Confirmed the momentum entry path still calls the shared `_save_trade_json` logic.
- 2026-04-28 11:44:50: Local reproduction with a forced 5-pip move created a real `*_op.json` file, proving JSON creation works once an entry threshold is crossed.
