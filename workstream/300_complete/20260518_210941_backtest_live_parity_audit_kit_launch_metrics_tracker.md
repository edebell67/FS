# Backtest Live Parity Audit Kit — Launch Metrics Tracker

## Task Type
Documentation / marketing operations artifact

## Destination
/mnt/c/Users/edebe/eds/products/backtest_live_parity_audit_kit/marketing/metrics_tracker.csv

## Dependency
Parent task t_20b21c7c created v0.2 package and launch assets.

## Plan
- Create a simple 60-day CSV tracker for launch activity and conversion metrics.
- Include fields for posts, DMs, Reddit discussions, creator contacts, page views, checkout clicks, sales by tier, revenue, objections, and next actions.
- Include target mix context for £3,173 revenue target without investment/trading-performance claims.
- Validate CSV structure and row count.

## Tests / Evidence Planned
- Parse CSV with Python csv module.
- Confirm required columns exist.
- Confirm 60 daily rows exist.

## Evidence
- Created `/mnt/c/Users/edebe/eds/products/backtest_live_parity_audit_kit/marketing/metrics_tracker.csv`.
- Tracker covers launch days 1–60 from 2026-05-18 to 2026-07-16.
- Target mix recorded in first row: 20 x £79, 5 x £199, 2 x £299 = £3,173.

## Implementation Log
- 2026-05-18 21:09 BST — Started task.
- 2026-05-18 21:10 BST — Generated CSV tracker in product marketing directory.
- 2026-05-18 21:10 BST — Validated CSV with Python csv module.

## Changes
- Added `products/backtest_live_parity_audit_kit/marketing/metrics_tracker.csv` with columns:
  - date
  - launch_day
  - posts
  - dms
  - reddit_discussions
  - creator_contacts
  - page_views
  - checkout_clicks
  - sales_79_gbp_tier
  - sales_199_gbp_tier
  - sales_299_gbp_tier
  - revenue_gbp
  - cumulative_revenue_gbp
  - target_mix_progress
  - objections
  - next_actions
  - notes

## Validation
Python CSV validation passed:

```json
{
  "row_count": 60,
  "column_count": 17,
  "missing_required_columns": [],
  "first_date": "2026-05-18",
  "last_date": "2026-07-16",
  "target_mix_cell": "Target totals: 20x79 + 5x199 + 2x299 = 3173 GBP"
}
```

## Risks
- Stripe/page analytics may need manual export or future automation depending on account permissions.
- CSV leaves daily metric cells blank intentionally so real launch data can be entered without fabricated numbers.

## Completion Status
Complete.
