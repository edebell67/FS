Source: User request in Codex session on 2026-04-24
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Remove non-forex product/strategy entries from `TradeApps/breakout/fs/json/live/forex/2026-04-24/_summary_net.json` using the breakout forex filename/product allowlist from `TradeApps/breakout/fs/config.json`.
Context: Single-file content edit scoped to `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-24\_summary_net.json`.
Destination Folder: None
Dependency: Forex allowlist established from `TradeApps/breakout/fs/config.json`.
Plan:
- [ ] 1. Create lifecycle record and move it to the active workstream lane.
  - [x] Test: Confirm the lifecycle file exists under `workstream/200_inprogress` and is readable.
  - Evidence: File successfully moved to `workstream/200_inprogress/20260424_123151_breakout_remove_non_forex_entries_from_summary_net.md`.
- [ ] 2. Inspect `_summary_net.json` structure and identify how product/strategy records are stored.
  - [x] Test: Read a small sample and capture top-level shape plus record keys.
  - Evidence: `_summary_net.json` is a top-level object with `last_update`, `session_max_net`, and `strategies`; each strategy contains product keys mapped to arrays of metric snapshots.
- [ ] 3. Remove only non-forex entries from `_summary_net.json`.
  - [x] Test: Rewrite the file and verify non-forex products/strategies no longer appear.
  - Evidence: Pre-edit scan found `660` non-forex product buckets across `11` products: `CL, ES, ETH, GC, HG, NG, NQ, SI, SOL, XRP, YM`, each appearing under `60` strategies. Post-edit verification reported `REMAINING_NON_FOREX_BUCKETS=0`.
- [ ] 4. Report the file-content cleanup result to the user.
  - [x] Test: Final response states what was removed and what validation passed.
  - Evidence: Final response prepared with removed bucket counts and clean verification results.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: PowerShell pre/post inspection of `_summary_net.json`, including pre-edit non-forex bucket counts and post-edit zero remaining non-forex buckets.
  - Objective-Proved: Confirms that non-forex product buckets were removed from the summary file content.
  - Status: captured
- Evidence-Type: diff
  - Artifact: In-place JSON rewrite of `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-24\_summary_net.json` preserving only forex allowlist product buckets under `strategies`.
  - Objective-Proved: Confirms the file content changed exactly in the intended direction.
  - Status: captured

## Implementation Log
- 2026-04-24 12:31:51 Created lifecycle task file for `_summary_net.json` cleanup.
- 2026-04-24 12:32:05 Moved lifecycle file into `workstream/200_inprogress`.
- 2026-04-24 12:32:20 Inspected `_summary_net.json` and confirmed top-level structure is `{ last_update, session_max_net, strategies }`.
- 2026-04-24 12:32:35 Counted product buckets in `strategies`; identified `660` non-forex buckets across `CL, ES, ETH, GC, HG, NG, NQ, SI, SOL, XRP, YM`.
- 2026-04-24 12:32:50 Rewrote `_summary_net.json` to keep only forex allowlist product keys from `TradeApps/breakout/fs/config.json`.
- 2026-04-24 12:33:19 Verified zero remaining non-forex buckets and `240` remaining strategies.

## Changes Made
- Added lifecycle documentation file only.
- Edited `TradeApps/breakout/fs/json/live/forex/2026-04-24/_summary_net.json` in place.
- Removed non-forex product buckets from every strategy and preserved forex buckets only.

## Validation
- Structure inspection:
  - Top-level keys: `last_update`, `session_max_net`, `strategies`
- Pre-edit bucket counts:
  - Forex buckets present: `AUD, CAD, CHF, EUR, EURAUD_C, EURNZD_C, GBP, GBPAUD_C, GBPEUR_C, GBPEUR_S, GBPNZD_C, NZDAUD_C`
  - Non-forex buckets present: `CL=60`, `ES=60`, `ETH=60`, `GC=60`, `HG=60`, `NG=60`, `NQ=60`, `SI=60`, `SOL=60`, `XRP=60`, `YM=60`
  - Total non-forex buckets: `660`
- Post-edit verification:
  - `REMAINING_NON_FOREX_BUCKETS=0`
  - `STRATEGY_COUNT=240`

## Risks/Notes
- The file is large, so the structure must be sampled before rewriting to avoid damaging the JSON shape.
- Removal must be content-based inside the summary file rather than filesystem deletion.
- The cleanup removed non-forex product buckets, not partial datapoints inside forex product buckets.

## Completion Status
- Complete - 2026-04-24 12:33:19
