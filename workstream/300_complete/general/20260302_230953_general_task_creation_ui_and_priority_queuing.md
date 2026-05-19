# Task Summary
Create a unified "Create New Entry" UI modal on the Kanban Dashboard to natively author either a Backlog Specification or an Atomic Task. Introduce a Priority field (1=High, 2=Normal, 3=Low) that fundamentally alters the execution queue order inside the headless agent's worker loop.

# Context
Currently, users must manually create `.md` files in a text editor like VSCode, format the internal Markdown headers perfectly, and physically save them into the correct `workstream` subfolder to inject work into the engine. This breaks the single-pane-of-glass dashboard experience.

We need a native Form UI on the Kanban board to securely author these files.

Furthermore, the system currently executes tasks purely on a First-In-First-Out (FIFO) basis by just sorting filenames chronologically. We need a `Priority` metric to preemptively reorder the `100_todo` execution queue (e.g., P1 tasks skip the line and execute before P2/P3). P1 tasks should be processed immediately. P3 tasks should logically fall behind all P2 tasks. 

# Implementation Plan
1. **Frontend Dashboard UI - Creation Modal**:
   - Add a "➕ Create Entry" button to the main dashboard header.
   - Build a Form Modal containing:
     - **Type Toggle**: [Backlog Item] vs [Atomic Task]
     - **Agent Target**: [Codex] / [Gemini] / [Claude] / [General] / [📁 ROOT (Hold)]
     - **Priority Level**: [P1 (High)] / [P2 (Normal)] / [P3 (Low)]
     - **Title/Project Area**: Text inputs to generate the `{timestamp}_{project}_{title}.md` filename structure.
     - **Markdown Editor**: A `<textarea>` to write the actual instructions/requirements.
   - If User selects "Saved to ROOT", the target path is forced to `000_backlog` or `100_todo` without an agent subdirectory (leaving it on hold).

2. **Backend API Endpoint (`/api/create-entry`)**:
   - Create a new POST handler in `kanban_dashboard.py`.
   - Receive the JSON payload and securely write the new `.md` file to the correct target folder.
   - Inject the `Priority: X` meta-tag straight into the file (e.g., `# Meta\nPriority: 2\n`).

3. **Backend Agent Execution Logic (The Priority Sorting)**:
   - Upgrade the `multi_model_lane_worker` polling logic in `100_todo`.
   - Instead of blindly calling `valid_tasks.sort()` (which just sorts by timestamp), the worker must physically open/peek into every valid `.md` file in `100_todo/{agent}`.
   - Extract the `Priority: X` value (defaulting to 2 if missing).
   - Perform a composite sort: `sort(key=lambda t: (get_priority(t), timestamp))`. This guarantees P1 tasks are pulled before P2 tasks, regardless of their creation timestamp.
   
4. **Dashboard UI Updates**:
   - Update `createCardHtml` to visibly render a Priority Badge on the Kanban UI (e.g., a red ⚡ for P1, grey for P3) so the user visually sees the queue order.

# Validation Steps
* [ ] Open UI, click Create Entry, select `Task`, `Codex`, `Priority 1`, and write "Test P1".
* [ ] Verify the file is generated perfectly inside `100_todo/codex` with the Priority tag.
* [ ] Create a `Priority 2` task and a `Priority 1` task simultaneously in the UI while Codex is paused.
* [ ] Unpause/Observe the Codex worker: Validate it picks up the newer P1 task *before* the older P2 task.
* [ ] Ensure Saving a Backlog to `Root` correctly places it in `000_backlog` without an agent hook, pausing it.
