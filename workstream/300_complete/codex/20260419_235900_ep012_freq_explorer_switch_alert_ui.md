---
Task Type: standard
Task Attributes:
  workflow_task: true
  workflow_name: adaptive_strategy_selection_engine
  workflow_stage: backlog
  depends_on: []
  feeds_into: []
---
**Epic:** adaptive_strategy_selection_engine

# Frequency Explorer — Switch Alert UI with Configurable Rules

**Source:** User request — add configurable switching rule controls and alert actions to frequency_explorer.html
**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

## Task Summary
Add a switching rule configuration panel to frequency_explorer.html. At each 5-min snapshot,
evaluate the configured rule against the current rank-1 vs held strategy. When criteria is met,
fire the selected action (notification, highlight, grid send, or do nothing).

## Background / Context
Analysis (see task 20260419_235500) identified rank-1 + net>100 AND gap>20 as the best
switching rule ($791/day avg, 35 switches over 25 days). The UI should allow the user to
configure and test different threshold combinations live.

**Switching rule:** Only consider a switch when rank-1 changes AND new rank-1 has net > 0.
Then apply the configured filter (net gap, count gap, or both).

## Requirements

### 1. Threshold Controls Panel
Two threshold selectors (only active when relevant mode is selected):

**net>X** — dropdown options: 25, 50, 100, 200, 300, 500
- Label: "Net Gap ($)"
- Compare: new rank-1 net vs held strategy net

**gap>X** — dropdown options: 5, 10, 15, 20, 25, 30, 50
- Label: "Count Gap (#)"
- Compare: new rank-1 rank1_count_cum vs held rank1_count_cum (yellow badge)

### 2. Combination Mode — 3 radio options
1. **Net only** — trigger if net gap condition met (gap selector disabled)
2. **Count only** — trigger if count gap condition met (net selector disabled)
3. **OR** — trigger if net gap OR count gap condition met (both selectors active)
4. **AND** — trigger if net gap AND count gap both met (both selectors active)

### 3. Action on Trigger — 4 options (radio/select)
When switching criteria is met, fire one of:

1. **Send to Grid** — send product + strategy to grid for L-trade execution
2. **Highlight Monitor** — highlight the monitor button (draw attention)
3. **Notification only** — expand yellow notification banner with product/strategy + reason
4. **Do nothing** — evaluate silently (useful for backtesting/observation)

### 4. Held Strategy Tracking
- On first positive rank-1 of the session → set as held strategy (shown in panel)
- When switch criteria fires and action taken → update held strategy
- Display held strategy name + net + count badge in panel
- Allow manual override (click to set held strategy)

### 5. Yellow Notification Banner (on trigger)
Expand existing yellow notification area with:
- "SWITCH SIGNAL: [product] / [strategy]"
- Net gap: +$XXX | Count gap: +XX
- Rule that fired: net>X / gap>X / both
- Timestamp
- Dismiss button

## Plan
- [ ] 1. Add switch rule panel HTML + CSS (collapsible, above timeline)
- [ ] 2. Implement held strategy tracking in JS (set on first positive rank-1)
- [ ] 3. Implement rule evaluation logic at each snapshot render
- [ ] 4. Wire up action handlers:
       - Notification banner expand
       - Monitor button highlight
       - Grid send (POST to grid API or fire existing grid event)
       - Do nothing (silent log)
- [ ] 5. Persist panel settings in localStorage
- [ ] 6. Test against 2026-04-17 data (known: held=EURAUD_C breakout_2_tp5_sl3)

## Evidence / Acceptance Criteria
- [ ] Panel renders with correct dropdowns and mode selectors
- [ ] Held strategy updates correctly on session open and after switch
- [ ] Notification banner fires when criteria met with correct values
- [ ] Settings persist across page reload
- [ ] No regressions to existing timeline rendering

## Notes
- net>X compares held strategy's CURRENT net at that snapshot (not opening net)
- gap>X compares rank1_count_cum (yellow badge value) — already computed in renderTimeline()
- Switch cost ($50) not applied in UI — purely a signal/alert tool
- Only trigger on rank-1 changes where new rank-1 net > 0 (exclude negatives)

## Completion Status
PENDING
