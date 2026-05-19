Source: User request in Codex thread on 2026-03-31 to create and implement recurring scheduling natively in the Kanban/workstream engine.
Task Type: standard
Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
Task Summary: Extend the Kanban-native scheduler so a completed scheduled task can automatically spawn its next backlog instance based on recurrence metadata.
Context: `C:\Users\edebe\eds\workstream\run_agent.py`, recurring Twitter/posting tasks under `workstream`, task markdown metadata and completion flow.
Dependency: `C:\Users\edebe\eds\workstream\200_inprogress\20260331_213249_workstream_add_kanban_scheduled_for_execution.md`

## Plan
- [x] 1. Inspect the task completion path and define the minimal recurrence metadata needed for native Kanban rescheduling.
  - [x] Test: Read `workstream/run_agent.py` around task completion and confirm where the next occurrence should be created.
  - Evidence: Confirmed the correct spawn point is the successful completion path in `AgentController._lane_worker(...)` after agent execution returns output.
- [x] 2. Implement recurring-task parsing plus next-instance spawning after successful completion.
  - [x] Test: File diff shows recurring metadata is parsed and a new backlog task with an updated `Scheduled For` timestamp is created only after success.
  - Evidence: Added recurring metadata parsing and `_spawn_next_recurring_instance(...)` logic in `workstream/run_agent.py`, hooked into the success path only.
- [x] 3. Validate recurring behavior with a synthetic task that proves the next scheduled instance is created correctly.
  - [x] Test: Execute a local Python validation that simulates completion of a recurring task and inspects the spawned backlog file.
  - Evidence: Validation output showed a next backlog instance was created at `20260401_033000_test_recurring.md` with `Scheduled For: 2026-04-01T03:30:00+01:00`.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: The workstream scheduler can now reschedule recurring tasks natively.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Inline Python validation run against `run_agent.py` recurrence helpers using `C:\Users\edebe\eds\workstream\_tmp_recur_validate`
  - Objective-Proved: A completed recurring task spawns its next scheduled backlog instance with the correct timing.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: pending
  - Objective-Proved: Operators can mark a task as recurring and observe the next occurrence appear automatically after completion.
  - Status: planned

## Implementation Log
- 2026-03-31 23:28:12 Europe/London: Created lifecycle task for Kanban recurring rescheduling support.
- 2026-03-31 23:29 Europe/London: Confirmed the next occurrence should be created only after a successful completion in `run_agent.py`, not at claim time.
- 2026-03-31 23:30 Europe/London: Added recurring metadata parsing using `recurring_task: true` plus `recurrence_interval_hours: <n>`.
- 2026-03-31 23:31 Europe/London: Implemented next-instance spawning so a completed recurring task creates a new backlog task with an updated `Scheduled For` timestamp.
- 2026-03-31 23:31 Europe/London: Validated the recurrence helper with a synthetic task and confirmed the next instance was created in the expected backlog lane.

## Changes Made
- `C:\Users\edebe\eds\workstream\run_agent.py`
  - Added parsing for task metadata lines `recurring_task: true` and `recurrence_interval_hours: <hours>`.
  - Added helper logic to compute the next scheduled time from the prior `Scheduled For` timestamp and interval, advancing until it lands in the future.
  - Added recurring-instance spawning on successful completion only, preserving the completed original task and writing the next run as a new backlog task file.
  - New spawned tasks retain recurrence metadata, update `Scheduled For`, and record `Spawned From: <previous task>`.

## Validation
- Read `C:\Users\edebe\eds\workstream\run_agent.py`
  - Result: Confirmed the success path after `process.communicate(...)` is the correct place to create the next recurring occurrence.
- `python -m py_compile "C:\Users\edebe\eds\workstream\run_agent.py"`
  - Result: Passed.
- Inline Python recurrence validation
  - Result:
    - `spawned_exists=True`
    - `spawned_name=20260401_033000_test_recurring.md`
    - `spawned_scheduled_for=2026-04-01T03:30:00+01:00`
    - `spawned_recurring=True`
    - `spawned_interval_hours=6`
    - `spawned_from_present=True`
- User verification requested: complete a real recurring task containing `recurring_task: true`, `recurrence_interval_hours: 6`, and `Scheduled For: ...`, then confirm the next backlog instance appears automatically with the next due time.

## Risks/Notes
- Recurrence should only spawn the next instance after a successful completion, not after failure or while a task is still in progress.
- The recurrence metadata needs to stay simple enough to fit the existing markdown task model.
- The active scheduler is `workstream/run_agent.py`; recurring rescheduling was implemented there. The legacy internal worker path in `kanban_dashboard.py` was not extended for recurrence because it is disabled by default in current operation.
- `workstream/run_agent.py` already had unrelated local modifications in the worktree before this recurrence patch; the recurring metadata parse and completion-spawn hook are the changes for this task.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-03-31 23:31 Europe/London


# User Feedback
User Verified: PASS
