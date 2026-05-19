# Task: Implement Immutable Historical Timeline Logic (v10)

**Project:** breakout
**Task Type:** standard
**Destination Folder:** TradeApps/breakout/fs/tools/
**Dependency:** None

## Task Summary
Refactor the timeline generator to ensure historical data is immutable. The script must transition from a "Full Recalculation" model to an "Incremental Append" model. Once a 10-minute interval is finalized and written to disk, it must never be modified by subsequent runs.

## Context
- Tool: `TradeApps/breakout/fs/tools/dominance_leader_selector_final.py`
- Current Issue: Entire timeline is overwritten every loop, allowing history to change if logic or logs are updated.
- Requirement: Past data must be immutable.

## Plan
- [ ] 1. Update `process_product` to load existing `_leadership_timeline.json` and `_dominance_timeline.json` files if they exist.
- [ ] 2. Implement logic to identify the last processed checkpoint (The "Immutable Watermark").
- [ ] 3. Filter the processing loop to only evaluate checkpoints that are NEWER than the existing data.
- [ ] 4. Only finalize a checkpoint when the current wall-clock time has progressed at least 1 minute past the checkpoint end (Safety Buffer).
- [ ] 5. Merge new intervals with existing historical data and save.

## Evidence
- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: log_output
  - Artifact: TBD
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-04-16\_leadership_timeline.json`
  - Objective-Proved: Modification of the script logic does not change existing keys in the JSON file.
  - Status: planned

## Completion Status
**In Progress**
