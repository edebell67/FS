Source: User request in Codex session on 2026-04-26
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Modify `TradeApps/breakout/fs/trade_bucket.html` so each trade bucket card has its own `Net View` selector (`D1` / `D2`) and each card defaults to the bucket’s persisted `TB Delta Type`.
Context: `TradeApps/breakout/fs/trade_bucket.html`, bucket card rendering, per-bucket delta calculations, and persisted `delta_type` coming from trade bucket creation / workflow `TB Delta Type`.
Destination Folder: TradeApps/breakout/fs/
Dependency: None

Plan:
- [x] 1. Trace the current page-level `Net View` implementation and identify where it drives all bucket cards together.
  - [x] Test: Inspect the selector markup and render path; pass when the current global delta-mode dependency is identified.
- [x] 2. Trace the bucket-level persisted `delta_type` path used to initialize card state.
  - [x] Test: Inspect the bucket payload/render inputs; pass when the authoritative per-bucket `delta_type` source is confirmed.
- [x] 3. Implement per-card `Net View` controls and bucket-scoped render logic.
  - [x] Test: Review the code diff; pass when each card has its own `D1`/`D2` selector and changing one card does not change the others.
- [x] 4. Ensure each card initializes from the bucket’s `TB Delta Type`.
  - [x] Test: Open multiple bucket cards with differing persisted delta types; pass when each card starts on the matching mode in source.
- [ ] 5. Validate the updated behavior and capture evidence.
  - [ ] Test: Refresh `trade_bucket.html`; pass when per-card `Net View` state remains bucket-correct and no longer depends on a single page-level selector.

## Evidence
Objective-Delivery-Coverage: 80%
Auto-Acceptance: false
- Evidence-Type: source_trace
  - Artifact: `TradeApps/breakout/fs/trade_bucket.html`
  - Objective-Proved: The original page used one global `netViewMode` selector to calculate delta display for every bucket card together.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/trade_bucket.html`
  - Objective-Proved: Each bucket card now renders its own `D1`/`D2` selector, initializes from `bucket.delta_type`, and updates `delta_type` through the bucket update API.
  - Status: captured

## Implementation Log
- 2026-04-26 22:02:33+01:00 Created backlog lifecycle task to replace the global `Net View` in `trade_bucket.html` with per-card `D1`/`D2` selectors that initialize from each bucket’s `TB Delta Type`.
- 2026-04-26 22:05:00+01:00 Moved the task into `200_inprogress` and confirmed the existing implementation used one page-level `netViewMode` selector to drive all bucket totals and row delta values together.
- 2026-04-26 22:08:30+01:00 Reworked `renderBuckets(...)` so each card derives its own delta mode from `bucket.delta_type`, renders a local `D1`/`D2` selector, and calculates bucket/strategy net values from that bucket-local mode.
- 2026-04-26 22:10:20+01:00 Added `changeBucketNetView(name, deltaType)` to persist per-card mode changes through `/api/trade_buckets/update`, so refresh and reload keep each card aligned with the bucket’s own `TB Delta Type`.

## Changes Made
- Updated `TradeApps/breakout/fs/trade_bucket.html`.
- Removed the global page-level `Net View` selector and its shared client-side persistence logic.
- Updated `renderBuckets(...)` to compute `useDelta1` and the delta label from each bucket’s own `delta_type`.
- Added a per-card `Net View` selector with `D1` / `D2` options inside each bucket card.
- Added `changeBucketNetView(name, deltaType)` to persist card-level delta-mode changes by updating the bucket’s `delta_type` on the backend.
- Kept bucket totals and strategy-row `Net (Δ)` values aligned to the card’s own selected/persisted mode.

## Validation
- Ran `rg -n "Net View|changeBucketNetView\\(|delta_type|bucketDeltaMode|D1|D2|netViewMode|handleNetViewModeChange|applyPreferredDeltaMode" "TradeApps\\breakout\\fs\\trade_bucket.html"`.
- Pending browser verification with multiple visible bucket cards.

## Risks/Notes
- The main behavioral change is from one shared page-level delta mode to independent bucket-card modes, so render state, drilldowns, and refresh behavior all need to remain bucket-scoped.

## Completion Status
- Awaiting user verification.


# User Feedback
User Verified: PASS
