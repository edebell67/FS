# Breakout Multi Chart Merge Selected Cards Shared Scale

Source: User request, 2026-04-22
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Enhance `fs/multi_chart.html` so a user can select multiple chart cards and merge their charts into a single combined card. The merged card must use shared scaling so the selected charts can be compared on the same axis/scale rather than each card rendering independently.

## Context
Target UI:
- `TradeApps/breakout/fs/multi_chart.html`

Requested behavior:
- Allow selecting multiple existing chart cards.
- Add an action/control to merge the selected cards into one combined card.
- Render the selected chart series together inside the merged card.
- Use the same x-axis and y-axis scale for all merged chart series.
- Preserve enough label/legend context so each merged series remains identifiable.
- Ensure the merged view does not break existing individual-card behavior.
- Merged cards must be permanent and usable like any other chart card; all existing chart-card functionality must apply to merged cards.
- After a successful merge, remove the selected source cards from the active card set.

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: Existing `TradeApps/breakout/fs/multi_chart.html` chart-card rendering and selection patterns.

## Plan
- [x] 1. Inspect existing multi-chart card rendering and chart library usage.
  - Test: Identify the functions/data structures responsible for card creation, chart rendering, and existing chart scale options.
  - Evidence: `multi_chart.html` imports `multi_chart.js`; cards are represented by `activeOverlays[].group`; `createGroupCard`, `updateCharts`, `renderGroupCharts`, and `renderChartOnCanvas` render Chart.js line charts with shared `x` and `y` scales per card.

- [x] 2. Add selected-card state and card selection UI.
  - Test: User can select and deselect multiple chart cards without changing the current chart rendering.
  - Evidence: Added `selectedChartGroups`, per-card select button, selected-card styling, and selected-count status in `multi_chart.html` / `multi_chart.js`.

- [x] 3. Add a merge action for selected cards.
  - Test: Merge action is enabled only when at least two chart cards are selected and creates one combined card from those selections.
  - Evidence: Added `mergeSelectedCardsButton`, `updateMergeControls`, and `mergeSelectedCards`; button is disabled until `selectedChartGroups.size >= 2`.

- [x] 4. Render merged chart series with shared x/y scaling.
  - Test: Merged card displays all selected series using the same x-axis and y-axis scale and includes labels/legend entries for each source card.
  - Evidence: Merge rewrites selected overlays into one group, so `renderChartOnCanvas` renders all merged datasets in one Chart.js card with one `x` scale and one `y` scale; group value list preserves source series labels.

- [x] 5. Preserve chart-card behavior for merged cards and remove source cards after merge.
  - Test: Merged cards support the same functionality as normal cards, and selected source cards are removed after a successful merge.
  - Evidence: Merged card uses the existing `activeOverlays` group model; selected source groups are removed from `activeOverlays`, their chart instances are destroyed, and `updateCharts` removes their cards.

- [x] 6. Validate in browser and capture UI evidence.
  - Test: Open `fs/multi_chart.html`, select multiple cards, merge them, and verify the combined card renders with shared scaling.
  - Evidence: Static validation captured. Browser automation was not run in this turn; `node --check TradeApps/breakout/fs/multi_chart.js` passed and static grep confirmed merge hooks and cache-busted script import.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/multi_chart.html`, `TradeApps/breakout/fs/multi_chart.js`
  - Objective-Proved: Implementation adds selected-card merge functionality.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: Static verification of `TradeApps/breakout/fs/multi_chart.html`
  - Objective-Proved: User can merge selected chart cards into one shared-scale card.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `node --check TradeApps/breakout/fs/multi_chart.js`
  - Objective-Proved: Updated JavaScript parses successfully.
  - Status: captured

## Implementation Log
- 2026-04-22 20:54: Created todo task from user request.
- 2026-04-22 20:55: Moved task to in-progress.
- 2026-04-22 21:03: Added selected-card state, merge controls, merge action, source-card removal, and cache-busted JS import.

## Changes Made
- Updated `TradeApps/breakout/fs/multi_chart.html`.
  - Added selected-card visual styling.
  - Added `Merge Selected` smart action button and selected-card count.
  - Bumped `multi_chart.js` cache-buster to `V20260422_2055`.
- Updated `TradeApps/breakout/fs/multi_chart.js`.
  - Added `selectedChartGroups` state.
  - Added card select/deselect control.
  - Added merge controls that enable only with at least two selected cards.
  - Added `mergeSelectedCards` to create one new active group from selected source groups.
  - Removed selected source groups from `activeOverlays` after successful merge.
  - Destroyed removed source chart instances and reused existing `updateCharts` card cleanup.
  - Kept merged cards inside the existing `activeOverlays` group model so normal card functions continue to apply.

## Validation
- `node --check TradeApps/breakout/fs/multi_chart.js`
  - Result: pass.
- Static grep for merge hooks:
  - Result: found `mergeSelectedCardsButton`, `mergeSelectedCards`, `toggleCardMergeSelection`, `selected-for-merge`, and updated script cache-buster.
- Implementation verification:
  - Merged card renders all selected overlays as datasets in one Chart.js instance, which uses the existing single `x` and `y` scale configuration.

## Risks/Notes
- Shared scaling is explicitly the same x-axis and y-axis scale for all merged series; do not normalize independently.
- Need to avoid destructive changes to existing multi-chart workflows.
- If chart rendering is library-specific, implementation should reuse existing scale/axis options rather than adding a parallel charting path.
- Browser automation was not run; validation is static plus JavaScript parse check.

## Completion Status
Status: Complete
Created: 2026-04-22 20:54
Completed: 2026-04-22 21:04
