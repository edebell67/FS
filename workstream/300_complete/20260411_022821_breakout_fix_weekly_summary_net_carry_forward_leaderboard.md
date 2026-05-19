# Task: Fix Weekly Summary Net Leaderboard to Carry Forward Latest Known Totals

Source: User clarification on 2026-04-11 that product/strategy rows compete continuously, so the current leader must remain `#1` until another row overtakes its cumulative weekly total.

Task Type: bugfix

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Correct the weekly summary-net winner stream so each 30-minute bucket ranks all product+strategy rows using their latest known cumulative weekly values as of that bucket, not only rows that emitted a fresh snapshot in that bucket.

## Acceptance Criteria

- The winner at each 30-minute bucket is chosen from the carried-forward state of all known rows.
- A prior leader remains `#1` when later buckets do not contain a higher cumulative total.
- The `top1_true` outputs contain exactly one winner row per 30-minute bucket.
- Validation demonstrates that a low fresh row cannot displace a higher carried-forward leader.

## 2026-04-11 02:28:21 Execution

Implemented in:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py`

Correction applied:
- `top1` selection now uses a carried-forward leaderboard state.
- At each 30-minute bucket, every known product+strategy competes using its latest known cumulative weekly total as of that bucket.
- The winner remains in place until another row exceeds it.
- The `top1_true` outputs now represent a real rolling leaderboard instead of bucket-local fresh-row comparisons.

## 2026-04-11 02:28:22 Validation

Commands run:
- `python -m pytest TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py -q`
- Regenerated `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-06_summary_net_30m.json`

Results:
- Test passed: `1 passed`
- The regression test confirms a leader with `100` remains `#1` at the next bucket even when a fresh competitor row is only `40`.
- Live file re-check across `2026-04-10T16:30:00`, `17:00:00`, `17:30:00`, and `18:00:00` now carries the same winner forward instead of switching to a low fresh row.

Note:
- The existing TXT export file was locked by another process during regeneration, so JSON outputs are the authoritative corrected artifacts for this run.
