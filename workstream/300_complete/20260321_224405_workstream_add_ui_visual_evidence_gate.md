# Add UI Visual Evidence Gate

## Metadata
- Project: workstream
- Task: add_ui_visual_evidence_gate
- Started: 2026-03-21 22:44:05
- Status: complete

## Source
- User request in Codex thread on 2026-03-21 to incorporate an actual visual deliverable check successfully for UI tasks.

## Task Summary
Add a stricter UI evidence gate so user-facing tasks cannot pass review or enter review-ready state with blank or otherwise invalid screenshot evidence.

## Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect the existing completion and review validation paths for UI tasks.
  - Test: Locate the functions that validate completion and auto-accept review items.
  - Evidence: Confirmed `_validate_task_completion`, `_task_completion_gate`, and `_execute_task` are the relevant acceptance and review-handoff points in `kanban_dashboard.py`.
- [x] 2. Implement a UI screenshot-evidence validator and wire it into task validation.
  - Test: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Evidence: Added UI visual-evidence enforcement in both `_validate_task_completion` and `_task_completion_gate`, plus pre-review rejection in `_execute_task` for invalid UI screenshots.
- [x] 3. Validate the new gate against the known blank `C3` screenshot artifact.
  - Test: Direct import check confirms the validator flags `frontend_social_proof.png` as invalid visual evidence.
  - Evidence: Validator returned `screenshot_mostly_blank:frontend_social_proof.png:1.00` and `_task_completion_gate` returned `visual_evidence_invalid:...`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: C:\Users\edebe\eds\workstream\kanban_dashboard.py
  - Objective-Proved: UI tasks now require valid screenshot evidence before auto-validation or review handoff can pass.
  - Status: verified
- Evidence-Type: command
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: Updated kanban module compiles successfully.
  - Status: verified
- Evidence-Type: command
  - Artifact: Direct import check against `frontend_social_proof.png`
  - Objective-Proved: Known blank `C3` screenshot is rejected with `screenshot_mostly_blank`.
  - Status: verified

## Execution Notes
- 2026-03-21 22:49: Wired `_validate_ui_visual_evidence()` into `_validate_task_completion()` so review auto-validation rejects bad UI screenshot evidence.
- 2026-03-21 22:50: Wired `_validate_ui_visual_evidence()` into `_task_completion_gate()` so completion gating fails UI tasks with invalid screenshots.
- 2026-03-21 22:51: Added pre-review rejection in `_execute_task()` so tasks marked `Awaiting user verification` do not enter `050_review` with blank/missing screenshot evidence.
- 2026-03-21 22:52: Validated the gate against the existing `C3` artifact and confirmed the blank screenshot is detected.

## Validation
- [x] Locate the UI-task validation points.
- [x] Run `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`.
- [x] Confirm the new gate rejects the blank `C3` screenshot.
