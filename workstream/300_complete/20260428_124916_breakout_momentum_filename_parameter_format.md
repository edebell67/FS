Source: User request on 2026-04-28 to make `momentum` trades use parameter text `0_tp5.0_sl7.0` in line with existing breakout filename/strategy formatting.
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
Task Summary: Update `momentum.py` naming so generated trades follow the breakout-style parameterized strategy prefix and use `0_tp5.0_sl7.0` for the momentum strategy identity.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Dependency: None
Plan:
- [x] 1. Inspect the existing breakout filename/strategy-name format and identify the correct momentum prefix shape.
  - [x] Test: Read current breakout filenames and relevant name-generation code.
  - Evidence: Existing breakout trades use a strategy prefix like `breakout_R_2_tp10.0_sl20.0_...`; `run_multiwindow` builds this from `script_alias`.
- [x] 2. Modify momentum naming so the generated strategy/file prefix uses `momentum_0_tp5.0_sl7.0` semantics instead of the current generic `momentum`.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`
  - Evidence: Added `build_momentum_script_alias(...)` and wired `__main__` to pass `momentum_0_tp5.0_sl7.0`-style aliases into `run_multiwindow`; compile passed.
- [x] 3. Run a controlled verification to confirm generated JSON filenames include the expected parameter segment.
  - [x] Test: Local bootstrap run that creates `momentum_*_op.json` and inspect the output names.
  - Evidence: Verified real file creation with names `momentum_0_tp5.0_sl7.0_3a1e8119_CHF_20260428_125500_1_5.0_5.0_7.0_op.json` and `momentum_0_tp5.0_sl7.0_5ae1100c_CHF_20260428_125500_1_5.0_5.0_7.0_op.json`.
Evidence:
Objective-Delivery-Coverage: 100%
- `momentum.py` now emits breakout-style strategy/file prefixes using `momentum_0_tp5.0_sl7.0`
- Verified against real generated `*_op.json` files
Execution Log:
- 2026-04-28 12:49:16: Task file created in `workstream/100_todo`.
- 2026-04-28 12:49:30: Task moved to `workstream/200_inprogress`.
- 2026-04-28 12:51:00: Patched `momentum.py` to derive the runtime alias from TP/SL as `momentum_0_tp5.0_sl7.0`.
- 2026-04-28 12:52:00: Verified bootstrap-generated filenames include the expected parameter segment.
