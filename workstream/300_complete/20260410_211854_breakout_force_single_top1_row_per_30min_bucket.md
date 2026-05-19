# Task: Force Single #1 Row Per 30-Minute Bucket

Source: User request on 2026-04-10 to select only one `#1` row every 30 minutes and use the first row when multiple rows tie on top `cum_total_net`.

Task Type: implementation

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Update the weekly summary-net generator so each 30-minute bucket has exactly one `is_1_by_total_net:true` row per `product_type`, using the first row in the bucket output order as the tie-breaker.

## 2026-04-10 21:18:54 Execution

Implemented in:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py`

Rule applied:
- Rank rows by top `cum_total_net` within each `{product_type, 30-minute bucket}`.
- If multiple rows tie at the top, keep only the first row in the bucket output order.
- Bucket output order remains sorted by `(product, strategy)`.

## 2026-04-10 21:18:55 Validation

Commands run:
- `python -m pytest TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py -q`
- Regenerated `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-06_summary_net_30m.json`

Results:
- Test passed: `1 passed`
- Midnight bucket `2026-04-06T00:00:00` now has exactly one `true` row:
- `2026-04-06T00:00:00 forex GBPAUD_C breakout_2_tp20.0_sl10.0 180.00 0.00 180.00 true`
- JSON artifacts refreshed successfully.
- Existing TXT export file could not be overwritten because it is locked by another process:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-06_summary_net_30m_top1_true.txt`
