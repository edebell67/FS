# Task: Fix Weekly Summary Net #1 Rule to Use Top Row cum_total_net Per Bucket

Source: User clarification on 2026-04-10 that `#1` means the top `cum_total_net` at each 30-minute bucket and does not sum different strategies together.

Task Type: bugfix

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Correct the weekly summary-net generator so `is_1_by_total_net` is determined by the top row-level `cum_total_net` within each `{product_type, 30-minute bucket}` and not by summing multiple strategies for a product.

## Acceptance Criteria

- No summing across different strategies is used for `#1`.
- `is_1_by_total_net` is `true` only for row(s) tied at the maximum `cum_total_net` for that bucket and product type.
- Existing chained-week cumulative values remain intact.
- Filtered `top1_true` artifacts reflect the corrected row-level ranking rule.

## 2026-04-10 21:05:30 Execution

Implemented in:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py`

Correction applied:
- Removed cross-strategy summing for product-level ranking.
- `is_1_by_total_net` now evaluates each row directly against the maximum row-level `cum_total_net` in the same `{product_type, 30-minute bucket}`.
- Ties are preserved, so multiple rows can still be `true` when they share the same top `cum_total_net`.

## 2026-04-10 21:05:31 Validation

Commands run:
- `python -m pytest TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py -q`
- Regenerated `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-06_summary_net_30m.json`

Results:
- Test passed: `1 passed`
- Midnight bucket re-check for `2026-04-06T00:00:00` produced `5` true rows, all tied at `cum_total_net = 180.0`
- Correct midnight winners:
- `GBPAUD_C breakout_2_tp20.0_sl10.0`
- `GBPAUD_C breakout_2_tp20.0_sl20.0`
- `GBPAUD_C breakout_2_tp20.0_sl30.0`
- `GBPAUD_C breakout_2_tp20.0_sl5.0`
- `GBPAUD_C breakout_2_tp20.0_sl50.0`
