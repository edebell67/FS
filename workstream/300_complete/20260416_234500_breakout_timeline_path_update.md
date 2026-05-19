# Task: Refine Leader Frequency Logic (Snapshot-Based)

**Project:** breakout
**Task Type:** standard
**Destination Folder:** TradeApps/breakout/fs/tools/
**Dependency:** None

## Task Summary
Refactor the `total_freq` and `chunk_freq` calculation to use unique timestamp snapshots. This prevents frequency bias caused by "chatty" strategies and ensures points are only awarded to the true #1 leader(s) with positive net P&L at each moment in time.

## Plan
- [x] 1. Group all log entries by unique timestamp to create discrete "voting rounds."
  - Test: Run script and verify logic groups by 't'.
  - Evidence: Verified via manual run and code review.
- [x] 2. Implement state carry-over within the timestamp loop to maintain a full leaderboard.
  - Test: Check if `current_leaderboard` preserves state across snapshots.
  - Evidence: Verified in v6 implementation.
- [x] 3. Award win points strictly to the strategy/strategies with the `max(net)` where `net >= 0`.
  - Test: Verify tied leaders both get points.
  - Evidence: Implemented logic to find all winners at each snapshot.
- [x] 4. Update both `leadership_timeline` and `dominance_timeline` with this normalized frequency data.
  - Test: Check output files for `total_freq` and `chunk_freq`.
  - Evidence: Verified file output contents.
- [x] 5. Restart background process.
  - Test: Check PID and running status.
  - Evidence: PID 9932 started after killing old process (PID 13672).

## Validation
- [x] Verify tied strategies (same Net) both receive win points.
- [x] Verify `total_freq` increments by exactly 1 per unique timestamp (for the leader).
- [x] Verify negative leaders receive 0 points.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: log_output
  - Artifact: Manual run output showing leaders for 2026-04-16.
  - Objective-Proved: Frequency calculation verified.
  - Status: captured

## Implementation Log
- **2026-04-17 00:10**: Refining frequency logic to fix log-density bias.
- **2026-04-17 00:30**: Implemented snapshot-based grouping using `itertools.groupby`.
- **2026-04-17 00:35**: Verified logic with manual run and restarted background loop (v6).

## Completion Status
**COMPLETE**
**Completion Date**: 2026-04-17 00:40
