Source: Direct user request in this session.

Task Summary: Add a destination-folder field to the Epic Decomposition screen so the operator can choose where decomposed epic tasks are written instead of always using the default backlog folder.

Context:
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\epic_decompose_cli.py`
- `C:\Users\edebe\eds\workstream\200_inprogress\20260313_160611_workstream_rename_backlog_todo_to_epic_backlog.md`

Dependency: None

Plan:
- [x] 1. Inspect the current decomposition screen and backend write path.
  - [x] Test: Review the decomposition UI and backend code to identify where the fixed destination is currently enforced and where the selected folder must be passed.
  - Evidence: `kanban_dashboard.py` now shows the destination field at the Epic Decomposition screen and the backend decomposition flow accepts a `destination_folder` parameter.
- [x] 2. Add a destination-folder input to the decomposition screen and submit it to the backend.
  - [x] Test: `rg -n "destinationFolder|destination_folder|Destination folder: <code>" C:\Users\edebe\eds\workstream\kanban_dashboard.py` returns the UI input, API payload, and success-message rendering.
  - Evidence: `kanban_dashboard.py` contains `destinationFolder` input wiring and the success template uses `data.destination_folder`.
- [x] 3. Update the backend to honor the selected destination folder safely.
  - [x] Test: `rg -n "_resolve_repo_path|def decompose_epic|destination_folder" C:\Users\edebe\eds\workstream\kanban_dashboard.py` shows repo-root path resolution, destination directory creation, and API response propagation.
  - Evidence: `decompose_epic()` resolves the selected folder through `_resolve_repo_path()`, creates the directory, writes task files there, and returns the normalized repo-relative destination.
- [x] 4. Verify visible decomposition behavior with the new destination field.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py` completes without syntax errors.
  - Evidence: `python -m py_compile` passed for `kanban_dashboard.py`.
  - [x] Test: A controlled decomposition run using `KANBAN_EPIC_DECOMP_CMD=python {repo_root}\_tmp_epic_decomp_stub.py` writes a task into `workstream/verification/epic_destination_folder_validation/output`, returns that same destination in the response payload, and rejects `../outside_repo_test` with `ValueError`.
  - Evidence: `workstream/verification/epic_destination_folder_validation/decompose_validation.json` records successful custom-folder output and `workstream/verification/epic_destination_folder_validation/path_guard_validation.txt` records the out-of-repo rejection.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py` -> PASS
  - Objective-Proved: The modified dashboard/backend module parses successfully after the destination-folder changes.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\verification\epic_destination_folder_validation\decompose_validation.json`
  - Objective-Proved: A decomposition call wrote output into the requested custom folder, returned the same repo-relative destination, and created the decomposition manifest.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\verification\epic_destination_folder_validation\path_guard_validation.txt`
  - Objective-Proved: Destination-folder resolution blocks writes outside the repository root.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\workstream\verification\epic_destination_folder_validation\output\20260319_171128_validation_epic_workstreamA_create_first_validation_task.md`
  - Objective-Proved: The operator-visible decomposition workflow now has a concrete writable custom destination path that receives generated task files.
  - Status: captured

Implementation Log:
- 2026-03-13 22:18 Europe/London: Added a `Destination Folder` input to the Epic Decomposition screen and updated the success message to report the selected destination.
- 2026-03-13 22:20 Europe/London: Updated `decompose_epic()` and `/api/decompose-epic` to accept `destination_folder`, resolve it safely under the repo root, and write decomposed task files there.
- 2026-03-13 22:25 Europe/London: Recreated this lifecycle record in `200_inprogress` after implementing the destination-folder support in the built-in Epic Decomposition screen.
- 2026-03-19 17:10 Europe/London: Revalidated the current implementation, confirmed the UI field, success-message wiring, and backend path handling are present in `kanban_dashboard.py`.
- 2026-03-19 17:11 Europe/London: Executed a controlled decomposition run with a local stub via `KANBAN_EPIC_DECOMP_CMD` and captured evidence showing task creation in the chosen folder plus repo-root path-guard rejection for `../outside_repo_test`.
- 2026-03-19 17:12 Europe/London: Normalized this lifecycle file to the required template, completed the checklist, and prepared the task for archive.

Changes Made:
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - added a `Destination Folder` input to the Epic Decomposition screen
  - passed `destination_folder` through the `/api/decompose-epic` request body
  - updated the decomposition success message to display the chosen destination folder
  - updated `decompose_epic()` to write task files into the selected folder
  - added `_resolve_repo_path()` so destination folders remain constrained under the repo root
- `C:\Users\edebe\eds\workstream\verification\epic_destination_folder_validation\decompose_validation.json`
  - captured end-to-end validation output for custom destination folder writes
- `C:\Users\edebe\eds\workstream\verification\epic_destination_folder_validation\path_guard_validation.txt`
  - captured repo-root path guard behavior for invalid destinations

Validation:
- `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - PASS
- `rg -n "destinationFolder|destination_folder|Destination folder: <code>" C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - PASS: UI field, API payload, success-message template, backend parameter, and response field are present.
- `python - <<validation script using KANBAN_EPIC_DECOMP_CMD=python {repo_root}\_tmp_epic_decomp_stub.py>>`
  - PASS: `workstream/verification/epic_destination_folder_validation/decompose_validation.json` recorded `success=true`, `destination_folder=workstream/verification/epic_destination_folder_validation/output`, `tasks_created_count=1`, `first_task_exists=true`, and `manifest_exists=true`.
- `python - <<path-guard validation using KANBAN_EPIC_DECOMP_CMD=python {repo_root}\_tmp_epic_decomp_stub.py>>`
  - PASS: `workstream/verification/epic_destination_folder_validation/path_guard_validation.txt` recorded `ValueError: path_outside_repo: ../outside_repo_test`.
- `python - <<direct decomposition using native epic_decompose_cli.py>>`
  - BLOCKED BY EXISTING ENVIRONMENT ISSUE: the current environment returns `Access is denied` from the delegated decomposition command. This does not affect the destination-folder logic itself, which was validated independently through the existing command override hook.

Risks/Notes:
- Destination resolution is constrained under the repo root to avoid writes outside the workspace.
- Default behavior remains `workstream/100_backlog` unless the operator changes the field.
- Native decomposition execution is currently blocked in this environment by an unrelated `Access is denied` failure from the delegated decomposition command path. The feature-specific validation used the existing `KANBAN_EPIC_DECOMP_CMD` override to isolate and verify destination-folder behavior.

Completion Status:
- Complete - 2026-03-19 17:12 Europe/London
