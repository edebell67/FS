# Task: Fix Recurring Auto-Promote Task Spawn Semantics

## Source
- Source Task: `C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260407_160000_breakout_weekly_perf_auto_promote_toggle.md`
- User Directive: 2026-04-08

## Task Type
standard

## Task Attributes
recurring_task: true
recurrence_type: scheduled
recurrence_rule: interval
looping_task: false
splittable_task: false
workflow_task: false

## Task Summary
Implement the recurring-task execution model for the breakout weekly performance auto-promote toggle workflow so the task runs every 4 hours. At the moment an eligible scheduled instance starts execution, the system must create the next future-dated backlog instance scheduled 4 hours later. The currently executing instance must then continue through normal execution and move to `300_complete` if successful, rather than being reused as the future scheduled copy.

## Context
- Existing lifecycle records currently show conflicting state placement for the same task file:
  - `C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260407_160000_breakout_weekly_perf_auto_promote_toggle.md`
  - `C:\Users\edebe\eds\workstream\300_complete\gemini\20260407_160000_breakout_weekly_perf_auto_promote_toggle.md`
- Workstream lifecycle rules are defined in `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`.
- Backlog lanes available under `C:\Users\edebe\eds\workstream\100_backlog\`.
- The required behavioral correction is:
  - recurring cadence is every 4 hours;
  - execution start spawns the next scheduled instance;
  - the executing instance completes normally and is archived independently.

## Destination Folder
C:\Users\edebe\eds\workstream\

## Dependency
Dependency: None

## Plan
- [ ] 1. Identify the scheduler or lifecycle code path that currently handles recurring task promotion and instance creation for workstream task files.
  - Test: `rg -n "recurring_task|recurrence_rule|100_backlog|200_inprogress|300_complete|spawn.*instance|next.*instance" C:\Users\edebe\eds`
  - Evidence: Search results captured showing the authoritative recurring-task execution path and target files to update.
- [ ] 2. Implement recurring execution semantics so an execution-ready instance creates a new backlog copy scheduled 4 hours ahead at execution start, without mutating the active instance into the future copy.
  - Test: Code inspection of the updated implementation shows a distinct branch for "spawn next scheduled instance" before normal completion handling, with the next instance timestamp advanced by 4 hours.
  - Evidence: File diff captured showing the spawn-on-execution logic and timestamp calculation.
- [ ] 3. Update lifecycle handling so the executing task instance can move to `300_complete` independently after successful execution while the spawned future instance remains in backlog.
  - Test: Run a controlled simulation or targeted script invocation that starts a recurring instance and verify the result is exactly one new future backlog task plus one completed current instance.
  - Evidence: Validation output captured with resulting file paths and state transitions.
- [ ] 4. Validate the fix against the breakout auto-promote recurring-task expectation and document the recurrence behavior in the lifecycle record.
  - Test: Manual review confirms the lifecycle narrative states "spawn next instance at execution start, then complete current instance normally" and the recurrence interval is 4 hours.
  - Evidence: Final lifecycle notes and validation summary captured in this file.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: planned
  - Objective-Proved: code changes implementing spawn-on-execution recurring task behavior
  - Status: planned
- Evidence-Type: test_output
  - Artifact: planned
  - Objective-Proved: recurring execution produces one completed current instance and one future backlog instance
  - Status: planned
- Evidence-Type: file_output
  - Artifact: planned
  - Objective-Proved: resulting task files exist in the correct lifecycle folders with correct future timestamping
  - Status: planned

## Implementation Log
- 2026-04-08 12:12:03: Created backlog task to implement recurring-task spawn semantics for the breakout weekly auto-promote workflow.
- 2026-04-08 12:12:03: Recorded required behavior: every 4 hours, next instance is spawned at execution start, current instance completes independently.

## Changes Made
- Created lifecycle task file `C:\Users\edebe\eds\workstream\100_backlog\codex\20260408_121203_breakout_recurring_auto_promote_task_spawn_fix.md`.

## Validation
- Verified lifecycle skill requirements from `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`.
- Verified backlog lane availability under `C:\Users\edebe\eds\workstream\100_backlog\`.
- Identified conflicting prior lifecycle state for the existing auto-promote task, supporting the need for a dedicated implementation task.

## Risks/Notes
- The existing recurring-task model may already be shared by other workstreams; implementation should avoid introducing duplicate spawn behavior for unrelated tasks.
- Timestamping and filename identity rules must preserve one-file-per-instance while avoiding collisions when multiple recurring tasks trigger near the same time.
- If the orchestration currently treats recurrence as "move same file back to backlog", migration logic may be needed for already-active recurring tasks.

## Completion Status
- State: BACKLOG
- Timestamp: 2026-04-08 12:12:03
