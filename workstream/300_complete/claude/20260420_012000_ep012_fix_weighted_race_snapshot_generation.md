---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on: [20260420_011000_ep012_freq_explorer_held_net_summary_fallback]
  feeds_into: []
  priority: urgent
---
**Epic:** adaptive_strategy_selection_engine

# Fix: weighted_race.py — Buggy 5-Minute Snapshot Generation

**Source:** Investigation of switch signal firing to wrong strategy revealed
`weighted_race.py` retroactively overwrites ALL historical snapshots every 5 seconds.

**File:** `TradeApps/breakout/fs/weighted_race.py`

---

## Bug 1 — CRITICAL: Full History Rewrite on Every Run (retroactive mutation)

`build_race()` re-reads ALL trade files and rebuilds every snapshot from scratch on each call.
`run_race()` calls `build_race()` and overwrites `_frequency.json` completely every loop.
The main loop runs every **5 seconds** (`time.sleep(5)`).

```python
# Every 5 seconds:
trades = load_trades(base_dir)          # ALL trade files
snapshots, summary = build_race(trades) # rebuilds EVERY snapshot from scratch
with dated_output.open('w') as f:
    json.dump(output, f)                # overwrites entire _frequency.json
```

**Impact:** When any trade closes (at any time of day), its net is added to `cumulative`
and ALL historical snapshots are recomputed retroactively. A snap at 01:00 may show
completely different leaders 6 hours later when new trades have closed. This is the
root cause of the switch signal bug (03:25 firing to wrong strategy).

**Fix Required:**
- Load existing `_frequency.json` if present
- Identify the timestamp of the last stored snapshot
- Only compute NEW buckets beyond that timestamp (incremental/append-only)
- Append new snapshots to the existing list — NEVER rewrite historical ones
- Summary/leaders section can still be recomputed as it is cumulative metadata

```python
# Pseudocode for fix
existing = load_existing_frequency(dated_output)
last_snap_time = existing['snapshots'][-1]['time'] if existing['snapshots'] else None
new_snapshots = build_race_incremental(trades, from_time=last_snap_time)
existing['snapshots'].extend(new_snapshots)
save(existing)
```

---

## Bug 2 — Top-5 Leaders Dominated by Same-Strategy Variants

`top = sorted(cumulative.items(), key=lambda kv: kv[1], reverse=True)[:5]`

`cumulative` key is `(product, strategy)`. Multiple `sl` variants of the same strategy
(e.g. `tp20.0_sl3.0`, `tp20.0_sl5.0`, `tp20.0_sl20.0`, `tp20.0_sl30.0`, `tp20.0_sl50.0`)
all share the same underlying trade, accumulating the same net independently.

Result: at 03:25, all 5 leaders are EURAUD_C/tp20.0_sl* with identical net=180.
The leaderboard shows no meaningful diversity — it's the same strategy 5 times.

**Fix Required — deduplicate by product+base_strategy before ranking:**
Extract the strategy base name (strip sl parameter) for grouping, keep only best-net
representative per `(product, base_strategy)` group in the top-5 display.

OR: Keep top-1 per product in the displayed leaders (showing the leading strategy
per product, up to 5 products).

---

## Bug 3 — Runs Every 5 Seconds (excessive compute + mutation rate)

`time.sleep(5)` causes full history rebuild 12× per minute. Combined with Bug 1,
this means historical snapshots mutate up to 12 times per minute.

**Fix Required:** Increase sleep to 60 seconds (aligns with reasonable refresh rate).
After Bug 1 is fixed (append-only), this becomes less critical but still advisable.

---

## Files to Modify
| File | Change |
|---|---|
| `weighted_race.py` — `build_race()` | Add `from_time` parameter, skip already-stored buckets |
| `weighted_race.py` — `run_race()` | Load existing JSON, append-only write |
| `weighted_race.py` — `build_race()` | Deduplicate leaders by product+base_strategy |
| `weighted_race.py` — `main()` | Increase sleep to 60s |

## Changes Applied — 2026-04-20

### Bug 1 — Sealed snapshot merge in `run_race()`
Snapshots older than `SEAL_MINUTES=10` are loaded from the existing file and kept unchanged.
Only recent/new buckets are appended. Atomic write via `.tmp` rename.

### Bug 2 — `_best_per_product()` helper in `build_race()`
`top = _best_per_product(cumulative)` — returns one best-net strategy per product, max 5.
Eliminates all-sl-variant dominated leaderboards.

### Bug 3 — Sleep increased to 60s

## Completion Status
COMPLETE -- 2026-04-20
