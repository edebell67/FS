# Trade Promotion on Activation Plan
**Date**: 2026-01-27 16:05  
**Version**: V20260127_1610  
**Description**: Add immediate trade promotion when activations are toggled via UI

## Objective
When a user clicks Auto Buy/Sell buttons in `strategy_performance.html`, immediately promote any existing open trades for that strategy/product/direction combination to L-trades (live trades).

## Current Behavior
- Clicking Auto Buy/Sell only updates `activations.json`
- No immediate action on existing open trades
- Trades only become live when strategy next runs and checks activations

## Desired Behavior
- Clicking Auto Buy/Sell updates `activations.json` AND
- Scans for existing open trades matching the activated strategy/product/direction
- Promotes those trades to L-trades by:
  - Setting `order_sent_net=true` (or `order_sent_alt=true`)
  - Creating tradeable JSON order files
  - Updating the open trade JSON with live flags

## Implementation Plan

### 1. Backend: Add Promotion Endpoint
**File**: `TradeApps/breakout/fs/trade_viewer_api.py`

Add new endpoint `/api/promote_trades` that:
- Accepts: `mode`, `strategy`, `product`, `direction`, `parm`
- Scans: `json/{mode}/{date}/` for open trade files
- Matches: Trades with matching strategy, product, direction
- Promotes: Updates JSON and creates tradeable orders

### 2. Frontend: Call Promotion After Activation
**File**: `TradeApps/breakout/fs/strategy_performance.html`

In `toggleAutoActivation()` function:
- After successful activation update
- Call `/api/promote_trades` with same parameters
- Log results to console

### 3. Version Update
**File**: `TradeApps/breakout/fs/constants.py`
- Update to `V20260127_1610`

## Detailed Changes

### Change 1: Add `/api/promote_trades` endpoint
**File**: `trade_viewer_api.py`
**Location**: After `update_activations()` function
**Action**: Add new route and handler

```python
@app.route("/api/promote_trades", methods=["POST"])
def promote_trades():
    """Promote existing open trades to L-trades when activation is toggled."""
    payload = request.json or {}
    mode = payload.get('mode', 'live').lower()
    strategy = payload.get('strategy', '')
    product = payload.get('product', '')
    direction = payload.get('direction', '')  # 'buy' or 'sell'
    parm = payload.get('parm', '')
    
    # Implementation details...
```

### Change 2: Call promotion from frontend
**File**: `strategy_performance.html`
**Location**: In `toggleAutoActivation()` after successful API response
**Action**: Add promotion call

```javascript
// After activation update succeeds
const promoteResponse = await fetch('/api/promote_trades', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        mode: mode,
        strategy: strategy,
        product: product,
        direction: direction,
        parm: parm
    })
});
```

### Change 3: Update version
**File**: `constants.py`
**Action**: Change version string

## Checklist
- [ ] Add `/api/promote_trades` endpoint in `trade_viewer_api.py`
- [ ] Implement trade file scanning logic
- [ ] Implement trade matching logic (strategy, product, direction, parm)
- [ ] Create tradeable JSON orders for matched trades
- [ ] Update open trade JSON files with live flags
- [ ] Add promotion call in `strategy_performance.html`
- [ ] Update version in `constants.py`
- [ ] Test with real activation toggle
- [ ] Verify L-trades are created immediately
- [ ] Verify trade JSONs are updated correctly

## Testing Steps
1. Ensure some open trades exist for a strategy/product
2. Click Auto Buy/Sell button in strategy_performance.html
3. Verify console shows promotion API call
4. Check that matching open trades now have `order_sent_net=true`
5. Verify tradeable JSON orders were created
6. Confirm trades appear as L-trades in UI

## Notes
- Only promote trades that match ALL criteria (strategy, product, direction, parm)
- Respect `bypass_criteria_check` config setting
- Log all promotions for debugging
- Handle errors gracefully (file not found, JSON parse errors, etc.)
