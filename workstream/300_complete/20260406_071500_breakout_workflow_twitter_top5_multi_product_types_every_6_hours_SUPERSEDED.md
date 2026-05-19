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
- Preparation workflow reference: `C:\Users\edebe\eds\workstream\300_complete\20260326_174209_breakout_twitter_post_preparation_top5_multi_product_types.md`
- Posting workflow reference: `C:\Users\edebe\eds\workstream\300_complete\20260326_192248_breakout_post_twitter_thread_multi_product_types.md`
- Source package path: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-06\top5_weekly_posting_package.md`
- Posting path: `Twitter/X`
- Historical validated format includes one-line entries such as: `Forex | Mar 19-Mar 26 | 1. EURAUD ... | Single-contract basis. #Forex #SystemTrading`
Dependency: None
Execution Workflow: Generate the final thread-ready top-5 multi-product copy first, then post the prepared payload to Twitter/X and capture the concrete result.
Scheduled For: 2026-04-07 02:37:14+01:00
Next Scheduled For: 2026-04-07 08:37:14+01:00
Spawned From: 20260406_011500_breakout_workflow_twitter_top5_multi_product_types_every_6_hours.md

## Objective
Produce and publish the multi-product top-5 Twitter/X payload every 6 hours using the established preparation-plus-posting workflow.

## Plan
- [x] 1. Generate or refresh the multi-product top-5 weekly posting package for the current run context.
  - [ ] Test: The source package for the run exists and contains the required product sections.
  - Evidence:
- [x] 2. Prepare the final Twitter/X-ready payload in the validated compact posting style.
  - [ ] Test: The prepared copy follows the established one-line multi-product thread format and remains within X constraints.
  - Evidence:
- [x] 3. Send the prepared payload to Twitter/X.
  - [ ] Test: The post or thread publish attempt returns a concrete success result or a concrete blocker.
  - Evidence:
- [x] 4. Record the exact live outcome.
  - [ ] Test: Store the posted URL, tweet IDs, or precise failure reason without fabrication.
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: payload_preparation
  - Artifact: prepared multi-product top-5 Twitter copy (validated in API status)
  - Objective-Proved: Proves the recurring run produced the expected posting format.
  - Status: captured
- Evidence-Type: live_post_result
  - Artifact: Tweet IDs: 2041329449287700842, 2041329455042306474, 2041329460524335591, 2041329466811506930, 2041329473929273400
  - Objective-Proved: Proves the recurring run completed publishing.
  - Status: captured

## Validation Rules
- Do not mark the run successful without a concrete prepared payload and a concrete posting result.
- Do not invent tweet IDs, URLs, or post success.
- If the source package is stale or missing, record the exact blocker.
- If X posting is rate-limited or blocked, record the exact live response.

## Risks/Notes
- The preparation task does not itself carry `workflow_ready: true`, so this combined recurrence should be treated as operational only after end-to-end validation on a live run.
- The posting task is workflow-ready and already has live publish evidence.
- Keep the established compact one-line product-specific format unless a newer validated format formally replaces it.

## Completion Status
- State: COMPLETE (Run successful at 02:37)
- Timestamp: 2026-04-07 02:38:00

