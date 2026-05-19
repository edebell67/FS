# Source
- User request on 2026-04-08 to generate an investigation task for why no new live trades have been created for hours even though the price feed is reported as active.
- Supporting screenshot context: System Health shows `Price Feed Connection: Active` and `Latest Trade Age: 234 min` on the live panel.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

# Task Summary
Investigate why the live breakout system has produced no new trades for multiple hours while the price feed appears active, with primary focus on the trade-generation and live-order gating logic in `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`. The task must identify and document the concrete reason for suppression inside this lifecycle file.

# Context
- Workspace: `C:\Users\edebe\eds`
- Primary investigation target: `C:\Users\edebe\eds\TradeApps\breakout\fs\common.py`
- Related output area: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\`
- Related runtime/config files likely involved: `config.json`, `activations.json`, `grid_live.json`, daily live trade JSON outputs, trade summaries, strategy selection outputs, and any runtime logs that explain gating.
- Symptom to explain: price feed looks connected, but no fresh trades are being generated.

Destination Folder: None

Dependency: None

# Plan
- [x] 1. Capture the current symptom with concrete runtime evidence.
  - [x] Test: Inspect the latest live day-folder outputs and any health/summary artifacts to confirm the most recent trade timestamp and whether fresh strategy/trade candidate files are still updating.
  - Evidence: `fs/json/live/2026-04-08/_market_update*.json` and `fs/json/live/forex/2026-04-08/_targeted_strategies.json` continued updating around 23:38, while the latest non-summary forex trade JSON remained around 19:27.

- [x] 2. Trace the trade-creation path in `common.py` from fresh price input to trade file creation.
  - [x] Test: Read the relevant `common.py` functions and enumerate the exact guards that can block new trade creation while the feed remains connected, including activation, schedule, profitability, market bias, cap, duplicate, and routing checks.
  - Evidence: `common.py` shows live-order gating in `_handle_live_orders()` and cap enforcement in `_create_l_trade_order()`; `grid_live_monitor.py` separately enforces a global live-trade cap via `count_current_live_trades()`.

- [x] 3. Determine which specific guard or missing upstream condition is stopping today's live trades.
  - [x] Test: Inspect the current-day configs/artifacts/logs and match the observed runtime state to one concrete blocking reason, with file references or line references proving it.
  - Evidence: `grid_live_monitor.log` repeatedly reports `Current Live Trades: 2, Max Allowed: 1` and `Match:0`; the two counted open live trades are test metals files `breakout_test_test-guid_SI_20260408_120554_..._op.json` and `breakout_test_test-guid_SI_20260408_120632_..._op.json`, both `status: "OPEN"` and `is_live_trade: true`.

- [x] 4. Record the root cause and recommended next action inside this task file.
  - [x] Test: Update this lifecycle file with a `Reason Identified` entry and a `Recommended Next Action` entry that cite the proving artifacts.
  - Evidence: Captured in `Reason Identified`, `Recommended Next Action`, and `Validation` below.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\grid_live_monitor.log`
  - Objective-Proved: Confirms the live engine is still running but repeatedly blocking new promotions because `Current Live Trades: 2, Max Allowed: 1`.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\2026-04-08\breakout_test_test-guid_SI_20260408_120554_2_0.00015_30.0_5.0_op.json`
  - Objective-Proved: One of the stale open live-trade JSONs that is consuming the global cap.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\2026-04-08\breakout_test_test-guid_SI_20260408_120632_2_0.00015_30.0_5.0_op.json`
  - Objective-Proved: Second stale open live-trade JSON consuming the global cap, taking the total counted live trades to 2.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-08\_targeted_strategies.json`
  - Objective-Proved: Confirms the feed/selection pipeline is still active and updated late in the session, so the issue is not a dead price feed.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: this lifecycle file
  - Objective-Proved: Captures the explicit reason no new trades were created and the next remediation step.
  - Status: captured

# Implementation Log
- 2026-04-08 23:24:59 Created investigation task from user request.
- 2026-04-08 23:24:59 Investigation objective explicitly set to capture the concrete no-trade reason within this task file.
- 2026-04-08 23:38:07 Moved lifecycle file into `workstream/200_inprogress` and began investigation.
- 2026-04-08 23:40:00 Confirmed live summaries were still updating while non-summary forex trade files had stopped updating after the 19:27 range.
- 2026-04-08 23:43:00 Traced live-order gating in `common.py` and live-cap enforcement in `grid_live_monitor.py`.
- 2026-04-08 23:46:00 Identified two stale `metals` test trades marked `is_live_trade=true` and `status=OPEN`, matching the monitor's `Current Live Trades: 2` log output.

# Changes Made
- Added this lifecycle task file only.

# Validation
- Runtime freshness:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-04-08\_market_update.json` last updated around 23:38.
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-08\_targeted_strategies.json` last updated around 23:38 and still showed eligible strategies.
- Current blocker from monitor:
  - `grid_live_monitor.log` repeatedly logs `Current Live Trades: 2, Max Allowed: 1`.
  - The same log repeatedly logs `Mon:1 Match:0 Pending:0`, showing the monitor loop is alive but not promoting anything.
- Files consuming the cap:
  - `...metals\2026-04-08\breakout_test_test-guid_SI_20260408_120554_2_0.00015_30.0_5.0_op.json`
  - `...metals\2026-04-08\breakout_test_test-guid_SI_20260408_120632_2_0.00015_30.0_5.0_op.json`
  - Both files are `status: OPEN`, `order_sent_net: true`, `order_sent_alt: true`, and `is_live_trade: true`.
- Code path proving the cap logic:
  - `grid_live_monitor.py` `count_current_live_trades()` counts every `*_op.json` with `is_live_trade == true`.
  - `grid_live_monitor.py` uses that count against `max_live_trades` before allowing more live promotions.
- Additional observation:
  - Several forex trade JSONs from the last non-summary trade burst include `trade_block_reason` values showing bypass/grid-live mismatch, but the active runtime blocker explaining the present multi-hour dry spell is the global live-cap exhaustion.

# Risks/Notes
- An active price feed does not by itself prove the trade engine is eligible to create new trades; upstream candidate starvation or downstream guardrails in `common.py` may still suppress output.
- The two blocking `SI` files appear to be test artifacts rather than intended live production positions, so they should be reviewed and cleared carefully.
- Separate from the cap issue, some recent forex candidate files show `trade_block_reason` values tied to grid-live mismatch. That is a secondary suppression signal, but it is not required to explain the current monitor-wide “no new live trades” condition.

# Reason Identified
- The current reason no new live trades have been created for hours is that the live monitor believes there are already **2 open live trades while the configured max is 1**, so it blocks all further live promotion.
- The 2 counted live trades are stale test metal entries:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\2026-04-08\breakout_test_test-guid_SI_20260408_120554_2_0.00015_30.0_5.0_op.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\2026-04-08\breakout_test_test-guid_SI_20260408_120632_2_0.00015_30.0_5.0_op.json`
- `grid_live_monitor.py` counts any open `*_op.json` with `is_live_trade=true`, and `grid_live_monitor.log` shows that this count remains stuck at `2` throughout the evening while `max_live_trades` is `1`.

# Recommended Next Action
- Review and clear or close the two stale `SI` test `*_op.json` files so they no longer count as active live trades, then restart or let `grid_live_monitor.py` re-evaluate the live count.
- After clearing them, confirm `grid_live_monitor.log` drops below the cap and stops reporting `Current Live Trades: 2, Max Allowed: 1`.
- If no new live trades still appear after the cap is cleared, investigate the secondary forex `trade_block_reason` path tied to grid-live/bypass mismatch.

# Completion Status
Complete - 2026-04-08 23:46:00
