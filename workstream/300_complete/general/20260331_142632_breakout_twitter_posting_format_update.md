# Twitter Posting Format Update

## Source
User request on 2026-03-31 to update the social posting workflow to a new posting format that shows top return by product for `Today` and `Weekly so far`, includes necessary hashtags, and supports more regular posting.

## Task Type
standard

## Task Attributes
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false
- depends_on: []
- feeds_into: []

## Task Summary
Update the Strategy Warehouse social posting generator and related skill/workflow documentation so the primary Twitter/X draft uses the new structure:
- update timestamp
- `Today` ranking by top-return product
- `Weekly so far` ranking by top-return product
- optional up/down movement markers where prior package data exists
- `Full details to Follow`
- necessary posting hashtags

## Context
- Generator:
  - `TradeApps/breakout/fs/tools/social_posting_package/generate_posting_package.py`
- Workflow reference:
  - `TradeApps/breakout/fs/tools/social_posting_package/README.md`
- Posting skill:
  - `skills/strategy-warehouse-social-posting/SKILL.md`
- Posting automation guidance:
  - `skills/twitter-automation/SKILL.md`
- Current package output still uses the older `Current leaders:` format.

## Dependency
Dependency: None

## Plan

- [x] 1. Update the package generator so the consolidated draft is built from the new `Today / Weekly so far / Full details to Follow` structure.
  - [x] Test: Run the generator and inspect the consolidated draft in the JSON/Markdown package output.
  - Evidence: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py` regenerated the package successfully and the consolidated draft in `top5_weekly_posting_package.md` now uses `Update at`, `Today`, `Weekly so far`, and `Full details to follow.` sections.

- [x] 2. Add concise, reusable hashtags appropriate for regular Strategy Warehouse posting.
  - [x] Test: Confirm the consolidated draft includes the selected hashtags and remains suitable for X/Twitter posting workflow.
  - Evidence: Consolidated draft now ends with `#StrategyWarehouse #FuturesTrading #AlgoTrading`, and the package generator persists the hashtag set in `consolidated_hashtags`.

- [x] 3. Update the local skill/workflow docs so operators and automations point to the new format.
  - [x] Test: Review the updated skill and README text and confirm the old `Current leaders` guidance has been replaced.
  - Evidence: Updated `skills/strategy-warehouse-social-posting/SKILL.md`, `skills/twitter-automation/SKILL.md`, and `TradeApps/breakout/fs/tools/social_posting_package/README.md` now describe the new consolidated posting flow.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: diff
  - Artifact: `TradeApps/breakout/fs/tools/social_posting_package/generate_posting_package.py`, `TradeApps/breakout/fs/tools/social_posting_package/README.md`, `skills/strategy-warehouse-social-posting/SKILL.md`, `skills/twitter-automation/SKILL.md`, `workstream/200_inprogress/20260331_134840_workstream_twitter_draft_automation_twice_daily.md`
  - Objective-Proved: Proves the generator, operator workflow, skills, and recurring automation framing were updated to the new posting format and hashtag requirements.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py` => `[INFO] JSON package written to C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-30\top5_weekly_posting_package.json` and `[INFO] Markdown package written to C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-30\top5_weekly_posting_package.md`
  - Objective-Proved: Proves the revised posting package generator runs successfully and writes updated outputs.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: Updated consolidated draft in `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-30\top5_weekly_posting_package.md`
  - Objective-Proved: Supports visual review of the new draft format and hashtag line before regular posting begins.
  - Status: planned

## Implementation Log
- 2026-03-31 14:26:32 +01:00 — Task created from user request to update the Twitter/X draft format and hashtags for regular posting.
- 2026-03-31 14:28:00 +01:00 — Updated the posting package generator to build consolidated `Today` and `Weekly so far` product-leader sections with a fixed hashtag line.
- 2026-03-31 14:29:00 +01:00 — Updated the social posting skill, workflow README, and Twitter automation guidance to point to the new consolidated draft format.
- 2026-03-31 14:30:11 +01:00 — Regenerated the social posting package and confirmed the new draft text appears in the dated Markdown and JSON outputs.
- 2026-03-31 14:37:33 +01:00 — Corrected the output-folder behavior so package generation creates a fresh folder for the actual update date (`2026-03-31`) instead of reusing the source-data target date folder.

## Changes Made
- `TradeApps/breakout/fs/tools/social_posting_package/generate_posting_package.py`
  - Replaced the old `Current leaders` consolidated post with `Update at / Today / Weekly so far / Full details to follow.` output.
  - Added global top-product extraction across all included product types for daily and weekly ranking.
  - Added optional weekly rank movement based on the latest prior generated package when comparable metadata exists.
  - Added consolidated hashtag output: `#StrategyWarehouse #FuturesTrading #AlgoTrading`.
  - Changed package output-folder selection to use the actual generation date, creating a fresh dated folder for each update run.

- `TradeApps/breakout/fs/tools/social_posting_package/README.md`
  - Updated the documented workflow and review checklist to prioritize the new consolidated draft structure.

- `skills/strategy-warehouse-social-posting/SKILL.md`
  - Updated the skill example and operator guidance to use the new post structure and hashtag line.

- `skills/twitter-automation/SKILL.md`
  - Updated posting review guidance so operators check the new consolidated draft before live posting.

- `workstream/200_inprogress/20260331_134840_workstream_twitter_draft_automation_twice_daily.md`
  - Updated the recurring automation framing to anchor on the social posting package workflow and new consolidated draft format.

- `workstream/200_inprogress/20260331_142632_breakout_twitter_posting_format_update.md`
  - Updated lifecycle documentation with implementation and validation evidence.

## Validation
- `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
  - Result: `[INFO] JSON package written to C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-31\top5_weekly_posting_package.json`
  - Result: `[INFO] Markdown package written to C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-31\top5_weekly_posting_package.md`
- `Test-Path 'C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-31'`
  - Result: `True`
- `Get-ChildItem 'C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-03-31' -File | Select-Object -ExpandProperty Name`
  - Result: `_top_one.json`, `top5_weekly_posting_package.json`, `top5_weekly_posting_package.md`
- Reviewed generated output:
  - Result: consolidated draft in the new `2026-03-31` folder now shows `Update at`, `Today`, `Weekly so far`, `Full details to follow.`, and `#StrategyWarehouse #FuturesTrading #AlgoTrading`
- User review pending
  - Requested check: confirm the new consolidated post format and hashtag set are acceptable for regular posting.

## Risks/Notes
- Rank movement requires a prior generated package with comparable weekly-rank metadata; when unavailable, movement is intentionally omitted rather than guessed.
- The current generated package still reports `target_date = 2026-03-30` inside the content because that is what the available stats files contain, but the output folder is now correctly dated to the actual update run on `2026-03-31`.
- The consolidated draft now follows the requested structure, but final acceptance still depends on your review of the exact copy style.

## Completion Status
Awaiting user verification as of 2026-03-31 14:30:11 +01:00.


# User Feedback
User Verified: PASS
