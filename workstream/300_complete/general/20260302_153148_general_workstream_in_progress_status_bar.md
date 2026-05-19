# Task Summary
Display a visual progress bar on task cards within the Kanban Dashboard, specifically designed to indicate the percentage of completion when a task is in the "In Progress" state run by the agents.

# Context
With the introduction of the multi-model lane worker, tasks are picked up and processed automatically. While a task is running in the `200_inprogress` queue, it can be useful to have a visual indicator (like a status bar) showing how far along the task is, rather than just waiting blindly for it to move to `300_complete`.

# Implementation Plan
1. **Define Progress Indicator Protocol**:
   - Establish a standard way for agents to report their progress. For example, the worker daemon or the agent itself could write a metadata tag into the `.md` file, such as `Progress: 45%` or `[45/100]`.
   - Alternatively, if execution involves looping through a set of sub-tasks, the python script could track log outputs and calculate completion percentages, updating the `.md` file.

2. **Dashboard Backend Parser Update (`kanban_dashboard.py`)**:
   - Update the `/api/tasks` regex or parsing logic to scan the content of the `.md` files for the defined `Progress` tag.
   - Return this `progress` percentage value (e.g., an integer from 0 to 100) alongside the normal task JSON object.

3. **Dashboard UI Updates**:
   - Modify the `createCardHtml(task)` Javascript function.
   - If the task has a `progress` value (and potentially only if it is in particular states like `200_inprogress`), render a simple CSS-based progress bar (e.g., `<div class="progress-container"><div class="progress-bar" style="width: ${t.progress}%;"></div></div>`).
   - Add some nice animations or colors (e.g., blue/purple gradient) to fit the dark mode styling.

# Changes To Make
- Update `kanban_dashboard.py` python parser to extract progress percentage.
- Update `kanban_dashboard.py` JS template to render the progress bar.
- (Prerequisite): Ensure lane workers/agents actually emit this progress data into the file logic.

# Validation Steps
* [ ] Manually add `Progress: 50%` to a mock file in `200_inprogress`.
* [ ] Verify the python dashboard API returns `"progress": 50` for that task.
* [ ] Validate that the frontend renders a visual 50% filled progress bar on the card.
* [ ] Verify cards without the progress tag do not break and simply hide the bar.
