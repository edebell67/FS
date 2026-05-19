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

# Frequency Explorer — Backfill grid_live When switch_rule Entry Missing

**Source:** User question — if grid_live.json has no entry at a given moment (e.g. server restart,
manual clear, or bug), how do we restore what it should contain?

**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

## Problem
`heldStrategyData` (tracked in-memory via the immutable signal cache) always knows the correct
active strategy. But if `grid_live.json` is empty or lacks a `switch_rule` entry, that knowledge
is stranded in the browser — activations_explorer and the trading system see nothing.

## Solution: Two-layer backfill

### 1. Auto-sync (passive, on every renderTimeline)
After signals are evaluated, `autoSyncToGrid()` checks `GET /api/grid_live?mode={runMode}`.
If the response contains no entry with `source: 'switch_rule'`, silently calls
`sendSwitchToGrid(heldStrategyData.product, heldStrategyData.strategy)` to restore the entry.

```javascript
async function autoSyncToGrid() {
    if (!heldStrategyData) return;
    const resp = await fetch(`/api/grid_live?mode=${runMode || 'live'}`);
    const json = await resp.json();
    const hasSwitchRule = (json.data || []).some(m => m.source === 'switch_rule');
    if (!hasSwitchRule) {
        await sendSwitchToGrid(heldStrategyData.product, heldStrategyData.strategy);
    }
}
```

Called at end of `renderTimeline()` after `fireSwitchAction`.

### 2. Manual sync (explicit, via Switch Rule modal)
"Sync to Grid" button added to the Switch Rule modal (⚡), above the rule controls.
Green-styled, shows inline status after sync.

```javascript
async function manualSyncToGrid() {
    if (!heldStrategyData) { status.textContent = 'No held strategy — load data first'; return; }
    btn.disabled = true;
    status.textContent = 'Syncing…';
    await sendSwitchToGrid(heldStrategyData.product, heldStrategyData.strategy);
    status.textContent = `✓ Synced: ${heldStrategyData.product} / ${strategy}…`;
    // clears after 5 seconds
}
```

## Changes Made

### `frequency_explorer.html` — HTML (Switch Rule modal)
- Added "Sync to Grid" button (`id="syncToGridBtn"`) below held-display
- Added status span (`id="syncToGridStatus"`) for inline feedback

### `frequency_explorer.html` — JS
- `autoSyncToGrid()` — checks grid_live, backfills if switch_rule entry absent
- `manualSyncToGrid()` — explicit sync with button state + status feedback
- `renderTimeline()` — calls `autoSyncToGrid()` after signal firing

## Behaviour
| Scenario | Result |
|---|---|
| Server restarted, grid_live empty | Next renderTimeline auto-restores held strategy |
| grid_live manually cleared | Auto-restored on next render cycle |
| User opens Switch Rule modal, wants to force sync | Click "Sync to Grid" button |
| No held strategy yet (before 01:00) | Both auto and manual are silent no-ops |
| Already has switch_rule entry | autoSyncToGrid exits early — no duplicate write |

## Completion Status
COMPLETE -- 2026-04-20
