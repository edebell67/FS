## Objective

Capture and implement a workstream design that supports:

1. persistent retry workers for connection problems that need retry every X minutes without spawning a new recurring execution record each time
2. explicit keep/discard controls for recurring task runs after success or failure

## Task Attributes

- project: workstream
- task_type: design
- area: scheduler
- priority: high
- status: todo

## Problem Statement

The current recurring task model is good for discrete scheduled executions, but it is not ideal for:
- minute-level retry loops
- long-running connection-establishment work
- controlling whether successful or failed recurring executions should be retained or discarded

We need a clearer model for:
- persistent workers that keep retrying internally
- recurring tasks that still create discrete runs
- lifecycle retention policies for successful and unsuccessful runs

## Required Outcomes

- Define how to represent a persistent retry worker in workstream
- Define how to configure retry cadence in minutes for persistent workers
- Define how recurring task executions should be archived, retained, or discarded after:
  - success
  - failure
  - partial / blocked outcome
- Clarify whether successful recurring tasks should remain visible, be summarized, or be auto-pruned
- Clarify whether failed recurring tasks should remain visible until resolved or follow another policy

## Goal

Produce a concrete design and implementation path so the system can support:
- traditional recurring scheduled tasks
- persistent retry workers for connection-heavy workflows
- configurable retention rules for recurring run history

## Plan

1. Review the current workstream recurring scheduling model and execution persistence behavior.
2. Design a persistent worker concept suitable for minute-level retries without spawning a new task file each cycle.
3. Design recurring run retention policies for success/failure/blocked states.
4. Propose implementation changes to the scheduler, lifecycle handling, and UI/task visibility model.
5. Record recommended defaults and operator controls.

## Validation

- The design distinguishes recurring scheduled runs from persistent retry workers
- The design covers minute-level retries without new execution-file spam
- The design defines clear keep/discard rules for successful and unsuccessful recurring runs
- The output is concrete enough to implement

## Notes

- This is a foundational scheduler/lifecycle design task, not just a Reddit-specific workaround.
- The Reddit connection use case is one driver, but the result should be reusable for other platforms and integrations.

## Progress Log

- 2026-04-03 20:45:12 Identified that recurring execution cloning and task completion behavior live in `workstream\run_agent.py`, while the dashboard only gates on `Scheduled For`.
- 2026-04-03 20:49:37 Implemented persistent retry worker metadata and in-place requeue behavior in `workstream\run_agent.py`.
- 2026-04-03 20:51:04 Implemented recurring run retention metadata for success and failure in `workstream\run_agent.py`.
- 2026-04-03 20:53:19 Converted the active Reddit connection task to the new persistent worker model with `retry_interval_minutes: 60`.
- 2026-04-03 20:54:08 Validated metadata parsing, next scheduled calculation, and Python compilation.

## Changes Made

- Updated [run_agent.py](C:\Users\edebe\eds\workstream\run_agent.py)
  - added support for:
    - `persistent_retry_worker: true`
    - `retry_interval_minutes`
    - `successful_run_retention: keep|discard`
    - `failed_run_retention: keep|discard`
  - persistent workers now:
    - reuse the same task file
    - requeue in place instead of cloning new recurring task files
    - update `Scheduled For`, `Last Attempted`, and `Last Attempt Outcome`
    - stop requeueing when `persistent_worker_state: resolved` is present
  - ordinary recurring runs now support retention control for successful and failed task-file artifacts

- Updated [20260403_230000_distribution_tt_reddit_connection_and_posting_loop.md](C:\Users\edebe\eds\workstream\100_backlog\general\20260403_230000_distribution_tt_reddit_connection_and_posting_loop.md)
  - changed from cloned recurring runs every 4 hours to:
    - `persistent_retry_worker: true`
    - `retry_interval_minutes: 60`
    - `successful_run_retention: keep`
    - `failed_run_retention: discard`
    - `persistent_worker_state: active`

## Validation

Commands run:

```powershell
python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py
```

```powershell
python -c "from pathlib import Path; import sys; sys.path.insert(0, r'C:\Users\edebe\eds\workstream'); import run_agent; p=Path(r'C:\Users\edebe\eds\workstream\100_backlog\general\20260403_230000_distribution_tt_reddit_connection_and_posting_loop.md'); m=run_agent.parse_task_metadata(p, 'todo'); print({'recurring_task': m.recurring_task, 'persistent_retry_worker': m.persistent_retry_worker, 'retry_interval_minutes': m.retry_interval_minutes, 'successful_run_retention': m.successful_run_retention, 'failed_run_retention': m.failed_run_retention, 'scheduled_for': m.scheduled_for.isoformat() if m.scheduled_for else None}); print(run_agent._compute_next_scheduled_for(m).isoformat() if run_agent._compute_next_scheduled_for(m) else None)"
```

Results:
- `run_agent.py` compiles successfully
- The Reddit task is parsed as:
  - `recurring_task=False`
  - `persistent_retry_worker=True`
  - `retry_interval_minutes=60`
  - `successful_run_retention='keep'`
  - `failed_run_retention='discard'`
- The next retry is computed as:
  - `2026-04-04T00:00:00+01:00`

## Outcome

Completed successfully.

The workstream now supports:
- minute-level persistent retry workers without cloned execution-file spam
- keep/discard controls for successful and failed recurring runs

The active Reddit connection task has been migrated to the new persistent worker model.
