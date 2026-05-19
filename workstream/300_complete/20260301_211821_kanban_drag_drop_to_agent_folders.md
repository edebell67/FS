# Task Summary
Enhance the Kanban Dashboard to display the specific agent folders (`codex`, `gemini`, `claude`) as distinct, interactive drop zones within the `000_backlog` column. Users must be able to drag existing backlog cards and drop them directly into these specific agent folders to reassign them on the filesystem.

# Context
Currently, the drag-and-drop functionality allows moving cards between major Kanban columns (e.g., Backlog to To Do). However, within the Backlog column itself, we have sub-folders (`codex/000_backlog`, `gemini/001_backlog`, `claude/002_backlog`). The user needs a way to visually drag a general backlog task and drop it into a specific AI agent's folder to assign it.

# Implementation Plan
1. **Frontend Drop Zones:**
   * Modify the JavaScript `renderBoard` function that groups the agent folders (`🤖 Codex`, `✨ Gemini`, etc.).
   * Add `ondragover` and `ondrop` event listeners specifically to the `.project-group` or `.group-header` elements representing these agent folders.
   * Pass the exact sub-folder path (e.g., `codex/000_backlog`) as the target to the `handleDrop` function when dropping into these specific areas.
2. **Handle Drop Logic Updates:**
   * Ensure `handleDrop` correctly processes the specific target folder string rather than just the generic column ID.
   * Prevent event bubbling so that dropping on an agent group doesn't trigger the main column's drop event (which would just send it to `000_backlog` root).
3. **Backend API Compatibility:**
   * The `/api/move-task` endpoint already accepts `source_folder` and `target_folder`. Ensure it correctly joins these paths when folders contain subdirectories (e.g., `os.path.join(WORKSTREAM_DIR, "codex/000_backlog", filename)`).

# Changes To Make
* Update `kanban_dashboard.py` frontend HTML payload. Specifically, the template literal that generates the `groupHtml` for the `000_backlog` column.
* Add `ondragover="handleDragOver(event)" ondrop="handleDrop(event, '${folder_path}')"` to the group containers.

# Validation Steps
* [ ] Drag a card from the general backlog and hover over the "Codex", "Gemini", or "Claude" group header/container.
* [ ] Drop the card and verify it visually moves into that group.
* [ ] Verify on the filesystem that the Markdown file actually moved into the `codex/000_backlog`, `gemini/001_backlog`, or `claude/002_backlog` folder.
