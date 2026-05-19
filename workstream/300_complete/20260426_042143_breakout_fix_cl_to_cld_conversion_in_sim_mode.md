Source: User request in Codex session on 2026-04-26
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Fix `_cl.json` files not converting to `_cld.json` in sim mode.
Context: `TradeApps/breakout/fs/summary_net_generator.py`, mode-specific processing paths, and any sim-mode file discovery or state logic affecting `_cl` to `_cld` rename behavior.
Destination Folder: TradeApps/breakout/fs/
Dependency: None

Plan:
- [x] 1. Reproduce and trace the sim-mode `_cl` to `_cld` processing path.
  - [x] Test: Review the sim-mode summary processing flow and identify where `_cl.json` files stop short of rename; pass when the failing branch or missing input is identified.
  - Evidence: Confirmed the real current-day sim blocker was sparse `_cl.json` payloads missing `product`, which caused `_trade_matches_target_product_type(...)` to reject them before rename.
- [x] 2. Implement a fix for sim-mode closed-trade digestion.
  - [x] Test: Review the code diff; pass when sim-mode `_cl.json` files can reach the same successful rename path as live mode.
  - Evidence: Added `_hydrate_trade_from_filename(fpath, trade_payload)` in `TradeApps/breakout/fs/summary_net_generator.py` and applied it before product-type matching for `_cld`, `_cl`, and `_op` file loads.
- [x] 3. Validate the fix and capture evidence.
  - [x] Test: Run targeted inspection or tests against the relevant FS components; pass when the sim-mode path is shown to convert `_cl.json` to `_cld.json`.
  - Evidence: `python -m py_compile "TradeApps\\breakout\\fs\\summary_net_generator.py"` passed; a direct probe showed `product_before=None`, `product_after='EUR'`, and `match_after=True`; a manual `process_date('sim', '2026-04-26', ...)` run logged `Updated: 375 new`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/summary_net_generator.py`
  - Objective-Proved: The summary generator now restores missing identity fields from the filename so current-day sim `_cl.json` files are not filtered out before rename.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile "TradeApps\\breakout\\fs\\summary_net_generator.py"`
  - Objective-Proved: The patched summary generator is syntactically valid.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: Manual one-off `process_date('sim', '2026-04-26', target)` run output: `[sim/forex/2026-04-26] Updated: 375 new, 977 op read (0 skipped)`
  - Objective-Proved: The current-day sim folder reached the closure digestion path after the fix.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: not_applicable
  - Objective-Proved: This is a technical file-processing fix validated by direct code and runtime evidence.
  - Status: not_applicable

## Implementation Log
- 2026-04-26 04:21:43+01:00 Created backlog lifecycle task for fixing sim-mode `_cl.json` to `_cld.json` conversion.
- 2026-04-26 04:22:30+01:00 Moved the task into `200_inprogress` and traced the summary generator rename path.
- 2026-04-26 04:23:15+01:00 Determined the earlier older-date hypothesis was not valid for this repo’s intended process and was discarded.
- 2026-04-26 04:47:30+01:00 Identified the actual blocker: many current-day sim `_cl.json` payloads were missing `product`, causing `_trade_matches_target_product_type(...)` to return `False`.
- 2026-04-26 04:49:10+01:00 Patched `summary_net_generator.py` to hydrate `product` and strategy identifiers from the filename before product-type matching.
- 2026-04-26 04:54:48+01:00 Ran a manual `process_date('sim', '2026-04-26', target)` pass and observed `Updated: 375 new`.

## Changes Made
- Updated `TradeApps/breakout/fs/summary_net_generator.py`.
- Added `import re`.
- Added `_hydrate_trade_from_filename(fpath, trade_payload)` to recover `product`, `source_strategy`, `script_name`, and `app_name` from the trade filename when the JSON payload is sparse.
- Applied filename hydration before product-type filtering for `_cld`, `_cl`, and `_op` files.

## Validation
- Inspected `TradeApps/breakout/fs/summary_net_generator.py` and confirmed the rename path remains in `process_date(...)`.
- Ran `python -m py_compile "TradeApps\\breakout\\fs\\summary_net_generator.py"`.
- Probed a current-day sim `_cl.json` sample and confirmed `product_before=None`, `product_after='EUR'`, `match_after=True`, and `process_after=True`.
- Checked 500 current-day sim `_cl.json` files and confirmed `match_ok=500`, `match_bad=0` after the patch.
- Measured current-day sim/forex folder counts before and after a manual `process_date(...)` pass:
  - Before: `cl=17670`, `cld=26048`
  - After: `cl=17635`, `cld=26145`

## Risks/Notes
- Sparse closed-trade payloads may still omit fields like `direction` or `entry_time`; this fix specifically restores enough identity data for current-day summary processing and `_cl -> _cld` conversion to proceed correctly.

## Completion Status
- Complete at 2026-04-26 04:54:48+01:00.
