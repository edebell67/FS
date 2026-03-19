# End-to-End Workstream Management Process

## Purpose

This runbook defines the current enforced end-to-end workflow for managing work in this repository. It reflects the live rules in the task lifecycle skill, the decomposition skill, and the current kanban review behavior.

## Core Principles

- One distinct task = one lifecycle file.
- The lifecycle file is the single source of truth for the task narrative.
- Tasks move through folders as work progresses.
- Completion requires tests plus normalized evidence.
- User-visible work requires either manual verification or valid auto-acceptance.
- Evidence must remain reviewable on demand through `Show Me`.

## Folder Model

```text
workstream/
|- 000_epic/        High-level specs, PRDs, strategic documents
|- 050_review/      Review-stage operational items used by the dashboard
|- 100_todo/        Atomic tasks waiting to start
|- 200_inprogress/  Active tasks
|- 300_complete/    Finished and verified or auto-accepted tasks
|- 400_failed/      Explicit failed outcomes
|- 500_dump/        Operational dump/archive area
'- .process/        Process/runbook documentation
```

## Lifecycle Overview

1. Intake
- If the work starts from a PRD/spec/epic, create or use a file in `workstream/000_epic`.
- If the work is already atomic, create a task file in `workstream/100_todo`.

2. Decomposition
- For epic/spec work, use the decomposition process in `skills/document-to-task-decomposition/SKILL.md`.
- Create atomic tasks in `workstream/100_todo`.
- Rename processed epics with `_processed.md` when decomposition is complete.

3. Task Creation
- Create one file per task using:
  - `yyyymmdd_hhmmss_{project}_{unique_task}.md`
- Keep all task narrative in that one file.

4. Start Work
- Move the file from `workstream/100_todo` to `workstream/200_inprogress`.
- Update the same file continuously while work is active.

5. Execute Sequentially
- The `Plan` section must be step-based.
- Each step must include:
  - the step itself
  - an exact test
  - evidence of pass
- Do not start the next step until the current step is implemented, tested, and evidenced.

6. Record Changes and Validation
- Update:
  - `Implementation Log`
  - `Changes Made`
  - `Validation`
- Record exact files, commands, and summarized results.

## Mandatory Task File Structure

Each qualifying task file must include:

- `Source`
- `Task Summary`
- `Context`
- `Plan`
- `Implementation Log`
- `Changes Made`
- `Validation`
- `Evidence`
- `Risks/Notes`
- `Completion Status`

## Mandatory Evidence Schema

Every qualifying task must include an `Evidence` section with:

```markdown
## Evidence
- Objective-Delivery-Coverage: <0-100>%
- Auto-Acceptance: true|false
- Evidence-Type: <type>
  - Artifact: <path|url|output|not_applicable>
  - Objective-Proved: <what this proves>
  - Status: planned|captured|not_applicable
```

### Evidence Rules

- `Objective-Delivery-Coverage: 100%` means the recorded evidence claims full objective delivery.
- Any value below `100%` means the evidence is partial, conditional, or still needs reviewer judgement.
- `Auto-Acceptance: true` is the default for new tasks unless manual review is explicitly required.
- `Auto-Acceptance: false` forces manual acceptance even if coverage is `100%`.

### Allowed Evidence Types

- `demo`
- `url`
- `screenshot`
- `test_output`
- `log_output`
- `file_output`
- `diff`
- `manual_verification`
- `user_feedback`
- `not_applicable`

### Evidence Expectations

- User-visible tasks should include at least one deliverable-facing evidence item such as `demo`, `url`, `screenshot`, or `manual_verification`.
- Implementation/refactor/bugfix tasks should include at least one technical proof item such as `test_output`, `log_output`, `file_output`, or `diff`.
- `Validation` explains what was run.
- `Evidence` states what artifact proves completion.

## Completion Rules

A task can only be treated as complete when:

1. All `Plan` items are completed in order.
2. Each required test was executed.
3. Required evidence items are present and captured.
4. `Objective-Delivery-Coverage` is stated explicitly.
5. One of the following is true:
   - manual verification has been requested and resolved, or
   - auto-acceptance criteria are met.

## Manual Verification Gate

For user-visible work:

- Do not mark the task fully complete until verification is addressed.
- If waiting on human confirmation, use:
  - `Completion Status: Awaiting user verification`
- Record the review outcome in `Evidence` using:
  - `Evidence-Type: manual_verification`, or
  - `Evidence-Type: user_feedback`

## Auto-Acceptance Rule

Auto-acceptance is allowed only when both are true:

- `Objective-Delivery-Coverage: 100%`
- `Auto-Acceptance: true`

When those conditions are met, the kanban process may promote the task automatically from `200_inprogress` to `300_complete`.

If `Auto-Acceptance: false`, the task must stay manual-review only, even at `100%`.

## Kanban Review Behavior

The current kanban dashboard behavior includes:

- `VERIFY` button for tasks in `200_inprogress` that need verification
- `SHOW ME` button for tasks with evidence
- `SHOW ME` remains available in accepted tasks in `300_complete`
- evidence parsing from the normalized `Evidence` section
- display of:
  - `Objective-Delivery-Coverage`
  - `Auto-Acceptance`
  - evidence items and artifacts

### What `Show Me` Does

`Show Me` is the on-demand evidence review entry point.

It can surface and open:

- URLs
- demos
- screenshots
- logs
- files
- diffs
- legacy deliverable paths

This means accepted tasks remain reviewable after completion.

## Promotion Rules

### 000_epic -> 100_todo
- Happens through decomposition into atomic tasks.

### 100_todo -> 200_inprogress
- Happens when active work starts.

### 200_inprogress -> 300_complete
- Happens after:
  - validation passes, and
  - evidence is captured, and
  - either manual verification passes or auto-acceptance criteria are met.

### 200_inprogress -> 100_todo
- Can happen when verification fails and rework is required.

### Any active state -> 400_failed
- Used for explicit failed outcomes when work is not accepted and not simply returning to backlog.

## Epic Closure

An epic/backlog item is only complete when:

1. All derived tasks are in `300_complete`.
2. The epic/backlog file is updated with links to the completed tasks.
3. The epic/backlog is then moved to `300_complete`.

## Practical Review Flow

1. Open the task in kanban.
2. Read `Task Summary`, `Changes Made`, and `Validation`.
3. Check `Objective-Delivery-Coverage`.
4. Check `Auto-Acceptance`.
5. Use `Show Me` to inspect the actual evidence artifacts.
6. Decide:
- accept manually
- fail and request rework
- or allow auto-acceptance if the task is eligible

## Source of Truth

This runbook is derived from:

- `skills/workstream-task-lifecycle/SKILL.md`
- `skills/document-to-task-decomposition/SKILL.md`
- `workstream/kanban_dashboard.py`

If those files change, this runbook should be updated to stay aligned.
