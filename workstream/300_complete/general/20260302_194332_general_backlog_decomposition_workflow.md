# Task Summary
Add logic to the multi-model lane worker to automatically process unprocessed backlog files. When a backlog item is dropped into an agent-specific `000_backlog` folder (e.g. `000_backlog/codex`, excluding `general`), the worker should generate atomic tasks in `100_todo` and rename the backlog file to end with `_processed.md`.

# Context
We've set up the lane execution system for `100_todo`, `200_inprogress`, and `300_complete`, but the very first step—"Backlog Ingestion and Decomposition"—needs to be hooked into the daemon loop. The `000_backlog/{agent}` folders are waiting to be monitored.

# Implementation Plan
1. **Detect Backlog Files**: Update `multi_model_lane_worker` in `kanban_dashboard.py` to check `000_backlog/{agent}/` (ignoring `general`) for `.md` files that do NOT contain `_processed` at the end of the filename (before the `.md`).
2. **Check Agent Capacity Constraints**:
   - The daemon should ONLY trigger backlog task decomposition if there are **NO** tasks inside `100_todo/{agent}/` and **NO** tasks in `200_inprogress/{agent}/`.
   - If the agent is currently busy or already has atomic backlog items waiting in its `100_todo` queue, ignore the `000_backlog` file until its queue matches zero.
3. **Execute Decomposition Prompt**:
   - If conditions are met, invoke the headless agent CLI pointing to the `.md` backlog file and provide a standard system prompt instructing it to split the document down into atomic task markdown files and save them to `100_todo/{agent}/`.
4. **Mark as Processed**:
   - Once the atomic tasks have been confirmed explicitly generated, the worker script must rename the original backlog file to `{filename_without_md}_processed.md`. This indicates the backlog has been broken down and prevents the agent from triggering the decomposition process loop continuously.
5. **Update Skills**: I've already updated the `workstream-task-lifecycle` SKILL.md file to capture this backlog renaming standard.

# Validation Steps
* [ ] Create a dummy backlog file `20261111_000000_general_test_backlog.md` inside `000_backlog/gemini`.
* [ ] Ensure Gemini has zero tasks in `100_todo` or `200_inprogress`.
* [ ] The queue worker should automatically detect the backlog, simulate decomposition (e.g. create a dummy atomic task), and rename the backlog file to `20261111_000000_general_test_backlog_processed.md`.
* [ ] It should NOT process the backlog if a task is actively inside `100_todo`.
