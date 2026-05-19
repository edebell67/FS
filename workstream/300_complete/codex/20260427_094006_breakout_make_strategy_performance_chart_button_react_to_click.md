# Task: Make Strategy Performance Chart Button React To Click

## Created
- 2026-04-27 09:40:06

## Status
- Complete

## Request
- Modify `fs/strategy_performance.html` so the `Chart` button visibly reacts when clicked.

## Scope
- Inspect the current `Chart` button behavior in `fs/strategy_performance.html`.
- Add immediate visual feedback when the button is clicked.
- Ensure the button reflects in-flight, success, or failure state if the click triggers async work.
- Keep the behavior aligned with the existing UI patterns used elsewhere in the Breakout frontend.

## Acceptance Criteria
- Clicking `Chart` produces immediate visible feedback.
- The button does not appear unresponsive while the action is running.
- If the action completes, the button returns to a normal usable state.
- If the action fails, the button shows an error state or equivalent visible feedback.

## Validation
- Open `fs/strategy_performance.html`.
- Click `Chart`.
- Confirm the button visibly changes state on click and during processing.
- Confirm the button resets correctly after completion or failure.

## Updates
- 2026-04-27 09:48:00: Implemented button-state feedback in `TradeApps/breakout/fs/strategy_performance.html`.
- Added `is-busy`, `is-success`, and `is-error` visual states for `.push-btn`.
- Added `setChartButtonState(...)` and wired `sendSummarySelectionToMultiChart(...)` to show `Sending...`, `Opening...`, `Sent`, and `Failed` states.
- Updated Strategy Performance, Top 20, and summary product chart buttons to pass their button element into the shared feedback flow.

## Validation Results
- Verified the new state hooks and button call sites exist with `rg`.
- Manual browser verification still required to confirm the visual timing and final UX states.
