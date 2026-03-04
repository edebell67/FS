# Task Lifecycle

- Task: Enforce per-strategy Live Net as strict sum of that strategy L-trades
- Project: tradeapps
- Started: 2026-03-03 22:30:15
- Completed: 2026-03-03 22:31:52
- Status: complete

## Updates

### 2026-03-03 22:30:15
- Created lifecycle file in `100_todo`.
- Moved lifecycle file to `200_inprogress`.
- Identified existing fallback from per-strategy computed L-trade sum to `s.live_trade_net`.

### 2026-03-03 22:31:52
- Removed per-strategy `live_trade_net` fallback.
- Added `resolveStrategyParsedKey(...)` to derive strategy model/product key from object fields when `stratKey` is incomplete.
- Enforced strict per-strategy Live Net calculation from matched L-trades only.

## Validation

- `rg -n "stratLiveNet =|live_trade_net|resolveStrategyParsedKey\(|Strict rule" TradeApps/breakout/fs/trade_bucket.html`
  - Confirmed strict calculation path and helper presence.
- `Get-Content TradeApps/breakout/fs/trade_bucket.html | Select-Object -Skip 700 -First 70`
  - Verified strategy row rendering uses strict computed `stratLiveNet` from matched L-trades.
