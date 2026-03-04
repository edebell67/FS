# Task Summary
Update the filenames of all task documents within the new agentic backlog folders (`000_backlog/codex`, `000_backlog/gemini`, `000_backlog/claude`) to explicitly include the agent's name in the filename schema. 

# Context
We need better file-level traceability of which agent created or is assigned to a specific task file, independent of the folder it sits in. The current format is `yyyymmdd_hhmmss_{project}_{description}.md`. We are updating this schema for agent-assigned tasks to be `yyyymmdd_hhmmss_{agent name}_{project}_{description}.md`.

Example:
**Old:** `20260222_212458_bizPA_Strategic_Refinement_v3.md`
**New:** `20260222_212458_gemini_bizPA_Strategic_Refinement_v3.md`

# Implementation Plan
1. **Script/Manual Renaming:**
   - Iterate through the files in `000_backlog/codex`, `000_backlog/gemini`, and `000_backlog/claude`.
   - Identify files adhering to the timestamp prefix `^\d{8}_\d{6}_`.
   - Reconstruct the filename by injecting the directory's agent name directly after the timestamp.
2. **Dashboard Parser Updates (Mandatory):**
   - Update `kanban_dashboard.py` API file parsing Regex. The current regex `pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")` incorrectly assigns the first field after the timestamp as the `project`.
   - Modify the python parser logic so that if the first field matches an agent name (`codex`, `gemini`, `claude`, `general`), it treats that as the `agent_name` and assigns the second field as the `project`.

3. **Dynamic Drag-and-Drop Renaming:**
   - Modify the `/api/move-task` endpoint logic in `KanbanHandler`.
   - When a ticket is dragged from one agent to another (e.g., from `codex` to `gemini`), the python backend must automatically parse the filename, strip the old `codex_` token from it, and prepend the new target folder agent's identifier `gemini_` before saving it to the new location.
   - Example: dragging `20260222_212458_claude_bizPA_Strategic_Refinement_v3.md` into `gemini` changes it seamlessly to `20260222_212458_gemini_bizPA_Strategic_Refinement_v3.md` during the drop.

# Changes To Make
- Write a quick python utility script or use bash commands to perform the bulk renaming of existing files inside the agent folders.
- Verify `kanban_dashboard.py` doesn't break when reading these new file structures.

# Validation Steps
* [ ] Verify files in `000_backlog/gemini` have `gemini_` injected after their timestamp.
* [ ] Verify files in `000_backlog/codex` have `codex_` injected after their timestamp.
* [ ] Verify files in `000_backlog/claude` have `claude_` injected after their timestamp.
* [ ] Ensure the Kanban Dashboard correctly loads and the Kanban project groups parse the correct `{project}` instead of grouping natively under the agent name.
* [ ] Verify dynamic drag-and-drop: Drag a card from Codex to Gemini and ensure the filename changes from `...codex...` to `...gemini...` and reloads correctly.
