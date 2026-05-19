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

# Frequency Explorer — Convert Switch Rule Panel to Modal

**Source:** User request — move the Switch Rule inline panel into a modal, accessible via a new button next to the rank alert bell button
**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

## Task Summary
Remove the Switch Rule `data-panel` from the page body and replace with a modal.
Add a new header button (⚡ icon) next to the existing rank alert bell button (🔔) to open it.
All existing functionality (mode, thresholds, action, held display, signal banners) remains unchanged.

## Current State
Switch Rule panel sits inline above the Snapshot Timeline as a `switch-rule-panel` div.
Accessible but takes up permanent vertical space on the page.

## Required Changes

### 1. Remove inline panel from page body
- Remove the `<div class="switch-rule-panel" id="switchRulePanel">` block from the HTML body
- Keep all JS logic (evaluateSwitchSignals, fireSwitchAction, updateSwitchRule etc.) unchanged

### 2. Add Switch Rule Modal
New modal (`id="switchRuleModal"`) following same pattern as `drilldownModal` and `freqChartModal`:
- Modal overlay with backdrop blur
- Modal content with header + body
- Header: "⚡ Switch Rule" title + close button
- Body: held strategy display + mode/threshold/action controls (same as current panel)
- Close on backdrop click or close button

### 3. Add header button
New button in `.header-actions` next to the existing rank alert bell button:
```html
<button class="btn-outline" onclick="openSwitchRuleModal()"
    title="Switch Rule"
    style="color:#ffe600; border-color:#ffe600;">
    <i class="fas fa-bolt"></i>
</button>
```

### 4. JS changes
- Add `openSwitchRuleModal()` — shows modal, calls `initSwitchRuleUI()`
- Add `closeSwitchRuleModal()` — hides modal
- Remove `toggleSwitchRulePanel()` (no longer needed)
- `initSwitchRuleUI()` — remove panel open/close logic, keep settings restore
- Keep `switchRulePanelOpen` localStorage key removal (cleanup)

### 5. Signal banners in timeline
Timeline signal banners (yellow-bordered cards + inline ⚡ banner) remain on the main page —
they are rendered by `renderTimeline()` and do not depend on the modal being open.

## Plan
- [ ] 1. Add modal HTML (switchRuleModal) with header + body containing existing controls
- [ ] 2. Add ⚡ button to header-actions next to bell button
- [ ] 3. Add `openSwitchRuleModal()` / `closeSwitchRuleModal()` JS functions
- [ ] 4. Remove inline switch-rule-panel HTML from page body
- [ ] 5. Update `initSwitchRuleUI()` to remove panel toggle logic
- [ ] 6. Remove switch-rule-panel CSS (keep switch-signal-card, held-display, switch-signal-banner)

## Evidence / Acceptance Criteria
- [ ] ⚡ button visible in header next to 🔔 bell button
- [ ] Clicking ⚡ opens modal with all controls intact
- [ ] Settings persist (localStorage) across open/close
- [ ] Timeline signal banners still render correctly without modal open
- [ ] No regressions to existing timeline rendering or rank alert

## Completion Status
PENDING
