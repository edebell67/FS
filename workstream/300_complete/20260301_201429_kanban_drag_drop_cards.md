# Task Summary
Implement drag-and-drop functionality for task cards within the Kanban Dashboard (`kanban_dashboard.py`). Users should be able to drag a card from one column (e.g., Backlog or To Do) and drop it into another (e.g., In Progress or Complete), updating both the visual UI and moving the actual file on the filesystem.

# Context
The user requested a way to move tickets intuitively by dragging. Currently, tickets must be moved manually on the filesystem, but drag-and-drop on the board is a staple Kanban feature.

# Implementation Plan
1. **Frontend Updates (HTML/JS):**
   * Add `draggable="true"` to `.task-card` elements and hook up standard HTML5 `dragstart` events, storing the task's current file path and data.
   * Add `dragover`, `dragenter`, and `drop` event listeners to the `.column-content` or `.project-group` drop zones.
   * On `drop`, visually represent the change or display a "Moving..." spinner.
   * Send an asynchronous JSON `POST` request (`/api/move-task`) containing the source folder, target folder, and filename.

2. **Backend Updates (Python):**
   * Introduce a new API endpoint in `KanbanHandler` (`/api/move-task`) that listens for `POST` requests.
   * Verify the file exists in the correct source directory.
   * Issue a filesystem move command using `os.rename` from the old folder to the target folder.
   * Return a JSON success response.

3. **State Management Edge Cases:**
   * Accommodate the auto-refresh mechanism (2s polling loop) by either pausing polling during drags or simply relying on the next poll to confirm the new card position once the API returns success.

# Changes To Make
* Modify the `HTML_PAGE` payload inside `c:\Users\edebe\eds\workstream\kanban_dashboard.py` to add drag-and-drop JS boilerplate payload.
* Modify `KanbanHandler.do_POST` to handle `/api/move-task` moves safely to prevent race conditions or missing files.

# Validation Steps
* [ ] Pick up a card with the mouse and verify it correctly enters dragged state.
* [ ] Verify the drop zone visually highlights.
* [ ] Drop the card into another section and ensure it persists and the underlying file is physically moved to the destination folder in Windows Explorer.
