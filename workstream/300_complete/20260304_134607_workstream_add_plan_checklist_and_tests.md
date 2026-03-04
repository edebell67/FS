# Task Lifecycle

- Task: Add checklist Plan+Test section to target task MD and update lifecycle skill instructions
- Project: workstream
- Started: 2026-03-04 12:40:00
- Completed: 2026-03-04 12:49:10
- Status: complete

## Updates

### 2026-03-04 12:40:00
- Created lifecycle file in `100_todo` and moved to `200_inprogress`.

### 2026-03-04 12:49:10
- Rewrote `20260303_172508_kanban_real_llm_decomposition.md` into clean markdown format.
- Added `## Plan` section as checklist with explicit test item under each step.
- Updated `skills/workstream-task-lifecycle/SKILL.md` to mandate checklist-format plan and per-step tests for tasks.

## Validation

- `rg -n -F "## Plan" workstream/200_inprogress/20260303_172508_kanban_real_llm_decomposition.md`
  - Confirmed plan section exists.
- `rg -n "Plan\`: checklist|Format requirement|A task may be marked complete only when all required `Plan`" skills/workstream-task-lifecycle/SKILL.md`
  - Confirmed instructions added and enforceable.
