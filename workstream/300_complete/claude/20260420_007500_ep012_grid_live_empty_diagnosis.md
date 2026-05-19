---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_007000_ep012_freq_explorer_grid_live_backfill]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Investigate: grid_live Still Empty After Backfill Implementation

**Source:** User reported grid_live.json still empty after auto-sync and manual sync were implemented.

## Most Likely Cause
`trade_viewer_api.py` has NOT been restarted since the `/api/switch_rule/activate` endpoint
was added. Every call to `sendSwitchToGrid` is hitting 404 silently — the endpoint does not
exist in the running process.

**Action required: restart `trade_viewer_api.py`**

## Diagnostic Logging Added
Enhanced `autoSyncToGrid()` with explicit console logging so the exact failure point is visible
in browser DevTools → Console:

```
[SwitchRule:autoSync] skipped — no heldStrategyData
   → heldStrategyData is null; evaluateSwitchSignals hasn't set it yet

[SwitchRule:autoSync] GET grid_live failed 404
   → trade_viewer_api.py not restarted OR wrong server port

[SwitchRule:autoSync] grid_live entries=0 hasSwitchRule=false held=EURAUD_C/breakout_2_...
   → grid_live is empty, about to backfill

[SwitchRule:autoSync] backfilling grid_live...
   → sendSwitchToGrid called — check Network tab for POST /api/switch_rule/activate result
```

## Verification Steps
1. Restart `trade_viewer_api.py`
2. Reload `frequency_explorer.html`
3. Open browser DevTools → Console
4. Look for `[SwitchRule:autoSync]` lines
5. Check `grid_live.json` — should contain switch_rule entry after backfill log appears

## Completion Status
COMPLETE -- 2026-04-20
