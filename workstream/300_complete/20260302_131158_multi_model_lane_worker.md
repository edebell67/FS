# Task Summary
Create a Multi-Model Lane Worker script to automate the workflow for backlog item ingestion, atomic task generation, sequential execution, and blocker handling for the specific AI agents (Codex, Claude, Gemini).

# Context
We now have dedicated agent lanes within our Kanban board (`000_backlog`, `100_todo`, `200_inprogress`). The goal is to fully automate the task execution lifecycle for these agents. When a backlog item is dropped into an agent's backlog folder (e.g., `000_backlog/codex`), a dedicated lane worker should automatically pick it up, break it down, and execute it using the designated model CLI.

# Implementation Plan
1. **Develop Lane Worker Script (`agent_lane_worker.py`)**:
    *   **Folder Polling**: The script must independently poll the respective agent folders (`000_backlog/AGENT`, `100_todo/AGENT`).
    *   **Decomposition**: When a new backlog item is detected, the worker utilizes the agent CLI to decompose the backlog item into actionable, atomic markdown tasks. These tasks should be created in the `100_todo/AGENT` folder, containing links to the parent backlog ticket.
    *   **Sequential Locking**: The worker claims one atomic task at a time by moving it from `100_todo/AGENT` to `200_inprogress/AGENT`. This file move acts as a native system lock.
    *   **Task Execution Loop**: 
        *   Trigger the specific model CLI (e.g., `coder`, `gemini`, `claude`) providing the task file and a standard system prompt instructing it to read `skills.md` and adhere to its lane constraints.
        *   The execution should ideally involve a build/test verification step (exit code 0).
    *   **Feedback & Blocker Handling**:
        *   If the model stops prematurely, times out, or fails a build, the worker must capture the `stderr` and the tail of the logs.
        *   It then generates a *new* atomic blocker task in `100_todo/AGENT` containing these error logs, moving the stalled task into a `failed` state or keeping it linked for retry.
    *   **Completion Sync**: Once all atomic tasks linked to a parent backlog item are marked complete, the worker must update the original backlog item's metadata and move it to `300_complete/AGENT`.
    
2. **Standardization Details**:
    *   Define the exact standard start prompt that forces the models to output specific state markers (e.g. `STATUS: DONE`, `STATUS: BLOCKED`).
    *   Ensure the script is highly durable (e.g. simply restarting the python script gracefully resumes execution based solely on the current file locations).

# Changes To Make
*   Create a robust Python/PowerShell daemon script responsible for managing this async queue.
*   Ensure it interacts smoothly with the folder structures created in previous tasks.

# Validation Steps
*   [ ] Drop a mock backlog item into `000_backlog/gemini`.
*   [ ] Verify the worker scripts automatically pick it up and generate multiple `100_todo/gemini` atomic tasks.
*   [ ] Verify the worker sequentially moves one task to `200_inprogress`, executes a mock CLI command, and transitions it to `300_complete`.
*   [ ] Trigger an intentional mock failure and verify a blocker task is automatically spawned with the captured logs.
*   [ ] Verify the parent backlog item is moved to Complete only when all children are resolved.
