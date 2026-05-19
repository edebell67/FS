Source: Follow-up from `C:\Users\edebe\eds\workstream\300_complete\20260430_203025_breakout_999_forex_live_auto_archive_filecount_breach_investigation.md` after confirming the auto-archive selector only targets `*_cld.json` while standard closed trades are written as `*_cl.json`.
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
  depends_on:
    - C:\Users\edebe\eds\workstream\300_complete\20260430_203025_breakout_999_forex_live_auto_archive_filecount_breach_investigation.md
  feeds_into: []
Task Summary: Update the forex/live auto-archive implementation so it archives the actual standard closed trade files (`*_cl.json`) rather than only `*_cld.json`, and harden runtime supervision so the threshold watcher remains active reliably.
Context: Likely affected areas include `TradeApps\breakout\fs\common.py`, `TradeApps\breakout\fs\archive_cld.py`, `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py`, archive selection rules, and validation in the live forex JSON path.
Destination Folder: None
Dependency: C:\Users\edebe\eds\workstream\300_complete\20260430_203025_breakout_999_forex_live_auto_archive_filecount_breach_investigation.md

## Plan
- [x] 1. Update archive selection logic so threshold auto-archive targets the correct standard closed trade files while excluding open/support files.
  - [x] Test: Targeted code review confirms the archive selector includes `*_cl.json` and preserves safe exclusions for `*_op.json` and underscore files.
  - Evidence: Added `_is_auto_archivable_closed_trade_file(...)` in `TradeApps\breakout\fs\common.py`; `_perform_cld_auto_archive(...)` now archives both standard `*_cl.json` and legacy `*_cld.json` while excluding underscore files and open trades.
- [x] 2. Harden watcher supervision so the dedicated auto-archive watcher is started and restarted by the watchdog process.
  - [x] Test: Repository review confirms `archive_cld.py` is included in the supervised script set or equivalent always-on runtime coverage is made explicit.
  - Evidence: Added `archive_cld.py` to the `file_names` watcher list in `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py`.
- [x] 3. Validate the updated behavior with a safe reproduction or controlled run and document exact outcomes.
  - [x] Test: Controlled validation proves the threshold logic moves eligible closed files into the dated archive folder when count exceeds the configured threshold.
  - Evidence: `python -m pytest TradeApps\breakout\fs\tests\test_auto_archive_closed_files.py -q` passed and verified archive movement for both `*_cl.json` and `*_cld.json`; `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` also passed as a regression check.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `TradeApps\breakout\fs\common.py`, `TradeApps\breakout\fs\archive_cld.py`, `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py`, `TradeApps\breakout\fs\tests\test_auto_archive_closed_files.py`
  - Objective-Proved: Confirms archive selection was expanded to include standard closed files, watcher supervision was hardened, and regression coverage was added.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest TradeApps\breakout\fs\tests\test_auto_archive_closed_files.py -q` => `1 passed in 8.60s`; `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` => `7 passed in 1.98s`
  - Objective-Proved: Confirms the updated auto-archive logic moves both closed-file variants safely and does not break the existing weekly auto-promote common tests.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\workstream\300_complete\20260430_215504_breakout_998_fix_forex_live_auto_archive_closed_file_selector.md
  - Objective-Proved: Captures the follow-up fix task required by the completed investigation.
  - Status: captured

## Implementation Log
- 2026-04-30 21:55:03 BST: Created this `_998_` follow-up task after the `_999_` investigation confirmed the selector mismatch between archived `*_cld.json` and actual closed trade files `*_cl.json`.
- 2026-05-01 00:05:00 BST: Moved the task into `workstream/200_inprogress` and reviewed the existing closed-file suffix logic, archive watcher, and watchdog supervision.
- 2026-05-01 00:10:00 BST: Updated `TradeApps\breakout\fs\common.py` so threshold auto-archive selects both standard `*_cl.json` and legacy `*_cld.json` closed trades while excluding underscore/support files and open trades.
- 2026-05-01 00:11:00 BST: Updated `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py` to supervise `archive_cld.py`.
- 2026-05-01 00:13:00 BST: Added `TradeApps\breakout\fs\tests\test_auto_archive_closed_files.py` to validate archive behavior against a temporary day folder.
- 2026-05-01 00:16:47 BST: Ran targeted pytest validation for the new archive test and the existing weekly auto-promote common suite; both passed.

## Changes Made
- Expanded the threshold auto-archive selector in `TradeApps\breakout\fs\common.py` to include both:
  - standard closed trade files `*_cl.json`
  - legacy closed trade files `*_cld.json`
- Preserved exclusions for:
  - open trades `*_op.json`
  - underscore/support files such as `_summary_net.json`
- Added `archive_cld.py` to the supervised script list in `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py`.
- Added a targeted regression test in `TradeApps\breakout\fs\tests\test_auto_archive_closed_files.py`.

## Validation
- Verified `TradeApps\breakout\fs\common.py` now uses `_is_auto_archivable_closed_trade_file(...)` and archives both `*_cl.json` and `*_cld.json`.
- Verified `TradeApps\breakout\fs\verify_algo_execution_and_restart_02.py` now includes `archive_cld.py` in the watchdog process set.
- Verified `python -m pytest TradeApps\breakout\fs\tests\test_auto_archive_closed_files.py -q` passed.
- Verified `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_common.py -q` passed.

## Risks/Notes
- This change improves future archive behavior but does not retroactively clean the already-bloated 2026-04-30 forex folder.
- The implementation preserves legacy `*_cld.json` handling rather than deprecating it, to avoid breaking any existing downstream process that still emits or expects that form.
- A separate operational cleanup/backfill may still be needed if you want the current oversized forex day folder normalized immediately.

## Completion Status
- State: Complete
- Timestamp: 2026-05-01 00:16:47 BST
