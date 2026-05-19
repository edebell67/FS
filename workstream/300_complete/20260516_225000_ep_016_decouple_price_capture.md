# Task: EP_016 Decouple Price Capture into Independent Daemon
# Date: 2026-05-16 22:50
# Version: V20260516_2250

## Task Type
Infrastructure / Optimization

## Destination Folder
epics/ep_016_turning_point_pattern_engine/logic

## Dependency
20260516_221500_ep_016_live_logic_throttling_and_mid_price.md

## Plan
1. **Create Price Capture Daemon**:
    - [ ] Create `price_capture_daemon.py` to handle the `_price_capture.jsonl` file generation independently.
    - [ ] Implement robust error handling and directory management.
    - Evidence: `price_capture_daemon.py` exists.

2. **Refactor Live Analyzer**:
    - [ ] Remove `capture_snapshot` function and related variables from `price_frequency_pattern_analyzer_v2.py`.
    - [ ] Clean up redundant data-writing logic.
    - Evidence: Analyzer code is focused purely on signal processing and trading.

3. **Create Launcher**:
    - [ ] Create `run_price_capture_daemon.bat`.
    - Evidence: File exists.

4. **Update Documentation**:
    - [ ] Update `RESEARCH_JOURNAL.md` to reflect the new mandatory data capture infrastructure.
    - Evidence: Journal updated.

## Evidence Inventory
- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: false

## Implementation Log
- 2026-05-16 22:50: Task created to decouple price capture for improved reliability and to avoid file lock collisions when running multiple analyzers.

## Completion Status
**IN PROGRESS**
