# Task: Implement Duration-Based Leadership Frequency (v8)

**Project:** breakout
**Task Type:** standard
**Destination Folder:** TradeApps/breakout/fs/tools/
**Dependency:** None

## Task Summary
Refactor the frequency calculation to measure the actual duration (in minutes) that a strategy holds the #1 spot. This replaces the "snapshot count" with "time-at-the-top," ensuring that the total frequency in any 10-minute window never exceeds 10.

## Context
- Tool: TradeApps/breakout/fs/tools/dominance_leader_selector_final.py
- Problem: 	otal_freq of 29 in a 10-minute window (impossible in time-units).
- Solution: Calculate time deltas between leadership changes.

## Plan
- [x] 1. Implement event-driven duration tracking: Calculate delta = current_timestamp - previous_timestamp.
- [x] 2. Award delta time to the strategy holding the max(net) where 
et >= 0.
- [x] 3. Convert total duration to decimal minutes for 	otal_freq and chunk_freq.
- [x] 4. Ensure interval checkpoints (10m) correctly slice the ongoing duration.
- [x] 5. Restart background process.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-16\_leadership_timeline.json
  - Objective-Proved: Sum of chunk_freq for all strategies in a 10-minute window equals exactly 10.
  - Status: captured

## Implementation Log
- **2026-04-17 01:30**: Refactored to Duration-Based Frequency. Verified sum of chunk_freq is 10.0 per bucket. Started background process with 300s loop.

## Completion Status
**Complete**

