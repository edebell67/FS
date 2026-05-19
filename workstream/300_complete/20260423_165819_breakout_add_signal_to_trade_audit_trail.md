# Source
User requirement: need to be able to determine what happens to missing trades after signal is generated.

# Task Type
standard

# Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false

# Task Summary
Add an audit trail for breakout signal generation so each signal can be traced through trade JSON creation, activation checks, guard blocks, and live order handling.

# Context
- `TradeApps/breakout/fs/common.py`
- `TradeApps/breakout/fs/json/live/<product_type>/<date>/`
- Breakout strategy runtime and trade persistence flow

# Destination Folder
None

# Dependency
Investigation context from `workstream/200_inprogress/20260423_164826_breakout_restart_from_start_trade_generation_investigation.md`

# Plan
- [x] 1. Identify the exact pipeline stages where signal outcomes should be audited.
  - Test: Read signal/trade handling code; expected pass condition is a stage list covering signal, save, activation, guard, and order handling.
  - Evidence: `common.py` stage coverage confirmed across `enter_trade`, `_save_trade_json`, `_check_immediate_live_activation`, and `_handle_live_orders`.
- [x] 2. Implement a persisted per-day audit file for signal lifecycle events.
  - Test: `python -m py_compile TradeApps/breakout/fs/common.py` passes after implementation.
  - Evidence: `_signal_audit.json` writer added in `common.py`; compile validation passed.
- [x] 3. Emit audit events for the main failure/stop paths after signal generation.
  - Test: Code inspection confirms events for generated signal, saved trade, blocked activation, blocked order, and successful order path.
  - Evidence: audit events added for signal generation, JSON save, immediate activation blocks, live-order blocks, attempts, successes, and create-failures.
- [x] 4. Summarize the new traceability path and access location.
  - Test: Provide exact artifact path and event meaning; expected pass condition is usable operator guidance.
  - Evidence: access path and event summary documented below.

# Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/common.py`
  - Objective-Proved: Signal lifecycle audit trail implemented in runtime code.
  - Status: complete
- Evidence-Type: test_output
  - Artifact: `python -m py_compile TradeApps/breakout/fs/common.py`
  - Objective-Proved: Updated runtime code is syntactically valid.
  - Status: complete

# Implementation Log
- 2026-04-23 16:58 - Created task.
- 2026-04-23 17:07 - Added per-day `_signal_audit.json` append helper and strategy-level `_audit_signal_event(...)` wrapper in `common.py`.
- 2026-04-23 17:12 - Added audit events for signal generation, open-trade JSON save, immediate activation block/attempt/result, and normal live-order block/attempt/result.
- 2026-04-23 17:13 - Validated syntax with `python -m py_compile TradeApps/breakout/fs/common.py`.

# Changes Made
- `TradeApps/breakout/fs/common.py`
  - Added `_signal_audit.json` artifact creation in each product/date folder.
  - Added `signal_generated` and `open_trade_json_saved` events.
  - Added immediate activation audit events:
    - `immediate_activation_blocked_market_bias`
    - `immediate_activation_blocked_grid_side`
    - `immediate_activation_blocked_non_positive_summary`
    - `immediate_activation_attempt`
    - `immediate_activation_order_created`
    - `immediate_activation_create_failed`
  - Added normal live-order audit events:
    - `live_order_path_skipped_generation_mode`
    - `live_order_blocked_market_bias`
    - `live_order_blocked_auto_promote_weekly_net`
    - `live_order_blocked_bypass_strategy_not_in_grid_live`
    - `live_order_blocked_bypass_grid_side`
    - `live_order_blocked_bypass_summary_non_positive`
    - `live_order_blocked_activation_inactive`
    - `live_order_blocked_profitability_guard`
    - `live_order_attempt`
    - `live_order_created`
    - `live_order_create_failed`

Traceability artifact:
- `TradeApps/breakout/fs/json/<run_mode>/<product_type>/<date>/_signal_audit.json`
- Example:
  - `TradeApps/breakout/fs/json/live/forex/2026-04-23/_signal_audit.json`

# Validation
- `python -m py_compile TradeApps/breakout/fs/common.py`

# Risks/Notes
- This task adds observability only; it should not change trade-selection behavior.
- `_signal_audit.json` is trimmed to the last 5000 events per product/date to keep file size bounded.
- Corrupt audit files are preserved as `_signal_audit_corrupt_YYYYMMDD_HHMMSS.json` before a new audit file is started.

# Completion Status
Complete.
