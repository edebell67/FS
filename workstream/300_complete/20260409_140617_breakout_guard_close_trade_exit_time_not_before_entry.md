# Source
- User request on 2026-04-09 to implement a defensive check ensuring `exit_time` is never earlier than `entry_time` in breakout trade JSON output.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

# Task Summary
Add a defensive timestamp guard in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` so `close_trade()` forces `exit_time` to a current timestamp whenever the supplied close timestamp is missing or earlier than the trade's `entry_time`.

# Context
- Target file: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Target function: `close_trade()`
- Symptom: some trade JSON files were written with `exit_time < entry_time`, producing impossible trade lifecycles.

Destination Folder: None

Dependency: None

# Plan
- [x] 1. Add a close-time monotonicity guard in `close_trade()`.
  - [x] Test: Inspect the updated function and confirm it replaces invalid `exit_time` values with a current timestamp before trade finalization.
  - Evidence: `common.py` `close_trade()` now replaces missing or earlier-than-entry close timestamps with `pd.Timestamp.now()` and logs a `[TIME-GUARD]` warning.

- [x] 2. Run a lightweight verification pass on the updated file.
  - [x] Test: Run a syntax/compile check or targeted code inspection confirming the edit is valid.
  - Evidence: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` passed.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
  - Objective-Proved: Confirms the timestamp guard was implemented in the close path
  - Status: captured

- Evidence-Type: test_output
  - Artifact: verification command output
  - Objective-Proved: Confirms the edited file remains valid Python
  - Status: captured

# Implementation Log
- 2026-04-09 14:06:17 Created remediation task for invalid close timestamps.
- 2026-04-09 14:07:00 Added a monotonicity guard in `close_trade()` to replace invalid close timestamps with current time.
- 2026-04-09 14:07:30 Ran `py_compile` against `common.py`; syntax check passed.

# Changes Made
- Added this lifecycle task file.
- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py` so `close_trade()` cannot write `exit_time` earlier than `entry_time`.

# Validation
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Result: Passed with exit code `0`.

# Risks/Notes
- This change is a defensive guard only; it does not by itself explain or fix the upstream stale timestamp source.

# Completion Status
Complete - 2026-04-09 14:07:30
