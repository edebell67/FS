# Add Review Lane User Decision Actions

## Metadata
- Project: workstream
- Task: add_review_lane_user_decision_actions
- Started: 2026-03-22 00:14:00
- Status: complete

## Source
- User request in Codex thread on 2026-03-22 to add clear buttons for `050_review` items awaiting user input so they can move either back to `100_backlog/general` for more work or to `300_complete` after successful review.

## Task Summary
Update the kanban review-lane UX and backend so ordinary tasks in `050_review` expose explicit user-decision actions and route rejected items to `100_backlog/general` instead of leaving them stranded.

## Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect the current `050_review` UI and verify-task backend path.
  - Test: Locate the current review buttons and `/api/verify-task` move logic.
  - Evidence: Confirmed ordinary task verification used `/api/verify-task`, but review cards only showed verify actions while still in `200_inprogress`.
- [x] 2. Update the review-lane task UI to expose review decision actions.
  - Test: Ensure `050_review` user-verification tasks show a review/verify action.
  - Evidence: Updated `createCardHtml()` so `050_review` cards with `needs_verification` expose a `REVIEW` button that opens the same verification modal used for user pass/fail.
- [x] 3. Route failed/rework review outcomes back to `100_backlog/general`.
  - Test: Verify backend move logic sends failed `050_review` items to general backlog and pass moves to complete.
  - Evidence: Updated `/api/verify-task` to route failed items originating from `050_review` to `100_backlog/general`, while pass still routes to `300_complete/{agent}`.
- [x] 4. Validate the updated dashboard module.
  - Test: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Evidence: Module compiles after the review-lane changes; only the pre-existing `SyntaxWarning` remains.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: Review-lane tasks now expose explicit review action buttons and rejected review items route back to `100_backlog/general`.
  - Status: verified
- Evidence-Type: command
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: Updated dashboard module compiles successfully.
  - Status: verified

## Execution Notes
- 2026-03-22 00:18: Confirmed the existing backend already supported `/api/verify-task`, but the card UI only exposed verify controls while tasks were still in `200_inprogress`.
- 2026-03-22 00:20: Updated `createCardHtml()` so `050_review` verification tasks show a `REVIEW` button that opens the existing verification modal.
- 2026-03-22 00:22: Updated `/api/verify-task` so failed decisions from `050_review` route to `100_backlog/general`, matching the intended rework flow.
- 2026-03-22 00:23: Recompiled `kanban_dashboard.py` successfully after the change.

## Validation
- [x] Locate current `050_review` decision flow.
- [x] Confirm review cards now expose a verify/review action.
- [x] Confirm rejected review items route to `100_backlog/general`.
- [x] Run `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`.
