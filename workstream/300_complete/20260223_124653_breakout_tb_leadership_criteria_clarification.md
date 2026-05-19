# Task Summary
Clarify Trade Bucket leadership criteria: net delta vs creation-point comparison.

## Context
- TradeApps/breakout/fs/trade_viewer_api.py

## Implementation Log
- Reviewed TB leader scoring and threshold functions.
- Verified which timestamp anchor is used in promotion/reconciliation logic.

## Changes Made
- No code changes. Clarification only.

## Validation
- _calculate_bucket_strat_perf uses current_total - baseline_at_or_before(start_time).
- _get_bucket_top2_stats ranks by that diff.
- _bucket_passes_threshold: top-second gap >= minimum_difference (or top_diff for single strategy).
- Promotion/reconcile paths call these with bucket.start_time.

## Risks/Notes
- chart_start_time and net_at_creation are not used for promotion decision in current logic.

## Completion Status
- Completed on 2026-02-23.
