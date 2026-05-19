# Task: Investigate workflow supporting Auto Buy and Auto Sell buttons on strategy_performance.html

Source: User Directive
Task Type: investigation
Task Attributes:
  workflow_task: true
  workflow_name: "breakout_trading_system"
  workflow_stage: backlog
Dependency: None

## Task Summary
Investigate and document the end-to-end workflow for the "Auto Buy" and "Auto Sell" buttons on the `strategy_performance.html` screen. This includes tracing the UI event handlers, the API communication layer, the backend storage mechanism (primarily `grid_live.json`), and the downstream consumption of these activation states by the trading strategies in `common.py`.

## Investigation Findings

### 1. UI Event Workflow (`strategy_performance.html`)
- **Trigger**: `toggleAutoActivation(strategy, parm, product, direction, button)` is called when clicking the toggle buttons.
- **Payload Generation**:
  - `metric`: Derived from direction (`buy_net` or `sell_net`).
  - `modelName`: Combined strategy and parameter string (e.g., `Strategy12_60_10_20_20`).
  - `group`: Set to the `product` (e.g., `GBPUSD`).
  - `manual`: Hardcoded to `true` for UI-initiated toggles.
  - `source`: Hardcoded to `strategy_performance`.
- **Action**:
  - Fetches current grid state via `GET /api/grid_live`.
  - Toggles (adds/removes) the specific model from the list.
  - Submits updated list via `POST /api/grid_live`.
  - Calls `POST /api/promote_trades` if activating.

### 2. Backend API Workflow (`trade_viewer_api.py`)
- **`POST /api/grid_live`**:
  - Receives the model list for a group.
  - Uses `GRID_LIVE_LOCK` for thread safety.
  - Updates `grid_live.json`.
  - Triggers `_sync_grid_to_activations(grid_data, mode)`.
- **`_sync_grid_to_activations`**:
  - Rebuilds `activations.json` from `grid_live.json`.
  - Preserves `manual` flag and `activated_at` timestamps.
  - Normalizes metrics (e.g., `net` -> `buy_net` + `sell_net`).
- **`GET /api/activations`**:
  - Used by UI to display button states.
  - Currently has a hardcoded logic error: sets `manual: False` for all entries derived from `grid_live.json`, causing the UI to show 'A' instead of 'M'.

### 3. Trade Promotion (`/api/promote_trades`)
- Scans `open_trades` for the specified mode/date.
- Matches trades using `_match_trade(data, strategy, product, direction, parm)`.
- Calls `_promote_trade_to_live` to transition trade status from 'V' to 'L'.

### 4. Strategy Execution Workflow (`common.py`)
- Strategies call `self._is_active(direction, mode)` in their main loop.
- **Criteria for Activation**:
  - Key construction: `{script_name}_{window_size}_{pip_buffer}_{tp_pips}_{sl_pips}_{direction.lower()}_{mode.lower()}`.
  - Entry must exist in `activations.json`.
  - `active` must be `true`.
  - The current `trade_product` (e.g., `GBPUSD`) must be present in the `products` list of the activation entry.

### 5. Selection Criteria/States
- **OFF**: No matching entry in `activations.json` or `active: false`.
- **A (Auto)**: Entry exists and `manual: false`.
- **M (Manual)**: Entry exists and `manual: true`.

## Plan
- [x] 1. Trace `toggleAutoActivation` function in `strategy_performance.html` to understand payload generation.
  - Test: Verify the exact JSON payload sent to `/api/grid_live`.
  - Evidence: Findings documented in Section 1.
- [x] 2. Analyze the `POST /api/grid_live` implementation in `trade_viewer_api.py`.
  - Test: Confirm how `grid_live.json` is updated and how concurrency is handled via locks.
  - Evidence: Findings documented in Section 2.
- [x] 3. Analyze the `GET /api/activations` implementation and the transformation logic from `grid_live.json`.
  - Test: Verify how the "A" (Auto) vs "M" (Manual) labels are derived in the UI from this API response.
  - Evidence: Confirmed bug in `trade_viewer_api.py:2465` where `manual` is hardcoded to `False`.
- [x] 4. Investigate the `/api/promote_trades` endpoint triggered upon activation.
  - Test: Confirm the SQL or logic used to change trade status from 'V' (Virtual) to 'L' (Live).
  - Evidence: Findings documented in Section 3.
- [x] 5. Trace the activation check logic in `common.py` (e.g., `_load_activations` and its usage in `_get_activation_details`).
  - Test: Verify how the system matches the strategy key, parameters, and product against the activation file.
  - Evidence: Findings documented in Section 4.
- [x] 6. Document the final workflow and criteria for "Auto" vs "Manual" vs "OFF" states clearly.
  - Test: Create a sequence diagram or clear step-by-step documentation in the task results.
  - Evidence: Documented in Sections 1-5.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: manual_verification
  - Artifact: Investigation results documented within this task file.
  - Objective-Proved: End-to-end workflow and criteria fully mapped.
  - Status: captured

## Implementation Log
- 2026-04-07 12:30: Task initialized in backlog.
- 2026-04-07 12:35: Moved to in-progress. Starting investigation of `strategy_performance.html` UI events.
- 2026-04-07 13:05: Completed tracing of UI, API, and Strategy logic. Identified `manual` flag hardcoding bug in `/api/activations`.

## Changes Made
- None (Investigation only)

## Validation
- Traced code paths in `strategy_performance.html`, `trade_viewer_api.py`, and `common.py`.

## Risks/Notes
- **Bug Identified**: `trade_viewer_api.py` line 2465 hardcodes `manual: False`, preventing the UI from correctly showing 'M' for manual activations.
- **Sync Note**: `activations.json` is the actual source of truth for the trade engine, while `grid_live.json` is the source of truth for the UI and management APIs.

## Completion Status
**COMPLETE**
2026-04-07 13:10
