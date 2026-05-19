# Frequency Explorer Forex Unknown Scope Fix

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
Fix forex opening trade selection where `AUD` rank #1 was excluded as unknown product type, causing `NZDAUD_C` rank #2 to be opened.

## Context
Affected file:
- `TradeApps/breakout/fs/frequency_explorer.html`

Observed issue:
- Forex snapshot at 01:00 had `AUD` rank #1 with count 1 and +70 net.
- Opening signal selected `NZDAUD_C` with count 0 because `AUD` did not match the canonical forex-pair inference pattern.

## Destination Folder
Destination Folder: `TradeApps/breakout/fs/`

## Dependency
Dependency: `workstream/300_complete/20260421_152621_frequency_explorer_product_type_switch_scope.md`

## Plan
- [x] 1. Adjust product-type scope guard so selected folder type remains authoritative for unknown products while known nonmatching products remain excluded.
  - [x] Test: Static code inspection confirms `isLeaderInSwitchScope` allows unresolved products in a selected non-empty scope but still compares resolved known types.
  - Evidence: `isLeaderInSwitchScope` now returns true for unresolved product type and compares resolved known product types to the active scope.

- [x] 2. Validate the AUD/NZDAUD selection case from the reported snapshot.
  - [x] Test: Static simulation of products `AUD`, `NZDAUD_C`, and `NQ` under `forex` scope returns eligible, eligible, excluded.
  - Evidence: Node simulation returned `AUD=true`, `NZDAUD_C=true`, `NQ=false`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/frequency_explorer.html`
  - Objective-Proved: Unknown forex-folder products no longer get dropped from forex opening/switch selection.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: PowerShell static checks returned `unknown_allowed=True`, `known_compared=True`, `currentdatasource_removed=True`.
  - Objective-Proved: Scope logic allows unresolved selected-source products and still excludes known mismatches.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: Node static simulation returned `AUD=true`, `NZDAUD_C=true`, `NQ=false`.
  - Objective-Proved: Reported forex case now includes `AUD` while still excluding `NQ` leakage.
  - Status: captured

## Implementation Log
- 2026-04-21 15:37: Created task from reported `AUD` rank #1 versus `NZDAUD_C` opening mismatch.
- 2026-04-21 15:39: Updated scope guard to allow unresolved products from the selected source while excluding known nonmatching products.
- 2026-04-21 15:40: Validated reported product cases with a static Node simulation.

## Changes Made
- `TradeApps/breakout/fs/frequency_explorer.html`
  - `isLeaderInSwitchScope(...)` now treats unresolved product types as eligible inside the selected product-type source.
  - Known mismatches still fail scope comparison, so `NQ` remains excluded when forex is selected.

## Validation
- PowerShell static checks:
  - Result: `unknown_allowed=True`, `known_compared=True`, `currentdatasource_removed=True`.
- Node static simulation:
  - Result: `AUD=true`, `NZDAUD_C=true`, `NQ=false`.

## Risks/Notes
- This intentionally keeps known non-forex products such as `NQ` excluded from forex scope while allowing unresolved products from the selected forex file to participate.

## Completion Status
Status: Complete
Created: 2026-04-21 15:37
Completed: 2026-04-21 15:40
