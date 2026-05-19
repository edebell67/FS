# Frequency Explorer Product-Type Switch Scope Fix

Source: User report, 2026-04-21
Task Type: standard

## Task Attributes
recurring_task: false
looping_task: false
splittable_task: false
workflow_task: false
depends_on: []
feeds_into: []

## Task Summary
Fix `frequency_explorer.html` so switch/open signals cannot mix product types. A forex leaderboard was showing an opening trade for `NQ`, which belongs to `indices`.

## Context
Affected file:
- `TradeApps/breakout/fs/frequency_explorer.html`

Observed issue:
- Selected forex data showed forex-like leaderboard rows but emitted `OPENING TRADE NQ / breakout_2_tp10.0_sl20.0`.
- Signal cache keys are scoped only by date and rule, not product type/source.
- Product-type resolver only uses explicit `product_type` or `config.product_type_by_product`; forex pairs such as `GBPAUD_C` are not in the config map.

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: None

## Plan
- [x] 1. Patch product-type resolution and signal cache scoping.
  - [x] Test: Inspect code to confirm cache key includes selected product type/source and cached signals are revalidated before firing.
  - Evidence: `frequency_explorer.html` now builds `sigCache_${sessionDate}_${runMode}_${selectedType}_${sourceFile}_${_getRuleFingerprint()}` and guards cached/current/fired signals with product-type scope checks.

- [x] 2. Validate syntax/static behavior.
  - [x] Test: Run targeted grep/checks for updated helpers and ensure no stale unscoped cache calls remain.
  - Evidence: `cache_scope=True`, `cached_guard=True`, `fire_guard=True`, `forex_infer=True`; targeted `rg` shows product-type guards at signal selection, cached signal replay, computed switch creation, and fire action.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Product-type scoping implemented for browser switch/open signal generation.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `rg -n "function _getSigCacheKey|function inferProductTypeFromProduct|function isSignalInSwitchScope|isLeaderInSwitchScope|fireSwitchAction" TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Required helpers and guarded fire path exist in the browser implementation.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: PowerShell static checks returned `cache_scope=True`, `cached_guard=True`, `fire_guard=True`, `forex_infer=True`.
  - Objective-Proved: Cache scoping, cached signal rejection, final fire rejection, and forex product inference are present.
  - Status: captured

## Implementation Log
- 2026-04-21 15:26: Created in-progress task from user report.
- 2026-04-21 15:31: Added product-type inference for canonical forex pairs and known non-forex product roots.
- 2026-04-21 15:33: Scoped localStorage switch-signal cache by run mode, selected product type, and data source file.
- 2026-04-21 15:36: Added switch-scope guards for positive leader selection, cached signal replay, current held reset, computed switch creation, and final fire action.
- 2026-04-21 15:41: Ran targeted static validation checks.

## Changes Made
- `TradeApps/breakout/fs/frequency_explorer.html`
  - `_getSigCacheKey(sessionDate)` now includes `runMode`, selected `productType`, current data source file, and rule fingerprint.
  - Added `inferProductTypeFromProduct(product)` so forex pairs like `GBPAUD_C` resolve to `forex` even when missing from `config.product_type_by_product`; known roots such as `NQ` resolve to `indices`.
  - Added `isLeaderInSwitchScope(...)` and `isSignalInSwitchScope(...)`.
  - Filtered switch/open eligible leaders to the selected/current product type.
  - Rejected cached, computed, and fired signals that do not match the active product-type scope.

## Validation
- `rg -n "function _getSigCacheKey|function inferProductTypeFromProduct|function isSignalInSwitchScope|isLeaderInSwitchScope|fireSwitchAction" TradeApps/breakout/fs/frequency_explorer.html`
  - Result: Found all required helper and call sites.
- `rg -n "sigCache_|_getSigCacheKey|localStorage\\.getItem\\(key|localStorage\\.setItem\\(_sigCacheKey|isSignalInSwitchScope\\(|isLeaderInSwitchScope\\(" TradeApps/breakout/fs/frequency_explorer.html`
  - Result: Cache use is routed through `_getSigCacheKey`; scope guards are present at cached replay, current held validation, computed switch creation, and final firing.
- PowerShell static checks:
  - Result: `cache_scope=True`, `cached_guard=True`, `fire_guard=True`, `forex_infer=True`.

## Risks/Notes
- Existing unscoped `localStorage` signal caches may remain in users' browsers; new cache keys prevent reuse, but old entries are not automatically deleted.
- Product keys that are not canonical forex pairs, such as bare `AUD`, are not inferred as forex unless explicitly mapped in `config.product_type_by_product`. That prevents ambiguous products from generating forex switch/open signals.
- This task fixes switch/open signal leakage only. It does not change how raw leaderboard rows are displayed if a source file itself contains mixed products.

## Completion Status
Status: Complete
Created: 2026-04-21 15:26
Completed: 2026-04-21 15:42
