# Task: Implement Auto-Select Function in Weekly Performance Dashboard

## Source
- User Directive: 2026-04-07
- Follow-up remediation: 2026-04-08 review findings resolved during Codex implementation pass

## Task Type
standard

## Task Attributes
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary
Introduce an auto-select workflow in the weekly performance dashboard that supports per-product-type modes and an explicit multi-select allowlist of permitted product types. Auto-selection must only activate or deactivate strategies inside the current product-type boundary and must persist both the per-type mode map and permitted-type allowlist in `config.json`.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Config API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Config file: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`

## Destination Folder
None

## Dependency
None

## UI Requirements
- Auto Select dropdown: `None`, `All`, `Scalper`, `Rev_scalper` scoped per viewed product type.
- Permitted Types selector: user can select one or more product types for which auto-select is allowed to operate.

## Logic Requirements
1. `evaluateAutoSelect()` must check `auto_select_permitted_types` before promoting or clearing leaders.
2. Auto-selection actions must stay within the current `product_type` boundary.
3. Triggers: dropdown change, permitted-type change, and data refresh.
4. Actions must toggle the top strategy with `manual: false` and `auto_promote: true`.
5. `auto_select_modes` and `auto_select_permitted_types` must persist in `config.json`.
6. If the current product type is no longer permitted, any scoped auto-promoted leader must be cleared.

## Plan
- [x] 1. Update config storage to support `auto_select_modes` and `auto_select_permitted_types`.
  - [x] Test: Read `TradeApps\breakout\fs\config.json` and confirm both keys exist.
  - Evidence: `config.json` now includes `auto_select_modes` and `auto_select_permitted_types`.
- [x] 2. Add permitted product-type selection UI to `weekly_performance.html`.
  - [x] Test: Read `weekly_performance.html` and confirm the `autoSelectPermittedTypes` container and permit-chip styles exist.
  - Evidence: Added permit-chip UI block and styling to the auto-select control panel.
- [x] 3. Refine auto-select logic to enforce allowlist gating and strict product-type scoping.
  - [x] Test: Read `weekly_performance.html` and confirm `evaluateAutoSelect()` checks `isCurrentProductTypePermitted()` and `getCurrentAutoLeadersForScope()` resolves leaders by product type.
  - Evidence: Auto-select now loads/saves `auto_select_permitted_types`, uses a product-to-type map, and clears scoped leaders when a type is no longer permitted.
- [x] 4. Fix config persistence so partial `/api/config` updates do not overwrite unrelated settings.
  - [x] Test: Read `trade_viewer_api.py` and confirm POST merges `incoming` into the current config before writing.
  - Evidence: `update_config()` now merges with `old_cfg` and normalizes `auto_select_modes` and `auto_select_permitted_types`.
- [x] 5. Validate the updated workflow against the review findings.
  - [x] Test: Confirm this task file is lifecycle-complete and that the code paths exist for: one-or-more permitted types, blocked non-permitted type, and scoped clear/apply behavior.
  - Evidence: This file now includes the required lifecycle sections and the implementation contains explicit boundary checks plus allowlist persistence.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: The weekly dashboard exposes the permitted-types selector and enforces scoped auto-select behavior in the client logic.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Objective-Proved: Partial config updates are merged safely and auto-select config fields are normalized before persistence.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Objective-Proved: Config defaults now include `auto_select_modes` and `auto_select_permitted_types`.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Code review of `evaluateAutoSelect()`, `getCurrentAutoLeadersForScope()`, and the permitted-type selector handlers
  - Objective-Proved: Auto-selection only runs for explicitly selected product types and remains within the current product-type boundary.
  - Status: captured

## Implementation Log
- 2026-04-07 18:40:00: Initial task created for auto-select support in the weekly performance dashboard.
- 2026-04-08 23:21:24 BST: Codex reopened the implementation area to resolve review findings and finish the missing allowlist/scoping behavior.
- 2026-04-08 23:21:24 BST: Added a multi-select permitted product-type UI to `weekly_performance.html`.
- 2026-04-08 23:21:24 BST: Hardened scope detection using normalized product-type mapping so auto-promoted strategies are only cleared within the active product-type boundary.
- 2026-04-08 23:21:24 BST: Updated `/api/config` writes to merge with the existing config and normalized the new auto-select config fields.
- 2026-04-08 23:21:24 BST: Rewrote this lifecycle file to satisfy the repository’s required schema and complete-state rules.

## Changes Made
- `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Added `auto_select_permitted_types` load/save support.
  - Added permitted product-type chips for one-or-more selection.
  - Added `productTypeByProduct` mapping helpers.
  - Updated `getCurrentAutoLeadersForScope()` to resolve real product-type scope.
  - Updated `evaluateAutoSelect()` to block non-permitted types and clear scoped auto-leaders when permission is removed.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Changed `/api/config` POST to merge incoming partial updates into the current config.
  - Added normalization for `auto_select_modes` and `auto_select_permitted_types`.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
  - Added default keys for `auto_select_modes` and `auto_select_permitted_types`.
- `C:\Users\edebe\eds\workstream\300_complete\gemini\20260407_184000_breakout_weekly_perf_auto_select_feature.md`
  - Rebuilt the lifecycle record so it is consistent with complete-state requirements.

## Validation
- Read back `weekly_performance.html` and confirmed:
  - the auto-select control now contains `autoSelectPermittedTypes`
  - `loadConfig()` loads `auto_select_permitted_types`
  - `handlePermittedTypeToggle()` persists the allowlist
  - `updateAutoSelectStatus()` shows blocked state for non-permitted product types
  - `evaluateAutoSelect()` gates on `isCurrentProductTypePermitted()` and only processes candidates whose resolved `product_type` matches the current scope
- Read back `trade_viewer_api.py` and confirmed:
  - `incoming` config is merged with `old_cfg`
  - `auto_select_modes` is normalized as a keyed map
  - `auto_select_permitted_types` is normalized as a deduplicated lowercase list
- Read back `config.json` and confirmed default auto-select persistence keys exist.

## Risks/Notes
- This change preserves the existing hardcoded product-type tabs in the weekly dashboard; the new allowlist is independent from the active view tab.
- Automatic browser validation was not run in this turn, so the verification recorded here is code-level rather than UI-clickthrough evidence.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-08 23:21:24 BST
