---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on: [20260420_003000_ep012_freq_explorer_immutable_signal_cache]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Investigate: Switch Signal Not Propagating to Grid or Activations Explorer

**Source:** User observation — switch signal fired correctly in timeline (⚡ SWITCH SIGNAL → EURAUD_C / breakout_2_tp5.0_sl20.0 / Net +$90 · Count +7) but:
1. Grid (`grid_live`) does not contain the product/strategy after signal fires
2. `fs/activations_explorer.html` shows no activation details

## Observed State
```
01:00 AM snapshot
Rank-1: EURAUD_C / breakout_2_tp5.0_sl20.0  net=+90  count=7
⚡ SWITCH SIGNAL fired → EURAUD_C / breakout_2_tp5.0_sl20.0
Expected: entry appears in grid_live + activation visible in activations_explorer
Actual:   grid empty / activations_explorer shows nothing
```

## Areas to Investigate

### 1. `sendSwitchToGrid()` in frequency_explorer.html
- Does the POST to `/api/grid_live/toggle` actually execute?
- Check `switchActionPref` — is it set to `'grid'`? If set to `'notify'` or `'none'`, the grid call is skipped
- Opening trade fires `sendSwitchToGrid()` unconditionally — verify this path runs
- Check browser console for network errors on the POST
- Endpoint: `POST /api/grid_live/toggle` with `{ product, strategy, action: 'add', source: 'switch_rule' }`

### 2. `/api/grid_live/toggle` endpoint (api_server_sql/main.py or trade_viewer_api.py)
- Does the endpoint exist and accept the payload?
- Does it write to the grid state (DB or in-memory)?
- Does it create the tradeable JSON file in `trades_rt3/orders/`?
- Check what `action: 'add'` does vs what the endpoint expects

### 3. Grid Live data flow
- Where does grid_live state live? (DB table? In-memory dict? JSON file?)
- After POST, is the grid_live state queryable by other pages?
- Does `fs/activations_explorer.html` read from the same grid_live source?

### 4. `fs/activations_explorer.html` data source
- What API endpoint does it poll for activation data?
- Is it expecting a specific product type filter that doesn't match EURAUD_C?
- Does it need a page reload / manual trigger to refresh?
- Is there a product_type or date filter that excludes the newly added strategy?

### 5. `fireSwitchAction()` signal type handling
- Opening trade (`type: 'open'`) always calls `sendSwitchToGrid()` — confirm
- Switch signal (`type: 'switch'`) only calls grid if `switchActionPref === 'grid'` — confirm user has this set
- The signal shown is a SWITCH signal (⚡), not an OPEN signal (🟢) — check action preference

## Files to Read
- `TradeApps/breakout/fs/frequency_explorer.html` — `fireSwitchAction()`, `sendSwitchToGrid()`
- `TradeApps/breakout/fs/activations_explorer.html` — data source, API calls, filters
- `api_server_sql/main.py` or `TradeApps/breakout/fs/trade_viewer_api.py` — `/api/grid_live/toggle` handler
- `TradeApps/breakout/fs/grid_live_monitor.py` — order file creation logic

## Expected Outcome
- Identify the break in the signal → grid → activation chain
- Determine if it's a config issue (action pref), API issue, or data flow issue
- Fix or document required config for end-to-end flow to work

## Completion Status
OPEN
