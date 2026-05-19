# Task: Sync Weekly Performance Live Toggle to grid_live

Source: User request on 2026-04-11 after investigation of `GBPAUD_C | breakout_R_2_tp20.0_sl5.0` trades on `2026-04-10` not being marked live even though `fs/weekly_performance.html` indicated the strategy as live.

Task Type: implementation

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: true

## Task Summary
Update the weekly performance live-toggle workflow so enabling a product/strategy from `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html` writes not only to `activations.json` but also creates the corresponding runtime-monitoring entry in `grid_live.json`, and disabling it removes that weekly-owned grid entry.

## Problem Statement

Current behavior:
- `weekly_performance.html` toggles activation state through `/api/activations`
- runtime live-order generation can still block with `strategy not monitored in grid_live`
- this means weekly-triggered live intent does not reliably propagate into actual live routing

Observed evidence:
- `GBPAUD_C | breakout_R_2_tp20.0_sl5.0` trades on `2026-04-10` had:
- `is_live_trade: false`
- `order_sent_net: false`
- `trade_block_reason: ... strategy not monitored in grid_live`
- `grid_live.json` had no matching entry for that strategy/product

## Objective

Make the weekly performance live toggle a true execution trigger by ensuring weekly-on selections are represented in both:
- `activations.json`
- `grid_live.json`

## Requested Changes

- When `weekly_performance.html` toggles a strategy/product on:
- preserve the current activation write to `activations.json`
- add or update a `grid_live.json` entry for that exact strategy/product
- tag the grid entry source so it is identifiable as weekly-driven, for example `weekly_performance`

- When `weekly_performance.html` toggles a strategy/product off:
- preserve the current activation update
- remove only the weekly-owned `grid_live.json` entry for that strategy/product
- do not remove unrelated grid entries from other sources

- Ensure the sync is idempotent so repeated toggles do not duplicate grid entries.
- Ensure the runtime sees weekly-driven grid entries as valid monitoring entries for live routing.

## Acceptance Criteria

- Enabling a weekly performance row creates the expected `activations.json` state and a matching `grid_live.json` entry.
- Disabling that row removes the weekly-owned `grid_live.json` entry without disturbing other sources.
- Repeated enable actions do not create duplicates in `grid_live.json`.
- A newly opened qualifying trade for a weekly-enabled strategy/product is no longer blocked solely for `strategy not monitored in grid_live`.
- Existing manual/grid workflows continue to function without regression.

## Validation

- Toggle on a known weekly strategy/product from `weekly_performance.html`.
- Verify both `activations.json` and `grid_live.json` reflect the enabled state.
- Trigger or simulate a qualifying new trade for that strategy/product.
- Confirm the resulting trade JSON is not blocked for missing `grid_live` monitoring.
- Toggle the strategy/product off and verify only the weekly-owned grid entry is removed.

## Notes

- Keep source attribution on `grid_live` entries so cleanup/removal can target only weekly-owned records.
- Prefer centralizing the sync logic on the API side rather than duplicating persistence rules in frontend JavaScript.

## 2026-04-11 04:28:16 Execution

Implemented in:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py`

Behavior added:
- Weekly performance toggle posts now include:
- `source: weekly_performance`
- `sync_grid_live: true`
- The activations API now syncs weekly-owned `grid_live.json` entries for the affected strategy/product pairs.
- Weekly toggle ON adds or updates a single `grid_live` entry:
- `source = weekly_performance`
- `group = weekly_performance`
- `metric = net`
- Weekly toggle OFF removes only matching weekly-owned `grid_live` entries.

Implementation details:
- Sync is centralized server-side in `trade_viewer_api.py`.
- The backend derives the runtime model name from the activation key so UI-style keys such as `breakout_breakout_R_2_tp20.0_sl5.0_buy_net` resolve to `breakout_R_2_tp20.0_sl5.0`.
- `grid_live` writes are idempotent and preserve unrelated entries from other sources.

## 2026-04-11 04:28:17 Validation

Command run:
- `python -m pytest TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`

Results:
- `2 passed`
- Added regression coverage proving:
- weekly activation creates a matching `grid_live` entry
- repeated activation does not require duplicate rows
- weekly deactivation removes only the weekly-owned `grid_live` entry

Remaining validation gap:
- I did not run a live end-to-end runtime trade to verify the full GBPAUD_C case in production state.
- The code path is in place and tested at the API persistence layer, but the runtime trade-generation confirmation remains a manual follow-up.
