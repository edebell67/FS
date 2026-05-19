Source: User request on 2026-04-28 to update `skills/workstream-task-lifecycle` so fix tasks created from investigations use `_998_` in the filename.
Task Type: standard
Task Attributes:
  recurring_task: false
  recurrence_type: scheduled
  recurrence_rule: None
  looping_task: false
  loop_until: manual_stop
  splittable_task: false
  split_output_type: files
  split_spawn_task: false
  split_failure_mode: fail_fast
  workflow_task: false
  workflow_name: ""
  workflow_stage: in_progress
  depends_on: []
  feeds_into: []
Task Summary: Update the workstream lifecycle skill so implementation work that fixes an already-investigated issue must use `_998_` in the lifecycle filename.
Context: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
Destination Folder: C:\Users\edebe\eds\skills\workstream-task-lifecycle\
Dependency: None
Plan:
- [x] 1. Update the Required Naming section to define `_998_` for fix-followup work derived from an investigation.
  - [x] Test: Read the naming section and confirm `_998_` guidance appears alongside `_999_`.
  - Evidence: `SKILL.md` now includes “Fix-followup task files” with the example `yyyymmdd_hhmmss_{project}_998_{unique_task}.md`.
- [x] 2. Update any related execution guidance so the `_998_` rule is unambiguous in practice.
  - [x] Test: Read the surrounding workflow rules and confirm the fix-followup case is described clearly.
  - Evidence: The added bullets state that `_998_` applies when work is implementing or validating a fix for an issue concluded by an `_999_` investigation, and that a distinct `_998_` task should be started instead of continuing under the investigative filename.
Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
  - Objective-Proved: Skill text was updated to add the `_998_` naming rule.
  - Status: captured
Execution Log:
- 2026-04-28 14:15:54: Task file created in `workstream/100_todo`.
- 2026-04-28 14:16:00: Added `_998_` naming guidance to the Required Naming section in `SKILL.md`.
- 2026-04-28 14:17:00: Read back the updated naming block and confirmed the new fix-followup rule is explicit and unambiguous.
