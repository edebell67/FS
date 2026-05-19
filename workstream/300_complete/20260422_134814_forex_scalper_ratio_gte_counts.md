# Forex Scalper Ratio GTE Counts

Source: User correction, 2026-04-22
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Rerun forex scalper counts for `2026-04-22/_summary_net.json` using corrected scalper definition: `SL / TP >= scalper_ratio`, not exact equality.

## Context
Input files:
- `TradeApps/breakout/fs/config.json`
- `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`

Corrected scalper definition:
- `scalper_ratio` from `config.json` is `6`.
- Strategy is scalper when `SL / TP >= 6`.
- This includes `tp5/sl30` and `tp5/sl50`.

## Destination Folder
Destination Folder: None

## Dependency
Dependency: `workstream/300_complete/20260422_132823_forex_scalper_summary_net_trade_counts.md`

## Plan
- [x] 1. Identify all strategies where `SL / TP >= scalper_ratio`.
  - [x] Test: Confirm `tp5/sl30` and `tp5/sl50` strategy families are included.
  - Evidence: `scalper_strategy_keys=30`; strategy list includes `breakout_2_tp5.0_sl50.0` and `breakout_R_2_tp5.0_sl50.0`.

- [x] 2. Recompute closed/open/profit/loss/net totals.
  - [x] Test: Count non-open closed entries, open markers, profit/loss deltas, and net totals.
  - Evidence: `closed=774`, `open_count=109`, `profit_count=660`, `profit_net=13215.0`, `loss_count=114`, `loss_net=-15600.0`, `net_total=-2385.0`.

- [x] 3. Recompute consecutive losing streaks.
  - [x] Test: Report global and per strategy/product max loss streaks.
  - Evidence: Global max consecutive losses = 12; per strategy/product max consecutive losses = 3.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: Python parser output from `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`.
  - Objective-Proved: Corrected scalper definition results are computed from current local JSON.
  - Status: captured

## Implementation Log
- 2026-04-22 13:48: Created in-progress task for corrected `SL / TP >= scalper_ratio` rerun.
- 2026-04-22 13:49: Parsed current `_summary_net.json` using `SL / TP >= 6`.
- 2026-04-22 13:50: Computed corrected scalper strategy list, trade counts, net totals, and loss streaks.

## Changes Made
- None. Investigation only.

## Validation
- Input timestamp:
  - Result: `_summary_net.json last_update=2026-04-22T13:49:04.635427`.
- Strategy inclusion:
  - Result: 30 strategy keys matched `SL / TP >= 6`, including `breakout_2_tp5.0_sl50.0` and `breakout_R_2_tp5.0_sl50.0`.
- Trade totals:
  - Result: closed 774, open 109, profit 660, loss 114, breakeven 0.
- Net totals:
  - Result: profit net +13215, loss net -15600, total net -2385.
- Consecutive losses:
  - Result: global max consecutive losses 12; per strategy/product max consecutive losses 3.

## Risks/Notes
- Input file is live and may change during the session.
- Corrected definition includes all strategies where stop loss is at least 6x take profit, not only exactly 6x.

## Completion Status
Status: Complete
Created: 2026-04-22 13:48
Completed: 2026-04-22 13:50
