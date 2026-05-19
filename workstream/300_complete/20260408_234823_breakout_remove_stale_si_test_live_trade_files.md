# Source
- User request on 2026-04-08 to remove the two stale `SI` test live-trade files that were blocking new live trade promotion.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

# Task Summary
Remove the two stale `SI` test `*_op.json` files under the live metals day folder so they no longer count against the live-trade cap.

# Context
- Target file 1: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\2026-04-08\breakout_test_test-guid_SI_20260408_120554_2_0.00015_30.0_5.0_op.json`
- Target file 2: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\2026-04-08\breakout_test_test-guid_SI_20260408_120632_2_0.00015_30.0_5.0_op.json`
- Related investigation: `C:\Users\edebe\eds\workstream\300_complete\20260408_232459_breakout_investigate_no_new_live_trades_despite_active_price_feed.md`

Destination Folder: None

Dependency: None

# Plan
- [x] 1. Confirm both stale blocker files exist at the expected paths.
  - [x] Test: Run `Test-Path` for both absolute file paths and confirm both return `True`.
  - Evidence: Pre-removal `Test-Path` returned `True` for both target files.

- [x] 2. Remove the two files and validate they are gone.
  - [x] Test: Use `Remove-Item` on both exact paths, then run `Test-Path` again and confirm both return `False`.
  - Evidence: Final `Test-Path` returned `False` for both target files after forced per-file removal.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: `Test-Path` results before and after removal
  - Objective-Proved: Confirms the requested files were present and then removed
  - Status: captured

- Evidence-Type: file_output
  - Artifact: deleted target file paths listed in this lifecycle file
  - Objective-Proved: Identifies the exact stale blockers that were removed
  - Status: captured

# Implementation Log
- 2026-04-08 23:48:23 Created remediation task from user request.
- 2026-04-08 23:48:44 Confirmed both target files existed.
- 2026-04-08 23:49:10 Initial removal command returned without clearing the files.
- 2026-04-08 23:49:23 Retried with explicit per-file `Remove-Item -Force`; final existence check showed both files removed.

# Changes Made
- Added this lifecycle task file.
- Removed the two stale `SI` test live-trade JSON files from the metals live day folder.

# Validation
- Pre-removal checks:
  - `Test-Path <file1>` => `True`
  - `Test-Path <file2>` => `True`
- Post-removal checks:
  - `Test-Path <file1>` => `False`
  - `Test-Path <file2>` => `False`

# Risks/Notes
- This action removes only the two identified stale test blockers.
- After removal, the monitor may need one more cycle to recalculate live count.

# Completion Status
Complete - 2026-04-08 23:49:23
