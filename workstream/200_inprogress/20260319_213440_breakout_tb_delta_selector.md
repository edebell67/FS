# Trade Bucket Delta 1 / Delta 2 Selector

## Source
User request during conversation 3f749427-1d10-4b77-85a1-6cba67b76b00

## Task Summary
Add a selection function to the Trade Bucket UI that enables switching between Delta 1 and Delta 2 calculations. Default is Delta 2. When Delta 1 is selected, the displayed Net (Δ) values change accordingly.

- **Delta 1**: `Current Net - Start Net` (Daily profit since Midnight)
- **Delta 2** (default): `Current Net - Create Net` (Profit since bucket creation)

## Context
- `TradeApps/breakout/fs/trade_bucket.html` — Frontend UI rendering buckets and strategy rows
- `TradeApps/breakout/fs/trade_viewer_api.py` — Backend API returning `delta1` and `delta2` fields (already implemented in V20260319_2135)
- `TradeApps/breakout/fs/Constants.py` — Version tracking

## Dependency
Dependency: None — Backend already returns both `delta1` and `delta2` in the API response.

## Plan

- [x] 1. Update `trade_bucket.html`: Replace or repurpose the existing `netViewMode` dropdown to offer "Delta 1 (vs Start)" and "Delta 2 (vs Create)" options, defaulting to Delta 2.
  - Test: Hard refresh `trade_bucket.html`, verify dropdown shows Delta 1 and Delta 2 options with Delta 2 selected by default.
  - Evidence: Dropdown updated at line 459, options: `delta2` (default), `delta1`.

- [x] 2. Update `renderBuckets()` in `trade_bucket.html`: Read the selected delta mode. Display `s.delta1` when Delta 1 is selected, `s.delta2` when Delta 2 is selected, in the strategy row Net column. Active column is bold.
  - Test: Switch dropdown to Delta 1, verify strategy row values change to daily profit. Switch back to Delta 2, verify values revert to bucket-creation-based profit.
  - Evidence: renderBuckets reads `deltaMode`, applies `d1Style`/`d2Style` for bold highlight on active column.

- [x] 3. Update bucket-level `TOTAL NET (Δ)` summary: Aggregate from the selected delta (`delta1` or `delta2`) across all strategies in the bucket. Label dynamically changes.
  - Test: Verify the TOTAL NET header value and label change when toggling between Delta 1 and Delta 2.
  - Evidence: `bucketTotalNet` uses `useDelta1 ? s.delta1 : s.delta2`. Label uses `deltaLabel`.

- [x] 4. Update `Constants.py` VERSION to `V20260319_2140`.
  - Test: Verify `Constants.py` shows `V20260319_2140`.
  - Evidence: Constants.py updated.

- [x] 5. Commit and push to GitHub.
  - Test: Verify `git log -1` shows the correct commit message.
  - Evidence: Commit `V20260319_2140: Added Delta 1/Delta 2 selector to Trade Buckets with dynamic column highlighting and total recalculation.`

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: manual_verification
  - Artifact: `http://192.168.1.110:5000/trade_bucket.html`
  - Objective-Proved: Delta selector switches between Delta 1 and Delta 2 calculations correctly
  - Status: planned

- Evidence-Type: diff
  - Artifact: Git commit f66e3621ff
  - Objective-Proved: Code changes are minimal and correctly scoped
  - Status: captured

## Implementation Log
- 2026-03-19 21:34 — Task created. Backend already returns both `delta1` and `delta2` fields (V20260319_2135). Only frontend changes needed.
- 2026-03-19 21:40 — All UI changes implemented. Dropdown updated, renderBuckets refactored, bucket total and column highlighting added. Pushed to GitHub.

## Changes Made
- `trade_bucket.html`: Replaced `netViewMode` dropdown options (delta2/delta1), refactored `renderBuckets()` to use delta mode, dynamic column highlighting, dynamic TOTAL NET label.
- `Constants.py`: VERSION updated to V20260319_2140.

## Validation
- Awaiting user hard refresh and visual confirmation.

## Risks/Notes
- No backend changes required — API already serves both delta values.

## Completion Status
**Awaiting user verification** — 2026-03-19 21:40
