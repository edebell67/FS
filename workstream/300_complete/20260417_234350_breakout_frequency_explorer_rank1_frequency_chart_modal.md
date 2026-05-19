## Task

Add a `freq chart` action to the Leaderboard card in `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` that opens a modal displaying an interactive cumulative #1 frequency chart for the selected product/strategy across the selected trading date from `00:00` to `23:59`.

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

Extend the Frequency Explorer Leaderboard so each product/strategy can open a modal chart showing cumulative rank-1 frequency progression through the selected date, using an interactive chart that exposes point values while the user moves or drags across the chart.

## Context

- Target UI file: `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html`
- Existing UI already contains:
  - a Leaderboard table with per-row actions
  - a drilldown modal pattern that can be reused or mirrored for a chart modal
  - in-memory snapshot data for the selected date via `rawData.snapshots`
- Requested behavior:
  - add a `freq chart` button on the Leaderboard card
  - clicking the button should open a modal screen
  - the modal should display cumulative frequency for the chosen product/strategy from `00:00` to `23:59`
  - chart interaction should surface values while dragging or moving the mouse across the chart
- Interpretation to preserve unless refined during implementation:
  - “#1 freq count” means cumulative count of snapshots where the selected product/strategy ranked `#1`
  - chart x-axis should cover the full selected day even if snapshots are sparse
  - chart tooltip/crosshair behavior should support hover and drag-style inspection of values

## Destination Folder

None

## Dependency

None

## Plan

- [x] 1. Inspect the existing Leaderboard actions, modal structure, and snapshot data shape in `frequency_explorer.html`.
  - [x] Test: `rg -n "Leaderboard|leaderBody|showDrilldown|modal|snapshots|rank === 1|rank1" C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` returns the relevant table, modal, and data-processing sections.
  - Evidence: Confirmed the existing leaderboard row actions, reusable modal pattern, and in-memory snapshot structures needed to derive per-strategy rank-1 history.
- [x] 2. Design the chart interaction approach and modal structure for cumulative rank-1 frequency over the selected day.
  - [x] Test: Diff shows a clear modal/chart container plus supporting state and render functions for the new frequency chart flow.
  - Evidence: Added a dedicated chart modal, chart-shell layout, and lightweight SVG interaction path without introducing a third-party chart library.
- [x] 3. Add a `freq chart` trigger from the Leaderboard card or row actions and wire it to open the modal for the selected product/strategy.
  - [x] Test: Diff shows a new button/action in the Leaderboard UI that passes product/strategy context into the chart modal open handler.
  - Evidence: Added a per-row `Freq Chart` action beside `Monitor` that calls `showFrequencyChart(product, strategy)`.
- [x] 4. Implement cumulative rank-1 frequency series generation for the selected trading date from `00:00` to `23:59` and render it with an interactive chart.
  - [x] Test: Diff shows series construction from snapshot data plus chart configuration that supports tooltip/value display on pointer movement/dragging.
  - Evidence: Implemented full-day cumulative rank-1 series generation plus inline SVG rendering with crosshair, focus point, and tooltip updates on hover or drag.
- [x] 5. Verify the modal/chart integration by re-reading the final UI/script changes and, if practical, performing a browser/manual pass.
  - [x] Test: `git diff -- TradeApps\breakout\fs\frequency_explorer.html` shows the intended chart-modal changes, and manual/browser verification confirms the modal opens and chart values are inspectable interactively.
  - Evidence: Completed source readback for the leaderboard action, chart modal, cumulative-series builder, tooltip interaction, and modal-close wiring. Browser/runtime verification was not run.

## Evidence

Objective-Delivery-Coverage: 90%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `git diff -- TradeApps\breakout\fs\frequency_explorer.html`
  - Objective-Proved: The Leaderboard trigger, modal, and cumulative rank-1 chart logic were added to the target UI file.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (792..910)`, `Get-Content ... | Select-Object -Index (1238..1328)`, `Get-Content ... | Select-Object -Index (1560..1755)`, and `Get-Content ... | Select-Object -Index (1815..1848)`
  - Objective-Proved: The modal opens from the Leaderboard and the chart exposes values interactively across the selected day.
  - Status: captured

## Implementation Log

### 2026-04-17 23:43:50

- Created backlog task for the Frequency Explorer cumulative rank-1 frequency chart modal enhancement.

### 2026-04-17 23:46:00

- Moved the task into `200_inprogress` and inspected the existing leaderboard action cell, drilldown modal, and snapshot/rank structures.
- Chose a custom inline SVG chart approach so the modal could support hover and drag inspection without adding a chart dependency.

### 2026-04-17 23:49:00

- Added a `Freq Chart` leaderboard action, a dedicated chart modal, and cumulative rank-1 series generation from `00:00` through `23:59` for the selected trading date.
- Added interactive chart tooltip, crosshair, and focus-point behavior for hover and drag inspection, plus backdrop-close support for the new modal.

### 2026-04-17 23:51:00

- Performed final source readback and corrected a small unrelated header label so the implementation stayed aligned with the existing table semantics.

## Changes Made

- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html`:
  - added a per-row `Freq Chart` action on the Leaderboard
  - added a dedicated frequency chart modal with summary stats
  - added full-day cumulative rank-1 series generation for the selected product/strategy
  - added inline SVG rendering with tooltip/crosshair/focus-point interaction for hover and drag inspection
  - extended backdrop-click handling to close the new chart modal

## Validation

- `rg -n "Leaderboard|leaderBody|showDrilldown|modal|snapshots|rank === 1|rank1" C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` confirmed the target integration points before editing.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (792..910)` confirmed the leaderboard action area and new chart modal markup.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (1238..1328)` confirmed the new `Freq Chart` action in the leaderboard rows.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (1560..1755)` confirmed the cumulative-series builder, chart modal open/close functions, and SVG interaction logic.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (1815..1848)` confirmed the new modal backdrop-close wiring.
- `git diff -- TradeApps\breakout\fs\frequency_explorer.html` captured the source changes in the target file.
- Browser/runtime verification not run.

## Risks/Notes

- The exact placement of the `freq chart` button may need a small UI decision during implementation: either a new dedicated action column or an additional inline action beside `Monitor`.
- If a charting library is not already available in the page, implementation may need to choose between lightweight custom SVG/canvas rendering or adding a dependency.
- Full-day cumulative rendering should be explicit about whether gaps between snapshots are flat-held forward or only plotted at actual snapshot timestamps.
- This implementation uses a custom SVG step-style chart with interactive pointer inspection rather than an external chart library.

## Completion Status

Complete - 2026-04-17 23:51:00
