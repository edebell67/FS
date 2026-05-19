# Task: Increase Font Size in Strategy Snapshots 15m

- **Source**: User request via Gemini CLI
- **Task Type**: standard
- **Destination Folder**: None
- **Dependency**: None

## Task Summary
Increase the font size of the main data elements in `fs/strategy_snapshots_15m.html` to improve readability and visual hierarchy.

## Context
- File: `C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_snapshots_15m.html`
- Current font sizes are relatively small (0.72rem - 0.82rem for most table data).

## Task Attributes
- standard

## Plan
- [x] 1. Increase Summary Card Net P&L font size.
  - Test: Check `.summary-card .net` in CSS. Expected: `1.8rem`.
  - Evidence: `Successfully modified file: C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_snapshots_15m.html. New value: font-size: 1.8rem;`
- [x] 2. Increase main Table font size.
  - Test: Check `table` in CSS. Expected: `0.9rem`.
  - Evidence: `Successfully modified file: C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_snapshots_15m.html. New value: font-size: 0.9rem;`
- [x] 3. Increase Table Header (`th`) font size.
  - Test: Check `th` in CSS. Expected: `0.8rem`.
  - Evidence: `Successfully modified file: C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_snapshots_15m.html. New value: font-size: 0.8rem;`
- [x] 4. Increase Group Pill and Snap Chip font sizes.
  - Test: Check `.group-pill` and `.snap-chip` in CSS. Expected: `0.85rem`.
  - Evidence: `Successfully modified file: C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_snapshots_15m.html. New values: .group-pill: 0.85rem, .snap-chip: 0.85rem`

## Evidence
### Objective-Delivery-Coverage: 100%
### Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\fs\strategy_snapshots_15m.html
  - Objective-Proved: All font size increases applied and verified via tool output.
  - Status: captured

## Implementation Log
- 2026-04-23 12:45: Initial task creation based on file inspection.
- 2026-04-23 12:50: Moved to in-progress and applied all 4 steps of font size increases.

## Changes Made
- Modified `fs/strategy_snapshots_15m.html`:
    - `.summary-card .net`: `1.55rem` -> `1.8rem`
    - `table`: `0.82rem` -> `0.9rem`
    - `th`: `0.72rem` -> `0.8rem`
    - `.group-pill`: `0.72rem` -> `0.85rem`
    - `.snap-chip`: `0.82rem` -> `0.85rem`

## Validation
- Verified each change against the `replace` tool's feedback.

## Risks/Notes
- Readability improved as requested.

## Completion Status
**COMPLETE** - 2026-04-23 12:52
