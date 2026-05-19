# Task Summary
Enable backlog items to be moved between different folders seamlessly via the Kanban interface. 

# Context
Currently, the drag-and-drop mechanics handle atomic tasks effectively across internal agent folders and across columns. However, we need to ensure that Backlog items (specifically those in `000_backlog` and its subfolders `codex`, `gemini`, `claude`, `general`) can be properly dragged and dropped between different agent lanes or out of the backlog altogether. 

# Implementation Plan
1. **Verify Kanban API endpoints**:
   - Check the `/api/move-task` endpoint logic in `kanban_dashboard.py` to ensure it correctly handles file paths when the `source_folder` starts with `000_backlog`. 
   - Ensure the automatic agent tagging (e.g., prepending `gemini_` to the filename) applies flawlessly when a backlog item is dropped into an agent-specific backlog folder (e.g., `000_backlog/gemini`).
2. **Review Frontend Drag & Drop**:
   - Ensure the UI groups in the `000_backlog` column have identical `ondrop` handlers configured as the other columns, allowing them to accept payload drops.
3. **Handle `_processed.md` edge cases**:
   - Ensure that moving an already processed backlog item does not break its status or filename.

# Changes To Make
- Update `kanban_dashboard.py` (if necessary) to permit and adapt renaming rules for backlog files dragged between agent folders.
- Validate drag-and-drop events in the Javascript frontend for the `.kanban-column#col-000_backlog` element.

# Validation Steps
* [ ] Drag an item from `000_backlog/general` into `000_backlog/codex` and verify the file successfully physically moves.
* [ ] Verify the file is renamed appropriately to include `codex_` if required by the schema.
* [ ] Drag a backlog item from `000_backlog/codex` back into `000_backlog/general` and verify the agent tag is stripped.
