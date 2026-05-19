## Objective

Add persistent worker retry limits so a task can specify a maximum retry count and the same task file counts down remaining retries from that number to `0`.

## Task Attributes

- project: workstream
- task_type: implementation
- area: scheduler
- priority: high
- status: todo

## Plan

1. Extend persistent worker metadata parsing to support max retry count and remaining retry count.
2. Update requeue behavior to decrement the remaining retry count on each retry.
3. Stop requeueing once the countdown reaches `0`.
4. Validate parsing, countdown mutation, and Python compilation.

## Progress Log

- 2026-04-03 21:28:42 Added max-retry metadata support to `workstream\run_agent.py`.
- 2026-04-03 21:29:31 Updated persistent worker requeue handling so remaining retries count down toward `0`.
- 2026-04-03 21:30:04 Updated the live Reddit persistent worker task to start with `max_retry_attempts: 30` and `remaining_retry_attempts: 30`.
- 2026-04-03 21:30:36 Validated parsing, decrement behavior, and Python compilation.

## Changes Made

- Updated [run_agent.py](C:\Users\edebe\eds\workstream\run_agent.py)
  - added support for:
    - `max_retry_attempts`
    - `remaining_retry_attempts`
  - persistent workers now:
    - decrement remaining retries on each requeue
    - write the updated remaining count back into the same task file
    - stop requeueing when remaining retries reaches `0`
    - record the countdown value in the persistent retry log

- Updated [20260403_230000_distribution_tt_reddit_connection_and_posting_loop.md](C:\Users\edebe\eds\workstream\100_backlog\general\20260403_230000_distribution_tt_reddit_connection_and_posting_loop.md)
  - set:
    - `max_retry_attempts: 30`
    - `remaining_retry_attempts: 30`

## Validation

Commands run:

```powershell
python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py
```

```powershell
python -c "from pathlib import Path; import sys; sys.path.insert(0, r'C:\Users\edebe\eds\workstream'); import run_agent; p=Path(r'C:\Users\edebe\eds\workstream\100_backlog\general\20260403_230000_distribution_tt_reddit_connection_and_posting_loop.md'); m=run_agent.parse_task_metadata(p,'todo'); print({'max_retry_attempts': m.max_retry_attempts, 'remaining_retry_attempts': m.remaining_retry_attempts}); print('effective', run_agent._effective_remaining_retries(m)); print('decremented', run_agent._decrement_retry_count(m))"
```

Results:
- `run_agent.py` compiles successfully
- The Reddit task parses as:
  - `max_retry_attempts=30`
  - `remaining_retry_attempts=30`
- Countdown logic works:
  - current effective retries = `30`
  - next retry count = `29`

## Outcome

Completed successfully.

Persistent retry workers can now be bounded with a countdown that decreases from the configured retry limit to `0`.
