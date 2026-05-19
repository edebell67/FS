# Task: Make Task Dependency Mandatory In Skills

## Source
- User direction that every task must declare dependency explicitly, and if there is no prerequisite it must state `Dependency: None`.

## Task Summary
- Update the decomposition and lifecycle skills so dependency declaration is mandatory on every task.

## Context
- `skills/document-to-task-decomposition/SKILL.md`
- `skills/workstream-task-lifecycle/SKILL.md`

## Plan
- [x] 1. Review the current skill wording around dependency handling.
  - [x] Test: inspect both skill files for dependency requirements.
  - [x] Evidence: confirmed dependency is mentioned only as a clarity rule and is not mandatory on every task.
- [ ] 2. Update both skills to require explicit dependency declaration for every task.
  - [x] Test: each skill must state that every task declares `Dependency`, with `Dependency: None` when there is no prerequisite.
  - [x] Evidence: updated rule text present in both skill files.
- [ ] 3. Validate the updated skill text.
  - [x] Test: `rg -n "Dependency: None|Dependency declaration is mandatory|every task must declare" ...`
  - [x] Evidence: targeted matches confirm the new mandatory rule is present.

## Implementation Log
- 2026-03-16 16:19: Reviewed both skill files and confirmed dependency is not yet mandatory.
- 2026-03-16 16:21: Updated `skills/document-to-task-decomposition/SKILL.md` to make dependency declaration mandatory for every generated task and to require `Dependency: None` when there is no prerequisite.
- 2026-03-16 16:22: Updated `skills/workstream-task-lifecycle/SKILL.md` to make explicit dependency declaration part of the required task content template.
- 2026-03-16 16:23: Validated the new rule text with targeted `rg` checks.

## Changes Made
- Updated `skills/document-to-task-decomposition/SKILL.md`:
  - dependency declaration is now mandatory for every generated task
  - `Dependency: None` is now required when there is no prerequisite
  - the example task structure now includes a dependency field
- Updated `skills/workstream-task-lifecycle/SKILL.md`:
  - explicit dependency declaration is now a required task content item
  - `Dependency: None` is required when a task has no prerequisite

## Validation
- `rg -n "Dependency: None|Dependency declaration is mandatory|Every qualifying task MUST declare dependency explicitly|every generated task must include an explicit dependency field|Dependency clarity:" skills\\document-to-task-decomposition\\SKILL.md skills\\workstream-task-lifecycle\\SKILL.md`
- Result: pass

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: false
- Evidence-Type: file_output
- Artifact: `skills/document-to-task-decomposition/SKILL.md` and `skills/workstream-task-lifecycle/SKILL.md`
- Objective-Proved: enforces mandatory dependency declaration and `Dependency: None` when there is no prerequisite
- Status: captured
- Evidence-Type: test_output
- Artifact: `rg -n "Dependency: None|Dependency declaration is mandatory|Every qualifying task MUST declare dependency explicitly|every generated task must include an explicit dependency field|Dependency clarity:" skills\\document-to-task-decomposition\\SKILL.md skills\\workstream-task-lifecycle\\SKILL.md`
- Objective-Proved: confirms the mandatory dependency rule is present in both skills
- Status: captured

## Completion Status
- Complete - 2026-03-16 16:23 Europe/London


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:30
