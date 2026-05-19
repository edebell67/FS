## Task

Enhance `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` so cumulative frequency charts can display multiple product/strategy series on the same chart and same scale.

## Source

- User request in Codex thread on 2026-04-18.

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

Extend the existing cumulative rank-1 frequency chart flow so users can compare more than one product/strategy on a single shared-scale chart, either by plotting multiple series at once or by adding selected cumulative-frequency series into an already-open chart.

## Context

- Target UI file: `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html`
- Existing implementation already provides:
  - a per-row `Freq Chart` action on the Leaderboard
  - a dedicated frequency chart modal
  - custom inline SVG rendering for a single cumulative rank-1 frequency series
  - tooltip/crosshair behavior for interactive point inspection
- New requested capability:
  - provide an additional function to plot all different charts on a single chart
  - or enable functionality to add one or more cumulative-frequency series for selected product/strategy into an existing chart on the same scale
- Implementation should likely converge these into one comparison workflow rather than treating them as unrelated features.

## Destination Folder

None

## Dependency

- `C:\Users\edebe\eds\workstream\300_complete\20260417_234350_breakout_frequency_explorer_rank1_frequency_chart_modal.md`

## Plan

- [x] 1. Inspect the current single-series frequency chart modal, leaderboard trigger path, and chart state in `frequency_explorer.html`.
  - [x] Test: `rg -n "Freq Chart|showFrequencyChart|freqChart|buildFrequencyChartSeries|renderFrequencyChartSvg" C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` returns the relevant trigger, modal, and rendering sections.
  - Evidence: Confirmed the existing single-series chart modal, per-row `Freq Chart` trigger, and inline SVG render path before extending it.
- [x] 2. Define the comparison-chart interaction model, including whether users can add series incrementally, load all visible series at once, or both.
  - [x] Test: Diff shows explicit comparison-chart state and UI controls for multi-series selection/addition on one shared chart.
  - Evidence: Implemented a hybrid model: repeated `Freq Chart` clicks append series while the modal is open, and the modal also exposes a `Plot Visible` control for the currently visible leaderboard set.
- [x] 3. Update the chart modal and leaderboard/chart controls so one or more product/strategy cumulative-frequency series can be plotted together.
  - [x] Test: Diff shows new UI actions or modal controls that support adding/comparing multiple series on the same chart.
  - Evidence: Added modal comparison controls, a legend, and per-row append behavior for multi-series comparison on one chart.
- [x] 4. Extend the chart renderer so multiple cumulative-frequency series are drawn on the same shared axis scale with clear legend/series identification and interactive value inspection.
  - [x] Test: Diff shows multi-series rendering logic, shared y-axis scaling, and tooltip/crosshair behavior that identifies the inspected series values.
  - Evidence: Reworked the renderer to use multiple datasets, shared y-axis scaling, per-series color assignment, legend output, and a tooltip that shows all compared cumulative values at the inspected time.
- [x] 5. Verify the multi-series comparison flow by re-reading the updated UI/script and, if practical, running a browser/manual check.
  - [x] Test: `git diff -- TradeApps\breakout\fs\frequency_explorer.html` shows the intended multi-series chart changes, and manual/browser verification confirms multiple cumulative-frequency lines can be displayed together on the same scale.
  - Evidence: Completed source readback for the comparison controls, append behavior, multi-series renderer, and tooltip logic. Browser/runtime verification was not run.

## Evidence

Objective-Delivery-Coverage: 90%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `git diff -- TradeApps\breakout\fs\frequency_explorer.html`
  - Objective-Proved: The chart workflow was extended from single-series to shared-scale multi-series cumulative frequency comparison.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (520..610)`, `Get-Content ... | Select-Object -Index (960..990)`, `Get-Content ... | Select-Object -Index (1418..1440)`, and `Get-Content ... | Select-Object -Index (1688..1915)`
  - Objective-Proved: Users can compare one or more cumulative-frequency series on the same chart and inspect values interactively.
  - Status: captured

## Implementation Log

### 2026-04-18 00:03:28

- Created backlog task for the Frequency Explorer multi-series cumulative-frequency chart enhancement.

### 2026-04-18 00:05:00

- Moved the task into `200_inprogress` and inspected the current single-series chart modal, trigger path, and SVG chart state.
- Chose a hybrid comparison interaction: append series via repeated leaderboard `Freq Chart` clicks while the modal is open, plus a modal action to plot all currently visible leaderboard rows.

### 2026-04-18 00:08:00

- Added comparison controls, legend output, shared multi-dataset chart state, and a multi-series renderer using the existing inline SVG approach.
- Updated tooltip behavior to report the cumulative values for all compared series at the inspected time instead of only one line.

### 2026-04-18 00:10:00

- Completed source readback and diff verification for the comparison controls, renderer updates, and append/plot-visible workflow.

## Changes Made

- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html`:
  - replaced single-series chart state with multi-dataset comparison state
  - added `Plot Visible` and `Clear Compare` controls to the chart modal
  - added a legend for compared product/strategy series
  - updated `Freq Chart` row actions so additional clicks append into the open comparison chart
  - extended the inline SVG renderer to plot multiple cumulative-frequency series on one shared scale
  - updated tooltip/crosshair behavior to show the values for all compared series at the hovered time

## Validation

- `rg -n "Freq Chart|showFrequencyChart|freqChart|buildFrequencyChartSeries|renderFrequencyChartSvg" C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html` confirmed the target chart-comparison integration points before editing.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (520..610)` confirmed the added comparison controls and legend styling.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (960..990)` confirmed the modal now includes `Plot Visible`, `Clear Compare`, and legend markup.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (1418..1440)` confirmed the leaderboard `Freq Chart` action now appends when the modal is already open.
- `Get-Content C:\Users\edebe\eds\TradeApps\breakout\fs\frequency_explorer.html | Select-Object -Index (1688..1915)` confirmed the multi-dataset chart state, comparison controls, shared-scale renderer, and multi-series tooltip logic.
- `git diff -- TradeApps\breakout\fs\frequency_explorer.html` captured the source changes in the target file.
- Browser/runtime verification not run.

## Risks/Notes

- The biggest design decision is the selection workflow: `plot all`, `add selected to current chart`, or a hybrid that supports both.
- Multi-series comparison will need clear color assignment, legend behavior, and tooltip logic so overlapping cumulative lines remain readable.
- Shared-scale rendering should preserve exact cumulative counts for all series; the y-axis must be derived from the maximum across every displayed series.
- This implementation uses the hybrid approach: users can append series one-by-one from the leaderboard or load the current visible leaderboard set into the same chart.

## Completion Status

Complete - 2026-04-18 00:10:00
