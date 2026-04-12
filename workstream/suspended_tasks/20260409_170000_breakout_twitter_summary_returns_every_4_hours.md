# SUSPENDED: 2026-04-09 13:35

This recurring task has been suspended by user request. 
Future runs of this chain are paused until further notice.

Source: User request on 2026-04-09 to "suspend both tasks".

---
Source: User request on 2026-04-03 to mark the current top-2 package generation and X posting workflows as ready, then replace the 4-hour recurring task so it runs both in sequence and continues posting to X every 4 hours.

Task Type: standard

Task Attributes:
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- recurrence_interval_hours: 4
- priority: high
- execution_owner: codex
- workflow_ready: true

**Suggested Agent:** codex

Task Summary: Every 4 hours, generate the current-date top-2 cross-product social package from source data, refresh `temp_tweet_top2.txt`, post that payload through `POST /api/social/x_api_post`, and keep the recurring chain aligned to the next future 4-hour slot instead of replaying overdue runs.

Context:
- Workspace: `C:\Users\edebe\eds`
- Package generator: `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Canonical workflow: `C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py`
- Generated package artifacts: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-09\top2_cross_product_post.json` and `.md`
- Live payload file: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
- Workflow status artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
- X API response artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
- Scheduler controller: `C:\Users\edebe\eds\workstream\run_agent.py`

Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\`; `C:\Users\edebe\eds\workstream\`
Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
Scheduled For: 2026-04-09 17:00:00+01:00
Next Scheduled For: 2026-04-09 21:00:00+01:00
Spawned From: 20260409_130000_breakout_twitter_summary_returns_every_4_hours.md

## Plan
- [ ] 1. Generate the current-date top-2 cross-product package from source data.
  - [ ] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-09` completes successfully.
  - Evidence:

- [ ] 2. Validate the refreshed payload before posting.
  - [ ] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence:

- [ ] 3. Verify the local API is reachable.
  - [ ] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence:

- [ ] 4. Run the canonical posting workflow and capture the live route outcome.
  - [ ] Test: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-09` records either a live post success or a concrete blocker in `twitter_workflow_status.json` and `twitter_x_api_post_response.json`.
  - Evidence:

- [ ] 5. Prevent the recurring chain from replaying overdue slots.
  - [ ] Test: When this task starts, the controller rolls it forward to the next future 4-hour slot only and archives stale backlog duplicates from the same recurring chain.
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-09\top2_cross_product_post.json`
  - Objective-Proved: Proves the current-date top-2 cross-product package was generated.
  - Status: planned

- Evidence-Type: log_output
  - Artifact: `TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the end-to-end workflow status for this run.
  - Status: planned

- Evidence-Type: log_output
  - Artifact: `TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the live X API response outcome for this run.
  - Status: planned

## Implementation Log
- 2026-04-09 13:07:00 Europe/London: Task spawned from the 13:00 execution and queued for 17:00.

## Changes Made
- None yet.

## Validation
- None yet.

## Risks/Notes
- Task completion remains pending user verification because this is a user-visible live posting workflow and `Auto-Acceptance` is `false`.

## Completion Status
- State: TODO
- Timestamp:
