# Source
- User request on 2026-03-01: check C:\Users\edebe\eds\TradeApps\breakout\fs\trade_bucket.html so that when a strategy becomes new leader, only trades entered after leadership start are eligible for l-trade consideration.
- User follow-up on 2026-03-01: apply the same change to the DB version and keep it in this same task.

# Task Summary
Validate and enforce leader-change eligibility gating in both FS and DB trade bucket UIs: trades with `entry_time` before strategy leadership start must be excluded from l-trade eligibility.

# Context
- UI files:
  - `TradeApps/breakout/fs/trade_bucket.html`
  - `TradeApps/breakout/DB/trade_bucket.html`
- Likely related logic: API/runtime trade filtering in fs/DB strategy selection and trade-bucket computation paths.
- Rule to enforce: `trade.entry_time >= strategy_leader_since` for l-trade consideration.

# Scope
- Identify current leader detection and l-trade eligibility flow.
- Confirm whether historical pre-leadership trades are currently included.
- Implement/adjust gating so only post-leadership entries are eligible in both FS and DB UI variants.
- Validate behavior with targeted scenario checks (leader flip with existing open/history trades).
- Document evidence and outcomes in this lifecycle file.

# Implementation Log
- 2026-03-01 00:25:53: Task created in todo.
- 2026-03-01 15:50: Identified existing logic in both `fs/trade_bucket.html` and `DB/trade_bucket.html` that intentionally did not strictly enforce `leaderTakeoverMs` for leader strategy rows.
- 2026-03-01 15:52: Patched both files to enforce leader takeover boundary for leader rows:
  - `if (isLeaderTrade && leaderTakeoverMs && entryMs && entryMs < leaderTakeoverMs) return false;`
- 2026-03-01 15:53: Verified both files contain the new guard at line 1235.

# Changes Made
- Updated: `TradeApps/breakout/fs/trade_bucket.html`
  - Added hard gate excluding leader trades entered before `leaderTakeoverMs`.
- Updated: `TradeApps/breakout/DB/trade_bucket.html`
  - Added the same hard gate for DB version.
- Updated inline comments to reflect that leader rows are now takeover-time gated.

# Validation
- Static validation:
  - `rg -n "isLeaderTrade && leaderTakeoverMs" TradeApps/breakout/fs/trade_bucket.html TradeApps/breakout/DB/trade_bucket.html`
  - Result:
    - `TradeApps\\breakout\\fs\\trade_bucket.html:1235`
    - `TradeApps\\breakout\\DB\\trade_bucket.html:1235`
- Pending user verification:
  - Confirm in UI that pre-leadership leader trades are excluded.
  - Confirm post-leadership leader trades remain eligible.
  - Confirm behavior in both FS and DB pages.

# Risks/Notes
- Leadership timestamp source must be explicit and stable (UI-derived timestamps may differ from server time normalization).
- `leaderTakeoverMs` is derived from summary rows; missing/inaccurate takeover time upstream can affect eligibility boundaries.

# Completion Status
- Awaiting user verification (requested 2026-03-01 15:53).


# User Feedback
User Verified: FAIL
Details: The Live net col needs to show the sum of the net of trades that are indicated as l-trades in the drill down (i.e. related trades)...   this is not consitently showing the summary value