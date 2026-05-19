# Task: Epic Task Decomposition Screen

## Status
TODO

## Source
- **Project**: Kanban Dashboard / Workstream Management
- **Skill Reference**: `skills/epic-decomposition/SKILL.md`

## Metadata
**Epic:** Kanban Epic Decomposition
**Workstream:** A — UI Integration
**Epic Sequence:** 1.1
**Depends On:** none
**Blocks:** none
**Readiness:** ready
**Priority:** 2
**Epic Output Folder:** C:\Users\edebe\eds\workstream

## Description
Implement a new Epic Task Decomposition screen accessible from both the Kanban Dashboard and Epic Review screen. This screen enables users to browse for an epic document (markdown file) from ANY folder, trigger automated task decomposition using the `epic-decomposition` skill, and generate properly formatted task files that integrate seamlessly with the Epic Review workflow.

## Objective
Streamline the process of breaking down high-level epic documents into actionable, atomic tasks that can be reviewed, allocated, and tracked through the existing Epic Review system.

## Sub-tasks

### Phase 1: UI Integration
- [ ] Add "Epic Decomposition" button to Kanban Dashboard header (alongside existing Epic Review button)
- [ ] Add "Decompose Epic" button/link to Epic Review screen
- [ ] Create new route `/epic-decomposition` in `kanban_dashboard.py`
- [ ] Design decomposition screen UI with file browser component

### Phase 2: File Browser Implementation
- [ ] Implement file browser modal that can navigate ANY folder (not restricted to backlog)
- [ ] Default starting location: `workstream/000_backlog/` but allow navigating up/out
- [ ] Support browsing to `epic/` folder or any other user-specified path
- [ ] Support browsing subdirectories (codex, gemini, claude, general)
- [ ] Display file preview on selection (first 500 chars of markdown)
- [ ] Filter to show only `.md` files
- [ ] Add API endpoint `GET /api/browse-files?path=...` to list files in any directory

### Phase 3: Decomposition Engine (per `epic-decomposition` skill)
- [ ] Create `decompose_epic()` function implementing the skill workflow
- [ ] **Step 1 - Parse Epic Structure**: Identify workstreams by patterns:
  - `# WORKSTREAM {LETTER} — {NAME}`
  - `## WORKSTREAM {LETTER} — {NAME}`
- [ ] **Step 2 - Extract Tasks**: For each workstream, identify tasks by patterns:
  - `## TASK {ID} {Title}`
  - `### TASK {ID} {Title}`
  - Extract: Purpose, Input, Output, Fields, Action, Verification
- [ ] **Step 3 - Generate Task Files**: Using naming convention below
- [ ] **Step 4 - Organize by Agent**: Distribute to agent folders based on assignment

### Phase 4: Naming Convention Compliance
**File Naming Convention (from skill):**
```
{yyyymmdd}_{hhmmss}_{epic_snake_case}_workstream{Letter}_{task_name_snake_case}.md
```

**Rules to implement:**
- [ ] Include epic name in snake_case after timestamp (enables filtering/grouping by epic)
- [ ] Use consistent timestamp base for all tasks in a decomposition batch
- [ ] Increment seconds to maintain sort order within workstream
- [ ] Use snake_case for all name components (lowercase, underscores)
- [ ] Keep task names concise but descriptive
- [ ] Epic name in filename MUST match `**Epic:**` metadata field inside the task file

**Output Location:**
```
workstream/100_todo/{agent}/
├── {timestamp}_{epic}_workstream{X}_{task_name}.md
```

### Phase 5: Task File Template Implementation
Each generated task file MUST follow this structure:
```markdown
# TASK {ID}: {Task Title}

**Workstream:** {Letter} — {WORKSTREAM NAME}
**Epic:** {Epic Title}
**Status:** [ ] Not Started

---

## Purpose
{Why this task exists}

## Input
{What this task requires}

## Output
{What this task produces}

## Fields / Components (if applicable)
- {field_1}
- {field_2}

## Verification
- [ ] {Verification criteria}

---

## Notes
_Add implementation notes here_
```

### Phase 6: Epic Review Integration
- [ ] Ensure `_parse_epic_review_task()` extracts `**Epic:**` field correctly
- [ ] Verify `_list_epics()` picks up new epic in dropdown (grouped by Epic field)
- [ ] Confirm `get_epic_tasks()` returns all tasks for new epic
- [ ] Verify `_extract_task_id()` can parse task IDs like `A1`, `B2`, etc.
- [ ] Test allocation workflow for decomposed tasks
- [ ] Verify workstream letter extracted by `_extract_workstream_group()` for allocation matrix

### Phase 7: API Endpoints
- [ ] `GET /api/browse-files?path=...` - List files in any directory (with parent navigation)
- [ ] `POST /api/decompose-epic` - Trigger decomposition of selected epic
  - Request: `{ "epic_path": "/path/to/epic.md", "agent_assignments": {"A": "gemini", "B": "claude"} }`
  - Response: `{ "success": true, "tasks_created": [...], "epic_slug": "...", "validation": {...} }`
- [ ] `GET /api/decomposition-preview` - Preview task breakdown before creation

## Verification Test

### Test 1: Navigation Access
1. Start Kanban Dashboard server
2. Verify "Epic Decomposition" button appears on main dashboard
3. Click button and confirm navigation to `/epic-decomposition`
4. Navigate to Epic Review screen
5. Verify "Decompose Epic" link/button is present
6. Click and confirm navigation to `/epic-decomposition`

### Test 2: File Browser - Any Folder
1. Open Epic Decomposition screen
2. Click "Browse" button
3. Verify file browser shows contents of default folder
4. Navigate UP to parent directory
5. Navigate to `epic/` folder (or any other folder)
6. Select a `.md` file
7. Verify file preview displays correctly

### Test 3: Task Generation with Correct Naming
1. Select an epic document with workstreams A, B, C
2. Assign agents: A→gemini, B→claude, C→codex
3. Click "Decompose" button
4. Verify tasks are created in correct agent folders:
   - `workstream/100_todo/gemini/20260311_XXXXXX_{epic}_workstreamA_*.md`
   - `workstream/100_todo/claude/20260311_XXXXXX_{epic}_workstreamB_*.md`
   - `workstream/100_todo/codex/20260311_XXXXXX_{epic}_workstreamC_*.md`
5. Verify timestamp increments by 1 second for each task in workstream
6. Open a generated task and verify:
   - `**Epic:**` field matches epic name in filename
   - `**Workstream:**` field shows letter and name
   - Template structure is complete

### Test 4: Epic Review Integration
1. After decomposition, navigate to Epic Review screen
2. Verify new epic appears in the epic dropdown list
3. Select the new epic
4. Verify all generated tasks appear in the task list
5. Verify workstream grouping works (filter by workstream letter)
6. Select a task and allocate to different agent
7. Verify task moves correctly
8. Refresh Epic Review and confirm task count updates

### Test 5: Validation Checklist (from skill)
After decomposition, verify:
- [ ] All tasks from epic are represented
- [ ] Each task file has complete metadata (Epic, Workstream, Status)
- [ ] Verification criteria preserved from epic
- [ ] File naming follows convention exactly
- [ ] Tasks organized into correct agent folders
- [ ] No orphaned tasks (all have workstream assignment)

## Technical Notes

### File Dependencies
- `workstream/kanban_dashboard.py` - Main server (add routes and decomposition logic)
- `workstream/apps/task_review/static/` - Epic Review UI assets
- `skills/epic-decomposition/SKILL.md` - Authoritative reference for naming and structure

### Key Functions to Implement
```python
def _browse_files(path: str) -> dict[str, Any]:
    """List files and folders in any directory with parent navigation."""

def _parse_epic_workstreams(content: str) -> list[dict]:
    """Extract workstreams from epic document."""

def _parse_workstream_tasks(workstream_content: str) -> list[dict]:
    """Extract tasks from a workstream section."""

def decompose_epic(
    epic_path: str,
    agent_assignments: dict[str, str]
) -> dict[str, Any]:
    """Parse epic document and generate task files per skill spec."""

def _generate_task_filename(
    timestamp_base: str,
    epic_slug: str,
    workstream_letter: str,
    task_name: str,
    sequence: int
) -> str:
    """Generate filename following: {yyyymmdd}_{hhmmss}_{epic}_workstream{X}_{task}.md"""

def _render_decomposition_html() -> str:
    """Render the epic decomposition screen."""
```

### Agent Assignment Guidelines (from skill)
| Agent | Best For |
|-------|----------|
| **gemini** | Data schemas, database work, backend infrastructure |
| **claude** | Content generation, UI/UX, documentation, creative tasks |
| **codex** | Mobile apps, client applications, integrations |
| **general** | Unassigned or cross-cutting tasks |

## Completion Date
YYYY-MM-DD HH:MM
