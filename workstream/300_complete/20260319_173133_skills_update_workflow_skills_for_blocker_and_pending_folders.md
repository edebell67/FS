Priority: 2

# Task Summary
Update the relevant local workflow skills so their documented lifecycle/process guidance reflects the current kanban pipeline behavior that now includes `blocker` handling and `pending` subfolders for parked items in active columns.

# Context
- `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
- `C:\Users\edebe\eds\skills\task-execution-ordering\SKILL.md`
- Any other local skill file whose instructions describe lifecycle folders or queue movement behavior

Dependency: `C:\Users\edebe\eds\workstream\200_inprogress\20260319_171503_workstream_kanban_epic_focus_pipeline_mode.md`

# Plan
- [x] 1. Review the workflow-related skill files and identify which instructions are now stale due to blocker and pending folder behavior.
  - [x] Test: Read the relevant skill markdown files and compare their documented folder/lifecycle rules against the implemented kanban behavior.
  - [x] Evidence: Identified stale lifecycle guidance in `skills/workstream-task-lifecycle/SKILL.md` and stale readiness-state guidance in `skills/task-execution-ordering/SKILL.md`.
- [x] 2. Update the affected skill documentation to describe blocker handling and pending folder semantics accurately and concisely.
  - [x] Test: Re-read the changed sections and verify the wording matches the current lifecycle and queue behavior.
  - [x] Evidence: Updated both skill files to document `pending` subfolders plus blocker lanes under `100_backlog` / `200_inprogress`.
- [x] 3. Validate the final skill text for internal consistency with the current app behavior and task lifecycle guidance.
  - [x] Test: Review updated skills side by side with `workstream/kanban_dashboard.py` focus/blocker logic and confirm no contradictory instructions remain.
  - [x] Evidence: `rg -n "pending|blocker|200_inprogress/blocker|100_backlog/pending|200_inprogress/pending" workstream/kanban_dashboard.py` plus post-edit file reads confirmed alignment.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, `C:\Users\edebe\eds\skills\task-execution-ordering\SKILL.md`
  - Objective-Proved: The skill files were updated to include blocker and pending folder workflow guidance.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: Post-edit review against `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: The updated skill instructions align with the live workflow behavior.
  - Status: captured

# Implementation Log
- 2026-03-19 17:31:33: Created task from user request to update workflow skills for blocker and pending folder behavior.
- 2026-03-19 17:33:00: Read `skills/skills-main/skills/skill-creator/SKILL.md` and used it as guidance for a targeted skill update rather than creating a new skill.
- 2026-03-19 17:34:00: Reviewed `skills/workstream-task-lifecycle/SKILL.md` and `skills/task-execution-ordering/SKILL.md` against the current kanban implementation.
- 2026-03-19 17:36:00: Updated `workstream-task-lifecycle` to include `pending` subfolders, blocker lanes, and parking semantics in lifecycle rules.
- 2026-03-19 17:37:00: Updated `task-execution-ordering` so readiness checks treat `pending` and blocker-lane tasks as unresolved, not complete.
- 2026-03-19 17:38:00: Tightened wording to reflect that blocker lanes may exist under both `100_backlog` and `200_inprogress`.

# Changes Made
- Updated `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`:
  - expanded the description
  - documented `100_backlog/pending`, `100_backlog/blocker`, `200_inprogress/pending`, and `200_inprogress/blocker`
  - added queue-state semantics and lifecycle rules for parked/blocked work
  - updated the example flow to include `pending` and blocker parking
- Updated `C:\Users\edebe\eds\skills\task-execution-ordering\SKILL.md`:
  - expanded trigger description to include blocker lanes and `pending`
  - added parked-work checks to epic task discovery and readiness gating
  - clarified that `pending` and blocker-lane tasks are not complete and must still be respected as dependencies

# Validation
- Read:
  - `skills/workstream-task-lifecycle/SKILL.md`
  - `skills/task-execution-ordering/SKILL.md`
  - `workstream/kanban_dashboard.py`
- Confirmed the updated skill wording matches the implemented state model:
  - `pending` subfolders exist conceptually for active states
  - blocker lanes exist in configured folders and are used by the worker pipeline
  - parked work is not treated as ready or complete

# Risks/Notes
- Skills should describe current behavior without over-specifying transient implementation details.
- This was a documentation-only update; no runtime code changed in this task.

# Completion Status
- Complete.
