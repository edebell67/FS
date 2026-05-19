# Task Lifecycle

- Task: Remove grid_live dependency from TB L-trade determination
- Project: tradeapps
- Started: 2026-03-04 10:51:55
- Completed: 2026-03-04 10:58:10
- Status: complete

## Updates

### 2026-03-04 10:51:55
- Created lifecycle file in `100_todo`.
- Identified dependency points where TB L-trade determination used `grid_live` leader-window logic.

### 2026-03-04 10:58:10
- Updated `fs/trade_bucket.html` and `DB/trade_bucket.html` so TB L-trades are determined from TB trade flags only (`is_live_trade`, `live_trade_executed`, `order_sent_net`, `order_sent_alt`).
- Removed `grid_live`-based leader-window usage in:
  - card-level `Live Trade Net` aggregation path,
  - `showBucketLTrades(...)` filtering path,
  - drilldown L-trade labeling/filtering path.
- Ensured bucket L-trade modal (`forceOnlyL`) labels all rows as L-TRADE in that dedicated view.
- Removed remaining DB `showDrilldown` lookup block that still called `buildLeaderWindowsMap`.

## Validation

- `rg -n "buildLeaderWindowsMap\(bucketName, gridRows\)|const leaderWindowsMap = buildLeaderWindowsMap\(String\(bucket.name|isTradeInLeaderWindow\(t, leaderWindowsMap\)|if \(!isLTradeFromFlags\(t\)\) return false;|forceOnlyL \|\| isTradeLTrade\(t\)" TradeApps/breakout/fs/trade_bucket.html TradeApps/breakout/DB/trade_bucket.html`
  - Confirmed no active `grid_live` leader-window calls remain in TB flow and flag-based gating is active.
