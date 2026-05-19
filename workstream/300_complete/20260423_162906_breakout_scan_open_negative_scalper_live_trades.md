# Source
User request: create a task to run a scan on open trades for scalper strategies where the `net_return` is currently negative.

# Task Type
standard

# Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false

# Task Summary
Scan current open trades and identify those that are scalper strategies with negative current `net_return`.

# Context
- `TradeApps/breakout/fs/json/<mode>/<product_type>/<date>/`
- `TradeApps/breakout/fs/extract_live_trades.py`
- `TradeApps/breakout/fs/common.py`
- `TradeApps/breakout/fs/config.json`

# Destination Folder
None

# Dependency
None

# Plan
- [x] 1. Determine the exact source files and scalper classification rule for the scan.
  - Test: Inspect the relevant trade artifacts and config values; expected pass condition is a clear rule for identifying open scalper trades.
  - Evidence: `config.json` shows `scalper_ratio: 6`; scan used day-folder `*_op.json` files and classified a strategy as scalper when `sl >= tp * 6`.
- [x] 2. Run the scan for open trades where `net_return < 0`.
  - Test: Execute a read-only scan; expected pass condition is a count and list of matching trades.
  - Evidence: Read-only scan completed against `json/live/forex/2026-04-23/*_op.json`; found 9 open negative scalper trades.
- [x] 3. Summarize the scan output with enough detail to trace each match.
  - Test: Produce product/strategy-level results; expected pass condition is a usable report of all matching open scalper trades.
  - Evidence: Matching trades are listed below with file, product, strategy, entry time, direction, and current negative net.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: trade JSON files and config values used for the scan
  - Objective-Proved: Identifies which open live trades qualify as negative scalper trades.
  - Status: captured

# Implementation Log
- 2026-04-23 16:29 - Created task.
- 2026-04-23 16:32 - Confirmed `scalper_ratio: 6` in `config.json`.
- 2026-04-23 16:33 - Scanned `json/live/forex/2026-04-23/*_op.json` for open trades with negative `net_return` and scalper TP/SL ratio.
- 2026-04-23 16:34 - Confirmed `_live_trades.json` is currently empty, so there are zero negative open scalper trades with `is_live_trade == true`.

# Changes Made
None.

# Validation
- Read `TradeApps/breakout/fs/config.json`.
- Read `TradeApps/breakout/fs/json/live/forex/2026-04-23/_live_trades.json`.
- Read `TradeApps/breakout/fs/json/live/forex/2026-04-23/*_op.json`.
- Executed a read-only Python scan over the day folder to classify scalpers and filter `net_return < 0`.

# Risks/Notes
- The exact result depends on selected `mode`, `date`, and `product_type` at scan time.
- This scan used the current scope `live/forex/2026-04-23`.
- `_live_trades.json` had `trade_count: 0`, so none of the matching open negative scalper trades are currently flagged as live trades.

## Findings
Scope:
- `mode`: `live`
- `product_type`: `forex`
- `date`: `2026-04-23`
- `scalper_ratio`: `6`

Result summary:
- Open negative scalper trades in `*_op.json`: `9`
- Open negative scalper trades with `is_live_trade == true`: `0`

Matches:
- `EURNZD_C` / `breakout_2_tp3.0_sl50.0` / `2026-04-23T10:18:07.801404` / `SHORT` / `net_return -440.00`
- `EURNZD_C` / `breakout_2_tp5.0_sl50.0` / `2026-04-23T10:18:07.801404` / `SHORT` / `net_return -440.00`
- `NZDAUD_C` / `breakout_2_tp3.0_sl50.0` / `2026-04-23T10:51:20.958181` / `SHORT` / `net_return -410.00`
- `NZDAUD_C` / `breakout_2_tp5.0_sl50.0` / `2026-04-23T10:51:20.958181` / `SHORT` / `net_return -410.00`
- `GBPEUR_S` / `breakout_2_tp3.0_sl50.0` / `2026-04-23T06:00:35.224534` / `SHORT` / `net_return -120.00`
- `GBPEUR_S` / `breakout_R_2_tp3.0_sl50.0` / `2026-04-23T06:34:13.233597` / `SHORT` / `net_return -100.00`
- `GBPEUR_S` / `breakout_R_2_tp5.0_sl50.0` / `2026-04-23T06:16:39.926883` / `SHORT` / `net_return -90.00`
- `CAD` / `breakout_2_tp5.0_sl30.0` / `2026-04-23T14:00:53.131220` / `LONG` / `net_return -35.00`
- `CAD` / `breakout_2_tp5.0_sl50.0` / `2026-04-23T14:00:53.131220` / `LONG` / `net_return -35.00`

# Completion Status
Complete - 2026-04-23 16:35.
