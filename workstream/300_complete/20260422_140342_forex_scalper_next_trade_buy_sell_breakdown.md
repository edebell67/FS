# Forex Scalper Next Trade Buy Sell Breakdown

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
Break down the next-trade-after-loss scalper analysis by BUY and SELL direction.

## Context
Input files:
- `TradeApps/breakout/fs/config.json`
- `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`

Criteria:
- Corrected scalper definition: `SL / TP >= scalper_ratio`.
- `scalper_ratio = 6`.
- Primary definition: next closed trade in the same strategy/product series after a losing trade.
- Alternate definition: next closed scalper trade globally by timestamp after a losing trade.

## Destination Folder
Destination Folder: None

## Dependency
Dependency: `workstream/300_complete/20260422_135713_forex_scalper_next_trade_after_loss.md`

## Plan
- [x] 1. Parse scalper closed trades with direction.
  - [x] Test: Infer BUY/SELL from `buy_net`/`sell_net` and `b_c`/`s_c` deltas.
  - Evidence: Parsed current file `last_update=2026-04-22T14:04:20.953459`; closed count 788, loss count 117.

- [x] 2. Compute same strategy/product next-trade breakdown by direction.
  - [x] Test: Report BUY/SELL counts, winners, losers, profit net, loss net, and net_return.
  - Evidence: Same-series next trades: BUY 34 / SELL 35 / MIXED 21; total net_return -1870.

- [x] 3. Compute global chronological next-trade breakdown by direction.
  - [x] Test: Report BUY/SELL counts, winners, losers, profit net, loss net, and net_return.
  - Evidence: Global next trades: BUY 60 / SELL 39 / MIXED 18; total net_return -8035.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: Python parser output from current `_summary_net.json`.
  - Objective-Proved: BUY/SELL breakdown is derived from current local JSON.
  - Status: captured

## Implementation Log
- 2026-04-22 14:03: Created in-progress task.
- 2026-04-22 14:04: Parsed corrected scalper closed trades with inferred direction.
- 2026-04-22 14:05: Computed same-series and global next-trade-after-loss breakdowns by BUY/SELL/MIXED.

## Changes Made
- None. Investigation only.

## Validation
- Input timestamp:
  - Result: `_summary_net.json last_update=2026-04-22T14:04:20.953459`.
- Same strategy/product next-trade breakdown:
  - Result: total 90, skipped 27, BUY net -1795, SELL net +245, MIXED net -320.
- Global chronological next-trade breakdown:
  - Result: total 117, skipped 0, BUY net -6005, SELL net -1170, MIXED net -860.

## Risks/Notes
- Input file is live and may change during the session.
- Direction inference uses per-entry deltas from `buy_net`, `sell_net`, `b_c`, and `s_c`.
- `MIXED` means the summary entry changed both buy and sell fields in the same closed-entry row; it is reported separately rather than forced into BUY or SELL.

## Completion Status
Status: Complete
Created: 2026-04-22 14:03
Completed: 2026-04-22 14:05
