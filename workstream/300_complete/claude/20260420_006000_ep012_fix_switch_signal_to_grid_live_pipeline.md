---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
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

## Root Cause (Three compounding failures)

### 1 — Wrong server (404)
`frequency_explorer.html` was calling `/api/grid_live/toggle` (relative URL).
That endpoint exists only in `api_server_sql/main.py` (port 8001 — FastAPI).
The page is served by `trade_viewer_api.py` (Flask — different port).
Flask had no `/api/grid_live/toggle` route → **silent 404**.

### 2 — Payload schema mismatch (422)
Even if port 8001 had been reached, the payload was wrong:

| Sent by `frequency_explorer.html` | Expected by `GridLiveToggle` (api_server_sql) |
|---|---|
| `product: "EURAUD_C"` | ❌ not in schema |
| `strategy: "breakout_2..."` | ❌ not in schema |
| `action: 'add'` | `active: bool` |
| `source: 'switch_rule'` | `group: str` |
| — | `models: List[{model, product}]` ← missing entirely |

### 3 — Source gating would have blocked it anyway
`trade_viewer_api.py` `/api/grid_live` POST silently rejects sources not in its allowlist
(`rank_alert`, `frequency`, `ui`, `grid_live`, `breakout`). `switch_rule` is not listed.

---

## Fix

### New endpoint in `trade_viewer_api.py`

Added `/api/switch_rule/activate` (POST) immediately before `_sync_grid_to_activations`:

```python
@app.route('/api/switch_rule/activate', methods=['POST'])
def switch_rule_activate():
    """[V20260420] Activates a strategy in grid_live.json from the Frequency Explorer switch rule."""
    payload  = request.json or {}
    product  = str(payload.get('product', '')).strip()
    strategy = str(payload.get('strategy', '')).strip()
    mode     = str(payload.get('mode', 'live')).lower()

    if not product or not strategy:
        return jsonify({'success': False, 'message': 'product and strategy are required'}), 400

    grid_live_file = ROOT_PATH / "grid_live.json"
    entry = {'model': strategy, 'product': product, 'source': 'switch_rule'}

    with GRID_LIVE_LOCK:
        full_data = {'live': [], 'sim': []}
        if grid_live_file.exists():
            with open(grid_live_file, 'r') as f:
                full_data = json.load(f)
            if isinstance(full_data, list):
                full_data = {'live': full_data, 'sim': []}

        target = full_data.get(mode, [])
        existing_switch = [m for m in target if m.get('source') == 'switch_rule']
        if existing_switch:
            _archive_grid_live(mode)  # archive before replacing
        # Remove previous switch_rule entry — one active at a time
        target = [m for m in target if m.get('source') != 'switch_rule']
        target.append(entry)
        full_data[mode] = target

        with open(grid_live_file, 'w') as f:
            json.dump(full_data, f, indent=4)

    print(f"[SWITCH_RULE] Activated {product} / {strategy} in grid_live ({mode})")
    return jsonify({'success': True, 'product': product, 'strategy': strategy, 'mode': mode})
```

### Updated `sendSwitchToGrid()` in `frequency_explorer.html`

```javascript
// Before — wrong endpoint + wrong payload
async function sendSwitchToGrid(product, strategy) {
    await fetch('/api/grid_live/toggle', {   // ← 404 on Flask server
        method: 'POST',
        body: JSON.stringify({ product, strategy, action: 'add', source: 'switch_rule' }) // ← wrong schema
    });
}

// After — correct endpoint + correct payload
async function sendSwitchToGrid(product, strategy) {
    const resp = await fetch('/api/switch_rule/activate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product, strategy, mode: runMode || 'live' })
    });
    if (!resp.ok) console.warn('[SwitchRule] Activate failed', resp.status);
    else console.log('[SwitchRule] grid_live updated:', product, strategy);
}
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| New endpoint, not reuse of existing | Existing `/api/grid_live` POST has source-gating that would silently reject `switch_rule`; cleaner to have a dedicated route |
| One switch_rule entry at a time | Each activation replaces the previous — avoids stale entries accumulating |
| Archive before replace | `_archive_grid_live(mode)` called when a previous switch_rule entry exists — full snapshot written to `grid_live_history/grid_live_{mode}_{timestamp}.json` before overwrite |
| `source: 'switch_rule'` tag | Allows grid_live readers to identify and distinguish switch rule entries from Trade Bucket / Frequency entries |
| Uses `GRID_LIVE_LOCK` | Thread-safe alongside all other grid_live writers |
| `runMode` from frontend | Respects live/sim mode already tracked in the page |

---

## Expected Result After Fix
1. Opening trade fires at 01:00 → POST to `/api/switch_rule/activate`
2. `grid_live.json` contains: `{ "live": [{ "model": "breakout_2_tp5.0_sl20.0", "product": "EURAUD_C", "source": "switch_rule" }] }`
3. `activations_explorer.html` polls `/api/grid_live?mode=live` → shows EURAUD_C entry
4. Subsequent switch signal replaces previous switch_rule entry in grid_live

## Completion Status
COMPLETE -- 2026-04-20
