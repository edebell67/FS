# Task: Add Alt Net Column To Trade Bucket Strategy Drilldown Trades

Source: User request on 2026-04-12 to add an `alt_net` column to the trades page opened from Trade Bucket strategy drilldown.

Task Type: feature

Task Attributes:
- priority: medium
- execution_owner: codex
- workflow_ready: true
- ui_task: true

## Task Summary
Add an `alt_net` column to the strategy drilldown trades table launched from Trade Bucket cards so users can view both normal `net_return` and `alt_net` values for each trade directly in the drilldown.

## Scope Notes
- This applies to the Trade Bucket strategy drilldown modal/table.
- The column should display per-trade `alt_net` from the trade payload when available.
- Existing L-trade filtering and metric-aware drilldown behavior must remain intact.
- The table layout should remain readable with the added column.

## Validation Plan
- Update the Trade Bucket drilldown table headers and row rendering to include `alt_net`.
- Verify the drilldown still renders correctly for `net` and `alt_net` strategy views.
- Run a focused sanity check or regression validation for the updated drilldown rendering path.

## Execution Log
- 2026-04-12 23:18 Moved task to in-progress and reviewed the Trade Bucket drilldown modal/table in `TradeApps/breakout/fs/trade_bucket.html`.
- 2026-04-12 23:22 Added an `Alt Net` header column next to the existing `Net P&L` column in the strategy drilldown trades table.
- 2026-04-12 23:24 Updated row rendering to display both the metric-aware `Net P&L` value and the raw `alt_net` value for each trade.
- 2026-04-12 23:25 Updated drilldown loading, empty, and error-row `colspan` values to match the expanded 11-column table layout.

## Validation Results
- Command: `rg -n 'Alt Net|Net P&L|colspan="11"|getTradePnlValue\(t, activeMetric\)|getTradePnlValue\(t, ''alt_net''\)' C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html`
- Result: confirmed the new `Alt Net` header, dual P&L row rendering, and all updated 11-column drilldown states.

## Outcome
- The Trade Bucket strategy drilldown trades table now shows both `net_return` and `alt_net`.
- Existing metric-aware drilldown behavior remains intact: the `Net P&L` column still reflects the active drilldown metric, while `Alt Net` exposes the raw inverted P&L for comparison.
