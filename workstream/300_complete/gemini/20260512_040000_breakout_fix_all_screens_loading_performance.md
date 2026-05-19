# Task: Fix Loading Performance for All Sidebar Screens

**Task Type:** Bug Fix / Performance
**Project:** breakout
**Created:** 2026-05-12 04:00:00

## Task Summary

Loading performance has deteriorated for multiple screens accessible from the sidebar menu. Audit all screens and ensure instant data load for each.

## Dependency

- 20260512_033617_breakout_fix_multi_chart_slow_loading (pattern established)

## Plan

1. [ ] List all screens available from sidebar menu
2. [ ] Profile each screen's loading time
3. [ ] Identify common bottlenecks:
   - Sequential API calls
   - Redundant data fetches
   - Large payload processing
   - DOM rendering delays
4. [ ] Apply optimization patterns:
   - Parallelize API calls with Promise.all()
   - Remove redundant fetches
   - Add loading state for perceived performance
   - Consider data caching where appropriate
5. [ ] Test and verify each screen
6. [ ] Document changes per screen

## Screens to Audit

Based on sidebar.html and fs directory:
- [ ] multi_chart.html (DONE - see prior task)
- [ ] trade_viewer.html
- [ ] realtime_stats.html
- [ ] strategy_performance.html
- [ ] lead_lag_snapshots.html
- [ ] trade_bucket.html
- [ ] weekly_performance.html
- [ ] execution_center.html
- [ ] frequency_explorer.html
- [ ] activations_explorer.html
- [ ] live_trades.html
- [ ] ai_picker.html
- [ ] top10_history.html
- [ ] portfolio_treemap.html

## Evidence

- Objective-Delivery-Coverage: 0%
- Before/after load time measurements per screen

## Implementation Log

- 2026-05-12 04:00: Task created

## Risks/Notes

- Large scope - may need to be split into multiple tasks
- Some screens may require API-side optimizations
- Pattern from multi_chart fix should be reusable
