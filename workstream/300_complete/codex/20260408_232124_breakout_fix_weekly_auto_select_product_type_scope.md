# Task: Fix Weekly Auto-Select Product Type Scope

## Source
- User request: resolve review findings and ensure auto-select only affects explicitly selected product types in the weekly performance dashboard

## Task Type
standard

## Task Attributes
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary
Update the weekly performance dashboard so auto-select can be enabled for one or more permitted product types, enforce product-type boundaries during auto-promotion and deactivation, and fix config persistence so the dashboard does not overwrite unrelated settings.

## Context
- UI: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
- Config API: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
- Config file: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- Reviewed task doc: `C:\Users\edebe\eds\workstream\300_complete\gemini\20260407_184000_breakout_weekly_perf_auto_select_feature.md`

## Destination Folder
None

## Dependency
None

## Plan
- [x] 1. Inspect the weekly auto-select flow and config persistence path.
  - [x] Test: Read the relevant sections of `weekly_performance.html`, `trade_viewer_api.py`, and `config.json`.
  - Evidence: Confirmed the existing delayed leader logic, allowlist UI/load-save hooks, and merge-first `/api/config` path; the remaining gap was that `mode === 'None'` did not clear scoped auto-promoted leaders.
- [x] 2. Implement product-type allowlist UI and scoping fixes in the weekly dashboard.
  - [x] Test: Code inspection must show `auto_select_permitted_types` load/save support plus explicit allowlist gating before activation/deactivation.
  - Evidence: `weekly_performance.html` contains the permitted-type selector plus `auto_select_permitted_types` load/save handling at lines 650-765, and `evaluateAutoSelect()` now clears only scoped auto-leaders when mode is `None` or the current type is not permitted at lines 884-912.
- [x] 3. Fix config persistence so partial `/api/config` updates merge with existing config.
  - [x] Test: Code inspection must show POST payload merged into the current config before normalization and write.
  - Evidence: Verified `trade_viewer_api.py` already merges `incoming` into `old_cfg` before normalization and write at lines 3620-3686, including `auto_select_modes` and `auto_select_permitted_types`.
- [x] 4. Validate the updated behavior and document results.
  - [x] Test: Run targeted checks against the edited files and summarize the resulting line references.
  - Evidence: `python -m py_compile TradeApps\breakout\fs\trade_viewer_api.py` passed, and targeted readback via `rg`/line inspection confirmed the allowlist persistence, scoped clear path, and safe config merge behavior.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html:650-765` and `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html:884-912`
  - Objective-Proved: The weekly dashboard loads and persists `auto_select_permitted_types`, resolves product-type scope, and clears only in-scope auto-promoted leaders when a scope is disabled or not permitted.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Objective-Proved: This turn's patch closes the remaining frontend scope hole by clearing scoped auto-leaders when the current product type is set to `None`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - Objective-Proved: The config API file remains syntactically valid after validation and its existing merge logic is intact.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py:3620-3686`
  - Objective-Proved: Partial `/api/config` updates are merged with the stored config before normalization and write, so unrelated settings are preserved.
  - Status: captured

## Implementation Log
- 2026-04-08 23:21:24 BST: Located existing auto-select delay logic in `weekly_performance.html`.
- 2026-04-08 23:21:24 BST: Confirmed `weekly_performance.html` currently persists only `auto_select_modes` and has no multi-product-type allowlist.
- 2026-04-08 23:21:24 BST: Confirmed the task scope includes `/api/config` persistence safety and re-validated the current merge-first implementation in `trade_viewer_api.py`.
- 2026-04-08 23:30:09 BST: Re-read the completed workspace state and confirmed the allowlist UI, `auto_select_permitted_types` persistence, and `/api/config` merge logic were already present before this turn's patch.
- 2026-04-08 23:30:09 BST: Patched `evaluateAutoSelect()` so selecting `None` clears only the current scope's auto-promoted leaders instead of leaving them active.
- 2026-04-08 23:30:09 BST: Ran targeted validation (`py_compile`, `rg`, and line readback) and updated this lifecycle record with corrected evidence.

## Changes Made
- `C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html`
  - Confirmed the existing permitted-types selector, allowlist persistence handlers, and normalized product-type helpers remain in place.
  - Updated `evaluateAutoSelect()` so `mode === 'None'` deactivates only the current product type's auto-promoted leaders.
- `C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py`
  - No additional code change was required in this turn; verified the existing merge-first `/api/config` implementation and auto-select field normalization.
- `C:\Users\edebe\eds\workstream\300_complete\codex\20260408_232124_breakout_fix_weekly_auto_select_product_type_scope.md`
  - Corrected the lifecycle record so the evidence and change summary match the actual workspace state and validations from this turn.

## Validation
- Read `weekly_performance.html` around lines 471-801 and identified the exact auto-select UI and logic hooks.
- Read `trade_viewer_api.py` around lines 3620-3729 and confirmed the current implementation merges partial config writes into the stored config before normalization and write.
- Ran `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` and it exited successfully with no syntax errors.
- Ran `rg -n "auto_select_permitted_types|mode disabled for scope|current product type is not permitted|auto_select_modes|data = dict\\(old_cfg\\)|data\\.update\\(incoming\\)" C:\Users\edebe\eds\TradeApps\breakout\fs\weekly_performance.html C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py` and confirmed:
  - `weekly_performance.html:660-662` loads `auto_select_modes`, `auto_select_permitted_types`, and `product_type_by_product`
  - `weekly_performance.html:758-763` persists the permitted-type allowlist
  - `weekly_performance.html:894-912` clears scoped auto-leaders when auto-select is disabled or the current type is not permitted
  - `trade_viewer_api.py:3634-3635` merges partial payloads into the existing config
  - `trade_viewer_api.py:3669-3686` normalizes `auto_select_modes` and `auto_select_permitted_types` before write
- Requested user verification in the final response for an optional browser pass on the weekly dashboard.

## Risks/Notes
- The weekly page currently hardcodes visible product-type buttons; this change will preserve that layout while making auto-select permissions independent from the active tab.
- If other pages rely on destructive replacement semantics for `/api/config`, a merge-based update changes that behavior; this is expected to be safer for existing partial-update callers.
- Browser-level clickthrough validation was not run in this turn; verification here is syntax plus code-level readback.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-08 23:30:09 BST
