Priority: 2

# Source
- User request on 2026-03-02: create new codex_breakoutfs task to fix live net display of summarized net in trade bucket.
- Suspected regression after: 20260302_002553_codex_breakoutfs_validate_leader_change_ltrade_eligibility_window.md.

# Task Summary
Investigate and fix regression where live net display of summarized net no longer appears in trade bucket after recent leadership eligibility changes.

# Context
- Affected UI(s): TradeApps/breakout/fs/trade_bucket.html (and DB parity check if shared logic applies).
- Prior related task: workstream/200_inprogress/20260302_002553_breakoutfs_validate_leader_change_ltrade_eligibility_window.md.
- Likely touchpoints: bucket summary net rendering, leader/l-trade filtering, and data merge paths.

# Scope
- Reproduce missing live net summarized display issue in trade bucket.
- Identify exact regression cause introduced by recent changes.
- Implement targeted fix without breaking leader eligibility gating.
- Validate summarized net appears correctly across expected buckets.
- Document commands, evidence, and outcomes in this lifecycle file.

# Implementation Log
- 2026-03-02 22:16:59: Task created in todo.

# Changes Made
- None yet.

# Validation
- Required:
  - Repro before fix showing missing live summarized net.
  - Verification after fix showing correct summarized net rendering.
  - Regression check confirming leader-takeover eligibility rule still enforced.

# Risks/Notes
- FS and DB trade bucket pages are near-parity; changes may need to be mirrored.

# Completion Status
- Todo
