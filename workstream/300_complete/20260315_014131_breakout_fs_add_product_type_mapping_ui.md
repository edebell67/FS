# Breakout FS Add Product Type Mapping UI

## Objective
Add an operator-facing FS config UI for mapping products to `product_type`, so mappings can be maintained directly in the interface instead of editing raw JSON.

## Problem
- FS supports `product_type_by_product`, but the current config UI only exposes it as raw JSON.
- Operators need a clearer mapping workflow.
- The UI should support assigning each product to the correct `product_type` without relying on manual JSON edits.

## Required Capability
Support one of these operator-friendly patterns:
- per-product assignment:
  - show each product with a `product_type` selector beside it
- per-type allocation buckets/windows:
  - show each `product_type` as a bucket and allocate products into it

The implementation can choose the cleaner/better option, but it must persist to `config.product_type_by_product`.

## Scope
- Update the FS config UI in `trade_viewer.html`.
- Load products from `config.trade_products`.
- Load product types from `config.product_types`.
- Save the resulting mapping into `config.product_type_by_product`.
- Keep the raw JSON contract intact for runtime compatibility.

## Plan
1. Review the current config UI and identify where the mapping editor should live.
2. Choose the operator-facing interaction model:
   - per-product dropdowns
   - or per-type allocation buckets
3. Implement the UI so products can be assigned clearly and saved safely.
4. Normalize output on save:
   - uppercase product keys
   - normalized product-type values
   - omit empty mappings
5. Validate that saved mappings appear in `config.json` and are consumed by runtime path resolution.

## Validation
- UI shows the available products and available product types.
- Operator can assign products without editing JSON directly.
- Saving updates `config.product_type_by_product` in `config.json`.
- Runtime continues to resolve mapped products to the expected `product_type`.

## Implementation
- Updated `TradeApps/breakout/fs/trade_viewer.html` config modal to add an operator-facing product mapping section.
- Chosen interaction model: per-product assignment.
- The config UI now:
  - lists products from `config.trade_products`
  - lists available types from `config.product_types`
  - shows a dropdown beside each product
  - supports `Default (<product_type>)` as the fallback option
  - writes only explicit overrides into `config.product_type_by_product`
- Retained a read-only JSON preview so the saved mapping remains transparent.

## Validation Notes
- This change is frontend/config-modal only; no Python backend change was required because `/api/config` already normalizes `product_type_by_product`.
- Manual UI verification is still required:
  - open the config modal
  - assign one or more products to a non-default type
  - save
  - confirm `config.json` reflects the selected mapping entries
  - confirm runtime uses those mappings on the next write path

## Chronology
- 2026-03-15 01:41 Europe/London: Task created to add a proper product-to-product-type mapping UI after clarifying that raw JSON editing is not sufficient.
- 2026-03-15 01:49 Europe/London: Implemented per-product mapping dropdowns in the FS config UI and switched save behavior to collect explicit mapping overrides from the UI.
