# Workstream Kanban Today Date Selector Fix

## Source
User report during conversation on 2026-03-31 with attached Workstream Kanban screenshot showing `Today` paired with `30 Mar` while the current local date is `2026-03-31`.

## Task Type
standard

## Task Attributes
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
- depends_on: []
- feeds_into: []

## Task Summary
Fix the Workstream Kanban date selector so the `Today` preset and adjacent displayed date always resolve to the current local calendar date. The selector currently shows `30 Mar` on `2026-03-31`, which indicates the page is using UTC-derived ISO dates instead of local-date formatting.

## Context
- `workstream/kanban_dashboard.py`
- The visible defect is in the Workstream Kanban header filter where `Today` is shown with `30 Mar` even though the current date is `2026-03-31`.
- Likely fault points already identified in the page script:
  - `start: start.toISOString().split('T')[0]`
  - `end: end.toISOString().split('T')[0]`
  - `new Date().toISOString().split('T')[0]` for custom-range defaults
  - `const today = new Date().toISOString().split('T')[0]` during preset recalculation
- These UTC conversions can drift to the previous day in Europe/London after local midnight and before UTC midnight.

## Dependency
Dependency: None

## Plan

- [x] 1. Inspect the Workstream Kanban date preset code path and identify every UTC-based date-string conversion affecting `Today`, default dates, and displayed labels.
  - [x] Test: Run `Select-String -Path workstream\kanban_dashboard.py -Pattern "toISOString\(\)\.split\('T'\)\[0\]|toISOString\(\)\.slice\(0, 10\)|dateRangePreset|dateRangeDisplay|startDate|endDate" -CaseSensitive:$false` and confirm all affected lines are documented in this task.
  - Evidence: Confirmed UTC selector conversions in `workstream/kanban_dashboard.py` before the patch at the range return values, custom-date defaults, and saved-preset recalculation path.

- [x] 2. Replace UTC date generation with a shared local-date helper and ensure preset calculation, hidden filter state, and custom-date defaults use the same local calendar source.
  - [x] Test: Review the updated script and confirm all `Today`-dependent values route through one local-date helper instead of `toISOString().split('T')[0]`.
  - Evidence: Added `toLocalDateIso()` and replaced all selector-related UTC conversions in `workstream/kanban_dashboard.py`; `rg` now shows only helper-based local-date generation at lines `1329`, `1384`, `1385`, `1420`, and `1421`.

- [ ] 3. Verify the rendered selector shows `31 Mar` for `Today` on `2026-03-31` and that other presets still populate valid ranges.
  - [ ] Test: Open the Workstream Kanban UI, leave the preset on `Today`, and confirm the displayed date reads `31 Mar`; then switch through `Yesterday`, `This Week`, and `Custom Range` to confirm ranges still update correctly.
  - Evidence: Pending browser verification artifact from the Workstream Kanban header after the fix, plus notes for preset regression checks.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: screenshot
  - Artifact: Attached user screenshot showing `Today` with `30 Mar` on local date `2026-03-31`.
  - Objective-Proved: Confirms the user-visible defect exists in the Workstream Kanban header.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'` => `2026-03-31 13:19:35 +01:00`; `rg -n "toISOString\(\)\.split\('T'\)\[0\]|toISOString\(\)\.slice\(0, 10\)|toLocalDateIso\(" workstream\kanban_dashboard.py` => helper usage only at lines `1329`, `1384`, `1385`, `1420`, `1421`; `Select-String -Path 'workstream\kanban_dashboard.py' -Pattern 'toLocalDateIso\(|dateRangeDisplay|startDate|endDate'` confirmed selector flow references.
  - Objective-Proved: Proves the selector logic no longer uses UTC date slicing and now routes through the shared local-date helper.
  - Status: captured

- Evidence-Type: diff
  - Artifact: `workstream/kanban_dashboard.py`
  - Objective-Proved: Proves the selector logic was updated from UTC date slicing to local-date handling via `toLocalDateIso()`.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: Planned Workstream Kanban UI check on `2026-03-31` showing `Today` aligned to `31 Mar`.
  - Objective-Proved: Will prove the visible selector now matches the actual current date in the browser.
  - Status: planned

- Evidence-Type: user_feedback
  - Artifact: Pending user confirmation after fix deployment.
  - Objective-Proved: Final user-visible validation of the corrected selector behavior.
  - Status: planned

## Implementation Log
- 2026-03-31 12:25:08 +01:00 — Task created in `workstream/100_todo` from user-reported Workstream Kanban date-selector defect.
- 2026-03-31 12:25:08 +01:00 — Initial triage identified UTC ISO date-string usage in `workstream/kanban_dashboard.py` as the probable cause of the `30 Mar` display on local date `2026-03-31`.
- 2026-03-31 13:12:00 +01:00 — Moved task to `workstream/200_inprogress` when implementation began.
- 2026-03-31 13:17:00 +01:00 — Added `toLocalDateIso()` and replaced UTC selector date generation in `workstream/kanban_dashboard.py`.
- 2026-03-31 13:19:35 +01:00 — Verified the selector path no longer contains `toISOString().split('T')[0]` and documented the remaining helper call sites.

## Changes Made
- `workstream/kanban_dashboard.py`
  - Added a shared `toLocalDateIso()` helper for selector-safe local-date formatting.
  - Updated `calculateDateRange()` to return local calendar dates instead of UTC-converted ISO strings.
  - Updated custom-range defaults to use local-date formatting instead of `new Date().toISOString().split('T')[0]`.
  - Removed the stale UTC `today` fallback from saved-preset loading because non-custom presets are recalculated through `calculateDateRange()`.

- `workstream/200_inprogress/20260331_122508_workstream_kanban_today_date_selector_fix.md`
  - Updated lifecycle state, validation evidence, and implementation notes after the code patch.

## Validation
- `Get-Date -Format "yyyyMMdd_HHmmss"`
  - Result: `20260331_122508`
- `Select-String -Path workstream\kanban_dashboard.py -Pattern "today|toISOString|dateRangePreset|selectedDate|dateRangeDisplay|startDate|endDate" -CaseSensitive:$false`
  - Result: confirmed selector-related UTC date conversions at the preset calculation and default-date paths, including `toISOString().split('T')[0]` occurrences around the `currentDateRange` logic.
- `Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'`
  - Result: `2026-03-31 13:19:35 +01:00`
- `rg -n "toISOString\(\)\.split\('T'\)\[0\]|toISOString\(\)\.slice\(0, 10\)|toLocalDateIso\(" workstream\kanban_dashboard.py`
  - Result: `1329:function toLocalDateIso(date = new Date()) {`, `1384:start: toLocalDateIso(start),`, `1385:end: toLocalDateIso(end)`, `1420:document.getElementById('startDate').value = currentDateRange.start || toLocalDateIso();`, `1421:document.getElementById('endDate').value = currentDateRange.end || toLocalDateIso();`
- `Select-String -Path 'workstream\kanban_dashboard.py' -Pattern 'toLocalDateIso\(|dateRangeDisplay|startDate|endDate' | ForEach-Object { "{0}:{1}" -f $_.LineNumber, $_.Line.Trim() }`
  - Result: helper and selector-flow references confirmed at lines `941`, `943`, `945`, `1329`, `1384`, `1385`, `1395`, `1396`, `1420`, `1421`, `1429`, `1436`, `1437`, `1439`, `1444`, `1449`, `1450`, `1497`, `1498`, `1505`, `2690`, and `2693`
- User verification pending
  - Requested check: Reload Workstream Kanban on `2026-03-31`, keep the preset on `Today`, and confirm the header shows `31 Mar` instead of `30 Mar`. Also switch through `Yesterday`, `This Week`, and `Custom Range` once to ensure the selector still updates correctly.

## Risks/Notes
- This is a user-visible UI defect and should not be marked complete until the rendered Workstream Kanban selector is checked in the browser on local date `2026-03-31`.
- The same UTC/local-date bug pattern was already fixed in another app on `2026-03-30`, so the Kanban page should reuse the same local-date helper approach rather than adding another one-off patch.
- If the page stores preset state in local storage, saved non-custom values should be recalculated on load so stale prior-day dates are not restored.

## Completion Status
Awaiting user verification as of 2026-03-31 13:19:35 +01:00.


# User Feedback
User Verified: PASS
