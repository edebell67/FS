# Task: Standardize task evidence and make it mandatory via skills

## Source
- User request on 2026-03-16: standardize task evidence via skills and make it mandatory.
- Related review: `workstream/300_complete/20260316_110345_workstream_review_show_me_skill_demo_on_demand_coverage.md`

## Task Summary
- Update the repository skills so workstream tasks use a consistent evidence schema and so that evidence declaration becomes mandatory for qualifying tasks.

## Context
- `skills/workstream-task-lifecycle/SKILL.md`
- `skills/document-to-task-decomposition/SKILL.md`

## Plan
- [x] 1. Define a concise mandatory evidence model in the lifecycle skill.
  - [x] Test: update `skills/workstream-task-lifecycle/SKILL.md` with required evidence sections, evidence types, and completion rules.
  - [x] Evidence: added mandatory `Evidence` section schema, allowed `Evidence-Type` values, completion gating for required evidence items, and explicit evidence rules in `skills/workstream-task-lifecycle/SKILL.md`.
- [x] 2. Align task-generation guidance so new tasks are created with the same evidence structure.
  - [x] Test: update `skills/document-to-task-decomposition/SKILL.md` to require the evidence schema in generated tasks.
  - [x] Evidence: decomposition skill now requires `Evidence` in generated tasks, adds evidence clarity as a key principle, and includes an `Evidence` block in the example task structure.
- [x] 3. Validate that both skills now express the requirement clearly and consistently.
  - [x] Test: run `rg` over the updated skills for the new evidence headings and mandatory rules.
  - [x] Evidence: `rg` confirmed the new required language in both skills, including `Evidence Rules`, `Evidence-Type: <type>`, `required evidence items`, `normalized proof inventory`, and `Evidence clarity`.

## Implementation Log
- 2026-03-16 11:25:16 Created task from user request.
- 2026-03-16 11:28:00 Updated `skills/workstream-task-lifecycle/SKILL.md` to add a mandatory normalized `Evidence` section, standard evidence types, and completion rules that require captured evidence before task completion.
- 2026-03-16 11:29:00 Updated `skills/document-to-task-decomposition/SKILL.md` so newly generated tasks include the same evidence schema from the start.
- 2026-03-16 11:30:00 Validated the changes with `rg` against both skill files.

## Changes Made
- Updated [SKILL.md](C:/Users/edebe/eds/skills/workstream-task-lifecycle/SKILL.md):
  - Added mandatory `Evidence` section to the required task content template.
  - Standardized allowed evidence types: `demo`, `url`, `screenshot`, `test_output`, `log_output`, `file_output`, `diff`, `manual_verification`, `user_feedback`, `not_applicable`.
  - Added completion rule that required evidence items must be `captured` or `not_applicable` before completion.
  - Added evidence handling under the user verification gate.
- Updated [SKILL.md](C:/Users/edebe/eds/skills/document-to-task-decomposition/SKILL.md):
  - Required generated tasks to include `Evidence`.
  - Added evidence clarity as a decomposition principle.
  - Updated the example task structure to include a normalized `Evidence` block.

## Validation
- Command:
  - `rg -n "Evidence Rules|Evidence-Type: <type>|required evidence items|normalized proof inventory|Evidence clarity" skills\workstream-task-lifecycle\SKILL.md skills\document-to-task-decomposition\SKILL.md`
- Result:
  - `skills\document-to-task-decomposition\SKILL.md:41:   - Evidence: normalized proof inventory using the lifecycle schema`
  - `skills\document-to-task-decomposition\SKILL.md:62:- Evidence clarity: every generated task must declare what artifact will prove completion, not just what test will be run.`
  - `skills\workstream-task-lifecycle\SKILL.md:79:    - \`- Evidence-Type: <type>\``
  - `skills\workstream-task-lifecycle\SKILL.md:106:- A task may be marked complete only when its \`Evidence\` section contains the required evidence items and each required item is \`captured\` or explicitly \`not_applicable\`.`
  - `skills\workstream-task-lifecycle\SKILL.md:124:  3. required evidence items are captured,`
  - `skills\workstream-task-lifecycle\SKILL.md:127:## Evidence Rules`
  - `skills\workstream-task-lifecycle\SKILL.md:129:- \`Validation\` remains the narrative of commands/checks performed; \`Evidence\` is the normalized proof inventory.`

## Risks/Notes
- The evidence schema must stay concise enough that task files remain usable.
- This task updates repository process rules, not existing historical task files retroactively.
- Existing completed task files are not automatically normalized; the rule applies going forward unless a retrofit task is explicitly requested.

## Completion Status
- Complete - 2026-03-16 11:30 GMT
