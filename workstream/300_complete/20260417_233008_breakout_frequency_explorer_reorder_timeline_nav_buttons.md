## Task

Update `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` so the Snapshot Timeline `<` button is placed next to the `>` button after the time-slot selection list.

## Source

- User request in Codex thread on 2026-04-17.

## Task Type

standard

## Task Attributes

- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
- depends_on: []
- feeds_into: []

## Task Summary

Adjust the Snapshot Timeline control order so the time-slot dropdown appears first and both navigation buttons are grouped after it, with `<` positioned next to `>` after the list.

## Context

- Target UI file: `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html`
- The Snapshot Timeline controls were recently added and currently place the buttons around the dropdown.
- This follow-up task is layout-only and should preserve the existing `shiftTimelineRange()` behavior and disabled-state logic.

## Destination Folder

None

## Dependency

- `C:\Users\edebe\eds\workstream\300_complete\20260417_222552_breakout_frequency_explorer_interaction_and_timeline_navigation.md`

## Plan

- [x] 1. Inspect the current Snapshot Timeline control markup and CSS in `frequency_explorer.html`.
  - [x] Test: `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (770..785)` shows the current `timeline-controls` order.
  - Evidence: Confirmed the existing control block placed `<` before the dropdown and `>` after it.
- [x] 2. Reorder the control markup so the time-slot dropdown comes first and the `<` button sits next to the `>` button after the dropdown without changing button handlers.
  - [x] Test: Diff shows the same controls with updated DOM order only.
  - Evidence: Reordered the `timeline-controls` markup so the select is first, followed by the unchanged `timelinePrevBtn` and `timelineNextBtn`.
- [x] 3. Verify the final markup readback and confirm the control order matches the request.
  - [x] Test: `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (770..785)` shows `select`, then `<`, then `>`.
  - Evidence: Post-edit readback confirms the requested control order in the Snapshot Timeline panel.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `git diff -- C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html`
  - Objective-Proved: The Snapshot Timeline control order was updated to place the nav buttons after the dropdown.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (814..823)`
  - Objective-Proved: The markup order matches the requested layout with `<` next to `>` after the time-slot list.
  - Status: captured

## Implementation Log

### 2026-04-17 23:30:08

- Created backlog task for the Snapshot Timeline nav-button reorder follow-up.

### 2026-04-17 23:31:00

- Moved the task into `200_inprogress`, inspected the current Snapshot Timeline control order, and confirmed the previous layout placed `<` before the dropdown.
- Reordered the markup so the dropdown appears first and the `<` and `>` buttons are grouped immediately after it.
- Verified the final control order by source readback and diff inspection.

## Changes Made

- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` to reorder the Snapshot Timeline controls to `select`, then `<`, then `>`.

## Validation

- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (814..823)` confirmed the final order is dropdown, then `<`, then `>`.
- `git diff -- C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` confirmed the change is limited to the control-order adjustment.

## Risks/Notes

- This task should stay limited to control ordering unless the current flex layout requires a small CSS adjustment to preserve spacing/alignment.
- No CSS adjustment was required for this reorder.

## Completion Status

Complete - 2026-04-17 23:31:00
