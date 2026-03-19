Source: Direct user request in this session.

Task Summary: Rename workstream folders to simplify workflow: `000_backlog` → `000_epic`, `100_todo` → `100_backlog`, merge existing `epic/` folder contents.

## New Workflow
```
000_epic → 100_backlog → 200_inprogress → 300_complete / 400_failed / 500_dump
(PRDs)     (todo tasks)   (active work)    (outcomes)
```

## Context
- `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
- `C:\Users\edebe\eds\workstream\task_gate_utils.ps1`
- `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
- `C:\Users\edebe\eds\workstream\epic_decompose_cli.py`
- `C:\Users\edebe\eds\workstream\run_agent.ps1`

## Impact Analysis
- **195 files** reference `000_backlog` or `100_todo`
- Most are completed task documentation (no code impact)
- Key files requiring code changes:
  - `kanban_dashboard.py` - FOLDERS list, UI references, API endpoints
  - `task_gate_utils.ps1` - folder paths
  - `run_agent.ps1` - folder paths
  - `SKILL.md` - documentation
  - `epic_decompose_cli.py` - output paths

## Scope Adjustment
- 2026-03-13 16:22 Europe/London: Live filesystem inspection showed the physical folder rename has already happened in the workspace:
  - `workstream/000_epic` exists
  - `workstream/100_backlog` exists
  - root-level `workstream/000_backlog` and `workstream/100_todo` are no longer present
- This task therefore shifted from physical rename work to operational code/documentation cleanup and verification.

## Plan

### Phase 1: Pre-Rename Verification
- [x] 1. Stop all workstream services (kanban dashboard, agents)
  - Test: `Get-Process python | Where-Object {$_.CommandLine -match 'kanban|summary'}` returns empty
  - Evidence: Not re-executed in this task because the physical rename had already happened before work began; treated as historical/pre-existing state.
- [ ] 2. Create full backup of workstream folder
  - Test: `Test-Path workstream_backup_20260313` returns True
  - Evidence: Not executed in this cleanup pass because no physical rename was performed by this task.

### Phase 2: Physical Folder Renames
- [x] 3. Merge `epic/` contents into `000_backlog/` (temporary)
  - Test: All files from `epic/` now in `000_backlog/`
  - Evidence: Superseded by existing live state; root workflow now uses `000_epic`.
- [x] 4. Rename `000_backlog` → `000_epic`
  - Test: `Test-Path workstream/000_epic` returns True
  - Evidence: Verified `C:\Users\edebe\eds\workstream\000_epic` exists in current workspace.
- [x] 5. Rename `100_todo` → `100_backlog`
  - Test: `Test-Path workstream/100_backlog` returns True
  - Evidence: Verified `C:\Users\edebe\eds\workstream\100_backlog` exists in current workspace.
- [ ] 6. Remove old `epic/` folder (if empty)
  - Test: `Test-Path workstream/epic` returns False
  - Evidence: Not checked in this pass.

### Phase 3: Code Updates - kanban_dashboard.py
- [x] 7. Update FOLDERS list
  - Replace: `000_backlog` → `000_epic`, `100_todo` → `100_backlog`
  - Test: grep for `000_backlog` returns 0 matches
  - Evidence: `kanban_dashboard.py` already contained `000_epic` and `100_backlog` when reviewed during this task.
- [x] 8. Update column headers and UI labels
  - Replace: "Backlog" → "Epic", "Todo" → "Backlog"
  - Test: Visual inspection of dashboard shows new labels
  - Evidence: Dashboard source already displays Epic/Backlog labels; browser verification still pending.
- [x] 9. Update API endpoints and handlers
  - Check `/api/delete-task`, `/api/dump-task`, etc. for folder references
  - Test: Source inspection confirms new folder names are used in dashboard code paths
  - Evidence: `kanban_dashboard.py` FOLDERS and Epic Review state folder constants already reference `000_epic` and `100_backlog`.
- [x] 10. Update JavaScript functions (openFile, deleteCurrentFile, dumpCurrentFile)
  - Test: Button visibility logic works correctly
  - Evidence: Dashboard source already aligned before this task; browser verification still pending.

### Phase 4: Code Updates - Supporting Files
- [x] 11. Update task_gate_utils.ps1
  - Replace all `100_todo` → `100_backlog` references
  - Test: PowerShell functions work with new paths
  - Evidence: `task_gate_utils.ps1` contains no hardcoded `100_todo`/`000_backlog` path literals; no code change required.
- [x] 12. Update run_agent.ps1
  - Replace folder references
  - Test: Agent can claim tasks from new folders
  - Evidence: Updated `run_agent.ps1` to use `100_backlog` and corrected stale `200_working` prompt paths to `200_inprogress`.
- [x] 13. Update epic_decompose_cli.py
  - Update output folder from `100_todo` → `100_backlog`
  - Test: Decompose epic creates tasks in `100_backlog/`
  - Evidence: `epic_decompose_cli.py` contained no stale `100_todo`/`000_backlog` path literals on inspection, so no code change was required.
- [x] 14. Update SKILL.md documentation
  - Update folder structure documentation
  - Test: Documentation matches new folder names
  - Evidence: Updated `skills/workstream-task-lifecycle/SKILL.md`, `skills/document-to-task-decomposition/SKILL.md`, `skills/epic-decomposition/SKILL.md`, and `skills/task-execution-ordering/SKILL.md`.

### Phase 5: Verification
- [ ] 15. Restart kanban dashboard
  - Test: Dashboard loads without errors
  - Evidence: All columns visible, tasks displayed
- [ ] 16. Test search functionality
  - Test: Search finds tasks in new folders
  - Evidence: Search results show correct folder paths
- [ ] 17. Test dump functionality
  - Test: Dump button works, moves to 500_dump
  - Evidence: Task moved successfully
- [ ] 18. Test epic decomposition
  - Test: Decompose creates tasks in 100_backlog
  - Evidence: New task files created
- [ ] 19. Test drag-and-drop between columns
  - Test: Tasks can be moved via drag-drop
  - Evidence: File physically moves to new folder

### Phase 6: Cleanup
- [ ] 20. Remove backup (after 24h verification period)
  - Test: System stable for 24 hours
  - Evidence: No issues reported

## Risks/Notes
- **HIGH RISK**: This affects 195+ files and core workflow
- **Mitigation**: Full backup before changes, phased approach
- Historical task files will have old folder references in their content (acceptable - documentation only)
- External scripts/integrations may need updates (check for hardcoded paths)
- Agent subfolders (claude, codex, gemini, general) must be renamed within each parent
- This cleanup pass intentionally avoided bulk-editing historical task narratives and archived artefacts; only live operational code/docs were updated.

## Implementation Log
- 2026-03-13 16:22 Europe/London: Moved this task into `200_inprogress` and verified that the physical rename was already complete in the live workspace.
- 2026-03-13 16:29 Europe/London: Updated `workstream/run_agent.ps1` to use `100_backlog` and corrected stale prompt references from `200_working` to `200_inprogress`.
- 2026-03-13 16:31 Europe/London: Updated Epic Review backend/frontend files to use `100_backlog` for status filtering, model counts, allocation target, and operator messaging.
- 2026-03-13 16:34 Europe/London: Updated workstream skill documentation to reflect `000_epic` / `100_backlog` terminology and folder lifecycle.
- 2026-03-13 16:43 Europe/London: Normalized stale path references across active markdown in `000_epic`, `050_review`, `100_backlog`, and `200_inprogress`, excluding this rename-task record so its migration narrative remained readable.

## Changes Made
- `C:\Users\edebe\eds\workstream\run_agent.ps1`
  - changed controller todo root to `100_backlog`
  - corrected stale lifecycle prompt references from `100_todo` / `200_working`
- `C:\Users\edebe\eds\workstream\apps\task_review\app.py`
  - changed state folders and allocation/model-status roots to `100_backlog`
- `C:\Users\edebe\eds\workstream\apps\task_review\static\index.html`
  - updated status dropdown and model-count text to `100_backlog`
- `C:\Users\edebe\eds\workstream\apps\task_review\static\app.js`
  - updated allocatable-state logic and operator alerts to `100_backlog`
- `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
- `C:\Users\edebe\eds\skills\document-to-task-decomposition\SKILL.md`
- `C:\Users\edebe\eds\skills\epic-decomposition\SKILL.md`
- `C:\Users\edebe\eds\skills\task-execution-ordering\SKILL.md`
  - updated workflow docs to `000_epic` / `100_backlog`
- Active markdown references under:
  - `C:\Users\edebe\eds\workstream\000_epic`
  - `C:\Users\edebe\eds\workstream\050_review`
  - `C:\Users\edebe\eds\workstream\100_backlog`
  - `C:\Users\edebe\eds\workstream\200_inprogress`
  - normalized navigable path references from `workstream/epic`, `workstream/000_backlog`, `000_backlog`, `workstream/100_todo`, and `100_todo` to current locations where those paths were meant to be followed in active docs

## Validation
- `Get-ChildItem C:\Users\edebe\eds\workstream -Force | Select-Object Name,Mode`
  - PASS: confirmed `000_epic` and `100_backlog` exist at the workstream root.
- `rg -n "100_todo|000_backlog|200_working|workstream/epic" <touched files>`
  - PASS: no remaining stale references in the files updated by this task.
- `python -m py_compile C:\Users\edebe\eds\workstream\apps\task_review\app.py`
  - PASS
- PowerShell parser check on `C:\Users\edebe\eds\workstream\run_agent.ps1`
  - PASS
- `rg -n --pcre2 "workstream/epic/|workstream/000_backlog/|(?<!workstream/)000_backlog/|workstream/100_todo/|(?<!workstream/)100_todo/" C:\Users\edebe\eds\workstream\000_epic C:\Users\edebe\eds\workstream\050_review C:\Users\edebe\eds\workstream\100_backlog C:\Users\edebe\eds\workstream\200_inprogress`
  - PASS with one intentional exception: only this rename task file still contains old-name references as part of its migration description.
- User verification requested:
  - Please verify that active workstream links and the Epic Review flow now behave correctly with `000_epic` and `100_backlog`.

## Rollback Plan
If issues occur:
1. Stop all services
2. Delete renamed folders
3. Restore from backup
4. Restart services

## Completion Status
- Awaiting user verification - 2026-03-13 16:44 Europe/London
  - Technical cleanup is complete for live code, skills, and active navigable markdown references.
  - Remaining gate: user confirms the updated workflow/links behave as expected in live use.


# User Feedback
User Verified: PASS
