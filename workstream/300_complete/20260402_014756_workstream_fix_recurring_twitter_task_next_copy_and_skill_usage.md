Source: User request on 2026-04-02 that `20260401_170000_breakout_twitter_summary_returns_every_4_hours.md` must always keep the next scheduled recurring copy in `100_backlog`, and each run must explicitly use `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`.

Task Type: bugfix
Project: workstream

## Objective
- Ensure the Twitter summary recurring task always has the next scheduled copy ready in `100_backlog` instead of waiting until the current run finishes.
- Ensure this recurring task chain explicitly references and carries forward `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`.
- Keep the recurrence anchored to the task's intended execution owner rather than a transient rebalance lane.

## Plan
- [x] 1. Inspect recurring spawn timing and owner-selection behavior in `workstream/run_agent.py`.
  - [x] Test: Confirm the next instance is currently spawned only after completion and that owner selection can follow the current lane.
  - Evidence: `_spawn_next_recurring_instance()` was called only after agent execution finished, and `_recurrence_target_agent()` preferred `metadata.lane` over `metadata.suggested_agent`.
- [x] 2. Patch recurring claim/spawn logic so the next instance is ensured as soon as a recurring task is claimed, and normalize the Twitter task content to include the canonical posting skill.
  - [x] Test: Confirm the current recurring task path gains a `Required Skill` reference and that future spawned copies inherit it.
  - Evidence: `20260402_050000_breakout_twitter_summary_returns_every_4_hours.md` now contains `Required Skill: C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`, and spawned copies inherit the same line.
- [x] 3. Repair the live Twitter recurring chain so a next scheduled backlog copy exists now.
  - [x] Test: Confirm a `20260402_090000_*breakout_twitter_summary_returns_every_4_hours.md` copy exists in `100_backlog` with the required skill reference.
  - Evidence: `C:\Users\edebe\eds\workstream\100_backlog\general\20260402_090000_breakout_twitter_summary_returns_every_4_hours.md` exists and includes the required skill reference.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Proves the recurring scheduling and task normalization behavior were corrected in code.
  - Status: complete
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\100_backlog\general\20260402_090000_breakout_twitter_summary_returns_every_4_hours.md`
  - Objective-Proved: Proves the repaired live backlog copy exists with the correct next scheduled timestamp and skill reference.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py`; direct import-and-call verification; `C:\Users\edebe\eds\workstream\logs\agent_controller_py.log`
  - Objective-Proved: Proves the scheduler module still parses and the recurrence target/claim behavior is stable.
  - Status: complete

## Implementation Log
- 2026-04-02 01:47:56 Europe/London: Task created to fix recurring Twitter task next-copy availability and skill usage.
- 2026-04-02 01:48 Europe/London: Confirmed the scheduler only spawned recurring copies after completion and that owner selection could follow the transient lane.
- 2026-04-02 01:49 Europe/London: Patched `run_agent.py` to normalize the Twitter recurring task with a required canonical posting skill line, prefer `Suggested Agent` for recurrence target selection, and ensure the next recurring copy is created as soon as the task is claimed.
- 2026-04-02 01:49 Europe/London: Repaired the live chain from `C:\Users\edebe\eds\workstream\100_backlog\codex\20260402_050000_breakout_twitter_summary_returns_every_4_hours.md`, which created the next backlog copy for `2026-04-02 09:00:00+01:00`.
- 2026-04-02 01:50 Europe/London: Restarted the controller so future recurring claims use the patched logic.

## Changes Made
- Updated `build_agent_execution_command()` so agents are instructed to follow any extra skill files explicitly referenced by the task.
- Updated `_recurrence_target_agent()` to prefer `Suggested Agent` before the current lane.
- Added recurring task normalization helpers so the Twitter summary recurrence chain always carries `Required Skill: C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`.
- Added `_ensure_recurring_next_instance()` and called it immediately after recurring task claim, so the next scheduled backlog copy exists before the current run completes.
- Repaired the live recurring backlog chain and seeded the missing `09:00` copy under `100_backlog`.

## Validation
- `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py`
  - Result: pass
- Direct import-and-call repair
  - Result: `_ensure_recurring_next_instance()` on `C:\Users\edebe\eds\workstream\100_backlog\codex\20260402_050000_breakout_twitter_summary_returns_every_4_hours.md` returned `next_scheduled_for=2026-04-02T09:00:00+01:00` and created `C:\Users\edebe\eds\workstream\100_backlog\general\20260402_090000_breakout_twitter_summary_returns_every_4_hours.md`
- Current recurring task metadata
  - Result: `C:\Users\edebe\eds\workstream\100_backlog\codex\20260402_050000_breakout_twitter_summary_returns_every_4_hours.md` contains `Required Skill: C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
  - Result: the same file contains `Next Scheduled For: 2026-04-02 09:00:00+01:00`
- Spawned next copy
  - Result: `C:\Users\edebe\eds\workstream\100_backlog\general\20260402_090000_breakout_twitter_summary_returns_every_4_hours.md` exists and contains `Required Skill: C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
- Controller restart
  - Result: `C:\Users\edebe\eds\workstream\logs\agent_controller_py.log` shows `AI Agent Controller Starting: 20260402_015038`

## Risks/Notes
- The fix must avoid creating duplicate next-slot files when a valid recurring backlog copy already exists.
- The recurring chain should continue to advance even if a run is blocked.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-02 01:51:30 Europe/London
