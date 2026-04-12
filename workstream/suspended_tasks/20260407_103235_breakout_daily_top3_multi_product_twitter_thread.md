Source: User request on 2026-04-07 to create a daily version of the weekly multi-product top 5 Twitter thread, posting top 3 strategies per product type for the current date.
Task Type: standard
Task Attributes:
- recurring_task: true
- recurrence_type: scheduled
- recurrence_rule: interval
- recurrence_interval_hours: 24
- priority: high
- execution_owner: codex
- workflow_ready: false
**Suggested Agent:** codex
Task Summary: Generate and post a daily multi-product top-3 Twitter/X thread covering forex, indices, metals, and energy for the current date, using the same compact posting format as the weekly top-5 thread.
Context:
- Workspace: `C:\Users\edebe\eds`
- Weekly reference task: `C:\Users\edebe\eds\workstream\100_backlog\general\20260406_071500_breakout_workflow_twitter_top5_multi_product_types_every_6_hours.md`
- Weekly posting package reference: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\YYYY-MM-DD\top5_weekly_posting_package.md`
- Source data locations:
  - Forex: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\YYYY-MM-DD\_top20.json`
  - Indices: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\indices\YYYY-MM-DD\_top20.json`
  - Metals: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\YYYY-MM-DD\_top20.json`
  - Energy: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\energy\YYYY-MM-DD\_top20.json`
- Posting path: `Twitter/X`
Destination Folder: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-07\`
Dependency: None

## Objective

Produce and publish a daily multi-product top-3 Twitter/X thread for the current date, using the same compact one-line format established by the weekly top-5 thread.

## Output Format

### Thread Structure (5 posts)

#### Post 1 (Header)
```text
The Strategy Warehouse daily multi-product top 3 | Update at 2026-04-07 10:35 | Single-contract basis. Product detail posts follow. #StrategyWarehouse #FuturesTrading #AlgoTrading
```

#### Post 2 (Forex)
```text
Forex | 2026-04-07 | 1. GBPEUR_C brk R 2 tp20 sl10 360 | 2. EURAUD_C brk R 2 tp20 sl10 360 | 3. GBPEUR_C brk R 2 tp20 sl20 360 | Single-contract basis. #Forex #SystemTrading
```

#### Post 3 (Indices)
```text
Indices | 2026-04-07 | 1. NQ brk 2 tp30 sl5 2070 | 2. NQ brk 2 tp30 sl10 1920 | 3. NQ brk 2 tp30 sl20 1620 | Single-contract basis. #Indices #SystemTrading
```

#### Post 4 (Metals)
```text
Metals | 2026-04-07 | 1. SI brk 2 tp30 sl5 5300 | 2. SI brk R 3 tp30 sl5 2015 | 3. SI brk R 4 tp30 sl5 1695 | Single-contract basis. #Metals #SystemTrading
```

#### Post 5 (Energy)
```text
Energy | 2026-04-07 | 1. CL brk R 2 tp30 sl5 1600 | 2. CL brk R 2 tp30 sl10 1550 | 3. CL brk R 2 tp30 sl20 1450 | Single-contract basis. #Energy #SystemTrading
```

### Output Artifacts
- `top3_daily_posting_package.json` - structured data for automation
- `top3_daily_posting_package.md` - human-readable package with thread drafts
- `run_daily_top3_post.bat` - batch file to post the thread via API

## Plan
- [x] 1. Read daily source data for each product type from `_top20.json` for the current date.
  - [x] Test: All four product type source files exist and contain valid JSON with ranked strategies.
  - Evidence: Source files read successfully for forex, indices, metals, energy (2026-04-07)
- [x] 2. Extract top 3 strategies per product type, capturing product, strategy name, and net return.
  - [x] Test: Exactly 3 entries extracted per product type with valid net values.
  - Evidence: Forex (GBPEUR_C 360, EURAUD_C 360, GBPEUR_C 360), Indices (NQ 2070, 1920, 1620), Metals (SI 5300, 2015, 1695), Energy (CL 1600, 1550, 1450)
- [x] 3. Generate the daily posting package in both JSON and Markdown formats.
  - [x] Test: `top3_daily_posting_package.json` and `top3_daily_posting_package.md` exist in the destination folder.
  - Evidence: Files created at `TradeApps/breakout/fs/json/live/social_posting_package/2026-04-07/`
- [x] 4. Prepare the 5-post Twitter thread using the compact one-line format.
  - [x] Test: Each post is within X character limits and follows the established format.
  - Evidence: All 5 posts prepared in JSON and MD files, following weekly format
- [ ] 5. Post the thread to Twitter/X.
  - [ ] Test: POST returns success with tweet IDs or a concrete blocker.
  - Evidence: BLOCKED - API server at localhost:5000 not running. Run `run_daily_top3_post.bat` from Windows to post.
- [ ] 6. Record the live outcome with tweet IDs or failure reason.
  - [ ] Test: Evidence section updated with captured tweet IDs or exact error.
  - Evidence: Pending - requires posting step to complete

## Evidence
Objective-Delivery-Coverage: 80%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-07\top3_daily_posting_package.json`
  - Objective-Proved: Proves the daily package was generated with source-derived data.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-07\top3_daily_posting_package.md`
  - Objective-Proved: Proves the thread drafts were prepared in the validated format.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\run_daily_top3_post.bat`
  - Objective-Proved: Proves a reusable posting script was created for this workflow.
  - Status: captured
- Evidence-Type: live_post_result
  - Artifact: Tweet IDs from POST response
  - Objective-Proved: Proves the daily thread was successfully published to X.
  - Status: planned

## Implementation Log
- 2026-04-07 10:32:35 Europe/London: Task created to deliver daily top-3 multi-product Twitter thread.
- 2026-04-07 10:35:00 Europe/London: Read source data from all four product type _top20.json files.
- 2026-04-07 10:35:30 Europe/London: Extracted top 3 strategies per product type.
- 2026-04-07 10:36:00 Europe/London: Generated `top3_daily_posting_package.json` and `.md` in destination folder.
- 2026-04-07 10:38:00 Europe/London: Created `run_daily_top3_post.bat` to automate posting via API.
- 2026-04-07 10:40:00 Europe/London: Attempted to start API server from WSL but blocked due to Flask module not installed in Windows Python. Posting requires running from Windows CMD.

## Changes Made
- Created `TradeApps/breakout/fs/json/live/social_posting_package/2026-04-07/top3_daily_posting_package.json`
- Created `TradeApps/breakout/fs/json/live/social_posting_package/2026-04-07/top3_daily_posting_package.md`
- Created `TradeApps/breakout/fs/run_daily_top3_post.bat` for automated posting

## Validation Rules
- Do not fabricate strategy names, net returns, or tweet IDs.
- Use only source data from `_top20.json` for the current date.
- If source data is missing or stale, record the exact blocker.
- If X posting fails, record the exact error response.
- Each post must follow the compact one-line format established by the weekly thread.

## Risks/Notes
- Daily data may have fewer trades than weekly aggregates; top 3 should still be meaningful.
- If a product type has fewer than 3 strategies for the day, include only available entries and note the gap.
- Character limits for X posts should be validated before posting.
- This task supersedes the TODO task `20260403_200418_breakout_daily_top5_multi_product_types_same_thread_format.md` with a top-3 scope.
- **BLOCKER**: API server (localhost:5000) must be started from Windows before posting. Run `run_daily_top3_post.bat` from Windows CMD to complete the posting step.

## Completion Status
- State: BLOCKED - Awaiting API server start from Windows
- Timestamp: 2026-04-07 10:40:00
