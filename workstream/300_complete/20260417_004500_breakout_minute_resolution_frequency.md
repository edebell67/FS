# Task: Implement Minute-Resolution Frequency Tracking (v7)

**Project:** breakout
**Task Type:** standard
**Destination Folder:** TradeApps/breakout/fs/tools/
**Dependency:** None

## Task Summary
Normalize the frequency calculation by resampling the session state at 1-minute intervals. This eliminates log-density bias and ensures `total_freq` represents actual time spent at the top (in minutes).

## Plan
- [x] 1. Implement a time-generator to iterate through the session in 1-minute increments.
- [x] 2. Use State Carry-Over to determine the leader at each minute mark.
- [x] 3. Award exactly 1 win point per minute to the #1 strategy (where Net >= 0).
- [x] 4. Aggregate wins into 10-minute buckets (`chunk_freq` range: 0-10).
- [x] 5. Calculate `total_freq` as the running sum of minute wins.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-16\_leadership_timeline.json`
  - Objective-Proved: `total_freq` values now reflect minutes at top (e.g., ~480 for 8 hours).
  - Status: captured

## Completion Status
**In Progress**
