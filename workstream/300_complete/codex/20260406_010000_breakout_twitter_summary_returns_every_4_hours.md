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

Suggested Agent: codex

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

Dependency: None

Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\`
Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
Scheduled For: 2026-04-06 01:00:00+01:00
Next Scheduled For: 2026-04-06 05:00:00+01:00
Spawned From: `20260405_210000_breakout_twitter_summary_returns_every_4_hours.md`

## Plan

- [x] 1. Generate the current-date top-2 cross-product package from source data.
  - [x] Test: `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08` completes successfully.
  - Evidence: Generator completed successfully at 2026-04-08 14:09 Europe/London and refreshed `top2_cross_product_post.json`, `top2_cross_product_post.md`, and `temp_tweet_top2.txt` for `2026-04-08`.

- [x] 2. Validate the refreshed payload before posting.
  - [x] Test: `temp_tweet_top2.txt` is non-empty, matches `top2_cross_product_post.json`, and uses source-derived values only.
  - Evidence: `temp_tweet_top2.txt` contained the exact `top2_cross_product_post` body for `2026-04-08`, 194 characters total, with leaders `SI +4,130` and `CL +2,525`, matching `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json`.

- [x] 3. Verify the local API is reachable.
  - [x] Test: `GET http://localhost:5000/api/health` returns a concrete health response.
  - Evidence: Health probe returned `{"status":"ok","ts":"2026-04-08T13:09:24.515625"}` and the workflow health step also returned `{"status":"ok","ts":"2026-04-08T13:10:14.052691"}`.

- [x] 4. Post the refreshed payload to X.
  - [x] Test: `POST /api/social/x_api_post` returns a success response with a tweet ID or a concrete blocker such as a rate limit or credential error.
  - Evidence: `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08` exited with code `1` after recording a concrete blocker in `twitter_x_api_post_response.json`: HTTP `400` with `{"error":"Rate limit: wait 10 more minutes","success":false}`.

## Evidence

Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-08\top2_cross_product_post.json`
  - Objective-Proved: Proves which current-date top-2 package output was generated for this recurring run.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet_top2.txt`
  - Objective-Proved: Proves the exact body prepared for posting and that it matches the generated package payload.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python -m unittest TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow`
  - Objective-Proved: Proves the canonical workflow payload validation logic still accepts matching payloads and rejects mismatches after this execution.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `http://localhost:5000/api/health`
  - Objective-Proved: Proves the local API was reachable before the live posting attempt.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json`
  - Objective-Proved: Proves the gated workflow executed in order and stopped on the posting step because of a concrete X API rate-limit blocker.
  - Status: captured

- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
  - Objective-Proved: Proves the exact request body sent to `POST /api/social/x_api_post` and the concrete HTTP 400 rate-limit response from the live route.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: User verification requested in final response after execution.
  - Objective-Proved: Records that manual acceptance is still required because auto-acceptance is disabled and the live post was rate-limited.
  - Status: planned

## Implementation Log

- 2026-04-03 11:54:32 Europe/London: Replaced the previous recurring summary definition with a top-2 generate-then-post workflow that runs every 4 hours.
- 2026-04-08 14:00 Europe/London: Reviewed `skills/workstream-task-lifecycle/SKILL.md` requirements and loaded `skills/twitter-canonical-posting/SKILL.md`.
- 2026-04-08 14:02 Europe/London: Audited `run_twitter_canonical_workflow.py`, `generate_posting_package.py`, `run_twitter_consolidated_every4h.bat`, `social_publisher.py`, and the canonical workflow tests to confirm the runtime path already targeted `temp_tweet_top2.txt` and `POST /api/social/x_api_post`.
- 2026-04-08 14:09 Europe/London: Ran `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08`.
- 2026-04-08 14:09 Europe/London: Verified `GET http://localhost:5000/api/health` returned a healthy response.
- 2026-04-08 14:09 Europe/London: Ran `python -m unittest TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow`; both tests passed.
- 2026-04-08 14:10 Europe/London: Ran `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08`; workflow generation and payload validation passed, then the live post attempt was blocked by the route rate limiter and the response was captured in `twitter_x_api_post_response.json`.
- 2026-04-08 14:18 Europe/London: Normalized this lifecycle record to the required template and updated checklist, evidence, validation, and completion status based on the live run.

## Changes Made

- No production code changes were required; the existing workflow implementation already matched the task’s required top-2 generate-validate-post sequence.
- Updated this lifecycle file to:
  - add the missing `Destination Folder` declaration,
  - normalize evidence entries to allowed evidence types,
  - document the 2026-04-08 generator run, payload validation, health check, workflow test run, and live posting attempt,
  - mark checklist items complete with concrete pass evidence,
  - record the exact rate-limit blocker returned by the live X API route.

## Validation

- `python .\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-08`
  - Result: Pass
  - Summary: Refreshed `top2_cross_product_post.json`, `top2_cross_product_post.md`, and downstream package artifacts for `2026-04-08`.

- `@' from urllib import request; print(request.urlopen('http://localhost:5000/api/health', timeout=30).read().decode('utf-8')) '@ | python -`
  - Result: Pass
  - Summary: Returned `{"status":"ok","ts":"2026-04-08T13:09:24.515625"}`.

- `python -m unittest TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow`
  - Result: Pass
  - Summary: `Ran 2 tests in 0.106s` and `OK`.

- `python .\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-08`
  - Result: Blocked after validated execution
  - Summary: Exit code `1`; `twitter_workflow_status.json` recorded `verify_api=true`, `generate_content=true`, `validate_payload=true`, and `submit_post=false` because `POST /api/social/x_api_post` returned HTTP `400` with `{"error":"Rate limit: wait 10 more minutes","success":false}`.

- Manual verification request
  - Result: Pending
  - Summary: User verification requested after execution because `Auto-Acceptance` is `false`.

## Risks/Notes

- Do not fabricate timestamps, returns, counts, gaps, or labels; use only source artifacts produced by the current generator run.
- If the generated package source date lags the actual run date, record the mismatch explicitly before posting.
- The live posting path is still subject to the API route’s own cooldown window; on this run the workflow failed only at the posting step because the route returned a concrete rate-limit blocker.
- After each successful execution, the scheduler should queue the next run 4 hours later.

## Completion Status

- State: Awaiting user verification
- Timestamp: 2026-04-08 14:18 Europe/London
