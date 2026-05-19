# Breakout FS Migrate JSON Layout To Run Mode Product Type Date

## Objective
Migrate the FS runtime from `json/{run_mode}/{date}` to `json/{run_mode}/{product_type}/{date}` while treating all legacy data as `forex` by default and preserving backward-compatible reads during transition.

## Scope
- Add shared path helpers for FS runtime read/write operations.
- Update active FS runtime/API/archive/summary entry points to use the shared resolver.
- Default legacy product type to `forex`.
- Keep reads compatible with both new and legacy layouts.
- Add validation covering runtime-facing paths, not just the resolver.

## Out Of Scope
- Bulk migration of every historical utility script.
- Physical data move of old folders into `forex`.

## Validation
- Python syntax checks for changed FS modules.
- Targeted tests covering read compatibility and new-layout writes.
- Focused verification that legacy `json/live/{date}` is interpreted as `forex`.

## Implementation
- Added shared layout helpers in `TradeApps/breakout/fs/json_layout.py` for:
  - default `forex` fallback
  - configured product type list
  - per-product product type mapping
  - compatibility reads across legacy and new layouts
  - directory creation for new writes
- Updated `TradeApps/breakout/fs/common.py` to:
  - load `product_type`, `product_types`, and `product_type_by_product`
  - route trade writes into `json/{run_mode}/{product_type}/{date}`
  - read market bias, summary, live-trade counts, archive scans, and auto-activation scans across legacy and product-type day dirs
- Updated `TradeApps/breakout/fs/trade_viewer_api.py` to:
  - resolve/read trade files across legacy and product-type layouts
  - aggregate day-level reads for trades, top20, top_one, and stats summary across configured product types
  - normalize the new config keys on `/api/config` save
- Updated `TradeApps/breakout/fs/summary_net_generator.py` to scan all configured product-type day dirs instead of only `json/{mode}/{date}`
- Added config keys to `TradeApps/breakout/fs/config.json`:
  - `product_type`
  - `product_types`
  - `product_type_by_product`
- Updated `TradeApps/breakout/fs/trade_viewer.html` config UI to expose:
  - default product type
  - selectable product types
  - JSON editor for per-product product type mapping
- Added test coverage in `tests/test_breakout_fs_json_layout.py` for:
  - resolver preference/fallback
  - mapping-based product type selection
  - automatic directory creation from config
  - enumeration of legacy plus product-type dirs

## Chronology
- 2026-03-14 16:29 Europe/London: Task created for end-to-end FS layout migration after impact review and resolver test generation.
- 2026-03-14 16:40 Europe/London: Added shared layout helpers and expanded resolver tests to cover config-driven product type behavior.
- 2026-03-14 16:55 Europe/London: Patched active FS runtime/API/config UI paths to use the shared layout model with legacy-read compatibility.
- 2026-03-14 17:02 Europe/London: Validation passed with `python -m py_compile` on changed FS modules and `pytest tests/test_breakout_fs_json_layout.py` (`7 passed`).
