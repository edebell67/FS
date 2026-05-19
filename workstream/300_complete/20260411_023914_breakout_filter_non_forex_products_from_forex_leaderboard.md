# Task: Filter Non-Forex Products From Forex Leaderboard

Source: User report on 2026-04-11 that `SI` and `GC` appeared in the forex `top1` leaderboard despite not being forex products.

Task Type: bugfix

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Ensure the weekly forex summary-net leaderboard only includes products classified as forex by the breakout product-type mapping.

## 2026-04-11 02:39:14 Execution

Implemented in:
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`

Correction applied:
- Weekly summary generation now filters each product using the configured `product_type_by_product` mapping.
- Added `GC -> metals` to the config mapping.
- Added a defensive alias in the generator so `GC` resolves to metals when `GOLD -> metals` exists.

## 2026-04-11 02:39:15 Validation

Commands run:
- `python -m pytest TradeApps\breakout\fs\tests\test_aggregate_summary_net_30min.py -q`
- Regenerated `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\weekly\2026-04-06_summary_net_30m.json`

Results:
- Tests passed: `2 passed`
- Corrected forex `top1_true` JSON no longer contains `SI`
- Corrected forex `top1_true` JSON no longer contains `GC`
- Sample surviving products are forex-only: `CHF`, `EURAUD_C`, `EURNZD_C`, `GBPAUD_C`, `GBPEUR_C`
