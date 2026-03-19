# Negative Alt Net Closed Trade View Plan

## Goal
Expose the most recent closed trades whose Alt Net ($) is negative by surfacing a synthetic row on the "Closed Trades Summary by Trade Title" page. Selecting that row should drill into BUY/SELL groupings and ultimately list the individual trades so operators can review underperformers quickly.

## Implementation Steps

1. **Data Plumbing in `TradeLogProcessor`**
   - Add `get_recent_negative_alt_trades(limit: int = 25)` that filters `self.all_trades['closed']` for `Alt Net ($) < 0`, sorts by `Exit Time` (fallback to `Last Update Time`), and returns the newest rows.
   - Provide helper methods to group these filtered trades by `Position` (BUY/SELL) and to format them for table display, mirroring the existing `get_position_summary` and `get_individual_trades` helpers.

2. **Closed Summary Augmentation**
   - Extend `_build_trade_title_summary(..., trade_type='closed')` in `trade_monitor.py` to append a synthetic row with `Trade Title = 'negative Alt_nets'` when the helper returns any rows. Populate its totals using the filtered dataset and mark it with a flag so the view layer knows to treat it specially.
   - Update the headers to include the new row seamlessly without disturbing exports.

3. **UI Extensions**
   - In `view_trade_names_summary`, detect when the selected row corresponds to the synthetic title. Route the drill?down to a new function (`view_negative_alt_positions`) rather than the generic `view_position_summary`.
   - Implement `view_negative_alt_positions` to display BUY/SELL groupings with cumulative Net/Alt values and allow drill?down (e.g., input `#` or `b` rules identical to other pages). Selecting a position goes to `view_negative_alt_trades`.
   - Implement `view_negative_alt_trades` to list each recent negative Alt trade (trade number, entry/exit, pnl metrics) and allow CSV export similar to `view_individual_trades`.

4. **Shared Behaviors**
   - Reuse `print_table`, navigation helpers, timeout handling, and export hooks so the new views behave like existing ones.
   - Ensure hidden trade titles have no effect here (these trades are already closed but still should respect the same filtering logic if the base data excludes them).

5. **Testing / Validation**
   - Start the monitor, navigate to Closed Trades Summary, and confirm "negative Alt_nets" only appears when data exists.
   - Drill down through BUY/SELL to the individual trades and verify totals match the source JSON files.
   - Export from each new view to check CSV formatting.
   - Verify navigation (back, global jumps) and timeout refresh flows remain intact.

