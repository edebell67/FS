Source: User clarification on 2026-04-01 that recurring tasks must advance to the next expected schedule slot rather than drifting to the repair time.
Task Type: bugfix
Project: workstream

## Objective
- Keep recurring tasks anchored to their configured cadence.
- Ensure a failed `01:00` run records the next due time as `05:00`, not the next future wall-clock slot at repair time.
- Preserve the failed task record while creating the next expected execution copy.

## Plan
- [x] 1. Update recurring-slot calculation in `run_agent.py`.
- [x] 2. Repair the live Twitter recurring task so the failed `01:00` record points to `05:00`.
- [x] 3. Replace the incorrectly generated `13:00` follow-up with the correct `05:00` follow-up task.
- [x] 4. Restart the scheduler so the anchored recurrence logic is live.

## Implementation Log
- 2026-04-01 12:06 Europe/London: Confirmed the current repair incorrectly advanced recurrence to `13:00` because it walked forward to the current time.
- 2026-04-01 12:08 Europe/London: Updated recurrence calculation to advance by exactly one interval from the current task's scheduled slot.
- 2026-04-01 12:09 Europe/London: Updated the failed `01:00` task record so `Next Scheduled For` is `05:00`.
- 2026-04-01 12:10 Europe/London: Replaced the incorrect `13:00` backlog follow-up with the correct `05:00` follow-up task.
- 2026-04-01 12:11 Europe/London: Restarted the scheduler controller. Current `agent.lock` PID is `29580`.

## Validation
- `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py`
- Confirmed `C:\Users\edebe\eds\workstream\200_inprogress\blocker\gemini\20260401_010000_breakout_twitter_summary_returns_every_4_hours.md` contains `Next Scheduled For: 2026-04-01 05:00:00+01:00`
- Confirmed `C:\Users\edebe\eds\workstream\100_backlog\general\20260401_050000_breakout_twitter_summary_returns_every_4_hours.md` exists
- Confirmed the incorrect `C:\Users\edebe\eds\workstream\100_backlog\general\20260401_130000_breakout_twitter_summary_returns_every_4_hours.md` no longer exists

## Risks/Notes
- The Twitter/X session remains invalid, so overdue recurring tasks can still block until the operator refreshes the login session.
