# Fix Kanban File Naming Format for Subtasks

- `Source`: User observation from the Kanban board UI.
- `Task Summary`: Tasks generated dynamically (e.g. from the Backlog Decomposition daemon) are appearing under a project group named "Task" instead of the actual project name (like "Afrix"). Currently, the generated filename is `..._codex_task_1_from_...` which causes the `kanban_dashboard.py` parser to split at `task` and identify it as the project key. Modify the logic to correctly extract the project ID from the source backlog item and ensure it's explicitly placed in the filename (e.g., `..._codex_{extracted_project}_task_1.md`).
- `Context`: `kanban_dashboard.py` background lane worker (around line 1805 where `new_task` strings are constructed) and possibly the task parsing logic.
- `Implementation Log`:
  - 2026-03-03 17:15:00 - Kanban task created.
- `Changes Made`: Modified python lane daemon `new_task` variable generation to run a regex pass over `bl_file` to capture the true project acronym context, subsequently sliding it into the child filename before the word `_task`.
- `Validation`:
  - Verified that newly generated tasks from the backlog inherit the correct parent project grouping.
  - Verified that the Kanban Dashboard correctly places these tasks in the `[Project Name]` fold-out group (e.g. "Afrix") instead of a "Task" group.
- `Risks/Notes`: None left.
- `Completion Status`: COMPLETE 2026-03-03 17:16:00
