# Workstream Task: Trade Bucket Metric Display

## Source
Created based on user request to fix duplicate metric displays on 2026-03-08.
Reference plan: `C:\Users\edebe\eds\plans\20260308_2137_V20260308_2137_trade_bucket_metric_display.md`

## Task Summary
Add metric identifiers (Buy, Sell, Alt, Net) to the Trade Buckets UI. Instead of grouping identical strategy names that track different metrics into indistinguishable rows on a Trade Bucket card, properly tag them with suffixes e.g., `[B]`, `[S]`, `[A]`, or `[N]` so the user can see exactly which line mapped to which metric. Modify the chart saving mechanism to encode the metric.

## Context
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart.js`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart_v2.js`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\multi_chart_v3.js`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html`
- `C:\Users\edebe\eds\DataInsights\src\Constants.py`

## Plan
- [x] 1. Identify where `saveToBucket()` runs and how it constructs the `strategies` payload array. Update logic across `multi_chart*.js` files to pass the active metric alongside the key (e.g., `"strategy | product | metric"`).
  - [x] Test: Check that `saveToBucket` payloads look like `["breakout | GBPUSD_C | buy_net"]` instead of just `"breakout | GBPUSD_C"`.
  - Evidence: `rg -n "strategiesToSave = overlays\\.map" TradeApps\breakout\fs\multi_chart.js TradeApps\breakout\fs\multi_chart_v2.js TradeApps\breakout\fs\multi_chart_v3.js` confirmed metric-appending save logic at `multi_chart.js:1593`, `multi_chart_v2.js:1029`, and `multi_chart_v3.js:1016`.
- [ ] 2. Refactor `trade_bucket.html` to parse this 3-part key structure when building display strings, appending a visual badge (e.g., ` [B]`) for `buy_net`, ` [S]` for `sell_net`, ` [A]` for `alt_net`, and ` [N]` for `net` (or generic null).
  - [ ] Test: UI verification of Trade Bucket card rendering.
  - Evidence: Technical prep complete. `trade_bucket.html` now contains `normalizeBucketMetric`, `getMetricBadge`, and `parseBucketStrategy` at lines `1135`, `1143`, and `1162`, and row rendering now appends the badge at line `751`. Manual browser verification still pending.
- [ ] 3. Ensure Trade Drilldown and `bucketLTrades` filtering matches underlying trades correctly by stripping off the `| metric` component when matching string names.
  - [ ] Test: Click on a metric row to ensure drilldown returns only trades for the parent strategy.
  - Evidence: Technical prep complete. `parseBucketKey()` now reads the third segment but still matches trades on normalized model/product only, and `showDrilldown()` explicitly ignores the metric segment for trade lookup at line `1086`. Manual click-path verification still pending.
- [x] 4. Increment version number in `Constants.py` to `V20260308_2137`.
  - [x] Test: Verify the `VERSION` constant is now `"V20260308_2137"`.
  - Evidence: `rg -n "V20260308_2137" DataInsights\src\Constants.py` returned `DataInsights\src\Constants.py:2`.

## Implementation Log
- **2026-03-08 21:38**: Generated formal workstream task and plan per user request.
- **2026-03-08 22:xx**: Moved lifecycle file from `workstream/100_todo` to `workstream/200_inprogress` per mandatory lifecycle process before starting implementation.
- **2026-03-08 22:xx**: Confirmed `multi_chart.js` already contained metric-appending bucket save logic from partial prior work; aligned `multi_chart_v2.js` and `multi_chart_v3.js` to save `strategy | product | metric`.
- **2026-03-08 22:xx**: Updated `trade_bucket.html` parsing to normalize a third metric segment, render `[B]/[S]/[A]/[N]` tags, and preserve drilldown/L-trade matching against strategy/product only.
- **2026-03-08 22:xx**: Updated `DataInsights/src/Constants.py` to `V20260308_2137`.
- **2026-03-08 22:xx**: Performed static validation with `rg`; browser verification still required for completion.
- **2026-03-09 00:xx**: User verification failed. Reported symptom: bucket rows showed `[N]` only, which indicated the metric was not surviving persistence from `multi_chart*` into the stored trade bucket payload.
- **2026-03-09 00:xx**: Traced root cause to `TradeApps\breakout\DB\trade_viewer_api.py` `create_trade_bucket()`, which converted string strategy entries into objects with `key` only and dropped the third metric component.
- **2026-03-09 00:xx**: Patched backend trade bucket creation to split `"strategy | product | metric"` into `{ key: "strategy | product", metric: "<metric>" }` and patched `multi_chart.js`, `multi_chart_v2.js`, and `multi_chart_v3.js` bucket reload paths to prefer `s.metric` over the global selector when reopening saved buckets.
- **2026-03-09 00:xx**: User reported the save-to-TB flow still appeared broken and bucket rows still showed `[N]` only. Root cause was that the live UI is served from `TradeApps\breakout\DB\*`, while earlier UI patches had been applied only to `TradeApps\breakout\fs\*`.
- **2026-03-09 00:xx**: Patched the active `DB` frontend files (`multi_chart.js`, `multi_chart_v2.js`, `multi_chart_v3.js`, `trade_bucket.html`) so the live UI now appends metric during save, preserves stored `s.metric` on bucket reload, renders metric badges, and ignores the metric segment during drilldown lookup.
- **2026-03-09 00:xx**: User reported that a single click on the save button did nothing and a double-click opened trade drilldown. Root cause was event bubbling from the save button into the chart card's `ondblclick` handler.
- **2026-03-09 00:xx**: Patched active `DB` multi-chart save buttons to use `type="button"` plus `event.preventDefault(); event.stopPropagation();` before calling `saveToBucket(...)`.
- **2026-03-09 00:xx**: Browser console showed `bucketName is not defined` from `multi_chart.js?v=V20260126_1245`, but the on-disk patched file no longer matched that line mapping. Root cause was stale hardcoded asset version strings in the active `DB` HTML pages, causing the browser to keep loading outdated JS.
- **2026-03-09 00:xx**: Updated `DB/multi_chart.html`, `DB/multi_chart_v2.html`, and `DB/multi_chart_v3.html` script querystrings to `V20260308_2137` to force cache invalidation onto the patched JS files.

## Changes Made
- `TradeApps\breakout\fs\multi_chart_v2.js`
  - Updated `saveToBucket()` so each saved strategy key includes the overlay metric as a third `|`-delimited segment.
  - Updated bucket reload to use persisted `s.metric` when present.
- `TradeApps\breakout\fs\multi_chart_v3.js`
  - Updated `saveToBucket()` so each saved strategy key includes the overlay metric as a third `|`-delimited segment.
  - Updated bucket reload to use persisted `s.metric` when present.
- `TradeApps\breakout\fs\multi_chart.js`
  - Updated bucket reload to use persisted `s.metric` when present.
- `TradeApps\breakout\fs\trade_bucket.html`
  - Added metric normalization helper for old/new metric names.
  - Added badge-mapping helper to render `[B]`, `[S]`, `[A]`, or `[N]`.
  - Added strategy parsing helper so both string buckets and object-backed buckets can expose metric-aware display text.
  - Updated strategy row rendering to append the metric badge to the displayed strategy label.
  - Clarified drilldown parsing to ignore the metric segment for API lookup so trade matching remains strategy/product based.
- `TradeApps\breakout\DB\trade_viewer_api.py`
  - Fixed trade bucket creation so legacy string payload entries preserve the metric explicitly in stored bucket strategy objects instead of dropping it.
- `TradeApps\breakout\DB\multi_chart.js`
  - Updated active save-to-bucket flow to append metric in the persisted strategy payload.
  - Updated active bucket reload path to use persisted `s.metric` when present.
  - Hardened the save button click handler to stop bubbling into the card drilldown handler.
- `TradeApps\breakout\DB\multi_chart_v2.js`
  - Updated active save-to-bucket flow to append metric in the persisted strategy payload.
  - Updated active bucket reload path to use persisted `s.metric` when present.
  - Hardened the save button click handler to stop bubbling into the card drilldown handler.
- `TradeApps\breakout\DB\multi_chart_v3.js`
  - Updated active save-to-bucket flow to append metric in the persisted strategy payload.
  - Updated active bucket reload path to use persisted `s.metric` when present.
  - Hardened the save button click handler to stop bubbling into the card drilldown handler.
- `TradeApps\breakout\DB\trade_bucket.html`
  - Added active bucket-page metric parsing, badge rendering, and strategy parsing helpers.
  - Updated active bucket-page row rendering to show `[B]/[S]/[A]/[N]`.
  - Updated active drilldown parsing comments/behavior to ignore metric for trade lookup.
- `TradeApps\breakout\DB\multi_chart.html`
  - Updated chart script asset version querystring to force browser reload of patched JS.
- `TradeApps\breakout\DB\multi_chart_v2.html`
  - Updated chart script asset version querystring to force browser reload of patched JS.
- `TradeApps\breakout\DB\multi_chart_v3.html`
  - Updated chart script asset version querystring to force browser reload of patched JS.
- `DataInsights\src\Constants.py`
  - Bumped `VERSION` to `V20260308_2137`.

## Validation
- `rg -n "strategiesToSave = overlays\\.map" TradeApps\breakout\fs\multi_chart.js TradeApps\breakout\fs\multi_chart_v2.js TradeApps\breakout\fs\multi_chart_v3.js`
  - Pass: metric-appending save logic confirmed in all three chart variants.
- `rg -n "normalizeBucketMetric|getMetricBadge|parseBucketStrategy|ignoring metric for trade lookup" TradeApps\breakout\fs\trade_bucket.html`
  - Pass: metric parsing, badge rendering, and drilldown handling hooks are present.
- `rg -n "V20260308_2137" DataInsights\src\Constants.py`
  - Pass: version constant updated correctly.
- `rg -n "'metric': metric|parts = \\[p\\.strip\\(\\) for p in str\\(strat\\)\\.split\\('\\|'\\)\\]|metric: s\\.metric \\|\\| globalMetric|metricPart = o\\.metric" TradeApps\breakout\DB\trade_viewer_api.py TradeApps\breakout\fs\multi_chart.js TradeApps\breakout\fs\multi_chart_v2.js TradeApps\breakout\fs\multi_chart_v3.js`
  - Pass: backend persistence now stores `metric`, and all three chart variants reload persisted bucket metrics instead of flattening back to the global metric.
- `rg -n "strategiesToSave = overlays\\.map|metric: s\\.metric \\|\\| globalMetric|normalizeBucketMetric|getMetricBadge|parseBucketStrategy|ignoring metric for trade lookup" TradeApps\breakout\DB\multi_chart.js TradeApps\breakout\DB\multi_chart_v2.js TradeApps\breakout\DB\multi_chart_v3.js TradeApps\breakout\DB\trade_bucket.html`
  - Pass: the active `DB` UI files now contain the metric save, reload, display, and drilldown compatibility changes that were previously missing.
- `rg -n "event\\.preventDefault\\(\\); event\\.stopPropagation\\(\\); saveToBucket" TradeApps\breakout\DB\multi_chart.js TradeApps\breakout\DB\multi_chart_v2.js TradeApps\breakout\DB\multi_chart_v3.js`
  - Pass: the active `DB` save buttons now explicitly consume clicks instead of bubbling into card-level double-click drilldown behavior.
- `Select-String -Path TradeApps\breakout\DB\multi_chart.html,TradeApps\breakout\DB\multi_chart_v2.html,TradeApps\breakout\DB\multi_chart_v3.html -Pattern "V20260308_2137"`
  - Pass: active chart HTML pages now reference the new script asset version, invalidating stale browser caches.
- User verification requested:
  - Pending. Need a fresh save from the active `DB` multi-chart UI, followed by Trade Bucket confirmation that rows now show the actual persisted metric tags rather than defaulting to `[N]`, and that clicking a tagged row still opens the correct drilldown trades.

## Risks/Notes
- Older buckets saved prior to this fix will default to having no 3rd `|` split, so they should gracefully fall back to the generic `[N]` or simply no tag.
- `git diff --name-only` only surfaced `DataInsights/src/Constants.py` in this worktree during validation, so file-content checks were used as the authoritative validation source for the frontend files.
- Existing buckets saved before the backend patch will still lack a stored `metric` field unless they already retained the third pipe segment in `key`; newly saved buckets should carry the metric explicitly.
- Prior verification failures can be explained by a codepath split between `fs` and `DB`; the active served UI needed the `DB` file patches.

## Completion Status
Awaiting user verification.


# User Feedback
User Verified: FAIL
Details: trade bucket updates with [N] only...   the metrics are not being transposed over from multi_charts..  Need to fix to display the actual metrics



# User Feedback
User Verified: PASS
