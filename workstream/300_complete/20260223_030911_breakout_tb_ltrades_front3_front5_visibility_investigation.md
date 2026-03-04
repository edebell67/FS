# Task Summary
Investigate why L-trades shown from Trade Bucket UI do not look correct for front 3/5 winning scripts.

## Context
- TradeApps/breakout/fs/trade_bucket.html
- TradeApps/breakout/fs/trade_viewer_api.py

## Implementation Log
- Created lifecycle task file in workstream/100_todo.

## Changes Made
- Initialized task documentation.

## Validation
- N/A

## Risks/Notes
- None yet.

## Completion Status
- In progress.

## Implementation Log
- Traced TB L-trade card + modal flow in trade_bucket.html.
- Verified filtering logic in getBucketLTrades() and isLTradeFromFlags().
- Sampled latest live trade JSON metadata to validate flag prevalence and source tagging patterns.

## Changes Made
- No code changes. Investigation only.

## Validation
- Filter logic requires L-trade flags first:
  - trade_bucket.html:1139 (`if (!isLTradeFromFlags(t)) return false;`)
  - trade_bucket.html:953-958 (flags used: `is_live_trade`, `live_trade_executed`, `order_sent_net`, `order_sent_alt`)
- TB modal also scopes by bucket start time:
  - trade_bucket.html:1181 (`since=bucket.start_time`)
  - trade_bucket.html:1138 (exclude trades before bucket start)
- TB strategy matching is strict exact model+product:
  - trade_bucket.html:1119-1124
- Source fallback depends on bucket/source tagging:
  - trade_bucket.html:1148-1153
- Data sample (live 2026-02-23):
  - total trades: 8597
  - L-flagged trades: 1 (0.01%)
  - non-L: 8596
  - source_group mostly `breakout`, not bucket-specific tagging

## Risks/Notes
- Current UI behavior is expected from code but produces poor representation of "winning" scripts because:
  1. Almost all winning trades are filtered out as NON-L due to missing L flags.
  2. Older winners before bucket creation are excluded by `since=start_time` window.
  3. Front-3/front-5 ranking status is not used in `showBucketLTrades`; it only uses L-flag + bucket matching.

## Completion Status
- Completed on 2026-02-23. Root cause identified.
