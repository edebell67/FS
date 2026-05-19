Source: User report on 2026-04-02 that the recurring Twitter summary task spawned the `2026-04-02 17:00` slot twice.

Task Type: bugfix
Project: workstream

## Objective
- Stop recurring tasks from spawning the same next slot twice.
- Clean the existing `2026-04-02 17:00` duplicate backlog copies so only one canonical task remains live.

## Plan
- [x] 1. Inspect the recurring completion path in `workstream/run_agent.py` and confirm duplicate creation happens from both claim-time ensure and finish-time spawn.
  - [x] Test: Confirm log evidence shows both `ensured recurring backlog instance` and `spawned recurring instance` for the same `20260402_170000` slot.
  - Evidence: `agent_worker.log` contains both ensure-time and finish-time creation entries for `20260402_170000_breakout_twitter_summary_returns_every_4_hours.md` and the stray `general_` chain.
- [x] 2. Patch the scheduler so recurring next-slot creation only happens in one place.
  - [x] Test: Confirm the completion path no longer calls `_spawn_next_recurring_instance()`.
  - Evidence: `workstream/run_agent.py` completion path now only records `Next Scheduled For` on the finished file and no longer spawns a second next-slot copy.
- [x] 3. Repair the current live backlog state for `2026-04-02 17:00`.
  - [x] Test: Confirm only one canonical `20260402_170000_breakout_twitter_summary_returns_every_4_hours.md` remains under `100_backlog`, and the stray `general_` duplicate is removed from live lanes.
  - Evidence: only `C:\Users\edebe\eds\workstream\100_backlog\codex\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md` remains live; the two duplicate general-lane files were moved to `500_dump\dedupe_recurring_20260402_170000`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Proves recurring duplicate creation was removed in code.
  - Status: complete
- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\workstream\logs\agent_worker.log`
  - Objective-Proved: Proves the duplicate source was both ensure-time and finish-time creation for the same slot.
  - Status: complete
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\100_backlog\codex\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md`; `C:\Users\edebe\eds\workstream\500_dump\dedupe_recurring_20260402_170000`
  - Objective-Proved: Proves only one live `17:00` backlog copy remains after cleanup.
  - Status: complete

## Implementation Log
- 2026-04-02 14:53:46 Europe/London: Task created to fix duplicate recurring Twitter slot spawning.
- 2026-04-02 14:54 Europe/London: Confirmed from `agent_worker.log` that the same `20260402_170000` slot was being created twice, once via `ensured recurring backlog instance` and again via `spawned recurring instance`.
- 2026-04-02 14:54 Europe/London: Patched `workstream/run_agent.py` to stop finish-time recurring spawning and leave next-slot creation solely in the claim-time ensure path.
- 2026-04-02 14:55 Europe/London: Moved the duplicate live `17:00` files out of backlog into `C:\Users\edebe\eds\workstream\500_dump\dedupe_recurring_20260402_170000`, leaving one canonical live copy.
- 2026-04-02 14:55 Europe/London: Restarted the controller; `agent.lock` now points to a live Python process started at `14:55:04`.

## Changes Made
- Removed the finish-time `_spawn_next_recurring_instance()` call from the recurring completion path in `workstream/run_agent.py`.
- Kept the claim-time `_ensure_recurring_next_instance()` logic as the single source of next-slot creation.
- Archived the duplicate live `17:00` backlog files:
  - `C:\Users\edebe\eds\workstream\100_backlog\general\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md`
  - `C:\Users\edebe\eds\workstream\100_backlog\general\20260402_170000_general_breakout_twitter_summary_returns_every_4_hours.md`
- Preserved the one canonical live backlog copy:
  - `C:\Users\edebe\eds\workstream\100_backlog\codex\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md`

## Validation
- Duplicate-source log evidence
  - `agent_worker.log` contains both:
  - `ensured recurring backlog instance 20260402_170000_breakout_twitter_summary_returns_every_4_hours.md`
  - `spawned recurring instance 20260402_170000_breakout_twitter_summary_returns_every_4_hours.md`
- Syntax validation
  - `python -m py_compile C:\Users\edebe\eds\workstream\run_agent.py`
  - Result: pass
- Live backlog cleanup
  - `Get-ChildItem` under `C:\Users\edebe\eds\workstream\100_backlog` for `20260402_170000*breakout_twitter_summary_returns_every_4_hours.md`
  - Result: only `C:\Users\edebe\eds\workstream\100_backlog\codex\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md`
- Controller restart
  - `C:\Users\edebe\eds\workstream\agent.lock` -> `30448`
  - `Get-Process -Id 30448` shows a live Python process with start time `2026-04-02 14:55:04`

## Risks/Notes
- Cleanup must preserve one runnable `17:00` backlog copy and should not delete the only valid future slot.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-02 14:56:20 Europe/London
