# EP017 Reusable Marketing Outreach Runbook Task

Source: User asked whether the X outreach actions were captured because the exercise is expected to repeat for EP017 and other marketing exercises.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: true
- workflow_name: reusable marketing outreach process
- workflow_stage: backlog
- depends_on:
  - Completed EP017 X controlled outreach tasks
- feeds_into:
  - Repeatable campaign execution templates
  - Future non-EP017 marketing exercises

Task Summary: Convert the EP017 controlled outreach process into a reusable task/runbook pattern covering baseline posts, adaptive variants, rate-limit handling, URL preference, evidence capture, and channel-specific planning.

Context:
- Completed EP017 X tasks:
  - `workstream/300_complete/20260512_134923_ep017_997_controlled_outreach_run_001.md`
  - `workstream/300_complete/20260512_172614_ep017_997_remaining_landing_page_outreach.md`
- Result artifact:
  - `ep017_remaining_posts_result.json`
- User preference to preserve short `https://t.co/...` URL form in tweet text when provided.
- Future channels may include X, Reddit, LinkedIn, etc.

Destination Folder: `epics/ep_017_trader_pain_points/workstream/`

Dependency: Completed EP017 X outreach evidence and user feedback on URL/message handling.

## Plan

- [ ] 1. Extract repeatable X outreach workflow from completed tasks.
  - [ ] Test: Document required inputs, posting route, status checks, rate-guard handling, and output evidence fields.
  - Evidence: pending

- [ ] 2. Add adaptive-message decision layer.
  - [ ] Test: Define how response data should change later variants while only changing one variable at a time.
  - Evidence: pending

- [ ] 3. Add URL handling rules.
  - [ ] Test: Include explicit rule to preserve user-provided/preferred short `t.co` URLs in posted copy unless instructed otherwise.
  - Evidence: pending

- [ ] 4. Produce reusable task template or runbook.
  - [ ] Test: Generate a reusable Markdown template suitable for EP017 and other marketing exercises.
  - Evidence: pending

## Evidence

Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: this lifecycle task file
  - Objective-Proved: Reusable marketing process capture has been queued as a distinct task.
  - Status: captured

## Implementation Log

- 2026-05-12 19:21 BST: Created backlog task to turn the completed EP017 outreach exercise into a reusable marketing runbook/template.

## Changes Made

- Created backlog task:
  - `workstream/100_backlog/20260512_192105_ep017_999_reusable_marketing_outreach_runbook.md`

## Validation

```text
Created task file in workstream/100_backlog with _999_ investigation/process-capture marker.
```

## Risks/Notes

- This is deliberately separate from the already-completed X posting tasks so the process can become reusable beyond EP017.
- Adaptive changes should be based on observed response data, not immediate untracked copy churn.

## Completion Status

Status: Backlog — reusable runbook capture queued.
Timestamp: 2026-05-12 19:21:05 BST
