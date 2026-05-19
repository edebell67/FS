# Task: Implement Joint Leadership Frequency Increment (v9)

**Project:** breakout
**Task Type:** standard
**Destination Folder:** TradeApps/breakout/fs/tools/
**Dependency:** None

## Task Summary
Modify the leadership logic to support joint #1 rankings. If multiple strategies share the exact same highest positive Net P&L at a checkpoint, all of them should have their `total_freq` incremented and their `chunk_freq` set to 1 for that interval.

## Context
- Tool: `TradeApps/breakout/fs/tools/dominance_leader_selector_final.py`
- Current logic: Only awards a win to the first strategy in the sorted list.
- Requirement: Award wins to all strategies with `net == max_net` (where `max_net >= 0`).

## Plan
- [x] 1. Update `process_product` to identify a list of `winners` (all strategies with Net == max_net).
- [x] 2. Modify the checkpoint loop to increment `total_wins_counter` for every strategy in the `winners` list.
- [x] 3. Update the `leadership_output` generator to set `chunk_freq = 1` for any strategy present in the current checkpoint's `winners` list.
- [x] 4. Restart background process and verify with Forex data (where ties are common).

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-16\_leadership_timeline.json`
  - Objective-Proved: Multiple strategies at the same Net value show `chunk_freq: 1` and matching `total_freq` increments.
  - Status: captured

## Implementation Log
- **2026-04-17 01:25**: Task created to support joint-leadership scoring.

## Completion Status
**In Progress**
