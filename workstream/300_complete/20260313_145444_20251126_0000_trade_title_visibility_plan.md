# Trade Title Visibility & Deletion Plan

## Objectives
- Allow operators to hide specific trade titles from all monitor views by toggling a per-title `VIEW_STATUS` flag in `config_trade.json`.
- Provide a safe deletion workflow that removes a trade title from configuration, closes open positions tied to it, and terminates any running trade process.

## Implementation Steps
1. **Extend Trade Config Schema**
   - Default every trade entry to `{"VIEW_STATUS": "visible"}` when loading `config_trade.json`; auto-add the field for legacy entries.
   - Add helper functions in `Trades/trade_monitor/trade_monitor.py` (or re-use `execution_manager`) to fetch visible-only titles so UI logic does not repeatedly re-parse configs.

2. **Hide/Unhide Functionality**
   - Implement `execution_manager.set_view_status(trade_title, status)` that validates `visible`/`hidden` and persists the update to `config_trade.json`.
   - Update the RT config page?s table to show a new `View Status` column alongside `[ACTIVE]/[INACTIVE]` status.
   - Introduce an input pattern (e.g., `h#`) on the RT config page that calls the new helper to toggle visibility for a selected title.
   - Ensure `TradeLogProcessor.get_all_unique_trade_titles`, `_build_trade_title_summary`, and downstream pages filter out entries marked hidden so they stay invisible across the UI and exports.

3. **Delete Trade Workflow**
   - Create `delete_trade_config(trade_title, processor)` that:
     1. Collects open trades for the title and generates TWS close JSON files via `generate_tws_close_json`.
     2. Calls `execution_manager.stop_trade` to terminate any running strategy process and clean PID metadata.
     3. Removes the title from `config_trade.json` and `rt_trade_config.json`, then persists both files.
   - Expose this via `d#` input on the RT config page with a confirmation prompt summarizing the cascading actions.

4. **Processor & View Refresh**
   - Ensure `TradeLogProcessor.reload_all_trades()` refreshes the hidden-title cache so filtering stays current after hide/unhide or delete actions.
   - Verify navigation helpers and export functions receive pre-filtered datasets so hidden titles never leak to CSVs.

5. **Error Handling & Logging**
   - Log every hide/unhide/delete attempt to `trade_monitor_run.log`, capturing success/failure details.
   - Display clear CLI feedback when a title is missing, already hidden, or when config writes fail.

## Verification Checklist
- [ ] Launch `python Trades/trade_monitor/trade_monitor.py`, open the RT config page, and confirm the `View Status` column plus hide/unhide controls persist to `config_trade.json`.
- [ ] Hide a title and verify it disappears from open, closed, combined summaries, drill-down menus, and CSV exports.
- [ ] Delete a title with mocked open trades and ensure close-order JSON files appear, the trade process stops (`runtime/*.pid.json` removed), and the title is absent from both configuration files.
- [ ] Restart the monitor to confirm backwards compatibility when `VIEW_STATUS` is missing or when configs are empty.
