# Task: Breakout Archive Condition Update (20260224_140700)

## Task Summary
Modify the archive functionality condition so that it sets the `is_archived` status (or equivalent) to true when there are no `Breakout*.json` files left in the daily folder, rather than requiring the folder to be completely empty.

## Context
Currently, the archiving logic checks if the daily directory is completely empty before marking it as archived. However, in reality, summary files (like `_summary_net.json`, `_market_update.json`, `_trades_summary.json`) are immediately recreated or exist persistently in the folder, preventing the empty folder condition from ever being met.

## Sub-tasks
- [x] Identify the script/function responsible for the archive logic (e.g., `archive_old_trades.py` or within `trade_viewer_api.py`).
- [x] Change the check from `len(os.listdir(folder)) == 0` to a targeted glob search for `Breakout*.json` (case-insensitive) or any raw trade JSON files.
- [x] If no such raw trade files remain, mark the folder/date as fully archived.

## Status
COMPLETE
