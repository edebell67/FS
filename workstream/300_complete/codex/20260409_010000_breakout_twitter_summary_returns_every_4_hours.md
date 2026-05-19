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
Scheduled For: 2026-04-09 01:00:00+01:00
Next Scheduled For: 2026-04-09 05:00:00+01:00
Spawned From: 20260408_210000_breakout_twitter_summary_returns_every_4_hours.md

## Plan
- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-09` completes successfully.
  - Evidence: 2026-04-09 manual rerun completed successfully and rewrote the `2026-04-09` top-2 package artifacts.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: `temp_tweet_top2.txt` existed, measured 194 characters, and matched `top2_cross_product_post.json` exactly; the package reported `today_source_date` as `2026-04-08`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: `Invoke-RestMethod http://localhost:5000/api/health` returned `{"status":"ok","ts":"2026-04-09T00:02:02.922171"}`.

- [x] 4. Run the canonical posting workflow and capture the live route outcome.
  - [x] Test: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-09` records either a live post success or a concrete blocker in `twitter_workflow_status.json` and `twitter_x_api_post_response.json`.
  - Evidence: The scheduled `2026-04-09 01:00` run completed successfully at `2026-04-09T00:46`, recorded `final_status: success`, and captured X API HTTP 200 with tweet id `2042026313603572115`. The workflow was not replayed manually afterward to avoid creating a duplicate live post.

- [x] 5. Prevent the recurring chain from replaying overdue slots.
  - [x] Test: When this task starts, the controller rolls it forward to the next future 4-hour slot only and archives stale backlog duplicates from the same recurring chain.
  - Evidence: Backlog inspection after execution showed exactly one future instance at `workstream\100_backlog\general\20260409_050000_breakout_twitter_summary_returns_every_4_hours.md` and no stale duplicate backlog copies.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-09\top2_cross_product_post.json`
  - Objective-Proved: Proves the current execution generated the top-2 cross-product package payload for the 2026-04-09 run.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated workflow steps for verify-api, generate-content, validate-payload, and submit-post all succeeded for the live run.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the exact `POST /api/social/x_api_post` request payload and the HTTP 200 live posting response, including tweet id `2042026313603572115`.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\workstream\100_backlog\general\20260409_050000_breakout_twitter_summary_returns_every_4_hours.md`
  - Objective-Proved: Proves the recurring chain advanced to the next future `05:00` slot only.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: Pending user verification request in assistant final response for the live X post and recurrence behavior.
  - Objective-Proved: Will capture user pass/fail confirmation for the posted content and ongoing 4-hour scheduling behavior.
  - Status: planned

## Implementation Log
- 2026-04-08 17:33:00 Europe/London: Restored the recurring chain after the successful `17:00` execution so the next future slot remains active at `21:00`.
- 2026-04-09 01:00:03 Europe/London: Controller spawned the next recurring backlog instance at `workstream\100_backlog\general\20260409_050000_breakout_twitter_summary_returns_every_4_hours.md`.
- 2026-04-09 00:46:03 Europe/London: Canonical posting workflow recorded a successful live run for `2026-04-09` in `twitter_workflow_status.json`.
- 2026-04-09 00:46:12 Europe/London: X API response artifact recorded HTTP 200 with tweet id `2042026313603572115`.
- 2026-04-09 01:11:00 Europe/London: Re-ran the generator, revalidated the refreshed payload, rechecked local API health, and verified the recurring backlog state without replaying the live post.
- 2026-04-09 01:12:00 Europe/London: Updated the lifecycle file with captured evidence and marked the task as awaiting user verification.

## Changes Made
- No source-code edits were required during this execution pass because the workspace already contained the required top-2 canonical workflow and future-slot recurrence handling.
- Refreshed generated artifacts under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-09\`.
- Updated this lifecycle file with completed checklist items, validation results, and evidence references.

## Validation
- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-09`
  - Result: Passed. Rewrote the `2026-04-09` package files including `top2_cross_product_post.json` and `top2_cross_product_post.md`.
- `Invoke-RestMethod -Uri http://localhost:5000/api/health -Method Get`
  - Result: Passed. Returned `{"status":"ok","ts":"2026-04-09T00:02:02.922171"}`.
- PowerShell payload comparison between `temp_tweet_top2.txt` and `top2_cross_product_post.json`
  - Result: Passed. File existed, length was `194`, and payload matched the JSON exactly.
- Artifact review of `twitter_workflow_status.json`
  - Result: Passed. `final_status` was `success` for run date `2026-04-09`.
- Artifact review of `twitter_x_api_post_response.json`
  - Result: Passed. Captured HTTP `200`, `success: true`, and tweet id `2042026313603572115`.
- Backlog recurrence inspection under `workstream\100_backlog`
  - Result: Passed. Exactly one future recurring file remained: `20260409_050000_breakout_twitter_summary_returns_every_4_hours.md`.
- User verification request
  - Result: Pending. User confirmation will be requested for the posted content and recurrence behavior before moving this task to `300_complete`.

## Risks/Notes
- The generated 2026-04-09 package still reports `today_source_date: 2026-04-08`, which indicates the workflow used the latest available source snapshot while still producing the current-date package output.
- The live post step was intentionally not replayed after the successful scheduled run because repeating the workflow would create a duplicate X post.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-09 01:12:00+01:00
