# Fix Modal Layout Display

- `Source`: User bug report via screenshot
- `Task Summary`: Fix the display of the kanban task/backlog view modal. The header currently appears side-by-side with the content because of mismatched closing `<div>` tags which cause the `modal-body` to be placed outside the `modal-content` container, disrupting the flex layout. The header needs to appear at the top of the screen.
- `Context`: Kanban Dashboard UI (`kanban_dashboard.py` HTML template section, specifically the `#contentModal` element).
- `Implementation Log`:
  - 2026-03-03 10:36:30 - Task document created in `100_todo`.
- `Changes Made`: None yet.
- `Validation`:
  - Identified extraneous `</div>` elements in `#contentModal` and `#verifyModal` inside `kanban_dashboard.py` breaking CSS flex row displays. Removed them.
  - Verified proper wrapping of header buttons inside `.modal-header`.
- `Risks/Notes`: Need to double-check other modals (e.g. `verifyModal`) to ensure their HTML tags are correctly matching and nested.
- `Completion Status`: COMPLETE 2026-03-03 10:40:00
