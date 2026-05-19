Source: User report on 2026-04-01 that the scheduler is incorrectly applying the `MAX_CONCURRENT_PER_DATE` limit across the whole board rather than per model lane.

Task Type: bugfix
Project: workstream

## Objective
- Change the scheduler so the date-bucket concurrency rule is enforced per model lane, not globally across all agents.
- Unblock backlog tasks that should be runnable when a different model lane already has same-date work in progress.

## Plan
- [x] 1. Inspect the current date-bucket counting path in `workstream/run_agent.py`.
  - [x] Test: Confirm the current implementation counts in-progress tasks across all agents instead of only the current worker lane.
  - Evidence: `agent_controller_py.log` showed repeated `Bucket full for date 20260401: 2 >= 1` and `3 >= 1` skips across different workers before the fix.
- [x] 2. Patch the counting logic so the gate applies per worker lane.
  - [x] Test: Confirm same-date tasks in other lanes no longer block claim selection for the current worker.
  - Evidence: `_in_progress_count_for_date` now accepts `worker`, filters active tasks by `task.lane`, and the call site passes the current worker.
- [x] 3. Validate the scheduler module and verify the targeted backlog tasks become runnable under the corrected rule.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py` succeeds, and a direct scheduler probe shows the `20260401_*` general backlog tasks are no longer rejected by a global date bucket.
  - Evidence: compile passed, and after controller restart codex claimed `20260401_155057_claude_breakout_weekly_performance_make_all_columns_sortable.md`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `workstream/run_agent.py`
  - Objective-Proved: Proves the date-bucket scheduler logic now scopes the limit per model lane.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py`; `workstream/logs/agent_controller_py.log`; `workstream/logs/agent_worker.log`
  - Objective-Proved: Proves the patched scheduler parses and the backlog selection behavior matches the intended per-model rule.
  - Status: complete

## Implementation Log
- 2026-04-01 16:41:15 Europe/London: Task created to fix the date-bucket limit scope in `workstream/run_agent.py`.
- 2026-04-01 16:41:xx Europe/London: Confirmed the live controller was rejecting `20260401_*` backlog candidates globally with `Bucket full for date 20260401: 2 >= 1` rather than per lane.
- 2026-04-01 16:42:xx Europe/London: Patched `run_agent.py` so date-bucket counting is filtered to the current worker lane.
- 2026-04-01 16:42:27 Europe/London: Restarted the controller to load the patched scheduler logic.
- 2026-04-01 16:42:40 Europe/London: Verified codex claimed the previously blocked `20260401_155057_*` backlog task under the corrected rule.

## Changes Made
- Updated `_in_progress_count_for_date` in `workstream/run_agent.py` to accept the current `worker` and only count active in-progress tasks whose `task.lane` matches that worker.
- Updated the candidate gating call site to pass the current worker into `_in_progress_count_for_date`.
- Restarted the live controller so the running scheduler process picked up the corrected logic.

## Validation
- `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py`
  - Result: pass
- Direct scheduler probe after patch
  - Result: `TaskGate().select_next_runnable_task("codex")` returned `20260401_155057_claude_breakout_weekly_performance_make_all_columns_sortable.md`
- Log verification before fix
  - `workstream/logs/agent_controller_py.log` contained repeated `Bucket full for date 20260401: 2 >= 1` and `3 >= 1` entries across workers.
- Log verification after restart
  - `workstream/logs/agent_controller_py.log` shows `AI Agent Controller Starting: 20260401_164227`
  - `workstream/logs/agent_controller_py.log` shows `Selected dedicated task: 20260401_155057_claude_breakout_weekly_performance_make_all_columns_sortable.md`
  - `workstream/logs/agent_worker.log` shows `[CODEX] claimed C:\Users\edebe\eds\workstream\200_inprogress\codex\20260401_155057_claude_breakout_weekly_performance_make_all_columns_sortable.md`

## Risks/Notes
- This fix must preserve the in-progress-per-lane cap while removing the unintended global cross-lane block.
- The live controller may need a restart after the code fix for the running process to use the patched logic.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-01 16:43:30 Europe/London
