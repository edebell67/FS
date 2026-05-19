## Task

Investigate and fix missing daily summary values for forex in `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`, where the previous week view shows values only for the first day and `0.00` for most of the remaining week.

## Source

- User request in Codex thread on 2026-04-19.
- Attached Weekly Strategy Performance screenshot showing forex week `2026-04-13` to `2026-04-19` with populated Monday values and mostly zero/missing summaries for the rest of the week.

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

Fix the weekly performance aggregation or presentation path so prior-week forex data shows complete daily summaries across the full week instead of collapsing to one populated day with zeros for the remaining days.

## Context

- Target UI file: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Target API/backend path: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Current weekly API behavior:
  - `weekly_performance.html` fetches `/api/weekly_performance?product_type=...&target_date=...`
  - backend route writes/reads `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\<product_type>\stats\weekly\<week_start>.json`
  - backend uses `tools.aggregate_top_strategies.aggregate_for_product_type(...)` to generate/update the weekly artifact
- Visible symptom from screenshot:
  - forex selected
  - week range `2026-04-13` to `2026-04-19`
  - Monday has non-zero values
  - Tuesday through Sunday appear mostly as `0.00`
- Likely failure domains:
  - weekly aggregation logic producing incomplete daily rollups
  - stale or partial cached weekly stats artifact
  - date alignment/week-bound handling
  - forex source data availability or lookup path differences across the week
  - frontend rendering assumptions around absent day keys vs actual zero values

## Destination Folder

None

## Dependency

None

## Plan

- [x] 1. Inspect the weekly performance frontend, API route, and weekly aggregation code path to identify how day columns are sourced.
  - [x] Test: `rg -n "weekly_performance|aggregate_for_product_type|get_week_bounds|stats/weekly" C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py` returns the relevant rendering and aggregation sections.
  - Evidence: confirmed the page reads `/api/weekly_performance`, the route uses week-aligned cached files under `json/live/<product_type>/stats/weekly`, and the aggregation path reads daily `_trades_summary.json`.
- [x] 2. Inspect the generated weekly forex artifact for the affected week and compare it to underlying daily source data.
  - [x] Test: Read `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-13.json` and relevant per-day source files to determine whether the zeros originate in the aggregate artifact or in rendering.
  - Evidence: the weekly artifact had `last_update` on `2026-04-13` and only Monday populated, while `_trades_summary.json` existed with non-zero trade counts for `2026-04-14` through `2026-04-17`, proving the zeros were caused by a stale cached weekly artifact rather than missing source data or frontend rendering.
- [x] 3. Fix the aggregation and/or rendering path so prior-week forex summaries populate correctly across the full week.
  - [x] Test: Diff shows a targeted code change that addresses the identified root cause without regressing weekly caching behavior.
  - Evidence: added `_weekly_stats_artifact_is_stale(...)` in `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` and switched both weekly endpoints to refresh when the aligned week is in progress or when any underlying daily source file is newer than the cached weekly artifact.
- [x] 4. Regenerate or refresh the affected weekly artifact and verify the corrected week data.
  - [x] Test: The weekly stats output for forex week `2026-04-13` contains non-missing daily values where source data exists, and the API returns the corrected structure.
  - Evidence: regenerated `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-13.json` and `2026-04-13_summary_net_30m.json`; the refreshed weekly JSON now contains non-zero values for `2026-04-13` through `2026-04-17` and weekend zeros only.
- [x] 5. Validate the fix in the Weekly Performance UI, by source readback and, if practical, browser/manual verification against the affected week.
  - [x] Test: `python -c "import sys; sys.path.insert(0, r'C:\Users\edebe\eds\TradeApps\breakout\fs'); import trade_viewer_api as api; client=api.app.test_client(); resp=client.get('/api/weekly_performance?product_type=forex&target_date=2026-04-17'); print(resp.status_code); data=resp.get_json(); print(data['top_strategies'][0]['daily'])"` returns HTTP 200 with Tue-Fri populated.
  - Evidence: API validation passed and the returned weekly payload for forex week `2026-04-13` to `2026-04-19` shows populated weekdays instead of false zeros.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Objective-Proved: The root cause for missing prior-week forex summaries was fixed in code or artifact generation.
  - Status: complete
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-13.json`
  - Objective-Proved: The regenerated weekly forex stats artifact contains corrected day-level summary data.
  - Status: complete
- Evidence-Type: manual_verification
  - Artifact: Flask test-client request to `/api/weekly_performance?product_type=forex&target_date=2026-04-17`
  - Objective-Proved: The Weekly Performance screen for the affected forex week displays day summaries correctly.
  - Status: complete

## Implementation Log

### 2026-04-19 00:12:25

- Created backlog task for the missing forex weekly summary values shown in the Weekly Performance screenshot.

### 2026-04-19 00:24:30

- Confirmed the affected weekly file `json/live/forex/stats/weekly/2026-04-13.json` was stale: it had a `last_update` on Monday `2026-04-13` and zeros for the rest of the week despite daily `_trades_summary.json` inputs existing with non-zero trade counts on Tue-Fri.
- Patched `trade_viewer_api.py` to detect stale weekly artifacts by comparing cache timestamps against aligned-week source files and to always refresh an in-progress week.
- Regenerated the forex weekly artifacts for week `2026-04-13` and verified the API now returns populated weekday values for the previously missing days.

## Changes Made

- Updated `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` to refresh weekly cached artifacts when the current aligned week is still in progress or when source daily files are newer than the cache.
- Regenerated:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-13.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-13_summary_net_30m.json`

## Validation

- `rg -n "weekly_performance|aggregate_for_product_type|get_week_bounds|stats/weekly" C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py`
- `python -c "from tools.aggregate_top_strategies import aggregate_for_product_type, aggregate_summary_net_30min_for_product_type; from pathlib import Path; base=Path(r'C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly'); aggregate_for_product_type('forex', target_date='2026-04-13', output_file=base / '2026-04-13.json'); aggregate_summary_net_30min_for_product_type('forex', target_date='2026-04-13', output_file=base / '2026-04-13_summary_net_30m.json')"`
- `python -c "import json; p=r'C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-13.json'; data=json.load(open(p,'r',encoding='utf-8')); row=data['top_strategies'][0]; print(data['last_update']); print(row['strategy']); print(row['daily'])"`
- `python -c "import sys; sys.path.insert(0, r'C:\Users\edebe\eds\TradeApps\breakout\fs'); import trade_viewer_api as api; client=api.app.test_client(); resp=client.get('/api/weekly_performance?product_type=forex&target_date=2026-04-17'); print(resp.status_code); data=resp.get_json(); print(data['week_start'], data['week_end']); print(data['top_strategies'][0]['daily'])"`
- Result: API returned `200`, week `2026-04-13` to `2026-04-19`, and the leading strategy daily map now includes non-zero values for `2026-04-13` through `2026-04-17`; only `2026-04-18` and `2026-04-19` remain zero, which is consistent with empty weekend trade summaries.

## Risks/Notes

- Existing stale weekly artifacts for other product types or dates will self-heal on the next request because the API now compares cache mtimes to underlying source files.
- Browser verification was not run in a live headed session; validation used the regenerated artifact plus Flask test-client API checks.

## Completion Status

Complete - 2026-04-19 00:24:30
