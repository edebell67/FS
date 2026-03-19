# TASK: Add "Show Me" Button for Task Verification

**Workstream:** Workstream Kanban
**Epic:** User Verification Flow
**Priority:** 2
**Status:** Complete

---

## Purpose

Add a "Show Me" button to tasks marked as "Awaiting user verification" that demonstrates the deliverable for the task. This allows users to quickly verify completed work by seeing the actual output (UI, API endpoint, report, etc.) without manually navigating to find it.

## Input

- Tasks with "Awaiting user verification" status
- Task metadata containing deliverable type and location
- Existing verification modal in kanban dashboard

## Output

- "Show Me" button on verification modal/card
- Automatic demo launcher based on deliverable type:
  - **UI deliverable**: Opens browser to the relevant URL
  - **API endpoint**: Opens API docs or test endpoint
  - **File output**: Opens file explorer or displays content
  - **Code change**: Opens diff view or affected files

## Requirements

### Task Metadata
1. Tasks must specify deliverable type in markdown:
   - `Deliverable-Type: UI`
   - `Deliverable-URL: http://localhost:8080/feature`
   - Or `Deliverable-Path: /path/to/output/file`

2. Parse deliverable info when loading task

### UI Changes
1. Add "Show Me" button next to "Verify" and "Reject" buttons
2. Button only visible when deliverable info is present
3. Style: Eye icon with "Show Me" label

### Demo Actions by Type
| Type | Action |
|------|--------|
| UI | Open URL in new browser tab |
| API | Open API endpoint or Swagger docs |
| File | Open file in VS Code or display inline |
| Report | Display report content in modal |
| Code | Open GitHub diff or VS Code diff view |

## Action

1. Update task parsing to extract `Deliverable-Type` and `Deliverable-URL/Path`
2. Add "Show Me" button to verification modal in `kanban_dashboard.py`
3. Implement `showDeliverable()` JavaScript function
4. Add backend endpoint to handle file/code deliverables
5. Test with various deliverable types

## Verification

- [x] "Show Me" button appears on tasks with deliverable metadata
- [x] UI deliverables open correct URL in new tab
- [x] File deliverables open or display correctly
- [x] Button hidden when no deliverable info present
- [x] Works across all task statuses with verification flag

---

## Implementation Notes [V20260315]

**File:** `workstream/kanban_dashboard.py`

### Changes Made:

1. **Task Parsing** (lines 3909-3922):
   - Added extraction of `Deliverable-Type` and `Deliverable-URL/Path` from task markdown
   - Fields added to task JSON: `deliverable_type`, `deliverable_url`

2. **Verify Modal UI** (line 867):
   - Added "Show Me" button with purple gradient styling
   - Button only renders when `task.deliverable_url` is present
   - Eye icon (`fa-eye`) with "Show Me" label

3. **JavaScript Function** `showDeliverable(type, url)` (lines 884-917):
   - Handles URL deliverables: opens in new browser tab
   - Handles file paths: calls `/api/open-file` to open in VS Code
   - Handles relative URLs: prepends localhost:8080

4. **API Endpoint** `/api/open-file` (lines 4338-4362):
   - POST endpoint accepting `{path: "file_path"}`
   - Opens file in VS Code using subprocess

### Usage in Task Files:
```markdown
Deliverable-Type: UI
Deliverable-URL: http://localhost:8080/epic-decomposition
```
or
```markdown
Deliverable-Type: Code
Deliverable-Path: /mnt/c/Users/edebe/eds/workstream/kanban_dashboard.py
```
