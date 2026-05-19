Source: User request in Codex thread on 2026-04-28 to create `momentum.py` from `TradeApps/breakout/fs/breakout.py` with momentum-based directional entries.
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
Task Summary: Create a new `momentum.py` strategy that continuously opens new directional positions every configurable X pips from the anchor or most recent same-direction open trade, with default `TP=5` and `SL=7`, while allowing multiple simultaneous open positions.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\breakout.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Dependency: None
Plan:
- [x] 1. Inspect the current breakout wrapper and shared strategy base to determine the minimum safe customization surface for multi-position momentum entries.
  - [x] Test: `rg -n "class BaseBreakoutStrategy|enter_trade|close_trade|check_and_exit|run_multiwindow" C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Evidence: Confirmed the reusable single-trade lifecycle hooks in `common.py` at lines 1139, 2254, 2361, 2465, 2552, and 4679.
- [x] 2. Add `momentum.py` and implement multi-position momentum entry and exit handling while reusing existing JSON persistence and live-order generation paths.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`
  - Evidence: Compile passed with exit code 0 after adding `C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`.
- [x] 3. Add the configurable default momentum step to config and verify the new file and config are syntactically valid.
  - [x] Test: `python -c "import json, pathlib; json.load(open(r'C:\Users\edebe\eds\TradeApps\breakout\fs\config.json','r',encoding='utf-8')); print(pathlib.Path(r'C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py').exists())"`
  - Evidence: JSON parse passed and the command printed `True`.
Evidence:
Objective-Delivery-Coverage: 100%
- Validation command: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py`
- Validation command: `python -c "import json, pathlib; json.load(open(r'C:\Users\edebe\eds\TradeApps\breakout\fs\config.json','r',encoding='utf-8')); print(pathlib.Path(r'C:\Users\edebe\eds\TradeApps\breakout\fs\momentum.py').exists())"`
Execution Log:
- 2026-04-28 10:28:46: Task file created in `workstream/100_todo` before active implementation.
- 2026-04-28 10:29:00: Task moved to `workstream/200_inprogress` when implementation started.
- 2026-04-28 10:35:00: Added `momentum.py` with anchor-based momentum entries, multi-open-trade handling, persisted open-trade restore, and inherited order/JSON reuse.
- 2026-04-28 10:36:00: Added `momentum_step_pips` to `config.json` with default value `5`.
- 2026-04-28 10:38:00: Validated Python syntax and JSON parsing successfully.
