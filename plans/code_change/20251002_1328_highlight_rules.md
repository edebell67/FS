# Dashboard Highlight Rules Refresh

## Highlight Criteria
- **Last Update**: no highlight applied.
- **Dark Green (Buy)**: add `highlight-light-green` when value > 0.
- **Green (Buy)**: add `highlight-light-green` when value > 0.
- **Red (Buy)**: add `highlight-light-green` when `red_buy * 2 < red_sell`, add `highlight-light-red` when `red_buy > red_sell * 2`, otherwise clear both.
- **Current Price**: no highlight applied.
- **signal_final**: no highlight applied.
- **Red (Sell)**: uses the same thresholds as Red (Buy), applied to both red cells.
- **Green (Sell)**: add `highlight-light-red` when value > 0.
- **Dark Green (Sell)**: add `highlight-light-red` when value > 0.

## Implementation Notes
- Row rendering (`createRowElement`) and updates (`updateRowCells`) now compute both red column values upfront and call `applyRedBalanceHighlight` so the buy/sell red cells always change together.
- First row refresh only re-evaluates the red balance to keep the top row consistent without touching signal data.
- The helper `applyRedBalanceHighlight` clears prior styles, checks for finite values, and enforces the 2:1 thresholds before adding the light-green/light-red classes.
