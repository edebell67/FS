# Source
User request: run the scan in `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-23` on `breakout*op.json`.

# Task Type
standard

# Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false

# Task Summary
Run a read-only scan over `breakout*op.json` files in the specified live forex day folder and report open negative scalper matches.

# Context
- `TradeApps/breakout/fs/json/live/forex/2026-04-23/breakout*op.json`
- `TradeApps/breakout/fs/config.json`

# Destination Folder
None

# Dependency
None

# Plan
- [x] 1. Confirm scalper classification inputs and target file scope.
  - Test: Read config and enumerate matching files; expected pass condition is exact scope and scalper rule confirmed.
  - Evidence: `config.json` shows `scalper_ratio: 6`; `Get-ChildItem ... -Filter 'breakout*op.json'` found 50 matching files in the requested folder.
- [x] 2. Run the read-only scan over `breakout*op.json`.
  - Test: Execute scan and collect matching records; expected pass condition is a count and list of matches.
  - Evidence: Read-only Python scan completed over `breakout*op.json`; found 9 negative open scalper matches.
- [x] 3. Summarize results for the requested file scope only.
  - Test: Provide scan results constrained to the requested files; expected pass condition is clear match output.
  - Evidence: Results listed below are restricted to the exact requested filename pattern and folder.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: read-only scan output over `breakout*op.json`
  - Objective-Proved: Reports negative open scalper matches from the requested file scope.
  - Status: captured

# Implementation Log
- 2026-04-23 16:32 - Created task.
- 2026-04-23 16:33 - Confirmed `scalper_ratio: 6` and enumerated `breakout*op.json` files in the requested folder.
- 2026-04-23 16:34 - Ran the restricted read-only scan and collected matching open negative scalper records.

# Changes Made
None.

# Validation
- Read `TradeApps/breakout/fs/config.json`.
- Enumerated `TradeApps/breakout/fs/json/live/forex/2026-04-23/breakout*op.json`.
- Executed a read-only Python scan over the exact requested filename pattern.

# Risks/Notes
- This task is read-only and restricted to the exact filename pattern requested.

## Findings
Scope:
- Folder: `TradeApps/breakout/fs/json/live/forex/2026-04-23`
- Pattern: `breakout*op.json`
- Files scanned: `50`
- `scalper_ratio`: `6`

Result summary:
- Negative open scalper matches: `9`
- Matches with `is_live_trade == true`: `0`

Matches:
- `breakout_2_tp3.0_sl50.0_87f6187f_EURNZD_C_20260423_101807_2_0.00015_3.0_50.0_op.json`
  - `EURNZD_C / breakout_2_tp3.0_sl50.0 / SHORT / net_return -400.00`
- `breakout_2_tp5.0_sl50.0_0df85901_EURNZD_C_20260423_101807_2_0.00015_5.0_50.0_op.json`
  - `EURNZD_C / breakout_2_tp5.0_sl50.0 / SHORT / net_return -400.00`
- `breakout_2_tp3.0_sl50.0_e5134cb5_NZDAUD_C_20260423_105120_2_0.00015_3.0_50.0_op.json`
  - `NZDAUD_C / breakout_2_tp3.0_sl50.0 / SHORT / net_return -395.00`
- `breakout_2_tp5.0_sl50.0_cc4fc762_NZDAUD_C_20260423_105120_2_0.00015_5.0_50.0_op.json`
  - `NZDAUD_C / breakout_2_tp5.0_sl50.0 / SHORT / net_return -395.00`
- `breakout_2_tp3.0_sl50.0_6bdf0211_GBPEUR_S_20260423_060035_2_0.00015_3.0_50.0_op.json`
  - `GBPEUR_S / breakout_2_tp3.0_sl50.0 / SHORT / net_return -135.00`
- `breakout_R_2_tp3.0_sl50.0_f50bbc7e_GBPEUR_S_20260423_063413_2_0.00015_3.0_50.0_op.json`
  - `GBPEUR_S / breakout_R_2_tp3.0_sl50.0 / SHORT / net_return -115.00`
- `breakout_R_2_tp5.0_sl50.0_fe33aeeb_GBPEUR_S_20260423_061639_2_0.00015_5.0_50.0_op.json`
  - `GBPEUR_S / breakout_R_2_tp5.0_sl50.0 / SHORT / net_return -105.00`
- `breakout_2_tp5.0_sl30.0_3c92a5b7_CAD_20260423_140053_2_0.00015_5.0_30.0_op.json`
  - `CAD / breakout_2_tp5.0_sl30.0 / LONG / net_return -55.00`
- `breakout_2_tp5.0_sl50.0_2da379bb_CAD_20260423_140053_2_0.00015_5.0_50.0_op.json`
  - `CAD / breakout_2_tp5.0_sl50.0 / LONG / net_return -55.00`

# Completion Status
Complete - 2026-04-23 16:35.
