Source: User request to create a task for updating the orchestrator skill so it interprets task types directly from the task file and executes the correct behavior for each type.

Task Attributes:
- standard task

Task Summary:
- Update `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md` so the orchestrator skill reads task-type or task-attribute metadata from a lifecycle task file, chooses the correct execution behavior for that task type, and applies the correct end-of-lifecycle action according to the rules documented in `C:\Users\edebe\eds\workstream\300_complete\codex\20260330_132827_workstream_task_type_schema_update.md`.

Context:
- Source rules: `C:\Users\edebe\eds\workstream\300_complete\codex\20260330_132827_workstream_task_type_schema_update.md`
- Target skill: `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md`
- Supporting lifecycle schema: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`

Dependency:
- `C:\Users\edebe\eds\workstream\300_complete\codex\20260330_132827_workstream_task_type_schema_update.md`

Plan:
- [x] 1. Read the completed task-type schema update and extract the authoritative task types, execution attributes, and lifecycle-action rules the orchestrator must follow.
  - [x] Test: Re-read `C:\Users\edebe\eds\workstream\300_complete\codex\20260330_132827_workstream_task_type_schema_update.md`; pass if the orchestrator behavior matrix can be enumerated from the documented schema.
  - Evidence: Captured behavior requirements for `standard`, `recurring_task`, `looping_task`, `splittable_task`, `workflow_task`, multi-attribute combinations, lifecycle-end gates, and task-file authority rules.
- [x] 2. Update `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md` so it explicitly instructs the model to inspect task-file metadata first and branch behavior by task type or execution attributes.
  - [x] Test: Inspect the updated skill; pass if it requires task-file parsing before allocation/execution decisions and maps each supported task type/attribute to a defined execution path.
  - Evidence: `SKILL.md` now contains `Source of Truth`, `Read the Task File First`, `Task Type Interpretation`, and `Combined Attribute Rules`.
- [x] 3. Add end-of-lifecycle routing guidance so the orchestrator knows what action to take when each task type reaches completion.
  - [x] Test: Inspect the updated skill; pass if completion handling is defined per supported task type/attribute.
  - Evidence: `SKILL.md` now contains explicit lifecycle-end actions for `standard`, `recurring_task`, `looping_task`, `splittable_task`, and `workflow_task`, plus a shared `Lifecycle-End Gates` section.
- [x] 4. Validate that the updated skill remains concise, internally consistent, and aligned with the workstream lifecycle schema.
  - [x] Test: Re-read `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md`; pass if task-file interpretation, execution behavior, and lifecycle-end actions are all present without contradicting the lifecycle skill.
  - Evidence: Readback confirmed the approved measurable `loop_until` rule, workflow-stage advancement by explicit completion criteria, and lifecycle-file-authority requirements are present.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md`
  - Objective-Proved: The orchestrator skill was updated to interpret task-file task types and route execution/lifecycle actions correctly.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md`
  - Objective-Proved: Shows the exact behavioral additions for task-type interpretation and end-of-lifecycle handling.
  - Status: captured

Implementation Log:
- 2026-03-31 03:24:44 GMT: Read `C:\Users\edebe\eds\workstream\300_complete\codex\20260330_132827_workstream_task_type_schema_update.md` to confirm the authoritative task-type schema and orchestration fields.
- 2026-03-31 03:24:44 GMT: Created this lifecycle task to scope the orchestrator-skill enhancement before implementation.
- 2026-03-31 03:27:37 GMT: Reviewed the gap between the lifecycle schema and the original orchestrator skill and identified missing task-file interpretation, task-type branching, lifecycle-end behavior, combined-attribute rules, terminology resolution, and lifecycle-file maintenance requirements.
- 2026-03-31 03:27:37 GMT: Updated `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md` to make task-file metadata authoritative and add schema-driven execution behavior.
- 2026-03-31 03:27:37 GMT: Incorporated the approved refinements that `loop_until` must be discrete and measurable and that workflow-stage advancement must be based on explicit completion criteria across constituent workflow stages/tasks.
- 2026-03-31 03:27:37 GMT: Re-read the updated skill and verified the required rules landed in the live file.

Changes Made:
- Added lifecycle task file `C:\Users\edebe\eds\workstream\100_todo\20260331_032444_skills_update_task_orchestrator_for_task_type_interpretation.md`.
- Rewrote `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md` to:
  - require reading the lifecycle task file first
  - treat `Task Attributes` as the source of truth for execution behavior
  - define execution and lifecycle-end actions for `standard`, `recurring_task`, `looping_task`, `splittable_task`, and `workflow_task`
  - define precedence when multiple task attributes are active
  - require lifecycle-file maintenance during orchestration
  - enforce measurable `loop_until` conditions
  - require workflow stage advancement only when explicit completion criteria are met across constituent stages/tasks

Validation:
- Re-read `C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md`.
- Ran `rg -n "Always read the lifecycle task file first|Task Attributes win|loop_until must be discrete and measurable|workflow as an amalgamation|Advance `workflow_stage` only|Do not mark the workflow complete unless all required stages|The lifecycle file must remain authoritative" C:\Users\edebe\eds\skills\task-orchestrator\SKILL.md`.
- Validation result: pass.

Risks/Notes:
- The source schema uses execution-behavior attributes rather than loose labels alone, so the orchestrator skill must prioritize task-file attribute interpretation over simplistic string matching.
- The orchestrator skill should remain advisory/instructional; actual agent delegation still depends on runtime permissions and policies.

Completion Status:
- Complete - 2026-03-31 03:27:37 GMT
