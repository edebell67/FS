# Task Summary
Replicate the agent folder structure (`codex`, `gemini`, `claude`, `general`) and associated drag-and-drop / file renaming functionality currently available in `000_backlog` into the `100_todo` and `200_inprogress` kanban columns.

# Context
As established in `20260301_220813_kanban_agent_filename_schema.md`, tasks are being moved into agent-specific subfolders (`000_backlog/codex`, etc.). The Kanban dashboard groups these nicely under the Backlog column and automatically injects/strips agent tags from filenames during drag-and-drop.
The user wants this exact same functionality extended to the To Do (`100_todo`) and In Progress (`200_inprogress`) columns. This means creating the directories, parsing the files within them, grouping them visually on the board, and supporting dynamic filename adjustments during cross-column or cross-agent drag-and-drop events within these states.

# Implementation Plan
1. **Directory Structure Creation:**
   - Create directories: `100_todo/codex`, `100_todo/gemini`, `100_todo/claude`, `100_todo/general`.
   - Create directories: `200_inprogress/codex`, `200_inprogress/gemini`, `200_inprogress/claude`, `200_inprogress/general`.

2. **Dashboard Updates (`kanban_dashboard.py`):**
   - Update `FOLDERS` array to include these new paths.
   - Refactor the front-end Javascript `renderBoard` function. The logic that sets `isDummy`, `t.kanbanGroup`, and `t.dropFolder` for `000_backlog` needs to be generalized or repeated for `100_todo` and `200_inprogress`.
   - Ensure the UI groups them under the respective column headers with expand/collapse capability just like Backlog and Complete columns.

3. **Backend API Adjustments:**
   - Verify `/api/move-task` correctly handles paths like `100_todo/codex`. The current string splitting logic (`target_folder.split('/')[-1]`) should still identify `codex` properly, but needs validation to ensure moves between `100_todo/codex` and `200_inprogress/gemini` apply the correct `gemini_` tag and rename operations seamlessly.

# Changes To Make
- Update Python code to monitor multiple new subdirectories.
- Generalize Javascript rendering logic.

# Validation Steps
* [ ] Agent folders exist in `todo` and `inprogress` directories physically.
* [ ] Dashboard displays the agent drop zones (Codex, Gemini, Claude, General) in To Do and In Progress columns, even if empty.
* [ ] Dragging from Backlog > Codex into Todo > Gemini moves the file to `100_todo/gemini` and renames it with the `gemini_` prefix.
* [ ] Expanding and collapsing the new agent groups works independently in these columns.
