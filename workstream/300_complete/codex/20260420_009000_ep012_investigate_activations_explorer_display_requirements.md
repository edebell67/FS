---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on: [20260420_008000_ep012_grid_live_entry_format_fix]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Investigate: What Does activations_explorer.html Require to Display a Strategy?

**Source:** User observation — grid_live.json receives freq_switch_rule entry but
activations_explorer.html still shows nothing.

---

## What Is Already Known

### activations_explorer.html data source
- Reads from `/api/activations?mode={mode}` → returns contents of `activations.json`
- Does NOT read from `grid_live.json` directly
- Renders cards keyed by activation key (e.g. `breakout_2_tp5.0_sl20.0_buy_net`)
- Each card shows: key, products list, source, toggle controls

### activations.json is populated by `_sync_grid_to_activations(grid_data, mode)`
- Called from `_reconcile_active_buckets()` which is triggered on `GET /api/grid_live`
- Iterates grid_live entries, builds activation keys based on `metric` field:
  - `metric: 'net'`  → `{model}_buy_net` + `{model}_sell_net`
  - `metric: 'alt'`  → `{model}_buy_alt` + `{model}_sell_alt`
  - `metric: 'buy_net'` → `{model}_buy_net` only
  - etc.
- Each key gets `products: [product]`, `source`, `manual`, `activated_at`

### Expected activation keys for our entry
```json
{ "model": "breakout_2_tp5.0_sl20.0", "product": "EURAUD_C", "metric": "net", "source": "freq_switch_rule" }
```
Would produce in activations.json:
```json
{
  "breakout_2_tp5.0_sl20.0_buy_net":  { "products": ["EURAUD_C"], "source": "freq_switch_rule", ... },
  "breakout_2_tp5.0_sl20.0_sell_net": { "products": ["EURAUD_C"], "source": "freq_switch_rule", ... }
}
```

---

## What Needs Investigation

### 1. Is `_reconcile_active_buckets` actually calling `_sync_grid_to_activations` for `freq_switch_rule` entries?
- Check `_reconcile_active_buckets()` — does it filter by source?
- Does it skip entries whose source is not in an allowlist?
- Is there a source-gating check that blocks `freq_switch_rule`?

### 2. Is `GET /api/grid_live` being called after activation?
- `_reconcile_active_buckets` is triggered on `GET /api/grid_live`
- `frequency_explorer.html` calls `GET /api/grid_live` in `autoSyncToGrid` check
- But does it call it AFTER writing the entry? (timing issue — autoSync reads first, then writes)
- Does `activations_explorer.html` call `GET /api/grid_live` on load or refresh?

### 3. Does activations.json actually get updated?
- Check `activations.json` directly after grid_live is populated
- If activations.json is empty/missing the entry, sync is not firing

### 4. Does activations_explorer.html filter out `freq_switch_rule` source?
- Check filter controls in activations_explorer.html
- Is there a source dropdown that defaults to hiding automated entries?

---

## Files to Read
| File | What to Look For |
|---|---|
| `trade_viewer_api.py` `_reconcile_active_buckets()` | Source gating, what triggers sync to activations |
| `TradeApps/breakout/fs/activations.json` | Does it contain the entry after grid_live is populated? |
| `TradeApps/breakout/fs/activations_explorer.html` | Filter defaults, source display logic |

---

## Resolution Path (Hypothesis)
Most likely: `_reconcile_active_buckets` or `_sync_grid_to_activations` has a source check
that skips `freq_switch_rule` entries. Fix would be to add `freq_switch_rule` to the allowed
sources list, or call `_sync_grid_to_activations` explicitly from `switch_rule_activate()`
after writing to grid_live — bypassing the reconcile step entirely.

## Completion Status
OPEN
