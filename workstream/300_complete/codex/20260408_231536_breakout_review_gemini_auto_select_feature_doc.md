# Task: Review Gemini Auto-Select Feature Task Document

## Source
- User request: review `workstream/300_complete/gemini/20260407_184000_breakout_weekly_perf_auto_select_feature.md`

## Task Type
standard

## Task Attributes
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

## Task Summary
Review the Gemini task document for lifecycle compliance, requirement clarity, and implementation-risk gaps, then report findings with exact file references.

## Context
- Reviewed file: `C:\Users\edebe\eds\workstream\300_complete\gemini\20260407_184000_breakout_weekly_perf_auto_select_feature.md`
- Lifecycle skill: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
- Repository policy: `C:\Users\edebe\eds\AGENTS.md`

## Destination Folder
None

## Dependency
None

## Plan
- [x] 1. Read the target document and applicable lifecycle rules.
  - [x] Test: `Get-Content "C:\Users\edebe\eds\workstream\300_complete\gemini\20260407_184000_breakout_weekly_perf_auto_select_feature.md"` and `Get-Content "C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md" -TotalCount 260` both return expected content.
  - Evidence: Captured document body and lifecycle requirements including complete-stage and required-content rules.
- [x] 2. Identify review findings with exact line references.
  - [x] Test: `Get-Content` with numbered lines returns stable line references for the reviewed file.
  - Evidence: Numbered output captured for lines 1-37 of the reviewed document.
- [x] 3. Deliver the review summary to the user.
  - Findings drafted:
    - `P1`: file is stored in `300_complete` while it declares `IN_PROGRESS` and retains unchecked plan items
    - `P1`: required lifecycle schema sections are missing
    - `P2`: permitted-type removal behavior is undefined for already auto-promoted strategies
    - `P2`: validation plan does not directly prove cross-type scoping safety
  - [x] Test: Final response lists findings first, ordered by severity, with file references.
  - Evidence: Review response prepared from numbered file output and lifecycle rule comparison.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: manual_verification
  - Artifact: Reviewed markdown content and numbered line output for `C:\Users\edebe\eds\workstream\300_complete\gemini\20260407_184000_breakout_weekly_perf_auto_select_feature.md`
  - Objective-Proved: The review findings are grounded in the actual document text and line numbers.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`
  - Objective-Proved: Lifecycle compliance findings are checked against the repository's required workstream schema.
  - Status: captured

## Implementation Log
- 2026-04-08 23:15:36 BST: Located the target Gemini task file and workstream lifecycle instructions.
- 2026-04-08 23:15:36 BST: Read the target document, numbered its lines, and compared it against lifecycle requirements.
- 2026-04-08 23:15:36 BST: Created this Codex lifecycle file in `200_inprogress/codex`.
- 2026-04-08 23:15:36 BST: Recorded four review findings covering lifecycle state, required schema omissions, missing allowlist-removal behavior, and insufficient scoping validation.
- 2026-04-08 23:15:36 BST: Final review response prepared and task marked complete.
- 2026-04-08 23:33:00 BST: Verified the active task path supplied by the user was stale, confirmed the lifecycle record already resides in `300_complete/codex`, and updated this archive copy so the recorded artifact paths match the actual archived state.

## Changes Made
- Added this lifecycle record for the review task:
  - `C:\Users\edebe\eds\workstream\300_complete\codex\20260408_231536_breakout_review_gemini_auto_select_feature_doc.md`
- Refreshed the archived lifecycle record so the documented artifact path and validation notes match the file's actual location.

## Validation
- Ran document read on the target file and confirmed it contains 31 lines of task content plus completion metadata.
- Ran a numbered-line read to support precise review references.
- Read the lifecycle skill and confirmed the reviewed file is missing required sections such as `Task Type`, `Task Attributes`, `Destination Folder`, `Dependency`, `Evidence`, `Implementation Log`, `Changes Made`, `Validation`, and `Risks/Notes`.
- Findings prepared for final response with severity ordering and absolute file references.
- Confirmed `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260408_231536_breakout_review_gemini_auto_select_feature_doc.md` does not exist and `C:\Users\edebe\eds\workstream\300_complete\codex\20260408_231536_breakout_review_gemini_auto_select_feature_doc.md` exists, so the task is already archived in the correct lifecycle lane.

## Risks/Notes
- This review covers the task document itself, not the underlying code implementation.
- The reviewed file appears to violate both its own declared status and the repository lifecycle policy.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-08 23:15:36 BST
