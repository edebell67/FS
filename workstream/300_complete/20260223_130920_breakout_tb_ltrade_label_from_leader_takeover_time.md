# Task Summary
Update Trade Bucket UI so current-leader trades are marked L-trade only from leader takeover time onward.

## Context
- TradeApps/breakout/fs/trade_bucket.html
- TradeApps/breakout/fs/trade_viewer_api.py (read-only for endpoint reference)

## Implementation Log
- Created lifecycle task file and moved to in-progress.

## Changes Made
- Pending.

## Validation
- Pending.

## Risks/Notes
- Pending.

## Completion Status
- In progress.

## Implementation Log
- Added leader resolution helper in TB UI using existing net-gap logic.
- Added grid_live read path in UI to resolve per-bucket leader takeover timestamp (`activated_at`).
- Updated L-trade filtering so current leader trades are counted as L-trades only when trade entry time is on/after leader takeover timestamp.
- Applied same rule to card-level L-Trade Net and modal L-trade list for consistency.

## Changes Made
- Updated `TradeApps/breakout/fs/trade_bucket.html` only:
  - Added cache/state for grid rows (`lastGridLiveRows`).
  - Added helpers:
    - `getCurrentLeaderKey(bucket)`
    - `getGridLiveEntries(runMode)`
    - `getLeaderTakeoverTimeMs(bucket, runMode)`
    - `getLeaderTakeoverTimeMsFromRows(bucketName, leader, rows)`
  - Updated `loadBuckets()` to fetch and cache `grid_live` rows.
  - Updated `getBucketLTrades(bucket, allTrades, options)` to enforce leader-takeover-time gating for exact leader strategy matches.
  - Updated both card aggregation and modal L-trade list to pass leader/takeover context into `getBucketLTrades`.

## Validation
- Searched and confirmed injected anchors/usage:
  - `rg -n "lastGridLiveRows|getLeaderTakeoverTimeMsFromRows|getCurrentLeaderKey\(|getBucketLTrades\(bucket, allTrades" TradeApps/breakout/fs/trade_bucket.html`
- Manual logic validation against endpoint contract:
  - `/api/grid_live` returns `data` rows with `source` and `activated_at`.
- Note:
  - `node --check` cannot validate `.html` directly (expected limitation).

## Risks/Notes
- Fallback matching paths (source_group/source_screen) remain unchanged for non-exact strategy matches.
- If `activated_at` is missing for current leader in grid, logic falls back to prior behavior for exact matches (no takeover gate applied).

## Completion Status
- Completed on 2026-02-23.
