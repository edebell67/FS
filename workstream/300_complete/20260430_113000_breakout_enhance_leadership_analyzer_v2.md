# Task: Enhance Leadership Change Analyzer with Takeover and Final Net

Source: User Request
Task Type: enhancement
Destination Folder: TradeApps/breakout/fs/
Dependency: None

## Task Summary
Update `leadership_change_analyzer.py` to support a configurable threshold and add "Takeover Net" and "Final Net" columns to the detailed report. The report will also be updated with clean ASCII table formatting.

## Requirements
- Support `--threshold` / `-t` argument (default $200).
- Add `Takeover Net` column (Net of new leader at time of change).
- Add `Final Net` column (Net of that strategy at the end of the day).
- Calculate `Diff` as `New Leader Net - Old Leader Net` at the takeover point.
- Implement ASCII table formatting for the report.
- Update version to `[V20260430_1130]`.

## Context
- File: `TradeApps/breakout/fs/leadership_change_analyzer.py`

## Plan
- [ ] 1. Move task to in-progress.
- [ ] 2. Update `main()` to handle `--threshold` and `--date` using `argparse`.
- [ ] 3. Update `calculate_strategy_totals_at_timestamps` to ensure we can easily retrieve final values.
- [ ] 4. Update `detect_leadership_changes` to include necessary data for the new columns.
- [ ] 5. Modify `generate_report` to render the ASCII table.
- [ ] 6. Update version and timestamp.
- [ ] 7. Verify output.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: log_output
  - Artifact: `python leadership_change_analyzer.py 2026-04-28 -t 200`
  - Objective-Proved: Report generated with Takeover and Final net columns in ASCII table format.
  - Status: captured

## Implementation Log
- 2026-04-30 11:30: Task created.
- 2026-04-30 11:35: Updated script with argparse, multi-day data retrieval, and ASCII table rendering.
- 2026-04-30 11:40: Verified output for 2026-04-28.

## Completion Status
**COMPLETE** - 2026-04-30 11:45
