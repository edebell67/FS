---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_010000_ep012_investigate_rank1_selection_and_snapshot_leaders]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Fix: Held Strategy Net Goes Stale When Not in Top-5 Leaders

**Source:** User observed false switch at 14:10 — GBPNZD_C/tp10.0_sl50.0 (net=320) appeared
to beat EURAUD_C/tp5.0_sl20.0 by +230. Actual held net was 240 (not 90), so true gap = +80.
Switch should NOT have fired (320 < 240+100=340).

**Root Cause:**
`_frequency.json` only stores the top-5 leaders per 5-minute snap. Once the held strategy
drops out of the top 5, `held_live = null` in `evaluateSwitchSignals`, and the code falls
back to `currentHeld.net` which was last set at the opening trade snap (net=90).

For today's session:
- Opening trade: `EURAUD_C / breakout_2_tp5.0_sl20.0` at 01:00 — net=90
- Strategy dropped out of top-5 at 01:05 and never returned
- Actual net climbed to 240 by 06:43 (visible in `_summary_net.json`)
- Switch check at 14:10 used stale 90 → 320 > 190 → FALSE switch

**Fix Applied — `frequency_explorer.html`:**

### 1. Load `_summary_net.json` alongside `_frequency.json` in `fetchData()`
```javascript
try {
    const summaryPath = freqPath.replace(source.file, `_summary_net.json`);
    const summaryResp = await fetch(summaryPath);
    if (summaryResp.ok) summaryNetData = await summaryResp.json();
} catch(e) { summaryNetData = null; }
```

### 2. Helper function `_getSummaryNetAt(strategy, product, snapTime)`
Looks up the last `_summary_net.json` entry where `t <= snapTime`:
```javascript
function _getSummaryNetAt(strategy, product, snapTime) {
    if (!summaryNetData || !summaryNetData.strategies) return null;
    const entries = (summaryNetData.strategies[strategy] || {})[product];
    if (!entries || !entries.length) return null;
    let net = null;
    for (const e of entries) {
        if (e.t <= snapTime) net = e.net;
        else break;
    }
    return net;
}
```

### 3. Updated `heldCurrentNet` in `evaluateSwitchSignals`
```javascript
const heldCurrentNet = heldLive ? heldLive.net
    : (_getSummaryNetAt(currentHeld.strategy, currentHeld.product, snap.time) ?? currentHeld.net);
```
Priority: (1) top-5 leaders (most current), (2) `_summary_net.json` (event-based updates),
(3) last known net (ultimate fallback).

## Result
With corrected held net:
- At 14:10: held net = 240 (from `_summary_net.json` entry at 06:43)
- netCond = 320 > 240+100=340 → **FALSE**
- No switch fires today (AND mode, net+100, gap+20)

## Completion Status
COMPLETE -- 2026-04-20
