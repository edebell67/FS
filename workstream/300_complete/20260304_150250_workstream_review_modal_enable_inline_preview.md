# Workstream Task Lifecycle

- Task: Enable inline preview for generated review drafts in kanban approval modal
- Owner: codex
- Started: 2026-03-04 15:00:00
- Status: Completed

## Plan
- [x] Replace review list click action from external-open only to include an in-app preview action.  
Test: Review list entries render a Preview button calling openFile(folder, filename).
- [x] Keep explicit external open option as separate action.  
Test: Review list entries render an External button calling openAndCloseLocalReview(folder, filename).
- [x] Validate script syntax.  
Test: python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py succeeds.

## Validation Log
- Confirmed updated button wiring in checkReviewTasks() HTML template.
- python -m py_compile C:\Users\edebe\eds\workstream\kanban_dashboard.py passed.

## Files Changed
- C:\Users\edebe\eds\workstream\kanban_dashboard.py
