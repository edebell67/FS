Source:
- User request on 2026-03-12 to update decomposition so newly generated epic tasks include ordering metadata by default.

Task Summary:
- Update the epic decomposition skill so tasks generated from an epic include execution-order metadata and dependency gating fields aligned with the new `task-execution-ordering` skill.

Context:
- Primary target: `skills/epic-decomposition/SKILL.md`.
- New ordering skill already exists at `skills/task-execution-ordering/`.
- Output format must remain usable by different models working on the same epic.

Plan:
- [x] 1. Move this lifecycle file to in-progress and update the epic decomposition skill instructions.
  - [x] Test: Confirm the lifecycle file exists in `workstream/200_inprogress` and `skills/epic-decomposition/SKILL.md` is updated.
  - Evidence: Lifecycle file moved to `workstream/200_inprogress/20260312_153141_skills_update_epic_decomposition_with_ordering_metadata.md`; `skills/epic-decomposition/SKILL.md` updated with ordering-aware decomposition guidance.
- [x] 2. Add default epic ordering metadata to the generated task template, extraction rules, and validation guidance.
  - [x] Test: Review `skills/epic-decomposition/SKILL.md` and confirm it now specifies `Epic Sequence`, `Depends On`, `Blocks`, and `Readiness`.
  - Evidence: Task template, extraction table, decomposition algorithm, example task file, and validation checklist now all include `Epic Sequence`, `Depends On`, `Blocks`, and `Readiness`.
- [x] 3. Validate that the edited skill content is internally consistent and archive the lifecycle record.
  - [x] Test: Re-read the updated skill and confirm the example task file and checklist reflect the new metadata.
  - Evidence: Reviewed `skills/epic-decomposition/SKILL.md`; example task header uses the new fields and the validation checklist enforces metadata completeness plus dependency/readiness consistency.

Implementation Log:
- 2026-03-12 15:31:41: Task file created in `workstream/100_todo`.
- 2026-03-12 15:32:10: Task file moved to `workstream/200_inprogress`.
- 2026-03-12 15:34:30: Updated `skills/epic-decomposition/SKILL.md` to emit epic ordering metadata and reference `$task-execution-ordering` for ambiguous dependencies.
- 2026-03-12 15:35:10: Re-read the edited skill to confirm template, example, and checklist consistency.

Changes Made:
- Updated `skills/epic-decomposition/SKILL.md`.

Validation:
- Manual review of `skills/epic-decomposition/SKILL.md`
  - Result: task template, extraction rules, dependency mapping, example task file, and validation checklist consistently require `Epic Sequence`, `Depends On`, `Blocks`, and `Readiness`.

Risks/Notes:
- The decomposition guidance must add sequencing without over-constraining work that can run in parallel.
- The skill preserves parallel execution by allowing sibling numbering such as `1.1` and `1.2` within the same dependency layer.

Completion Status:
- Complete on 2026-03-12 15:35:10.
