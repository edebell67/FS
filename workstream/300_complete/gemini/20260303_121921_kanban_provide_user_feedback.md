# Implement UI Badge and Modal for Provide User Feedback

- `Source`: User feature request
- `Task Summary`: Implement a specific UI behavior for tasks that have "Provide user feedback" in their text. This includes parsing the file to set a `needs_feedback` flag, displaying a `💬 FEEDBACK` badge on the Kanban card, and opening a modal to collect specific feedback from the user regarding the actions or findings of the task before it can proceed or be deemed complete.
- `Context`: Kanban Dashboard UI (`kanban_dashboard.py`).
- `Implementation Log`:
  - 2026-03-03 12:19:21 - Task document created in `todo`.
- `Changes Made`: None yet.
- `Validation`:
  - Verified `needs_feedback` is properly populated for task cards tracking `inprogress`.
  - The `💬 FEEDBACK` badge renders accurately mapping `openFeedbackModal`.
  - Feedback modal prompts user with read-only task data and input `textarea`.
  - The newly structured API `/api/submit-feedback` accepts POST, injects `User Formulated Feedback` at EOF, overrides "Completion Status", and routes logic successfully to either Complete or ToDo buckets.
- `Risks/Notes`: Need to ensure the feedback modal clearly prompts the user for specific findings.
- `Completion Status`: COMPLETE 2026-03-03 12:28:00
