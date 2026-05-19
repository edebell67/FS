---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on: [20260420_004000_ep012_investigate_switch_signal_grid_and_activation]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Fix: Switch/Opening Signal Does Not Write to grid_live.json

**Source:** User observation — opening trade signal fired (EURAUD_C / breakout_2_tp5.0_sl20.0)
but `grid_live.json` remained empty and `activations_explorer.html` showed nothing.

**Destination:**
- `TradeApps/breakout/fs/frequency_explorer.html` — `sendSwitchToGrid()`
- `TradeApps/breakout/fs/trade_viewer_api.py` — new endpoint `/api/switch_rule/activate`

---

## Root Cause Analysis

### Problem 1 — Wrong endpoint called
`frequency_explorer.html` calls `/api/grid_live/toggle` (POST):
```javascript
body: JSON.stringify({ product, strategy, action: 'add', source: 'switch_rule' })
```

This endpoint lives in **`api_server_sql/main.py`** (port 8001), but `frequency_explorer.html`
is served by **`trade_viewer_api.py`** (Flask, different port). The relative URL `/api/grid_live/toggle`
resolves to `trade_viewer_api.py`, which has **no such route** → 404.

### Problem 2 — Payload schema mismatch
Even if the endpoint were reachable, the payload is wrong:

| Sent by `frequency_explorer.html` | Expected by `GridLiveToggle` (api_server_sql) |
|---|---|
| `product` | (not present) |
| `strategy` | (not present) |
| `action: 'add'` | `active: bool` |
| `source: 'switch_rule'` | `group: str` |
| — | `models: List[{model, product}]` |

### Problem 3 — Source gating in `trade_viewer_api.py` `/api/grid_live` POST
Even if correctly routed to the Flask endpoint, `source: 'switch_rule'` is not in the
allowlist that bypasses source-overrule checks. The endpoint would likely silently reject it.

---

## Resolution Plan

### Step 1 — Add new endpoint to `trade_viewer_api.py`

Add `/api/switch_rule/activate` (POST) that accepts the simple payload from `frequency_explorer.html`
and writes directly to `grid_live.json` via the existing `GRID_LIVE_LOCK` pattern:

```python
@app.route('/api/switch_rule/activate', methods=['POST'])
def switch_rule_activate():
    """Activates a strategy from the Frequency Explorer switch rule."""
    payload = request.json
    product  = payload.get('product')   # e.g. "EURAUD_C"
    strategy = payload.get('strategy')  # e.g. "breakout_2_tp5.0_sl20.0"
    mode     = payload.get('mode', 'live').lower()
    source   = 'switch_rule'

    if not product or not strategy:
        return jsonify({'success': False, 'message': 'product and strategy required'}), 400

    grid_live_file = ROOT_PATH / "grid_live.json"
    entry = { 'model': strategy, 'product': product, 'source': source }

    with GRID_LIVE_LOCK:
        full_data = {'live': [], 'sim': []}
        if grid_live_file.exists():
            try:
                with open(grid_live_file, 'r') as f:
                    full_data = json.load(f)
                if isinstance(full_data, list):
                    full_data = {'live': full_data, 'sim': []}
            except: pass

        target = full_data.get(mode, [])
        # Remove any existing switch_rule entries (one active at a time)
        target = [m for m in target if m.get('source') != 'switch_rule']
        target.append(entry)
        full_data[mode] = target

        with open(grid_live_file, 'w') as f:
            json.dump(full_data, f, indent=4)

    print(f"[SWITCH_RULE] Activated {product} / {strategy} in grid_live ({mode})")
    return jsonify({'success': True, 'product': product, 'strategy': strategy})
```

### Step 2 — Update `sendSwitchToGrid()` in `frequency_explorer.html`

Change the fetch target from `/api/grid_live/toggle` to `/api/switch_rule/activate`:

```javascript
async function sendSwitchToGrid(product, strategy) {
    try {
        const resp = await fetch('/api/switch_rule/activate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product, strategy, mode: runMode || 'live', source: 'switch_rule' })
        });
        if (!resp.ok) console.warn('[SwitchRule] Grid activate failed', resp.status);
        else console.log('[SwitchRule] Activated in grid_live:', product, strategy);
    } catch (e) {
        console.warn('[SwitchRule] Grid activate error', e);
    }
}
```

### Step 3 — Verify `activations_explorer.html` reads from `grid_live.json`
- Confirm it polls `/api/grid_live?mode=live`
- Confirm `trade_viewer_api.py` `/api/grid_live` GET returns the full `grid_live.json` contents
- After activation, activations_explorer should show the entry on next poll

### Step 4 — Validate end-to-end
1. Load `frequency_explorer.html` — wait for 01:00 snap
2. Opening trade fires → POST to `/api/switch_rule/activate`
3. Check `grid_live.json` — should contain `{ "live": [{ "model": "breakout_2_tp5.0_sl20.0", "product": "EURAUD_C", "source": "switch_rule" }] }`
4. Open `activations_explorer.html` — EURAUD_C entry should be visible

---

## Files to Change
| File | Change |
|------|--------|
| `TradeApps/breakout/fs/trade_viewer_api.py` | Add `/api/switch_rule/activate` endpoint |
| `TradeApps/breakout/fs/frequency_explorer.html` | Update `sendSwitchToGrid()` URL + payload |

## Completion Status
OPEN
