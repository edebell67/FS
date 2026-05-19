# Fix Single Slot Worker Refill Behavior

## Metadata
- Project: workstream
- Task: fix_single_slot_worker_refill_behavior
- Started: 2026-03-22 00:19:00
- Status: complete

## Source
- User request in Codex thread on 2026-03-22 to fix the behavior reviewed in `20260322_000500_workstream_review_single_slot_worker_refill_behavior.md`.

## Task Summary
Implement the reviewed scheduler fixes so the system uses a single orchestration path, avoids retry pinning into model-specific backlog lanes, and distributes shared backlog refill more predictably across available workers.

## Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\run_agent.py`

## Dependency
Dependency: `C:\Users\edebe\eds\workstream\300_complete\20260322_000500_workstream_review_single_slot_worker_refill_behavior.md`

## Plan
- [x] 1. Remove duplicate scheduling so the dashboard does not run a second worker scheduler by default.
  - Test: Verify the dashboard still launches the controller, but internal lane workers are no longer started unless explicitly enabled.
  - Evidence: Updated dashboard startup so `run_agent.py` remains the active scheduler and internal lane workers only start when `KANBAN_USE_INTERNAL_LANE_WORKERS` is explicitly enabled.
- [x] 2. Change failed-task retry routing back to general backlog.
  - Test: Confirm retry logic now moves failed tasks into `100_backlog/general`.
  - Evidence: `_auto_retry_failed_task()` now appends retry history and moves retries into `100_backlog/general`.
- [x] 3. Improve fairness in `run_agent.py` for shared/general backlog claims.
  - Test: Confirm shared/general tasks are claimed using a rotating turn instead of pure per-worker preference polling.
  - Evidence: `TaskGate` now tracks a shared-worker turn and rotates general/shared claims across available workers.
- [x] 4. Validate the updated modules.
  - Test: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`
  - Evidence: Both modules compile successfully after the scheduler changes; only the pre-existing dashboard `SyntaxWarning` remains.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: Duplicate internal lane scheduling is disabled by default and retries now return to `100_backlog/general`.
  - Status: verified
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Shared/general backlog claims now use rotating turn-based selection across workers.
  - Status: verified
- Evidence-Type: command
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Updated modules compile successfully.
  - Status: verified
- Evidence-Type: command
  - Artifact: Workspace validation script for `_auto_retry_failed_task()`
  - Objective-Proved: Retry routing moved a failed task into `100_backlog/general` with updated retry history.
  - Status: verified
- Evidence-Type: command
  - Artifact: Workspace validation script for `run_agent.TaskGate`
  - Objective-Proved: Shared claims rotated across `gemini`, `codex`, and `claude` in turn order.
  - Status: verified

## Execution Notes
- 2026-03-22 00:31: Disabled dashboard internal lane workers by default so `run_agent.py` is the sole task scheduler unless `KANBAN_USE_INTERNAL_LANE_WORKERS` is explicitly enabled.
- 2026-03-22 00:32: Updated dashboard failed-task retry logic to send retries to `100_backlog/general` instead of model-specific backlog lanes.
- 2026-03-22 00:34: Added shared-task round-robin handling in `run_agent.TaskGate` so general backlog work rotates across available workers.
- 2026-03-22 00:36: Validated retry routing and round-robin claim behavior with direct workspace scripts.

## Validation
- [x] Confirm duplicate worker scheduling is disabled by default.
- [x] Confirm retries route back to `100_backlog/general`.
- [x] Confirm shared claim logic uses rotation.
- [x] Run `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`.
