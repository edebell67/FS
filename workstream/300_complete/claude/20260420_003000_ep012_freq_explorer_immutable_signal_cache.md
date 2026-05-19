---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_002000_ep012_freq_explorer_opening_trade_01h]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Frequency Explorer — Immutable Signal Cache (Fix Retroactive Signal Changes)

**Source:** Bug report — switch signals and opening trade selection were changing retroactively as new snapshot data arrived, causing the strategy shown in historical timeline cards to flip between sessions.

**Root Cause:** `evaluateSwitchSignals()` re-ran from scratch on every `renderTimeline()` call. As new snapshots arrived, the entire evaluation sequence was re-computed, potentially producing different results for historical snaps (e.g., if cumulative counts or net values changed due to fresh data).

**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

## Problem Detail
- At 01:00 the opening trade was showing GBPAUD_C
- After new data arrived (01:20), the 01:00 card retroactively changed to show EURAUD_C
- Past signals must be immutable: once decided, they must never change

## Fix: localStorage Signal Cache

### New State Variables (near Switch Rule State block)
- `_sigCache` — in-memory object: `{ [snapTime]: signal|null }`
- `_sigCacheKey` — current cache key in localStorage
- `_getRuleFingerprint()` — returns `{mode}_{netThreshold}_{gapThreshold}` string
- `_getSigCacheKey(sessionDate)` — `sigCache_{date}_{fingerprint}`
- `_loadSigCache(sessionDate)` — loads from localStorage, no-op if already loaded for same key
- `_persistSigCache()` — writes `_sigCache` to localStorage
- `_clearSigCache(sessionDate)` — removes old cache, resets in-memory, resets `lastFiredSignalKey`

### Modified `updateSwitchRule()`
- Calls `_clearSigCache(sessionDate)` before re-rendering
- Ensures that when the user changes mode/thresholds, all signals are re-evaluated under new settings

### Modified `evaluateSwitchSignals(rank1AtSnap)`
Two paths per snapshot:

**Cache HIT** (`snapKey in _sigCache`):
- `null` cached → no signal; update held's live net/count from current data
- Signal cached → reconstruct with live net/count but **locked-in product/strategy identity**
- `currentHeld` is updated from cache; function never re-decides which strategy to hold

**Cache MISS** (new snap, not yet seen):
- Runs existing logic: opening trade selection or switch rule evaluation
- Result (signal or null) written to `_sigCache[snapKey]` and persisted to localStorage
- First write is final — subsequent renders always use the cached value

### Cache Key Design
- Keyed by `sessionDate` (date of first snapshot) + rule fingerprint
- Changing the date selector → different sessionDate → fresh cache
- Changing mode/thresholds → different fingerprint → `_clearSigCache()` called → fresh evaluation

## Behaviour After Fix
- 01:00 opening trade selection: locked in on first evaluation; never recalculated
- Switch signals: once fired at a given snap time, the FROM/TO identity is permanent
- Live net/count values in signal display still update (purely cosmetic, no logic impact)
- Rule changes: cache cleared; full re-evaluation from 01:00 with new settings

## Key Code — Cache Helpers (added near Switch Rule State block)

```javascript
let _sigCache = null;
let _sigCacheKey = '';

function _getRuleFingerprint() {
    return `${switchRuleMode}_${switchNetThreshold}_${switchGapThreshold}`;
}
function _getSigCacheKey(sessionDate) {
    return `sigCache_${sessionDate}_${_getRuleFingerprint()}`;
}
function _loadSigCache(sessionDate) {
    const key = _getSigCacheKey(sessionDate);
    if (_sigCacheKey === key && _sigCache !== null) return;
    _sigCacheKey = key;
    try { _sigCache = JSON.parse(localStorage.getItem(key) || '{}'); }
    catch(e) { _sigCache = {}; }
}
function _persistSigCache() {
    if (_sigCacheKey) localStorage.setItem(_sigCacheKey, JSON.stringify(_sigCache));
}
function _clearSigCache(sessionDate) {
    if (_sigCacheKey) localStorage.removeItem(_sigCacheKey);
    _sigCache = {};
    _sigCacheKey = _getSigCacheKey(sessionDate || '');
    lastFiredSignalKey = null;
}
```

## Key Code — Cache-Aware evaluateSwitchSignals (inner loop pattern)

```javascript
// Load cache at start of function
const sessionDate = new Date(snapshots[0].time).toLocaleDateString('en-CA');
_loadSigCache(sessionDate);

for (const snap of snapshots) {
    const snapKey = snap.time; // unique per snap

    // CACHE HIT — never recompute
    if (snapKey in _sigCache) {
        const cached = _sigCache[snapKey];
        if (cached !== null) {
            // Rebuild signal with live net/count but locked-in product/strategy
            const toLive = snap.leaders?.find(l => l.product === cached.to.product && l.strategy === cached.to.strategy);
            const signal = { ...cached,
                to: { ...cached.to, net: toLive ? toLive.net : cached.to.net,
                      count: snapCounts[`${cached.to.product}|${cached.to.strategy}`] || cached.to.count }
            };
            signalAtSnap.set(snap, signal);
            currentHeld = { product: cached.to.product, strategy: cached.to.strategy, ... };
        }
        continue; // skip all re-evaluation
    }

    // CACHE MISS — compute, then write once (immutable)
    // ... evaluation logic ...
    _sigCache[snapKey] = fires ? signal : null;
    _persistSigCache();
}
```

## Key Code — Cache clear on rule change (updateSwitchRule)

```javascript
function updateSwitchRule() {
    // ... update switchRuleMode / thresholds / localStorage ...
    const sessionDate = snapshots?.length > 0
        ? new Date(snapshots[0].time).toLocaleDateString('en-CA') : '';
    _clearSigCache(sessionDate); // invalidate — re-eval under new settings
    renderTimeline();
}
```

## Completion Status
COMPLETE -- 2026-04-20
