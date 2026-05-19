---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_003000_ep012_freq_explorer_immutable_signal_cache]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Investigate: Rank-1 Selection Bug + Snapshot Leaders at Point-of-Evaluation

**Source:** User observed switch signal fired to EURAUD_C/breakout_2_tp10.0_sl20.0 at 03:25
when the displayed rank-1 was clearly EURAUD_C/breakout_2_tp20.0_sl20.0 (net=180, count=29).
Data confirmed stable at 03:30 (same rank-1, count incremented to 30).

**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

---

## Observed Behaviour
```
03:25 AM
Displayed rank-1: EURAUD_C / breakout_2_tp20.0_sl20.0   count=29  net=+180
Switch signal:  → EURAUD_C / breakout_2_tp10.0_sl20.0   Net +$150 · Count +21

03:30 AM
Displayed rank-1: EURAUD_C / breakout_2_tp20.0_sl20.0   count=30  net=+180  (consistent)
```

Switch fired to a strategy that is NOT the visual rank-1. Data is NOT mutating.

---

## Hypothesis: rank field is product-level, not strategy-level

In `_frequency.json`, `rank=1` may be assigned to ALL strategies within the top-performing
product (i.e., all EURAUD_C strategies get `rank=1`). The visual display re-sorts by net/count
to show tp20.0_sl20.0 first. But the switch rule code does:

```javascript
const r1candidates = positiveLeaders.filter(l => l.rank === 1);
const newLeader = r1candidates[0];  // ← picks first in raw array, NOT best by net/count
```

`r1candidates` may contain ALL EURAUD_C strategies. `r1candidates[0]` picks whichever
appears first in the raw data array (e.g. sorted by sl value alphabetically), which could be
tp10.0_sl20.0 even though tp20.0_sl20.0 has higher net and count.

---

## Investigation Steps

### 1. Confirm rank field assignment in _frequency.json
- Read a sample `_frequency.json` snapshot file
- Check: does `rank=1` appear on ONE strategy or ALL strategies within the top product?
- File location: `TradeApps/breakout/fs/json/live/{product_type}/{date}/_frequency.json`

### 2. Log r1candidates at point-of-evaluation
Add temporary console logging inside `evaluateSwitchSignals` before the cache write:
```javascript
if (r1candidates.length > 1) {
    console.warn('[SwitchRule] Multiple rank-1 candidates:', r1candidates.map(l => `${l.product}/${l.strategy} net=${l.net}`));
}
```
This confirms whether multiple strategies share rank=1.

### 3. Snapshot leaders data at point-of-evaluation
When writing a new signal to `_sigCache`, also snapshot the full `snap.leaders` array
so future debugging can show exactly what data drove the decision:

```javascript
_sigCache[snapKey] = {
    type: 'switch',
    from: ..., to: ...,
    // Snapshot for audit/debug — what the data looked like when signal was decided
    _snapshot: {
        leaders: snap.leaders.map(l => ({ rank: l.rank, product: l.product, strategy: l.strategy, net: l.net })),
        rank1Counts: Object.fromEntries(Object.entries(snapCounts).filter(([k]) => snapCounts[k] > 0))
    }
};
```

### 4. Fix r1candidates selection
If hypothesis confirmed (multiple rank=1), fix by sorting candidates before selecting:
```javascript
r1candidates.sort((a, b) => b.net - a.net); // highest net = true rank-1
const newLeader = r1candidates[0];
```

---

## User's Correct Interpretation of Threshold Logic
For switch to fire with held net=N and count=C, new strategy must satisfy:
- `net > N + 100`  (net threshold)
- `count > C + 20`  (count threshold, AND mode)

If held = tp20.0_sl20.0 (net=180, count=29):
- New strategy needs net > 280 AND count > 49
- tp10.0_sl20.0 showing Net +$150 and Count +21 implies net=330 and count=50
- tp10.0_sl20.0 with net=330 should outrank tp20.0_sl20.0 (net=180) — contradiction

This confirms the bug: the held at 03:25 was NOT tp20.0_sl20.0, OR the rank-1 selection
is picking the wrong strategy.

---

## Files to Read
| File | Purpose |
|---|---|
| `TradeApps/breakout/fs/json/live/{type}/{date}/_frequency.json` | Confirm rank field values |
| `TradeApps/breakout/fs/frequency_explorer.html` `evaluateSwitchSignals()` | Fix r1candidates sort |

## Investigation Results — 2026-04-20

### 1. rank=1 IS unique (hypothesis DISPROVED)
Checked `_frequency.json` at 03:25 snap:
```
rank=1 score_rank=1  EURAUD_C  breakout_2_tp20.0_sl20.0  net=180  score=812
rank=2 score_rank=2  EURAUD_C  breakout_2_tp20.0_sl3.0   net=180  score=812
rank=3 score_rank=3  EURAUD_C  breakout_2_tp20.0_sl30.0  net=180  score=812
rank=4 score_rank=4  EURAUD_C  breakout_2_tp20.0_sl5.0   net=180  score=812
rank=5 score_rank=5  EURAUD_C  breakout_2_tp20.0_sl50.0  net=180  score=812
```
Each rank is globally unique. Scores tie, but backend assigns sequential ranks.
`r1candidates` will always have exactly 0 or 1 element — `r1candidates[0]` bug does NOT exist.

### 2. Actual root cause of the 03:25 switch to tp10.0_sl20.0
`_frequency.json` historical snapshots are **retroactively updated** as trades close.
`tp10.0_sl20.0` was rank=1 at 00:20 and 00:25 (net=80). When the user first viewed
the page (before immutable cache), the 01:00 snap may have still shown `tp10.0_sl20.0`
as rank=1 with the highest rank1_count_cum (count=2 vs 0 for others at that time),
causing the opening trade to select it. As the file mutated, 01:00 now shows `tp5.0_sl20.0`.

The **immutable signal cache** (task 20260420_003000) is the correct and sufficient fix.
Once a snap's signal is decided, it never changes regardless of data mutation.

### 3. Changes Applied
**`frequency_explorer.html` — `evaluateSwitchSignals()`:**

a) **Defensive sort on r1candidates** (no-op with current data, future-proof):
```javascript
const r1candidates = positiveLeaders.filter(l => l.rank === 1)
    .sort((a, b) => b.net - a.net);
```

b) **Leaders snapshot added to `_sigCache` entries** (both `open` and `switch` types):
```javascript
_snapshot: {
    leaders: snap.leaders.map(l => ({ rank, product, strategy, net })),
    rank1Counts: Object.fromEntries(Object.entries(snapCounts).filter(([, v]) => v > 0))
}
```
When a future signal fires unexpectedly, inspect `localStorage` key `sigCache_*`
and read `_snapshot.leaders` + `_snapshot.rank1Counts` to see exactly what data
drove the decision at that snap.

## Completion Status
COMPLETE -- 2026-04-20
