# Task: Review show me skill coverage for on-demand demo verification

## Source
- User request on 2026-03-16 to check the skills for "show me" proving a task has delivered its objective by being able to run a demo on demand.

## Task Summary
- Review the relevant skills and existing "Show Me" task implementation to determine whether the repository already defines a standard that completion should be demonstrated through an on-demand runnable demo.

## Context
- `skills/workstream-task-lifecycle/SKILL.md`
- `skills/ui-delivery-viewability/SKILL.md`
- `workstream/300_complete/20260315_204500_workstream_show_me_verification_button.md`
- `workstream/kanban_dashboard.py`

## Plan
- [x] 1. Review the lifecycle and UI viewability skills for explicit on-demand demo requirements.
  - [x] Test: open the relevant SKILL files and confirm whether they require a runnable demo path beyond screenshots and verification requests.
  - [x] Evidence: `workstream-task-lifecycle` requires user verification requests for user-visible tasks, but does not require a demo launcher. `ui-delivery-viewability` requires a starter script, localhost URL, smoke test, and screenshot for UI tasks, but not a generic "Show Me" mechanism for all task types.
- [x] 2. Review the implemented "Show Me" task and current kanban behavior.
  - [x] Test: inspect the completed task record and current code path in `kanban_dashboard.py` for how `Show Me` works.
  - [x] Evidence: completed task `20260315_204500_workstream_show_me_verification_button.md` defines metadata such as `Deliverable-Type` and `Deliverable-URL/Path`; `kanban_dashboard.py` renders a `Show Me` button only when deliverable metadata or heuristic URL/path extraction is present, and `showDeliverable()` opens URLs or posts file paths to `/api/open-file`.
- [x] 3. Record whether the current standards fully, partially, or do not cover on-demand demo delivery.
  - [x] Test: produce a written conclusion mapping skill requirements to current implementation.
  - [x] Evidence: conclusion captured below: coverage is partial, not complete.

## Implementation Log
- 2026-03-16 11:03:45 Created review task from user request.
- 2026-03-16 11:08:00 Reviewed `skills/workstream-task-lifecycle/SKILL.md`, `skills/ui-delivery-viewability/SKILL.md`, the completed Show Me task record, and the live kanban implementation in `workstream/kanban_dashboard.py`.

## Changes Made
- No code changes. Completed a standards/implementation review only.

## Validation
- Reviewed:
  - `skills/workstream-task-lifecycle/SKILL.md`
  - `skills/ui-delivery-viewability/SKILL.md`
  - `workstream/300_complete/20260315_204500_workstream_show_me_verification_button.md`
  - `workstream/kanban_dashboard.py`
- Result:
  - Skills do not currently define a universal rule that a task must be demonstrable through a single on-demand demo launcher.
  - The closest existing rule is in `ui-delivery-viewability`, which applies to UI deliverables only and requires a starter script plus URL and screenshot evidence.
  - The current "Show Me" capability is implemented as a kanban feature, not as a repository-wide skill requirement.

## Risks/Notes
- Conclusion:
  - `workstream-task-lifecycle` covers verification workflow and user signoff gating.
  - `ui-delivery-viewability` covers runnable access for UI tasks only.
  - The "Show Me" implementation partially supports on-demand demo verification, but only when deliverable metadata/path extraction is present, and it does not guarantee service startup or a runnable demo path for non-UI tasks.
- If the desired standard is "every verification-ready task must support a one-click runnable demo of its objective", that is a gap today and should be captured as a new skill/workstream requirement.

## Completion Status
- Complete - 2026-03-16 11:08 GMT
