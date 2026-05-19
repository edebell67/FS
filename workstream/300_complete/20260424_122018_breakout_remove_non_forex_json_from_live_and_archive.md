Source: User request in Codex session on 2026-04-24
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Remove non-forex `breakout*.json` files from the forex live folder and its archive subtree using filename matching against `TradeApps/breakout/fs/config.json` `trade_products`.
Context: Scope limited to `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-24` and `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-24\archive`.
Destination Folder: None
Dependency: Filename rule confirmed in `workstream/300_complete/20260424_121604_breakout_validate_non_forex_by_trade_products_field.md`.
Plan:
- [ ] 1. Create lifecycle record and move it to the active workstream lane.
  - [x] Test: Confirm the lifecycle file exists under `workstream/200_inprogress` and is readable.
  - Evidence: File successfully moved to `workstream/200_inprogress/20260424_122018_breakout_remove_non_forex_json_from_live_and_archive.md`.
- [ ] 2. Compute the exact delete set for the live folder and archive subtree using the approved filename rule.
  - [x] Test: Produce counts for matching files in both target scopes before deletion.
  - Evidence: Pre-delete counts were `LIVE=1412` for the live folder excluding archive and `ARCHIVE=5956` for the archive subtree.
- [ ] 3. Remove only the matching files from the two target scopes.
  - [x] Test: Execute scoped deletion and confirm the targeted files no longer exist.
  - Evidence: Deletion command reported `REMOVED_LIVE=1412` and `REMOVED_ARCHIVE=5956`. Clean verification then reported `REMAINING_LIVE=0` and `REMAINING_ARCHIVE=0`.
- [ ] 4. Report the deletion result to the user.
  - [x] Test: Final response states the counts removed from the live folder and archive subtree.
  - Evidence: Final response prepared with verified removal counts and scope note.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: PowerShell pre-delete count, deletion output, and post-delete verification for the two scoped target paths.
  - Objective-Proved: Confirms that only the non-forex filename matches were removed and none remain in the live folder or archive subtree.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Sample deleted path `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-24\breakout_Rev_2_tp10.0_sl20.0_780db76f_CL_20260424_085633_2_0.00015_10.0_20.0_op.json` returned `Test-Path=False`.
  - Objective-Proved: Confirms actual file removal in the requested scope.
  - Status: captured

## Implementation Log
- 2026-04-24 12:20:18 Created lifecycle task file for scoped non-forex file removal.
- 2026-04-24 12:20:35 Moved lifecycle file into `workstream/200_inprogress`.
- 2026-04-24 12:21:10 Counted non-forex filename matches using `TradeApps/breakout/fs/config.json` `trade_products`: `1412` in the live folder excluding archive and `5956` in the archive subtree.
- 2026-04-24 12:26:50 Executed scoped deletion for the two target paths only.
- 2026-04-24 12:27:23 Verified a deleted sample file no longer exists.
- 2026-04-24 12:28:10 Re-ran clean verification and confirmed zero non-forex matches remain in both target scopes.

## Changes Made
- Added lifecycle documentation file only.
- Removed non-forex `breakout*.json` files from the requested live folder and archive subtree.
- Updated lifecycle file with pre-delete counts, deletion evidence, and clean verification.

## Validation
- Scope existence check:
  - Verified both target paths existed before deletion.
- Pre-delete count:
  - `LIVE=1412`
  - `ARCHIVE=5956`
- Deletion command:
  - `REMOVED_LIVE=1412`
  - `REMOVED_ARCHIVE=5956`
- Sample removal check:
  - `Test-Path=False` for deleted `...780db76f_CL_20260424_085633...json`
- Post-delete clean verification:
  - `REMAINING_LIVE=0`
  - `REMAINING_ARCHIVE=0`

## Risks/Notes
- Deletion is intentionally limited to files under the two user-specified paths.
- Forex classification uses filename containment against `TradeApps/breakout/fs/config.json` `trade_products`.
- The live-folder verification explicitly excluded the `archive` subtree to avoid double-counting.

## Completion Status
- Complete - 2026-04-24 12:28:10
