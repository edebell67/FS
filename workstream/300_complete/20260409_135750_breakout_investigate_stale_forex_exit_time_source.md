# Source
- User request on 2026-04-09 to create a task and investigate why forex trades for a strategy were being written with invalid `exit_time` values earlier than `entry_time`.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

# Task Summary
Investigate the source of stale forex close timestamps causing invalid `exit_time` values to be written into trade JSON files, with focus on the timestamp path from quote ingestion into `process_new_tick()` and `close_trade()` in `common.py`.

# Context
- Primary code: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Example broken payload symptom: `entry_time` on 2026-04-09 with `exit_time` on 2026-04-08 for the same trade record.
- Key functions already identified:
  - `_normalize_timestamp()`
  - `_load_quote_ticks()`
  - `process_new_tick()`
  - `check_and_exit()`
  - `close_trade()`
- Related strategy files:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\breakout.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_R.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_Rev.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\breakout_R_Rev.py`

Destination Folder: None

Dependency: None

# Plan
- [x] 1. Trace the timestamp flow from quote records into strategy tick processing.
  - [x] Test: Read the quote-loading and dispatch logic to identify the exact source field and ordering used for forex timestamps.
  - Evidence: `fetch_latest_quotes()` reads `record.timestamp|quote_time|time|ts`, normalizes it via `_normalize_timestamp()`, sorts ticks by that timestamp, then the main loop passes `latest_tick.timestamp` directly into each processor's `process_new_tick()`.

- [x] 2. Determine how a stale timestamp can reach `close_trade()`.
  - [x] Test: Follow the exit path and identify the specific failure mode that allows `exit_time < entry_time`.
  - Evidence: `process_new_tick()` stores `current_time = self._coerce_timestamp(timestamp_value)` and `check_and_exit()` passes that `current_time` straight into `close_trade()`. `close_trade()` writes `exit_time_ts` directly into the JSON with no monotonicity guard against `exit_time_ts < entry_time`.

- [x] 3. Identify the concrete root cause in code or runtime assumptions.
  - [x] Test: Correlate the broken payload with the code path and isolate the point where stale timestamps are reused or trusted incorrectly.
  - Evidence: The current runtime config does not define `max_quote_age_seconds_by_product_type`, so `_max_quote_age_seconds_for_product()` returns `None` and the main loop never rejects stale forex timestamps. As a result, an old forex quote timestamp can be treated as the current tick timestamp and written as `exit_time` when TP/SL is hit. Secondary risk: `_save_trade_json()` starts from `disk_data.copy()` and does not explicitly clear stale close fields if an existing file path is reused.

- [x] 4. Record the root cause and remediation recommendation in this task file.
  - [x] Test: Update `Reason Identified` and `Recommended Next Action` with supporting references.
  - Evidence: Captured below.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: relevant code references and broken trade JSON characteristics documented in this task
  - Objective-Proved: Confirms where the stale close timestamp enters the trade lifecycle
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: this lifecycle file
  - Objective-Proved: Captures the root cause and next remediation step
  - Status: captured

# Implementation Log
- 2026-04-09 13:57:50 Created investigation task for stale forex exit timestamps.
- 2026-04-09 14:00:00 Traced quote timestamp normalization and processor dispatch in `common.py`.
- 2026-04-09 14:02:00 Verified that `close_trade()` writes the supplied tick timestamp directly as `exit_time`.
- 2026-04-09 14:04:00 Confirmed there is currently no configured quote-age threshold in the active config, so stale feed timestamps are not rejected before exit handling.
- 2026-04-09 14:05:00 Identified a secondary persistence risk where `_save_trade_json()` can preserve stale close fields from prior disk content if a file path is reused.

# Changes Made
- Added this lifecycle task file only.

# Validation
- Timestamp flow:
  - `fetch_latest_quotes()` normalizes timestamps from the feed record.
  - The main loop takes `latest_tick = quotes[-1]` and passes `latest_tick.timestamp` directly into `processor.process_new_tick(...)`.
  - `check_and_exit()` passes `current_time` directly into `close_trade()`.
  - `close_trade()` writes that timestamp directly as `exit_time`.
- Stale-tick rejection:
  - `_max_quote_age_seconds_for_product()` only works if `max_quote_age_seconds_by_product_type` is configured.
  - The active `config.json` does not currently define that field, so the stale-quote skip path is effectively disabled.
- Broken payload correlation:
  - The provided sample had `entry_time` on 2026-04-09 and `exit_time` on 2026-04-08, which is only possible if an old timestamp was supplied to the close path or stale close metadata was preserved.
- Secondary corruption risk:
  - `_save_trade_json()` starts from `disk_data.copy()` and writes a new open-state payload without explicitly clearing fields like `exit_time`, `exit_price`, and `exit_reason`.

# Risks/Notes
- The broken `exit_time` appears systemic for at least one strategy and is likely upstream of JSON finalization.
- Primary likely root cause: stale forex feed timestamps are trusted as current tick time because no age threshold is configured.
- Secondary risk: even after the stale-timestamp issue is fixed, file-path reuse could preserve stale close metadata unless open saves explicitly clear close fields.

# Reason Identified
- The close timestamp written to the forex trade JSON is not generated locally at close time; it is taken directly from the tick timestamp flowing through `process_new_tick()`.
- The quote-ingestion loop in `common.py` trusts feed timestamps end-to-end and currently has no active max-age rejection for forex ticks because `max_quote_age_seconds_by_product_type` is missing from the active config.
- That means a stale forex quote timestamp can reach `check_and_exit()` and then be written as `exit_time`, producing impossible records such as `exit_time < entry_time`.
- There is also a secondary persistence bug risk: `_save_trade_json()` preserves prior disk fields and does not explicitly clear old close metadata when writing a fresh open-state file.

# Recommended Next Action
- Add a defensive guard in `close_trade()`:
  - if `exit_time_ts` is missing or earlier than `entry_time`, replace it with `pd.Timestamp.now()` or reject/log the stale value.
- Enable stale quote rejection by configuring `max_quote_age_seconds_by_product_type` for forex and other product types, or enforce a safe default in code when the config is missing.
- Harden `_save_trade_json()` so open-state writes explicitly clear `exit_time`, `exit_price`, `exit_reason`, and any stale closed-state fields.
- After patching, validate against the affected strategy and confirm no file can be written with `exit_time < entry_time`.

# Completion Status
Complete - 2026-04-09 14:06:00
