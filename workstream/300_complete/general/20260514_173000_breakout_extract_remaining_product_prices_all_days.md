# Task: Extract Remaining Product Prices Across All Available Days

## Status
- [x] **100_backlog**: Task created
- [x] **200_inprogress**: Work started
- [x] **300_complete**: Task finished

## Metadata
- **Source**: User request to create a new task for extracting prices for all other products across all available days.
- **Task Type**: standard
- **Task Attributes**:
  - recurring_task: false
  - looping_task: false
  - splittable_task: false
  - workflow_task: false
- **Destination Folder**: `C:\Users\edebe\eds\epics\ep_021_product_price_compile\remaining_products\`
- **Dependency**: Completed reference outputs for the four already-extracted products under `epics/ep_021_product_price_compile/`.

## Task Summary
Extract unique per-product entry and exit price records for every remaining product in the available breakout live JSON archive, excluding the four products already completed in EP 021, and compile outputs across all available days.

## Context
- Available source archive in this environment:
  - `C:\Users\edebe\eds\TradeApps\breakout\DB\json\live`
- Already completed products that must be excluded from this task:
  - `EURAUD_C`
  - `EURNZD_C`
  - `GBPAUD_C`
  - `GBPNZD_C`
- Required extraction shape:
  - `product`
  - `entry_time`
  - `entry_price`
  - `entry_price_side`
  - `exit_time`
  - `exit_price`
  - `exit_price_side`
- Price-side derivation rule:
  - `LONG` entry => `ask`
  - `SHORT` entry => `bid`
  - `LONG` exit => `bid`
  - `SHORT` exit => `ask`
- Scope:
  - all remaining products
  - all available days in the archive
  - unique records only

## Plan
- [x] 1. Enumerate the full product universe in the archive and separate already-completed products from remaining products.
  - [x] Test: Generate a product inventory from the JSON archive and confirm the remaining-product list excludes `EURAUD_C`, `EURNZD_C`, `GBPAUD_C`, and `GBPNZD_C`.
  - Evidence: Final remaining product set recorded in `summary.txt` and excludes the four already completed EP 021 products.
- [x] 2. Extract unique entry/exit records for all remaining products across all available days.
  - [x] Test: Produce compiled outputs under `C:\Users\edebe\eds\epics\ep_021_product_price_compile\remaining_products\` in machine-readable and tabular formats.
  - Evidence: JSON/CSV outputs and summary counts produced.
- [x] 3. Validate representative products and dates against raw source files.
  - [x] Test: Manually compare sample rows from multiple remaining products back to raw JSON timestamps, prices, and direction-derived bid/ask sides.
  - Evidence: AUD and GBPEUR_C raw-file checks recorded in Validation.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `workstream/100_backlog/general/20260514_173000_breakout_extract_remaining_product_prices_all_days.md`
  - Objective-Proved: The remaining-products extraction task has been captured with explicit exclusion scope and output destination.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `epics/ep_021_product_price_compile/remaining_products/remaining_product_entry_exit_prices.json`
  - Objective-Proved: Machine-readable compilation of remaining product entry/exit price records across all available days.
  - Status: produced

- Evidence-Type: file_output
  - Artifact: `epics/ep_021_product_price_compile/remaining_products/remaining_product_entry_exit_prices.csv`
  - Objective-Proved: Tabular export of remaining product entry/exit price records for downstream review and analysis.
  - Status: produced

- Evidence-Type: file_output
  - Artifact: `epics/ep_021_product_price_compile/remaining_products/summary.txt`
  - Objective-Proved: Final product counts, scan volume, and extraction filter rule.
  - Status: produced

## Implementation Log
- 2026-05-14 17:30: Created backlog task for extracting remaining product prices across all available days.
- 2026-05-14 19:05: Started extraction work against `C:\Users\edebe\eds\TradeApps\breakout\DB\json\live`.
- 2026-05-14 19:12: First broad pass surfaced non-trade/control JSON artifacts; refined extraction to require `entry_time` and `entry_price` so only trade-like records are captured.
- 2026-05-14 19:28: Completed refined extraction and wrote final JSON, CSV, and summary outputs to `C:\Users\edebe\eds\epics\ep_021_product_price_compile\remaining_products\`.

## Changes Made
- Extracted unique remaining-product entry/exit price records across all available days from the local live archive.
- Excluded previously completed EP 021 products: `EURAUD_C`, `EURNZD_C`, `GBPAUD_C`, `GBPNZD_C`.
- Applied direction-to-side mapping in compiled output:
  - `LONG` entry => `ask`
  - `SHORT` entry => `bid`
  - `LONG` exit => `bid`
  - `SHORT` exit => `ask`
- Applied trade filter requiring both `entry_time` and `entry_price` to suppress non-trade/control JSON noise.
- Wrote outputs to:
  - `C:\Users\edebe\eds\epics\ep_021_product_price_compile\remaining_products\remaining_product_entry_exit_prices.json`
  - `C:\Users\edebe\eds\epics\ep_021_product_price_compile\remaining_products\remaining_product_entry_exit_prices.csv`
  - `C:\Users\edebe\eds\epics\ep_021_product_price_compile\remaining_products\summary.txt`

## Validation
- Confirmed the four-product EP 021 extraction already exists and was excluded from this task.
- Verified output artifacts exist:
  - `remaining_product_entry_exit_prices.json`
  - `remaining_product_entry_exit_prices.csv`
  - `summary.txt`
- Verified final summary counts:
  - `scan_file_hits_total=129082`
  - `remaining_product_count=9`
  - `AUD: 2628`
  - `CAD: 2885`
  - `CHF: 2533`
  - `EUR: 3209`
  - `GBP: 3820`
  - `GBPEUR_C: 7491`
  - `GBPEUR_S: 31`
  - `NZD: 2021`
  - `NZDAUD_C: 5757`
- Raw-file spot checks matched compiled output:
  - `AUD` sample from `...2026-01-22\breakout_R_Rev_4_tp3.0_sl6.0_AUD_20260122_040339_4_0.00015_3.0_6.0_op.json` showed `direction=SHORT`, `entry_time=2026-01-22T04:03:39.104076`, `entry_price=0.680725`, `exit_time=2026-01-22T04:50:31.810203`, `exit_price=0.6804749999999999`, matching the compiled row with `entry_price_side=bid` and `exit_price_side=ask`.
  - `AUD` sample from `...2026-01-22\breakout_R_Rev_4_tp20.0_sl6.0_AUD_20260122_045031_4_0.00015_20.0_6.0_op.json` showed `direction=LONG`, `entry_time=2026-01-22T04:50:31.810203`, `entry_price=0.6804749999999999`, `exit_time=2026-01-22T07:14:42.751549`, `exit_price=0.680925`, matching the compiled row with `entry_price_side=ask` and `exit_price_side=bid`.
  - `GBPEUR_C` sample from `...2026-01-22\breakout_R_Rev_4_tp3.0_sl6.0_GBPEUR_C_20260122_040339_4_0.00015_3.0_6.0_op.json` showed `direction=SHORT`, `entry_time=2026-01-22T04:03:39.104076`, `entry_price=2.51265`, `exit_time=2026-01-22T04:13:34.202900`, `exit_price=2.5132499999999998`, matching the compiled row with `entry_price_side=bid` and `exit_price_side=ask`.

## Risks/Notes
- Source execution used the accessible local archive `C:\Users\edebe\eds\TradeApps\breakout\DB\json\live` because the earlier `X:\...` path was not mounted in this shell environment.
- Product names in the remaining archive are not all normalized FX pair symbols; the final remaining-product set is whatever trade-like product identifiers are present after exclusion and filtering.
- Some records remain `OPEN`, so `exit_time` and `exit_price` can legitimately be null in the compiled outputs when the source trade is still open.

## Completion Status
- **Status**: COMPLETE
- **Timestamp**: 2026-05-14 19:28


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-05-14 18:16:12
- Retry target: 100_backlog/general (previous lane: codex)
- Retry scheduled at 2026-05-14 18:17:12
- Retry target: 100_backlog/general (previous lane: codex)
