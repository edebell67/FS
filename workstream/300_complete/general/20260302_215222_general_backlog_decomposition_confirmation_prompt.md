# Task Summary
Inject a mandatory confirmation prompt into the automated workflow engine immediately after atomic tasks have been generated from a parent backlog item, but before they are formally released into the agent's work queue.

# Context
Currently, the `multi_model_lane_worker` daemon automatically decomposes a backlog item and silently injects the resulting tasks into the `100_todo` queue while marking the backlog as `_processed.md`. To maintain human oversight before AI agents begin executing potentially flawed or incomplete task plans, we need a "Validation Gate" UI modal. 

When tasks are generated from a backlog, the system should halt and present the user with a confirmation modal displaying the proposed atomic tasks.

# Implementation Plan
1. **Workflow State Change**:
   - Instead of dropping generated tasks directly into `100_todo`, the worker should place them in a temporary holding state or a staging directory (e.g., `050_review`), or simply mark them with a status block that pauses execution.
   
2. **Dashboard UI (The Confirmation Modal)**:
   - Create a specialized modal pop-up on the Kanban board that alerts the user when a backlog has finished decomposing.
   - The modal will list out the generated tasks for the user to review.
   - **Three Action Buttons**:
     1. **Approve & Proceed**: Positive confirmation. The system officially moves the tasks into `100_todo`, renames the backlog to `_processed.md`, and the agent worker continues.
     2. **Request Changes / Additions**: The flow pauses. A text input appears to capture additional requirements or feedback. Once submitted, the backend re-invokes the prompt generation, passing the feedback to adjust and regenerate the task list, then presents the updated list again.
     3. **Reject & Suspend**: The backlog item is suspended (e.g., moved to a `500_suspended` folder or marked `_suspended.md`), and the generated draft tasks are discarded.

3. **Backend API Logic**:
   - Create necessary endpoints (e.g., `/api/review-tasks`, `/api/approve-tasks`, `/api/regenerate-tasks`, `/api/suspend-backlog`) to handle the modal's actions and coordinate the state transition of these `.md` files.

# Validation Steps
* [ ] Drop a backlog into an agent lane and ensure the daemon pauses instead of blindly processing it.
* [ ] Verify the Confirmation Modal appears on the UI with the drafted tasks.
* [ ] **Test Approve**: Click approve, verify tasks land in `100_todo` and backlog gets `_processed`.
* [ ] **Test Modify**: Request a change ("Add a UI formatting task"), verify the system regenerates the tasks and re-presents the modal.
* [ ] **Test Reject**: Click 'Reject and Suspend', verify the drafted tasks are deleted and the backlog is parked safely without processing.
