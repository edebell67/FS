# Task Summary
Modify the Kanban dashboard's "Backlog" / "To Do" column so that tasks are automatically grouped by project and collapsed by default. Include expand/collapse buttons for individual groups (+) and global expand/collapse all, mirroring the approach used for the "Complete" section.

# Context
The user requested this feature to make the "Backlog" column more manageable, as it frequently accumulates many tasks. Similar to the Complete section, the UI should display project-based groups by default with a `+` button to expand them individually, as well as a global expand/collapse feature.

# Implementation Plan
* Adapt the Javascript rendering logic (`renderBoard` / grouping aggregator) to also apply to the `000_backlog` (Backlog) column. 
* Group all backlog records by their parsed `{project}` string.
* Wrap individual cards within the Backlog column inside project-grouped elements natively.
* Reuse the `onclick="toggleGroup('proj')"` expanding listener for each group header with `+`/`-` styling in the Backlog section.
* Add an `Expand All` toggle explicitly into the `Backlog` header area allowing global toggles.
* Ensure the Javascript state properly caches `expandedGroups` for the Backlog section across consecutive polling loops.
* Test and execute the UI, ensuring smooth frontend interaction.

# Changes To Make
* Extend `kanban_dashboard.py` (or the respective frontend injection script) to apply group HTML aggregation loops inside the javascript for the backlog column.

# Validation Steps
* [x] Run the python server and ensure the dashboard launches correctly.
* [x] Verify tasks inside the 'Backlog' column properly group by project name and collapse by default.
* [x] Verify the expand/collapse toggles work as expected.

# Risks/Notes
* If project names contain strange unicode or symbols it may break the JS HTML builder slightly, but standard characters should collapse correctly without issues. Ensure that group ID handling is consistent for the backlog rendering logic.

# Completion Status
Completed on 2026-03-01 15:32.
