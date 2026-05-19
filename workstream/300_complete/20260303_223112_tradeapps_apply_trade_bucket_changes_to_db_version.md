# Task Lifecycle

- Task: Apply trade_bucket leader-window and strict strategy live-net logic to DB version
- Project: tradeapps
- Started: 2026-03-03 22:31:12
- Completed: 2026-03-03 22:34:25
- Status: complete

## Updates

### 2026-03-03 22:31:12
- Created lifecycle file in `100_todo`.
- Located DB variant at `TradeApps/breakout/DB/trade_bucket.html`.
- Moved lifecycle file to `200_inprogress`.

### 2026-03-03 22:34:25
- Applied leader-window L-trade persistence logic to DB version (historical leader trades remain L-trades).
- Updated drilldown L-trade labeling/filtering to use flags OR leader-window membership.
- Enforced strict per-strategy Live Net as sum of matched L-trades only.
- Added strategy key resolver helper for robust matching when `stratKey` is incomplete.

## Validation

- `rg -n "lastDrilldownLeader|live_trade_net|resolveStrategyParsedKey|buildLeaderWindowsMap|isTradeInLeaderWindow|isTradeLTrade|leaderWindowsMap" TradeApps/breakout/DB/trade_bucket.html`
  - Confirmed new logic is present and old `live_trade_net` fallback removed from strategy calc path.
- `Get-Content TradeApps/breakout/DB/trade_bucket.html | Select-Object -Skip 700 -First 95`
  - Verified strict per-strategy Live Net computation from matched L-trades.
- `Get-Content TradeApps/breakout/DB/trade_bucket.html | Select-Object -Skip 960 -First 420`
  - Verified drilldown + bucket L-trade logic uses leader windows consistently.
