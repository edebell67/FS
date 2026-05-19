# Breakout FS Add Product To Product Type Allocation Workflow

## Objective
Provide a clear FS workflow for assigning each product to a specific `product_type`, so runtime writes and UI views can use a stable product-to-type mapping instead of relying only on the default type.

## Problem
- The runtime now supports `json/{run_mode}/{product_type}/{date}`.
- A default `product_type` exists, but that is not enough when some products belong to `crypto`, `energy`, `indices`, or other non-forex classes.
- Operators need an explicit way to assign products to a specific product type.
- Without this, new products will silently fall back to `forex`, which is incorrect for mixed-asset coverage.

## Scope
- Add a product-to-product-type allocation mechanism backed by `config.product_type_by_product`.
- Expose allocation in the FS config UI so the operator can manage mappings without hand-editing JSON.
- Validate that runtime writes route each mapped product into the correct `product_type` folder.

## Expected Behavior
- Operator can assign a product like `BTCUSD` to `crypto`, `XTIUSD` to `energy`, etc.
- Unmapped products still fall back to the default `product_type`.
- Allocations are persisted in `config.json`.
- Runtime writes for a mapped product go to `json/{run_mode}/{mapped_product_type}/{date}`.

## Plan
1. Define the canonical config contract for allocations:
   - `product_type` as default fallback
   - `product_types` as allowed choices
   - `product_type_by_product` as explicit mapping
2. Add/update FS config UI to support allocation editing in an operator-friendly form.
3. Normalize and validate mappings on config save:
   - uppercase product keys
   - normalized product type values
   - reject/clean invalid empty mappings
4. Verify runtime behavior by mapping at least one non-forex product and confirming its writes land in the mapped folder.
5. Document migration rules for legacy/unmapped products so fallback behavior remains predictable.

## Validation
- Save config with one or more product allocations.
- Start FS runtime and confirm mapped products write to the assigned `product_type` folder.
- Confirm unmapped products still write to the default type.

## Chronology
- 2026-03-14 21:08 Europe/London: Task created to add explicit product-to-product-type allocation workflow after confirming the new runtime folder structure appears on startup.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
