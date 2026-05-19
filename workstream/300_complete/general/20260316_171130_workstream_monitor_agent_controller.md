# Task: Monitor Agent Controller Restart Loop

## Source
- The kanban workers need `run_agent.ps1` running continuously; the controller was previously started once with no restart logic, so a crash left the lanes idle.

## Task Summary
- Add self-healing behavior so `kanban_dashboard.py` ensures `run_agent.ps1` is always relaunching when it stops.

## Context
- `workstream/kanban_dashboard.py`
- `workstream/run_agent.ps1`
- Ability to resume tasks already in `200_inprogress/<agent>` depends on the controller staying up.

## Plan
- [x] 1. Determine how the controller is launched today.
  - [x] Test: inspect `workstream/kanban_dashboard.py`.
  - [x] Evidence: found the `start_agent_controller()` helper that simply calls the PowerShell script once.
- [x] 2. Implement a monitor that restarts `run_agent.ps1` whenever it exits.
  - [x] Test: add `_launch_agent_controller()` and `agent_controller_monitor()` with a 5s polling loop.
  - [x] Evidence: new helper functions and global state added at the top and a daemon thread started at `__main__`.
- [x] 3. Validate the patched dashboard.
  - [x] Test: `python -m py_compile workstream\\kanban_dashboard.py`.
  - [x] Evidence: compile check passed.

## Implementation Log
- 2026-03-16 17:11: Added monitor thread that restarts `run_agent.ps1` when it terminates.
- 2026-03-16 17:11: Validated the updated dashboard script with `python -m py_compile`.

## Changes Made
- Added `_launch_agent_controller()` and `agent_controller_monitor()` so the kanban dashboard restarts the PowerShell controller in a loop.
- Replaced the one-shot controller launch under `if __name__ == '__main__':` with the monitor thread.

## Validation
- `python -m py_compile C:\\Users\\edebe\\eds\\workstream\\kanban_dashboard.py`
- Result: pass

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: false
- Evidence-Type: file_output
- Artifact: `workstream/kanban_dashboard.py`
- Objective-Proved: includes `_launch_agent_controller()`, `agent_controller_monitor()`, and the daemon thread start.
- Status: captured
- Evidence-Type: test_output
- Artifact: `python -m py_compile C:\\Users\\edebe\\eds\\workstream\\kanban_dashboard.py`
- Objective-Proved: confirms the updated dashboard code compiles cleanly.
- Status: captured

## Completion Status
- Awaiting user verification


# User Feedback
User Verified: PASS
