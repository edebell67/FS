# Reduce Kanban Task Loading To Single Slot

## Metadata
- Project: workstream
- Task: reduce_kanban_task_loading_to_single_slot
- Started: 2026-03-21 21:45:04
- Status: complete

## Source
- User request in Codex thread on 2026-03-21 to change the kanban so it only loads one item at a time and refills a slot with one item when available.

## Task Summary
Reduce kanban/controller concurrency so only one active task is loaded at a time, with refill behavior limited to a single new task whenever the active slot becomes free.

## Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\run_agent.py`

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect the current concurrency gates in both the dashboard worker loop and the standalone agent controller.
  - [x] Test: Locate the active concurrency constants and claim guards.
  - [x] Evidence: Identified `MAX_CONCURRENT_INPROGRESS_TASKS = 3` in `kanban_dashboard.py` and `MAX_CONCURRENT_PER_DATE = 3` in `run_agent.py`, with both used as task-claim guards.
- [x] 2. Update both code paths to enforce a single active slot.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`
  - [x] Evidence: Updated both concurrency constants to `1`; modules compile successfully.
- [x] 3. Validate the effective configuration values after the change.
  - [x] Test: Direct import check confirms the concurrency constants resolve to `1` in both modules.
  - [x] Evidence: Output shows `MAX_CONCURRENT_INPROGRESS_TASKS=1` and `MAX_CONCURRENT_PER_DATE=1`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\kanban_dashboard.py`, `C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Both kanban execution paths are configured for single-slot active loading.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: The updated modules parse successfully after the concurrency change.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: Direct import checks reported `MAX_CONCURRENT_INPROGRESS_TASKS=1` and `MAX_CONCURRENT_PER_DATE=1`.
  - Objective-Proved: Runtime configuration now resolves to one active slot in both controller paths.
  - Status: captured

## Lifecycle Log
### 2026-03-21 21:45:04
- Created lifecycle record for reducing kanban task loading to a single active slot.

### 2026-03-21 21:45:20
- Inspected the dashboard and standalone agent controller concurrency gates.
- Confirmed both execution paths were previously configured to allow three concurrent claims.

### 2026-03-21 21:45:40
- Updated `kanban_dashboard.py` to set `MAX_CONCURRENT_INPROGRESS_TASKS = 1`.
- Updated `run_agent.py` to set `MAX_CONCURRENT_PER_DATE = 1`.

### 2026-03-21 21:46:00
- Ran syntax validation and direct import checks.
- Confirmed both modules now resolve their concurrency settings to `1`.

## Validation
- [x] Locate the current concurrency gates.
- [x] Run `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`.
- [x] Confirm the resolved concurrency values are both `1`.
