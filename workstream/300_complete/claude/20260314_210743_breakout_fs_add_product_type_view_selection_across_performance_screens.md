# Breakout FS Add Product Type View Selection Across Performance Screens

## Objective
Add a `product_type` view selector to FS performance/read screens so the operator can choose which product-type dataset to view at a given time, instead of implicitly viewing only the default `forex` dataset.

## Problem
- The FS runtime can now create data under `json/{run_mode}/{product_type}/{date}`.
- Multiple product types may be produced simultaneously.
- Current read screens still assume a single implicit dataset view, which is effectively `forex` by default.
- This makes it hard to inspect `crypto`, `energy`, or other product-type data cleanly without mixing views.

## Scope
- Add a visible `product_type` selector to [strategy_performance.html](/C:/Users/edebe/eds/TradeApps/breakout/fs/strategy_performance.html).
- Extend the same selection model to other FS read screens that currently assume a single default dataset view.
- Pass the selected `product_type` through API requests where day-level files are resolved.
- Default the selector to `forex` when no explicit value is chosen.

## Expected Behavior
- User can choose one `product_type` at a time from configured values in `config.json`.
- All data shown on that screen should come from the selected `product_type` only.
- Existing behavior remains unchanged when `forex` is selected.
- Screens that aggregate date/mode data should no longer silently merge all product types unless explicitly intended.

## Candidate Screens
- `strategy_performance.html`
- `trade_viewer.html`
- `trade_bucket.html`
- `multi_chart.html`
- any other FS read/dashboard pages currently reading summary/top20/top_one/trade files without an explicit product-type filter

## Plan
1. Audit FS screens and API routes that currently resolve day-level files without a `product_type` parameter.
2. Define a shared UI pattern for `product_type` selection using values from `config.product_types`, defaulting to `config.product_type`.
3. Update API routes to accept optional `product_type` and restrict file resolution to that view when provided.
4. Update frontend pages to:
   - load available product types from config
   - persist the selected product type per page/session
   - include the selected product type in all relevant fetches
5. Verify that:
   - `forex` remains the default behavior
   - selecting another product type cleanly switches the dataset shown
   - screens do not leak mixed product-type data into a single view

## Validation
- Manual verification on `strategy_performance.html` first.
- Targeted verification on other affected screens after API/UI wiring.
- Confirm that switching between `forex` and another configured product type changes the underlying files being read.

## Chronology
- 2026-03-14 21:07 Europe/London: Task created to add explicit product-type view selection across FS read screens after live validation of the new runtime folder structure.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:30
