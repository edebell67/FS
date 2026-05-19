Source: User request in Codex thread on 2026-03-31 to prefer Kanban-based future scheduling over Codex desktop automations or Windows Task Scheduler.
Task Type: standard
Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
Task Summary: Add native future-time task gating to the workstream Kanban scheduler so tasks can declare a `Scheduled For` timestamp and remain unclaimable until that time is reached.
Context: `C:\Users\edebe\eds\workstream\run_agent.py`, `C:\Users\edebe\eds\workstream\kanban_dashboard.py`, task markdown metadata parsing, worker task selection.
Dependency: None

## Plan
- [x] 1. Inspect the active Kanban execution path and identify where task metadata is parsed and claimability is decided.
  - [x] Test: Read `workstream/run_agent.py` and the corresponding legacy worker block in `workstream/kanban_dashboard.py` to confirm the task-selection gate.
  - Evidence: Confirmed `AgentController`/`TaskGate` in `workstream/run_agent.py` are the active scheduler, while `multi_model_lane_worker` in `workstream/kanban_dashboard.py` is a legacy fallback path.
- [x] 2. Implement `Scheduled For` parsing and enforce a future-time gate in the active scheduler, with parity in the legacy fallback worker.
  - [x] Test: File diff shows scheduler metadata and runnable checks reject tasks whose scheduled time is still in the future.
  - Evidence: Added `Scheduled For` parsing plus future-time runnable checks in `workstream/run_agent.py` and mirrored backlog gating in `workstream/kanban_dashboard.py`.
- [x] 3. Run focused validation proving a future-scheduled task is blocked before its due time and runnable after its due time.
  - [x] Test: Execute a local Python check against scheduler helpers with synthetic task files representing past and future scheduled times.
  - Evidence: Validation output showed the future task was non-runnable with a `Scheduled for future execution` reason, the past task was runnable, and the scheduler selected only the past task.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\run_agent.py`, `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: The Kanban scheduler code now understands and enforces future execution times.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Inline Python validation run against `run_agent.TaskGate` using synthetic tasks in `C:\Users\edebe\eds\workstream\_tmp_sched_validate`
  - Objective-Proved: Validation proves future-scheduled tasks are deferred until their due time and released afterward.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: pending
  - Objective-Proved: Operators can schedule a task using `Scheduled For:` in the workstream and rely on the native Kanban scheduler behavior.
  - Status: planned

## Implementation Log
- 2026-03-31 21:32:49 Europe/London: Created lifecycle task for Kanban-native scheduled execution support.
- 2026-03-31 21:33 Europe/London: Confirmed `workstream/run_agent.py` is the active scheduler and `workstream/kanban_dashboard.py` only contains the disabled-by-default legacy worker fallback.
- 2026-03-31 21:34 Europe/London: Added `Scheduled For` parsing in the active scheduler and blocked task claimability until the parsed timestamp is reached.
- 2026-03-31 21:34 Europe/London: Mirrored the same future-time gate in the legacy Kanban worker loop so fallback behavior remains aligned.
- 2026-03-31 21:35 Europe/London: Validated with synthetic past/future task files that only due tasks are selected for execution.

## Changes Made
- `C:\Users\edebe\eds\workstream\run_agent.py`
  - Added parsing support for task metadata lines of the form `Scheduled For: <timestamp>`.
  - Added timezone-aware parsing that accepts ISO datetimes plus values like `2026-03-31 21:30 Europe/London`.
  - Updated `TaskGate.test_task_runnable(...)` so future-scheduled tasks remain non-runnable until their due time.
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Added matching scheduled-time parsing helpers.
  - Updated the legacy `multi_model_lane_worker(...)` backlog selection loop to treat future-scheduled tasks as not ready.

## Validation
- Read `C:\Users\edebe\eds\workstream\run_agent.py`
  - Result: Active scheduler uses `TaskGate.claim_next_task(...)` inside `AgentController._lane_worker(...)`.
- Read `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Result: Legacy internal workers remain available but are disabled by default in favor of `run_agent.py`.
- `python -m py_compile "C:\Users\edebe\eds\workstream\run_agent.py"`
  - Result: Passed.
- `python -m py_compile "C:\Users\edebe\eds\workstream\kanban_dashboard.py"`
  - Result: Passed with an existing unrelated `SyntaxWarning` at line 579 about an invalid escape sequence in the embedded HTML string.
- Inline Python scheduler validation
  - Result:
    - `future_runnable=False`
    - `future_reasons=['Scheduled for future execution: 2099-03-31T21:30:00+01:00']`
    - `past_runnable=True`
    - `selected_task=20260331_200000_test_past.md`
- User verification requested: add a real `Scheduled For:` line to a backlog task and confirm the Kanban runner does not claim it before the due time, then does claim it once the due time passes.

## Risks/Notes
- The actual scheduler of record is `workstream/run_agent.py`; `kanban_dashboard.py` still contains a legacy internal worker path that should remain behaviorally aligned.
- Time parsing should tolerate explicit timezone offsets and fall back cleanly when no `Scheduled For` field is present.
- `workstream/kanban_dashboard.py` already had unrelated local changes in the worktree before this scheduling patch; only the `Scheduled For` helper and readiness gate were added for this task.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-03-31 21:35 Europe/London


# User Feedback
User Verified: PASS
