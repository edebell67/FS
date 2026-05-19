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

Task Summary: Every 4 hours, generate the current-date top-2 cross-product social package from source data, refresh `temp_tweet_top2.txt`, then post that exact payload through `POST /api/social/x_api_post` and record the live response.

Context:
- Workspace: `C:\Users\edebe\eds`
- Package generator: `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Generated package artifacts: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\YYYY-MM-DD\top2_cross_product_post.json` and `.md`
- Live payload file: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
- X API route: `http://localhost:5000/api/social/x_api_post`
- Health route: `http://localhost:5000/api/health`
- Workflow references:
  - `C:\Users\edebe\eds\workstream\300_complete\20260403_114522_breakout_run_top2_cross_product_package_for_current_date.md`
  - `C:\Users\edebe\eds\workstream\300_complete\20260403_114950_breakout_post_current_top2_payload_to_x.md`

Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\`

Dependency: None
Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
Scheduled For: 2026-04-06 13:00:00+01:00
Next Scheduled For: 2026-04-06 17:00:00+01:00
Spawned From: 20260406_090000_breakout_twitter_summary_returns_every_4_hours.md

## Plan

- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08` completes successfully.
  - Evidence: Generator wrote `top2_cross_product_post.json` and related package artifacts under `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: `temp_tweet_top2.txt` matched `top2_cross_product_post` exactly at 194 characters; `generated_date=2026-04-08`, `today_source_date=2026-04-08`, `today_source_last_update=2026-04-08T14:44:37.315932`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Health route returned HTTP 200 with `{"status":"ok","ts":"2026-04-08T13:45:18.133177"}` during validation and `{"status":"ok","ts":"2026-04-08T13:45:55.064293"}` during the canonical workflow run.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08` reached `submit_post` and recorded `HTTP 400 {"error":"Rate limit: wait 5 more minutes","success":false}` in `twitter_x_api_post_response.json`.

## Evidence
Objective-Delivery-Coverage: 75%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date package output was generated for this execution.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact prepared payload text for review and confirms the payload existed locally before submission.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated workflow reached API verification, generation, payload validation, and the live post submission step for `2026-04-08`.
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the exact X API posting attempt outcome for this run, including the recorded rate-limit blocker.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Objective-Proved: Proves the workflow payload validation logic still passes its targeted regression tests.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: `Pending user verification request for rate-limit retry decision`
  - Objective-Proved: Captures whether the user wants the run retried after the recorded X API cooldown expires.
  - Status: planned

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-08 14:44:45 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08`.
- 2026-04-08 14:45:05 Europe/London: Verified `temp_tweet_top2.txt` matched `top2_cross_product_post.json` and captured source metadata for the generated payload.
- 2026-04-08 14:45:18 Europe/London: Verified `GET http://localhost:5000/api/health` returned HTTP 200 with `status=ok`.
- 2026-04-08 14:45:58 Europe/London: Ran `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08`; workflow reached live submission and recorded an X API rate-limit blocker in `twitter_x_api_post_response.json`.
- 2026-04-08 14:46:12 Europe/London: Ran `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` and confirmed the targeted workflow tests passed.

## Changes Made

- No application source changes were required for this execution; the existing canonical workflow and scheduled runner already matched the task definition.
- Updated this lifecycle file with the current execution evidence, validation outputs, and blocker state for the `2026-04-08` run.

## Validation

- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08`
  - Result: Success. Wrote `top2_cross_product_post.json`, `top2_cross_product_post.md`, and refreshed `temp_tweet_top2.txt`.
- Payload comparison against `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json`
  - Result: Match `true`; payload length `194`; source metadata `generated_date=2026-04-08`, `today_source_date=2026-04-08`, `today_source_last_update=2026-04-08T14:44:37.315932`.
- `GET http://localhost:5000/api/health`
  - Result: HTTP 200 with `{"status":"ok","ts":"2026-04-08T13:45:18.133177"}`.
- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08`
  - Result: Exit code `1`. `verify_api`, `generate_content`, and `validate_payload` passed; `submit_post` returned `HTTP 400 {"error":"Rate limit: wait 5 more minutes","success":false}` and wrote `twitter_x_api_post_response.json`.
- `python -m unittest .\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
  - Result: `Ran 2 tests in 0.087s` and `OK`.
- User verification request
  - Result: Pending. Final chat response must ask whether to retry after the rate-limit cooldown or leave the recorded blocker as the outcome for this slot.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- The last successful top-2 post recorded before this run was at `2026-04-08T14:41:27.508321` with tweet ID `2041874121181519879`; the current run generated a newer payload timestamp (`14:45`) but was blocked by the API cooldown.
- The task objective is not fully delivered until a live post succeeds for the refreshed payload or the user explicitly accepts the recorded rate-limit blocker for this slot.
- After each successful execution, the scheduler should queue the next run 4 hours later.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-08T14:46:12+01:00
