# Frequency Explorer Config Product-Type Scope Fix

Source: User correction, 2026-04-21
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Make frequency explorer switch/open product-type eligibility use `config.json` `product_type_by_product` instead of hard-coded product inference.

## Context
Affected files:
- `TradeApps/breakout/fs/frequency_explorer.html`
- `TradeApps/breakout/fs/config.json`

Observed correction:
- `config.json` contains the authoritative product-to-product_type map.
- `NQ` is mapped to `indices`.
- Forex products such as `AUD` and `NZDAUD_C` are not individually mapped, so the selected forex source remains eligible unless config explicitly maps the product to another type.

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: `workstream/300_complete/20260421_153713_frequency_explorer_forex_unknown_scope.md`

## Plan
- [x] 1. Remove hard-coded product inference from switch/open scope resolution.
  - [x] Test: `rg` confirms `inferProductTypeFromProduct` is removed and `resolveLeaderProductType` uses config mapping only.
  - Evidence: `rg` shows no `inferProductTypeFromProduct` symbol; `resolveLeaderProductType` returns `productTypeByProduct[productKey]` after explicit row metadata.

- [x] 2. Validate reported product behavior using config-map semantics.
  - [x] Test: Static simulation shows `AUD=true`, `NZDAUD_C=true`, `NQ=false` under selected forex scope using `product_type_by_product`.
  - Evidence: Node simulation returned `AUD=true`, `NZDAUD_C=true`, `NQ=false`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Switch/open scope uses config mapping, not hard-coded inference.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `rg -n "inferProductTypeFromProduct|resolveLeaderProductType|productTypeByProduct|isLeaderInSwitchScope" TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Product-type resolution uses config map and no inference helper remains.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Static checks returned `config_lookup=True`, `explicit_first=True`, `no_inference=True`, `unknown_allowed=True`.
  - Objective-Proved: Scope logic is config-driven and does not rely on hard-coded product inference.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Node simulation returned `AUD=true`, `NZDAUD_C=true`, `NQ=false`.
  - Objective-Proved: Under forex scope, unmapped forex-source products remain eligible while config-mapped `NQ` is excluded.
  - Status: captured

## Implementation Log
- 2026-04-21 15:39: Created task from user correction to use `config.json` mapping.
- 2026-04-21 15:42: Removed `inferProductTypeFromProduct` hard-coded fallback.
- 2026-04-21 15:43: Confirmed product-type resolution uses row metadata first, then `config.json` `product_type_by_product`.
- 2026-04-21 15:44: Validated expected forex-scope behavior with static checks and Node simulation.

## Changes Made
- `TradeApps/breakout/fs/frequency_explorer.html`
  - Removed hard-coded product-type inference for forex pairs, indices, crypto, metals, and energy.
  - `resolveLeaderProductType(...)` now uses explicit `leader.product_type` if present, otherwise `productTypeByProduct[product]` loaded from `config.json`.
  - `isLeaderInSwitchScope(...)` blocks config-mapped products from other product types and allows unmapped products from the selected source.

## Validation
- `rg -n "inferProductTypeFromProduct|resolveLeaderProductType|productTypeByProduct|isLeaderInSwitchScope" TradeApps/breakout/fs/frequency_explorer.html`
  - Result: no inference helper; config map lookup present.
- Static checks:
  - Result: `config_lookup=True`, `explicit_first=True`, `no_inference=True`, `unknown_allowed=True`.
- Node simulation with `config.json` map:
  - Result: `AUD=true`, `NZDAUD_C=true`, `NQ=false`.

## Risks/Notes
- Products missing from `product_type_by_product` are treated as not explicitly excluded by config when viewing a selected product_type folder.
- Products explicitly mapped to a different product_type in config are excluded from the selected product_type switching process.

## Completion Status
Status: Complete
Created: 2026-04-21 15:39
Completed: 2026-04-21 15:44
