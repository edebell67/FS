# Task: Implement Delayed Leader Switching for Auto-Select

## Source
- User Directive: 2026-04-07

## Task Type
Task Type: standard

## Task Attributes
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary
Modify `weekly_performance.html` so Auto-Select does not immediately switch to a new weekly leader. A new leader must remain on top for `auto_select_delay_seconds` before the current auto-selected strategy is deactivated and the new one is activated.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Config: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- Auto-select state source: `activations` entries loaded from `/api/activations?mode=live`

## Destination Folder
Destination Folder: None

## Dependency
Dependency: None

## Plan
- [x] 1. Confirm `auto_select_delay_seconds` exists in `config.json` with a default of 60 seconds.
  - [x] Test: `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\config.json'`
  - Evidence: `config.json` already contains `"auto_select_delay_seconds": 60`, so no config file edit was required.
- [x] 2. Add dashboard state and UI feedback for delayed leader switching.
  - [x] Test: `Select-String -Path 'C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html' -Pattern 'autoSelectStatus|autoSelectDelaySeconds|pendingAutoLeader|leadershipChangeDetectedAt'`
  - Evidence: `weekly_performance.html` now includes the `autoSelectStatus` status element plus `autoSelectDelaySeconds`, `pendingAutoLeader`, and `leadershipChangeDetectedAt` state variables.
- [x] 3. Update `evaluateAutoSelect()` so a pending leader must persist for the configured delay and is cancelled if leadership reverses.
  - [x] Test: PowerShell here-string piped to `node -` that extracts the inline dashboard script from `weekly_performance.html`, stubs DOM/fetch dependencies, and asserts both delayed switch and cancellation behavior.
  - Evidence: Harness output returned `PASS auto_select_delay_switch` and `PASS auto_select_delay_cancel`.
- [x] 4. Validate the updated inline script syntax and record review evidence.
  - [x] Test: PowerShell here-string piped to `node -` that extracts the inline script from `weekly_performance.html` and compiles it with `new vm.Script(...)`.
  - Evidence: Harness output returned `PASS js_syntax`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: The dashboard now exposes a visible auto-select status message, tracks a pending leader, reads `auto_select_delay_seconds`, and applies delayed switching logic.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Node harness output: `PASS auto_select_delay_switch`, `PASS auto_select_delay_cancel`, `PASS js_syntax`
  - Objective-Proved: The updated inline script parses successfully, delays promotion until the timer expires, and clears the pending switch when the original leader regains the top spot.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Pending user verification request for `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: Final UI confirmation is still required for the live dashboard behavior.
  - Status: captured

## Implementation Log
- 2026-04-08 17:18: Read `skills\workstream-task-lifecycle\SKILL.md` and opened the assigned lifecycle task file before making changes.
- 2026-04-08 17:27: Confirmed `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json` already contained `auto_select_delay_seconds: 60`.
- 2026-04-08 17:35: Updated `weekly_performance.html` to add delayed auto-select state, a pending leader countdown message, and guarded leader switching logic.
- 2026-04-08 17:40: Ran Node-based validation harnesses to verify JavaScript syntax, delayed switching after 10 seconds, and cancellation when the original leader retakes rank #1 before expiry.
- 2026-04-08 17:42: Updated lifecycle evidence, validation notes, and completion state.

## Changes Made
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`:
  - Added `autoSelectStatus` UI messaging beside the Auto Select dropdown.
  - Added `autoSelectDelaySeconds`, `pendingAutoLeader`, and `leadershipChangeDetectedAt` dashboard state.
  - Added helper functions to normalize leaders, deduplicate current auto leaders, manage pending countdown state, and apply delayed leader switching.
  - Reworked `evaluateAutoSelect()` so the current auto leader stays active until the challenger remains #1 for the configured delay.
  - Added a one-second status refresh loop that updates the countdown and finalizes the switch when the delay expires.
- No edit was required in `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json` because the requested `auto_select_delay_seconds` key already existed with the correct default.

## Validation
- `Get-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\fs\config.json'`
  - Result: Confirmed `"auto_select_delay_seconds": 60`.
- `Select-String -Path 'C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html' -Pattern 'autoSelectStatus|autoSelectDelaySeconds|pendingAutoLeader|leadershipChangeDetectedAt'`
  - Result: Confirmed the status element and pending-leader state logic are present in the dashboard script.
- PowerShell here-string piped to `node -` to compile the extracted inline script with `new vm.Script(...)`
  - Result: `PASS js_syntax`
- PowerShell here-string piped to `node -` to execute the extracted inline script inside a stubbed VM context and simulate leader changes with a 10-second delay
  - Result: `PASS auto_select_delay_switch`
  - Result: `PASS auto_select_delay_cancel`
- User verification requested:
  - Please verify in the live dashboard that:
  - Pass/Fail 1: with `auto_select_delay_seconds` set to `10`, a new top strategy shows as pending and only switches after 10 seconds.
  - Pass/Fail 2: if the original auto leader retakes #1 within the 10-second window, the pending switch clears and no toggle occurs.

## Risks/Notes
- The countdown and switch finalization run locally once a challenger is detected, but leaderboard reversals still depend on the page fetching fresh data. If upstream rankings change without a dashboard refresh, the browser cannot see that reversal until the next fetch.
- Manual toggle behavior was left unchanged; this task only modifies the automatic leader-switch path.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-08 17:49:14

- 2026-04-08 17:55: Verified implementation and behavioral logic with Node.js harness. Syntax check passed.
