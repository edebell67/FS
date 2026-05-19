Source: User request in Codex session on 2026-04-24
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Identify `breakout*.json` files under `TradeApps/breakout/fs/json/live/forex/2026-04-24` that are not forex instruments.
Context: TradeApps breakout live JSON folder review limited to `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-24`.
Destination Folder: None
Dependency: None
Plan:
- [ ] 1. Create lifecycle record and move it to the active workstream lane.
  - [x] Test: Confirm the lifecycle file exists under `workstream/200_inprogress` and is readable.
  - Evidence: File successfully moved to `workstream/200_inprogress/20260424_121045_breakout_identify_non_forex_json_in_forex_live_folder.md` and read back with `Get-Content`.
- [ ] 2. Scan the target folder for `breakout*.json` files and classify filenames that indicate non-forex instruments.
  - [x] Test: Run a folder-restricted file scan and extract distinct non-forex symbols from matching filenames.
  - Evidence: Regex-based scan against `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-24` found `TOTAL=1418` non-forex files with symbols `CL, ES, ETH, GC, HG, NG, NQ, SI, SOL, XRP, YM`.
- [ ] 3. Report the identified non-forex files to the user with the scope restriction noted.
  - [x] Test: Final response contains only files from the requested folder and names the non-forex symbols found.
  - Evidence: Final response prepared with counts by non-forex symbol and example full paths from the restricted folder only.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: PowerShell folder-restricted scan output showing `TOTAL=1418` and grouped counts for `CL=124`, `ES=194`, `ETH=160`, `GC=121`, `HG=171`, `NG=121`, `NQ=24`, `SI=60`, `SOL=83`, `XRP=151`, `YM=209`.
  - Objective-Proved: Confirms the exact set of non-forex symbols present in `breakout*.json` files within the requested folder.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Example file paths captured from the restricted folder scan, including `...\\breakout_Rev_2_tp10.0_sl20.0_780db76f_CL_20260424_085633_2_0.00015_10.0_20.0_op.json` and `...\\breakout_Rev_2_tp20.0_sl20.0_522fb145_ES_20260424_085701_2_0.00015_20.0_20.0_op.json`.
  - Objective-Proved: Demonstrates that the identified non-forex files are real files inside the user-specified directory.
  - Status: captured

## Implementation Log
- 2026-04-24 12:10:45 Created lifecycle task file for a folder-restricted verification scan.
- 2026-04-24 12:11:00 Moved lifecycle file from `workstream/100_todo` to `workstream/200_inprogress`.
- 2026-04-24 12:12:36 Completed regex-based filename classification anchored on the hash/date boundary to avoid misreading the hash as the symbol.
- 2026-04-24 12:12:36 Confirmed only the following non-forex symbols occur in the restricted folder: `CL, ES, ETH, GC, HG, NG, NQ, SI, SOL, XRP, YM`.

## Changes Made
- Added lifecycle documentation file only.
- Updated lifecycle file with validation evidence and final scan results.

## Validation
- `Get-Content 'C:\Users\edebe\eds\workstream\200_inprogress\20260424_121045_breakout_identify_non_forex_json_in_forex_live_folder.md'`
  - Pass: lifecycle file exists in the active lane and is readable.
- Folder-restricted scan:
  - `Get-ChildItem -LiteralPath 'C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-24' -Filter 'breakout*.json' -File | ...`
  - Pass: extracted non-forex totals `TOTAL=1418` with grouped symbols `CL, ES, ETH, GC, HG, NG, NQ, SI, SOL, XRP, YM`.

## Risks/Notes
- Classification is based on the instrument token embedded in filenames unless file contents show a conflicting symbol field.
- Scope is restricted to the single directory requested by the user.
- Forex pair variants such as `EURAUD_C`, `GBPEUR_S`, and `NZDAUD_C` were explicitly normalized as forex and excluded from the non-forex result set.

## Completion Status
- Complete - 2026-04-24 12:12:36
