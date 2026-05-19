# Forex Scalper Next Trade After Loss

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
Calculate net return if the next closed trade was taken after each losing scalper trade in `2026-04-22/_summary_net.json`.

## Context
Input files:
- `TradeApps/breakout/fs/config.json`
- `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`

Criteria:
- Corrected scalper definition from prior task: `SL / TP >= scalper_ratio`.
- `scalper_ratio = 6`.
- "Next trade" is interpreted as the next closed trade in the same strategy/product series after a losing closed trade.

## Destination Folder
Destination Folder: None

## Dependency
Dependency: `workstream/300_complete/20260422_134814_forex_scalper_ratio_gte_counts.md`

## Plan
- [x] 1. Parse corrected scalper closed trade outcomes.
  - [x] Test: Confirm current file timestamp, loss count, and closed count.
  - Evidence: `_summary_net.json last_update=2026-04-22T13:57:41.992206`; parsed 779 closed trades and 116 losses under `SL / TP >= 6`.

- [x] 2. For every losing trade, collect the next closed trade in the same strategy/product series.
  - [x] Test: Report number of losses with a following trade and number skipped because no later trade exists.
  - Evidence: Same-series next trade exists for 85 losses; 31 losses had no later closed trade in the same strategy/product series.

- [x] 3. Sum next-trade net return and outcome counts.
  - [x] Test: Report next-trade profit/loss counts and total net_return.
  - Evidence: Same-series next trades: 69 winners / 16 losers, profit net +1500, loss net -3500, net_return -2000.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: Python parser output from current `_summary_net.json`.
  - Objective-Proved: Next-trade-after-loss net return is derived from current local JSON.
  - Status: captured

## Implementation Log
- 2026-04-22 13:57: Created in-progress task.
- 2026-04-22 13:58: Parsed corrected scalper set with `SL / TP >= 6`.
- 2026-04-22 13:59: Computed same-strategy/product next closed trade after each loss.
- 2026-04-22 14:00: Computed alternate global chronological next-trade metric for comparison.

## Changes Made
- None. Investigation only.

## Validation
- Same strategy/product next-trade definition:
  - Result: 116 losses, 85 with next closed trade, 31 without later closed trade.
  - Result: next winners 69, next losers 16, next profit net +1500, next loss net -3500, next net_return -2000.
- Global chronological alternate definition:
  - Result: 116 losses, 116 next trades, next winners 41, next losers 75, next profit net +720, next loss net -8785, next net_return -8065.

## Risks/Notes
- Input file is live and may change during the session.
- If the user intended "next trade globally by timestamp" instead of "next trade in same strategy/product series", rerun with that definition.
- The final answer reports the same-strategy/product definition as primary and includes the global chronological alternate to remove ambiguity.

## Completion Status
Status: Complete
Created: 2026-04-22 13:57
Completed: 2026-04-22 14:00
