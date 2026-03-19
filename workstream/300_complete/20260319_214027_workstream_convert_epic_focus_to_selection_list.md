Priority: 2

# Task Summary
Convert the kanban epic focus control from a free-text input into a true selectable epic list so users can choose from the canonical epic families already known to the app instead of typing them manually.

# Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- Existing epic focus UI and `/api/pipeline-focus` endpoint
- Existing canonical epic-family availability list used for focus suggestions

Dependency: `C:\Users\edebe\eds\workstream\300_complete\20260319_171503_workstream_kanban_epic_focus_pipeline_mode.md`

# Plan
- [x] 1. Inspect the current epic focus UI and identify the exact controls and data sources to replace.
  - [x] Test: Read the header focus-control markup and related JS in `workstream/kanban_dashboard.py`.
  - [x] Evidence: Confirmed the existing control used `focusEpicInput` plus a `datalist` populated from `available_epics`.
- [x] 2. Replace the free-text epic focus input with a proper selection list sourced from the canonical epic list.
  - [x] Test: Verify the UI control uses the returned canonical epic list rather than manual text entry.
  - [x] Evidence: Replaced the input+datalist with `focusEpicSelect` and populate it from `available_epics`.
- [x] 3. Validate that applying/clearing focus still works with the new selection control.
  - [x] Test: Exercise the selection-driven focus path and confirm it still submits the selected epic family correctly.
  - [x] Evidence: JS now reads from `focusEpicSelect`, preserves selected value on refresh, and clears selection when focus is removed.

# Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: Kanban epic focus UI updated from free-text to selection list.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: User verification in thread on 2026-03-19: dropdown visible, selection applies focus, and clear resets selection.
  - Objective-Proved: The selection-list UX works correctly in the running app.
  - Status: captured

# Implementation Log
- 2026-03-19 21:40:27: Created task from user request to convert epic focus into a selection list of epics.
- 2026-03-19 21:42:00: Reviewed the existing focus control markup and JS update/apply/clear paths in `kanban_dashboard.py`.
- 2026-03-19 21:43:00: Replaced the free-text `focusEpicInput` and `focusEpicList` datalist with a real `focusEpicSelect` dropdown.
- 2026-03-19 21:44:00: Updated `updatePipelineFocusUI()`, `applyPipelineFocus()`, and `clearPipelineFocus()` to use the selection control and preserve/reset selected values correctly.

# Changes Made
- Updated `C:\Users\edebe\eds\workstream\kanban_dashboard.py`:
  - replaced the epic focus free-text input with a selectable dropdown
  - populated the dropdown from canonical `available_epics`
  - kept the same `/api/pipeline-focus` contract
  - updated focus apply/clear logic to use the selected option rather than typed text

# Validation
- `python -m py_compile workstream/kanban_dashboard.py`
  - Pass. Only the pre-existing embedded-HTML `SyntaxWarning` remains.
- `rg -n "focusEpicInput|focusEpicList|focusEpicSelect|Select epic\\.\\.\\.|Select an epic family to focus" workstream/kanban_dashboard.py`
  - Pass. No stale references to the old text input/datalist remain; new selection control references are present.
- User verification still required:
  - Requested.
- User verification captured on 2026-03-19:
  - `1 yes`: epic focus control is now a dropdown list of epics
  - `2 yes`: selecting an epic and applying focus works
  - `3 yes`: clearing focus resets the selection

# Risks/Notes
- The selectable list should remain aligned with the canonical epic-family list already exposed by the app.
- This change is UI-only on top of the previously verified focus-mode backend behavior.

# Completion Status
- Complete.
