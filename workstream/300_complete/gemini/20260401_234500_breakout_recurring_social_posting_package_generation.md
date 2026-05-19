Priority: 2

# Recurring: Daily/Weekly Social Posting Package Generation

## Source
User request on 2026-04-01 to automate the delivery of the daily and weekly top-performing strategy summaries using the canonical return calculation.

## Task Type
recurring

## Task Attributes
- recurring_task: true
- recurrence_type: daily
- recurrence_rule: every day at 23:00
- priority: high
- execution_owner: codex

## Scope
- Generate the daily social posting package using the canonical per-strategy return rule.
- Include Forex, Indices, Metals, and Energy product types.
- Produce both structured JSON and operator-ready Markdown outputs.
- Verify that "Today" and "Weekly so far" metrics are correctly aggregated.
- Ensure the package is stored in the dated `json/live/social_posting_package/YYYY-MM-DD/` directory.

## Acceptance Criteria
- A fresh dated folder exists for every trading day.
- Markdown package contains consolidated leaderboard and per-product top 5 lists.
- Weekly figures represent the highest cumulative total for a single strategy.
- Character counts for Twitter drafts are within the 280-character limit.

## Instructions
Run the following command daily:
```powershell
python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py
```

## Progress Log
- 2026-04-01 23:45:00: Recurring task created. Initial version of the generator validated with the per-strategy weekly aggregation fix.

workflow_ready:True

## Dependency
Dependency: None

## Plan
- [ ] 1. Execute the social posting package generator script.
  - Test: python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py
  - Evidence: Captured command output.
- [ ] 2. Verify output files exist in the dated directory.
  - Test: ls C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-01\
  - Evidence: Directory listing output.
- [ ] 3. Validate Markdown content and character counts.
  - Test: Manual check of generated Markdown file.
  - Evidence: Markdown content summary and char counts.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: command output
  - Objective-Proved: execution success
  - Status: planned
- Evidence-Type: file_output
  - Artifact: C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-01\top5_weekly_posting_package.md
  - Objective-Proved: deliverable generation
  - Status: planned

## Implementation Log
- 2026-04-01 23:55:00: Initializing task with standard lifecycle template and plan.

## Changes Made
- None (recurring execution task)

## Validation
- Pending execution

## Risks/Notes
- Ensure all source stats files exist before running.

## Completion Status
- In Progress (2026-04-01 23:55:00)

workflow_ready:True
