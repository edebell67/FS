# Forex Scalper Closed Files Buy Sell Breakdown

Source: User request, 2026-04-22
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Recompute scalper BUY/SELL breakdown from matching `*_cl*.json` closed-trade files in `TradeApps/breakout/fs/json/live/forex/2026-04-22` and its `archive` subfolders.

## Context
Input folders:
- `TradeApps/breakout/fs/json/live/forex/2026-04-22`
- `TradeApps/breakout/fs/json/live/forex/2026-04-22/archive`

Criteria:
- Corrected scalper definition: `SL / TP >= scalper_ratio`.
- `scalper_ratio = 6` from `config.json`.
- Match strategy from closed trade filenames and/or JSON payload.

## Destination Folder
Destination Folder: None

## Dependency
Dependency: `workstream/300_complete/20260422_134814_forex_scalper_ratio_gte_counts.md`

## Plan
- [x] 1. Inspect closed-trade file naming and JSON schema.
  - [x] Test: Read sample `*_cl*.json` files from root and archive.
  - Evidence: Root compact `_cl.json` can omit `direction`; richer `_cld.json` includes `guid`, `product`, `direction`, `entry_time`, and `exit_time`.

- [x] 2. Deduplicate matching scalper closed-trade files.
  - [x] Test: Count root/archive files, matching scalper files, and unique trade records.
  - Evidence: `total_cl_files=7560`, `matching_scalper_files_before_dedupe=1317`, `root=604`, `archive=713`, `unique_scalper_closed_trades=839`.

- [x] 3. Compute BUY/SELL/MIXED profit/loss/net breakdown from unique closed files.
  - [x] Test: Report closed count, profit/loss counts, profit/loss net, and net total by direction.
  - Evidence: BUY closed 463 net -7250; SELL closed 376 net +1425; total closed 839 net -5825.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: Python parser output over `TradeApps/breakout/fs/json/live/forex/2026-04-22/**/*_cl*.json`.
  - Objective-Proved: Closed-file BUY/SELL breakdown is derived from source trade JSON files.
  - Status: captured

## Implementation Log
- 2026-04-22 14:20: Created in-progress task.
- 2026-04-22 14:22: Inspected root `_cl.json` and archive `_cld.json` sample schemas.
- 2026-04-22 14:25: Parsed root and archive closed files matching `SL / TP >= 6`.
- 2026-04-22 14:27: Deduplicated by `(strategy, guid, product)` and preferred records with explicit `direction`.
- 2026-04-22 14:29: Computed BUY/SELL profit/loss/net breakdown.

## Changes Made
- None. Investigation only.

## Validation
- File counts:
  - Result: 7560 total `*_cl*.json` files scanned.
  - Result: 1317 scalper-matching files before dedupe: 604 root, 713 archive.
  - Result: 839 unique scalper closed trades after dedupe by `(strategy, guid, product)`.
- BUY breakdown:
  - Result: 463 closed, 419 profit, 44 loss, profit net +7320, loss net -14570, net -7250.
- SELL breakdown:
  - Result: 376 closed, 359 profit, 17 loss, profit net +5760, loss net -4335, net +1425.
- Totals:
  - Result: 839 closed, 778 profit, 61 loss, profit net +13080, loss net -18905, net -5825.

## Risks/Notes
- Archive folders may contain repeated snapshots of the same trade file. Deduplication is required.
- Deduplication used `(strategy, guid, product)`.
- When both compact `_cl.json` and richer `_cld.json` existed for the same trade, the record with explicit `direction` was preferred.
- Compact `_cl.json` may only contain `market_bias_at_open`; this was used only when explicit `direction` was unavailable.

## Completion Status
Status: Complete
Created: 2026-04-22 14:20
Completed: 2026-04-22 14:29
