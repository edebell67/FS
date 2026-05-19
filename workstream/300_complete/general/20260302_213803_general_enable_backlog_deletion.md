# Task Summary
Introduce the ability to delete a backlog item directly from the Kanban UI, restricted exclusively to items sitting in the `general` backlog section (`000_backlog/general`), and only if they do not already have spawned/derived child tasks in the system.

# Context
We need a safe way to discard drafted, unused, or abandoned backlog specifications directly from the dashboard without leaving clutter. However, deleting backlog items that have already been decomposed by an agent into child atomic tasks (e.g., in `100_todo` or `200_inprogress`) would orphan those tasks and corrupt the execution trail. The deletion must strictly apply to unprocessed items in the `general` staging lane.

# Implementation Plan
1. **Develop Dashboard API Endpoint (`/api/delete-task`)**:
   - Create a POST handler in `kanban_dashboard.py`.
   - Validate the target folder restricts deletion to `000_backlog/general` (or the `📁 Root` backlog).
   - **Safety Check**: Implement a filesystem check to verify no child tasks exist. It should scan the filesystem for tasks containing the core backlog filename (e.g., `_from_20260302...` or similar linked filenames).
   - If no children exist, physically call `os.remove()` to delete the `.md` file.

2. **Dashboard UI Updates**:
   - Render a "🗑️ Delete" button on task cards (or inside the card's open Modal) for tasks located strictly in the `000_backlog` -> `general` lane.
   - When clicked, prompt the user with a Javascript `confirm()` dialogue to prevent accidental clicks.
   - On confirmation, fire a fetch request to `/api/delete-task` and then re-render the board if successful.

# Changes To Make
- Update `kanban_dashboard.py` backend server to support a safe deletion POST request.
- Update `kanban_dashboard.py` frontend HTML/JS to selectively render a delete button for general backlog items.

# Validation Steps
* [ ] Create a dummy backlog item in `000_backlog/general`.
* [ ] Verify a delete button appears for it in the Dashboard.
* [ ] Click delete, confirm, and verify the file is successfully deleted from disk and vanishes from the UI.
* [ ] Move a processed backlog item (with spawned tasks) into `000_backlog/general`, try to delete it, and verify the backend blocks the deletion because child tasks exist.
