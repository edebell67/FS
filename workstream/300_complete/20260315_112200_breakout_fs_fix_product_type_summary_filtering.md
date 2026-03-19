# Breakout FS Fix Product Type Summary Filtering

## Metadata
- Project: breakout
- Task: fix product type summary filtering in performance screens
- Status: Complete
- Owner: Codex
- Started: 2026-03-15 11:22:00

## Request
When a product type such as `crypto` is selected in the performance screen, the data shown must only come from that product-type path. Current evidence shows `_summary_net.json` under `json/sim/crypto/<date>` still contains forex products.

## Plan
1. Update summary generation so each product-type day folder only aggregates trades matching that folder's product type.
2. Validate the generated summary/top20 payloads with a focused fixture test.
3. Document the fix and leave the task open only if live verification is still needed.

## Execution Log
### 2026-03-15 11:22:00
- Created lifecycle record after confirming `json/sim/crypto/2026-03-15/_summary_net.json` contains forex rows.
- Patching `summary_net_generator.py` to filter by target folder product type.

### 2026-03-15 11:30:00
- Updated `TradeApps/breakout/fs/summary_net_generator.py` so per-folder summary generation now filters trades by the target folder product type.
- Added regression test `tests/test_breakout_fs_summary_product_type_filter.py` covering a mixed-product input folder under `json/sim/crypto/<date>`.
- Validation passed locally, but the live `json/sim/crypto/2026-03-15/_summary_net.json` file is still stale and needs regeneration by the running summary generator process.

### 2026-03-15 11:42:00
- Reproduced an additional runtime bug: `SummaryGenerator` cache state was keyed only by `(mode, date)`, so one generator instance processing multiple product-type folders for the same date contaminated later outputs.
- Patched `TradeApps/breakout/fs/summary_net_generator.py` to scope closed-cache, totals, trade index, and init state by target folder.
- Strengthened `tests/test_breakout_fs_summary_product_type_filter.py` to process both `forex` and `crypto` folders for the same date in one generator instance.
- Regenerated `TradeApps/breakout/fs/json/sim/crypto/2026-03-15`, but the on-disk `_summary_net.json` was overwritten back to mixed-product output by an older long-running `summary_net_generator.py` process.
- Verified the patched generator itself is correct by inspecting in-memory totals after `process_date(...)`; accepted products were only `BTC, ETH, SOL, XRP`.

### 2026-03-15 11:53:00
- Stopped the stale resident `summary_net_generator.py` process (old lock PID `22536`) and started a fresh patched instance (new lock PID `36032`).
- Regenerated `TradeApps/breakout/fs/json/sim/crypto/2026-03-15`.
- Verified on-disk outputs after regeneration:
  - `_summary_net.json` products: `BTC, ETH, SOL, XRP`
  - `_top20.json` products: `BTC, ETH, SOL, XRP`
- Live operational issue is resolved for the target crypto summary folder.

## Validation
```powershell
python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\summary_net_generator.py C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py
pytest C:\Users\edebe\eds\tests\test_breakout_fs_summary_product_type_filter.py C:\Users\edebe\eds\tests\test_breakout_fs_json_layout.py
python C:\Users\edebe\eds\TradeApps\breakout\fs\generate_historical_summary.py C:\Users\edebe\eds\TradeApps\breakout\fs\json\sim\crypto\2026-03-15 sim 2026-03-15
```

## Result
- `8 passed in 0.40s`
- Code fix is complete, including cache isolation across product-type folders.
- Resident generator restarted successfully with patched code.
- Live verification passed for `TradeApps/breakout/fs/json/sim/crypto/2026-03-15`.
