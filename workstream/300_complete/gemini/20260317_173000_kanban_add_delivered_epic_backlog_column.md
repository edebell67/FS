# Task: Kanban Delivered Epic/Backlog Column

`Source`: `C:\Users\edebe\eds\plans\20260317_1730_V20260317_1730_Kanban_Delivered_Column.md`
`Task Summary`: Add a new dashboard column grouping all tasks by Epic, positioned between the Completed and Fail/Blocked columns. Highlights completion status in Green/Red with expandable lists.
`Context`: `workstream\kanban_dashboard.py`, `TradeApps\breakout\fs\constants.py`
`Dependency`: None

## Plan
- [ ] 1. Modify `kanban_dashboard.py` backend to aggregate tasks by source Epic.
  - Test: Check `/api/kanban` output for `epics` object.
  - Evidence: API response includes tasks grouped by Epic slug.
- [ ] 2. Implement the "Delivered (Epic/Backlog)" column in the UI template, positioned between "Completed" and "Fail & Blocked".
  - Test: UI shows the new column in the correct sequence.
  - Evidence: HTML layout updated.
- [ ] 3. Add JS logic for expandable Epic cards and task status coloring.
  - Test: Clicking Epic name expands/collapses list; status colors match folder location.
  - Evidence: Functional expansion and conditional styling applied.
- [ ] 4. Update version in `constants.py`.
  - Test: `VERSION` is `V20260317_1730`.
  - Evidence: `constants.py` updated.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `workstream\kanban_dashboard.py`
  - Objective-Proved: New Delivered column and grouping logic implemented.
  - Status: planned
- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\constants.py`
  - Objective-Proved: Version bumped to V20260317_1730.
  - Status: planned

## Implementation Log
- 2026-03-17 17:30: Created task and plan.

## Changes Made
- (Pending)

## Validation
- (Pending)

## Risks/Notes
- Large epics might clutter the column if not collapsed by default.

## Completion Status
**PENDING**
