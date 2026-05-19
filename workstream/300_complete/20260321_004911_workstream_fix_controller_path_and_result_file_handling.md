# Fix Controller Path And Result File Handling

## Metadata
- Project: workstream
- Task: fix_controller_path_and_result_file_handling
- Started: 2026-03-21 00:49:11
- Status: complete

## Source
- User-reported controller/runtime errors from `kanban_dashboard.py` and `run_agent.py`.

## Task Summary
Stabilize the kanban controller by fixing path-related `WinError 3` failures during epic focus parking and by preventing `.result.md` artifacts from breaking task scans due to UTF-8-only decoding assumptions.

## Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\run_agent.py`

## Dependency
Dependency: None

## Plan
- [x] 1. Inspect the failing controller code paths and identify the exact move/read failure modes.
  - [x] Test: Reproduce the reported traceback locations from local imports or targeted commands and identify the failing lines.
  - [x] Evidence: Direct import traceback showed `_pipeline_focus_status()` failing in `_park_non_focus_items()` -> `_move_file_preserving_uniqueness()`; hex inspection confirmed the `.result.md` file starts with `FF FE` (UTF-16 LE BOM).
- [x] 2. Patch the controller to tolerate concurrent file moves and ignore or safely decode result artifacts.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`
  - [x] Evidence: Both modules compiled successfully; only the pre-existing `SyntaxWarning` in `kanban_dashboard.py:450` remains.
- [x] 3. Validate the affected runtime entry points after the patch.
  - [x] Test: Targeted import/checks confirm `_pipeline_focus_status()` returns without traceback and task scanning no longer errors on `.result.md`.
  - [x] Evidence: Validation output reported `focus_success=True`, `focus_enabled=True`, `available_epics=8`, and `_is_task_markdown=False` for the UTF-16 `.result.md` artifact.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Updated controller modules parse successfully after the patch.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: Direct import output: `focus_success=True`, `focus_enabled=True`, `available_epics=8`, `parked_keys=['100_backlog', '200_inprogress']`
  - Objective-Proved: Pipeline focus status now returns without the prior `WinError 3` traceback.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: Direct checks against `20260320_232000_workstream_move_decomposed_epic_root_tasks_to_general_backlog.result.md` reported `_is_task_markdown=False` and successfully decoded the UTF-16 content prefix.
  - Objective-Proved: Result artifacts are excluded from task scans and can still be decoded safely if read directly.
  - Status: captured

## Lifecycle Log
### 2026-03-21 00:49:11
- Created lifecycle record for controller path and result-file handling fixes.

### 2026-03-21 00:49:47
- Reproduced pipeline focus failure from direct import. Traceback showed `_pipeline_focus_status()` failing inside `_park_non_focus_items()` when `_move_file_preserving_uniqueness()` attempted to move a file that had already disappeared from `100_backlog/claude`.
- Reproduced result artifact mismatch. Verified `20260320_232000_workstream_move_decomposed_epic_root_tasks_to_general_backlog.result.md` is UTF-16 and was being treated like a normal task markdown file.

### 2026-03-21 00:50:32
- Patched `kanban_dashboard.py` with centralized markdown-task filtering, best-effort markdown decoding, and race-tolerant focus parking file moves.
- Patched `run_agent.py` with the same task-file filtering and best-effort markdown decoding so `.result.md` artifacts are excluded from structured task scans.

### 2026-03-21 00:51:18
- Validated `python -m py_compile` for both updated modules.
- Validated direct import of `kanban_dashboard.py` and confirmed `_pipeline_focus_status()` returns successfully with focus still enabled.
- Validated that the UTF-16 `.result.md` artifact is no longer treated as a task markdown file.

## Validation
- [x] Reproduce current failures and capture the exact traceback locations.
- [x] Run `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py C:\Users\edebe\eds\workstream\run_agent.py`.
- [x] Run targeted import checks for pipeline focus status and result-file handling.
