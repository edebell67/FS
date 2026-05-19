Source: User request on 2026-04-03 to create a new recurring task that runs every 6 hours and combines the multi-product top-5 Twitter preparation task with the payload posting task, using `workflow` in the filename for tasks that combine workflow-ready tasks.

Task Type: standard

Task Attributes:
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- recurrence_interval_hours: 6
- priority: high
- execution_owner: codex
- workflow_ready: false

**Suggested Agent:** codex

Task Summary: Every 6 hours, prepare the multi-product top-5 weekly Twitter/X post copy from the validated package, then send the prepared payload to Twitter/X and record the live posting outcome.

Context:
- Workspace: `C:\Users\edebe\eds`
- Preparation workflow reference:
  - `C:\Users\edebe\eds\workstream\300_complete\20260326_174209_breakout_twitter_post_preparation_top5_multi_product_types.md`
- Posting workflow reference:
  - `C:\Users\edebe\eds\workstream\300_complete\20260326_192248_breakout_post_twitter_thread_multi_product_types.md`
- Workflow runner:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_top5_multi_product_workflow.py`
- Source package path:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\YYYY-MM-DD\top5_weekly_posting_package.md`
- Posting path:
  - `Twitter/X`
- Historical validated format includes one-line entries such as:
  - `Forex | Mar 19-Mar 26 | 1. EURAUD ... | Single-contract basis. #Forex #SystemTrading`

Dependency: None

Execution Workflow: Generate the final thread-ready top-5 multi-product copy first, then post the prepared payload to Twitter/X and capture the concrete result.

Scheduled For: 2026-04-04 13:00:00+01:00
Next Scheduled For: 2026-04-04 19:00:00+01:00
Spawned From: 20260404_070000_breakout_workflow_twitter_top5_multi_product_types_every_6_hours.md

## Objective
Produce and publish the multi-product top-5 Twitter/X payload every 6 hours using the established preparation-plus-posting workflow.

## Plan
- [x] 1. Generate or refresh the multi-product top-5 weekly posting package for the current run context.
  - [x] Test: The source package for the run exists and contains the required product sections.
  - Evidence: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top5_weekly_posting_package.json` was refreshed at the 2026-04-04 13:02 run and includes `forex`, `indices`, `metals`, and `energy`.
- [x] 2. Prepare the final Twitter/X-ready payload in the validated compact posting style.
  - [x] Test: The prepared copy follows the established one-line multi-product thread format and remains within X constraints.
  - Evidence: `top5_multi_product_thread_posts` contains 5 posts; the lead post is 173 chars and product posts are 240, 218, 223, and 216 chars, all single-line compact entries.
- [x] 3. Send the prepared payload to Twitter/X.
  - [x] Test: The post or thread publish attempt returns a concrete success result or a concrete blocker.
  - Evidence: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_top5_multi_product_workflow_result.json` recorded HTTP 200 success from `http://localhost:5000/api/social/x_api_thread_post`.
- [x] 4. Record the exact live outcome.
  - [x] Test: Store the posted URL, tweet IDs, or precise failure reason without fabrication.
  - Evidence: Recorded tweet IDs `2040399704312132094`, `2040399711824220405`, `2040399719445254353`, `2040399729251500530`, and `2040399736084029495` with matching X thread URLs.

## Evidence
Objective-Delivery-Coverage: 95%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top5_weekly_posting_package.json`
  - Objective-Proved: Proves the 13:02 recurring run refreshed the package and produced the thread-ready payload for all four product types.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m unittest TradeApps.breakout.fs.tests.test_social_publisher_thread TradeApps.breakout.fs.tests.test_run_twitter_top5_multi_product_workflow`
  - Objective-Proved: Proves the direct thread-publishing path and workflow payload validation still pass locally before the live run.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_top5_multi_product_workflow_status.json`
  - Objective-Proved: Proves the API health check, generation step, payload validation, publish step, and outcome-recording step all succeeded during the 2026-04-04 13:02 execution.
  - Status: captured
- Evidence-Type: url
  - Artifact: `https://x.com/i/web/status/2040399704312132094`
  - Objective-Proved: Proves a live thread root URL was returned for the published top-5 multi-product post.
  - Status: captured
- Evidence-Type: log_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_top5_multi_product_workflow_result.json`
  - Objective-Proved: Proves the exact prepared payload, API response, tweet IDs, and reply-chain URLs recorded for this run.
  - Status: captured
- Evidence-Type: user_feedback
  - Artifact: Pending user confirmation of the 2026-04-04 13:02 live thread contents at `https://x.com/i/web/status/2040399704312132094`
  - Objective-Proved: Will confirm the visible live thread content matches the expected posting package and is acceptable for completion.
  - Status: planned

## Validation Rules
- Do not mark the run successful without a concrete prepared payload and a concrete posting result.
- Do not invent tweet IDs, URLs, or post success.
- If the source package is stale or missing, record the exact blocker.
- If X posting is rate-limited or blocked, record the exact live response.

## Implementation Log
- 2026-04-04 13:02:25+01:00: Confirmed current run time and local API health (`/api/health` returned `{"status":"ok",...}`).
- 2026-04-04 13:02:28+01:00: Ran `python -m unittest TradeApps.breakout.fs.tests.test_social_publisher_thread TradeApps.breakout.fs.tests.test_run_twitter_top5_multi_product_workflow`; 6 tests passed.
- 2026-04-04 13:02:37+01:00: Executed `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_top5_multi_product_workflow.py 2026-04-04`.
- 2026-04-04 13:02:40+01:00: Workflow refreshed `top5_weekly_posting_package.json` and regenerated the compact 5-post thread payload.
- 2026-04-04 13:02:52+01:00: Workflow posted the live 5-post X thread and wrote result/status artifacts with tweet IDs and URLs.
- 2026-04-04 13:03:00+01:00: Updated this lifecycle file with captured evidence and requested user verification before archival.

## Changes Made
- Refreshed generated package outputs:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top5_weekly_posting_package.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top5_weekly_posting_package.md`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-04\top2_cross_product_post.md`
- Refreshed workflow audit artifacts:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_top5_multi_product_workflow_status.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_top5_multi_product_workflow_result.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\social_posts.json`
- Updated lifecycle tracking document:
  - `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260404_130000_breakout_workflow_twitter_top5_multi_product_types_every_6_hours.md`
- No source-code changes were required; the existing workflow implementation executed successfully as-is.

## Validation
- Command: `python -m unittest TradeApps.breakout.fs.tests.test_social_publisher_thread TradeApps.breakout.fs.tests.test_run_twitter_top5_multi_product_workflow`
  - Result: `Ran 6 tests in 0.162s` and `OK`.
- Command: `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/health`
  - Result: HTTP 200 with `{"status":"ok","ts":"2026-04-04T12:02:27.479814"}`.
- Command: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_top5_multi_product_workflow.py 2026-04-04`
  - Result: Exit code `0`.
  - Result Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_top5_multi_product_workflow_status.json`
  - Result Summary: `final_status` = `success`; `submit_post` returned HTTP 200 with 5 tweet IDs.
- Validation Request: User to verify the visible thread at `https://x.com/i/web/status/2040399704312132094` and confirm pass/fail for payload formatting and live publish correctness.

## Risks/Notes
- The preparation task does not itself carry `workflow_ready: true`, so this combined recurrence remains operationally validated by successful runs rather than by an upstream workflow-ready flag.
- The live package used fallback data for `metals` from `2026-04-03`; this is reflected in the generated package and is not fabricated.
- Auto-acceptance is disabled, so this task should remain outside `300_complete` until user verification is captured.
- Keep the established compact one-line product-specific format unless a newer validated format formally replaces it.

## Completion Status
- State: Awaiting user verification
- Timestamp: 2026-04-04T13:03:00+01:00
