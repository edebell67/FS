# Task: Make Task Dependency Mandatory In Skills

## Source
- User direction that every task must declare dependency explicitly, and if there is no prerequisite it must state `Dependency: None`.

## Task Summary
- Update the decomposition and lifecycle skills so dependency declaration is mandatory on every task.

## Context
- `skills/document-to-task-decomposition/SKILL.md`
- `skills/workstream-task-lifecycle/SKILL.md`
- `skills/epic-decomposition/SKILL.md`

## Dependency
Dependency: None

## Plan
- [x] 1. Review the current skill wording around dependency handling.
  - [x] Test: inspect all decomposition and lifecycle skill files for dependency requirements.
  - [x] Evidence: confirmed dependency is mentioned but not mandatory on all decomposition and lifecycle tasks.
- [x] 2. Update skills to require explicit dependency declaration for every task.
  - [x] Test: each skill must state that every task declares `Dependency`, with `Dependency: None` when there is no prerequisite.
  - [x] Evidence: updated rule text present in `document-to-task-decomposition`, `workstream-task-lifecycle`, and `epic-decomposition`.
- [x] 3. Validate the updated skill text.
  - [x] Test: `Select-String -Path "C:\Users\edebe\eds\skills\*\SKILL.md" -Pattern "Dependency: None|Dependency declaration is mandatory|Every qualifying task MUST declare dependency explicitly|every generated task must include an explicit dependency field|Dependency clarity:"`
  - [x] Evidence: targeted matches confirm the new mandatory rule is present in all relevant skills.

## Implementation Log
- 2026-03-16 16:19: Reviewed skill files and confirmed dependency is not yet mandatory.
- 2026-03-16 16:21: Updated `skills/document-to-task-decomposition/SKILL.md` to make dependency declaration mandatory for every generated task.
- 2026-03-16 16:22: Updated `skills/workstream-task-lifecycle/SKILL.md` to make explicit dependency declaration part of the required task content template.
- 2026-03-21 11:45: Discovered that `skills/epic-decomposition/SKILL.md` was missing the update on disk despite being in prompt context.
- 2026-03-21 11:50: Updated `skills/epic-decomposition/SKILL.md` to include mandatory dependency rules and updated its Validation Checklist.
- 2026-03-21 11:55: Validated all updated skills with targeted `Select-String` checks.
- 2026-03-21 12:05: Confirmed all three skills on disk are correct and consistent.

## Changes Made
- Updated `skills/document-to-task-decomposition/SKILL.md`:
  - dependency declaration is now mandatory for every generated task
  - `Dependency: None` is now required when there is no prerequisite
- Updated `skills/workstream-task-lifecycle/SKILL.md`:
  - explicit dependency declaration is now a required task content item
  - `Dependency: None` is required when a task has no prerequisite
- Updated `skills/epic-decomposition/SKILL.md`:
  - dependency declaration is now mandatory for every generated task
  - `Dependency: None` is now required when there is no prerequisite
  - Added dependency check to Validation Checklist.

## Validation
- `Select-String -Path "C:\Users\edebe\eds\skills\*\SKILL.md" -Pattern "Dependency: None|Dependency declaration is mandatory|Every qualifying task MUST declare dependency explicitly|every generated task must include an explicit dependency field|Dependency clarity:"`
- Result: pass (Verified in document-to-task-decomposition, workstream-task-lifecycle, and epic-decomposition)

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: file_output
- Artifact: `skills/document-to-task-decomposition/SKILL.md`, `skills/workstream-task-lifecycle/SKILL.md`, and `skills/epic-decomposition/SKILL.md`
- Objective-Proved: enforces mandatory dependency declaration and `Dependency: None` when there is no prerequisite
- Status: captured
- Evidence-Type: test_output
- Artifact: `Select-String` output showing the mandatory rule in all three skill files.
- Objective-Proved: confirms the mandatory dependency rule is present in all relevant skills
- Status: captured

## Completion Status
- Complete - 2026-03-21 12:10
