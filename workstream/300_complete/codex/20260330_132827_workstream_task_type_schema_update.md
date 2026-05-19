Source: User request on 2026-03-30 to update the workstream lifecycle skill so tasks can declare explicit execution-behavior attributes with required semantics.

Task Type: standard

Task Summary: Update `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md` so it uses an execution-behavior attribute model centered on `recurring_task`, `looping_task`, `splittable_task`, and `workflow_task`, with the corresponding required orchestration fields and rules.

Context:
- Target file: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`

Dependency: None

Plan:
- [x] 1. Add `Task Type` to the required content template with the allowed values and required formatting.
  - [x] Test: Inspect the updated skill file; pass if task-behavior orchestration fields are listed in the required content template with the requested semantics.
  - Evidence: Added `Task Attributes` to the required content template with `recurring_task`, `recurrence_type`, `recurrence_rule`, `looping_task`, `loop_until`, `loop_interval`, `splittable_task`, `split_outputs`, `split_routing`, `split_spawn_task`, `spawn_template`, `split_failure_mode`, `workflow_task`, `workflow_name`, `workflow_stage`, `depends_on`, and `feeds_into`.
- [x] 2. Add execution rules that define how task-type metadata must be recorded.
  - [x] Test: Inspect the updated skill file; pass if the rules cover defaults, multiple behaviors, and the required metadata for `recurring_task`, `looping_task`, `splittable_task`, and `workflow_task`.
  - Evidence: Added non-negotiable execution rules for `split_outputs` plus `split_routing`, `recurrence_rule`, `loop_until`, and `workflow_name` plus `workflow_stage`, along with the default `standard` behavior.
- [x] 3. Validate the skill update.
  - [x] Test: Re-read the updated file; pass if the new task-attribute section is internally consistent and user-requested fields are present.
  - Evidence: Readback confirmed all requested execution attributes and required metadata fields are present in `SKILL.md`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
  - Objective-Proved: The lifecycle skill now defines explicit execution attributes and orchestration rules rather than loose type labels.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: Readback of `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md` showing `Task Attributes`, `recurring_task`, `recurrence_rule`, `looping_task`, `loop_until`, `splittable_task`, `split_outputs`, `split_routing`, `workflow_task`, `workflow_name`, and `workflow_stage`.
  - Objective-Proved: The task-attribute schema was applied and is internally consistent in the live skill file.
  - Status: captured

## Implementation Log
- 2026-03-30 13:28:27 Created lifecycle task for the workstream task-type schema update.
- 2026-03-30 13:31:00 Updated the required content template in `workstream-task-lifecycle` to include `Task Type`.
- 2026-03-30 13:32:00 Added execution rules for default, multiple, recurring, looping, splittable, and workflow task types.
- 2026-03-30 13:33:00 Re-read the updated skill file and confirmed the requested schema landed correctly.
- 2026-03-30 14:05:00 Audited the completed lifecycle file, added the now-required `Task Type: standard` field, and re-validated the live skill content in the workspace.
- 2026-03-30 14:08:00 Refined the skill to align with the stricter task-attribute orchestration model and its non-negotiable execution rules.

## Changes Made
- Added lifecycle file `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260330_132827_workstream_task_type_schema_update.md`.
- Updated `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`.
- Updated `C:\Users\edebe\eds\workstream\300_complete\codex\20260330_132827_workstream_task_type_schema_update.md` to align the record with the current lifecycle schema requirements.
- Replaced the earlier loose `Task Type` guidance in the skill file with an explicit execution-behavior attribute model.

## Validation
- Re-read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`.
- Ran `rg -n "Task Attributes|recurring_task|recurrence_rule|looping_task|loop_until|splittable_task|split_outputs|split_routing|workflow_task|workflow_name|workflow_stage" C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`.
- Validation result: pass.
- Confirmed presence of:
  - `Task Attributes`
  - `standard` default behavior
  - `recurring_task`
  - `recurrence_type`
  - `recurrence_rule`
  - `looping_task`
  - `loop_until`
  - `loop_interval`
  - `splittable_task`
  - `split_output_type`
  - `split_outputs`
  - `split_routing`
  - `split_spawn_task`
  - `spawn_template`
  - `split_failure_mode`
  - `workflow_task`
  - `workflow_name`
  - `workflow_stage`
  - `depends_on`
  - `feeds_into`
- Confirmed the lifecycle record itself now includes `Task Type: standard`.

## Risks/Notes
- The update should stay additive and avoid breaking the current lifecycle format for existing tasks.

## Completion Status
- Complete on 2026-03-30 13:33:00.
