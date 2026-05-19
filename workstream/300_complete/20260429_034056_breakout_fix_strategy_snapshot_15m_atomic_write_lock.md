Source: User provided a runtime PermissionError on 2026-04-29 for strategy_snapshot_15m_generator.py writing _strategy_snapshots_15m.json.
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
Task Summary: Investigate and fix the PermissionError raised when strategy_snapshot_15m_generator.py replaces _strategy_snapshots_15m.json during cache/snapshot refresh.
Context: C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_snapshot_15m_generator.py and live json output folder for 2026-04-29.
Destination Folder: C:\Users\edebe\eds\TradeApps\breakout\fs\
Plan:
- [x] 1. Inspect the snapshot writer and identify why os.replace is failing on Windows.
- [x] 2. Implement a safe write strategy or retry logic that tolerates transient file locks.
- [x] 3. Validate the fix and close the lifecycle task.
Evidence:
Objective-Delivery-Coverage: 100%
Execution Log:
- 2026-04-29 03:40:56: Task created in workstream/200_inprogress.
- 2026-04-29 03:xx:xx: Inspected strategy_snapshot_15m_generator.py and confirmed write_payload used a single `tmp.replace(output_path)` with no retry or fsync, which is vulnerable to transient file locks on Windows.
- 2026-04-29 03:xx:xx: Compared the failing writer to the existing resilient atomic JSON write pattern already used in C:\Users\edebe\eds\TradeApps\breakout\fs\common.py.
- 2026-04-29 03:xx:xx: Patched write_payload to use a unique temp filename, flush + fsync before replace, and retry `os.replace` on PermissionError before failing.
- 2026-04-29 03:xx:xx: Verified syntax with `python -m py_compile`.
- 2026-04-29 03:xx:xx: Verified the patched write_payload by importing the module and successfully writing then deleting a test output file in the live forex 2026-04-29 folder.
Validation:
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_snapshot_15m_generator.py`
- direct functional call to `write_payload(...)` writing `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-29\_strategy_snapshots_15m_write_test.json`
Outcome:
- The `_strategy_snapshots_15m.json` writer now tolerates transient Windows file locks during atomic replace, which directly addresses the `PermissionError: [WinError 5] Access is denied` failure shown by the user.
