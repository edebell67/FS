Priority: 2

# Task Summary
Add percent-complete reporting for each epic so the kanban app shows real progress derived from workflow state counts rather than leaving progress implicit.

# Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- Existing epic reconciliation and epic listing UI/API
- Workstream state folders used to determine actual progress

Dependency: None

# Plan
- [x] 1. Inspect existing epic reconciliation/summary logic and identify the correct source of truth for epic completion percentage.
  - [x] Test: Read the reconciliation functions and epic list rendering paths in `workstream/kanban_dashboard.py`.
  - [x] Evidence: Chose `get_epic_full_reconciliation()` summary counts as the source of truth and used `complete / expected`, capped at `100`.
- [x] 2. Implement percent-complete calculation for each epic using actual workflow states and expose it through the relevant API payloads.
  - [x] Test: Run a local code-level validation to confirm the new percent field is present and numerically consistent with the state counts.
  - [x] Evidence: `_list_epics_with_solutions()` now returns `progress_pct`, `expected_count`, `complete_count`, `in_progress_count`, `backlog_count`, `review_count`, and `failed_count`.
- [x] 3. Render the epic percent-complete indicator in the UI so progress is visible per epic.
  - [x] Test: Verify the updated UI code references and output wiring include the new percent metric.
  - [x] Evidence: Reconciliation epic selector options now render as `Epic Name (NN% • complete/expected)`.

# Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: Kanban code updated to calculate and display epic percent complete.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Pending user verification in the running reconciliation UI
  - Objective-Proved: User-visible epic progress indicator works correctly in the running app.
  - Status: planned

# Implementation Log
- 2026-03-19 19:44:36: Created task from user request to report percent complete for each epic.
- 2026-03-19 19:46:00: Reviewed `get_epic_full_reconciliation()` and the reconciliation page UI; found the percent already exists inside a single epic view but was not surfaced on the epic list itself.
- 2026-03-19 19:47:00: Updated `_list_epics_with_solutions()` to use bare epic slugs, pull reconciliation summaries, and include percent/state counts for each epic.
- 2026-03-19 19:48:00: Updated the reconciliation epic selector so each option shows percent complete plus complete/expected counts.
- 2026-03-19 19:49:00: Capped percent complete at `100` to avoid overstating progress when augmented/subtasked epics produce more completed tasks than the original expected baseline.

# Changes Made
- Updated `C:\Users\edebe\eds\workstream\kanban_dashboard.py`:
  - fixed `with-solutions` epic list slugs to return the bare epic slug rather than `ep_<slug>`
  - exposed per-epic reconciliation counts and `progress_pct` in `_list_epics_with_solutions()`
  - updated reconciliation selector labels to show `NN% • complete/expected`
  - capped reconciliation `delivery_pct` at `100`

# Validation
- `python -m py_compile workstream/kanban_dashboard.py`
  - Pass. Only the existing embedded-HTML `SyntaxWarning` remains.
- `python -c "... m._list_epics_with_solutions() ..."`
  - Pass. Confirmed returned items now include:
    - `slug`
    - `progress_pct`
    - `expected_count`
    - `complete_count`
    - `in_progress_count`
    - `backlog_count`
    - `review_count`
    - `failed_count`
  - Sample validated values:
    - `autonomous_trading_signal_platform`: `100%`
    - `synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`: `80%`
    - `mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`: `20%`
- User verification still required:
  - open the reconciliation page
  - confirm each epic option now shows a sensible percent complete and `complete/expected` count

# Risks/Notes
- Percent complete must be based on a clear, defensible formula tied to actual workflow states.
- For epics without a usable decomposition manifest or expected task baseline, progress remains `0%` because there is no defensible denominator yet.

# Completion Status
- Awaiting user verification.
