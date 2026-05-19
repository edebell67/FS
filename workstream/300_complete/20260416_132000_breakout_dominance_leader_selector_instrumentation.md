# Task: Instrument Dominance Leader Selector with 10-Minute Frequency Chunks

**Project:** breakout
**Task Type:** standard
**Destination Folder:** TradeApps/breakout/fs/tools/
**Dependency:** None

## Task Summary
Enhance and verify the `dominance_leader_selector_final.py` tool to provide high-resolution frequency analysis of strategy performance. The tool must aggregate results into 10-minute intervals and track cumulative performance leaders throughout the session.

## Context
- Tool: `TradeApps/breakout/fs/tools/dominance_leader_selector_final.py`
- Source Data: `_summary_net.json` (nested strategy structure)
- Target Output: `TradeApps/breakout/fs/json/live/forex/leader_timeline.json`

## Plan
- [x] 1. Implement nested strategy structure parsing to handle multi-product strategy performance data.
  - Test: Run script against `_summary_net.json` and verify snapshot size > 0.
  - Evidence: `DEBUG: Snapshot size: 579` recorded in session.
- [x] 2. Implement 10-minute interval frequency aggregation starting from 01:00.
  - Test: Verify console output displays "HH:MM - HH:MM" chunks.
  - Evidence: Chunk output validated in session logs (e.g., 01:00 - 01:10).
- [x] 3. Implement cumulative frequency tracking to identify persistent session leaders.
  - Test: Verify "Cumulative Leaders" section appears in output for each chunk.
  - Evidence: Cumulative leader lists validated in session logs.
- [x] 4. Redirect JSON output to standard timeline path.
  - Test: Verify creation of `leader_timeline.json` at `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\`.
  - Evidence: `Full results saved to: C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\leader_timeline.json`

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: log_output
  - Artifact: Session console logs from 2026-04-16 13:10 to 13:25.
  - Objective-Proved: Tool correctly parses data, chunks by 10m, and calculates cumulative leaders.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\leader_timeline.json`
  - Objective-Proved: Final results are persisted for UI/downstream consumption.
  - Status: captured

## Implementation Log
- **2026-04-16 13:05**: Initial analysis of `dominance_leader_selector_final.py`.
- **2026-04-16 13:08**: Identified mismatch in JSON parsing logic for nested `strategies` key.
- **2026-04-16 13:12**: Fixed `get_snapshot` and `main` to correctly unwrap strategy/product rows.
- **2026-04-16 13:18**: Overwrote script with new 10-minute chunking logic and `datetime` handling.
- **2026-04-16 13:22**: Added cumulative frequency tracking and updated output path to `leader_timeline.json`.
- **2026-04-16 13:25**: Final verification run successful.

## Changes Made
- Modified `dominance_leader_selector_final.py`:
  - Updated `load_data` to handle nested `strategies` -> `product` -> `rows` structure.
  - Added 10-minute bucket calculation logic in `main`.
  - Added `cumulative_freq` dictionary to track persistent leaders.
  - Updated console output to show both Chunk and Cumulative leaders.
  - Set hardcoded `output_path` for `leader_timeline.json`.

## Validation
- Ran `python tools/dominance_leader_selector_final.py <path_to_summary>`
- Result: 0.0 diff between top strategies correctly handled; frequency counts successfully generated for 579 data points across multiple hours.

## Completion Status
**COMPLETE** - 2026-04-16 13:30
