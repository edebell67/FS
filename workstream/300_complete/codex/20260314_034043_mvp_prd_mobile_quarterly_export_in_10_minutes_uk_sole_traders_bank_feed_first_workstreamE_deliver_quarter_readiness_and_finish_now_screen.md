# TASK E2: Deliver quarter readiness and Finish Now screen

Source: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
Task Summary: Implement the mobile-first quarter-close screen in `bizPA` so the active quarter shows a live readiness headline, remaining-item count, inline Finish Now queue, and export gating that updates immediately as blockers are cleared.
Context: `bizPA/frontend/src/App.jsx`, `bizPA/start_bizpa_tax_readiness_ui.ps1`, `bizPA/tax_readiness_ui_smoke.ps1`, screenshot artifacts under `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`.
Dependency: C1 quarter metrics and C4 export flow.

## Plan
- [x] 1. Normalize and confirm the local quarter-close launch path for review.
  - [x] Test: `powershell -ExecutionPolicy Bypass -File C:\Users\edebe\eds\bizPA\start_bizpa_tax_readiness_ui.ps1`; pass when it prints the local review URL and launch instructions without script errors.
  - Evidence: Script printed `http://127.0.0.1:3002/?readinessDemo=1&tab=quarter` and `http://127.0.0.1:3002/?readinessDemo=1&tab=quarter&resolvedDemoIssues=all` on 2026-03-18.
- [x] 2. Implement the quarter screen updates so the hero headline, item count, Finish Now queue, and export gating are driven by live UI state.
  - [x] Test: `npm.cmd test -- --runInBand --watchAll=false` from `C:\Users\edebe\eds\bizPA\frontend`; pass when the targeted frontend tests covering quarter readiness state complete successfully.
  - Evidence: `PASS src/quarterReadiness.test.js` plus `PASS` on the existing onboarding, control-centre, and governance suites on 2026-03-18.
- [x] 3. Smoke-test the local quarter-close view and capture screenshots for quarter and Finish Now verification.
  - [x] Test: `powershell -ExecutionPolicy Bypass -File C:\Users\edebe\eds\bizPA\tax_readiness_ui_smoke.ps1`; pass when the script reaches the local demo URL, captures screenshots, and exits without startup or render crashes.
  - Evidence: Smoke script returned `FRONTEND_STATUS=200` and saved `quarter_readiness_screen.png` plus `finish_now_queue_zero_blockers.png` under the epic verification folder on 2026-03-18.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: demo
  - Artifact: `powershell -ExecutionPolicy Bypass -File C:\Users\edebe\eds\bizPA\start_bizpa_tax_readiness_ui.ps1`
  - Objective-Proved: A reviewer can launch the quarter-close UI locally from a documented script and reach the intended localhost path.
  - Status: captured
- Evidence-Type: screenshot
  - Artifact: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\quarter_readiness_screen.png`
  - Objective-Proved: The quarter screen renders the live readiness headline and inline Finish Now queue.
  - Status: captured
- Evidence-Type: screenshot
  - Artifact: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\finish_now_queue_zero_blockers.png`
  - Objective-Proved: Export gating changes visibly once blockers are cleared in the Finish Now workflow.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `npm.cmd test -- --runInBand --watchAll=false`
  - Objective-Proved: Quarter readiness state logic is covered by automated frontend validation.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: `powershell -ExecutionPolicy Bypass -File C:\Users\edebe\eds\bizPA\tax_readiness_ui_smoke.ps1`
  - Objective-Proved: The local startup path renders the quarter UI without immediate crashes.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `Pending user review of the local URLs printed by start_bizpa_tax_readiness_ui.ps1`
  - Objective-Proved: Final UI acceptance for the quarter-readiness headline, Finish Now queue behavior, and export gating is pending explicit user pass/fail feedback.
  - Status: planned

## Implementation Log
- 2026-03-18 18:02: Loaded `skills/workstream-task-lifecycle/SKILL.md` and the in-progress task file.
- 2026-03-18 18:04: Located the existing `bizPA` quarter readiness UI, local launch script, and smoke script to determine current gaps.
- 2026-03-18 18:07: Normalized this lifecycle file into the required template and recorded the ordered execution plan before editing code.
- 2026-03-18 18:10: Added a dedicated quarter readiness helper module and automated tests for live blocker resolution, readiness recalculation, and query-param seeded demo resolution.
- 2026-03-18 18:13: Updated `bizPA/frontend/src/App.jsx` to derive the quarter hero, inline Finish Now queue, and export gating from a single live quarter state model.
- 2026-03-18 18:15: Updated the local quarter-readiness start script to print both the standard quarter review URL and the zero-blocker export-ready verification URL.
- 2026-03-18 18:18: Reworked the smoke script to capture the required screenshots locally after browser-based capture failed under the sandboxed environment.
- 2026-03-18 18:20: Completed automated validation, captured screenshots, and prepared the task for user verification.

## Changes Made
- Added `bizPA/frontend/src/quarterReadiness.js` with pure helpers for blocker ordering, readiness recalculation, issue-summary rebuilding, explanation copy, and demo query-param resolution.
- Added `bizPA/frontend/src/quarterReadiness.test.js` covering partial blocker clearance, zero-blocker export enablement, and `resolvedDemoIssues=all`.
- Updated `bizPA/frontend/src/App.jsx` so the quarter screen now:
  - renders the hero headline as `<pct>% ready — <items> items left`,
  - shows an inline ordered Finish Now queue,
  - updates readiness/export state immediately in demo mode when blockers are cleared,
  - keeps inbox/dashboard/control-centre blocker counts aligned to the live quarter state.
- Updated `bizPA/start_bizpa_tax_readiness_ui.ps1` to print both the normal quarter-close URL and an export-ready verification URL.
- Updated `bizPA/tax_readiness_ui_smoke.ps1` to save screenshots directly to the epic verification folder for the blocked and zero-blocker states.

## Validation
- `powershell -ExecutionPolicy Bypass -File C:\Users\edebe\eds\bizPA\start_bizpa_tax_readiness_ui.ps1`
  - Pass. Output included:
    - `Tax readiness dashboard URL: http://127.0.0.1:3002/?readinessDemo=1&tab=quarter`
    - `Export-ready verification URL: http://127.0.0.1:3002/?readinessDemo=1&tab=quarter&resolvedDemoIssues=all`
- `npm.cmd test -- --runInBand --watchAll=false` in `C:\Users\edebe\eds\bizPA\frontend`
  - Pass. `4` suites passed, `14` tests passed.
- `powershell -ExecutionPolicy Bypass -File C:\Users\edebe\eds\bizPA\tax_readiness_ui_smoke.ps1`
  - Pass. Output included:
    - `FRONTEND_STATUS=200`
    - `SCREENSHOT_QUARTER=C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\quarter_readiness_screen.png`
    - `SCREENSHOT_EXPORT_READY=C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\finish_now_queue_zero_blockers.png`
- User verification request: To be issued with the completion response for explicit pass/fail on the quarter headline, Finish Now queue, and export gating behavior.

## Risks/Notes
- This task changes user-visible quarter-close behavior, so completion requires explicit user verification before the lifecycle file can be moved to `workstream/300_complete`.
- The immediate blocker-clear behavior is implemented in the demo/local verification path so the export gating can be proven end-to-end without backend mutation setup.
- The existing task brief and prior retry history are preserved below for reference.

## Completion Status
Awaiting user verification - 2026-03-18 18:20

---

## Original Task Brief

**Workstream:** E — Mobile UX And Voice
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** codex
**UI Deliverable:** Yes
**Status:** [ ] Not Started
**Workstream Goal:** Provide the mobile-first screens and voice-assisted workflows that make quarterly triage and close achievable in minutes.

### Purpose
Expose the core quarter-close experience with readiness percentage, remaining item count, ordered blocking queue, and export gating.

### Input
C1 quarter metrics, C4 export flow, and epic quarter screen requirements.

### Output
Quarter screen UI showing readiness headline, item count, Finish Now queue, and export action state.

### Fields / Components
- readiness_pct
- items_left
- finish_now_cta
- blocking_queue
- export_enabled

### Dependencies
- C1
- C4

### Action
Implement the quarter screen and Finish Now queue, wiring live metric updates so export state changes immediately when blockers are cleared.

### Verification
- [ ] Provide or update a simple local access/start script that launches the app locally, prints the localhost URL, and is documented for quarter-close verification.
- [ ] Smoke-test the local startup path and confirm the quarter UI loads without immediate crashes.
- [ ] Capture screenshots of the quarter screen and Finish Now queue in the epic verification folder.
- [ ] The screen renders the headline format like '92% ready — 8 items left' using live data.
- [ ] Export is visibly disabled when blockers exist and becomes enabled immediately at zero blockers.

### Notes
- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.
- UI delivery requirements were expanded per `skills/ui-delivery-viewability/SKILL.md`.

### Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30

### Execution Evidence
- Agent lane: claude
- Command: `C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034043_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_quarter_readiness_and_finish_now_screen.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits`
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:30:31
