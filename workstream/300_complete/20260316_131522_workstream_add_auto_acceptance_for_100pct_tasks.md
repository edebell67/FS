# Task: Add auto-acceptance for 100% evidence-complete tasks

## Source
- User request on 2026-03-16 to allow auto-acceptance for `100%` completed tasks when a new `Auto-Acceptance` flag is `true` by default, while retaining `Show Me` for accepted tasks.

## Task Summary
- Update the workstream rules and kanban behavior so tasks with `Objective-Delivery-Coverage: 100%` and `Auto-Acceptance: true` can be auto-accepted.
- Keep `Show Me` available after acceptance so reviewers can open evidence on demand from accepted tasks.

## Context
- `skills/workstream-task-lifecycle/SKILL.md`
- `skills/document-to-task-decomposition/SKILL.md`
- `workstream/kanban_dashboard.py`

## Plan
- [x] 1. Extend the task evidence schema with a mandatory auto-acceptance flag.
  - [x] Test: update the relevant skills to require `Auto-Acceptance: true|false` with default `true`.
  - [x] Evidence: both skill files now define `Auto-Acceptance` as mandatory alongside `Objective-Delivery-Coverage`.
- [x] 2. Implement kanban parsing and automatic promotion for eligible tasks.
  - [x] Test: update `kanban_dashboard.py` to parse `Auto-Acceptance`, auto-move eligible tasks from `200_inprogress` to `300_complete`, and record the auto-accept event.
  - [x] Evidence: `_parse_auto_acceptance()` and `_auto_accept_task()` are present, and task parsing calls `_auto_accept_task()` when coverage is `100%` and auto-acceptance is enabled.
- [x] 3. Keep Show Me available for accepted tasks.
  - [x] Test: update the task card UI so evidence review is accessible for tasks in `300_complete`.
  - [x] Evidence: `openEvidenceModal()` and a card-level `SHOW ME` button are rendered for tasks with evidence regardless of folder state.
- [x] 4. Validate the implementation.
  - [x] Test: run syntax validation and targeted rule/path checks.
  - [x] Evidence: `python -m py_compile workstream\kanban_dashboard.py` passed and `rg` confirmed the new rules/handlers.

## Implementation Log
- 2026-03-16 13:15:22 Created task from user request.
- 2026-03-16 13:20:00 Updated the lifecycle and decomposition skills so tasks must declare `Auto-Acceptance: true|false`, defaulting to `true`.
- 2026-03-16 13:24:00 Updated `kanban_dashboard.py` to parse the new field and auto-promote eligible `100%` verification tasks into `300_complete`.
- 2026-03-16 13:28:00 Added a separate evidence-review modal path so `SHOW ME` is available for accepted tasks and not tied only to manual verify flow.
- 2026-03-16 13:29:00 Ran syntax validation and targeted searches.

## Changes Made
- Updated `skills/workstream-task-lifecycle/SKILL.md`:
  - Added mandatory `Auto-Acceptance: true|false` under `Evidence`.
  - Defined auto-acceptance eligibility as `Objective-Delivery-Coverage: 100%` plus `Auto-Acceptance: true`.
  - Allowed completion via either manual verification or auto-acceptance criteria.
- Updated `skills/document-to-task-decomposition/SKILL.md`:
  - Required generated tasks to include `Auto-Acceptance: true|false`.
- Updated `workstream/kanban_dashboard.py`:
  - Added `_parse_auto_acceptance()` and `_auto_accept_task()`.
  - Auto-promotes eligible tasks from `200_inprogress` to `300_complete` during task refresh.
  - Records an `# Auto Acceptance` block in the task file when auto-accepted.
  - Added card-level `SHOW ME` buttons and `openEvidenceModal()` so accepted tasks retain on-demand evidence review.

## Validation
- `python -m py_compile workstream\kanban_dashboard.py`
  - Passed.
- `rg -n "Auto-Acceptance|_auto_accept_task|openEvidenceModal|SHOW ME|auto_acceptance|Objective-Delivery-Coverage" workstream\kanban_dashboard.py skills\workstream-task-lifecycle\SKILL.md skills\document-to-task-decomposition\SKILL.md`
  - Confirmed the new rules and handlers are present in both skill files and the kanban code.

## Evidence
- Objective-Delivery-Coverage: 90%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `python -m py_compile workstream\kanban_dashboard.py`
  - Objective-Proved: The updated kanban dashboard code is syntactically valid.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: Auto-acceptance parsing/promotion and accepted-task evidence review were implemented.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
  - Objective-Proved: Repository process rules now require the auto-acceptance field and define its meaning.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\skills\document-to-task-decomposition\SKILL.md`
  - Objective-Proved: Newly created tasks will include the auto-acceptance field by default.
  - Status: captured

## Risks/Notes
- Auto-acceptance must not hide evidence access; accepted tasks still need on-demand review.
- `Objective-Delivery-Coverage` is `90%`, not `100%`, because I validated the code paths and rule wiring but did not perform a live interactive kanban session that demonstrates an actual auto-promotion end to end in the browser.

## Completion Status
- Complete - 2026-03-16 13:29 GMT
