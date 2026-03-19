# Breakout FS Map Products To Product Type

## Objective
Create and maintain explicit product-to-product-type mappings in FS config so each product resolves to the correct `product_type` folder instead of relying only on the default fallback.

## Problem
- FS now supports `json/{run_mode}/{product_type}/{date}`.
- Unmapped products currently fall back to the default `product_type` (typically `forex`).
- Mixed-asset coverage needs explicit per-product routing, e.g. crypto products should not silently land under `forex`.

## Scope
- Add the required product entries to `config.product_type_by_product`.
- Validate that the runtime resolves those products into the intended `product_type`.
- Keep the mapping aligned with `config.product_types` and the available endpoint set.

## Examples
- `BTCUSD` -> `crypto`
- `ETHUSD` -> `crypto`
- `XTIUSD` -> `energy`

## Plan
1. Identify the products that need explicit mapping.
2. Update `config.product_type_by_product` with uppercase product keys and normalized product-type values.
3. Verify those product types are present in `config.product_types`.
4. Validate runtime folder resolution for at least one mapped product.

## Validation
- Config contains the expected mapping entries.
- Mapped products resolve to `json/{run_mode}/{mapped_product_type}/{date}`.
- Unmapped products still resolve to the default `product_type`.

## Chronology
- 2026-03-14 23:43 Europe/London: Task created to explicitly map products to `product_type` in FS config.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
