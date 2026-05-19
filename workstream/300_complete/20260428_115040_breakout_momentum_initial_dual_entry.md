Source: User request on 2026-04-28 to modify `momentum.py` so that both buy and sell trades are executed at the first price hit, with subsequent executions following the existing momentum rules.
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
Task Summary: Update `momentum.py` so the first qualifying price establishes at least one initial `LONG` and one initial `SHORT` trade, after which all subsequent entries continue to follow the existing momentum ladder rules already implemented.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Dependency: None
Plan:
- [x] 1. Define the initial-entry behavior precisely in `momentum.py` so the first live price creates one buy and one sell trade without breaking the current ladder logic.
  - [x] Test: Read updated entry flow and confirm the bootstrap logic is separate from subsequent momentum thresholds.
  - Evidence: Added `_bootstrap_initial_dual_entry(...)` and kept `check_and_enter(...)` for subsequent ladder-only entries.
- [x] 2. Implement the bootstrap dual-entry change while preserving current TP/SL handling and subsequent same-direction ladder entries.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`
  - Evidence: Compile completed with exit code 0.
- [x] 3. Run a controlled verification proving at least one initial `LONG` and one initial `SHORT` JSON trade are created, and that later entries still follow the existing rules.
  - [x] Test: Synthetic tick verification plus a real local JSON-creation check.
  - Evidence: Synthetic run returned `VERIFICATION_OK`; local proof created two `momentum_bootstrapcheck*_op.json` files on the first tick.
Evidence:
Objective-Delivery-Coverage: 100%
- Bootstrap verification: first tick opened both `LONG` and `SHORT`
- Ladder verification: subsequent ticks opened additional same-direction trades at the configured 5-pip step
- JSON verification: initial dual-entry produced two real `*_op.json` files for `momentum_bootstrapcheck`
Execution Log:
- 2026-04-28 11:50:40: Backlog task created in `workstream/100_todo` for the initial dual-entry momentum change.
- 2026-04-28 12:03:00: Task moved to `workstream/200_inprogress` and implementation started.
- 2026-04-28 12:04:00: Added first-tick bootstrap logic to open missing `LONG` and `SHORT` trades at the current anchor price.
- 2026-04-28 12:05:00: Verified that later ticks still follow the existing momentum ladder rules.
- 2026-04-28 12:06:00: Confirmed real JSON file creation for both initial bootstrap trades in a local reproduction.
