# Frequency Explorer Signal Cache Version Invalidation

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
Invalidate stale browser switch/open signal cache after product-type eligibility logic changed. The 01:00 forex opener still showed `NZDAUD_C` even though corrected logic should select `AUD`.

## Context
Affected file:
- `TradeApps/breakout/fs/frequency_explorer.html`

Root cause:
- `_sigCache` is immutable per snapshot and persisted in `localStorage`.
- Previous bad opener decisions can replay because the cache key did not change when product-type selection logic changed.

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: `workstream/300_complete/20260421_153952_frequency_explorer_config_product_type_scope.md`

## Plan
- [x] 1. Add a switch signal cache version to the cache key.
  - [x] Test: Static check confirms cache key includes a version token.
  - Evidence: Static checks returned `cache_version_const=True` and `cache_key_versioned=True`.

- [x] 2. Validate reported 01:00 selection logic with fresh cache behavior.
  - [x] Test: Static simulation of reported leaders shows `AUD` wins over `NZDAUD_C` when cache is not replaying stale data.
  - Evidence: Node simulation returned `AUD|breakout_R_2_tp5.0_sl20.0|net=70|count=1`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Stale cached open/switch signals are invalidated.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Static checks returned `cache_key_versioned=True`, `cache_version_const=True`, `config_lookup=True`, `no_inference=True`.
  - Objective-Proved: Cache key versioning is present and config-map scoping remains intact.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Node simulation returned `AUD|breakout_R_2_tp5.0_sl20.0|net=70|count=1`.
  - Objective-Proved: With stale cache bypassed, reported 01:00 snapshot opens the rank/count leader `AUD`, not `NZDAUD_C`.
  - Status: captured

## Implementation Log
- 2026-04-21 15:56: Created task from stale `NZDAUD_C` opener report.
- 2026-04-21 15:57: Added `SIGNAL_CACHE_VERSION` to the persisted signal cache key.
- 2026-04-21 15:58: Validated cache-key versioning and reported opener sort behavior.

## Changes Made
- `TradeApps/breakout/fs/frequency_explorer.html`
  - Added `SIGNAL_CACHE_VERSION = 'v20260421_config_product_scope'`.
  - Updated `_getSigCacheKey(...)` to include the signal cache version before date/run/product/source/rule fields.

## Validation
- Static checks:
  - Result: `cache_key_versioned=True`, `cache_version_const=True`, `config_lookup=True`, `no_inference=True`.
- Node simulation of reported 01:00 leaders:
  - Result: `AUD|breakout_R_2_tp5.0_sl20.0|net=70|count=1`.

## Risks/Notes
- Existing old localStorage cache entries will remain stored but will no longer be read because the key changes.

## Completion Status
Status: Complete
Created: 2026-04-21 15:56
Completed: 2026-04-21 15:58
