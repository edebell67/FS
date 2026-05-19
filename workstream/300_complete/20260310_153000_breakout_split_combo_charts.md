# Workstream Task: Multi-Chart Split/Combo Charts & Metric Enforcement

## Source
User conversation on 2026-03-10 describing persistent trade-bucket metric tag issues, the desire for card-level split/combo toggles, and stricter metric-driven filtering for grid promotions/drilldowns (screenshots and logs referenced from the multi-chart panel view and trade-bucket console output).

## Task Summary
- Replace the net-only card view with a strict `s`/`c` toggle: `s` appears only when the card is currently total-net `[T]`, and `c` appears only when the card is currently the paired buy/sell `[B]/[S]` state.
- Keep buy and sell as two overlapping line charts on the same axis inside the same card; no separate split panels and no split/combo iconography.
- Propagate the correct metric metadata when workflow-generated charts or saved buckets are promoted to the grid, ensuring the trade-bucket display/headline metric matches what was on the card.
- When drilling into a trade bucket, limit the matched live trades (especially `l-trades`) to the direction implied by the `[B]/[S]/[N]` metric so that buy-only buckets only show buys, while `[N]` allows both.

## Context
- Multi-chart card rendering and action handling in `TradeApps/breakout/DB/multi_chart.js`, `multi_chart_v2.js`, and `multi_chart_v3.js` (split/combo control needs to live in the shared card chrome in each variant).
- Trade-bucket drilldown and strategy parsing logic in `TradeApps/breakout/DB/trade_bucket.html` (metric badges exist already but matching logic still allows every direction).
- The bucket creation API in `TradeApps/breakout/DB/trade_viewer_api.py` and the grid/live sync payloads so the persisted metric tags survive (earlier work already touched these files but we may need to double-check consistency with the new toggle).

## Plan
- [ ] Add a split/combo control to every multi-chart card (v1/v2/v3) that reads the current overlay set, toggles between net and buy/sell net datasets, and updates the button icon/tooltip accordingly.
- [ ] Implement helper routines that generate buy/sell overlays with shared axes, reusing color information if possible, and ensure `updateCharts()` is triggered after toggling.
- [ ] Extend the trade-bucket drilldown helpers to recognize `parsedStrategy.metric` and to enforce direction-specific matching (`tradeMatchesBucketStrategy` / `getBucketLTrades`), keeping `[N]` as the default both-direction fallback.
- [ ] Verify grid promotions/loaders keep the same metric metadata so that toggled cards still surface the appropriate `[B]/[S]/[N]` badge after a save/load round trip.

## Implementation Log
- **2026-03-10 16:55**: User rejected the first pass because it used an icon-style split toggle and loose state detection. Requirement clarified: visible button content must be literal `s` or `c`, and the control must only be shown in the exact `[T]` or `[B]/[S]` states.
- **2026-03-10 16:56**: Updated active `DB` multi-chart pages so the split control no longer renders an icon, now renders `s`/`c` text only, and hides itself for unsupported mixed-metric card states.

## Validation
- (Pending.)
