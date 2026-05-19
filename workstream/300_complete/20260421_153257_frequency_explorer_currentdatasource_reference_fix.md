# Frequency Explorer CurrentDataSource Reference Fix

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
Fix the runtime error `currentDataSource is not defined` when loading forex `_frequency.json` after product-type switch scoping changes.

## Context
Affected file:
- `TradeApps/breakout/fs/frequency_explorer.html`

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: `workstream/300_complete/20260421_152621_frequency_explorer_product_type_switch_scope.md`

## Plan
- [x] 1. Replace undefined `currentDataSource` reference with an existing source resolver.
  - [x] Test: Static check confirms no `currentDataSource` references remain.
  - Evidence: `rg -n "currentDataSource" TradeApps/breakout/fs/frequency_explorer.html` returned no matches.

- [x] 2. Validate cache key still includes source file.
  - [x] Test: Static check confirms `_getSigCacheKey` uses `DATA_SOURCES[dataSourceKey]` source file.
  - Evidence: PowerShell static checks returned `cache_scope=True`, `cache_uses_datasources=True`, `no_currentdatasource=True`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Runtime reference error removed.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `rg -n "currentDataSource" TradeApps/breakout/fs/frequency_explorer.html` returned no matches.
  - Objective-Proved: Undefined variable reference is removed.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: PowerShell static checks returned `cache_scope=True`, `cache_uses_datasources=True`, `no_currentdatasource=True`.
  - Objective-Proved: Signal cache remains scoped by source file without using undefined state.
  - Status: captured

## Implementation Log
- 2026-04-21 15:32: Created task from forex JSON load error.
- 2026-04-21 15:34: Replaced `currentDataSource?.file` with `DATA_SOURCES[dataSourceKey] || DATA_SOURCES.standard`.
- 2026-04-21 15:35: Ran targeted static validation.

## Changes Made
- `TradeApps/breakout/fs/frequency_explorer.html`
  - `_getSigCacheKey(sessionDate)` now resolves source file from existing `DATA_SOURCES[dataSourceKey]`.
  - Removed dependency on nonexistent `currentDataSource`.

## Validation
- `rg -n "currentDataSource" TradeApps/breakout/fs/frequency_explorer.html`
  - Result: no matches.
- PowerShell static checks:
  - Result: `cache_scope=True`, `cache_uses_datasources=True`, `no_currentdatasource=True`.

## Risks/Notes
- This is a targeted runtime fix for the prior product-type cache scoping patch.

## Completion Status
Status: Complete
Created: 2026-04-21 15:32
Completed: 2026-04-21 15:35
