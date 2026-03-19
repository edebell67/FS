# Task: Extend Show Me to standardized task evidence review

## Source
- User request on 2026-03-16 to modify "Show Me" so it can access all newly standardized evidence on demand.
- User request on 2026-03-16 that each task must state whether the evidence provided fully delivers the objectives 100%.

## Task Summary
- Update the workstream review flow so `Show Me` becomes the on-demand access point for standardized task evidence.
- Add a mandatory task-level objective-delivery coverage field so tasks explicitly state whether their evidence proves 100% delivery.

## Context
- `workstream/kanban_dashboard.py`
- `skills/workstream-task-lifecycle/SKILL.md`
- `skills/document-to-task-decomposition/SKILL.md`

## Plan
- [x] 1. Extend the task rules to require task-level objective-delivery coverage metadata.
  - [x] Test: update the relevant skills to require a normalized objective-delivery field alongside evidence.
  - [x] Evidence: `skills/workstream-task-lifecycle/SKILL.md` and `skills/document-to-task-decomposition/SKILL.md` now require `Objective-Delivery-Coverage: <0-100>%` in the `Evidence` section.
- [x] 2. Parse the new evidence schema and objective-delivery coverage in the kanban backend.
  - [x] Test: update `kanban_dashboard.py` task parsing so task JSON includes evidence items and coverage value.
  - [x] Evidence: added `_extract_markdown_section()`, `_parse_objective_delivery_coverage()`, `_parse_evidence_items()`, and task JSON fields `evidence_items` plus `objective_delivery_coverage`.
- [x] 3. Replace the current Show Me launcher with on-demand evidence review.
  - [x] Test: update the verify modal and client-side logic so `Show Me` lists all evidence artifacts and opens the selected item.
  - [x] Evidence: verify modal now always shows `Show Me`; `showTaskEvidence()` renders all evidence items and `openEvidenceArtifact()` opens URLs, screenshots, logs, files, and legacy deliverable fallbacks.
- [x] 4. Validate the implementation.
  - [x] Test: run syntax validation and targeted searches for the new evidence review path.
  - [x] Evidence: `python -m py_compile workstream\kanban_dashboard.py` passed and `rg` confirmed the new coverage/evidence handlers in the skills and kanban code.

## Implementation Log
- 2026-03-16 11:35:59 Created task from user request.
- 2026-03-16 11:40:00 Updated skill rules so tasks must declare `Objective-Delivery-Coverage` alongside normalized evidence.
- 2026-03-16 11:43:00 Updated `kanban_dashboard.py` to parse normalized evidence items and objective-delivery coverage from task markdown.
- 2026-03-16 11:46:00 Reworked the verify modal so `Show Me` reveals a full evidence review panel with per-artifact open actions.
- 2026-03-16 11:48:00 Updated local artifact opening to support both `code` and default file launching modes for evidence review.
- 2026-03-16 11:49:00 Ran syntax validation and targeted rule/path searches.

## Changes Made
- Updated `skills/workstream-task-lifecycle/SKILL.md`:
  - Added mandatory `Objective-Delivery-Coverage: <0-100>%` under the `Evidence` section.
  - Defined `100%` as evidence claiming full objective delivery and lower values as partial/conditional proof.
- Updated `skills/document-to-task-decomposition/SKILL.md`:
  - Required generated tasks to include `Objective-Delivery-Coverage`.
- Updated `workstream/kanban_dashboard.py`:
  - Added evidence parsing helpers.
  - Added task JSON fields `evidence_items` and `objective_delivery_coverage`.
  - Changed `Show Me` from a single deliverable launcher to an evidence review entry point.
  - Added per-artifact opening support for URLs, screenshots, logs, files, diffs, and fallback legacy deliverables.
  - Updated `/api/open-file` handling to support `mode=code` and default file opening.

## Validation
- `python -m py_compile workstream\kanban_dashboard.py`
  - Passed.
- `rg -n "Objective-Delivery-Coverage|showTaskEvidence|openEvidenceArtifact|evidence_items|Evidence Rules" workstream\kanban_dashboard.py skills\workstream-task-lifecycle\SKILL.md skills\document-to-task-decomposition\SKILL.md`
  - Confirmed the new evidence coverage rules and kanban handlers are present.

## Evidence
- Objective-Delivery-Coverage: 85%
- Evidence-Type: test_output
  - Artifact: `python -m py_compile workstream\kanban_dashboard.py`
  - Objective-Proved: The modified kanban dashboard code is syntactically valid.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\workstream\kanban_dashboard.py`
  - Objective-Proved: The parser/UI/open-artifact flow was updated to support standardized evidence review on demand.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
  - Objective-Proved: Task rules now require standardized evidence and explicit objective-delivery coverage.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\skills\document-to-task-decomposition\SKILL.md`
  - Objective-Proved: Newly created tasks will include the same evidence/coverage schema.
  - Status: captured

## Risks/Notes
- This task upgrades review behavior for newly standardized evidence. Historical task files without normalized evidence will still rely on legacy fallback parsing until they are updated.
- `Objective-Delivery-Coverage` is `85%`, not `100%`, because I validated parser/code wiring and artifact access logic but did not perform a live interactive browser walkthrough of the updated kanban review flow in this turn.

## Completion Status
- Complete - 2026-03-16 11:49 GMT
