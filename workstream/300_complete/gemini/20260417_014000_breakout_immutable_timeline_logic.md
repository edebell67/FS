# Task: Implement Full-Session State Rebuild for Immutability (v11)

**Project:** breakout
**Task Type:** standard
**Destination Folder:** TradeApps/breakout/fs/tools/
**Dependency:** None

## Task Summary
Refactor the leader selector to ensure that `total_freq` and `freq_rank` are calculated using the full session history (from 01:00 AM) while maintaining the immutability of previously written checkpoints. This ensures that strategies which stop updating are not lost from the leaderboard state.

## Plan
- [x] 1. Re-process the entire `_summary_net.json` from the start of the day (01:00 AM) in every loop to build a perfect state.
- [x] 2. Ensure `current_leaderboard` (Net P&L) and `total_wins_counter` (History) are persistent in memory during the rebuild.
- [x] 3. Only append NEW or non-finalized checkpoints to the `leadership_timeline` and `dominance_timeline` JSON files.
- [x] 4. Verify that strategies with a high `total_freq` (like GBPAUD_C) maintain their rank even if they haven't updated in the current 10-minute window.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-16\_leadership_timeline.json`
  - Objective-Proved: Historical win counts (total_freq) are preserved and carried forward into new checkpoints.
  - Status: captured

## Completion Status
**In Progress**
