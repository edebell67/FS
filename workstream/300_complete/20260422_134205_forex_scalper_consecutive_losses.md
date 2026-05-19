# Forex Scalper Consecutive Losses

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
Count consecutive losing streaks for scalper strategies in `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`.

## Context
Input files:
- `TradeApps/breakout/fs/config.json`
- `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`

Scalper definition:
- `scalper_ratio` from `config.json` is `6`.
- Strategy is scalper when `SL / TP == 6`.

## Destination Folder
Destination Folder: None

## Dependency
Dependency: `workstream/300_complete/20260422_132823_forex_scalper_summary_net_trade_counts.md`

## Plan
- [x] 1. Parse scalper closed-trade outcomes chronologically.
  - [x] Test: Confirm input file timestamp and outcome count.
  - Evidence: `_summary_net.json` `last_update=2026-04-22T13:42:31.882814`; parsed 103 closed outcomes: 87 profit, 16 loss, 0 breakeven.

- [x] 2. Count consecutive losing streaks.
  - [x] Test: Report max losing streak and streak distribution.
  - Evidence: Global max consecutive losses = 7; global streak distribution `{1: 1, 2: 1, 3: 2, 7: 1}`. Per strategy/product max = 2; per strategy/product distribution `{1: 14, 2: 1}`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: Python JSON parser output from `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`.
  - Objective-Proved: Consecutive-loss counts are derived from current local JSON.
  - Status: captured

## Implementation Log
- 2026-04-22 13:42: Created in-progress investigation task.
- 2026-04-22 13:42: Parsed scalper outcomes from current live `_summary_net.json`.
- 2026-04-22 13:43: Counted global chronological and per-strategy/product consecutive losing streaks.

## Changes Made
- None. Investigation only.

## Validation
- Input timestamp:
  - Result: `last_update=2026-04-22T13:42:31.882814`.
- Outcome counts:
  - Result: 103 closed outcomes, 87 profit, 16 loss, 0 breakeven.
- Global chronological loss streaks:
  - Result: 5 loss streaks; max consecutive losses = 7; distribution `{1: 1, 2: 1, 3: 2, 7: 1}`.
- Per strategy/product loss streaks:
  - Result: 15 loss streaks; max consecutive losses = 2; distribution `{1: 14, 2: 1}`.

## Risks/Notes
- The input file is live and may change during the session.
- Outcome classification follows the prior investigation: non-open entries are closed trades, and profit/loss is the net delta versus the prior non-open entry for the same strategy/product.
- "Global" means all scalper closed outcomes sorted by timestamp across products and strategies.
- "Per strategy/product" means streaks are counted independently within each scalper strategy/product series.

## Completion Status
Status: Complete
Created: 2026-04-22 13:42
Completed: 2026-04-22 13:43
