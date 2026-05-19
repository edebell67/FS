# Task: Implement Parallel Leadership and Dominance Timelines

**Project:** breakout
**Task Type:** standard
**Destination Folder:** TradeApps/breakout/fs/tools/
**Dependency:** None

## Task Summary
Refactor the leader selection tool to provide two distinct analytical outputs: "Dominance" (Session-wide consistency) and "Leadership" (Momentary P&L superiority). This ensures data captures both persistent performers and current market leaders as seen in the UI.

## Context
- Tool: `TradeApps/breakout/fs/tools/dominance_leader_selector_final.py`
- Current Output: `leader_timeline.json` (Frequency-based)
- Requirement: Rename to `dominance_timeline.json` and add `leadership_timeline.json` based on absolute Net P&L at checkpoints.

## Plan
- [ ] 1. Refactor `process_product` to track momentary absolute P&L leaders at each 10-minute checkpoint.
  - Test: Run script and verify `leadership_timeline.json` contains strategies with the highest Net at each timestamp.
  - Evidence: TBD
- [ ] 2. Rename existing output logic for frequency analysis.
  - Test: Verify `dominance_timeline.json` is created with cumulative frequency data.
  - Evidence: TBD
- [ ] 3. Update background loop to generate both files in parallel for all 5 product types.
  - Test: Check logs for successful parallel writes to both filenames.
  - Evidence: TBD

## Evidence
- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\{product}\dominance_timeline.json`
  - Objective-Proved: Consistency metrics are preserved under the new naming convention.
  - Status: planned
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\{product}\leadership_timeline.json`
  - Objective-Proved: Momentary P&L leadership matches UI observations.
  - Status: planned

## Implementation Log
- **2026-04-16 13:40**: Task created to resolve tally mismatch with UI.

## Completion Status
**In Progress**
