# Source
- User request on 2026-04-09 to proceed with a forex-specific investigation because the displayed latest-trade age is sourced from the forex folder, while the previously identified stale blockers were in metals.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

# Task Summary
Investigate the forex-local cause of the stale "Latest Trade Age" symptom by tracing how system health calculates the forex latest-trade age and by identifying any forex-specific blocker preventing new live forex trade files from being created after the last visible forex trade burst.

# Context
- UI page: `C:\Users\edebe\eds\TradeApps\breakout\fs\system_health.html`
- API source: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Forex day folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-08`
- Trade logic source: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Related prior task: `C:\Users\edebe\eds\workstream\300_complete\20260408_232459_breakout_investigate_no_new_live_trades_despite_active_price_feed.md`

Destination Folder: None

Dependency: None

# Plan
- [x] 1. Confirm how system health computes forex latest-trade age.
  - [x] Test: Read the relevant API and UI code paths and identify the exact data source, file path, and timestamp field used for forex latest-trade age.
  - Evidence: `trade_viewer_api.py` `_get_health_status()` resolves the live day directory via `_resolve_day_dir(mode, today_str)` and calculates age from the filesystem modified time of the newest non-underscore JSON file in that forex folder; `system_health.html` simply displays `latest_trade_age_min`.

- [x] 2. Compare the system-health forex age calculation with the actual latest timestamps in the forex folder.
  - [x] Test: Inspect the latest forex summary/trade files and determine whether the UI age matches the newest forex trade timestamp or is based on a stale/incorrect source.
  - Evidence: The age calculation ignores `_targeted_strategies.json`, `_summary_net.json`, and other underscore-prefixed summaries. On 2026-04-08 the forex summaries were updating near 23:38 while non-summary trade files had been stale around 19:27, so the UI could correctly show a multi-hour forex trade age even with fresh summary/feed activity. By 2026-04-09 01:21 new forex non-summary close files had appeared, which would reduce the displayed age.

- [x] 3. Identify the forex-local blocker for new forex live trades, if present.
  - [x] Test: Inspect recent forex trade JSON files and live-order gating artifacts to determine the specific forex-local block reason after the last forex trade burst.
  - Evidence: Recent forex trade JSONs from 2026-04-08 around 19:26-19:27 record `trade_block_reason` values of `NET: Bypass blocked (strategy not monitored in grid_live); ALT: Bypass blocked (strategy not monitored in grid_live)`, proving a forex-local live-promotion block in `common.py` for those strategies/products.

- [x] 4. Record the forex-specific reason and remediation.
  - [x] Test: Update this file with a `Reason Identified` entry and a `Recommended Next Action` entry supported by the proving artifacts.
  - Evidence: Captured below in `Reason Identified`, `Recommended Next Action`, and `Validation`.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: relevant code and forex-day JSON files referenced in this task
  - Objective-Proved: Confirms both the latest-trade-age data source and the forex-local blocker
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: this lifecycle file
  - Objective-Proved: Captures the forex-specific root cause and recommended remediation
  - Status: captured

# Implementation Log
- 2026-04-09 01:51:21 Created forex-specific follow-up investigation task.
- 2026-04-09 01:53:00 Read the system-health API and UI age-display logic.
- 2026-04-09 01:55:00 Compared the age logic with current forex non-summary file mtimes.
- 2026-04-09 01:57:00 Re-read representative forex trade JSONs showing local bypass/grid-live block reasons.

# Changes Made
- Added this lifecycle task file only.

# Validation
- Age calculation path:
  - `trade_viewer_api.py` `_get_health_status()` uses `_resolve_day_dir("live", today)` and scans only non-underscore `*.json` files in the resolved folder.
  - It computes `latest_trade_age_min` from the newest file's `st_mtime`, not from `entry_time`, `exit_time`, feed timestamps, or summary mtimes.
- Forex-folder behavior:
  - On 2026-04-08 the forex summary files were still updating late in the evening, but the latest non-summary forex trade files were older, so the UI age could legitimately show several hours.
  - On 2026-04-09 around 01:21, fresh forex close files appeared, proving the folder-local age metric drops only when another non-summary forex trade file is written.
- Forex-local blocker proof:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-08\breakout_R_2_tp30.0_sl50.0_e43e5b7a_GBPEUR_C_20260408_182600_2_0.00015_30.0_50.0_op.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-08\breakout_R_2_tp5.0_sl50.0_ce751d67_GBPEUR_C_20260408_182600_2_0.00015_5.0_50.0_cl.json`
  - Both include `trade_block_reason` showing bypass blocked because the strategy was not monitored in `grid_live`.

# Risks/Notes
- The stale age symptom may be caused by either a UI/API age-calculation issue or a genuine lack of new forex trade files, or both.
- This task shows the age display was not using the wrong folder, but it is sensitive only to actual forex trade-file writes, not to summary/feed freshness.
- The forex-local block observed here does not prove every missing forex trade had the same reason, but it does prove a real local gating path existed in the affected forex files.

# Reason Identified
- The system-health "Latest Trade Age" for live mode is indeed using the forex folder, but it is calculated from the filesystem modified time of the newest non-summary forex trade JSON file, not from the feed status or summary-file updates.
- That means the UI can show a very old age even while `_targeted_strategies.json`, `_summary_net.json`, and the feed are actively updating.
- In the captured forex trade files from the affected evening window on 2026-04-08, the forex-local live-order block reason was:
  - `Bypass blocked (strategy not monitored in grid_live)`
- So the forex-specific issue was not “wrong folder”; it was:
  1. the age metric only advancing on actual forex trade-file writes, and
  2. recent forex candidates carrying a local bypass/grid-live mismatch that prevented live promotion.

# Recommended Next Action
- If the health card should reflect trading activity rather than raw forex file mtime, change the age source to a domain-specific timestamp such as the latest forex trade `entry_time` / `exit_time`, or display separate values for `latest forex trade file`, `latest summary update`, and `feed latency`.
- For the forex-local no-live-trade behavior, review why bypass/grid-live mode was active for strategies like `breakout_R_2_tp30.0_sl50.0` on `GBPEUR_C` while `grid_live.json` only contained `breakout_R_2_tp5.0_sl10.0` for that product.
- Specifically inspect the runtime setting/history of `bypass_criteria_check` and the intended contract between `common.py` and `grid_live.json` for forex live promotion.

# Completion Status
Complete - 2026-04-09 01:58:00
