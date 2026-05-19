# Task: Fix Trade Bucket Product Type Sync And Reconcile

Source: User request on 2026-04-12 to create a task and fix the Trade Bucket product-type bug.

Task Type: bugfix

Task Attributes:
- priority: high
- execution_owner: codex
- workflow_ready: true
- ui_task: false

## Task Summary
Fix Trade Bucket live-promotion and reconciliation so bucket leader selection, summary reads, and grid-live sync all use the correct `product_type`-scoped day folders.

## Validation Plan
- Patch bucket sync to carry `product_type` through summary resolution and grid sync.
- Patch reconciliation to load and reconcile buckets per product type instead of default-only scope.
- Add a regression test covering multiple product types with different leaders.
- Run the focused test suite for the new bugfix.

## Execution Log
- 2026-04-12 22:22 Started implementation review in `TradeApps/breakout/fs/trade_viewer_api.py` for `_sync_bucket_to_grid_live(...)`, `_reconcile_active_buckets(...)`, and Trade Bucket update/delete/remove-all endpoints.
- 2026-04-12 22:28 Patched `_sync_bucket_to_grid_live(...)` to accept `product_type` and resolve `_summary_net.json` from the matching product-type day folder instead of default-only scope.
- 2026-04-12 22:31 Patched `_reconcile_active_buckets(...)` to iterate configured product types, enforce caps per product type bucket file, and reconcile leaders against the matching product-type summary data.
- 2026-04-12 22:33 Patched Trade Bucket update/delete/remove-all call sites to pass `product_type` through grid-live sync and stale-entry removal paths.
- 2026-04-12 22:37 Added regression test `test_trade_bucket_sync_uses_bucket_product_type_for_summary` in `TradeApps/breakout/fs/tests/test_weekly_auto_promote_activation_api.py` to prove an `indices` bucket promotes the `indices` leader rather than a `forex` leader.

## Validation Results
- Command: `python -m pytest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_weekly_auto_promote_activation_api.py -q`
- Result: `3 passed`

## Outcome
- Trade Bucket grid-live promotion is now product-type-safe.
- Trade Bucket reconciliation now respects product-type bucket files and matching `_summary_net.json` inputs.
- Non-default product types no longer risk promoting leaders from the wrong summary scope.
