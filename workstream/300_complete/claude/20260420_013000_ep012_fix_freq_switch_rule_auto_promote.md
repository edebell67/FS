---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_009000_ep012_investigate_activations_explorer_display_requirements]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Fix: freq_switch_rule Activations Not Triggering L-Trade Promotions

**Source:** User observed 4 valid EURAUD_C trades (01:01, 03:30, 05:26, 05:39) executing
after strategy reached Rank #1 with no corresponding l-trade promotions.

---

## Full Pipeline: How L-Trade Promotions Work for Breakout

```
frequency_explorer.html
    → evaluateSwitchSignals() selects opening/switch strategy
        → sendSwitchToGrid(product, strategy)
            → POST /api/switch_rule/activate
                → grid_live.json  [source: "freq_switch_rule"]
                    → _sync_grid_to_activations()
                        → activations.json  [active: true, auto_promote: ???]
                            → breakout.py _is_auto_promote_active()
                                → create l-trade order file
```

`grid_live_monitor.py` is NOT in this path for breakout — line 426 hard-disables
breakout open promotion: `# Strategies now control live activation for breakout trades. continue`

The only promotion path is: `activations.json` → `common.py` → `breakout.py`.

---

## Root Cause — Two Compounding Issues

### Issue 1: `_sync_grid_to_activations` always writes `auto_promote=False` for new entries

`_sync_grid_to_activations()` in `trade_viewer_api.py` inherits `auto_promote` from the
EXISTING activation entry for that key. For `freq_switch_rule` activations this entry
never exists beforehand → `existing.get('auto_promote', False)` = **False**.

```python
# Before fix — always False for new freq_switch_rule entries:
'auto_promote': bool(existing.get('auto_promote', False)),
```

Result in `activations.json`:
```json
"breakout_2_tp5.0_sl20.0_buy_net": {
    "active": true,
    "auto_promote": false,   ← ❌ blocks all promotions
    "source": "freq_switch_rule",
    "products": ["EURAUD_C"]
}
```

### Issue 2: `common.py` requires BOTH `active=True` AND `auto_promote=True`

`_is_auto_promote_active()` in `common.py`:
```python
if isinstance(entry, dict) and entry.get('active') and entry.get('auto_promote'):
    return self.trade_product.upper() in [p.upper() for p in activated_products]
return False  # ← always hit when auto_promote=False
```

With `auto_promote=False`, every call returns `False` → `_maybe_send()` skips the
auto-promote path entirely → no l-trade order files created → no broker submissions.

---

## Fix Applied — `trade_viewer_api.py` `_sync_grid_to_activations()`

```python
# [V20260420] freq_switch_rule entries are autonomous selections — always auto_promote
auto_promote_default = True if source == 'freq_switch_rule' else bool(existing.get('auto_promote', False))
active_definitions[key] = {
    'products': set(),
    'source': ...,
    'manual': ...,
    'auto_promote': auto_promote_default,   ← True for freq_switch_rule
    'activated_at': ...
}
```

`freq_switch_rule` = system autonomously selected the strategy. Auto-promote is the
entire purpose of the selection — no additional manual flag should be required.
All other sources (`ui`, `TB_*`) are unchanged and still respect existing toggle state.

Result in `activations.json` after fix:
```json
"breakout_2_tp5.0_sl20.0_buy_net": {
    "active": true,
    "auto_promote": true,    ← ✅ promotions will fire
    "source": "freq_switch_rule",
    "products": ["EURAUD_C"]
}
```

---

## Promotion Flow After Fix

1. `frequency_explorer.html` fires opening trade / switch → `sendSwitchToGrid()`
2. `POST /api/switch_rule/activate` → `grid_live.json` updated
3. `_sync_grid_to_activations()` writes `auto_promote=true` for `freq_switch_rule` source
4. `breakout.py` runs on next trade signal for `EURAUD_C / breakout_2_tp5.0_sl20.0`
5. `_is_auto_promote_active('buy', 'net')` → `True` → weekly net check passes → l-trade created

## Action Required
Restart `trade_viewer_api.py` then trigger a re-sync:
- Either reload `frequency_explorer.html` (triggers `autoSyncToGrid()`)
- Or click "Sync to Grid" in the Switch Rule modal

## Completion Status
COMPLETE -- 2026-04-20
