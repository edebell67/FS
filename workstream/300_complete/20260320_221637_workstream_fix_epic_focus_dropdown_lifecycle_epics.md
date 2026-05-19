Source: User request in Codex thread on 2026-03-20 to create a task for fixing the kanban epic focus dropdown so it picks up the list of all epics at the start of the lifecycle.

Task Summary: Fix the kanban screen epic focus dropdown so its option list is sourced from all epic items that exist at the lifecycle start, rather than an incomplete or incorrect subset.

Context:
- [`C:\Users\edebe\eds\workstream\kanban_dashboard.py`](/C:/Users/edebe/eds/workstream/kanban_dashboard.py)
- Existing epic focus work in [`C:\Users\edebe\eds\workstream\300_complete\20260319_171503_workstream_kanban_epic_focus_pipeline_mode.md`](/C:/Users/edebe/eds/workstream/300_complete/20260319_171503_workstream_kanban_epic_focus_pipeline_mode.md)
- Existing dropdown conversion work in [`C:\Users\edebe\eds\workstream\300_complete\20260319_214027_workstream_convert_epic_focus_to_selection_list.md`](/C:/Users/edebe/eds/workstream/300_complete/20260319_214027_workstream_convert_epic_focus_to_selection_list.md)

Dependency:
- [`C:\Users\edebe\eds\workstream\300_complete\20260319_171503_workstream_kanban_epic_focus_pipeline_mode.md`](/C:/Users/edebe/eds/workstream/300_complete/20260319_171503_workstream_kanban_epic_focus_pipeline_mode.md)
- [`C:\Users\edebe\eds\workstream\300_complete\20260319_214027_workstream_convert_epic_focus_to_selection_list.md`](/C:/Users/edebe/eds/workstream/300_complete/20260319_214027_workstream_convert_epic_focus_to_selection_list.md)

Plan:
- [x] 1. Inspect the current epic focus dropdown population path and identify which endpoint/helper currently supplies the option list.
  - [x] Test: Trace the UI control and API response in `kanban_dashboard.py` and confirm the exact source of the dropdown options.
  - [x] Evidence: Confirmed `updatePipelineFocusUI()` populates `focusEpicSelect` from `/api/pipeline-focus` -> `_pipeline_focus_status()` -> `_available_epic_families()`.
- [x] 2. Define the correct lifecycle-start source of truth for epic options.
  - [x] Test: Verify which lifecycle folders and filename/content patterns represent “epics at the start of the lifecycle” and confirm the expected canonical option list.
  - [x] Evidence: Confirmed `000_epic` is the lifecycle-start lane and should be the dropdown source, rather than all workflow states filtered by `KNOWN_EPIC_FAMILIES`.
- [x] 3. Update the backend/UI so the dropdown includes all lifecycle-start epics and preserves canonical epic-family behavior.
  - [x] Test: Refresh the kanban screen and confirm the dropdown contains the full lifecycle-start epic list and still supports focus selection.
  - [x] Evidence: Updated `_available_epic_families()` to derive options from `000_epic` files, dedupe by detected canonical family, and only fall back to all states if `000_epic` is empty.
- [ ] 4. Validate that epic focus still works after the dropdown-source fix.
  - [x] Test: Select one of the newly surfaced epics and confirm `/api/pipeline-focus` accepts it and the status reflects the chosen epic family.
  - [x] Evidence: User confirmed on 2026-03-20 that the updated Strategy Warehouse epic appears in the list, the dropdown is readable, and focus applies successfully.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\20260320_221637_workstream_fix_epic_focus_dropdown_lifecycle_epics.md`
  - Objective-Proved: A lifecycle task exists to track the requested dropdown fix.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: User verification in Codex thread on 2026-03-20: `1 - yes`, `2 - yes`, `3 - yes`
  - Objective-Proved: The kanban dropdown visibly lists all lifecycle-start epics after the fix.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py` and Python introspection of `kanban_dashboard._available_epic_families()`
  - Objective-Proved: Backend/UI validation confirms the corrected option source and epic focus behavior.
  - Status: captured

Implementation Log:
- 2026-03-20 22:16:37: Created backlog task from user request to fix the kanban epic focus dropdown option source.
- 2026-03-20 22:17:00: Linked this task to the prior completed epic focus pipeline and dropdown-selection work as explicit dependencies/context.
- 2026-03-20 22:25:00: Moved task to `workstream/200_inprogress` when implementation began.
- 2026-03-20 22:27:00: Confirmed the dropdown is populated in `updatePipelineFocusUI()` from `/api/pipeline-focus`, whose `available_epics` payload comes from `_pipeline_focus_status()` -> `_available_epic_families()`.
- 2026-03-20 22:28:00: Identified root cause: `_available_epic_families()` scanned all states but discarded anything outside `KNOWN_EPIC_FAMILIES`, causing real lifecycle epics to be omitted from the dropdown.
- 2026-03-20 22:30:00: Updated `_available_epic_families()` to source options from actual `000_epic` markdown documents, dedupe by detected epic family, and only fall back to all-state scanning if `000_epic` is empty.
- 2026-03-20 22:31:00: Ran `py_compile` and a Python introspection check; helper now returns `['autonomous_trading_signal_platform', 'bizpa', 'breakout', 'mvp_prd_mobile_quarterly_export', 'piphunter', 'sfx_technical_design', 'strategy_warehouse_marketing_engine', 'workstream']`.
- 2026-03-20 22:32:00: Requested user verification against the running kanban screen because the change is user-visible.
- 2026-03-20 22:40:00: User reported that the Epic Focus dropdown popup remained too light to read clearly in the browser despite the populated option list.
- 2026-03-20 22:41:00: Added dedicated dark styling for `#focusEpicSelect` and `#focusEpicSelect option`, plus `color-scheme: dark`, and updated the control’s inline background/text colors to reinforce the darker popup theme.
- 2026-03-20 22:42:00: Re-ran `py_compile` and confirmed the new dark-theme selectors are present in `kanban_dashboard.py`.
- 2026-03-20 23:02:00: Refined Epic Focus options to return readable labels sourced from active `000_epic` documents while preserving canonical family slugs as the selected values.
- 2026-03-20 23:03:00: Verified payload now includes the active merged epic as label `Strategy Warehouse Autonomous Marketing Engine` with value `strategy_warehouse_marketing_engine`.
- 2026-03-20 23:06:00: User verified the final UI behavior: the updated epic label appears in the dropdown, the dropdown is dark/readable, and focus applies successfully.

Changes Made:
- Added a new lifecycle task in `workstream/100_todo` for the epic focus dropdown fix.
- Updated `C:\Users\edebe\eds\workstream\kanban_dashboard.py`:
  - changed lifecycle-start epic option sourcing from raw family-only values to labeled options derived from active `000_epic` documents
  - removed the hard dependency on `KNOWN_EPIC_FAMILIES` for dropdown population
  - kept a fallback scan across all states if `000_epic` contains no epic files
  - darkened the Epic Focus select control and its option popup styling for readability in the browser
  - updated the dropdown JS to render friendly labels while keeping canonical focus values

Validation:
- [x] Create a lifecycle task file in `workstream/100_todo` for the requested fix.
- [x] Start implementation and move the task to `workstream/200_inprogress`.
- [ ] Verify the dropdown lists all lifecycle-start epics and epic focus still works.
- [x] Verify the dropdown lists all lifecycle-start epics and epic focus still works.

User Verification Request:
- Please refresh the kanban page at `http://localhost:8080`, open the Epic Focus dropdown, and confirm whether the list now shows the expected epic items.
- Please confirm whether the Strategy Warehouse entry now appears as `Strategy Warehouse Autonomous Marketing Engine`.
- Please also select one of the newly visible options and confirm whether Focus applies successfully.
- Please confirm whether the dropdown background is now dark enough for the option text to be clearly readable.

Risks/Notes:
- “At the start of the lifecycle” likely maps to epic documents in `000_epic`, but the implementation task should confirm whether `000_epic` alone is the correct source or whether review-state epic documents must also contribute.
- The fix should preserve canonical epic-family normalization so duplicate variants do not create duplicate dropdown options.

Completion Status: Complete - 2026-03-20 23:06:00
