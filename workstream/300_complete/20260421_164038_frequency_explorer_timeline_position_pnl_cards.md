# Frequency Explorer Timeline Position PnL Cards

Source: User request, 2026-04-21
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Enhance `fs/frequency_explorer.html` Snapshot Timeline so that after a position is opened or switched, subsequent 5-minute snapshot cards show a mini-card with the currently held position's updated result.

## Context
Affected file:
- `TradeApps/breakout/fs/frequency_explorer.html`

Requested behavior:
- When an `OPENING TRADE` signal occurs, record the opened product/strategy as the active held position.
- When a `SWITCH SIGNAL` occurs, replace the active held position with the switched-to product/strategy.
- For every subsequent 5-minute snapshot while a position is held, show a mini-card under the snapshot content using the same visual format style as the current opening/switch signal cards.
- The mini-card should show the updated result for the held position at that snapshot.
- The mini-card should be green when the held position is in profit and red when it is in loss.

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect current Snapshot Timeline rendering and signal evaluation flow.
  - [x] Test: Identify where `signalAtSnap`, `snap.leaders`, and `_summary_net` lookup are available during timeline render.
  - Evidence: `renderTimeline()` builds `signalAtSnap`; new helper uses `snap.leaders` first and `_getSummaryNetAt(...)` fallback.

- [x] 2. Add held-position replay state during timeline rendering.
  - [x] Test: Timeline iteration carries active held product/strategy forward after open/switch signals.
  - Evidence: `buildHeldStatusAtSnap(signalAtSnap)` iterates all snapshots chronologically and updates active held state on each open/switch signal.

- [x] 3. Add mini-card rendering for held-position updated result under subsequent snapshots.
  - [x] Test: Cards display product/strategy, current net/result, and are green for profit and red for loss.
  - Evidence: `renderHeldPositionBanner(...)` renders `HELD POSITION` with current net, entry net, result, held-since time; CSS includes `.held-position-banner.profit` and `.held-position-banner.loss`.

- [x] 4. Validate no product-type leakage in held-position cards.
  - [x] Test: Held-position card uses the same signal product/strategy chosen by product-type scoped switch logic.
  - Evidence: Held status is derived only from `signalAtSnap`, which is produced by existing product-type scoped switch/open evaluation.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Snapshot Timeline displays ongoing held-position PnL mini-cards after open/switch.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `rg -n "held-position-banner|buildHeldStatusAtSnap|getHeldCurrentNetAtSnap|renderHeldPositionBanner|heldStatusAtSnap|HELD POSITION" TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Required CSS, replay, result lookup, and render functions are present.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Static checks returned `css_loss=True`, `css_profit=True`, `render_insert=True`, `replay_map=True`, `summary_fallback=True`.
  - Objective-Proved: Green/red styling, held replay map, timeline insertion, and `_summary_net` fallback are implemented.
  - Status: captured

## Implementation Log
- 2026-04-21 16:40: Created backlog task from user request.
- 2026-04-21 16:43: Moved task to in-progress.
- 2026-04-21 16:45: Added held-position banner CSS with green profit and red loss variants.
- 2026-04-21 16:47: Added held-position replay helpers and current net lookup using leaderboard first, `_summary_net` fallback second.
- 2026-04-21 16:48: Inserted held-position mini-card rendering into Snapshot Timeline cards.
- 2026-04-21 16:50: Ran targeted static validation checks.

## Changes Made
- `TradeApps/breakout/fs/frequency_explorer.html`
  - Added `.held-position-banner`, `.held-position-banner.profit`, and `.held-position-banner.loss` styles.
  - Added `getHeldCurrentNetAtSnap(held, snap)`.
  - Added `buildHeldStatusAtSnap(signalAtSnap)`.
  - Added `renderHeldPositionBanner(status)`.
  - Updated `renderTimeline()` to build `heldStatusAtSnap` and render the held-position mini-card under each timeline snapshot after an open/switch has occurred.

## Validation
- `rg -n "held-position-banner|buildHeldStatusAtSnap|getHeldCurrentNetAtSnap|renderHeldPositionBanner|heldStatusAtSnap|HELD POSITION" TradeApps/breakout/fs/frequency_explorer.html`
  - Result: Found CSS, helper functions, replay map, and render insertion.
- Static checks:
  - Result: `css_loss=True`, `css_profit=True`, `render_insert=True`, `replay_map=True`, `summary_fallback=True`.

## Risks/Notes
- “Updated result” is implemented as `currentNet - entryNet`.
- `currentNet` uses the held product/strategy net from the current snapshot leaderboard when present; otherwise it falls back to `_summary_net` at the snapshot time.
- The held card is labelled `HELD POSITION` to distinguish it from `OPENING TRADE` and `SWITCH SIGNAL` action cards.

## Completion Status
Status: Complete
Created: 2026-04-21 16:40
Completed: 2026-04-21 16:50
