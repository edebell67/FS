# Forex Scalper Summary Net Trade Counts

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
Investigate `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json` and report scalper strategy counts plus closed/open/profit/loss trade counts. Scalper strategies are defined by the TP:SL relationship using `scalper_ratio` from `config.json`.

## Context
Input files:
- `TradeApps/breakout/fs/config.json`
- `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`

Interpretation:
- `config.json` has `scalper_ratio: 6`.
- For strategy names with `tpX_slY`, scalper means `SL / TP == scalper_ratio` because the configured ratio describes stop-loss size relative to take-profit size in existing strategy naming.

## Destination Folder
Destination Folder: None

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect config and summary JSON shape.
  - [x] Test: Confirm `scalper_ratio` and identify trade/status fields in `_summary_net.json`.
  - Evidence: `config.json` has `scalper_ratio: 6`; `_summary_net.json` has top-level `strategies` with per-strategy/per-product entry arrays containing `t`, `net`, `b_c`, `s_c`, and occasional `open: true` / `count`.

- [x] 2. Count scalper strategies.
  - [x] Test: Parse strategy names with `tp..._sl...` and count unique strategies where `SL / TP == scalper_ratio`.
  - Evidence: `scalper_ratio=6`, `total_strategy_keys=122`, `scalper_strategy_keys=6`.

- [x] 3. Count closed/open/profit/loss trades for scalper strategies.
  - [x] Test: Parse trade records associated with scalper strategies and classify by open/closed and positive/negative net/PnL.
  - Evidence: `closed=100`, `open=12`, `profit=87`, `loss=13`, `breakeven=0`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: test_output
  - Artifact: Python JSON inspection of `TradeApps/breakout/fs/config.json` and `TradeApps/breakout/fs/json/live/forex/2026-04-22/_summary_net.json`.
  - Objective-Proved: Counts are derived from local JSON and config.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Count output: `scalper_strategy_keys=6`, `closed=100`, `open=12`, `profit=87`, `loss=13`, `breakeven=0`.
  - Objective-Proved: Requested scalper strategy and trade outcome counts are complete.
  - Status: captured

## Implementation Log
- 2026-04-22 13:28: Created in-progress investigation task.
- 2026-04-22 13:29: Confirmed input file exists and read `scalper_ratio=6` from `config.json`.
- 2026-04-22 13:31: Inspected `_summary_net.json` schema and confirmed cumulative strategy/product entry arrays.
- 2026-04-22 13:35: Counted scalper strategies where `SL / TP == 6`.
- 2026-04-22 13:39: Counted closed/open/profit/loss trades using non-open entries as closed records and `open:true` entries as open trade markers.

## Changes Made
- None. Investigation only.

## Validation
- JSON schema inspection:
  - Result: top-level keys are `last_update`, `session_max_net`, `strategies`.
  - Result: strategy/product entries contain `t`, `net`, `buy_net`, `sell_net`, `b_c`, `s_c`, and sometimes `open: true`, `count`.
- Scalper strategy count:
  - Result: 6 strategy keys matched `SL / TP == scalper_ratio`.
- Trade outcome count:
  - Result: 100 closed entries, 12 open markers, 87 profitable closed entries, 13 losing closed entries, 0 breakeven.

## Risks/Notes
- `_summary_net.json` is cumulative by strategy/product, but for this file the entry-level interpretation reconciles cleanly: 100 non-open entries plus 12 open markers.
- Profit/loss classification uses per-entry `net` delta versus the prior non-open entry for the same strategy/product. Positive delta = profit trade, negative delta = losing trade, zero = breakeven.
- `b_c+s_c` is not strictly monotonic in three scalper series, so final cumulative counts alone are not used for profit/loss classification.

## Completion Status
Status: Complete
Created: 2026-04-22 13:28
Completed: 2026-04-22 13:40
