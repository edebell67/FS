# Strategy 15m Snapshot Persistence And Rollup

Source: User request, 2026-04-22
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Extend the 15-minute strategy snapshot workflow so the required summary data is persisted as an underscore-prefixed JSON file in each product-type daily folder, backfilled for all available forex daily folders, and viewable at either strategy-level rollup or product/strategy detail level.

## Context
Related existing work:
- `workstream/300_complete/20260422_154303_frequency_15min_cumulative_snapshot_viewer.md`
- `TradeApps/breakout/fs/strategy_snapshot_15m_generator.py`
- `TradeApps/breakout/fs/strategy_snapshots_15m.html`

Required storage convention:
- Store generated summary data under:
  - `TradeApps/breakout/fs/json/live/{product_type}/{current_date}/`
- File must be named with leading underscore:
  - `_{filename}.json`
- Current candidate artifact name from prior implementation:
  - `_strategy_snapshots_15m.json`

Required backfill:
- Generate the necessary snapshot summary data for `forex` for all daily folders available under:
  - `TradeApps/breakout/fs/json/live/forex/`

Required UI behavior:
- Default display should roll up by `strategy` level.
- Product-level detail must remain available.
- User should be able to switch between:
  - strategy rollup view
  - product/strategy detail view

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: `workstream/300_complete/20260422_154303_frequency_15min_cumulative_snapshot_viewer.md`

## Plan
- [x] 1. Confirm final artifact filename and underscore-prefixed storage path.
  - Test: Generated file path follows `json/live/{product_type}/{date}/_{filename}.json`.
  - Evidence: `_strategy_snapshots_15m.json` generated under every `TradeApps/breakout/fs/json/live/forex/YYYY-MM-DD/` folder.

- [x] 2. Update generator to support both row granularities.
  - Test: Artifact contains default strategy-level rollup rows and product/strategy detail rows, or contains enough normalized data for the UI to derive both without recomputing from raw trade files.
  - Evidence: Artifact snapshots contain `rows`, `strategy_rows`, and `product_rows`; `rows` aliases the default strategy rollup.

- [x] 3. Add forex all-date backfill command.
  - Test: Command iterates all `json/live/forex/YYYY-MM-DD` folders and writes the underscore-prefixed artifact into each folder.
  - Evidence: `python TradeApps/breakout/fs/strategy_snapshot_15m_generator.py --run-mode live --product-type forex --all-dates --newest-first --skip-existing` generated 36 dates and skipped 1 existing date.

- [x] 4. Update UI default view to strategy rollup.
  - Test: Opening the 15-minute snapshot page defaults to strategy-level rows, not product/strategy rows.
  - Evidence: `strategy_snapshots_15m.html` reads `payload.default_view` and defaults the `viewMode` selector to `strategy`.

- [x] 5. Preserve product-level drilldown/detail.
  - Test: UI control switches to product/strategy detail rows for the selected snapshot without losing sorting, group filtering, or selected snapshot time.
  - Evidence: `viewMode=product` renders `product_rows` and inserts the Product column; sorting and group filtering remain shared.

- [x] 6. Validate against available forex daily folders.
  - Test: Backfill reports number of forex day folders processed, number skipped, and generated artifact count; sample dates load in the UI.
  - Evidence: Validation count reported `daily_folders=37`, `with_artifact=37`, `missing=0`; sample dates parsed successfully.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `TradeApps/breakout/fs/json/live/forex/*/_strategy_snapshots_15m.json`
  - Objective-Proved: Underscore-prefixed 15-minute summary artifact is generated in each forex daily folder.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `TradeApps/breakout/fs/strategy_snapshots_15m.html`
  - Objective-Proved: UI defaults to strategy rollup and can switch to product-level detail.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m py_compile TradeApps/breakout/fs/strategy_snapshot_15m_generator.py`
  - Objective-Proved: Generator remains syntactically valid after rollup/backfill changes.
  - Status: captured

## Implementation Log
- 2026-04-22 17:30: Created backlog task from user request.
- 2026-04-22 17:34: Moved task to in-progress.
- 2026-04-22 17:40: Added strategy-level rollup rows, product-detail rows, underscore filename normalization, and all-date backfill options.
- 2026-04-22 17:45: Updated UI with strategy/product view selector and clearer missing-artifact errors.
- 2026-04-22 19:54: Backfilled all available live forex daily folders.

## Changes Made
- Updated `TradeApps/breakout/fs/strategy_snapshot_15m_generator.py`.
  - Adds `strategy_rows` rollup by strategy and preserves product/strategy detail in `product_rows`.
  - Keeps `rows` as the default strategy-level rows for backward-compatible UI loading.
  - Adds underscore-prefixed output filename normalization.
  - Adds `--all-dates`, `--skip-existing`, and `--newest-first`.
  - Uses a parallel raw-file loader so historical daily folders can be backfilled from detailed closed/open trade JSON.
- Updated `TradeApps/breakout/fs/strategy_snapshots_15m.html`.
  - Adds `View` selector with `strategy rollup` default and `product detail` option.
  - Product detail mode displays the Product column and reads `product_rows`.
  - Missing/non-JSON artifacts now produce a direct status message instead of a JSON parse error.
- Generated `_strategy_snapshots_15m.json` for all 37 available live forex daily folders.

## Validation
- `python -m py_compile TradeApps/breakout/fs/strategy_snapshot_15m_generator.py`
  - Result: pass.
- `python TradeApps/breakout/fs/strategy_snapshot_15m_generator.py --run-mode live --product-type forex --date 2026-04-22`
  - Result: `Wrote 77 snapshots ... (closed_with_exit=5580, open=183)`.
- `python TradeApps/breakout/fs/strategy_snapshot_15m_generator.py --run-mode live --product-type forex --all-dates --newest-first --skip-existing`
  - Result: `Backfill complete: generated=36 skipped=1`.
- Artifact count check:
  - Result: `daily_folders=37`, `with_artifact=37`, `missing=0`.
- Sample artifact sanity check:
  - `2026-03-16`: `snapshots=99`, `default=strategy`, `strategy_rows=192`, `product_rows=2304`.
  - `2026-04-01`: `snapshots=100`, `default=strategy`, `strategy_rows=201`, `product_rows=1870`.
  - `2026-04-22`: `snapshots=77`, `default=strategy`, `strategy_rows=122`, `product_rows=1163`.
- Static grep:
  - Result: UI and generator contain expected hooks for `viewMode`, `strategy_rows`, `product_rows`, `--all-dates`, `--skip-existing`, and `--newest-first`.

## Risks/Notes
- The interrupted prior on-demand-loading task is separate from this persistence/backfill/rollup task.
- Backfill over all forex folders is still IO-heavy because archive subfolders contain hundreds of thousands of `*_cl*.json` files, but it is now resumable with `--skip-existing`.
- Group summaries are based on strategy rollup rows so the UI default summary aligns with the default strategy-level view.

## Completion Status
Status: Complete
Created: 2026-04-22 17:30
Completed: 2026-04-22 19:56
