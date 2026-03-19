# P&L Graph Metric Refinements

The goal is to refine the "Buy Trades" and "Sell Trades" metrics in the P&L Graph. Currently, while the ranking logic sorts these by trade counts, the chart plots the Net P&L. I will update the chart to plot trade counts for these metrics and ensure tooltips are formatted correctly.

## Proposed Changes

### P&L Graph UI Logic

#### [MODIFY] [pnl_graph.js](file:///c:/Users/edebe/eds/TradeApps/breakout/pnl_graph.js)

- Update `updateChart` to use `pt.b_c` and `pt.s_c` when `metric` is `buy_trades` or `sell_trades`.
- Update the tooltip callback in `updateChart` to display raw numbers instead of currency when a trade-count metric is selected.
- Add a check in `updateChart` to adjust the Y-axis tick formatting if needed (though Chart.js default should be fine for counts).

### Application Metadata

#### [MODIFY] [Constants.py](file:///c:/Users/edebe/eds/TradeApps/breakout/Constants.py)

- Update `VERSION` to `V20260114_2355` (or current timestamp).

## Verification Plan

### Manual Verification
- Open `pnl_graph.html` in a browser.
- Select "Buy Trades (Positive Net)" from the Metric dropdown.
- Add some strategy/product overlays.
- Verify that the graph shows integers (counts) instead of currency.
- Verify that the tooltips show "Trades: 5" (example) instead of "$5.00".
- Toggle playback and ensure the counts update correctly over time.
- Verify that "Net", "Buy Net", and "Sell Net" still show currency values.
