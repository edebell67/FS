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

# Frequency Explorer — Reduce Margin Between Menu and Cards

**Source:** User request — reduce vertical gap between sidebar/header and the card content below
**Destination:** `TradeApps/breakout/fs/frequency_explorer.html`

## Task Summary
Tighten the vertical spacing between the top header/menu area and the summary cards/panels below.
Currently `.main-content` has `padding: 40px 50px 80px` — reduce top padding and shift all content closer to the menu.

## Plan
- [ ] 1. Reduce `.main-content` top padding (40px → ~16px)
- [ ] 2. Reduce `.header` bottom margin (30px → ~16px)
- [ ] 3. Reduce `.summary-grid` bottom margin (30px → ~16px) if needed
- [ ] 4. Check no cards are clipped or overlap header elements

## Completion Status
PENDING
