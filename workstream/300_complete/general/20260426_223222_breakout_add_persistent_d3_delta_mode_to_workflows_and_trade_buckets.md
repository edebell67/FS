Source: User request in Codex session on 2026-04-26
Task Type: standard
Task Attributes:
  recurring_task: false
  looping_task: false
  splittable_task: false
  workflow_task: false
Task Summary: Add persistent `D3` delta mode support so trade buckets can measure profit since the exact time `D3` was selected, and expose that mode in both `workflow_automation.html` and `trade_bucket.html`.
Context: `D1` is profit since day start, `D2` is profit since bucket creation, and new `D3` must be profit since the exact timestamp when `D3` is selected. That timestamp and the corresponding baseline net must remain absolutely persistent for the bucket/card while `D3` remains selected. Scope includes workflow creation options in `TradeApps/breakout/fs/workflow_automation.html` for `profile_match_workflow` and `top_x_multi_chart_workflow`, backend bucket persistence/calculation in `TradeApps/breakout/fs/trade_viewer_api.py`, and per-card selection/rendering in `TradeApps/breakout/fs/trade_bucket.html`.
Destination Folder: TradeApps/breakout/fs/
Dependency: None

Plan:
- [x] 1. Trace the current `D1` / `D2` bucket delta model end to end.
  - [x] Test: Inspect workflow payloads, bucket persistence, summary-based delta calculation, and trade bucket rendering; pass when all current `delta_type` touchpoints are identified.
- [x] 2. Design persistent `D3` bucket state.
  - [x] Test: Define the exact persisted fields needed for `D3` timestamp and baseline net values; pass when the storage/update model is source-backed and unambiguous.
- [x] 3. Add backend support for `D3`.
  - [x] Test: Review code diff and targeted backend flow; pass when buckets can store/select `delta3`, capture the selection-time baseline, and recalculate card/leader stats from that frozen baseline.
- [x] 4. Add `D3` selection to workflow creation paths.
  - [x] Test: Inspect `workflow_automation.html`; pass when `profile_match_workflow` and `top_x_multi_chart_workflow` both allow `D3` to be chosen and submitted as `delta_type`.
- [x] 5. Add `D3` selection to `trade_bucket.html`.
  - [x] Test: Inspect the card UI/render path; pass when each bucket card can select `D3` and show `D3`-based values using the persisted frozen baseline.
- [ ] 6. Validate persistence and behavior.
  - [ ] Test: Select `D3` on a bucket, capture the selection timestamp/baseline, refresh the page, and confirm the card still uses the same frozen baseline until the mode changes again.

## Evidence
Objective-Delivery-Coverage: 83%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/trade_viewer_api.py`
  - Objective-Proved: Backend now accepts `delta3`, persists `delta3_selected_at` plus per-strategy `delta3_net_at_selection`, captures a new frozen baseline when switching into `D3`, and computes `delta3` for bucket display/leadership.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/workflow_automation.html`, `TradeApps/breakout/fs/trade_bucket.html`
  - Objective-Proved: `D3` is selectable in both workflow creation surfaces and per-card bucket `Net View`.
  - Status: captured
- Evidence-Type: validation
  - Artifact: `python -m py_compile TradeApps/breakout/fs/trade_viewer_api.py TradeApps/breakout/fs/summary_net_generator.py`
  - Objective-Proved: Patched backend Python compiles cleanly.
  - Status: captured

## Implementation Log
- 2026-04-26 22:32:22+01:00 Created backlog lifecycle task to add persistent `D3` delta mode support across workflow creation, bucket persistence, and trade bucket card rendering.
- 2026-04-26 22:35:10+01:00 Moved the task into `200_inprogress` and traced the existing `D1`/`D2` path across workflow payloads, bucket creation/update persistence, bucket refresh calculation, and trade bucket card rendering.
- 2026-04-26 22:39:20+01:00 Added backend `delta3` normalization plus persistent capture helpers for `delta3_selected_at` and per-strategy `delta3_net_at_selection` in `trade_viewer_api.py`.
- 2026-04-26 22:42:15+01:00 Updated bucket refresh calculation and leadership/performance logic so `D3` computes current normalized net minus the frozen `D3` baseline.
- 2026-04-26 22:44:00+01:00 Updated bucket creation and bucket update flows so new `D3` buckets initialize a frozen baseline and switching an existing bucket into `D3` captures a fresh baseline at selection time.
- 2026-04-26 22:45:20+01:00 Added `delta3` options to `workflow_automation.html` for both `profile_match_workflow` and `top_x_multi_chart_workflow`, and added `D3` selection/render support to per-card `Net View` in `trade_bucket.html`.
- 2026-04-26 22:46:10+01:00 Ran `python -m py_compile` against the patched backend modules successfully.

## Changes Made
- Updated `TradeApps/breakout/fs/trade_viewer_api.py`.
- Extended `_normalize_delta_type(...)` to support `delta3`.
- Added persistent `D3` capture helpers that store:
  - bucket-level `delta3_selected_at`
  - strategy-level `delta3_net_at_selection`
  - strategy-level `delta3_selected_at`
- Updated bucket creation so buckets created with `delta3` initialize a frozen baseline from creation-time context.
- Updated bucket update so switching from `D1`/`D2` into `D3` captures a new frozen baseline at the exact selection time and keeps it fixed while the bucket remains in `D3`.
- Updated bucket refresh calculation so strategies expose `delta3`, and `total_net` follows `delta1`, `delta2`, or `delta3` based on the bucket’s persisted mode.
- Updated bucket leadership/performance calculation so `delta3` is used consistently in bucket-level ranking logic.
- Updated `TradeApps/breakout/fs/workflow_automation.html` to add `delta3` to `TB Delta Type` in `profile_match_workflow` and `top_x_multi_chart_workflow`.
- Updated `TradeApps/breakout/fs/trade_bucket.html` so per-card `Net View` now includes `D3` and renders bucket totals / strategy deltas from persisted `delta3`.

## Validation
- Ran `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py`.
- Pending UI verification of `D3` selection, persistence, refresh stability, and visible values.

## Risks/Notes
- `D3` is not just another display toggle. It requires persistent bucket state for the selection timestamp and baseline net(s), and downstream bucket leadership or trade-selection logic may also need to become `D3`-aware.
- The persistence model must define whether switching away from `D3` and later back to `D3` reuses the old frozen baseline or captures a new one. Current request implies capture at the time `D3` is selected, then remain fixed while `D3` stays selected.
- Implemented behavior follows that interpretation: re-entering `D3` from another mode captures a fresh frozen baseline; remaining on `D3` preserves the existing frozen timestamp/net values.

## Completion Status
- Awaiting user verification.


# User Feedback
User Verified: PASS
