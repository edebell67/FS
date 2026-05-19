## Objective

Make the persistent worker retry limit generic across the scheduler and set the default maximum retry count to `60` for any persistent worker task that does not specify an explicit retry cap.

## Task Attributes

- project: workstream
- task_type: implementation
- area: scheduler
- priority: high
- status: todo

## Plan

1. Update persistent worker retry logic in `run_agent.py`.
2. Apply a default max retry value of `60` when none is explicitly set.
3. Keep explicit task-level overrides working.
4. Validate parsing and default countdown behavior.

## Progress Log

- 2026-04-03 21:31:48 Added a scheduler-level default persistent worker retry cap to `workstream\run_agent.py`.
- 2026-04-03 21:32:26 Validated that explicit task-level retry settings still override the default.
- 2026-04-03 21:32:48 Validated that a persistent worker without explicit retry metadata now defaults to `60`.

## Changes Made

- Updated [run_agent.py](C:\Users\edebe\eds\workstream\run_agent.py)
  - added `DEFAULT_PERSISTENT_WORKER_MAX_RETRIES = 60`
  - persistent workers now inherit a default retry cap of `60` if:
    - `max_retry_attempts` is not set
    - `remaining_retry_attempts` is not set
  - explicit task metadata still takes precedence

## Validation

Commands run:

```powershell
python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py
```

```powershell
python -c "from pathlib import Path; import sys, tempfile; sys.path.insert(0, r'C:\Users\edebe\eds\workstream'); import run_agent; p=Path(r'C:\Users\edebe\eds\workstream\100_backlog\general\20260403_230000_distribution_tt_reddit_connection_and_posting_loop.md'); m=run_agent.parse_task_metadata(p,'todo'); print('explicit', run_agent._effective_remaining_retries(m)); tmp=Path(tempfile.gettempdir())/'persistent_worker_default_test.md'; tmp.write_text('Task Type: standard\n\nTask Attributes:\n- recurring_task: false\n- persistent_retry_worker: true\n- retry_interval_minutes: 2\n- priority: high\n', encoding='utf-8'); m2=run_agent.parse_task_metadata(tmp,'todo'); print('default', run_agent._effective_remaining_retries(m2)); tmp.unlink()"
```

Results:
- `run_agent.py` compiles successfully
- Explicit override case:
  - Reddit task effective retries = `30`
- Default case:
  - unspecified persistent worker effective retries = `60`

## Outcome

Completed successfully.

Persistent worker retry limits are now generic across the scheduler, with a default cap of `60` retries unless a task explicitly overrides it.
