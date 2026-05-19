## Objective

Update persistent retry workers so each retry appends its identified issues and attempt outcome into the same task file before requeue, allowing the next run to build on the prior run's findings.

## Task Attributes

- project: workstream
- task_type: implementation
- area: scheduler
- priority: high
- status: todo

## Plan

1. Update persistent worker retry handling in `workstream\run_agent.py`.
2. Append retry findings into the same task file on each unresolved or failed run.
3. Preserve enough context for the next retry to take a different path if possible.
4. Validate the file-update behavior and Python compilation.

## Progress Log

- 2026-04-03 21:23:10 Added persistent retry log helpers to `workstream\run_agent.py`.
- 2026-04-03 21:23:54 Wired persistent worker requeue paths to pass the latest result artifact into the same task file.
- 2026-04-03 21:24:02 Validated helper behavior with a temporary simulated result artifact, confirmed log insertion, then removed the temporary simulated entry from the live Reddit task file.
- 2026-04-03 21:24:36 Revalidated Python compilation after the change.

## Changes Made

- Updated [run_agent.py](C:\Users\edebe\eds\workstream\run_agent.py)
  - persistent workers now append retry notes into the same task file
  - each appended note includes:
    - attempt timestamp
    - attempt outcome
    - next retry timestamp
    - latest result artifact path when available
    - summarized findings extracted from the latest result markdown
  - notes are written under a `## Persistent Retry Log` section
  - `Last Attempted` and `Last Attempt Outcome` metadata are also updated in the task file

## Validation

Commands run:

```powershell
python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py
```

```powershell
python -c "from pathlib import Path; import sys; sys.path.insert(0, r'C:\Users\edebe\eds\workstream'); import run_agent; task=Path(r'C:\Users\edebe\eds\workstream\100_backlog\general\20260403_230000_distribution_tt_reddit_connection_and_posting_loop.md'); result=Path(r'C:\Users\edebe\eds\temp_retry_result.md'); result.write_text('Error: missing Reddit client secret\nReason: OAuth app not configured\n', encoding='utf-8'); meta=run_agent.parse_task_metadata(task,'todo'); run_agent._update_persistent_worker_attempt(task, 'requeued_active', run_agent._compute_next_scheduled_for(meta), result_path=result); print('updated')"
```

Observed behavior:
- `run_agent.py` compiles successfully
- the helper appended a `## Persistent Retry Log` entry into the same task file with summarized findings
- the temporary simulation artifact and temporary simulated log entry were removed after validation so the live Reddit task remains clean until a real run writes to it

## Outcome

Completed successfully.

Persistent retry workers now carry forward identified issues in the same task file, so each next run has more context than the last one.
