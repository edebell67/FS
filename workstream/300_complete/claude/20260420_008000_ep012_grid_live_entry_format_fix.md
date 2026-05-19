---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_006000_ep012_fix_switch_signal_to_grid_live_pipeline]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Fix: grid_live Entry Missing Required Fields (metric, group, activated_at)

**Source:** User identified entry format mismatch against existing grid_live_history records.

**Destination:** `TradeApps/breakout/fs/trade_viewer_api.py` — `freq_switch_rule_activate()`

## Required Format (from grid_live_history reference)
```json
{
    "model": "breakout_R_2_tp5.0_sl50.0",
    "product": "GBPNZD_C",
    "metric": "net",
    "group": "AUTO_TB_0417_172157_971_GBPNZD_C_breakout_R_2_tp5_0_sl50_0",
    "source": "TB_AUTO_TB_0417_...",
    "activated_at": "2026-04-17T23:59:54"
}
```

## What Was Missing
| Field | Before | After |
|---|---|---|
| `metric` | ❌ absent | `"net"` (hardcoded) |
| `group` | ❌ absent | `"freq_{product}_{strategy}"` (dots→underscores) |
| `activated_at` | ❌ absent | ISO timestamp at activation time |

`source` remains `"freq_switch_rule"` — used internally to identify and remove previous entry on switch.

## Fix Applied in `freq_switch_rule_activate()`
```python
safe_strategy = strategy.replace('.', '_')
group = f"freq_{product}_{safe_strategy}"
entry = {
    'model': strategy,
    'product': product,
    'metric': 'net',
    'group': group,
    'source': 'freq_switch_rule',
    'activated_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
}
```

## Example Output
```json
{
    "model": "breakout_2_tp5.0_sl20.0",
    "product": "EURAUD_C",
    "metric": "net",
    "group": "freq_EURAUD_C_breakout_2_tp5_0_sl20_0",
    "source": "freq_switch_rule",
    "activated_at": "2026-04-20T01:00:00"
}
```

## Note
`source` is kept as `"freq_switch_rule"` (not prefixed like `TB_`) so that the removal logic
`[m for m in target if m.get('source') != 'freq_switch_rule']` continues to work correctly.

## Completion Status
COMPLETE -- 2026-04-20
