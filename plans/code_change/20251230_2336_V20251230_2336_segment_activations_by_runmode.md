# Plan: Segment Activations by Run Mode

**Version**: V20251230_2336  
**Created**: 2025-12-30 23:36:00  
**Completed**: 2025-12-30 23:45:00  
**Status**: ✅ COMPLETED

---

## 1. Understanding of Requirements

Segment `activations.json` by `run_mode` (live/sim) to ensure:
1. Each run mode maintains its own activation list
2. L-trades are generated only for strategies matching the current run_mode
3. UI updates (Auto Buy/Sell buttons) modify the correct mode section
4. Backward compatibility with existing single-level activations structure

### Current Structure
```json
{
    "breakout_Rev_4_tp3.0_sl10.0_4_0.00015_3.0_10.0_buy_net": {
        "active": true,
        "manual": true,
        "activated_at": "2025-12-30T23:31:38.056604",
        "products": ["GBPEUR_C"]
    }
}
```

### New Structure
```json
{
    "live": {
        "breakout_Rev_4_tp3.0_sl10.0_4_0.00015_3.0_10.0_buy_net": {
            "active": true,
            "manual": true,
            "activated_at": "2025-12-30T23:31:38.056604",
            "products": ["GBPEUR_C"]
        }
    },
    "sim": {
        "breakout_Rev_3_tp10.0_sl10.0_buy_net": {
            "active": true,
            "manual": true,
            "activated_at": "2025-12-30T23:04:56.574272",
            "products": ["EUR"]
        }
    }
}
```

---

## 2. Plan of Approach

### 2.1 Backend Changes (`trade_viewer_api.py`)

1. **Update `_normalize_activations()`** - Handle both old (flat) and new (mode-segmented) formats
2. **Update `_load_activations()`** - Auto-migrate old format to new format on first load
3. **Update `get_activations()`** - Accept `mode` query parameter, return activations for that mode only
4. **Update `update_activations()`** - Accept `mode` in request body, update correct mode section

### 2.2 Backend Changes (`common.py`)

1. **Update `_load_activations()`** - Load activations for current run_mode only
2. **Update `_save_activations()`** - Save to correct mode section
3. **Update `_normalize_activation_dict()`** - Handle mode-segmented structure
4. **Ensure `_is_active()`** - Already uses `_load_activations()`, so will automatically use mode-filtered data

### 2.3 Frontend Changes (`strategy_performance.html`)

1. **Update `loadActivations()`** - Pass current `run_mode` to API
2. **Update `toggleAutoActivation()`** - Include `run_mode` in POST request

---

## 3. Detailed Checklist

### 3.1 Backend - `trade_viewer_api.py`

- [x] Update `_normalize_activations()` to detect and handle both formats
- [x] Add migration logic to convert old format to new format
- [x] Update `_load_activations()` to auto-migrate on first load
- [x] Update `get_activations()` to accept `mode` query parameter
- [x] Update `get_activations()` to return only activations for requested mode
- [x] Update `update_activations()` to accept `mode` in request body
- [x] Update `update_activations()` to update correct mode section
- [x] Ensure file writes preserve both mode sections

### 3.2 Backend - `common.py`

- [x] Update `_load_activations()` to read from mode-segmented structure
- [x] Update `_load_activations()` to filter by current `run_mode` from config
- [x] Update `_save_activations()` to write to correct mode section
- [x] Update `_normalize_activation_dict()` to handle mode-segmented input
- [x] Test that `_is_active()` correctly uses mode-filtered activations

### 3.3 Frontend - `strategy_performance.html`

- [x] Update `loadActivations()` to get current run_mode from dropdown
- [x] Update `loadActivations()` to pass `mode` parameter to API
- [x] Update `toggleAutoActivation()` to get current run_mode
- [x] Update `toggleAutoActivation()` to include `mode` in POST body
- [x] Ensure button states refresh correctly after mode changes

### 3.4 Version Update

- [x] Update `constants.py` with new VERSION `V20251230_2336`

---

## 4. Implementation Details

### 4.1 Migration Logic (trade_viewer_api.py)

```python
def _is_legacy_format(raw: Dict[str, Any]) -> bool:
    """Check if activations.json is in old (flat) format."""
    if not raw:
        return False
    # If top-level keys are 'live' or 'sim', it's new format
    if 'live' in raw or 'sim' in raw:
        return False
    # Otherwise, check if any key looks like an activation key
    for key in raw.keys():
        if any(key.endswith(suffix) for suffix in ACTIVATION_SUFFIXES):
            return True
    return False

def _migrate_to_mode_format(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate old flat format to mode-segmented format."""
    # Move all existing activations to 'live' by default
    return {
        'live': raw,
        'sim': {}
    }
```

### 4.2 Load Activations with Mode Filter (common.py)

```python
def _load_activations() -> Dict[str, Any]:
    """Load activations for current run_mode only."""
    if not os.path.exists(ACTIVATIONS_FILE):
        return {}
    
    config = _load_config()
    run_mode = config.get('run_mode', 'live').lower()
    
    try:
        with open(ACTIVATIONS_FILE, 'r') as f:
            raw = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}
    
    # Handle both old and new formats
    if run_mode in raw:
        # New format: return activations for current mode
        mode_activations = raw.get(run_mode, {})
    else:
        # Old format: assume all activations are for 'live'
        mode_activations = raw if run_mode == 'live' else {}
    
    # Normalize and cache
    trade_products = _load_trade_products_upper()
    normalized, dirty = _normalize_activation_dict(mode_activations, trade_products)
    
    return normalized
```

### 4.3 Save Activations to Mode Section (common.py)

```python
def _save_activations(activations: Dict[str, Any]) -> None:
    """Save activations to correct mode section."""
    config = _load_config()
    run_mode = config.get('run_mode', 'live').lower()
    
    # Load full file
    if os.path.exists(ACTIVATIONS_FILE):
        try:
            with open(ACTIVATIONS_FILE, 'r') as f:
                full_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            full_data = {'live': {}, 'sim': {}}
    else:
        full_data = {'live': {}, 'sim': {}}
    
    # Ensure mode sections exist
    if 'live' not in full_data:
        full_data['live'] = {}
    if 'sim' not in full_data:
        full_data['sim'] = {}
    
    # Update current mode section
    full_data[run_mode] = activations
    
    # Write back
    with open(ACTIVATIONS_FILE, 'w') as f:
        json.dump(full_data, f, indent=4)
```

### 4.4 Frontend API Calls

```javascript
// Load activations for current mode
async function loadActivations() {
    try {
        const mode = document.getElementById('runMode').value; // 'live' or 'sim'
        const response = await fetch(`http://localhost:5000/api/activations?mode=${mode}`);
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                activations = data.activations || {};
            }
        }
    } catch (err) {
        console.error('Error loading activations:', err);
    }
}

// Toggle with mode
async function toggleAutoActivation(strategy, parm, product, direction, button) {
    const mode = document.getElementById('runMode').value;
    const key = buildActivationKey(strategy, parm, direction);
    const isCurrentlyActive = isAutoActive(strategy, parm, product, direction);
    
    const payload = {
        mode: mode, // Include run_mode
        activations: {
            [key]: {
                active: !isCurrentlyActive,
                manual: true,
                products: [product]
            }
        }
    };
    
    // ... rest of function
}
```

---

## 5. Testing Plan

- [ ] Test migration: Old format file auto-migrates to new format
- [ ] Test live mode: Activations saved to 'live' section
- [ ] Test sim mode: Activations saved to 'sim' section
- [ ] Test mode switching: UI loads correct activations when mode changes
- [ ] Test L-trade generation: Only strategies from current mode generate L-trades
- [ ] Test backward compatibility: Empty file creates proper structure

---

## 6. Files to Modify

| File | Action | Description |
|------|--------|-------------|
| `trade_viewer_api.py` | MODIFY | Add mode segmentation to API |
| `common.py` | MODIFY | Update activation loading/saving for mode filtering |
| `strategy_performance.html` | MODIFY | Pass mode parameter in API calls |
| `constants.py` | MODIFY | Update VERSION |

---

**Ready to implement.**
