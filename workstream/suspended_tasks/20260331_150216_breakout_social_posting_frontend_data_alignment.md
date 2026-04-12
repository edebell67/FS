# Frontend Data Alignment For Social Posting Package

## Source
User request on 2026-03-31 to create a task and correct the consolidated Twitter/X draft so it matches the current data visible in the frontend rather than stale weekly stats-derived daily values.

## Task Type
standard

## Task Attributes
- recurring_task: false
- recurrence_type: none
- recurrence_rule: none
- workflow_ready: true
- priority: high
- execution_owner: codex

## Scope
- Trace the actual frontend data source for current rankings.
- Correct the consolidated `Today` section to use the live frontend-aligned source.
- Regenerate the posting package in a new dated folder without removing prior folders.
- Record validation evidence and resulting output paths.

## Acceptance Criteria
- The social posting package generator no longer derives `Today` from `stats/daily_net_return.json`.
- The generator uses the live per-day source that matches the frontend ranking feed.
- A new updated dated output folder is created for the corrected package run.
- Previous social posting package folders remain intact.

## Notes
- Initial investigation showed `fs/trade_viewer_api.py` merges per-product-type `_top20.json` files for the frontend `/api/top20` endpoint.
- Current generator still derives `Today` from `stats/daily_net_return.json`, which caused stale/incorrect consolidated output.

## Progress Log
- 2026-03-31 15:02:16: Task created in `workstream/100_todo`.
- 2026-03-31 15:03:28: Task moved to `workstream/200_inprogress`.
- 2026-03-31 15:04:55: Confirmed frontend `/api/top20` in `TradeApps/breakout/fs/trade_viewer_api.py` merges per-product-type live `_top20.json` files for the requested date.
- 2026-03-31 15:05:10: Patched `TradeApps/breakout/fs/tools/social_posting_package/generate_posting_package.py` so consolidated `Today` is sourced from:
  - `TradeApps/breakout/fs/json/live/forex/2026-03-31/_top20.json`
  - `TradeApps/breakout/fs/json/live/indices/2026-03-31/_top20.json`
  - `TradeApps/breakout/fs/json/live/metals/2026-03-31/_top20.json`
  - `TradeApps/breakout/fs/json/live/energy/2026-03-31/_top20.json`
- 2026-03-31 15:05:10: Weekly section intentionally left on `stats/daily_net_return.json` because it provides the week-to-date totals used by the package.
- 2026-03-31 15:05:10: Regenerated output:
  - `TradeApps/breakout/fs/json/live/social_posting_package/2026-03-31/top5_weekly_posting_package.json`
  - `TradeApps/breakout/fs/json/live/social_posting_package/2026-03-31/top5_weekly_posting_package.md`

## Validation
- Command:
  - `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Result:
  - JSON package written successfully to dated output folder `2026-03-31`
  - Markdown package written successfully to dated output folder `2026-03-31`
- Verified:
  - Consolidated `Today` no longer uses `stats/daily_net_return.json`
  - Previous dated folders remain present
  - Consolidated draft now separates live `Today` values from weekly totals

## Current Output Snapshot
```text
Update at 2026-03-31 15:05

Today
1. NQ 3385
2. CL 2570
3. ES 2485
4. SI 1775
5. YM 1245

Weekly so far
1. SI 2490
2. NQ 2375
3. CL 2315
4. ES 1675
5. YM 1170

Full details to follow.
#StrategyWarehouse #FuturesTrading #AlgoTrading
```

## Open Point
- The corrected output now matches the frontend source family for `Today`, but may still differ from the user's manually curated expected product set/order. If the frontend view applies additional editorial filtering or a different aggregation rule, that rule still needs to be encoded separately.
