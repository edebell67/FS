# Task Summary
Update the Kanban Dashboard (`kanban_dashboard.py`) to actively read from the new agentic backlog folders (`codex/000_backlog`, `gemini/001_backlog`, `claude/002_backlog`) and display their contents within the "Backlog" column. Each agent's backlog should be grouped by the agent folder name with expand/collapse functionality.

# Context
We created these separate folders to track tasks for individual AI agents. The current dashboard script only parses the main `000_backlog` directory. We need to expand this so that these sub-backlogs are visible, manageable, and clearly segmented by agent directly in the UI.

# Implementation Plan
* Update `FOLDERS` in `kanban_dashboard.py` or modify the file scanning logic to include `codex/000_backlog`, `gemini/001_backlog`, and `claude/002_backlog`.
* Map these incoming tasks to the main Backlog column (`col-000_backlog`).
* Instead of grouping these purely by project, inject a higher-level or side-by-side grouping logic for the "Agent" (derived from the folder path).
* Re-use or extend the `toggleGroupBacklog` functionality to handle expanding/collapsing these specific agent groups cleanly.
* Maintain a distinct color or badge so the user can tell an agent-assigned backlog task vs. a general backlog task.

# Changes To Make
* Modify Python file parsing loops in `/api/tasks` endpoint.
* Update JavaScript `renderBoard()` to accommodate the new folder sources and nest/group them appropriately before rendering HTML.

# Validation Steps
* [ ] Create a dummy markdown task file in `codex/000_backlog`.
* [ ] Open Kanban dashboard and confirm the task appears in the Backlog column under a "Codex" group.
* [ ] Toggle the expand/collapse button for the group and confirm it hides/shows the task.
* [ ] Confirm other agents (gemini, claude) render correctly without errors.
