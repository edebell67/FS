Source: User request in Codex thread on 2026-04-13 to explain `TradeApps/breakout/fs/verify_algo_execution_and_restart_02.py`.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on: []
  feeds_into: []
Task Summary: Inspect the breakout supervisor script, explain its control flow and operational behavior, and cite the relevant file sections.
Context: `C:\Users\edebe\eds\TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py`, `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`, selected managed child scripts.
Destination Folder: None
Dependency: None
Plan:
- [x] 1. Inspect the supervisor script and related runtime inputs.
  - [x] Test: Read the target script and config entries and confirm the managed script list is visible.
  - [x] Evidence: `Get-Content` output captured for `verify_algo_execution_and_restart_02.py`; `Select-String` confirmed `kill_switch` in `config.json`.
- [ ] 2. Summarize the script's behavior, restart logic, and operational caveats for the user.
  - [x] Test: Final response references the main loop, config controls, process table behavior, and shutdown path with file/line citations.
  - [x] Evidence: Explanation prepared from cited sections of `verify_algo_execution_and_restart_02.py` for delivery in the Codex thread.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: PowerShell `Get-Content` and `Select-String` output captured in Codex tool history for the target script and `config.json`
  - Objective-Proved: The explanation is grounded in the current checked-in script and current config keys rather than filename inference.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Codex final response in this thread explaining `verify_algo_execution_and_restart_02.py` with cited line references
  - Objective-Proved: The user receives the requested walkthrough with concrete references.
  - Status: captured

## Implementation Log
- 2026-04-13 11:38:56: Created lifecycle file for documentation/explanation task.
- 2026-04-13 11:39:00: Inspected `verify_algo_execution_and_restart_02.py`, `config.json`, `breakout.py`, and `trade_viewer_api.py`.
- 2026-04-13 11:39:30: Prepared user-facing explanation covering config control, watchdog loop, restart behavior, and shutdown semantics.

## Changes Made
- No repository code changes.
- Added this lifecycle file to track the explanation task.

## Validation
- `Get-Content -Path 'C:\Users\edebe\eds\TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py'`
  - Result: Pass. Script content and control flow captured.
- `Select-String -Path 'C:\Users\edebe\eds\TradeApps\breakout\fs\config.json' -Pattern 'sleep_duration|kill_switch' -Context 1,1`
  - Result: Partial. `kill_switch` confirmed; `sleep_duration` not shown in the matched excerpt.
- `Get-Content -Path 'C:\Users\edebe\eds\TradeApps\breakout\fs\breakout.py' -TotalCount 80`
  - Result: Pass. Confirmed this monitor launches trading logic implemented elsewhere.

## Risks/Notes
- This task is explanatory only; no behavioral verification of live subprocess launching was performed.
- The script imports `datetime` but the scheduled-task block using it is currently commented out.

## Completion Status
- Complete as of 2026-04-13 11:39:30.
