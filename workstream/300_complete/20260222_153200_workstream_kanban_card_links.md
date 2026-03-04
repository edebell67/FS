# Task Summary
Ensure the Kanban cards on the real-time dashboard link back to their underlying markdown documents, allowing the user to click a card to open the document locally.

# Context
The user requested the ability to open the task markdown files directly from the web-based Kanban dashboard. Since the server runs locally on Windows, we can use an API endpoint to trigger `os.startfile()` which opens the file in the user's default editor (likely VS Code or Notepad).

# Implementation Log
* Started task to add file-opening capability.
* Modified the front-end template to include an `onclick` hook pointing to a new JS function `openFile`.
* Added `openFile` JS method sending a POST request containing to `/api/open-file`.
* Wired up a `do_POST` handler in `kanban_dashboard.py` to capture payload, combine path with `WORKSTREAM_DIR`, and execute `os.startfile(filepath)`.
* Terminated the old background dashboard process and started the updated one.

# Changes Made
* `kanban_dashboard.py` has been updated to include a `do_POST` endpoint and updated HTML UI template handling interactions.

# Validation
* Ran python script and ensured port 8080 launches correctly.

# Risks/Notes
* Cross-platform compatibility is not an issue as the user is on Windows (`os.startfile` works well).

# Completion Status
Completed on 2026-02-22 15:35.
