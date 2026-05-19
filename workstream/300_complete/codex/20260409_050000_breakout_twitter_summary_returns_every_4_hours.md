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
Scheduled For: 2026-04-09 05:00:00+01:00
Next Scheduled For: 2026-04-09 09:00:00+01:00
Spawned From: 20260409_010000_breakout_twitter_summary_returns_every_4_hours.md

## Plan
- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-09` completes successfully.
  - Evidence: Captured in `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json` with generated package outputs under `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-09\`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: Captured via direct payload comparison; `temp_tweet_top2.txt` matched `top2_cross_product_post.json` at 198 chars with leaders `SI` and `GBPAUD`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Captured via manual health check returning HTTP 200 and `{"status":"ok"}` on 2026-04-09.

- [x] 4. Run the canonical posting workflow and capture the live route outcome.
  - [x] Test: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-09` records either a live post success or a concrete blocker in `twitter_workflow_status.json` and `twitter_x_api_post_response.json`.
  - Evidence: Captured by the scheduled execution artifacts showing a successful live post with tweet ID `2042075147956289599`.

- [x] 5. Prevent the recurring chain from replaying overdue slots.
  - [x] Test: When this task starts, the controller rolls it forward to the next future 4-hour slot only and archives stale backlog duplicates from the same recurring chain.
  - Evidence: Captured by the single active future backlog instance at `C:\Users\edebe\eds\workstream\100_backlog\general\20260409_090000_breakout_twitter_summary_returns_every_4_hours.md`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-09\top2_cross_product_post.json`
  - Objective-Proved: Proves the exact 2026-04-09 top-2 cross-product payload generated for this scheduled run.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated execution completed the API health check, package generation, payload validation, and post submission steps successfully.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the exact `POST /api/social/x_api_post` request text and the live HTTP 200 X-post outcome for this run.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\workstream\100_backlog\general\20260409_090000_breakout_twitter_summary_returns_every_4_hours.md`
  - Objective-Proved: Proves the recurring chain rolled forward to the next future 4-hour slot without leaving an overdue active duplicate in backlog.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\run_agent.py`
  - Objective-Proved: Proves the scheduler now normalizes recurring Twitter task dates so spawned instances reference the correct scheduled run date in their plan and artifact paths.
  - Status: captured

## Implementation Log
- 2026-04-08 17:33:00 Europe/London: Restored the recurring chain after the successful `17:00` execution so the next future slot remained active at `21:00`.
- 2026-04-09 05:00:15 Europe/London: Verified the scheduled `05:00` recurring run completed successfully via `twitter_workflow_status.json` and `twitter_x_api_post_response.json`, including the live `POST /api/social/x_api_post` success for run date `2026-04-09`.
- 2026-04-09 05:08:00 Europe/London: Patched `workstream/run_agent.py` so recurring Twitter task instances rewrite date-bound package and command references to the scheduled run date, then normalized the active `05:00` task and spawned `09:00` backlog task.

## Changes Made
- Updated `workstream\run_agent.py` recurring-task normalization to rewrite `social_posting_package\YYYY-MM-DD` artifact paths plus `generate_posting_package.py --date YYYY-MM-DD` and `run_twitter_canonical_workflow.py YYYY-MM-DD` command examples to each task instance's scheduled date.
- Normalized `workstream\200_inprogress\codex\20260409_050000_breakout_twitter_summary_returns_every_4_hours.md` and `workstream\100_backlog\general\20260409_090000_breakout_twitter_summary_returns_every_4_hours.md` so both task files now reference `2026-04-09` instead of stale `2026-04-08` dates.
- Confirmed the next active recurring backlog instance remains `workstream\100_backlog\general\20260409_090000_breakout_twitter_summary_returns_every_4_hours.md`.

## Validation
- Automated scheduled execution artifact review
  - Result: `twitter_workflow_status.json` reports `final_status: success` for `run_date: 2026-04-09`; `submit_post` recorded HTTP 200 with tweet ID `2042075147956289599`.

- Payload consistency check
  - Result: `temp_tweet_top2.txt` matched `top2_cross_product_post.json` exactly at 198 characters; the payload posted `SI leading +3,385` and `GBPAUD +1,260`.

- Manual API health check
  - Result: `GET http://localhost:5000/api/health` returned HTTP 200 with `{"status":"ok","ts":"2026-04-09T04:03:22.282430"}`.

- Recurring chain check
  - Result: the only active backlog instance for this recurring chain is `workstream\100_backlog\general\20260409_090000_breakout_twitter_summary_returns_every_4_hours.md`; no active overdue `2026-04-09` duplicate was present under `workstream\100_backlog`.

- User verification requested
  - Result: Pending user confirmation that the live X post content and the next-slot rollover behavior are acceptable.

## Risks/Notes
- I did not re-run `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-09` manually because the scheduled run had already posted successfully at `2026-04-09 04:00`, and re-running it would risk a duplicate live X post.
- This task now requires user verification because it changed live user-visible behavior and `Auto-Acceptance` is `false`.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-09 05:08:00+01:00
