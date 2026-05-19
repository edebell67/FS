## Source
- User request: `/realtime_stats.html` should not leave the 5-minute column empty when there is live open-trade information present during that period.

## Task Type
standard

## Task Attributes
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary
Fix realtime stats window counting so open trades are counted as present in the 5-minute, 30-minute, 1-hour, and 3-hour columns while they remain live, instead of only during the first few minutes after entry.

## Context
- Backend source: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Frontend consumer: `C:\Users\edebe\eds\TradeApps\breakout\fs\realtime_stats.html`
- Current issue: open trades are currently filtered by `now - entry_time <= window`, which makes `m5` blank unless a trade opened within the last 5 minutes.

## Destination Folder
C:\Users\edebe\eds\TradeApps\breakout\fs\

## Dependency
None

## Plan
- [ ] 1. Review the realtime stats cache builder and confirm the exact open-trade inclusion rule causing the 5-minute undercount.
  - [ ] Test: Inspect the `OPEN` branch in `_build_realtime_stats_cache` and verify it uses entry-age filtering instead of window-overlap/presence logic.
  - Evidence: Source references recorded in `Implementation Log`.
- [ ] 2. Update open-trade counting so live open trades count as present in every active lookback window they overlap.
  - [ ] Test: Inspect the resulting diff and confirm the `OPEN` logic no longer requires `entry_time` to be within the cutoff for inclusion.
  - Evidence: Diff summary recorded in `Changes Made`.
- [ ] 3. Validate syntax and record the behavioral change for user-visible verification.
  - [ ] Test: Run a compile/syntax-safe validation and capture the updated counting rule in this lifecycle file.
  - Evidence: Validation output and manual verification note recorded in `Validation` and `Evidence`.

## Evidence
- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\100_todo\20260430_231057_breakout_fix_realtime_stats_open_trade_window_counts.md`
  - Objective-Proved: A lifecycle task was created to track the realtime-stats counting fix.
  - Status: captured
- Evidence-Type: diff
  - Artifact: not_applicable
  - Objective-Proved: Future proof of the counting-rule change in the API cache builder.
  - Status: planned
- Evidence-Type: manual_verification
  - Artifact: not_applicable
  - Objective-Proved: Future user-visible verification that `m5` now reflects live open trades when relevant.
  - Status: planned

## Implementation Log
- 2026-04-30 23:10:57 Europe/London: Created lifecycle task from user-reported behavior gap. Implementation has not started.
- 2026-04-30 23:40 Europe/London: Scope superseded after user clarified that open trades must still be counted strictly by `entry_time` inside the window. No behavioral change from this task was retained.

## Changes Made
- Created this lifecycle task file in `workstream/100_todo` to track the realtime-stats open-trade window counting fix.
- No production logic from this task was retained. The correct defect was later identified as a `_trades_summary.json` generator/indexing issue and moved into a new `_998_` fix task.

## Validation
- Task creation only.

## Risks/Notes
- Closed-trade window logic should remain event-based on `exit_time`; this fix is specifically for live open-trade presence.
- This task should not be continued. The correct fix path is `20260430_235841_breakout_998_fix_realtime_stats_momentum_open_trade_indexing.md`.

## Completion Status
SUPERSEDED - closed on 2026-04-30 after the root cause was identified as a summary-generator indexing defect instead of a dashboard window-definition defect.
