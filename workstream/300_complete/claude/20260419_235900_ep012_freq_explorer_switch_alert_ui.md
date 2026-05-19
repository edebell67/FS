---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: complete
  depends_on: []
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Frequency Explorer — Switch Alert UI with Configurable Rules

**Source:** User request — add configurable switching rule controls and alert actions to frequency_explorer.html
**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

## Task Summary
Added a Switch Rule panel to frequency_explorer.html. At each 5-min snapshot, evaluates the
configured rule against rank-1 changes vs held strategy. When criteria is met, fires the
selected action (notification, highlight monitor, send to grid, or do nothing).

## Background / Context
Analysis established rank-1 + net>100 AND gap>20 as the best switching rule ($791/day avg,
35 switches over 25 clean days). The UI allows live configuration and testing of different
threshold combinations.

**Switching rule:** Only consider a switch when rank-1 changes AND new rank-1 has net > 0.
Then apply the configured filter (net gap, count gap, or both).

## Changes Made
- `TradeApps/breakout/fs/frequency_explorer.html`
  - Added CSS: `.switch-rule-panel` (yellow border panel), `.held-display`, `.switch-signal-card` (yellow border on timeline cards), `.switch-signal-banner` (signal indicator inside card), `.btn-monitor.switch-highlight` (pulsing yellow monitor button), `@keyframes monitorPulse`
  - Added HTML: Switch Rule panel above Snapshot Timeline containing:
    - Held strategy display (product / strategy / net / count)
    - Mode radios: Net Only / Count Only / Net OR Count / Net AND Count
    - Net>X dropdown: 25, 50, 100, 200, 300, 500 (default: 100)
    - Count>X dropdown: 5, 10, 15, 20, 25, 30, 50 (default: 20)
    - Action radios: Notification / Highlight Monitor / Send to Grid / Do Nothing
    - Show/Hide toggle
  - Added JS functions:
    - `initSwitchRuleUI()` — restores saved settings from localStorage
    - `toggleSwitchRulePanel()` — show/hide panel body
    - `updateSwitchRule()` — saves settings, re-renders timeline
    - `updateSwitchThresholdSelectors()` — disables irrelevant selector per mode
    - `updateHeldDisplay(data)` — updates held strategy display box
    - `evaluateSwitchSignals(rank1AtSnap)` — walks all snapshots, tracks held, evaluates rule, returns Map of snap -> signal
    - `fireSwitchAction(signal, snap)` — fires selected action (de-duped per snap)
    - `sendSwitchToGrid(product, strategy)` — POSTs to /api/grid_live/toggle
  - Modified `renderTimeline()`:
    - Calls `evaluateSwitchSignals()` after building rank1AtSnap
    - Fires action for latest snap signal
    - Renders `switch-signal-banner` inside cards where signal fired
    - Adds `switch-signal-card` class to flagged cards (yellow border)

## Behaviour
- Held strategy: set automatically from first positive rank-1 of the session; updates on switch signal
- Signal evaluation: runs across ALL snapshots (not just visible window) for accurate held tracking
- Timeline: shows yellow-bordered cards + inline banner at every snap where signal fired
- Notification action: reuses existing yellow rank alert popup with switch-specific content
- Send to Grid: calls /api/grid_live/toggle POST + shows notification
- Highlight Monitor: pulses monitor button yellow for 8 seconds
- All settings persist in localStorage

## Completion Status
COMPLETE -- 2026-04-19
