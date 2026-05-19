# Task: Skills Workstream - User Completion Verification Gate

## Status
TODO

## Source
- User request: require completion verification by asking user to verify changes.
- Skill: `skills/workstream-task-lifecycle/SKILL.md`

## Task Summary
Update the workstream lifecycle skill so completion requires an explicit user verification check for user-visible behavior changes.

## Context
- Affected file: `skills/workstream-task-lifecycle/SKILL.md`
- Goal: prevent marking tasks complete before user confirms pass/fail on implemented behavior.

## Implementation Log
- 2026-02-25 11:52:41: Task created in `workstream/100_todo`.
- 2026-02-25 11:53:10: Moved task to `workstream/200_inprogress`.
- 2026-02-25 11:53:45: Updated `skills/workstream-task-lifecycle/SKILL.md` to add mandatory completion verification gate rules.
- 2026-02-25 11:54:05: Verified insertion with `rg` search for new gate headings/rules.

## Changes Made
- Updated `skills/workstream-task-lifecycle/SKILL.md`:
  - Added `## Completion Verification Gate` section.
  - Added rule to explicitly ask user to verify user-visible changes before final completion.
  - Added `Completion Status` guidance: `Awaiting user verification` when pending.
  - Added complete-move criteria including user verification request/outcome capture.

## Validation
- Command:
  - `rg -n "Completion Verification Gate|Awaiting user verification|ask the user to verify" skills/workstream-task-lifecycle/SKILL.md`
- Result:
  - Confirmed new section and required rules are present.

## Risks/Notes
- Must avoid blocking purely internal/non-user-visible tasks where user verification is not practical.

## Completion Status
Complete - skill updated and validated.
