---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_008000_ep012_grid_live_entry_format_fix]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Investigate & Fix: activations_explorer.html Not Displaying freq_switch_rule Strategy

**Source:** User observation — grid_live.json has freq_switch_rule entry but activations_explorer shows nothing.

---

## Data Flow
```
grid_live.json
    → _sync_grid_to_activations()
        → activations.json
            → /api/activations GET
                → activations_explorer.html
```

## Root Cause

`_sync_grid_to_activations` is called by `_reconcile_active_buckets()` which has two hard exits:

```python
# Exit 1 — returns immediately if Trade Bucket is not the active automated source
if not _is_source_allowed('Trade Bucket'):
    return

# Exit 2 — returns if no live Trade Buckets exist
if not all_live_buckets:
    return
```

Neither condition is met when the switch_rule is the active source → `_sync_grid_to_activations`
was NEVER called → `activations.json` never updated → activations_explorer shows nothing.

## Fix — `switch_rule_activate()` in `trade_viewer_api.py`

Added direct call to `_sync_grid_to_activations` inside the GRID_LIVE_LOCK block, immediately
after writing grid_live.json — bypasses reconciler gating entirely:

```python
with open(grid_live_file, 'w') as f:
    json.dump(full_data, f, indent=4)

# Sync grid_live state directly to activations.json — bypasses reconciler gating
_sync_grid_to_activations(full_data.get(mode, []), mode=mode)
```

Passes the FULL mode list (not just the new entry) so activations.json reflects complete state.

## Expected activations.json After Fix
For `{ model: "breakout_2_tp5.0_sl20.0", product: "EURAUD_C", metric: "net" }`:
```json
{
  "breakout_2_tp5.0_sl20.0_buy_net":  { "products": ["EURAUD_C"], "source": "freq_switch_rule" },
  "breakout_2_tp5.0_sl20.0_sell_net": { "products": ["EURAUD_C"], "source": "freq_switch_rule" }
}
```
Both keys appear as cards in activations_explorer.html.

## Completion Status
COMPLETE -- 2026-04-20
