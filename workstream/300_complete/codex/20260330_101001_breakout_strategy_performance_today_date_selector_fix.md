# Strategy Performance Today Date Selector Fix

## Source
User report during conversation 1dc8e4c5-47c8-4ca9-9bc9-8cb42900b7de

## Task Summary
Fix the Strategy Performance date selector so the `Today` preset resolves to the actual local calendar date instead of drifting to the previous UTC day. The visible label and all related date-range logic on the page must remain aligned with the user’s local date.

## Dependency
Dependency: None

## Context
- `TradeApps/breakout/fs/strategy_performance.html`
- Current behavior shows `Today` while resolving to `29 Mar 2026` even though the current local date is `30 Mar 2026`
- The page still had UTC date fallbacks using `new Date().toISOString().slice(0, 10)`, which can resolve to the previous UTC day instead of the current local calendar date

## Plan

- [x] 1. Locate all strategy-performance date calculations that rely on UTC ISO date strings.
  - [x] Test: Confirm all `toISOString().split('T')[0]` and `toISOString().slice(0, 10)` usages affecting the selector and date validation paths in `strategy_performance.html`.
  - Evidence: `rg -n "toISOString\\(\\)\\.slice\\(0, 10\\)|toISOString\\(\\)\\.split\\('T'\\)\\[0\\]" TradeApps/breakout/fs/strategy_performance.html` identified the remaining UTC fallback paths at the summary handoff payload and bias-history fallback date loader.

- [x] 2. Add a shared local-date helper and update preset generation, custom-range defaults, and validation to use it consistently.
  - [x] Test: Verify the `Today` preset resolves to the local date and the label displays the correct day.
  - Evidence: Reused the existing `toLocalDateIso()` helper and replaced the last UTC fallback generators with it in `TradeApps/breakout/fs/strategy_performance.html`, keeping the selector, hidden `statsDate`, summary handoff, and bias-history date fallback on the same local-date source.

- [x] 3. Validate the page logic for date comparisons and playback gating still works with the local-date helper.
  - [x] Test: Review the existing `today` comparisons in the page and ensure they use the same local date source.
  - Evidence: `Select-String -Path TradeApps/breakout/fs/strategy_performance.html -Pattern 'toLocalDateIso\\(\\)'` confirmed shared local-date usage in custom defaults, saved-range validation, initialization fallback, `startAutoRefresh()`, `loadStats()`, summary handoff, and bias-history fallback.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/strategy_performance.html`
  - Objective-Proved: The page now routes all Strategy Performance date-selector and related fallback logic through the shared local-date helper instead of UTC date slicing.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: Strategy Performance UI date selector showing `30 Mar` for `Today` on 2026-03-30.
  - Objective-Proved: User-visible selector behavior matches the actual local date.
  - Status: planned

- Evidence-Type: test_output
  - Artifact: `Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'` => `2026-03-30 10:14:30 +01:00`; `rg -n "toISOString\\(\\)\\.slice\\(0, 10\\)|toISOString\\(\\)\\.split\\('T'\\)\\[0\\]" TradeApps/breakout/fs/strategy_performance.html` => no matches; `Select-String -Path TradeApps/breakout/fs/strategy_performance.html -Pattern 'toLocalDateIso\\(\\)'` => lines `2255`, `2256`, `2322`, `2505`, `2692`, `2730`, `4242`, `5296`
  - Objective-Proved: Local system date is `2026-03-30` and all remaining selector/gating fallback paths use `toLocalDateIso()` with no UTC date-slice leftovers in the page.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: Pending user verification request for the Strategy Performance `Today` preset and displayed date label on `2026-03-30`.
  - Objective-Proved: Final user-visible confirmation of the selector showing the correct local date is still required before closure.
  - Status: planned

## Implementation Log
- 2026-03-30 10:10 — Task created to fix the Strategy Performance `Today` date selector drift caused by UTC date formatting.
- 2026-03-30 10:10 — Moved from `workstream/100_todo` to `workstream/200_inprogress/codex` when implementation began.
- 2026-03-30 10:12 — Replaced UTC ISO date-string generation with a shared local-date helper in `TradeApps/breakout/fs/strategy_performance.html`.
- 2026-03-30 10:14 — Updated saved-preference loading so non-custom presets are recalculated on page load instead of restoring stale stored dates from a previous day.
- 2026-03-30 10:15 — Replaced the remaining UTC fallback dates in the summary handoff payload and bias-history loader with `toLocalDateIso()`.
- 2026-03-30 10:15 — Verified there are no remaining `toISOString().slice(0, 10)` or `toISOString().split('T')[0]` usages in `strategy_performance.html` and documented the shared helper call sites.

## Changes Made
- `TradeApps/breakout/fs/strategy_performance.html`
  - Updated the summary-to-multi-chart handoff payload to fall back to `toLocalDateIso()` instead of UTC date slicing when no date input is populated.
  - Updated `loadBiasHistoryData()` to fall back to `toLocalDateIso()` instead of UTC date slicing when `statsDate` is unavailable.
  - Preserved the existing local-date helper and existing `Today` preset logic so every selector/default/validation path on the page resolves from the same local calendar date source.

## Validation
- `Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'`
  - Result: `2026-03-30 10:14:30 +01:00`
- `rg -n "toISOString\\(\\)\\.slice\\(0, 10\\)|toISOString\\(\\)\\.split\\('T'\\)\\[0\\]" TradeApps/breakout/fs/strategy_performance.html`
  - Result: no matches
- `Select-String -Path 'TradeApps/breakout/fs/strategy_performance.html' -Pattern 'toLocalDateIso\\(\\)' | ForEach-Object { "{0}:{1}" -f $_.LineNumber, $_.Line.Trim() }`
  - Result: helper usage confirmed at lines `2255`, `2256`, `2322`, `2505`, `2692`, `2730`, `4242`, and `5296`
- User verification request pending
  - Requested check: Open Strategy Performance on 2026-03-30 local time, select `Today`, and confirm the visible range label shows `30 Mar` and no prior-day date appears in the selector flow.

## Risks/Notes
- This task changes user-visible date behavior in the Strategy Performance UI, so final closure still depends on user verification of the rendered label and preset behavior.
- The lifecycle file remains in `workstream/200_inprogress/codex` until that UI verification is captured.

## Completion Status
Awaiting user verification as of 2026-03-30 10:15 +01:00.
