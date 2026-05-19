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
- Source package path: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\YYYY-MM-DD\top5_weekly_posting_package.md`
- Posting path: `Twitter/X`
- Historical validated format includes one-line entries such as: `Forex | Mar 19-Mar 26 | 1. EURAUD ... | Single-contract basis. #Forex #SystemTrading`
Dependency: None
Execution Workflow: Generate the final thread-ready top-5 multi-product copy first, then post the prepared payload to Twitter/X and capture the concrete result.
Scheduled For: YYYY-MM-DD HH:MM:SS
Next Scheduled For:
Spawned From: 20260405_191500_breakout_workflow_twitter_top5_multi_product_types_every_6_hours.md

## Objective
Produce and publish the multi-product top-5 Twitter/X payload every 6 hours using the established preparation-plus-posting workflow.

## Plan
- [ ] 1. Generate or refresh the multi-product top-5 weekly posting package for the current run context.
  - [ ] Test: The source package for the run exists and contains the required product sections.
  - Evidence:
- [ ] 2. Prepare the final Twitter/X-ready payload in the validated compact posting style.
  - [ ] Test: The prepared copy follows the established one-line multi-product thread format and remains within X constraints.
  - Evidence:
- [ ] 3. Send the prepared payload to Twitter/X.
  - [ ] Test: The post or thread publish attempt returns a concrete success result or a concrete blocker.
  - Evidence:
- [ ] 4. Record the exact live outcome.
  - [ ] Test: Store the posted URL, tweet IDs, or precise failure reason without fabrication.
  - Evidence:

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: false
- Evidence-Type: payload_preparation
  - Artifact: prepared multi-product top-5 Twitter copy
  - Objective-Proved: Proves the recurring run produced the expected posting format before publishing.
  - Status: planned
- Evidence-Type: live_post_result
  - Artifact: X post/thread result
  - Objective-Proved: Proves the recurring run actually attempted or completed publishing.
  - Status: planned

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
- State: TODO
- Timestamp:
