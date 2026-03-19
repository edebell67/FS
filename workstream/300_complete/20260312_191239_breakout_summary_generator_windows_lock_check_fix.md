Source:
- User-reported runtime failure on 2026-03-12:
  - `summary_net_generator.py`
  - `os.kill(pid, 0)`
  - `OSError: [WinError 87] The parameter is incorrect`

Task Summary:
- Fix the Windows lock-file process existence check in `TradeApps/breakout/fs/summary_net_generator.py` so the generator no longer crashes when validating whether another instance is running.

Context:
- Target file: `TradeApps/breakout/fs/summary_net_generator.py`
- Current failure occurs in `SummaryGenerator.run()` during stale lock detection.
- Windows-specific behavior makes `os.kill(pid, 0)` unreliable in this path.

Plan:
- [x] 1. Move this lifecycle file to in-progress and inspect the failing lock-check logic.
  - [x] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and identify the exact failing code path in `summary_net_generator.py`.
  - Evidence: Lifecycle file moved to `workstream/200_inprogress/20260312_191239_breakout_summary_generator_windows_lock_check_fix.md`; failure confirmed in `SummaryGenerator.run()` at the stale lock check using `os.kill(pid, 0)`.
- [x] 2. Replace the lock check with a Windows-safe process existence check while preserving single-instance behavior.
  - [x] Test: Review `summary_net_generator.py` and confirm `run()` no longer uses raw `os.kill(pid, 0)` on Windows.
  - Evidence: Added `is_process_alive(pid)` helper using `OpenProcess` and `GetExitCodeProcess` on Windows with non-Windows fallback to `os.kill(pid, 0)`; `run()` now calls the helper before aborting for an active lock owner.
- [x] 3. Validate the updated file with targeted parsing/runtime checks and archive this lifecycle file.
  - [x] Test: Run a targeted check that imports or executes the new process-alive helper against the current platform without raising `WinError 87`.
  - Evidence: `python -m py_compile TradeApps\breakout\fs\summary_net_generator.py` passed; targeted helper test returned `current_pid_alive=True` and `invalid_pid_alive=False`.

Implementation Log:
- 2026-03-12 19:12:39: Task file created in `workstream/100_todo`.
- 2026-03-12 19:13:00: Task file moved to `workstream/200_inprogress`.
- 2026-03-12 19:15:00: Inspected the generator lock-file path and confirmed Windows failure at `os.kill(pid, 0)`.
- 2026-03-12 19:18:00: Added a Windows-safe process-alive helper and updated the stale-lock check to use it.
- 2026-03-12 19:19:00: Ran parse and helper validation successfully.

Changes Made:
- Updated `TradeApps/breakout/fs/summary_net_generator.py`.

Validation:
- `python -m py_compile TradeApps\breakout\fs\summary_net_generator.py`
  - Result: PASS
- Targeted helper validation:
  - Command: inline Python import of `summary_net_generator.py`, then `is_process_alive(os.getpid())` and `is_process_alive(-1)`
  - Result: `current_pid_alive=True`, `invalid_pid_alive=False`

Risks/Notes:
- The fix must not break stale-lock cleanup or allow multiple generator instances to run concurrently.
- The helper only checks whether the PID is alive; it does not distinguish unrelated processes reusing a stale PID, which matches the prior lock-file behavior.

Completion Status:
- Complete on 2026-03-12 19:19:00.
