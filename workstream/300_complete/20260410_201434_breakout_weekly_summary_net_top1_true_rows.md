# Task: Capture Weekly Summary Net Rows Where is_1_by_total_net Is True

Source: User request on 2026-04-10 to capture records from `2026-04-06_summary_net_30m.json` where `is_1_by_total_net:true` in order to model taking the trades of the strategies at `#1`.

Task Type: implementation

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Extend the weekly summary-net output so the generated weekly artifact also produces a filtered export containing only the rows where `is_1_by_total_net` is `true`.

## Objective
Create an explicit output for the weekly `#1` strategy-capture case so downstream modelling can use only the rows representing strategies attached to the product that is ranked `#1` by `cum_total_net` in each 30-minute bucket.

## Acceptance Criteria

- The weekly summary-net generation writes a filtered artifact containing only rows where `is_1_by_total_net` is `true`.
- The filtered artifact preserves the same row structure as the main weekly summary output.
- A plain-text export is also available in the requested line format for direct inspection or reuse.
- Validation confirms the filtered output is a strict subset of the source weekly summary output.

## 2026-04-10 20:14:34 Execution

Implemented in:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py`

Behavior added:
- Main weekly summary JSON now includes:
- `top1_rows`
- `top1_formatted_lines`
- Generator now also writes:
- `{week_start}_summary_net_30m_top1_true.json`
- `{week_start}_summary_net_30m_top1_true.txt`

Meaning:
- These filtered outputs keep only rows where `is_1_by_total_net` is `true`.
- This captures all strategy rows attached to the product that is ranked `#1` by `cum_total_net` for that 30-minute bucket.

## 2026-04-10 20:14:35 Validation

Commands run:
- `python -m pytest TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py -q`
- Regenerated live weekly forex summary output for the week containing `2026-04-10`

Results:
- Test passed: `1 passed`
- Base file rows: `20439`
- Filtered `top1_true` rows: `887`
- Filtered JSON exists and matched the inline `top1_rows` count.
- Filtered TXT exists and contains the requested plain-text line format.

Artifact paths:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-06_summary_net_30m.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-06_summary_net_30m_top1_true.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-06_summary_net_30m_top1_true.txt`
