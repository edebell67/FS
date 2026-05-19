---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: [20260420_000500_ep012_freq_explorer_switch_rule_modal]
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Frequency Explorer — Opening Trade at 01:00 Local Time

**Source:** User request — at 01:00 local time, automatically pick the opening strategy (highest rank1_count_cum among net>0) and fire Send to Grid
**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

## Changes Made

### `evaluateSwitchSignals(rank1AtSnap)`
- Added `openingTradePlaced` flag (false until first trade set)
- Added `hasPostOpenSnap` pre-check: determines if any snapshot in today's data reaches 01:00 local time
- **Before 01:00**: skips all snapshots if 01:00 data exists (waits for opening window)
- **Fallback**: if no snapshots reach 01:00 (all data is pre-01:00), treats first positive-net snap as opening
- **At first snap at/after 01:00**: sorts all net>0 leaders by rank1_count_cum descending (tiebreak: net), picks top one as opening trade
- Fires opening trade signal with `type: 'open'` into `signalAtSnap` map
- Sets `currentHeld` to opening strategy; switch rule monitoring continues from that point

### `fireSwitchAction(signal, snap)`
- Added `isOpen = signal.type === 'open'` branch
- Opening trade always fires (bypasses `switchActionPref === 'none'` check)
- Opening trade notification: "🟢 OPENING TRADE — {product}" with net + count
- Opening trade always calls `sendSwitchToGrid()` regardless of action preference

### Timeline card rendering
- Opening trade card: green border (`.opening-trade-card`) instead of yellow
- Opening trade banner: green colour scheme with "🟢 OPENING TRADE →" label
- Switch signals: unchanged yellow styling

### `renderTimeline()` firing logic
- Changed from "fire only if last snap has signal" to "fire most recent snap that has any signal"
- Ensures opening trade at 01:00 fires even if no switch has occurred since

### CSS added
- `.opening-trade-card` — green border `rgba(16,185,129,0.6)` and subtle green background

## Behaviour
- On each `renderTimeline()` call, opening trade fires once for the 01:00 snap (de-duped via `lastFiredSignalKey`)
- If session data loaded doesn't yet reach 01:00, opening fires from whatever positive-net leaders are available at start
- Opening trade always sends to grid (creates tradeable JSON in `trades_rt3/orders/`)
- Post-opening, switch rule continues as before (evaluating rank-1 changes vs held)

## Completion Status
COMPLETE -- 2026-04-20
