2026-04-03T00:00:07.705694Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_request\", error_description=\"No access token was provided in this request\", resource_metadata=\"https://mcp.supabase.com/.well-known/oauth-protected-resource/mcp\"" })
OpenAI Codex v0.117.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019d50a3-d386-7a52-b4d9-327f3c3782d7
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Then read and follow any additional skill files explicitly referenced by the task. Task file: C:\Users\edebe\eds\workstream\200_inprogress\codex\20260403_010000_breakout_twitter_summary_returns_every_4_hours.md. Implement required changes in the workspace, run validations, and update checklist items.
2026-04-03T00:00:07.901367Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer resource_metadata=https://mcp.stripe.com/.well-known/oauth-protected-resource" })
2026-04-03T00:00:07.934511Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"No authorization provided\", resource_metadata=\"https://mcp.vercel.com/.well-known/oauth-protected-resource\"" })
codex
I’m loading the required lifecycle skill and the task file first, then I’ll trace any explicitly referenced skills before making changes.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260403_010000_breakout_twitter_summary_returns_every_4_hours.md'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'Get-ChildItem -Name' in C:\Users\edebe\eds
 succeeded in 2303ms:
Source: User request on 2026-04-02 to replace the existing every-4-hours Twitter summary recurrence with a combined workflow that prepares the latest payload and posts it through the X API route.



Task Type: standard



Task Attributes:

- recurring_task: true

- recurrence_type: scheduled

- recurrence_rule: interval

- recurrence_interval_hours: 4

- priority: high

- execution_owner: codex



**Suggested Agent:** codex



Task Summary: Every 4 hours, regenerate the latest Strategy Warehouse summary payload into `temp_tweet.txt`, then submit that prepared text through `POST /api/social/x_api_post`, recording the exact live response.



Context:

- Workspace: `C:\Users\edebe\eds`

- Payload generator: `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`

- Prepared payload file: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`

- X API route: `http://localhost:5000/api/social/x_api_post`

- Summary returns inputs: latest Strategy Warehouse social posting package and related return summary artefacts under `TradeApps\breakout\fs\json\live\social_posting_package`

- Workflow references:

  - `C:\Users\edebe\eds\workstream\300_complete\20260402_150114_breakout_rerun_twitter_summary_slot_20260402_130000.md`

  - `C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md`



Dependency: None

Required Skill: `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`
Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
Scheduled For: 2026-04-03 01:00:00+01:00

Next Scheduled For: 2026-04-03 05:00:00+01:00
Spawned From: 20260402_210000_breakout_twitter_summary_returns_every_4_hours.md



## Plan



- [ ] 1. Regenerate the latest summary returns payload for the current run window.

  - [ ] Test: `generate_posting_package.py --date YYYY-MM-DD` completes successfully and refreshes `temp_tweet.txt`.

  - Evidence:



- [ ] 2. Validate the prepared post body without inventing unsupported figures.

  - [ ] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.

  - Evidence:



- [ ] 3. Submit the prepared payload through the X API route.

  - [ ] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.

  - Evidence:



## Evidence



Objective-Delivery-Coverage: 0%

Auto-Acceptance: false

- Evidence-Type: file_output

  - Artifact: not_applicable

  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.

  - Status: planned

- Evidence-Type: route_output

  - Artifact: not_applicable

  - Objective-Proved: Proves the X API posting attempt outcome for this run.

  - Status: planned

- Evidence-Type: manual_verification

  - Artifact: not_applicable

  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.

  - Status: planned



## Implementation Log



- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.



## Changes Made



- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.



## Validation



- Pending execution.



## Risks/Notes



- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.

- Use local data only; do not invent returns or write new market figures without a source artifact.

- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.



## Completion Status



- State: TODO

- Timestamp:



 succeeded in 2190ms:
---
name: workstream-task-lifecycle
description: Create and maintain timestamped task documentation files in the workstream lifecycle folders (`workstream/000_epic`, `workstream/100_backlog`, `workstream/200_inprogress`, `workstream/300_complete`) and respect supporting queue states such as `blocker` lanes and `pending` subfolders inside active columns. Use when a user asks to document changes, track progress for a distinct task, or enforce file movement across backlog/in-progress/complete states.
---

# Workstream Task Lifecycle

Execute this workflow whenever a distinct task needs a documented trail.

## Folder Structure
```
workstream/
├── 000_epic/        ← High-level specs, PRDs, strategic documents
│                      Source material for task decomposition
│                      Items remain here permanently as reference
│
├── 100_backlog/     ← Atomic tasks decomposed from epics
│                      Ready to be picked up
│   ├── pending/     ← Parked backlog items temporarily removed from active processing
│                      Do not treat as active-ready work until explicitly restored
│   └── blocker/     ← Backlog-stage blocked or retry-parked items when the pipeline uses blocker lanes
│                      Treat as blocked state, not ready backlog
│
├── 200_inprogress/  ← Currently active work
│                      One task = one active worker
│   ├── pending/     ← Parked in-progress items moved out of the active lane
│   │                  Preserve lifecycle file and resume only when restored
│   └── blocker/     ← Execution failures or blocked retries parked by lane/agent
│                      Treat as blocked state, not as normal active execution
│
└── 300_complete/    ← Finished and verified tasks
                       Archived for reference
```

## Queue State Semantics

- `100_backlog` and `200_inprogress` are the active queue surfaces.
- `pending` subfolders inside those active states are parking areas, not normal ready queues.
- `100_backlog/blocker/<agent>` and `200_inprogress/blocker/<agent>` are blocked/retry parking areas.
- When a pipeline control feature parks work into `pending`, do not silently pull it back into active processing unless the controlling condition has been cleared.
- When documenting a task, keep the same lifecycle file; folder movement changes state, not identity.

## Required Naming
- **Backlog items**: `yyyymmdd_hhmmss_{Project}_{Descriptive_Title}.md`
  - **Important**: Once atomic tasks have been generated from a backlog item, its filename must be renamed to end with `_processed.md` (e.g. `..._Title_processed.md`) to prevent duplicate processing.
- **Task files**: `yyyymmdd_hhmmss_{project}_{unique_task}.md`
- Use lowercase with underscores for `{project}` and `{unique_task}`.
- Keep one file per distinct task.

## Folder Lifecycle
1. **Epic** (`000_epic`): High-level specs live here until ALL derived tasks are complete. Use `document-to-task-decomposition` skill to create tasks from epics. Upon successful task decomposition, the epic file MUST be renamed to end with `_processed.md`.
   - **Mandatory manifest rule**: Every decomposed epic MUST also produce a decomposition manifest at `ep_<output_slug>/decomposition_manifest.json` in the epic output folder that will later be used for reconciliation.
   - The manifest MUST record, at minimum: canonical epic slug, epic name, source epic path, decomposition timestamp, workstreams, and the original task list.
   - If an epic already has decomposed tasks but the manifest is missing, the manifest MUST be backfilled before the decomposition/reconciliation workflow can be considered complete.
   - If the output folder slug differs from the canonical epic slug, the manifest must still exist in the actual output folder being used by the deliverable (for example the existing `ep_*` folder the tasks point to).
2. **Backlog** (`100_backlog`): Create atomic task files here (decomposed from epics or new requests).
3. **Backlog Pending** (`100_backlog/pending`): If the pipeline intentionally deprioritizes or suspends a backlog task, move it under the matching `pending` path and treat it as parked, not ready.
4. **In Progress** (`200_inprogress`): Move file here when active work starts. For decomposed work, model lanes pull the next dependency-ready task from active `100_backlog`, not from `pending`.
5. **In Progress Pending** (`200_inprogress/pending`): If active work is temporarily moved out of the live lane, keep the same file under the corresponding pending path until it is restored.
6. **Blocked / Retry Parking** (`100_backlog/blocker/...` or `200_inprogress/blocker/...`): If the pipeline parks blocked or retry work into a blocker lane, treat this as blocked, not complete or ready.
7. Update the same file continuously while working.
8. **Complete** (`300_complete`): Move task file here when finished and verified.
9. **Epic Completion**: When ALL tasks derived from an epic are complete, update the epic with links to completed tasks, then move the epic to `300_complete`.
10. Start a new file for each new distinct task.

## Backlog Completion Rules
A backlog item can ONLY be moved to `300_complete` when:
1. ALL tasks derived from it exist in `300_complete`
2. The backlog document has been updated with a "Completed Tasks" section listing links to each completed task
3. Each completed task links back to the source backlog

### Backlog Completion Template
Add this section to the backlog before moving to complete:
```markdown
## Completed Tasks
| Task | Completed | File |
|------|-----------|------|
| Phase 0: Brand | 2026-02-25 | `300_complete/20260224_130100_breakout_phase0_brand_design_foundation.md` |
| Phase 1: Website | 2026-02-26 | `300_complete/20260224_130200_breakout_phase1_website_build.md` |
...

## Backlog Status
**COMPLETE** - All tasks finished and verified
**Completion Date**: 2026-02-28
```

## Required Content Template
- `Source`: Link to backlog item (if derived from backlog).
- `Task Type`: mandatory explicit task-type declaration.
  - Every qualifying task MUST include `Task Type: <value>`.
  - `Task Type` MUST always be written explicitly, even when the value is `standard`.
  - If execution behavior is driven by the richer `Task Attributes` model, `Task Type` still remains required as the human-readable top-level declaration.
  - Minimum allowed explicit value:
    - `standard`
- `Task Attributes`: execution-behavior fields that control how the task behaves in orchestration.
  - Design principle:
    - Task attributes are not labels.
    - They define execution behavior.
    - If a field does not change how the system behaves, it should not exist.
  - Standard/default behavior:
    - If none of the task-behavior booleans below are enabled, the task is treated as a `standard` task by default: an end-to-end task with a straightforward start and finish.
  - Attribute model:
    - `recurring_task: true|false`
    - `recurrence_type: scheduled | trigger_based | state_based`
    - `recurrence_rule: cron | interval | condition`
    - `looping_task: true|false`
    - `loop_until: condition_met | manual_stop | max_iterations`
    - `loop_interval: <optional>`
    - `splittable_task: true|false`
    - `split_output_type: list | files | records | tasks`
    - `split_outputs:`
    - `  - id: "<item_id>"`
    - `    payload: {}`
    - `split_routing:`
    - `  process: "<downstream_process_name>"`
    - `  mode: parallel | sequential`
    - `  target_board: "<optional>"`
    - `  target_stage: "<optional>"`
    - `split_spawn_task: true|false`
    - `spawn_template: "<task_template_name>"`
    - `split_failure_mode: independent | fail_fast | retry_failed_only`
    - `workflow_task: true|false`
    - `workflow_name: "<string>"`
    - `workflow_stage: backlog | todo | in_progress | review | complete | failed`
    - `depends_on: []`
    - `feeds_into: []`
  - A task may enable more than one attribute.
  - `recurring_task` means the task creates new executions over time from an external trigger.
  - `looping_task` means the task repeats inside the same execution cycle until a stop condition is met.
  - `splittable_task` means the task creates multiple outputs that become new independent work items or routed outputs.
  - `workflow_task` means the task participates in a named workflow with structured lifecycle movement and dependencies.
- `Task Summary`: scope and requested outcome.
- `Context`: source files/systems affected.
- `Dependency`: mandatory prerequisite declaration.
  - Every qualifying task MUST declare dependency explicitly.
  - If there is no prerequisite, the task MUST state `Dependency: None`.
  - If there is a prerequisite, record the required upstream task or artifact explicitly.
- `Plan`: checklist of implementation steps with one explicit completion test per step.
  - Format requirement:
    - `- [ ] N. <step description>`
    - `  - Test: <exact command/manual check and expected pass condition>`
    - `  - Evidence: <output snippet, file diff, screenshot path, or log reference proving test pass>`
  - The plan checklist must be present for every task file (new and updated), unless the task is explicitly marked as archival/no-op.
  - Sequential rule: each checklist item must be completed, its `Test` must be executed, and evidence must be recorded before proceeding to the next checklist item.
  - Completion marking rule: after a step test passes and evidence is captured, mark both the step checkbox and its test line as checked.
- `Evidence`: mandatory normalized evidence inventory for the task.
  - Every qualifying task MUST include an `Evidence` section, even if the only valid value is `not_applicable`.
  - Every qualifying task MUST also include `Objective-Delivery-Coverage: <0-100>%` directly under the `Evidence` heading.
  - Every qualifying task MUST also include `Auto-Acceptance: true|false` directly under the `Evidence` heading. Default is `true` when a task is created unless there is a reason to force manual review.
  - Interpretation:
    - `100%` means the recorded evidence is claimed to prove the task objective is fully delivered.
    - Any value below `100%` means the evidence is partial, conditional, or still requires reviewer judgement.
    - `Auto-Acceptance: true` means a task may be auto-accepted when the system sees `Objective-Delivery-Coverage: 100%`.
    - `Auto-Acceptance: false` means the task always requires manual acceptance, even if coverage is `100%`.
  - Each evidence item must use this format:
    - `- Evidence-Type: <type>`
    - `  - Artifact: <path, URL, command output, screenshot path, or "not_applicable">`
    - `  - Objective-Proved: <what this evidence proves>`
    - `  - Status: planned|captured|not_applicable`
  - Allowed `Evidence-Type` values:
    - `demo`
    - `url`
    - `screenshot`
    - `test_output`
    - `log_output`
    - `file_output`
    - `diff`
    - `manual_verification`
    - `user_feedback`
    - `not_applicable`
  - For user-visible tasks, include at least one evidence item that points to the actual deliverable access path (`demo`, `url`, `screenshot`, or `manual_verification`).
  - For implementation/refactor/bugfix tasks, include at least one technical proof item (`test_output`, `log_output`, `file_output`, or `diff`).
  - When the deliverable is an API, webpage, URL-driven flow, or executable that depends on multiple launch/verification steps, you may deliver a single `.bat` wrapper as the review package if it reliably launches, opens, or verifies the required components from one entry point.
  - When using a `.bat` wrapper, record the batch file path as an evidence artifact (`demo`, `file_output`, or `manual_verification` as appropriate) and also state exactly what it launches or verifies.
  - A `.bat` wrapper is packaging/verification convenience, not a substitute for the underlying deliverable proof. The evidence must still make clear what API, URL, webpage, or executable the wrapper exposes.
- `Implementation Log`: chronological actions taken.
- `Changes Made`: exact files, functions, schema, and behavior updates.
- `Validation`: commands run and results.
- `Risks/Notes`: known caveats, exclusions, and assumptions.
- `Completion Status`: final state and timestamp.

## Execution Rules
- The document content MUST be updated to match the current status of the task at all times.
- Every qualifying task MUST explicitly declare `Task Type`.
- `Task Type` is mandatory at task creation time and may not be omitted, even when the intended value is `standard`.
- Every qualifying task MUST declare the relevant task attributes that change execution behavior.
- If no execution-behavior attributes are required, the task is still treated as `standard`, but the task file MUST explicitly state `Task Type: standard`.
- A task MAY declare more than one execution-behavior attribute when multiple behaviors apply.
- If `splittable_task: true`, `split_outputs` AND `split_routing` MUST be defined.
- If `recurring_task: true`, `recurrence_rule` MUST be defined.
- If `looping_task: true`, `loop_until` MUST be defined.
- If `workflow_task: true`, `workflow_name` AND `workflow_stage` MUST be defined.
- If `recurring_task: true`, `recurrence_type` SHOULD also be recorded.
- If `splittable_task: true`, `split_output_type` SHOULD be recorded and `split_spawn_task`, `spawn_template`, and `split_failure_mode` SHOULD be recorded whenever used by the orchestration.
- If `workflow_task: true`, `depends_on` and `feeds_into` SHOULD be recorded whenever they are known.
- When work begins, mark relevant `Plan` checklist items as in progress/completed as evidence accumulates.
- If a task is parked under a `pending` subfolder, record why it was parked and what condition restores it.
- If a task is moved to a `blocker` lane, record the blocking condition, retry expectations, and any known recovery path.
- For any decomposed epic, verify that `ep_<output_slug>/decomposition_manifest.json` exists before treating reconciliation, delivery coverage, or epic progress reporting as authoritative.
- If the manifest is missing for an already-active epic, create a dedicated lifecycle task to backfill it from the canonical task set and record that backfill in the same task file.
- A task may be marked complete only when all required `Plan` checklist items are checked off, each step test is checked off, and pass evidence is present.
- A task may be marked complete only when its `Evidence` section contains the required evidence items and each required item is `captured` or explicitly `not_applicable`.
- A task may not claim full objective delivery unless `Objective-Delivery-Coverage` is present and set intentionally based on the captured evidence.
- Automatic acceptance is allowed only when `Objective-Delivery-Coverage` is `100%` and `Auto-Acceptance` is `true`.
- Execute plan steps strictly in order: do not start item `N+1` until item `N` is checked, its associated test is checked, and evidence of pass is documented (or explicitly approved exception).
- Every test must be explicitly checked off; un-checked tests are treated as not executed.
- Update the current in-progress file before responding with final completion.
- Record concrete paths and command outputs in summarized form.
- Do not create side docs; keep the full task narrative in the one lifecycle file.
- Preserve prior entries; append updates rather than rewriting history.
- If the task scope changes materially, close current file and create a new task file.

## Completion Verification Gate
- For any task that changes user-visible behavior (UI, UX flow, outputs, business logic the user can validate), do **not** mark `Completion Status` as complete until user verification is requested.
- Before final completion, explicitly ask the user to verify the change and provide pass/fail for each implemented behavior.
- Record this verification request in the task file `Validation` section.
- Record the user-verification artifact in the task file `Evidence` section using `Evidence-Type: user_feedback` or `Evidence-Type: manual_verification`.
- If user verification is still pending, set `Completion Status` to `Awaiting user verification`.
- Move to `300_complete` only after:
  1. implementation is done,
  2. technical validation is documented,
  3. required evidence items are captured,
  4. either:
     - user verification has been requested and outcome captured, or
     - auto-acceptance criteria have been met (`100%` coverage plus `Auto-Acceptance: true`).

## Evidence Rules
- Evidence exists to answer: "what artifact proves this task met its objective?"
- `Validation` remains the narrative of commands/checks performed; `Evidence` is the normalized proof inventory.
- Prefer artifact paths and concrete outputs over prose-only claims.
- If a task supports on-demand review, record the runnable/openable target as `Evidence-Type: demo` or `Evidence-Type: url`.
- If a single `.bat` file is the intended verification entry point for an API/webpage/executable package, record that `.bat` path explicitly and describe the components it wraps.
- Screenshots are supporting evidence, not a substitute for technical validation unless the task is purely visual and that limitation is documented.
- `Objective-Delivery-Coverage` is the normalized reviewer-facing summary of how completely the evidence proves the objective. It must be explicit for every qualifying task.
- `Auto-Acceptance` controls whether `100%` evidence can be promoted automatically or must remain manual-review only.

## Deliverable Packaging Rule

- For deliverables such as APIs, webpages, URLs, local apps, or executables, it is acceptable to provide a single review wrapper like `run_deliverable.bat` or `verify_deliverable.bat` when that is the cleanest way to package all required startup/open/check steps.
- The batch file should be deterministic and focused on reviewability: launch the app, open the page, hit the API, or run the verification checks needed to prove delivery.
- The lifecycle file should still name the real deliverable targets behind the wrapper, for example:
  - API base URL
  - local webpage URL
  - executable path
  - generated output path
- Prefer concise naming such as `open_demo.bat`, `run_api_demo.bat`, or `verify_delivery.bat` so reviewers understand the intent immediately.

## Example
- File name: `20260221_205458_breakout_full_json_archive_backfill.md`
- Flow:
1. Create in `workstream/100_backlog`.
2. If the pipeline suspends it temporarily, move it to `workstream/100_backlog/pending/...` and document the parking reason.
3. Move to `workstream/200_inprogress` while edits/tests run.
4. If the pipeline parks it as blocked or retry-pending, it may move to `workstream/100_backlog/blocker/...` or `workstream/200_inprogress/blocker/...`.
5. Move to `workstream/300_complete` after completion and validation.


 succeeded in 2464ms:
__pycache__
_tmp_chrome_profile
_tmp_chrome_profile2
.adal
.agent
.agents
.android
.augment
.claude
.codebuddy
.commandcode
.continue
.cortex
.crush
.edsLaptop
.factory
.firecrawl
.gemini
.goose
.iflow
.junie
.kilocode
.kiro
.kode
.mcpjam
.mux
.neovate
.openhands
.pi
.playwright-cli
.playwright-mcp
.pochi
.pytest_cache
.qoder
.qwen
.roo
.trae
.venv
.vibe
.vscode
.windsurf
.zencoder
100_backlog
a2ui
access_token
AI_trades_agents
AI_voice
algo
algo_crypto
algo_forex
algo_simulate
algo_viewer
algo_zone_viewer
api
api_server_pg
api_server_sql
api_server_sql_copy
APPS
backup
bizAfroExchange
bizETRM
bizPA
bizPhoneApp
builds
chats
Content
context7
data
data_migration
data_migration2
Database
DataInsights
db_analysis
db_scripts
env
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
epics
exports
firecrawl-mcp-server
forex_data_download
forex-data-viewer
Game_trader
Game_trader_backup_20251022_163839
Game_trader_ms
gbp_trading_app
GHRepo
groq
jar
job_scraper
json
live_market_data
logs
market_prices_api
market_prices_api_with_options
MCP
migrate
mobile_app_repo
myreact
n8n
New folder
node_modules
obs
OpenManus
plans
price_generator
price-differential-dashboard
prices
python_trading_dashboard
quant-trading-dashboard
rest_api
roo_code
saas
screenshots
sequential-thinking-mcp
skills
SL
SP
sql_scripts
sqlserver_to_postgre
sync_engine
synthetic-trading-platform
synthetic-trading-platform-roo
Test
testenv
tests
tools
trade_dashboard
trade_workflows
TradeApps
TradeApps - Copy
tradedb
TradeDbApp
Trades
trades_rt
trades_rt_test
trades_rt2
trades_rt3
trades_rt3_sim
TradingDashboard
TradingDashboard2
TradingDashboard3
tradingdashboard4
web_apps
workstream
workstream_backup_20260313
zone_counts_dashboard
_codex_dump_log.py
_codex_leader_check.py
_codex_tmp.py
_codex_tmp2.py
_codex_tmp3.py
_tmp_api_test.py
_tmp_file
_tmp_patch.diff
.augmentignore
.gitignore
advanced_forex_signal_generator.py
AGENTS.md
algo_viewer_20250726_0114.zip
algo_viewer_20250726_0154_refactor.zip
algo_viewer_20250727_2056.zip(current version)
algo_viewer_20250728_0024.zip
algo_viewer_20250728_1449.zip
algo_viewer_20250728_2141.zip
algo_viewer_20250729_0309_64_3_10.zip
algo_viewer_20250807_0356.zip
algo_viewer_20250824_0009.zip
algo_viewer_20251201_0107.zip
algo_viewer_20251201_1517.zip
algo_viewer_20251202_1632.zip
algo_viewer_20251202_2048.zip
algo_viewer_20251208_2228.zip
algo_viewer_64_2_10_20250826_1452.zip
algo_viewer_64_2_7_20250825_0359.zip
algo_zone_viewer.zip
alter_view_v2.sql
alter_view_v4.sql
analyse_extract_model_output_to_csv2.py
analyze_recent_performance.py
api_server_sql.zip
api_server.py
app.py
apply_breach_logic.sql
apply_core_views.sql
apply_final_triggers.sql
arc_count.txt
backfill_errors.log
basic-windows-setup.bat
batch_migrate_logic.py
bizpa_backend_5051.log
bizpa_backend_test.log
bizpa_backend.log
bizpa_data_cloud.sql
bizpa_frontend_boot.log
bizpa_full_migration.sql
bizpa_harden_test.log
bizpa_schema_cloud.sql
bizpa_vat_test_final.log
bizpa_vat_test.log
check_bytes.js
check_cols.txt
check_count_dna.sql
check_count_strategy_side.sql
check_dna_data.sql
check_dna_nulls.sql
check_dna_nulls2.sql
check_latest_pg_data.py
check_pf_temp_table.sql
check_product_forex_dna_nulls.sql
check_product_forex_dna.sql
check_product_forex_dna2.sql
check_product_forex_nulls.sql
check_sp9006.txt
check_strategy_side_current.sql
check_tables.py
cleanup_cache.py
cols.txt
combined_trade_algo_202560406.zip
combined_trades_closed_help.txt
combined_trades_open_help.txt
common_types.txt
compare_dbs.py
copy.bat
crash_log.txt
crash_log2.txt
crash2.txt
create_all_objects.sql
create_and_populate_strategy_side.sql
create_fn_decode_dna_array_fixed.sql
create_fn_decode_dna_array.sql
create_fn_decode_dna_json.sql
create_fn_split_csv_with_index.sql
create_strategy_side_current.sql
create_view_direct.sql
create_view.sql
create_vw_product_forex_dna_expanded.sql
crypto_quotes.txt
daksheen_redesign.html
dashboard.html
data_extraction.log
data_ingestion.log
Database_20250609_1432.zip
db_comparison_report.md
db_dependencies
db_scripts_20251001_0110.zip
db_scripts_20251007_2229.zip
db_scripts_20251104.zip
db_scripts_20251115_0239.zip
dbo.sp_001_buy_sell_count_entry.StoredProcedure.sql
dbo.sp_loop_create_trades_v2.StoredProcedure.sql
debug_bias_summary.py
debug_cat_bias.py
debug_closed_bias.py
debug_db_check.py
debug_fs_totals.py
debug_join.txt
debug_sp_loop.sql
debug_sum_trades.py
debug_summary_net.py
debug_summary.txt
debug_top300_bias.py
DESIGN.md
dna_100007_20260123.txt
dna_100007_data.txt
dna_100216_20260123.txt
dna_100216_data.txt
dna_pnl_stream_cache.txt
drop_800_tables.sql
drop_sp_loop.sql
eds.code-workspace
eds.lnk
error_log.txt
event_log.jsonl
execute_sp.sql
export_pending_trades.sql
final_col_check.txt
final_fx_check.txt
final_sp_output.txt
find_open_l_trades.py
fix_pg_errors.sql
fn_legs_src.sql
forex_signal_generator.py
forex-data-viewer.zip
funcuts_redesign.html
futures_quotes.txt
fx_quotes_check.txt
Game_trader_backup_20251022_163839.zip
GEMINI.md
get_procs.ps1
get_views.ps1
get-pip.py
grouped_test.txt
host_backend.log
hotfix_common.py
hotfix_summary_gen.py
identified_outputs.txt
implementation_plan.md
insert_strategy_side_data.sql
inspect_db.py
interactive_dashboard.html
interactive_profitability_dashboard.html
key.json
list_views.py
market_simulator.py
migrate_tables_to_pg.py
migrate_triggers_to_pg.py
migrate_views_to_pg.py
mismatches.txt
missing_objects_report.md
model_check.txt
move_trade_RT_files.py
move_trade_RT2_files.py
online_db_schema.sql
optimize_view_v5.sql
parity_check.txt
patch.diff
performance_rankings.txt
pg_arc_count.txt
pg_counts.txt
pg_data_check.txt
pg_final.txt
pg_triggers_list.txt
plumbers_se19_se20_without_websites.csv
postgres_inventory.txt
postgres_raw.txt
radical_step1_cache_table.sql
radical_step2_materializer_v2.sql
radical_step2_materializer.sql
radical_step3_lightweight_view_v2.sql
radical_step3_lightweight_view.sql
rebuild_core_tables.py
research_dashboard.html
rest_api_plan.md
run_all_apis.bat
run_final_diff.py
run_simulation.bat
run_sp_000.sql
run_sp_test.sql
run_sp_test2.sql
run_sp.sql
scrape_plumbers_v2.py
scrape_plumbers_v3.py
scrape_plumbers_v4.py
scrape_plumbers.py
scrape_salons.py
simulate_trades.py
skills-lock.json
social_media_trade_blocks_sample.md
sp_001_create_trades_pg.sql
sp_001_create_trades_v9_setbased_debug.sql
sp_001_create_trades_v9_setbased_final.sql
sp_001_create_trades_v9_setbased_final2.sql
sp_001_create_trades_v9_setbased_fixed.sql
sp_001_create_trades_v9_setbased_fixed2.sql
sp_001_create_trades_v9_setbased_fixed3.sql
sp_001_create_trades_v9_setbased_minimal.sql
sp_001_create_trades_v9_setbased_new.sql
sp_001_create_trades_v9_setbased_simplified.sql
sp_001_v2_pg.sql
sp_001_v2_src.sql
sp_001_v3_src.sql
sp_003_close_pg.sql
sp_003_src.sql
sp_9004_src.sql
sp_9006_help.txt
sp_check.txt
sp_def_full.sql
sp_def.txt
sp_load_quotes_src.sql
sp_output_after_snapshot.txt
sp_output_before_first_insert.txt
sp_output_first_log_print.txt
sp_output_rowcount_check.txt
sp_output_with_print_snapshot.txt
sp_refresh_dna_pnl_cache_clean.sql
sp_refresh_dna_pnl_cache.sql
sp_test_result_set_output.txt
sp003_utf8.sql
sp9004_utf8.sql
sql_server_inventory_v2.txt
sql_server_inventory_v3.txt
sql_server_inventory.txt
sql_server_raw.txt
sql_triggers.txt
ss_counts.txt
ss_data_check.txt
ss_final.txt
start_all_trading_apps.bat
start_breakout_db_services.bat
stop_all_trading_apps.bat
stub_missing_objects_pyodbc.py
stub_missing_objects.py
summary_gen_debug.log
sync_all_data_to_pg.py
sync_data_to_pg.py
sync_resume.py
sync_tradedb.py
tbl_105_trade_lifecycle_snapshots.txt
tbl_archive_dynamic_leadership.txt
tbl_top_one_archive.txt
temp_add_config.sql
temp_analysis_script.py
temp_backfill_strategy_names.sql
temp_check_latest_closed_tradeable_status_output.txt
temp_check_latest_closed_tradeable_status.sql
temp_close_test_trades_output_4.txt
temp_close_test_trades_output_5.txt
temp_edit.py
temp_fix_spacing2.py
temp_insert_test_trade_output_4.txt
temp_insert_test_trade_s_output_4.txt
temp_inspect_arrow.py
temp_inspect.py
temp_query.sql
temp_replace_functions.py
temp_report.py
temp_sp_test_result_set.sql
temp_sum_alt_net_by_direction.py
temp_sum_net_return_by_direction.py
temp_sum_net_return.py
temp_test_archive.py
temp_test_rt_metrics_output.txt
temp_test_rt_metrics.sql
temp_test_signals_cte.sql
temp_test_sp_bias8.sql
temp_test.py
temp_trade_test.sql
temp_trigger_update_output_2.txt
temp_update_script.py
test_cand_structure.sql
test_cand_table.sql
test_log.txt
test_path_resolution.py
test_write.txt
test.txt
tmp_backend_log.txt
tmp_inspect.py
tmp_old.txt
tmp_patch.ps1
tmp_patch.txt
tmp_segment_repr.txt
tmp_snippet.txt
tmp_summary.js
tmp_weighted_top.py
trade_executor.log
trade_monitor_sim.err
trade_monitor_sim.log
trade_monitor_stderr.txt
trade_monitor_stdout.txt
trade_monitor_test.err
trade_monitor_test.out
TradeApps - Copy.zip
TradeApps_20251220_0455.zip
TradeApps_20251222_0125.zip
TradeApps.zip
tradepanel.log
tradepanel.log.1
tradepanel.log.2
tradepanel.log.5
Trades_20251124_2335.zip
Trades_20251209_1615.zip
Trades_20251210.zip
trading_agent_model.zip
trading_dashboard.py
trading_forensics_20260323.mp4
trading_podcast_20260323.wav
trading_summary_20260323.mp4
training_reports.log
transpiler_sql_to_pg.py
trg_rt_src.sql
twitter_snapshot.md
tws_fetch_bid_ask5_refactored.py
tws_monitor_and_place_trade02.py
type_diffs.txt
update_sp_staging.sql
view_count.txt
vw_106_src.sql
vw_113_combined_trades_all_src.txt
vw_def.sql
vw_def.txt
vw_trades_all_def.sql
vwCombined_trades_closed_src.txt

codex
The task requires the `twitter-canonical-posting` skill as well. I’m reading that now and then I’ll inspect the current workflow scripts and prior completed run docs to execute the steps in order.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\20260402_150114_breakout_rerun_twitter_summary_slot_20260402_130000.md'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\skills\\twitter-canonical-posting\\SKILL.md'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tools\\social_posting_package\\generate_posting_package.py'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\run_twitter_canonical_workflow.py'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md'" in C:\Users\edebe\eds
 succeeded in 1831ms:
Source: User request on 2026-04-02 to rerun the recurring Twitter summary task originally scheduled for `2026-04-02 13:00:00+01:00` because prior task records for today are not trustworthy as proof of a live post.

Task Type: rerun
Project: breakout
- workflow_read: true

## Objective
- Rerun the `2026-04-02 13:00` Twitter summary posting slot using `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`.
- Refresh the social posting package, attempt the post via `run_twitter_post_v3.py`, and record whether the rerun genuinely posts or blocks.

## Plan
- [x] 1. Refresh the canonical posting data for `2026-04-02`.
  - [x] Test: `generate_posting_package.py --date 2026-04-02` completes and updates `temp_tweet.txt`.
  - Evidence: JSON and Markdown posting packages were regenerated for `2026-04-02`, and `temp_tweet.txt` now contains the `Update at 2026-04-02 09:29` tweet body.
- [x] 2. Execute the canonical Twitter posting workflow.
  - [x] Test: `run_twitter_post_v3.py` either posts successfully or returns a concrete session/runtime blocker.
  - Evidence: initial sandboxed run failed with `PermissionError: [WinError 5] Access is denied` when Playwright tried to create its subprocess; rerun outside sandbox completed with `[SUCCESS] Tweet successfully posted.`
- [x] 3. Verify outcome from local audit artefacts.
  - [x] Test: confirm whether `posted_tweets.log` gained a fresh entry for the rerun, or whether an error artefact/log explains the failure.
  - Evidence: `posted_tweets.log` gained a new entry at `2026-04-02T15:03:36.707044 | Update at 2026-04-02 09:29`

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
  - Objective-Proved: Proves which generated tweet/content was used for the rerun.
  - Status: complete
- Evidence-Type: log_output
  - Artifact: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v3.py` output showing `[SUCCESS] Tweet successfully posted.`
  - Objective-Proved: Proves whether the rerun actually posted or failed.
  - Status: complete
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\posted_tweets.log`
  - Objective-Proved: Allows confirmation from `posted_tweets.log` or error artefacts that the rerun outcome is genuine.
  - Status: complete

## Implementation Log
- 2026-04-02 15:01:14 Europe/London: Task created to rerun the `2026-04-02 13:00` Twitter summary slot using the canonical posting skill workflow.
- 2026-04-02 15:02 Europe/London: Regenerated the social posting package for `2026-04-02` and refreshed `temp_tweet.txt`.
- 2026-04-02 15:02 Europe/London: Initial sandboxed run of `run_twitter_post_v3.py` failed with Playwright subprocess `PermissionError: [WinError 5] Access is denied`.
- 2026-04-02 15:03 Europe/London: Reran `run_twitter_post_v3.py` outside the sandbox; the script reported `[SUCCESS] Tweet successfully posted.`
- 2026-04-02 15:03 Europe/London: Verified a fresh `posted_tweets.log` entry was appended for the rerun.

## Changes Made
- Regenerated the canonical tweet content for `2026-04-02`.
- Successfully reran the Twitter summary post for the slot originally scheduled at `2026-04-02 13:00:00+01:00`.

## Validation
- Content refresh
  - `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-02`
  - Result: package regenerated and `temp_tweet.txt` updated
- Posting attempt
  - Sandboxed run result: blocked by Playwright subprocess `PermissionError: [WinError 5] Access is denied`
  - Escalated run result: `[SUCCESS] Tweet successfully posted.`
- Audit proof
  - `posted_tweets.log` contains new entry:
  - `2026-04-02T15:03:36.707044 | Update at 2026-04-02 09:29`

## Risks/Notes
- If the Twitter session is invalid, follow the skill's blocker handling and record the failure clearly rather than assuming success.

## Completion Status
- State: COMPLETE
- Timestamp: 2026-04-02 15:04:20 Europe/London


 succeeded in 1814ms:
#!/usr/bin/env python3
"""
Generate a daily social posting package for The Strategy Warehouse.

Builds top-N weekly strategy summaries from the per-product weekly stats files and
writes both JSON and Markdown package outputs for operator review/posting.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
FS_ROOT = SCRIPT_DIR.parent.parent
JSON_ROOT = FS_ROOT / "json" / "live"
TEMP_TWEET_PATH = FS_ROOT / "temp_tweet.txt"
DEFAULT_PRODUCT_TYPES = ["forex", "indices", "metals", "energy"]
DEFAULT_BRAND = "The Strategy Warehouse"
CONSOLIDATED_HASHTAGS = ["#StrategyWarehouse", "#FuturesTrading", "#AlgoTrading"]


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def shorten_strategy_name(name: str) -> str:
    shortened = name.replace("breakout", "brk")
    shortened = re.sub(r"\.0+", "", shortened)
    shortened = shortened.replace("_", " ")
    return shortened[:40]


def clean_product_name(name: str) -> str:
    return re.sub(r"_[CS]$", "", name)


def format_net_points(net: float) -> str:
    if net >= 0:
        return f"+{int(round(net))}"
    return str(int(round(net)))


def format_post_points(net: float) -> str:
    return str(int(round(net)))


def format_date_range(date_range: List[str]) -> str:
    if not date_range or len(date_range) < 2:
        return "this week"
    start = datetime.fromisoformat(date_range[0]).strftime("%b %d")
    end = datetime.fromisoformat(date_range[1]).strftime("%b %d")
    return f"{start}-{end}"


def title_case_product_type(product_type: str) -> str:
    return product_type.replace("_", " ").title()


def weekly_stats_path(product_type: str) -> Path:
    return JSON_ROOT / product_type / "stats" / "daily_net_return.json"


def live_top20_path(product_type: str, date_str: str) -> Path:
    return JSON_ROOT / product_type / date_str / "_top20.json"


def latest_live_top20_path(product_type: str, max_date_str: str) -> Optional[Path]:
    product_root = JSON_ROOT / product_type
    if not product_root.exists():
        return None

    candidate_dirs = sorted(
        [
            item
            for item in product_root.iterdir()
            if item.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", item.name) and item.name <= max_date_str
        ],
        key=lambda path: path.name,
        reverse=True,
    )

    for folder in candidate_dirs:
        candidate = folder / "_top20.json"
        if not candidate.exists():
            continue
        try:
            payload = load_json(candidate)
        except Exception:
            continue
        if payload.get("top20"):
            return candidate
    return None


def load_weekly_stats(product_type: str) -> Dict[str, Any]:
    path = weekly_stats_path(product_type)
    if not path.exists():
        raise FileNotFoundError(f"Weekly stats not found: {path}")
    return load_json(path)


def load_live_top20(product_type: str, date_str: str) -> Dict[str, Any]:
    path = live_top20_path(product_type, date_str)
    if not path.exists():
        return {"last_update": None, "top20": []}
    return load_json(path)


def load_live_top20_with_fallback(product_type: str, date_str: str) -> Tuple[Dict[str, Any], str]:
    requested_path = live_top20_path(product_type, date_str)
    requested_payload = load_live_top20(product_type, date_str)
    if requested_payload.get("top20"):
        return requested_payload, date_str

    fallback_path = latest_live_top20_path(product_type, date_str)
    if fallback_path and fallback_path != requested_path:
        fallback_payload = load_json(fallback_path)
        if fallback_payload.get("top20"):
            return fallback_payload, fallback_path.parent.name

    return requested_payload, date_str


def iter_iso_dates(start_date: str, end_date: str) -> List[str]:
    start = datetime.fromisoformat(start_date).date()
    end = datetime.fromisoformat(end_date).date()
    dates: List[str] = []
    current = start
    while current <= end:
        dates.append(current.isoformat())
        current += timedelta(days=1)
    return dates


def parse_strategy_label(strategy_label: str) -> Tuple[str, str]:
    if "|" in strategy_label:
        product, strategy_name = [part.strip() for part in strategy_label.split("|", 1)]
    else:
        product, strategy_name = "Unknown", strategy_label.strip()
    return clean_product_name(product), strategy_name


def extract_top_strategies(weekly_stats: Dict[str, Any], top_n: int) -> List[Dict[str, Any]]:
    items = []
    for rank, item in enumerate(weekly_stats.get("top_strategies", [])[:top_n], start=1):
        strategy_label = item.get("strategy", "")
        product, strategy_name = parse_strategy_label(strategy_label)
        items.append(
            {
                "rank": rank,
                "product": product,
                "strategy": shorten_strategy_name(strategy_name),
                "total_net": round(float(item.get("total_net", 0)), 2),
                "total_trades": int(item.get("total_trades", 0)),
            }
        )
    return items


def build_twitter_post(product_type: str, weekly_stats: Dict[str, Any], top_strategies: List[Dict[str, Any]], brand: str) -> str:
    date_label = format_date_range(weekly_stats.get("date_range", []))
    heading = f"{brand} {title_case_product_type(product_type)} top {len(top_strategies)} for {date_label}:"
    lines = [
        f"{item['rank']}. {item['product']} {item['strategy']} {format_net_points(item['total_net'])}"
        for item in top_strategies
    ]
    hashtags = f"#{title_case_product_type(product_type).replace(' ', '')} #AlgoTrading #StrategyWarehouse"
    text = f"{heading}\n" + "\n".join(lines) + f"\n{hashtags}"

    if len(text) <= 280:
        return text

    compact_lines = [
        f"{item['rank']}.{item['product']} {format_net_points(item['total_net'])}"
        for item in top_strategies
    ]
    text = f"{heading} " + " | ".join(compact_lines) + f" {hashtags}"
    if len(text) <= 280:
        return text

    text = (
        f"{title_case_product_type(product_type)} top {len(top_strategies)} {date_label}: "
        + " | ".join(compact_lines)
        + f" {hashtags}"
    )
    if len(text) > 280:
        text = text[:277] + "..."
    return text


def extract_dna_leaders(date_str: str, top_n: int = 1) -> List[Dict[str, Any]]:
    dna_path = JSON_ROOT / "forex" / date_str / "_dna_frequency.json"
    if not dna_path.exists():
        return []
    
    try:
        data = load_json(dna_path)
        leaders = data.get("leaders", [])
        return [
            {
                "product": item.get("product", "DNA"),
                "net": round(float(item.get("final_net", 0)), 2),
                "strategy": shorten_strategy_name(item.get("strategy", "")),
                "product_type": "dna"
            }
            for item in leaders[:top_n]
        ]
    except Exception:
        return []


def extract_dna_leaders_with_fallback(date_str: str, top_n: int = 1) -> Tuple[List[Dict[str, Any]], str]:
    leaders = extract_dna_leaders(date_str, top_n=top_n)
    if leaders:
        return leaders, date_str

    fallback_path = latest_live_top20_path("forex", date_str)
    if fallback_path:
        fallback_date = fallback_path.parent.name
        fallback_leaders = extract_dna_leaders(fallback_date, top_n=top_n)
        if fallback_leaders:
            return fallback_leaders, fallback_date

    return [], date_str


def extract_today_product_leaders_from_live_top20(
    live_top20_by_product_type: Dict[str, Dict[str, Any]],
    top_n: int = 5,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    product_best: Dict[str, Dict[str, Any]] = {}
    last_update: Optional[str] = None

    for product_type, top20_payload in live_top20_by_product_type.items():
        payload_update = top20_payload.get("last_update")
        if payload_update and (last_update is None or str(payload_update) > str(last_update)):
            last_update = str(payload_update)

        for item in top20_payload.get("top20", []):
            product = clean_product_name(str(item.get("product", "")).strip())
            if not product:
                continue
            value = float(item.get("total_net", 0) or 0)
            existing = product_best.get(product)
            if existing is None or value > existing["net"]:
                product_best[product] = {
                    "product": product,
                    "net": round(value, 2),
                    "product_type": product_type,
                    "strategy": shorten_strategy_name(str(item.get("strategy", ""))),
                }

    leaders = sorted(product_best.values(), key=lambda x: x["net"], reverse=True)
    return (
        [
            {
                "rank": rank,
                "product": item["product"],
                "net": item["net"],
                "product_type": item["product_type"],
                "strategy": item["strategy"],
            }
            for rank, item in enumerate(leaders[:top_n], start=1)
        ],
        last_update,
    )


def extract_weekly_product_leaders_from_weekly_stats(
    product_types: List[str],
    week_start_date: str,
    live_date: str,
    top_n: int = 5,
) -> List[Dict[str, Any]]:
    # [2026-04-01 23:35] V20260401_2330 - Corrected to aggregate by strategy cumulative total
    # instead of daily best summation.
    strategy_wtd: Dict[Tuple[str, str], Dict[str, Any]] = {}

    for date_str in iter_iso_dates(week_start_date, live_date):
        for product_type in product_types:
            live_top20 = load_live_top20(product_type, date_str)
            for item in live_top20.get("top20", []):
                product = clean_product_name(str(item.get("product", "")).strip())
                strategy_name = str(item.get("strategy", "")).strip()
                if not product or not strategy_name:
                    continue
                
                value = float(item.get("total_net", 0) or 0)
                key = (product, strategy_name)
                
                if key not in strategy_wtd:
                    strategy_wtd[key] = {
                        "product": product,
                        "strategy": strategy_name,
                        "net": 0.0,
                        "product_type": product_type
                    }
                strategy_wtd[key]["net"] += value

    # For each product, find the single best strategy performance for the week
    product_best: Dict[str, Dict[str, Any]] = {}
    for entry in strategy_wtd.values():
        product = entry["product"]
        existing = product_best.get(product)
        if existing is None or entry["net"] > existing["net"]:
            product_best[product] = entry

    leaders = sorted(product_best.values(), key=lambda x: x["net"], reverse=True)
    return [
        {
            "rank": rank,
            "product": item["product"],
            "net": round(float(item["net"]), 2),
            "product_type": item["product_type"],
        }
        for rank, item in enumerate(leaders[:top_n], start=1)
    ]


def previous_package_path(current_target_date: Optional[str]) -> Optional[Path]:
    package_root = JSON_ROOT / "social_posting_package"
    if not package_root.exists():
        return None

    candidate_dirs = sorted([item for item in package_root.iterdir() if item.is_dir()], key=lambda p: p.name, reverse=True)
    for folder in candidate_dirs:
        if current_target_date and folder.name >= current_target_date:
            continue
        candidate = folder / "top5_weekly_posting_package.json"
        if candidate.exists():
            return candidate
    return None


def load_previous_weekly_ranks(current_target_date: Optional[str]) -> Dict[str, int]:
    previous_path = previous_package_path(current_target_date)
    if not previous_path:
        return {}

    previous_package = load_json(previous_path)
    weekly_leaders = previous_package.get("weekly_product_leaders", [])
    return {
        item.get("product"): int(item.get("rank"))
        for item in weekly_leaders
        if item.get("product") and item.get("rank")
    }


def apply_rank_movement(leaders: List[Dict[str, Any]], previous_ranks: Dict[str, int]) -> List[Dict[str, Any]]:
    enriched = []
    for item in leaders:
        updated = dict(item)
        previous_rank = previous_ranks.get(item["product"])
        if previous_rank:
            delta = previous_rank - item["rank"]
            if delta > 0:
                updated["movement"] = f"up {delta}"
            elif delta < 0:
                updated["movement"] = f"down {abs(delta)}"
            else:
                updated["movement"] = "flat"
        else:
            updated["movement"] = None
        enriched.append(updated)
    return enriched


def build_consolidated_twitter_post(
    update_timestamp: Optional[str],
    today_source_date: Optional[str],
    generated_at: Optional[str],
    today_leaders: List[Dict[str, Any]],
    weekly_leaders: List[Dict[str, Any]],
) -> str:
    if update_timestamp:
        update_label = datetime.fromisoformat(update_timestamp).strftime("%Y-%m-%d %H:%M")
        lines = [f"Update at {update_label}", ""]
    else:
        lines = ["Update time unavailable", ""]

    today_heading = "Today"
    weekly_heading = "Weekly so far"
    if today_source_date and generated_at:
        generated_date = datetime.fromisoformat(generated_at).strftime("%Y-%m-%d")
        if today_source_date != generated_date:
            today_heading = f"{today_source_date} results"
            weekly_heading = f"Week to {today_source_date}"

    lines.append(today_heading)

    for item in today_leaders:
        lines.append(f"{item['rank']}. {item['product']} {format_post_points(item['net'])}")

    lines.extend(["", weekly_heading])
    for item in weekly_leaders:
        movement = item.get("movement")
        movement_suffix = f" {movement}" if movement and movement != "flat" else ""
        lines.append(f"{item['rank']}. {item['product']} {format_post_points(item['net'])}{movement_suffix}")

    lines.extend(
        [
            "",
            "Full details to follow.",
            " ".join(CONSOLIDATED_HASHTAGS),
        ]
    )
    return "\n".join(lines)


def build_package(product_types: List[str], top_n: int, brand: str, live_date: Optional[str] = None, generated_at: Optional[str] = None) -> Dict[str, Any]:
    packages = []
    if not generated_at:
        generated_at = datetime.now().isoformat()
    if not live_date:
        live_date = datetime.fromisoformat(generated_at).strftime("%Y-%m-%d")
    
    target_date: Optional[str] = None
    weekly_stats_by_product_type: Dict[str, Dict[str, Any]] = {}
    live_top20_by_product_type: Dict[str, Dict[str, Any]] = {}
    today_source_dates: List[str] = []

    for product_type in product_types:
        weekly_stats = load_weekly_stats(product_type)
        live_top20, resolved_live_date = load_live_top20_with_fallback(product_type, live_date)
        weekly_stats_by_product_type[product_type] = weekly_stats
        live_top20_by_product_type[product_type] = live_top20
        today_source_dates.append(resolved_live_date)
        top_strategies = extract_top_strategies(weekly_stats, top_n)
        twitter_post = build_twitter_post(product_type, weekly_stats, top_strategies, brand)
        packages.append(
            {
                "product_type": product_type,
                "target_date": weekly_stats.get("target_date"),
                "today_source_date": resolved_live_date,
                "date_range": weekly_stats.get("date_range", []),
                "source_file": str(weekly_stats_path(product_type)),
                "today_source_file": str(live_top20_path(product_type, resolved_live_date)),
                "top_strategies": top_strategies,
                "twitter_post": {
                    "text": twitter_post,
                    "char_count": len(twitter_post),
                },
            }
        )
        target_date = target_date or weekly_stats.get("target_date")

    today_leaders, today_last_update = extract_today_product_leaders_from_live_top20(
        live_top20_by_product_type,
        top_n=top_n,
    )
    
    # [2026-04-02 01:15] V20260402_0115 - Include DNA in today product leaders
    dna_top, dna_source_date = extract_dna_leaders_with_fallback(live_date, top_n=top_n)
    today_source_dates.extend([dna_source_date] if dna_top else [])
    all_today = today_leaders + [
        {
            "rank": 0,
            "product": d["product"],
            "net": d["net"],
            "product_type": "dna",
            "strategy": d["strategy"]
        }
        for d in dna_top
    ]
    all_today.sort(key=lambda x: x["net"], reverse=True)
    today_leaders = []
    for i, item in enumerate(all_today[:top_n], start=1):
        item["rank"] = i
        today_leaders.append(item)

    week_start_date = None
    for weekly_stats in weekly_stats_by_product_type.values():
        date_range = weekly_stats.get("date_range", [])
        if date_range:
            week_start_date = date_range[0]
            break
    if not week_start_date:
        week_start_date = live_date

    previous_ranks = load_previous_weekly_ranks(target_date)
    weekly_leaders = apply_rank_movement(
        extract_weekly_product_leaders_from_weekly_stats(product_types, week_start_date, live_date, top_n=top_n),
        previous_ranks,
    )
    resolved_today_source_date = max(today_source_dates) if today_source_dates else live_date
    consolidated_post = build_consolidated_twitter_post(
        today_last_update,
        resolved_today_source_date,
        generated_at,
        today_leaders,
        weekly_leaders,
    )

    return {
        "brand": brand,
        "generated_at": generated_at,
        "generated_date": live_date,
        "today_source_date": resolved_today_source_date,
        "today_source_last_update": today_last_update,
        "target_date": target_date,
        "top_n": top_n,
        "product_types": product_types,
        "packages": packages,
        "today_product_leaders": today_leaders,
        "weekly_product_leaders": weekly_leaders,
        "consolidated_twitter_post": consolidated_post,
        "consolidated_hashtags": CONSOLIDATED_HASHTAGS,
    }


def render_markdown(package: Dict[str, Any]) -> str:
    lines = [
        f"# {package['brand']} Daily Posting Package",
        "",
        f"- Generated: `{package['generated_at']}`",
        f"- Today source date: `{package.get('today_source_date')}`",
        f"- Today source last update: `{package.get('today_source_last_update')}`",
        f"- Target date: `{package['target_date']}`",
        f"- Product types: `{', '.join(package['product_types'])}`",
        f"- Top N: `{package['top_n']}`",
        "",
        "## Consolidated Leaderboard",
        "",
        "### Twitter Draft (Today + Weekly So Far)",
        "",
        "```text",
        package["consolidated_twitter_post"],
        "```",
        "",
        "### Consolidated Data",
        "",
        "| Section | Rank | Product | Net | Movement |",
        "| --- | --- | --- | --- | --- |",
    ]

    for item in package.get("today_product_leaders", []):
        lines.append(f"| Today | {item['rank']} | {item['product']} | {format_post_points(item['net'])} |  |")

    for item in package.get("weekly_product_leaders", []):
        lines.append(
            f"| Weekly so far | {item['rank']} | {item['product']} | {format_post_points(item['net'])} | {item.get('movement') or ''} |"
        )

    lines.extend(
        [
            "",
        "## Workflow",
        "1. Run the generator.",
        "2. Review the consolidated `Today` and `Weekly so far` draft first.",
        "3. Review the JSON and Markdown outputs for each product type.",
        "4. Review each Twitter post text before posting.",
        "5. Post the consolidated update first, then the product-type detail results in sequence.",
        "",
        ]
    )

    for entry in package["packages"]:
        lines.extend(
            [
                f"## {title_case_product_type(entry['product_type'])}",
                "",
                f"- Source: `{entry['source_file']}`",
                f"- Today source: `{entry['today_source_file']}`",
                f"- Week: `{format_date_range(entry['date_range'])}`",
                "",
                "| Rank | Product | Strategy | Net | Trades |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in entry["top_strategies"]:
            lines.append(
                f"| {item['rank']} | {item['product']} | {item['strategy']} | {format_net_points(item['total_net'])} | {item['total_trades']} |"
            )
        lines.extend(
            [
                "",
                "### Twitter Draft",
                "",
                "```text",
                entry["twitter_post"]["text"],
                "```",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def ensure_output_dir(target_date: str) -> Path:
    output_dir = JSON_ROOT / "social_posting_package" / target_date
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a daily social posting package.")
    parser.add_argument(
        "--product-types",
        nargs="+",
        default=DEFAULT_PRODUCT_TYPES,
        help="Product types to include in the package.",
    )
    parser.add_argument("--top-n", type=int, default=5, help="Number of strategies per product type.")
    parser.add_argument("--brand", default=DEFAULT_BRAND, help="Brand/source label for the package.")
    parser.add_argument("--output-dir", type=str, help="Optional explicit output directory.")
    parser.add_argument("--date", type=str, help="Optional target date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--stdout", action="store_true", help="Print JSON package to stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    
    # Use specified date or default to today
    if args.date:
        live_date = args.date
    else:
        live_date = datetime.now().strftime("%Y-%m-%d")
    generated_at = datetime.now().isoformat()

    package = build_package(args.product_types, args.top_n, args.brand, live_date=live_date, generated_at=generated_at)
    output_dir = Path(args.output_dir) if args.output_dir else ensure_output_dir(live_date)

    json_path = output_dir / "top5_weekly_posting_package.json"
    md_path = output_dir / "top5_weekly_posting_package.md"

    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(package, handle, indent=2, ensure_ascii=False)

    markdown = render_markdown(package)
    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write(markdown)

    TEMP_TWEET_PATH.write_text(package["consolidated_twitter_post"].strip() + "\n", encoding="utf-8")

    if args.stdout:
        print(json.dumps(package, indent=2, ensure_ascii=False))
    else:
        print(f"[INFO] JSON package written to {json_path}")
        print(f"[INFO] Markdown package written to {md_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


 succeeded in 2792ms:
# Twitter Canonical Posting & Automated Login Skill

This skill captures the high-reliability workflow for logging into Twitter/X using local credentials and publishing canonical strategy performance updates. It is designed to bypass common UI blockers and session corruption issues.

## 1. System Components
- **Credentials:** `C:\Users\edebe\eds\key.json` (JSON format with "username" and "password")
- **Login Automation:** `TradeApps/breakout/fs/auto_twitter_login.py`
- **Posting Automation:** `TradeApps/breakout/fs/run_twitter_post_v3.py`
- **Session Data:** `TradeApps/breakout/fs/twitter_session/`
- **Canonical Data Source:** `TradeApps/breakout/fs/temp_tweet.txt` (Updated by `generate_posting_package.py`)

## 2. Automated Login Workflow
If the session expires or "Something went wrong" appears on the login page:
1. **Kill existing Chrome instances:** `taskkill /F /IM chrome.exe`
2. **Execute Login Script:** `python auto_twitter_login.py`
3. **Behavior:** 
   - Automatically deletes the old `twitter_session` folder.
   - Opens a **visible** browser window.
   - Enters credentials from `key.json`.
   - **Manual Intervention:** If a CAPTCHA or Phone/Email verification appears, the script waits 60 seconds for the user to complete it in the visible window.

## 3. Background Posting Workflow
Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.

## 4. Troubleshooting
- **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
- **404/Login Redirect:** If the post script fails with a login redirect, the session has expired. Re-run `auto_twitter_login.py`.
- **Post Button Blocked:** If the script fails to click the Post button, ensure `run_twitter_post_v3.py` is being used, as it implements the `Control+Enter` shortcut fallback.

## 5. Verification
- **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.


 succeeded in 2848ms:
from pathlib import Path
import datetime
import json
import subprocess
import sys

from twitter_browser import TwitterBrowser

ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
TEMP_TWEET = ROOT / "temp_tweet.txt"
POSTED_LOG = ROOT / "posted_tweets.log"
WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"


def _write_status(status: dict) -> None:
    WORKFLOW_STATUS.write_text(json.dumps(status, indent=2), encoding="utf-8")


def _new_status(run_date: str) -> dict:
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "run_date": run_date,
        "steps": {
            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
            "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
        },
        "final_status": "failed",
    }


def _mark_step(status: dict, step: str, ok: bool, details: str) -> None:
    status["steps"][step]["ok"] = ok
    status["steps"][step]["details"] = details
    _write_status(status)


def _posted_log_tail() -> str:
    if not POSTED_LOG.exists():
        return ""
    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")


def _verify_login() -> tuple[bool, str]:
    with TwitterBrowser(headless=True) as tb:
        logged_in = tb.is_logged_in()
        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
        if not logged_in:
            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
        return True, f"Authenticated session verified. Current URL: {tb.page.url}"


def _run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=180000,
    )


def main() -> int:
    run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    status = _new_status(run_date)
    _write_status(status)

    logged_in, login_details = _verify_login()
    if not logged_in:
        _mark_step(status, "verify_login", False, login_details)
        return 1
    _mark_step(status, "verify_login", True, login_details)

    generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
    if generate_result.returncode != 0:
        _mark_step(
            status,
            "generate_content",
            False,
            f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
        )
        return 1
    if not TEMP_TWEET.exists():
        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
        return 1
    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
    if not tweet_text:
        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
        return 1
    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")

    before_log = _posted_log_tail()
    post_result = _run_command(["python", str(POST_SCRIPT)])
    if post_result.returncode != 0:
        _mark_step(
            status,
            "submit_post",
            False,
            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
        )
        return 1
    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")

    after_log = _posted_log_tail()
    if after_log == before_log:
        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
        return 1
    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")

    status["final_status"] = "success"
    _write_status(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


 succeeded in 2885ms:
## Objective

Rerun `POST /api/social/x_api_post` with the current prepared summary payload after refreshing `workstream/.env` so the live response shows whether the new X OAuth 1.0 credentials are now accepted.

## Context

- Active X credential source: `workstream/.env`
- Route owner: `TradeApps/breakout/fs/trade_viewer_api.py` with social routes added from `TradeApps/breakout/fs/social_publisher.py`
- Prior live blocker on 2026-04-02: `403 Forbidden` with X app OAuth1 permission error

## Task Attributes

- project: breakout
- task_type: verification
- area: social_publisher
- priority: high
- status: complete
- workflow_ready: true

## Plan

1. Confirm the live API server is reachable on the expected local port.
2. Load the current prepared summary payload from `temp_tweet.txt`.
3. Call `POST /api/social/x_api_post` and capture the exact response.
4. Record whether the refreshed token set changed the X API outcome.

## Progress Log

- 2026-04-02 18:49:57 Created lifecycle task.
- 2026-04-02 18:50:36 Validation: `GET http://localhost:5000/api/health` returned `{"status":"ok"}`.
- 2026-04-02 18:50:36 Loaded the current prepared post body from `TradeApps/breakout/fs/temp_tweet.txt`.
- 2026-04-02 18:51:03 Validation: `POST http://localhost:5000/api/social/x_api_post` returned HTTP `200` with `{"success": true, "message": "Tweet posted successfully", "tweet_id": "2039762743595569627"}`.

## Outcome

Completed. The rerun against the live local route succeeded after the workstream env credential refresh, confirming the current X OAuth 1.0 credential set is accepted for posting.


codex
The current workflow script still posts through the browser automation path. I’m checking the API route implementation and any scheduler hooks now, because the task objective requires replacing that last step with the live `x_api_post` route and capturing its exact response.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\trade_viewer_api.py'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\social_publisher.py'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"x_api_post|social_publisher|temp_tweet|run_twitter_canonical_workflow|twitter_workflow_status\" 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs'" in C:\Users\edebe\eds
 succeeded in 1702ms:
"""
PipHunter Social Media Publisher
Publishes market narratives to Twitter/X with teaser content linking to the website.

Credential lookup order:
1. Process environment
2. workstream/.env
3. access_token/key_X.json
4. config.json (legacy fallback)
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from narrative_generator import NarrativeGenerator

BASE_DIR = Path(__file__).parent
REPO_ROOT = BASE_DIR.resolve().parents[2]
CONFIG_FILE = BASE_DIR / "config.json"
POST_LOG_FILE = BASE_DIR / "social_posts.json"
WORKSTREAM_ENV_FILE = REPO_ROOT / "workstream" / ".env"
KEY_X_FILE = REPO_ROOT / "access_token" / "key_X.json"
WEBSITE_URL = "https://piphunter.io"  # Update when domain is live


def _console_safe_text(text: str) -> str:
    """Return text that can be printed on the active console encoding."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


def _load_simple_env_file(path: Path) -> Dict[str, str]:
    """Load a minimal KEY=VALUE .env file without external dependencies."""
    values: Dict[str, str] = {}
    if not path.exists():
        return values

    try:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                values[key] = value
    except Exception as exc:
        print(f"Error loading env file {path}: {exc}")

    return values


def _load_key_x_file(path: Path) -> Dict[str, str]:
    """Load X credentials from the dedicated key_X.json file."""
    if not path.exists():
        return {}

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Error loading X key file {path}: {exc}")
        return {}

    return {
        "TWITTER_API_KEY": str(raw.get("Consumer Key", "")).strip(),
        "TWITTER_API_SECRET": str(raw.get("Consumer Key Secret", "")).strip(),
        "TWITTER_ACCESS_TOKEN": str(raw.get("Access Token", "")).strip(),
        "TWITTER_ACCESS_SECRET": str(raw.get("Access Token Secret", "")).strip(),
        "TWITTER_BEARER_TOKEN": str(raw.get("bearerToken", "")).strip(),
    }


class SocialPublisher:
    """Publishes trading narratives to social media platforms."""

    # Posting constraints - configurable
    DEFAULT_POST_INTERVAL_MINUTES = 10
    DEFAULT_TRADE_UPDATE_INTERVAL_SECONDS = 0
    MAX_POSTS_PER_DAY = 144  # Maximum posts per day (144 = 24h * 6 per hour)
    POST_CHAR_LIMIT = 280  # Standard Twitter limit
    COMPACT_CHAR_LIMIT = 142  # Compact format for best-strategy tweets
    DEFAULT_RETRY_ATTEMPTS = 3
    DEFAULT_RETRY_BACKOFF_SECONDS = 2

    # Hashtags for branding
    HASHTAGS = ["#PipHunter", "#Trading", "#ForexSignals"]
    COMPACT_HASHTAG = "#PH"  # Short hashtag for compact mode

    def __init__(self):
        self.config = self._load_config()
        self.workstream_env = _load_simple_env_file(WORKSTREAM_ENV_FILE)
        self.key_x_credentials = _load_key_x_file(KEY_X_FILE)
        self.post_log = self._load_post_log()
        self.narrative_gen = NarrativeGenerator(data_source="file")
        self.api_enabled = self._check_api_credentials()
        self.MIN_POST_INTERVAL_MINUTES = self._get_config_int(
            "twitter_post_interval_minutes",
            self._get_config_int("social_post_interval_minutes", self.DEFAULT_POST_INTERVAL_MINUTES),
        )
        self.TRADE_UPDATE_INTERVAL_SECONDS = self._get_config_int(
            "twitter_trade_update_interval_seconds",
            self.DEFAULT_TRADE_UPDATE_INTERVAL_SECONDS,
        )
        self.RETRY_ATTEMPTS = max(
            1,
            self._get_config_int("twitter_retry_attempts", self.DEFAULT_RETRY_ATTEMPTS),
        )
        self.RETRY_BACKOFF_SECONDS = max(
            0,
            self._get_config_int("twitter_retry_backoff_seconds", self.DEFAULT_RETRY_BACKOFF_SECONDS),
        )

    def _load_config(self) -> Dict:
        """Load configuration from config.json."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    def _load_post_log(self) -> Dict:
        """Load post history from log file."""
        if POST_LOG_FILE.exists():
            try:
                with open(POST_LOG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading post log: {e}")
        return {"posts": [], "last_post_time": None}

    def _save_post_log(self):
        """Save post history to log file."""
        with open(POST_LOG_FILE, 'w') as f:
            json.dump(self.post_log, f, indent=2, default=str)

    def _get_config_int(self, key: str, default: int) -> int:
        """Read an integer config value with fallback."""
        value = self.config.get(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _get_twitter_credential(self, config_key: str, env_var: str) -> str:
        """Resolve credentials from env, then workstream env, key file, then config."""
        return (
            os.getenv(env_var)
            or self.workstream_env.get(env_var)
            or self.key_x_credentials.get(env_var)
            or self.config.get(config_key, "")
        )

    def _check_api_credentials(self) -> bool:
        """Check if Twitter API credentials are configured."""
        required_pairs = [
            ("twitter_api_key", "TWITTER_API_KEY"),
            ("twitter_api_secret", "TWITTER_API_SECRET"),
            ("twitter_access_token", "TWITTER_ACCESS_TOKEN"),
            ("twitter_access_secret", "TWITTER_ACCESS_SECRET"),
        ]
        return all(self._get_twitter_credential(config_key, env_var) for config_key, env_var in required_pairs)

    def _get_trigger_cooldown_seconds(self, trigger: str) -> int:
        """Return the minimum time between posts for a trigger."""
        if trigger == "trade_update":
            return self.TRADE_UPDATE_INTERVAL_SECONDS
        return self.MIN_POST_INTERVAL_MINUTES * 60

    def can_post(self, trigger: str = "manual") -> tuple[bool, str]:
        """Check if we can post based on rate limits."""
        now = datetime.now()

        # Check minimum interval
        if self.post_log.get("last_post_time"):
            last_post = datetime.fromisoformat(self.post_log["last_post_time"])
            elapsed_seconds = (now - last_post).total_seconds()
            required_gap = self._get_trigger_cooldown_seconds(trigger)
            if elapsed_seconds < required_gap:
                remaining_seconds = required_gap - elapsed_seconds
                if required_gap >= 60:
                    return False, f"Rate limit: wait {remaining_seconds / 60:.0f} more minutes"
                return False, f"Rate limit: wait {remaining_seconds:.0f} more seconds"

        # Check daily limit
        today = now.date().isoformat()
        today_posts = [p for p in self.post_log.get("posts", [])
                       if p.get("date", "")[:10] == today]
        if len(today_posts) >= self.MAX_POSTS_PER_DAY:
            return False, f"Daily limit reached ({self.MAX_POSTS_PER_DAY} posts)"

        return True, "OK"

    def format_teaser_post(self, metrics: Dict) -> str:
        """
        Format a teaser post for Twitter.
        Shows: Overall returns, bias, top performer name
        Hides: Trade details, prices, algo parameters
        """
        bias = metrics.get("bias", "NEUTRAL")
        buy_net = metrics.get("buy_net", 0)
        sell_net = metrics.get("sell_net", 0)
        imbalance = metrics.get("imbalance", 0)
        confidence = metrics.get("confidence", "LOW")
        top_strategy = metrics.get("top_strategy")
        winner = "BUY" if buy_net > sell_net else "SELL"

        emoji = "🟢" if winner == "BUY" else "🔴"

        # Build post
        lines = []
        lines.append(f"{emoji} LIVE BATTLE UPDATE")
        lines.append(f"Bias: {bias} | Confidence: {confidence}")

        if top_strategy:
            lines.append(f"Leader: {top_strategy[:15]}")

        lines.append(f"")
        lines.append(f"See full battle stats:")
        lines.append(WEBSITE_URL)
        lines.append("")
        lines.append(" ".join(self.HASHTAGS[:2]))

        post = "\n".join(lines)

        # Truncate if needed
        if len(post) > self.POST_CHAR_LIMIT:
            post = post[:self.POST_CHAR_LIMIT - 3] + "..."

        return post

    def format_milestone_post(self, milestone_type: str, value: float) -> str:
        """Format a milestone celebration post."""
        if milestone_type == "net_milestone":
            return f"""🎯 MILESTONE REACHED!

Our strategies just hit +{value:.0f} net return today!

See who's winning the battle:
{WEBSITE_URL}

{' '.join(self.HASHTAGS[:2])}"""

        elif milestone_type == "new_leader":
            return f"""👑 NEW LEADER!

{value} has taken the top spot in today's battle!

Watch the live rankings:
{WEBSITE_URL}

{' '.join(self.HASHTAGS[:2])}"""

        elif milestone_type == "bias_shift":
            return f"""⚡ BIAS SHIFT DETECTED!

Market sentiment has flipped to {value}!

See the full analysis:
{WEBSITE_URL}

{' '.join(self.HASHTAGS[:2])}"""

        return ""

    def format_hourly_summary(self, metrics: Dict) -> str:
        """Format an hourly summary post."""
        hour = datetime.now().strftime("%H:00")
        bias = metrics.get("bias", "NEUTRAL")
        confidence = metrics.get("confidence", "LOW")
        open_trades = metrics.get("open_trades", 0)

        return f"""📊 {hour} HOUR UPDATE

Market Bias: {bias}
Confidence: {confidence}
Active Positions: {open_trades}

Full battle stats:
{WEBSITE_URL}

{' '.join(self.HASHTAGS[:2])}"""

    def _truncate_with_suffix(self, value: str, max_len: int, suffix: str = "..") -> str:
        """Deterministically truncate a string and preserve a visible suffix."""
        if max_len <= 0:
            return ""
        if len(value) <= max_len:
            return value
        if max_len <= len(suffix):
            return suffix[:max_len]
        return value[: max_len - len(suffix)] + suffix

    def format_compact_best_strategy(self, metrics: Dict) -> str:
        """
        Format a compact best-strategy tweet (142 chars max).

        Shows: Best strategy name, net return, direction
        Format: "🏆 {STRATEGY} +{NET} {DIR} | {CONF} conf | piphunter.io #PH"
        """
        top = metrics.get("top_strategy", "")
        net = metrics.get("top_strategy_net", 0)
        bias = metrics.get("bias", "BUY")
        conf = metrics.get("confidence", "MED")[:3].upper()

        # Abbreviate confidence
        conf_map = {"HIG": "HI", "MED": "MED", "LOW": "LO"}
        conf_abbr = conf_map.get(conf, conf[:2])

        # Format net with sign
        net_str = f"+{net:.0f}" if net >= 0 else f"{net:.0f}"

        # Truncate strategy name to fit
        # Base: "🏆  +NET DIR | XX | piphunter.io #PH" ~45 chars
        max_strat_len = self.COMPACT_CHAR_LIMIT - 50
        strat = self._truncate_with_suffix(top, max_strat_len) if top else "---"

        emoji = "🟢" if bias == "BUY" else "🔴"

        post = f"{emoji} {strat} {net_str} {bias} | {conf_abbr} | piphunter.io {self.COMPACT_HASHTAG}"

        # Ensure under limit
        if len(post) > self.COMPACT_CHAR_LIMIT:
            # Further truncate strategy
            over = len(post) - self.COMPACT_CHAR_LIMIT
            strat = self._truncate_with_suffix(strat, max(1, len(strat) - over))
            post = f"{emoji} {strat} {net_str} {bias} | {conf_abbr} | piphunter.io {self.COMPACT_HASHTAG}"

        return post

    def format_compact_trade_update(self, trade: Dict) -> str:
        """
        Format a compact real-time trade update (142 chars max).

        Shows: Strategy, product, direction, result
        Format: "⚡ {STRAT} {PRODUCT} {DIR} {RESULT} | piphunter.io #PH"
        """
        strategy = self._truncate_with_suffix(trade.get("strategy_name", trade.get("strategy", "")), 20)
        product = trade.get("product", trade.get("symbol", ""))[:8]
        direction = trade.get("direction", "BUY")[:1]  # B or S
        result = trade.get("net_return", trade.get("pnl", 0))
        status = trade.get("status", "OPEN")

        # Format result
        result_str = f"+{result:.1f}" if result >= 0 else f"{result:.1f}"

        # Status emoji
        if status in ["CLOSED", "COMPLETE"]:
            status_emoji = "✅" if result >= 0 else "❌"
        else:
            status_emoji = "⚡"

        post = f"{status_emoji} {strategy} {product} {direction} {result_str} | piphunter.io {self.COMPACT_HASHTAG}"

        # Ensure under limit
        if len(post) > self.COMPACT_CHAR_LIMIT:
            over = len(post) - self.COMPACT_CHAR_LIMIT
            strategy = self._truncate_with_suffix(strategy, max(1, len(strategy) - over))
            post = f"{status_emoji} {strategy} {product} {direction} {result_str} | piphunter.io {self.COMPACT_HASHTAG}"

        return post

    def _send_tweet_with_retries(self, post_text: str) -> Dict:
        """Send a tweet with bounded retries and fixed backoff."""
        last_result: Dict = {"success": False, "error": "Unknown Twitter publishing failure"}
        for attempt in range(1, self.RETRY_ATTEMPTS + 1):
            result = self._send_tweet(post_text)
            if result.get("success"):
                if attempt > 1:
                    result["attempts"] = attempt
                return result
            last_result = result
            if attempt < self.RETRY_ATTEMPTS and self.RETRY_BACKOFF_SECONDS > 0:
                time.sleep(self.RETRY_BACKOFF_SECONDS)
        return last_result

    def publish_to_twitter(self, post_text: str, trigger: str = "manual") -> Dict:
        """
        Publish a post to Twitter.

        Args:
            post_text: The text to post
            trigger: What triggered this post (bias_shift, milestone, hourly, manual)

        Returns:
            Result dict with success status and details
        """
        # Check rate limits first
        can_post, reason = self.can_post(trigger=trigger)
        if not can_post:
            return {"success": False, "error": reason}

        # Check if API is configured
        if not self.api_enabled:
            # Dry run mode - just log the post
            print(_console_safe_text(f"[DRY RUN] Would post to Twitter:\n{post_text}\n"))
            result = {
                "success": True,
                "dry_run": True,
                "message": "API not configured - dry run mode"
            }
        else:
            # Actual Twitter API call
            try:
                result = self._send_tweet_with_retries(post_text)
            except Exception as e:
                return {"success": False, "error": str(e)}

        # Log the post
        post_entry = {
            "date": datetime.now().isoformat(),
            "trigger": trigger,
            "text": post_text[:100] + "..." if len(post_text) > 100 else post_text,
            "success": result.get("success", False),
            "dry_run": result.get("dry_run", False)
        }

        self.post_log["posts"].insert(0, post_entry)
        self.post_log["posts"] = self.post_log["posts"][:100]  # Keep last 100
        self.post_log["last_post_time"] = datetime.now().isoformat()
        self._save_post_log()

        return result

    def _send_tweet(self, text: str) -> Dict:
        """
        Send a tweet using Twitter API v2.

        Requires tweepy library: pip install tweepy
        """
        try:
            import tweepy
        except ImportError:
            return {
                "success": False,
                "error": "tweepy library not installed. Run: pip install tweepy"
            }

        try:
            client = tweepy.Client(
                consumer_key=self._get_twitter_credential("twitter_api_key", "TWITTER_API_KEY"),
                consumer_secret=self._get_twitter_credential("twitter_api_secret", "TWITTER_API_SECRET"),
                access_token=self._get_twitter_credential("twitter_access_token", "TWITTER_ACCESS_TOKEN"),
                access_token_secret=self._get_twitter_credential("twitter_access_secret", "TWITTER_ACCESS_SECRET")
            )

            response = client.create_tweet(text=text)

            return {
                "success": True,
                "tweet_id": response.data["id"],
                "message": "Tweet posted successfully"
            }

        except tweepy.TweepyException as e:
            return {"success": False, "error": str(e)}

    def check_and_post_triggers(self, current_metrics: Dict, previous_metrics: Optional[Dict] = None) -> List[Dict]:
        """
        Check for trigger events and post if conditions are met.

        Triggers:
        1. Bias shift (BUY <-> SELL)
        2. Net milestone (+500, +1000, etc.)
        3. Hourly interval

        Args:
            current_metrics: Current market metrics
            previous_metrics: Previous metrics for comparison

        Returns:
            List of post results
        """
        results = []

        # Check bias shift
        if previous_metrics:
            prev_bias = previous_metrics.get("bias")
            curr_bias = current_metrics.get("bias")
            if prev_bias and curr_bias and prev_bias != curr_bias:
                post_text = self.format_milestone_post("bias_shift", curr_bias)
                if post_text:
                    result = self.publish_to_twitter(post_text, trigger="bias_shift")
                    results.append(result)
                    if result.get("success"):
                        return results  # One post per check

        # Check net milestone (every 500)
        buy_net = current_metrics.get("buy_net", 0)
        sell_net = current_metrics.get("sell_net", 0)
        total_net = max(buy_net, sell_net)  # Use the winning side

        if total_net > 0:
            milestone = (int(total_net) // 500) * 500
            if milestone > 0:
                last_milestone = self.post_log.get("last_net_milestone", 0)
                if milestone > last_milestone:
                    post_text = self.format_milestone_post("net_milestone", milestone)
                    if post_text:
                        result = self.publish_to_twitter(post_text, trigger="milestone")
                        if result.get("success"):
                            self.post_log["last_net_milestone"] = milestone
                            self._save_post_log()
                        results.append(result)
                        if result.get("success"):
                            return results

        return results

    def publish_hourly(self) -> Dict:
        """Publish an hourly summary post."""
        data = self.narrative_gen.load_data()
        metrics = self.narrative_gen.extract_metrics(data)

        post_text = self.format_hourly_summary(metrics)
        return self.publish_to_twitter(post_text, trigger="hourly")

    def publish_teaser(self) -> Dict:
        """Publish a teaser post with current metrics."""
        data = self.narrative_gen.load_data()
        metrics = self.narrative_gen.extract_metrics(data)

        post_text = self.format_teaser_post(metrics)
        return self.publish_to_twitter(post_text, trigger="teaser")

    def publish_compact_best_strategy(self) -> Dict:
        """Publish a compact best-strategy summary (142 chars)."""
        data = self.narrative_gen.load_data()
        metrics = self.narrative_gen.extract_metrics(data)

        post_text = self.format_compact_best_strategy(metrics)
        return self.publish_to_twitter(post_text, trigger="compact_best")

    def publish_trade_update(self, trade: Dict) -> Dict:
        """
        Publish a real-time trade update (142 chars).

        Args:
            trade: Trade data dict with strategy_name, product, direction, status, net_return

        Returns:
            Result dict with success status
        """
        # Check for duplicate suppression
        trade_id = trade.get("trade_id", trade.get("id", ""))
        if self._is_duplicate_trade_post(trade_id):
            return {"success": False, "error": "Duplicate trade post suppressed"}

        post_text = self.format_compact_trade_update(trade)
        result = self.publish_to_twitter(post_text, trigger="trade_update")

        # Track posted trade IDs for dedup
        if result.get("success"):
            self._mark_trade_posted(trade_id)

        return result

    def publish_direct_text(self, post_text: str, trigger: str = "manual_api") -> Dict:
        """
        Publish arbitrary text directly through the configured X/Twitter API path.

        Args:
            post_text: Fully prepared post body.
            trigger: Trigger name for rate-limit and audit logging.

        Returns:
            Result dict with success status and details.
        """
        text = str(post_text or "").strip()
        if not text:
            return {"success": False, "error": "Post text is required"}
        if len(text) > self.POST_CHAR_LIMIT:
            return {
                "success": False,
                "error": f"Post exceeds {self.POST_CHAR_LIMIT} character limit",
                "length": len(text),
            }
        return self.publish_to_twitter(text, trigger=trigger)

    def _is_duplicate_trade_post(self, trade_id: str) -> bool:
        """Check if this trade has already been posted recently."""
        if not trade_id:
            return False
        posted = self.post_log.get("posted_trade_ids", [])
        return trade_id in posted

    def _mark_trade_posted(self, trade_id: str):
        """Mark a trade as posted for duplicate suppression."""
        if not trade_id:
            return
        if "posted_trade_ids" not in self.post_log:
            self.post_log["posted_trade_ids"] = []
        self.post_log["posted_trade_ids"].append(trade_id)
        # Keep only last 100 trade IDs
        self.post_log["posted_trade_ids"] = self.post_log["posted_trade_ids"][-100:]
        self._save_post_log()

    def publish_best_strategy_trade_updates(self, trades: Optional[List[Dict]] = None) -> List[Dict]:
        """Publish updates for trades that belong to the current best strategy."""
        target_trades = trades if trades is not None else self.get_best_strategy_trades()
        results: List[Dict] = []
        for trade in target_trades:
            results.append(self.publish_trade_update(trade))
        return results

    def get_best_strategy_trades(self) -> List[Dict]:
        """Get recent trades for the current best strategy."""
        data = self.narrative_gen.load_data()
        metrics = self.narrative_gen.extract_metrics(data)
        best_strategy = metrics.get("top_strategy")

        if not best_strategy:
            return []

        # Load trades from grid_live
        grid_data = data.get("grid_live", {})
        trades = grid_data.get("trades", [])

        # Filter for best strategy
        return [t for t in trades if t.get("strategy_name", t.get("strategy", "")) == best_strategy]


# Flask endpoint integration
def add_social_routes(app):
    """Add social publishing API routes to existing Flask app."""

    publisher = SocialPublisher()

    @app.route('/api/social/status', methods=['GET'])
    def get_social_status():
        """Get social publishing status and recent posts."""
        can_post, reason = publisher.can_post()
        return {
            "api_enabled": publisher.api_enabled,
            "can_post": can_post,
            "reason": reason,
            "recent_posts": publisher.post_log.get("posts", [])[:10],
            "last_post_time": publisher.post_log.get("last_post_time")
        }

    @app.route('/api/social/preview', methods=['GET'])
    def preview_post():
        """Preview what would be posted."""
        data = publisher.narrative_gen.load_data()
        metrics = publisher.narrative_gen.extract_metrics(data)

        compact_best = publisher.format_compact_best_strategy(metrics)

        return {
            "teaser": publisher.format_teaser_post(metrics),
            "hourly": publisher.format_hourly_summary(metrics),
            "compact_best": compact_best,
            "compact_best_length": len(compact_best),
            "metrics": metrics
        }

    @app.route('/api/social/publish', methods=['POST'])
    def manual_publish():
        """Manually trigger a post (requires API key)."""
        from flask import request

        post_type = request.json.get("type", "teaser")

        if post_type == "teaser":
            result = publisher.publish_teaser()
        elif post_type == "hourly":
            result = publisher.publish_hourly()
        elif post_type == "compact_best":
            result = publisher.publish_compact_best_strategy()
        else:
            return {"success": False, "error": f"Unknown post type: {post_type}"}, 400

        return result

    @app.route('/api/social/publish_trade', methods=['POST'])
    def publish_trade():
        """Publish a real-time trade update."""
        from flask import request

        trade = request.json.get("trade", {})
        if not trade:
            return {"success": False, "error": "No trade data provided"}, 400

        result = publisher.publish_trade_update(trade)
        return result

    @app.route('/api/social/publish_best_strategy_trades', methods=['POST'])
    def publish_best_strategy_trades():
        """Publish trade updates for the current best strategy."""
        from flask import request

        payload = request.json or {}
        trades = payload.get("trades")
        result = publisher.publish_best_strategy_trade_updates(trades=trades)
        return {"results": result, "count": len(result)}

    @app.route('/api/social/best_strategy_trades', methods=['GET'])
    def get_best_strategy_trades():
        """Get trades for the current best strategy."""
        trades = publisher.get_best_strategy_trades()
        return {"trades": trades, "count": len(trades)}

    @app.route('/api/social/x_api_post', methods=['POST'])
    def publish_x_api_post():
        """Publish arbitrary prepared text through the X API-backed path."""
        from flask import request

        payload = request.json or {}
        post_text = payload.get("text", "")
        trigger = payload.get("trigger", "manual_api")

        result = publisher.publish_direct_text(post_text, trigger=trigger)
        status_code = 200 if result.get("success") else 400
        return result, status_code


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PipHunter Social Publisher")
    parser.add_argument("--action", choices=["preview", "publish", "status", "publish_best_strategy_trades"],
                        default="preview", help="Action to perform")
    parser.add_argument("--type", choices=["teaser", "hourly", "compact_best"],
                        default="teaser", help="Post type")

    args = parser.parse_args()

    publisher = SocialPublisher()

    if args.action == "status":
        can_post, reason = publisher.can_post()
        print(f"API Enabled: {publisher.api_enabled}")
        print(f"Can Post: {can_post} ({reason})")
        print(f"Post Interval: {publisher.MIN_POST_INTERVAL_MINUTES} minutes")
        print(f"Trade Update Interval: {publisher.TRADE_UPDATE_INTERVAL_SECONDS} seconds")
        print(f"Recent Posts: {len(publisher.post_log.get('posts', []))}")

    elif args.action == "preview":
        data = publisher.narrative_gen.load_data()
        metrics = publisher.narrative_gen.extract_metrics(data)

        if args.type == "teaser":
            print("=== TEASER POST PREVIEW ===")
            print(publisher.format_teaser_post(metrics))
        elif args.type == "hourly":
            print("=== HOURLY POST PREVIEW ===")
            print(publisher.format_hourly_summary(metrics))
        elif args.type == "compact_best":
            compact = publisher.format_compact_best_strategy(metrics)
            print("=== COMPACT BEST STRATEGY PREVIEW ===")
            print(_console_safe_text(compact))
            print(f"\n[Length: {len(compact)}/{publisher.COMPACT_CHAR_LIMIT} chars]")

    elif args.action == "publish":
        if args.type == "teaser":
            result = publisher.publish_teaser()
        elif args.type == "hourly":
            result = publisher.publish_hourly()
        elif args.type == "compact_best":
            result = publisher.publish_compact_best_strategy()
        print(f"Result: {json.dumps(result, indent=2)}")

    elif args.action == "publish_best_strategy_trades":
        results = publisher.publish_best_strategy_trade_updates()
        print(f"Results: {json.dumps(results, indent=2)}")


 succeeded in 2106ms:
"""
Breakout Trade Viewer API Server
Activation model v2:
- Activation keys are STRATEGY + DIRECTION + MODE ONLY
- Products are stored as metadata inside activation entries
- Legacy keys containing product suffixes are auto-migrated
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import threading
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
import re
import uuid
import shutil
import urllib.request # Switched to urllib for better compatibility
from typing import Dict, Any, List, Set, Tuple, Optional
from constants import VERSION # V20260105_2220
# V20260105_0025: Added /api/activations/remove endpoint
from market_update_generator import generate_market_update
from narrative_generator import add_narrative_routes
from social_publisher import add_social_routes
from subscriber_api import add_subscriber_routes
from json_layout import (
    configured_product_types,
    default_product_type,
    ensure_day_dir,
    iter_day_dirs,
    load_layout_config,
    product_type_for_product,
    resolve_day_dir,
)

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Global Locks
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# [V20260128_1515] Lock for serializing access to grid_live.json
GRID_LIVE_LOCK = threading.Lock()

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# App setup
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
app = Flask(__name__)
CORS(app)

# [V20260224] Add narrative generation routes for PipHunter
add_narrative_routes(app)

# [V20260224] Add social publishing routes for PipHunter
add_social_routes(app)

# [V20260224] Add subscriber management routes for PipHunter
add_subscriber_routes(app)

BASE_PATH = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json")
ROOT_PATH = BASE_PATH.parent
CONFIG_FILE = ROOT_PATH / "config.json"
ACTIVATIONS_FILE = ROOT_PATH / "activations.json"
WORKFLOWS_FILE = ROOT_PATH / "workflows.json"
WORKFLOW_MULTI_CHART_PAYLOAD_FILE = ROOT_PATH / "workflow_multi_chart_payload.json"
ACTIVATION_SUFFIXES = ("_buy_net", "_sell_net", "_buy_alt", "_sell_alt")


def _load_layout_runtime_config() -> dict:
    cfg = load_layout_config(CONFIG_FILE)
    cfg.setdefault("product_type", default_product_type(cfg))
    cfg.setdefault("product_types", configured_product_types(cfg))
    cfg.setdefault("product_type_by_product", {})
    return cfg


def _infer_product_type(product: str | None = None) -> str:
    return product_type_for_product(product, _load_layout_runtime_config())


def _trade_quantity_for_product(product: str | None = None, cfg: Optional[Dict[str, Any]] = None) -> int:
    cfg = cfg or _load_layout_runtime_config()
    raw_by_product = cfg.get('min_value_by_product', {})
    product_key = str(product or '').strip().upper()
    if isinstance(raw_by_product, dict) and product_key:
        raw_value = raw_by_product.get(product_key)
        if raw_value not in (None, ''):
            try:
                return max(1, int(round(float(raw_value) * 1000.0)))
            except (TypeError, ValueError):
                pass

    raw_by_type = cfg.get('min_value_by_product_type', {})
    product_type = _infer_product_type(product)
    if isinstance(raw_by_type, dict):
        raw_value = raw_by_type.get(str(product_type).strip().lower())
        if raw_value not in (None, ''):
            try:
                return max(1, int(round(float(raw_value) * 1000.0)))
            except (TypeError, ValueError):
                pass

    raw_default = cfg.get('default_min_value')
    if raw_default not in (None, ''):
        try:
            return max(1, int(round(float(raw_default) * 1000.0)))
        except (TypeError, ValueError):
            pass

    default_pct = float(cfg.get('trade_qty_percent', 45.0))
    pct = float(cfg.get('crypto_trade_qty_percent', default_pct)) if _infer_product_type(product) == 'crypto' else default_pct
    return int(100000 * (pct / 100.0))


def _resolve_day_dir(mode: str, date_str: str, product: str | None = None, product_type: str | None = None) -> Path:
    cfg = _load_layout_runtime_config()
    resolved_type = product_type or (product_type_for_product(product, cfg) if product else cfg.get("product_type"))
    return resolve_day_dir(BASE_PATH, mode, date_str, resolved_type)


def _ensure_day_dir(mode: str, date_str: str, product: str | None = None, product_type: str | None = None) -> Path:
    cfg = _load_layout_runtime_config()
    resolved_type = product_type or (product_type_for_product(product, cfg) if product else cfg.get("product_type"))
    return ensure_day_dir(BASE_PATH, mode, date_str, config=cfg, product=product, product_type=resolved_type)


def _iter_day_dirs_for(mode: str, date_str: str, product_type: str | None = None) -> list[Path]:
    if product_type:
        resolved = _resolve_day_dir(mode, date_str, product_type=product_type)
        return [resolved] if resolved.exists() else []
    return iter_day_dirs(BASE_PATH, mode, date_str, config=_load_layout_runtime_config())


def _iter_trade_json_files(day_dir: Path, include_archived_closed: bool = False, product_hint: str | None = None):
    """
    Yield candidate trade JSON files for a day directory.
    Open trades remain top-level only; archived closed trades can be included
    recursively from `archive/<HHMMSS>/`.
    """
    if not day_dir.exists():
        return

    glob_pattern = f"*{product_hint}*.json" if product_hint else "*.json"

    seen: set[str] = set()

    for json_file in day_dir.glob(glob_pattern):
        if not json_file.is_file():
            continue
        if json_file.name.startswith('_'):
            continue
        seen.add(str(json_file))
        yield json_file

    if not include_archived_closed:
        return

    archive_dir = day_dir / 'archive'
    if not archive_dir.exists():
        return

    for json_file in archive_dir.rglob(glob_pattern):
        if not json_file.is_file():
            continue
        if json_file.name.startswith('_'):
            continue
        if not json_file.name.lower().endswith(('_cl.json', '_cld.json')):
            continue
        json_file_key = str(json_file)
        if json_file_key in seen:
            continue
        seen.add(json_file_key)
        yield json_file


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# API Endpoints
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route('/api/trade_file', methods=['GET'])
def get_trade_file():
    """Load raw content of a specific trade JSON file [V20251230_0010] [V20260122_FS]"""
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product = request.args.get('product')
        product_type = request.args.get('product_type')
        # Support both 'filename' and 'trade_id' parameters for compatibility
        filename = request.args.get('filename') or request.args.get('trade_id')

        if not filename:
            return jsonify({'success': False, 'message': 'Filename or trade_id is required'}), 400

        # Prevent directory traversal
        safe_name = os.path.basename(filename)
        candidate_names = [safe_name]
        normalized = _strip_trade_suffix(safe_name)
        base_stem = Path(normalized).stem
        for suffix in ('_op.json', '_cl.json', '_cld.json'):
            candidate_names.append(f"{base_stem}{suffix}")

        candidate_day_dirs = _iter_day_dirs_for(run_mode, date, product_type)
        preferred_day_dir = _resolve_day_dir(run_mode, date, product=product, product_type=product_type)
        if preferred_day_dir not in candidate_day_dirs:
            candidate_day_dirs.insert(0, preferred_day_dir)
        file_path = None
        for candidate in candidate_names:
            for day_dir in candidate_day_dirs:
                for p in (day_dir / candidate, day_dir / 'virtual' / candidate):
                    if p.exists():
                        file_path = p
                        safe_name = candidate
                        break
                if file_path:
                    break
            if file_path:
                break

            for day_dir in candidate_day_dirs:
                for archived_file in _iter_trade_json_files(day_dir, include_archived_closed=True):
                    if archived_file.name == candidate:
                        file_path = archived_file
                        safe_name = candidate
                        break
                if file_path:
                    break
            if file_path:
                break

        # [V20260122_FS] Robust search: If no path found and 'filename' looks like an ID, search directory
        if not file_path and (filename.isdigit() or len(filename) < 10):
            print(f"[TRADE_FILE] Explicit match failed for {filename}, searching directory {date}...")
            for day_dir in candidate_day_dirs:
                search_dirs = [day_dir, day_dir / 'virtual']
                for s_dir in search_dirs:
                    if not s_dir.exists():
                        continue
                    for json_file in s_dir.glob('*.json'):
                        if filename in json_file.name:
                            try:
                                with open(json_file, 'r') as f:
                                    data = json.load(f)
                                    if str(data.get('trade_id')) == str(filename):
                                        file_path = json_file
                                        break
                            except:
                                continue
                    if file_path:
                        break
                if file_path:
                    break

            if not file_path:
                for day_dir in candidate_day_dirs:
                    for json_file in _iter_trade_json_files(day_dir, include_archived_closed=True):
                        if filename not in json_file.name:
                            continue
                        try:
                            with open(json_file, 'r') as f:
                                data = json.load(f)
                                if str(data.get('trade_id')) == str(filename):
                                    file_path = json_file
                                    break
                        except:
                            continue
                    if file_path:
                        break

        if not file_path:
            return jsonify({'success': False, 'message': f'File not found: {filename}'}), 404

        with open(file_path, 'r') as f:
            content = json.load(f)

        return jsonify({
            'success': True,
            'filename': filename,
            'content': content
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """Workflow automation definitions and runtime state."""
    try:
        data = _load_workflows()
        workflows = data.get("workflows", [])
        enriched = []
        for w in workflows:
            if not isinstance(w, dict):
                continue
            item = dict(w)
            item["active_now"] = _workflow_active_now(item)
            enriched.append(item)

        # Persist defaults if file missing/outdated
        if not WORKFLOWS_FILE.exists():
            save_payload = dict(data)
            save_payload["workflows"] = workflows
            _save_workflows(save_payload)

        return jsonify({"success": True, "workflows": enriched, "updated_at": data.get("updated_at")})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/workflows/update', methods=['POST'])
def update_workflow():
    """Update one workflow schedule/toggle settings."""
    try:
        payload = request.json or {}
        workflow_id = str(payload.get("id") or "").strip()
        if not workflow_id:
            return jsonify({"success": False, "message": "id is required"}), 400

        data = _load_workflows()
        workflows = data.get("workflows", [])
        target = None
        for w in workflows:
            if isinstance(w, dict) and str(w.get("id")) == workflow_id:
                target = w
                break
        if target is None:
            return jsonify({"success": False, "message": "Workflow not found"}), 404

        if "enabled" in payload:
            target["enabled"] = bool(payload.get("enabled"))

        if "start_time" in payload:
            st = str(payload.get("start_time") or "").strip()
            if _hhmm_to_minutes(st) is None:
                return jsonify({"success": False, "message": "start_time must be HH:MM"}), 400
            target["start_time"] = st

        if "end_time" in payload:
            et = str(payload.get("end_time") or "").strip()
            if _hhmm_to_minutes(et) is None:
                return jsonify({"success": False, "message": "end_time must be HH:MM"}), 400
            target["end_time"] = et

        if "config" in payload:
            cfg_in = payload.get("config")
            if not isinstance(cfg_in, dict):
                return jsonify({"success": False, "message": "config must be object"}), 400
            cfg_existing = target.get("config", {}) if isinstance(target.get("config"), dict) else {}
            cfg_merged = dict(cfg_existing)
            for k, v in cfg_in.items():
                cfg_merged[str(k)] = v
            target["config"] = cfg_merged

        target["updated_at"] = datetime.now().isoformat()
        data["workflows"] = workflows
        _save_workflows(data)

        out = dict(target)
        out["active_now"] = _workflow_active_now(out)
        return jsonify({"success": True, "workflow": out})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/workflows/run', methods=['POST'])
def run_workflow_now():
    """Run one workflow immediately (manual trigger)."""
    try:
        payload = request.json or {}
        workflow_id = str(payload.get("id") or "").strip()
        mode = str(payload.get("mode") or "").strip().lower()
        date_str = str(payload.get("date") or "").strip()
        if not workflow_id:
            return jsonify({"success": False, "message": "id is required"}), 400

        cfg_live = _load_config_safe()
        if mode not in ("live", "sim"):
            mode = str(cfg_live.get("run_mode", "live")).lower()
            if mode not in ("live", "sim"):
                mode = "live"
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        workflows_data = _load_workflows()
        workflows = workflows_data.get("workflows", [])
        wf = next((w for w in workflows if isinstance(w, dict) and str(w.get("id")) == workflow_id), None)
        if wf is None:
            return jsonify({"success": False, "message": "Workflow not found"}), 404

        if workflow_id == "TB_workflow":
            result = _run_tb_workflow_once(mode, date_str, wf)
        elif workflow_id == "profile_match_workflow":
            result = _run_profile_match_workflow_once(mode, date_str, wf)
        elif workflow_id == "top_x_multi_chart_workflow":
            result = _run_top_x_multi_chart_workflow(mode, date_str, wf)
        elif workflow_id == "multi_chart_prune_negative_non_live":
            result = {
                "success": True,
                "message": "Client-side workflow. It runs inside multi_chart every minute when enabled."
            }
        elif workflow_id == "tb_prune_all_negative":
            result = _run_tb_prune_all_negative_once(mode, date_str, wf)
        else:
            return jsonify({"success": False, "message": f"Run-now not supported for workflow '{workflow_id}'"}), 400

        _WORKFLOW_LAST_RUN[workflow_id] = time.time()
        return jsonify({"success": bool(result.get("success")), "result": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def _strip_trade_suffix(filename: str) -> str:
    name = os.path.basename(filename)
    # [V20260129_0130] Pre-clean double extensions like .json.json
    while name.lower().endswith('.json.json'):
        name = name[:-5]
        
    if not name.lower().endswith('.json'):
        name = f"{name}.json"
        
    for suffix in ('_cld.json', '_cl.json', '_op.json'):
        if name.lower().endswith(suffix):
            return name[:-len(suffix)] + '.json'
    return name



def _update_automated_source(source_name: str):
    """Update automated_trade_source in config.json. [V20260205_2100]"""
    try:
        if not CONFIG_FILE.exists():
            return
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        
        changed = False
        if cfg.get('automated_trade_source') != source_name:
            cfg['automated_trade_source'] = source_name
            changed = True
        current_multi = cfg.get('automated_trade_sources')
        if not isinstance(current_multi, list):
            current_multi = [cfg.get('automated_trade_source')] if cfg.get('automated_trade_source') else []
        normalized = []
        for s in current_multi:
            if isinstance(s, str) and s.strip():
                sv = s.strip()
                if sv not in normalized:
                    normalized.append(sv)
        if source_name not in normalized:
            normalized.append(source_name)
            changed = True
        cfg['automated_trade_sources'] = normalized
        if changed:
            with open(CONFIG_FILE, "w") as f:
                json.dump(cfg, f, indent=4)
            print(f"[CONFIG] automated_trade_source(s) updated: single={source_name}, multi={normalized}")
    except Exception as e:
        print(f"[ERROR] Failed to update automated_trade_source: {e}")

def _is_source_allowed(requested_source: str) -> bool:
    """Check if the requested automated source is allowed. [V20260205_2100]"""
    try:
        if not CONFIG_FILE.exists():
            return True # Default to allowed if no config
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        
        current_multi = cfg.get('automated_trade_sources')
        if isinstance(current_multi, list):
            allowed = [str(s).strip() for s in current_multi if isinstance(s, str) and str(s).strip()]
            if allowed:
                return requested_source in allowed
        current_source = cfg.get('automated_trade_source')
        if not current_source:
            return True
        return current_source == requested_source
    except Exception as e:
        print(f"[ERROR] Failed to check automated_trade_source: {e}")
        return True

def _load_trade_products() -> Set[str]:
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        return {p.upper() for p in cfg.get("trade_products", []) if isinstance(p, str)}
    except Exception:
        return set()


def _default_workflows_payload() -> dict:
    return {
        "version": "V20260216_0010",
        "updated_at": datetime.now().isoformat(),
        "workflows": [
            {
                "id": "TB_workflow",
                "name": "TB_workflow",
                "description": "Auto pipeline: pick top Summary row, expand same-parameter family, optimize start-from range, save+activate TB.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Select best Performance Summary Breakdown row by total net",
                    "Send selection to Multi Chart and add all same-parameter strategies/metrics",
                    "Adjust start-from so max net range is under configured threshold",
                    "Save as Trade Bucket and activate"
                ],
                "config": {
                    "metric": "net",
                    "delta_type": "delta2",
                    "product_type": "forex",
                    "max_range_target": 150,
                    "minimum_difference": 5.0,
                    "run_interval_sec": 900,
                    "max_buckets_per_day": 3,
                    "min_profitability_pct": 80.0,
                    "min_trade_count": 10,
                    "max_strategies_per_card": 4
                }
            },
            {
                "id": "profile_match_workflow",
                "name": "profile_match_workflow",
                "description": "Find current strategy/product pairs above profitability threshold and push to Multi Charts feed.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Scan current Top20 strategies for profitability >= threshold",
                    "Filter by minimum trade count, min total net >= X, and min avg net >= X",
                    "Optionally expand to all same-parameter strategies/metrics when preparing Multi Chart payload",
                    "Optionally adjust start-time baseline so highest net range is under 150 before TB send",
                    "Send matching strategy/product pairs to Multi Charts import payload"
                ],
                "config": {
                    "min_profitability_pct": 85.0,
                    "min_trade_count": 1,
                    "min_total_net": 0.0,
                    "min_avg_net": 0.0,
                    "max_items": 20,
                    "metric": "net",
                    "delta_type": "delta2",
                    "product_type": "forex",
                    "scalper_only": False,
                    "enforce_market_bias": False,
                    "bias_recent_profitable_count": 2,
                    "add_to_tb": False,
                    "add_same_parameter_strategies_metrics": False,
                    "adjust_start_time_under_150": False,
                    "run_interval_sec": 300
                }
            },
            {
                "id": "multi_chart_prune_negative_non_live",
                "name": "multi_chart_prune_negative_non_live",
                "description": "Scan multi-chart every minute and remove non-live cards only when all chart sums(net) in the card are negative.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Scan visible Multi Chart cards every minute",
                    "Skip cards currently LIVE",
                    "Remove cards where all sum(net) values are negative"
                ],
                "config": {
                    "run_interval_sec": 60,
                    "product_type": "forex",
                    "negative_threshold": 0
                }
            },
            {
                "id": "tb_prune_all_negative",
                "name": "tb_prune_all_negative",
                "description": "Every minute, remove trade buckets where all strategy net values are below threshold.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Scan trade buckets for current mode/date",
                    "Evaluate strategy nets inside each bucket",
                    "Delete bucket if all strategy nets are below threshold"
                ],
                "config": {
                    "run_interval_sec": 60,
                    "product_type": "forex",
                    "negative_threshold": -20
                }
            },
            {
                "id": "top_x_multi_chart_workflow",
                "name": "Top X Multi-Chart Loader",
                "description": "Extracts the Top X (by total net) strategies from the Top 20 list and forces them into the Multi-Chart view.",
                "enabled": False,
                "start_time": "00:00",
                "end_time": "23:59",
                "timezone": "local",
                "steps": [
                    "Fetch the current mode/date Top 20 strategies",
                    "Filter by Scalper and/or Rev Scalper type if selected",
                    "Sort the filtered list descending by Total Net",
                    "Select exactly Top X strategies from the sorted list",
                    "Optionally add the best matching strategy to TB and activate",
                    "Optionally include all same-parameter strategies/metrics in the Multi-Chart payload",
                    "Send the matching strategies to the Multi Charts import payload"
                ],
                "config": {
                    "top_x": 6,
                    "metric": "net",
                    "delta_type": "delta2",
                    "product_type": "forex",
                    "include_scalper": True,
                    "include_rev_scalper": True,
                    "add_to_tb": False,
                    "add_same_parameter_strategies_metrics": False,
                    "run_interval_sec": 300
                }
            }
        ]
    }

def _load_workflows() -> dict:
    if WORKFLOWS_FILE.exists():
        try:
            with open(WORKFLOWS_FILE, "r") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                data = {}
        except Exception:
            data = {}
    else:
        data = {}

    defaults = _default_workflows_payload()
    workflows = data.get("workflows")
    if not isinstance(workflows, list):
        workflows = []

    existing_ids = {str(w.get("id")) for w in workflows if isinstance(w, dict)}
    for d in defaults["workflows"]:
        if d["id"] not in existing_ids:
            workflows.append(d)

    out = {
        "version": data.get("version") or defaults["version"],
        "updated_at": data.get("updated_at") or datetime.now().isoformat(),
        "workflows": workflows
    }
    return out


def _save_workflows(payload: dict):
    payload = payload or {}
    payload["updated_at"] = datetime.now().isoformat()
    with open(WORKFLOWS_FILE, "w") as f:
        json.dump(payload, f, indent=4)


def _hhmm_to_minutes(hhmm: str) -> Optional[int]:
    s = str(hhmm or "").strip()
    m = re.fullmatch(r"([01]\d|2[0-3]):([0-5]\d)", s)
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def _workflow_active_now(workflow: dict) -> bool:
    if not bool(workflow.get("enabled")):
        return False
    start_m = _hhmm_to_minutes(workflow.get("start_time"))
    end_m = _hhmm_to_minutes(workflow.get("end_time"))
    if start_m is None or end_m is None:
        return False
    now = datetime.now()
    now_m = now.hour * 60 + now.minute
    if start_m <= end_m:
        return start_m <= now_m <= end_m
    # Overnight window (e.g. 22:00 -> 02:00)
    return now_m >= start_m or now_m <= end_m


def _parse_model_signature(model_name: str) -> Tuple[str, str]:
    """
    Split model into base + param-signature.
    Example: breakout_R_3_tp10.0_sl50.0 -> (breakout_R, 3_tp10.0_sl50.0)
    """
    s = str(model_name or "").strip()
    m = re.search(r"(_\d+)?_tp[\d\.]+_sl[\d\.]+$", s)
    if not m:
        return s, "default"
    suffix = s[m.start() + 1:]
    base = s[:m.start()]
    return base, suffix


def _series_value_at_or_before(series: List[dict], target_dt: datetime, field: str = "net") -> float:
    """[V20260311_1215] Get value for a specific field at or before target datetime."""
    v = 0.0
    for p in series:
        ts = p.get("t")
        if not ts:
            continue
        try:
            p_dt = datetime.fromisoformat(str(ts).replace("Z", ""))
        except Exception:
            continue
        if p_dt <= target_dt:
            try:
                # [V20260311_1345] Use the specified field (net, buy_net, sell_net, alt_net)
                v = float(p.get(field, p.get("net", 0.0)) or 0.0)
            except Exception:
                v = 0.0
        else:
            break
    return v


def _select_tb_workflow_candidate(mode: str, date_str: str, wf_cfg: Optional[dict] = None) -> Optional[dict]:
    """
    Step 1 + 2 selector:
    - Pick best model/product by latest total net
    - Expand to all model/product pairs with same params signature.
    """
    wf_cfg = wf_cfg or {}
    product_type = str(wf_cfg.get("product_type") or "").strip().lower() or None
    min_profitability = float(wf_cfg.get("min_profitability_pct", 80.0) or 80.0)
    min_trade_count = int(wf_cfg.get("min_trade_count", 10) or 10)
    max_card_strategies = int(wf_cfg.get("max_strategies_per_card", 4) or 4)

    # [V20260317_1105] Load all matching summary data
    strategies: Dict[str, dict] = {}
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        summary_file = day_dir / "_summary_net.json"
        if summary_file.exists():
            try:
                with open(summary_file, "r") as f:
                    s_data = json.load(f) or {}
                    s_strats = s_data.get("strategies", {})
                    if isinstance(s_strats, dict):
                        for m_name, products in s_strats.items():
                            if m_name not in strategies:
                                strategies[m_name] = {}
                            strategies[m_name].update(products)
            except Exception:
                pass

    if not strategies:
        return None

    # Choose one best "card" candidate from top20 with profitability/trade-count gating.
    # [V20260317_1105] Load all matching top20 entries
    best = None
    candidates = []
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        top20_file = day_dir / "_top20.json"
        if top20_file.exists():
            try:
                with open(top20_file, "r") as f:
                    top20 = (json.load(f) or {}).get("top20", [])
                for r in top20:
                    if not isinstance(r, dict):
                        continue
                    strategy = str(r.get("strategy") or "").strip()
                    product = str(r.get("product") or "").strip()
                    trade_count = int(r.get("trade_count", 0) or 0)
                    buy_count = int(r.get("buy_count", 0) or 0)
                    sell_count = int(r.get("sell_count", 0) or 0)
                    buy_pct = float(r.get("buyPercent", 0.0) or 0.0)
                    sell_pct = float(r.get("sellPercent", 0.0) or 0.0)
                    total_net = float(r.get("total_net", 0.0) or 0.0)
                    denom = max(1, buy_count + sell_count)
                    profitability = ((buy_pct * buy_count) + (sell_pct * sell_count)) / denom
                    if trade_count < min_trade_count:
                        continue
                    if profitability < min_profitability:
                        continue
                    candidates.append({
                        "model": strategy,
                        "product": product,
                        "net": total_net,
                        "trade_count": trade_count,
                        "profitability": profitability
                    })
            except Exception:
                pass

    # Fallback if top20 unavailable/empty: pick best latest-net from summary.
    if not candidates:
        for model, products in strategies.items():
            if not isinstance(products, dict):
                continue
            for product, series in products.items():
                if not isinstance(series, list) or not series:
                    continue
                try:
                    net = float(series[-1].get("net", 0.0) or 0.0)
                except Exception:
                    net = 0.0
                candidates.append({
                    "model": model,
                    "product": product,
                    "net": net,
                    "trade_count": 0,
                    "profitability": 0.0
                })

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x["net"], x["profitability"], x["trade_count"]), reverse=True)
    best = candidates[0]

    _, sig = _parse_model_signature(best["model"])
    product_scope = str(best["product"]).upper()

    # 1-card scope: same params signature + same product only, capped to max_strategies_per_card.
    family_all = []
    for model, products in strategies.items():
        if not isinstance(products, dict):
            continue
        _, model_sig = _parse_model_signature(model)
        if model_sig != sig:
            continue
        for product, series in products.items():
            if str(product).upper() != product_scope:
                continue
            if not isinstance(series, list) or not series:
                continue
            try:
                latest_net = float(series[-1].get("net", 0.0) or 0.0)
            except Exception:
                latest_net = 0.0
            family_all.append({"model": model, "product": product, "series": series, "latest_net": latest_net})

    family_all.sort(key=lambda x: x.get("latest_net", 0.0), reverse=True)
    family = family_all[:max(1, max_card_strategies)]

    return {
        "best": best,
        "base": _parse_model_signature(best["model"])[0],
        "sig": sig,
        "family": family
    }


def _optimize_start_from_for_range(family: List[dict], target_max: float) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Step 3 optimizer:
    choose earliest start_dt where max(current_net - start_net) across family <= target_max.
    Returns (start_dt, eval_dt).
    """
    timestamps = []
    for item in family:
        for p in item.get("series", []):
            ts = p.get("t")
            if not ts:
                continue
            try:
                timestamps.append(datetime.fromisoformat(str(ts).replace("Z", "")))
            except Exception:
                pass
    if not timestamps:
        return None, None

    timestamps = sorted(set(timestamps))
    eval_dt = timestamps[-1]

    def max_range_from(start_dt: datetime) -> float:
        max_delta = 0.0
        for item in family:
            series = item.get("series", [])
            start_net = _series_value_at_or_before(series, start_dt)
            end_net = _series_value_at_or_before(series, eval_dt)
            d = end_net - start_net
            if d > max_delta:
                max_delta = d
        return max_delta

    chosen = None
    for t in timestamps:
        if max_range_from(t) <= float(target_max):
            chosen = t
            break
    if chosen is None:
        # fallback to latest timestamp; yields smallest range.
        chosen = eval_dt
    return chosen, eval_dt


def _run_tb_workflow_once(mode: str, date_str: str, wf: dict) -> dict:
    """
    Execute TB_workflow:
    1) choose best summary row
    2) add all same-parameter strategies
    3) optimize start-from range <= target
    4) save+activate TB
    """
    cfg = wf.get("config", {}) if isinstance(wf, dict) else {}
    target_max = float(cfg.get("max_range_target", 150) or 150)
    min_diff = float(cfg.get("minimum_difference", 5.0) or 5.0)

    selected = _select_tb_workflow_candidate(mode, date_str, cfg)
    if not selected:
        return {"success": False, "message": "No summary candidate found"}
    bias_at_creation = _get_current_bias(mode, date_str) or "UNKNOWN"

    family = selected["family"]
    if not family:
        return {"success": False, "message": "No same-parameter family found"}

    start_from_dt, eval_dt = _optimize_start_from_for_range(family, target_max)
    if not start_from_dt or not eval_dt:
        return {"success": False, "message": "No usable timeline points"}

    now = datetime.now()
    mmdd = now.strftime("%m%d")
    hhmmss_mmm = now.strftime("%H%M%S") + f"_{int(now.microsecond/1000):03d}"
    base = selected.get("base") or "model"
    sig = selected.get("sig") or "default"
    product = str(selected.get("best", {}).get("product") or "MIX").upper()
    bucket_name = f"AUTO_TB_{mmdd}_{hhmmss_mmm}_{product}_{base}_{sig}".replace(" ", "")

    data = _load_trade_buckets(mode=mode, date_str=date_str)
    buckets = data.get("buckets", [])
    if any(str(b.get("name")) == bucket_name for b in buckets):
        return {"success": False, "message": "Bucket already exists"}

    processed_strategies = []
    # [V20260311_1215] If family has only 1 strategy, split into Buy and Sell to satisfy "no single row" rule.
    if len(family) == 1:
        item = family[0]
        model = str(item.get("model") or "").strip()
        product = str(item.get("product") or "").strip()
        series = item.get("series") or []
        
        for m_type, m_field in [("buy_net", "buy_net"), ("sell_net", "sell_net")]:
            creation_net = round(_series_value_at_or_before(series, eval_dt, field=m_field), 2)
            start_from_net = round(_series_value_at_or_before(series, start_from_dt, field=m_field), 2)
            processed_strategies.append({
                "strategy_id": str(uuid.uuid4()),
                "key": f"{model} | {product}",
                "metric": m_type,
                "bias_at_creation": bias_at_creation,
                "start_from_net": start_from_net,
                "net_at_creation": creation_net,
                "current_total_net": creation_net,
                "start_net_delta_from_chart": round(creation_net - start_from_net, 2),
                "current_net_from_chart": round(creation_net - start_from_net, 2),
                "net_delta_from_creation": 0.0,
                "total_net": 0.0,
                "live_trade_net": 0.0
            })
    else:
        for item in family:
            model = str(item.get("model") or "").strip()
            product = str(item.get("product") or "").strip()
            series = item.get("series") or []
            if not model or not product:
                continue
            creation_net = round(_series_value_at_or_before(series, eval_dt), 2)
            start_from_net = round(_series_value_at_or_before(series, start_from_dt), 2)
            processed_strategies.append({
                "strategy_id": str(uuid.uuid4()),
                "key": f"{model} | {product}",
                "metric": "net",
                "bias_at_creation": bias_at_creation,
                "start_from_net": start_from_net,
                "net_at_creation": creation_net,
                "current_total_net": creation_net,
                "start_net_delta_from_chart": round(creation_net - start_from_net, 2),
                "current_net_from_chart": round(creation_net - start_from_net, 2),
                "net_delta_from_creation": 0.0,
                "total_net": 0.0,
                "live_trade_net": 0.0
            })

    # [V20260311_1345] Deduplicate by strategy+product+metric to ensure real diversity
    seen_strategies = set()
    deduped_strategies = []
    for s in processed_strategies:
        d_key = f"{s.get('key')}|{s.get('metric')}"
        if d_key not in seen_strategies:
            seen_strategies.add(d_key)
            deduped_strategies.append(s)
    processed_strategies = deduped_strategies

    if len(processed_strategies) < 2:
        # If we still have only 1 after dedup, force a Buy/Sell split if it was 'net' [V20260311_1345]
        if len(processed_strategies) == 1 and processed_strategies[0]['metric'] == 'net':
            s = processed_strategies[0]
            processed_strategies = []
            model_key = s.get('key')
            parts = model_key.split(' | ')
            if len(parts) == 2:
                model_name, product_name = parts[0].strip(), parts[1].strip()
                series = summary_data.get("strategies", {}).get(model_name, {}).get(product_name, [])
                for m_type in ("buy_net", "sell_net"):
                    c_net = round(_series_value_at_or_before(series, eval_dt, field=m_type), 2)
                    s_net = round(_series_value_at_or_before(series, start_from_dt, field=m_type), 2)
                    processed_strategies.append({
                        "strategy_id": str(uuid.uuid4()),
                        "key": model_key,
                        "metric": m_type,
                        "bias_at_creation": bias_at_creation,
                        "start_from_net": s_net,
                        "net_at_creation": c_net,
                        "current_total_net": c_net,
                        "start_net_delta_from_chart": round(c_net - s_net, 2),
                        "current_net_from_chart": round(c_net - s_net, 2),
                        "net_delta_from_creation": 0.0,
                        "total_net": 0.0,
                        "live_trade_net": 0.0
                    })

    if len(processed_strategies) < 2:
        return {"success": False, "message": "Minimum 2 unique strategies/metrics required for a Trade Bucket [V20260311_1345]"}

    new_bucket = {
        "bucket_id": str(uuid.uuid4()),
        "name": bucket_name,
        "start_time": now.isoformat(),
        "chart_start_time": start_from_dt.isoformat(),
        "mode": mode,
        "market_bias_at_creation": bias_at_creation,
        "strategies": processed_strategies,
        "live": True,
        "open_trades": False,
        "open_trade_count": 0,
        "minimum_difference": float(min_diff),
        "created_by_workflow": "TB_workflow"
    }

    buckets.append(new_bucket)
    data["buckets"] = buckets
    _save_trade_buckets(data, mode=mode, date_str=date_str)

    # activate into grid
    _sync_bucket_to_grid_live(new_bucket, mode, date_str)
    _update_automated_source("Trade Bucket")

    return {
        "success": True,
        "bucket_name": bucket_name,
        "family_size": len(processed_strategies),
        "selected_model": selected.get("best", {}).get("model"),
        "selected_product": selected.get("best", {}).get("product"),
        "start_from_time": start_from_dt.isoformat(),
        "created_time": eval_dt.isoformat()
    }


def _run_profile_match_workflow_once(mode: str, date_str: str, wf: dict) -> dict:
    cfg = wf.get("config", {}) if isinstance(wf, dict) else {}
    product_type = str(cfg.get("product_type") or "").strip().lower() or None
    delta_type = _normalize_delta_type(cfg.get("delta_type"))
    min_profitability = float(cfg.get("min_profitability_pct", 85.0) or 85.0)
    min_trade_count = int(cfg.get("min_trade_count", 10) or 10)
    min_total_net = float(cfg.get("min_total_net", 0.0) or 0.0)
    min_avg_net = float(cfg.get("min_avg_net", 0.0) or 0.0)
    max_items = int(cfg.get("max_items", 20) or 20)
    metric_cfg = str(cfg.get("metric", "net") or "net").lower()
    scalper_only = bool(cfg.get("scalper_only", False))
    rev_scalper_only = bool(cfg.get("rev_scalper_only", False))
    enforce_market_bias = bool(cfg.get("enforce_market_bias", False))
    try:
        bias_recent_profitable_count = int(cfg.get("bias_recent_profitable_count", 2) or 2)
    except Exception:
        bias_recent_profitable_count = 2
    bias_recent_profitable_count = max(1, bias_recent_profitable_count)
    add_to_tb = bool(cfg.get("add_to_tb", False))
    add_same_parameter = bool(cfg.get("add_same_parameter_strategies_metrics", False))
    adjust_start_time_under_150 = bool(cfg.get("adjust_start_time_under_150", False))
    current_bias = str(_get_current_bias(mode, date_str) or "").upper()

    trades_summary_rows: List[dict] = []
    # [V20260317_1105] Multi-dir support via product_type
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        summary_file = day_dir / "_trades_summary.json"
        if summary_file.exists():
            try:
                with open(summary_file, "r") as f:
                    d = json.load(f) or {}
                rows = d.get("trades", [])
                if isinstance(rows, list):
                    trades_summary_rows.extend([r for r in rows if isinstance(r, dict)])
            except Exception:
                pass

    def _passes_bias_recent_two_profitable(model_name: str, product_name: str) -> bool:
        if not enforce_market_bias:
            return True
        if current_bias not in ("BUY", "SELL"):
            return False
        side = "LONG" if current_bias == "BUY" else "SHORT"
        candidates_rows = []
        for t in trades_summary_rows:
            app = str(t.get("app_name") or t.get("script_name") or "").strip()
            prod = str(t.get("product") or "").strip().upper()
            if app != str(model_name).strip() or prod != str(product_name).strip().upper():
                continue
            if str(t.get("status") or "").upper() != "CLOSED":
                continue
            d = str(t.get("direction") or "").upper()
            if side == "LONG" and "LONG" not in d:
                continue
            if side == "SHORT" and "SHORT" not in d:
                continue
            candidates_rows.append(t)
        if len(candidates_rows) < bias_recent_profitable_count:
            return False
        candidates_rows.sort(key=lambda x: str(x.get("entry_time") or x.get("exit_time") or ""), reverse=True)
        last_n = candidates_rows[:bias_recent_profitable_count]
        return all(float(r.get("net_return", 0.0) or 0.0) > 0 for r in last_n)

    scalper_models: Set[str] = set()

    # [V20260317_1105] Load scalper status from targeted strategies (multi-dir)
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        targeted_file = day_dir / "_targeted_strategies.json"
        if targeted_file.exists():
            try:
                with open(targeted_file, "r") as f:
                    targeted = json.load(f) or {}
                for s in (targeted.get("strategies") or []):
                    if isinstance(s, dict) and bool(s.get("scalper")):
                        model = str(s.get("strategy") or "").strip()
                        if model:
                            scalper_models.add(model)
            except Exception:
                pass

    _sr = 5.0
    _rsr = 2.0
    _cfg_path = BASE_PATH / "config.json"
    if _cfg_path.exists():
        try:
            with open(_cfg_path, "r") as f:
                _c = json.load(f)
                _sr = float(_c.get("scalper_ratio", 5.0))
                _rsr = float(_c.get("rev_scalper_ratio", 2.0))
        except: pass

    def _looks_like_scalper(model_name: str) -> bool:
        s = str(model_name or "").lower()
        tp_match = re.search(r'tp([\d.]+)', s)
        sl_match = re.search(r'sl([\d.]+)', s)
        if tp_match and sl_match:
            try:
                tp_val = float(tp_match.group(1))
                sl_val = float(sl_match.group(1))
                if tp_val > 0 and sl_val >= tp_val * _sr:
                    return True
            except: pass
        return ("scalp" in s) or ("_s_" in s) or s.endswith("_s")

    def _looks_like_rev_scalper(model_name: str) -> bool:
        s = str(model_name or "").lower()
        tp_match = re.search(r'tp([\d.]+)', s)
        sl_match = re.search(r'sl([\d.]+)', s)
        if tp_match and sl_match:
            try:
                tp_val = float(tp_match.group(1))
                sl_val = float(sl_match.group(1))
                if sl_val > 0 and tp_val >= sl_val * _rsr:
                    return True
            except: pass
        return False

    # [V20260317_1105] Multi-dir top20 load
    top20_rows = []
    for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
        top20_file = day_dir / "_top20.json"
        if top20_file.exists():
            try:
                with open(top20_file, "r") as f:
                    batch = (json.load(f) or {}).get("top20", [])
                    if isinstance(batch, list):
                        top20_rows.extend(batch)
            except Exception:
                pass

    if not top20_rows:
        return {"success": False, "message": f"top20 data not found for {product_type or 'all'}"}

    candidates = []
    seen = set()
    for r in top20_rows:
        if not isinstance(r, dict):
            continue
        model = str(r.get("strategy") or "").strip()
        product = str(r.get("product") or "").strip().upper()
        if not model or not product:
            continue
        if scalper_only and rev_scalper_only:
            is_scalper = (model in scalper_models) or _looks_like_scalper(model)
            is_rev = _looks_like_rev_scalper(model)
            if not is_scalper and not is_rev:
                continue
        elif scalper_only:
            is_scalper = (model in scalper_models) or _looks_like_scalper(model)
            if not is_scalper:
                continue
        elif rev_scalper_only:
            is_rev = _looks_like_rev_scalper(model)
            if not is_rev:
                continue
        key = (model, product)
        if key in seen:
            continue
        seen.add(key)

        buy_count = int(r.get("buy_count", 0) or 0)
        sell_count = int(r.get("sell_count", 0) or 0)
        trade_count = int(r.get("trade_count", buy_count + sell_count) or 0)
        if trade_count < min_trade_count:
            continue

        buy_pct = float(r.get("buyPercent", 0.0) or 0.0)
        sell_pct = float(r.get("sellPercent", 0.0) or 0.0)
        denom = max(1, buy_count + sell_count)
        profitability = ((buy_pct * buy_count) + (sell_pct * sell_count)) / denom
        if profitability < min_profitability:
            continue

        total_net = float(r.get("total_net", 0.0) or 0.0)
        if total_net <= 0:
            continue
        if total_net < min_total_net:
            continue
        avg_net = float(r.get("avg_net", 0.0) or 0.0)
        if avg_net == 0.0:
            avg_net = (total_net / trade_count) if trade_count > 0 else 0.0
        if avg_net < min_avg_net:
            continue
        if not _passes_bias_recent_two_profitable(model, product):
            continue
        candidates.append({
            "model": model,
            "product": product,
            "trade_count": trade_count,
            "profitability": profitability,
            "total_net": total_net,
            "avg_net": avg_net
        })

    if not candidates:
        return {"success": False, "message": "no strategies matched threshold"}

    candidates.sort(key=lambda x: (x["profitability"], x["total_net"], x["trade_count"]), reverse=True)
    picked = candidates[:max(1, max_items)]

    summary_strategies: Dict[str, Dict[str, List[dict]]] = {}
    summary_net_file = _resolve_day_dir(mode, date_str) / "_summary_net.json"
    if summary_net_file.exists():
        try:
            with open(summary_net_file, "r") as f:
                summary_strategies = (json.load(f) or {}).get("strategies", {}) or {}
        except Exception:
            summary_strategies = {}

    def _series_for(model_name: str, product_name: str) -> List[dict]:
        try:
            products = summary_strategies.get(str(model_name), {})
            if isinstance(products, dict):
                series = products.get(str(product_name))
                if isinstance(series, list):
                    return series
        except Exception:
            pass
        return []

    def _family_for_same_param(model_name: str, product_name: str) -> List[dict]:
        _, sig = _parse_model_signature(model_name)
        product_scope = str(product_name).upper()
        out = []
        for model, products in summary_strategies.items():
            if not isinstance(products, dict):
                continue
            _, model_sig = _parse_model_signature(str(model))
            if model_sig != sig:
                continue
            for product, series in products.items():
                if str(product).upper() != product_scope:
                    continue
                if not isinstance(series, list) or not series:
                    continue
                try:
                    latest_net = float(series[-1].get("net", 0.0) or 0.0)
                except Exception:
                    latest_net = 0.0
                out.append({
                    "model": str(model),
                    "product": str(product).upper(),
                    "series": series,
                    "latest_net": latest_net
                })
        out.sort(key=lambda x: x.get("latest_net", 0.0), reverse=True)
        return out

    if metric_cfg == "bias_side":
        bias = str(_get_current_bias(mode, date_str) or "").upper()
        metric = "buy_net" if bias == "BUY" else ("sell_net" if bias == "SELL" else "net")
    else:
        metric = metric_cfg if metric_cfg in ("net", "buy_net", "sell_net") else "net"

    now_dt = datetime.now()
    now_local = now_dt.isoformat().split(".")[0]
    hhmmss = now_dt.strftime("%H%M%S")
    group_name = f"WF_PROFILE_{date_str}_{int(min_profitability)}_{hhmmss}"
    payload_items = []
    payload_seen: Set[str] = set()
    for item in picked:
        model = str(item["model"])
        product = str(item["product"]).upper()
        if add_same_parameter:
            expanded = _family_for_same_param(model, product)
            if not expanded:
                expanded = [{"model": model, "product": product, "series": _series_for(model, product)}]
        else:
            expanded = [{"model": model, "product": product, "series": _series_for(model, product)}]

        for m in expanded:
            m_model = str(m.get("model") or "").strip()
            m_product = str(m.get("product") or "").strip().upper()
            if not m_model or not m_product:
                continue
            # Enforce net filters for expanded family members too.
            # This prevents negative/low-net same-parameter members from being pushed to multi_chart.
            m_latest_net = None
            try:
                if isinstance(m.get("series"), list) and m.get("series"):
                    m_latest_net = float(m["series"][-1].get("net", 0.0) or 0.0)
                else:
                    m_latest_net = float(m.get("latest_net", 0.0) or 0.0)
            except Exception:
                m_latest_net = 0.0
            if m_latest_net <= 0:
                continue
            if m_latest_net < min_total_net:
                continue
            dedup_key = f"{m_model}|{m_product}".lower()
            if dedup_key in payload_seen:
                continue
            payload_seen.add(dedup_key)

            safe_model = re.sub(r'[^A-Za-z0-9_]+', '_', m_model).strip('_')
            safe_product = re.sub(r'[^A-Za-z0-9_]+', '_', m_product).strip('_')
            per_card_group = f"{group_name}_{safe_product}_{safe_model}"
            payload_items.append({
                "strategy": m_model,
                "product": m_product,
                "group": per_card_group,
                "parm_raw": ""
            })

    payload = {
        "source": "profile_match_workflow",
        "mode": mode,
        "date": date_str,
        "preferred_metric": metric,
        "delta_type": delta_type,
        "group": group_name,
        "preset_name": group_name,
        "created_at": now_local,
        "run_id": f"{mode}_{date_str}_{int(time.time())}",
        "items": payload_items
    }
    try:
        with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "w") as f:
            json.dump(payload, f, indent=4)
    except Exception as e:
        return {"success": False, "message": f"failed to write multi-chart payload: {e}"}

    tb_result = {
        "requested": add_to_tb,
        "created": False,
        "activated": False,
        "reason": "not_requested"
    }
    if add_to_tb and picked:
        max_live_tb = _get_max_live_tb()
        tb_data = _load_trade_buckets(mode=mode, date_str=date_str)
        tb_buckets = tb_data.get("buckets", [])
        def _norm_key(model_name: str, product_name: str) -> str:
            m = str(model_name or "").strip().lower()
            p = str(product_name or "").strip().upper()
            return f"{m}|{p}"

        existing_keys: Set[str] = set()
        for b in tb_buckets:
            if not isinstance(b, dict):
                continue
            for s in (b.get("strategies") or []):
                if not isinstance(s, dict):
                    continue
                key_raw = str(s.get("key") or "")
                parts = key_raw.split(" | ") if " | " in key_raw else key_raw.split("|")
                if len(parts) == 2:
                    existing_keys.add(_norm_key(parts[0], parts[1]))
        live_count = sum(1 for b in tb_buckets if isinstance(b, dict) and bool(b.get("live")))
        if live_count >= max_live_tb:
            tb_result = {
                "requested": True,
                "created": False,
                "activated": False,
                "reason": f"max_live_tb_reached ({live_count}/{max_live_tb})"
            }
        else:
            tb_results_list = []
            
            for candidate in picked:
                if live_count >= max_live_tb:
                    tb_results_list.append({"requested": True, "created": False, "reason": f"max_live_tb_reached ({live_count}/{max_live_tb})"})
                    break
                    
                c_model = str(candidate.get("model") or "")
                c_prod = str(candidate.get("product") or "").upper()
                if _norm_key(c_model, c_prod) in existing_keys:
                    tb_results_list.append({"requested": True, "created": False, "reason": "already_exists"})
                    continue
                    
                if add_same_parameter:
                    c_family = _family_for_same_param(c_model, c_prod)
                else:
                    c_family = [{
                        "model": c_model, 
                        "product": c_prod, 
                        "series": candidate.get("series", []),
                        "latest_net": float(candidate.get("latest_net", 0.0) or 0.0)
                    }]
                
                if len(c_family) >= 1:
                    pre_tb_family = c_family
                    best_model = c_model
                    best_product = c_prod

                    now_dt = datetime.now()
                    mmdd = now_dt.strftime("%m%d")
                    hhmmss_mmm = now_dt.strftime("%H%M%S") + f"_{int(now_dt.microsecond/1000):03d}"
                    safe_product = re.sub(r'[^A-Za-z0-9_]+', '_', best_product).strip('_').upper()
                    safe_model = re.sub(r'[^A-Za-z0-9_]+', '_', best_model).strip('_')
                    bucket_name = f"AUTO_TB_{mmdd}_{hhmmss_mmm}_{safe_product}_{safe_model}".replace(" ", "")
                    bias_at_creation = _get_current_bias(mode, date_str) or "UNKNOWN"
                    total_net = round(float(candidate.get("total_net", 0.0) or 0.0), 2)
                    min_diff = float(cfg.get("minimum_difference", 5.0) or 5.0)
                    requested_metric = str(cfg.get("metric", "net") or "net").strip()

                    start_from_dt = now_dt
                    eval_dt = now_dt
                    if adjust_start_time_under_150:
                        family_with_series = [f for f in pre_tb_family if isinstance(f.get("series"), list) and f.get("series")]
                        if family_with_series:
                            s_dt, e_dt = _optimize_start_from_for_range(family_with_series, 150.0)
                            if s_dt and e_dt:
                                start_from_dt = s_dt
                                eval_dt = e_dt

                    processed_strategies = []
                    # [V20260311_1215] Forced split for single-strategy family OR buy_sell metric
                    should_split = (len(pre_tb_family) == 1) or (requested_metric == "buy_sell")

                    for fam in pre_tb_family:
                        fm = str(fam.get("model") or "").strip()
                        fp = str(fam.get("product") or "").strip().upper()
                        if not fm or not fp:
                            continue

                        series = fam.get("series") if isinstance(fam.get("series"), list) else []
                        
                        # [V20260323_1510] Filter expansion members for positive net in TB
                        f_latest_net = float(fam.get("latest_net", 0.0) or 0.0)
                        if f_latest_net <= 0:
                            continue
                        if bool(cfg.get("require_positive_total_net", True)):
                            try:
                                f_total_net = float(series[-1].get("net", 0.0) or 0.0) if series else f_latest_net
                            except: f_total_net = f_latest_net
                            if f_total_net <= 0:
                                continue
                        
                        metrics_to_add = [("buy_net", "buy_net"), ("sell_net", "sell_net")] if should_split else [("net", "net")]
                        
                        for m_type, m_field in metrics_to_add:
                            if series and adjust_start_time_under_150:
                                creation_net = round(_series_value_at_or_before(series, eval_dt, field=m_field), 2)
                                start_from_net = round(_series_value_at_or_before(series, start_from_dt, field=m_field), 2)
                            else:
                                creation_net = round(float(fam.get("latest_net", total_net) or 0.0), 2)
                                start_from_net = creation_net

                            processed_strategies.append({
                                "strategy_id": str(uuid.uuid4()),
                                "key": f"{fm} | {fp}",
                                "metric": m_type,
                                "bias_at_creation": bias_at_creation,
                                "start_from_net": start_from_net,
                                "net_at_creation": creation_net,
                                "current_total_net": creation_net,
                                "start_net_delta_from_chart": round(creation_net - start_from_net, 2),
                                "current_net_from_chart": round(creation_net - start_from_net, 2),
                                "net_delta_from_creation": 0.0,
                                "total_net": 0.0,
                                "delta_type": delta_type,
                                "live_trade_net": 0.0
                            })
                    
                    if len(processed_strategies) < 2:
                        tb_results_list.append({"requested": True, "created": False, "reason": "min_rows_violation_len1_no_split"})
                        continue

                    new_bucket = {
                        "bucket_id": str(uuid.uuid4()),
                        "name": bucket_name,
                        "date": date_str,
                        "mode": mode,
                        "market_bias_at_creation": bias_at_creation,
                        "metric": cfg.get("metric", "net"),
                        "delta_type": delta_type,
                        "chart_start_time": start_from_dt.isoformat(),
                        "start_time": eval_dt.isoformat(),
                        "strategies": processed_strategies,
                        "live": True,
                        "open_trades": False,
                        "open_trade_count": 0,
                        "minimum_difference": float(min_diff),
                        "created_by_workflow": "profile_match_workflow"
                    }

                    tb_buckets.append(new_bucket)
                    existing_keys.add(_norm_key(best_model, best_product))
                    live_count += 1
                    
                    _sync_bucket_to_grid_live(new_bucket, mode, date_str)

                    tb_results_list.append({
                        "requested": True,
                        "created": True,
                        "activated": True,
                        "bucket_name": bucket_name,
                        "family_size": len(processed_strategies),
                        "reason": "success"
                    })
                else:
                    tb_results_list.append({"requested": True, "created": False, "reason": "no_candidate_found_for_tb"})

            if any(r.get("created") for r in tb_results_list):
                tb_data["buckets"] = tb_buckets
                _save_trade_buckets(tb_data, mode=mode, date_str=date_str)
                _update_automated_source("Trade Bucket")
                tb_result = {
                    "requested": True,
                    "created": True,
                    "activated": True,
                    "reason": "ok",
                    "bucket_name": bucket_name
                }

    return {
        "success": True,
        "matched": len(candidates),
        "pushed": len(payload_items),
        "metric": metric,
        "group": group_name,
        "scalper_only": scalper_only,
        "rev_scalper_only": rev_scalper_only,
        "enforce_market_bias": enforce_market_bias,
        "bias_recent_profitable_count": bias_recent_profitable_count,
        "min_total_net": min_total_net,
        "min_avg_net": min_avg_net,
        "add_same_parameter_strategies_metrics": add_same_parameter,
        "adjust_start_time_under_150": adjust_start_time_under_150,
        "delta_type": delta_type,
        "target": "multi_chart_payload",
        "tb": tb_result
    }

def _run_top_x_multi_chart_workflow(mode: str, date_str: str, wf: dict) -> dict:
    cfg = wf.get("config", {}) if isinstance(wf, dict) else {}
    product_type = str(cfg.get("product_type") or "").strip().lower() or None
    delta_type = _normalize_delta_type(cfg.get("delta_type"))
    top_x = int(cfg.get("top_x", 6) or 6)
    include_scalper = bool(cfg.get("include_scalper", True))
    include_rev_scalper = bool(cfg.get("include_rev_scalper", True))
    add_to_tb = bool(cfg.get("add_to_tb", False))
    t_split_for_tb = bool(cfg.get("t_split_for_tb", False))
    add_same_parameter = bool(cfg.get("add_same_parameter_strategies_metrics", False))
    # [V20260306_1845] Metric type selector: net, buy_net, sell_net, buy_sell
    selected_metric = str(cfg.get("metric", "net") or "net").strip()
    # Map metric to the _top20.json field name used for sorting
    _METRIC_SORT_FIELD = {
        "net": "total_net",
        "buy_net": "buy_net",
        "sell_net": "sell_net",
        "buy_sell": "total_net"  # buy_sell sorts by total_net but displays both
    }
    sort_field = _METRIC_SORT_FIELD.get(selected_metric, "total_net")
    # Map metric to _summary_net.json series field name
    _METRIC_SERIES_FIELD = {
        "net": "net",
        "buy_net": "buy_net",
        "sell_net": "sell_net",
        "buy_sell": "net"
    }
    series_net_field = _METRIC_SERIES_FIELD.get(selected_metric, "net")

    summary_strategies: Dict[str, Dict[str, List[dict]]] = {}
    if add_same_parameter or add_to_tb:
        for summary_net_file in [day_dir / "_summary_net.json" for day_dir in _iter_day_dirs_for(mode, date_str, product_type)]:
            if not summary_net_file.exists():
                continue
            try:
                with open(summary_net_file, "r") as f:
                    loaded_strategies = (json.load(f) or {}).get("strategies", {}) or {}
                if not isinstance(loaded_strategies, dict):
                    continue
                for model_name, products in loaded_strategies.items():
                    if not isinstance(products, dict):
                        continue
                    model_bucket = summary_strategies.setdefault(str(model_name), {})
                    for product_name, series in products.items():
                        if isinstance(series, list):
                            model_bucket[str(product_name)] = series
            except Exception:
                continue

    def _series_for(model_name: str, product_name: str) -> List[dict]:
        try:
            products = summary_strategies.get(str(model_name), {})
            if isinstance(products, dict):
                series = products.get(str(product_name))
                if isinstance(series, list):
                    return series
        except Exception:
            pass
        return []

    def _family_for_same_param(model_name: str, product_name: str) -> List[dict]:
        _, sig = _parse_model_signature(model_name)
        product_scope = str(product_name).upper()
        out = []
        for model_k, products in summary_strategies.items():
            if not isinstance(products, dict):
                continue
            _, model_sig = _parse_model_signature(str(model_k))
            if model_sig != sig:
                continue
            for prod_k, series in products.items():
                if str(prod_k).upper() != product_scope:
                    continue
                if not isinstance(series, list) or not series:
                    continue
                try:
                    # [V20260306_1845] Use selected metric field for family net value
                    latest_net = float(series[-1].get(series_net_field, 0.0) or 0.0)
                except Exception:
                    latest_net = 0.0
                out.append({
                    "model": str(model_k),
                    "product": str(prod_k).upper(),
                    "series": series,
                    "latest_net": latest_net
                })
        out.sort(key=lambda x: x.get("latest_net", 0.0), reverse=True)
        return out

    try:
        top_20: List[dict] = []
        for top20_file in [day_dir / "_top20.json" for day_dir in _iter_day_dirs_for(mode, date_str, product_type)]:
            if not top20_file.exists():
                continue
            with open(top20_file, "r") as f:
                top_20.extend((json.load(f) or {}).get("top20", []))

        if not top_20:
            return {"success": False, "message": "top20 file not found."}

        if not top_20 or not isinstance(top_20, list):
            return {"success": False, "message": "Failed to retrieve top 20 or list empty."}

        _sr = 5.0
        _rsr = 2.0
        _cfg_path = CONFIG_FILE
        if _cfg_path.exists():
            try:
                with open(_cfg_path, "r") as f:
                    _c = json.load(f)
                    _sr = float(_c.get("scalper_ratio", 5.0))
                    _rsr = float(_c.get("rev_scalper_ratio", 2.0))
            except: pass

        filtered = []
        for entry in top_20:
            strat_name = entry.get("strategy", "")
            if not strat_name:
                continue
            
            m = re.search(r'tp([\d.]+)_sl([\d.]+)', strat_name, re.IGNORECASE)
            is_scalper = ("scalp" in strat_name.lower()) or ("_s_" in strat_name.lower()) or strat_name.lower().endswith("_s")
            is_rev_scalper = False
            
            if m:
                tp = float(m.group(1))
                sl = float(m.group(2))
                if tp > 0 and sl >= tp * _sr:
                    is_scalper = True
                if sl > 0 and tp >= sl * _rsr:
                    is_rev_scalper = True
            
            should_include = False
            if not include_scalper and not include_rev_scalper:
                should_include = True
            else:
                if include_scalper and is_scalper:
                    should_include = True
                if include_rev_scalper and is_rev_scalper:
                    should_include = True
                
            if should_include:
                # [V20260312_1410] Ensure positive net for the selected sort metric
                metric_value = float(entry.get(sort_field, 0.0) or 0.0)
                if metric_value > 0:
                    # [V20260323_1500] Enforce total_net > 0 if explicitly requested in config
                    if bool(cfg.get("require_positive_total_net", True)):
                        if float(entry.get("total_net", 0.0) or 0.0) <= 0:
                            continue
                    
                    # [V20260324_1500] Require proven persistence parameter
                    if not entry.get("pick_now", False):
                        continue
                        
                    filtered.append(entry)

        # [V20260306_1845] Sort by selected metric field instead of hardcoded total_net
        filtered.sort(key=lambda x: float(x.get(sort_field, 0.0) or 0.0), reverse=True)
        sliced = filtered[:top_x]
        
        now_local = datetime.now().isoformat()
        payload_items = []
        payload_seen: Set[str] = set()
        group_name = f"WF_TOPX_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        for entry in sliced:
            m_model = str(entry.get("strategy", "")).strip()
            m_product = str(entry.get("product", "")).strip().upper()
            
            m_latest_net_from_top20 = float(entry.get(sort_field, 0.0) or 0.0)
            if add_same_parameter:
                expanded = _family_for_same_param(m_model, m_product)
                if not expanded:
                    expanded = [{"model": m_model, "product": m_product, "series": _series_for(m_model, m_product), "latest_net": m_latest_net_from_top20}]
            else:
                expanded = [{"model": m_model, "product": m_product, "series": _series_for(m_model, m_product), "latest_net": m_latest_net_from_top20}]
            
            for m in expanded:
                ex_model = str(m.get("model") or "").strip()
                ex_product = str(m.get("product") or "").strip().upper()
                if not ex_model or not ex_product:
                    continue

                # [V20260323_1510] Filter expansion members for positive net
                m_latest_net = float(m.get("latest_net", 0.0) or 0.0)
                if m_latest_net <= 0:
                    continue
                # Also check total_net if configured
                if bool(cfg.get("require_positive_total_net", True)):
                    try:
                        m_series = m.get("series") or []
                        m_total_net = float(m_series[-1].get("net", 0.0) or 0.0) if m_series else m_latest_net
                    except: m_total_net = m_latest_net
                    if m_total_net <= 0:
                        continue
                        
                dedup_key = f"{ex_model}|{ex_product}".lower()
                if dedup_key in payload_seen:
                    continue
                payload_seen.add(dedup_key)

                safe_model = re.sub(r'[^A-Za-z0-9_]+', '_', ex_model).strip('_')
                safe_product = re.sub(r'[^A-Za-z0-9_]+', '_', ex_product).strip('_')
                per_card_group = f"{group_name}_{safe_product}_{safe_model}"
                
                # [V20260306_1845] For buy_sell, create two overlay entries (buy_net + sell_net)
                if selected_metric == "buy_sell":
                    payload_items.append({
                        "strategy": ex_model,
                        "product": ex_product,
                        "group": per_card_group,
                        "metric": "buy_net",
                        "parm_raw": ""
                    })
                    payload_items.append({
                        "strategy": ex_model,
                        "product": ex_product,
                        "group": per_card_group,
                        "metric": "sell_net",
                        "parm_raw": ""
                    })
                else:
                    payload_items.append({
                        "strategy": ex_model,
                        "product": ex_product,
                        "group": per_card_group,
                        "metric": selected_metric if selected_metric != "net" else None,
                        "parm_raw": ""
                    })

        payload = {
            "source": "top_x_multi_chart_workflow",
            "mode": mode,
            "date": date_str,
            "preferred_metric": selected_metric,  # [V20260306_1845] Use selected metric type
            "delta_type": delta_type,
            "group": group_name,
            "preset_name": group_name,
            "created_at": now_local,
            "run_id": f"{mode}_{date_str}_{int(time.time())}_top_x",
            "items": payload_items
        }

        try:
            with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "w") as f:
                json.dump(payload, f, indent=4)
        except Exception as e:
            return {"success": False, "message": f"failed to write multi-chart payload: {e}"}

        tb_result = {
            "requested": add_to_tb,
            "created": False,
            "activated": False,
            "reason": "not_requested"
        }

        if add_to_tb and sliced:
            max_live_tb = _get_max_live_tb()
            tb_data = _load_trade_buckets(mode=mode, date_str=date_str)
            tb_buckets = tb_data.get("buckets", [])
            def _norm_key(model_name: str, product_name: str) -> str:
                m_str = str(model_name or "").strip().lower()
                p_str = str(product_name or "").strip().upper()
                return f"{m_str}|{p_str}"

            existing_keys: Set[str] = set()
            for b in tb_buckets:
                if not isinstance(b, dict):
                    continue
                for s in (b.get("strategies") or []):
                    if not isinstance(s, dict):
                        continue
                    key_raw = str(s.get("key") or "")
                    parts = key_raw.split(" | ") if " | " in key_raw else key_raw.split("|")
                    if len(parts) == 2:
                        existing_keys.add(_norm_key(parts[0], parts[1]))

            live_count = sum(1 for b in tb_buckets if isinstance(b, dict) and bool(b.get("live")))
            if live_count >= max_live_tb:
                tb_result = {
                    "requested": True,
                    "created": False,
                    "activated": False,
                    "reason": f"max_live_tb_reached ({live_count}/{max_live_tb})"
                }
            else:
                tb_results_list = []
                
                for candidate in sliced:
                    if live_count >= max_live_tb:
                        tb_results_list.append({"requested": True, "created": False, "reason": f"max_live_tb_reached ({live_count}/{max_live_tb})"})
                        break
                        
                    c_model = str(candidate.get("strategy") or "")
                    c_prod = str(candidate.get("product") or "").upper()
                    if _norm_key(c_model, c_prod) in existing_keys:
                        tb_results_list.append({"requested": True, "created": False, "reason": "already_exists"})
                        continue
                        
                    if add_same_parameter:
                        c_family = _family_for_same_param(c_model, c_prod)
                    else:
                        c_family = [{
                            "model": c_model, 
                            "product": c_prod, 
                            "series": _series_for(c_model, c_prod),
                            "latest_net": float(candidate.get(sort_field, 0.0) or 0.0)
                        }]
                    
                    if len(c_family) >= 1:
                        pre_tb_family = c_family
                        best_model = c_model
                        best_product = c_prod

                        now_dt = datetime.now()
                        mmdd = now_dt.strftime("%m%d")
                        hhmmss_mmm = now_dt.strftime("%H%M%S") + f"_{int(now_dt.microsecond/1000):03d}"
                        safe_product_tb = re.sub(r'[^A-Za-z0-9_]+', '_', best_product).strip('_').upper()
                        safe_model_tb = re.sub(r'[^A-Za-z0-9_]+', '_', best_model).strip('_')
                        bucket_name = f"AUTO_TB_{mmdd}_{hhmmss_mmm}_{safe_product_tb}_{safe_model_tb}".replace(" ", "")
                        bias_at_creation = _get_current_bias(mode, date_str) or "UNKNOWN"
                        total_net = round(float(candidate.get("total_net", 0.0) or 0.0), 2)
                        min_diff = float(cfg.get("minimum_difference", 5.0) or 5.0)

                        start_from_dt = now_dt
                        eval_dt = now_dt

                        processed_strategies = []
                        # Split when the workflow explicitly requests it for Total Net,
                        # when buy_sell is selected, or when a single-row family would
                        # otherwise violate the 2-row minimum bucket rule.
                        should_split = (
                            (len(pre_tb_family) == 1)
                            or (selected_metric == "buy_sell")
                            or (selected_metric == "net" and t_split_for_tb)
                        )

                        for fam in pre_tb_family:
                            fm = str(fam.get("model") or "").strip()
                            fp = str(fam.get("product") or "").strip().upper()
                            if not fm or not fp:
                                continue
                            series = fam.get("series") if isinstance(fam.get("series"), list) else []
                            
                            # [V20260323_1510] Filter expansion members for positive net in TB
                            f_latest_net = float(fam.get("latest_net", 0.0) or 0.0)
                            if f_latest_net <= 0:
                                continue
                            if bool(cfg.get("require_positive_total_net", True)):
                                try:
                                    f_total_net = float(series[-1].get("net", 0.0) or 0.0) if series else f_latest_net
                                except: f_total_net = f_latest_net
                                if f_total_net <= 0:
                                    continue
                            
                            metrics_to_add = [("buy_net", "buy_net"), ("sell_net", "sell_net")] if should_split else [("net", "net")]
                            
                            for m_type, m_field in metrics_to_add:
                                if series:
                                    creation_net = round(_series_value_at_or_before(series, eval_dt, field=m_field), 2)
                                    start_from_net = round(_series_value_at_or_before(series, start_from_dt, field=m_field), 2)
                                else:
                                    creation_net = round(float(fam.get("latest_net", total_net) or 0.0), 2)
                                    start_from_net = creation_net

                                processed_strategies.append({
                                    "strategy_id": str(uuid.uuid4()),
                                    "key": f"{fm} | {fp}",
                                    "metric": m_type,
                                    "bias_at_creation": bias_at_creation,
                                    "start_from_net": start_from_net,
                                    "net_at_creation": creation_net,
                                    "current_total_net": creation_net,
                                    "start_net_delta_from_chart": round(creation_net - start_from_net, 2),
                                    "current_net_from_chart": round(creation_net - start_from_net, 2),
                                    "net_delta_from_creation": 0.0,
                                    "total_net": 0.0,
                                    "delta_type": delta_type,
                                    "live_trade_net": 0.0
                                })
                        
                        # [V20260311_1345] Deduplicate by strategy+product+metric
                        seen_s = set()
                        final_strategies = []
                        for s in processed_strategies:
                            d_key = f"{s.get('key')}|{s.get('metric')}"
                            if d_key not in seen_s:
                                seen_s.add(d_key)
                                final_strategies.append(s)
                        processed_strategies = final_strategies

                        if len(processed_strategies) < 2:
                            # Try emergency split if we have 1 'net' row left [V20260311_1345]
                            if len(processed_strategies) == 1 and processed_strategies[0]['metric'] == 'net':
                                s = processed_strategies[0]
                                processed_strategies = []
                                mk = s.get('key')
                                ps = mk.split(' | ')
                                if len(ps) == 2:
                                    mn, pn = ps[0].strip(), ps[1].strip()
                                    ser = summary_strategies.get(mn, {}).get(pn, [])
                                    for mt in ("buy_net", "sell_net"):
                                        cn = round(_series_value_at_or_before(ser, eval_dt, field=mt), 2)
                                        sn = round(_series_value_at_or_before(ser, start_from_dt, field=mt), 2)
                                        processed_strategies.append({
                                            "strategy_id": str(uuid.uuid4()),
                                            "key": mk,
                                            "metric": mt,
                                            "bias_at_creation": bias_at_creation,
                                            "start_from_net": sn,
                                            "net_at_creation": cn,
                                            "current_total_net": cn,
                                            "start_net_delta_from_chart": round(cn - sn, 2),
                                            "current_net_from_chart": round(cn - sn, 2),
                                            "net_delta_from_creation": 0.0,
                                            "total_net": 0.0,
                                            "delta_type": delta_type,
                                            "live_trade_net": 0.0
                                        })

                        if len(processed_strategies) < 2:
                            tb_results_list.append({"requested": True, "created": False, "reason": "min_rows_violation_after_dedup"})
                            continue
                        
                        new_bucket = {
                            "bucket_id": str(uuid.uuid4()),
                            "name": bucket_name,
                            "date": date_str,
                            "mode": mode,
                            "market_bias_at_creation": bias_at_creation,
                            "metric": cfg.get("metric", "net"),
                            "delta_type": delta_type,
                            "chart_start_time": start_from_dt.isoformat(),
                            "start_time": eval_dt.isoformat(),
                            "strategies": processed_strategies,
                            "live": True,
                            "open_trades": False,
                            "open_trade_count": 0,
                            "minimum_difference": float(min_diff),
                            "created_by_workflow": "top_x_multi_chart_workflow"
                        }

                        tb_buckets.append(new_bucket)
                        existing_keys.add(_norm_key(best_model, best_product))
                        live_count += 1
                        
                        _sync_bucket_to_grid_live(new_bucket, mode, date_str)

                        tb_results_list.append({
                            "requested": True,
                            "created": True,
                            "activated": True,
                            "bucket_name": bucket_name,
                            "family_size": len(processed_strategies),
                            "reason": "success"
                        })
                    else:
                        tb_results_list.append({"requested": True, "created": False, "reason": "no_candidate_found_for_tb"})

                if any(r.get("created") for r in tb_results_list):
                    tb_data["buckets"] = tb_buckets
                    _save_trade_buckets(tb_data, mode=mode, date_str=date_str)
                    _update_automated_source("Trade Bucket")

                created_count = sum(1 for r in tb_results_list if r.get("created"))
                if created_count > 0:
                    tb_result = {
                        "requested": True,
                        "created": True,
                        "activated": True,
                        "reason": f"success ({created_count} buckets)",
                        "details": tb_results_list
                    }
                else:
                    tb_result = {
                        "requested": True,
                        "created": False,
                        "activated": False,
                        "reason": "no_candidate_found_for_tb" if not tb_results_list else tb_results_list[0].get("reason", "unknown")
                    }


        # [V20260323_1645] Log historical Top 10 snapshot
        _log_top10_history_snapshot(mode, date_str, product_type, sliced)

        return {
            "success": True,
            "message": f"Successfully created Top {len(sliced)} multi-chart payload.",
            "top_x_selected": len(sliced),
            "payload_items": len(payload_items),
            "tb": tb_result
        }
    except Exception as e:
        return {"success": False, "message": str(e)}

def _run_tb_prune_all_negative_once(mode: str, date_str: str, wf: dict) -> dict:
    """
    Remove trade buckets where all strategy net values are below threshold.
    """
    cfg = wf.get("config", {}) if isinstance(wf, dict) else {}
    threshold = float(cfg.get("negative_threshold", -20) or -20)
    product_type = str(cfg.get("product_type") or "").strip().lower() or None

    data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
    buckets = data.get("buckets", [])
    if not buckets:
        return {"success": True, "removed": 0, "message": f"no buckets for {product_type or 'all'}"}

    kept = []
    removed_names = []
    removed_buckets = []

    def _load_summary_strategies_from_file(fpath: Path) -> dict:
        if not fpath.exists():
            return {}
        try:
            with open(fpath, "r") as f:
                return (json.load(f) or {}).get("strategies", {}) or {}
        except Exception:
            return {}

    def _latest_mode_date(_mode: str) -> str:
        mode_dir = BASE_PATH / _mode
        if not mode_dir.exists():
            return date_str
        try:
            dates = [p.name for p in mode_dir.iterdir() if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name)]
            return sorted(dates)[-1] if dates else date_str
        except Exception:
            return date_str

    latest_date = _latest_mode_date(mode)
    summary_current = {}
    for day_dir in _iter_day_dirs_for(mode, latest_date, product_type):
        summary_current.update(_load_summary_strategies_from_file(day_dir / "_summary_net.json"))
    
    if not summary_current:
        for day_dir in _iter_day_dirs_for(mode, date_str, product_type):
            summary_current.update(_load_summary_strategies_from_file(day_dir / "_summary_net.json"))

    def _strategy_net_live(bucket: dict, s: dict) -> float:
        """
        Use the same basis as TB UI current range net:
        current_net_from_chart = latest_summary_net - start_from_net.
        Fallback to persisted fields only when live series is unavailable.
        """
        strat_key = str(s.get("key", "") or "")
        parts = strat_key.split(" | ")
        if len(parts) != 2:
            parts = strat_key.split("|")
        if len(parts) == 2 and summary_current:
            strategy_name = parts[0].strip()
            product = parts[1].strip()
            series = summary_current.get(strategy_name, {}).get(product, [])
            if isinstance(series, list) and series:
                try:
                    latest_net = float(series[-1].get("net", 0.0) or 0.0)
                except Exception:
                    latest_net = 0.0
                try:
                    start_from = float(s.get("start_from_net", s.get("net_at_creation", 0.0)) or 0.0)
                except Exception:
                    start_from = 0.0
                return float(round(latest_net - start_from, 2))

        for k in ("current_net_from_chart", "net_delta_from_creation", "total_net", "current_total_net", "net_at_creation", "start_from_net"):
            if k in s:
                try:
                    return float(s.get(k, 0) or 0)
                except Exception:
                    continue
        return 0.0

    for b in buckets:
        strategies = b.get("strategies", []) if isinstance(b, dict) else []
        if not isinstance(strategies, list) or not strategies:
            kept.append(b)
            continue
        nets = [_strategy_net_live(b, s) for s in strategies if isinstance(s, dict)]
        if nets and all(n < threshold for n in nets):
            bucket_name = str(b.get("name") or "UNKNOWN_BUCKET")
            removed_names.append(bucket_name)

            # Step 1 (required): Deactivate bucket before removing.
            # Persist live=false and push grid sync-off for this bucket source.
            if isinstance(b, dict):
                b["live"] = False
            try:
                _sync_bucket_to_grid_live({**b, "live": False}, mode, date_str)
            except Exception:
                pass

            removed_buckets.append(dict(b) if isinstance(b, dict) else {"name": bucket_name, "live": False})
            continue
        kept.append(b)

    if removed_buckets:
        try:
            hist_file = _resolve_day_dir(mode, date_str) / "_trade_buckets_removed_history.json"
            history = []
            if hist_file.exists():
                with open(hist_file, "r") as hf:
                    history = json.load(hf) or []
            if not isinstance(history, list):
                history = []
            history.append({
                "timestamp": datetime.now().isoformat(),
                "workflow": "tb_prune_all_negative",
                "threshold": threshold,
                "removed_count": len(removed_buckets),
                "removed_buckets": removed_buckets
            })
            with open(hist_file, "w") as hf:
                json.dump(history, hf, indent=4)
        except Exception as e:
            print(f"[WORKFLOW] tb_prune_all_negative archive write failed: {e}")

    if len(kept) != len(buckets):
        data["buckets"] = kept
        _save_trade_buckets(data, mode=mode, date_str=date_str, product_type=product_type)

    return {
        "success": True,
        "removed": len(removed_names),
        "removed_names": removed_names,
        "threshold": threshold
    }


@app.route('/api/workflows/multi_chart_payload', methods=['GET'])
def get_workflow_multi_chart_payload():
    """Return latest workflow-generated payload for Multi Chart import."""
    try:
        if not WORKFLOW_MULTI_CHART_PAYLOAD_FILE.exists():
            return jsonify({"success": True, "payload": None})
        with open(WORKFLOW_MULTI_CHART_PAYLOAD_FILE, "r") as f:
            payload = json.load(f)
        return jsonify({"success": True, "payload": payload})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/market_update', methods=['GET'])
def get_market_update():
    """Return latest periodic market narrative for mode/date."""
    try:
        mode = str(request.args.get('mode', 'live')).lower()
        date_str = str(request.args.get('date') or datetime.now().strftime('%Y-%m-%d'))
        update_file = _resolve_day_dir(mode, date_str) / "_market_update.json"
        if not update_file.exists():
            return jsonify({"success": True, "exists": False, "message": "No market update generated yet."})
        with open(update_file, "r") as f:
            payload = json.load(f) or {}
        return jsonify({"success": True, "exists": True, "update": payload})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/market_update/history', methods=['GET'])
def get_market_update_history():
    """Return historical market narrative blurbs for mode/date."""
    try:
        mode = str(request.args.get('mode', 'live')).lower()
        date_str = str(request.args.get('date') or datetime.now().strftime('%Y-%m-%d'))
        limit_raw = request.args.get('limit')
        try:
            limit = int(limit_raw) if limit_raw is not None else 200
        except Exception:
            limit = 200
        limit = max(1, min(limit, 2000))

        history_file = _resolve_day_dir(mode, date_str) / "_market_update_history.json"
        if not history_file.exists():
            return jsonify({"success": True, "exists": False, "history": []})
        with open(history_file, "r") as f:
            history = json.load(f) or []
        if not isinstance(history, list):
            history = []
        history = history[-limit:]
        history.reverse()  # newest first
        return jsonify({"success": True, "exists": True, "count": len(history), "history": history})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def _extract_product(core: str, products: Set[str]) -> Tuple[str, Optional[str]]:
    core_upper = core.upper()
    for p in sorted(products, key=len, reverse=True):
        if core_upper.endswith(f"_{p}"):
            return core[: -(len(p) + 1)], p
    return core, None


def _normalize_key(raw_key: str, products: Set[str]) -> Tuple[str, Optional[str]]:
    suffix = next((s for s in ACTIVATION_SUFFIXES if raw_key.endswith(s)), None)
    if not suffix:
        return raw_key, None
    core = raw_key[: -len(suffix)]
    base, product = _extract_product(core, products)
    return f"{base}{suffix}", product


def _coerce_entry(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        # [V20260127_1520] Handle None products safely
        raw_products = value.get("products") or []
        return {
            "active": bool(value.get("active")),
            "manual": bool(value.get("manual")),
            "activated_at": value.get("activated_at"),
            "source": value.get("source") or "ui",
            "products": sorted({p.upper() for p in raw_products if isinstance(p, str)})
        }
    return {
        "active": bool(value),
        "manual": False,
        "activated_at": None,
        "source": "ui",
        "products": []
    }


def _merge_entries(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    a["active"] = a["active"] or b["active"]
    a["manual"] = a["manual"] or b["manual"]
    if b.get("activated_at") and (
        not a.get("activated_at") or b["activated_at"] > a["activated_at"]
    ):
        a["activated_at"] = b["activated_at"]
    
    # [V20260204_2057] Preserve source from the most recent or non-'ui' entry
    if b.get("source") and b["source"] != "ui":
        a["source"] = b["source"]
    elif not a.get("source"):
        a["source"] = b.get("source", "ui")

    a["products"] = sorted(set(a.get("products", [])) | set(b.get("products", [])))
    return a


def _is_legacy_format(raw: Dict[str, Any]) -> bool:
    """Check if activations.json is in old (flat) format. [V20251230_2336]"""
    if not raw:
        return False
    # If top-level keys are 'live' or 'sim', it's new format
    if 'live' in raw or 'sim' in raw:
        return False
    # Otherwise, check if any key looks like an activation key
    for key in raw.keys():
        if any(key.endswith(suffix) for suffix in ACTIVATION_SUFFIXES):
            return True
    return False


def _migrate_to_mode_format(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate old flat format to mode-segmented format. [V20251230_2336]"""
    # Move all existing activations to 'live' by default
    return {
        'live': raw,
        'sim': {}
    }


def _normalize_activations(raw: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    products = _load_trade_products()
    out: Dict[str, Any] = {}
    dirty = False

    for raw_key, raw_val in raw.items():
        base_key, product = _normalize_key(str(raw_key), products)
        entry = _coerce_entry(raw_val)

        if product:
            entry["products"].append(product)

        entry["products"] = sorted(set(entry["products"]))

        if raw_key != base_key or product:
            dirty = True

        if base_key in out:
            out[base_key] = _merge_entries(out[base_key], entry)
        else:
            out[base_key] = entry

    return out, dirty


def _load_activations() -> Dict[str, Any]:
    """Load activations with mode segmentation support. [V20251230_2336]"""
    if not ACTIVATIONS_FILE.exists():
        # Create new format structure
        return {'live': {}, 'sim': {}}

    try:
        with open(ACTIVATIONS_FILE, "r") as f:
            raw = json.load(f)
    except json.JSONDecodeError as jde:
        print(f"[ERROR] Corrupted activations.json: {jde}")
        return {'live': {}, 'sim': {}}
    except Exception as e:
        print(f"[ERROR] Loading activations.json failed: {e}")
        return {'live': {}, 'sim': {}}

    # Check if migration is needed
    if _is_legacy_format(raw):
        print("[MIGRATION] Converting activations.json to mode-segmented format...")
        raw = _migrate_to_mode_format(raw)
        dirty = True
    else:
        dirty = False

    # Ensure both mode sections exist
    if 'live' not in raw:
        raw['live'] = {}
        dirty = True
    if 'sim' not in raw:
        raw['sim'] = {}
        dirty = True

    # Normalize each mode section
    for mode in ['live', 'sim']:
        if mode in raw and isinstance(raw[mode], dict):
            normalized, mode_dirty = _normalize_activations(raw[mode])
            raw[mode] = normalized
            dirty = dirty or mode_dirty

    # Save if any changes were made
    if dirty:
        with open(ACTIVATIONS_FILE, "w") as f:
            json.dump(raw, f, indent=4)

    return raw


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# API Endpoints
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@app.route("/api/activations", methods=["GET"])
def get_activations():
    """Get activations from grid_live.json. [V20260211_1550]"""
    mode = request.args.get('mode', 'live').lower()
    
    try:
        grid_live_file = ROOT_PATH / "grid_live.json"
        if not grid_live_file.exists():
            return jsonify({
                "success": True,
                "activations": {}
            })
        
        with open(grid_live_file, "r") as f:
            grid_data = json.load(f)
        
        # Handle both legacy (list) and new (dict) formats
        if isinstance(grid_data, list):
            # Legacy format - assume it's for 'live' mode
            mode_entries = grid_data if mode == 'live' else []
        elif isinstance(grid_data, dict):
            mode_entries = grid_data.get(mode, [])
        else:
            mode_entries = []
        
        # Transform grid_live.json format to activations.json format
        # grid_live.json has: [{model, product, metric, group, source, activated_at}, ...]
        # activations.json expects: {key: {active, manual, products, source, activated_at}, ...}
        
        activations = {}
        for entry in mode_entries:
            model = entry.get('model', '')
            product = entry.get('product', '')
            metric = entry.get('metric', 'net')  # e.g., 'buy_net', 'sell_net', 'net', 'alt'
            source = entry.get('source', 'grid_live')
            activated_at = entry.get('activated_at')
            
            # Parse metric into one or more activation keys.
            # net/total_net and alt represent BOTH directions.
            metric_l = str(metric or 'net').lower()
            target_keys = []
            if metric_l.startswith('buy_'):
                mode_type = metric_l.replace('buy_', '') or 'net'
                target_keys = [f"{model}_buy_{mode_type}"]
            elif metric_l.startswith('sell_'):
                mode_type = metric_l.replace('sell_', '') or 'net'
                target_keys = [f"{model}_sell_{mode_type}"]
            elif metric_l in ('net', 'total_net'):
                target_keys = [f"{model}_buy_net", f"{model}_sell_net"]
            elif metric_l == 'alt':
                target_keys = [f"{model}_buy_alt", f"{model}_sell_alt"]
            else:
                target_keys = [f"{model}_buy_net", f"{model}_sell_net"]

            # Add or merge into activations dict
            for key in target_keys:
                if key in activations:
                    existing_products = set(activations[key].get('products', []))
                    existing_products.add(product.upper())
                    activations[key]['products'] = sorted(existing_products)
                    if activated_at and (not activations[key].get('activated_at') or activated_at > activations[key]['activated_at']):
                        activations[key]['activated_at'] = activated_at
                else:
                    activations[key] = {
                        'active': True,
                        'manual': False,  # grid_live entries are automated
                        'products': [product.upper()] if product else [],
                        'source': source,
                        'activated_at': activated_at
                    }
        
        return jsonify({
            "success": True,
            "activations": activations
        })
    except Exception as e:
        print(f"[ERROR] /api/activations failed: {e}")
        return jsonify({
            "success": False,
            "message": str(e),
            "activations": {}
        })



# [V20260127_1520] Get available dates for a given mode
@app.route("/api/dates", methods=["GET"])
def get_dates():
    """Get available trade dates for specified mode."""
    mode = request.args.get('mode', 'live').lower()
    product_type = request.args.get('product_type', 'all').lower()
    required_file = request.args.get('file') # [V20260318_1055]
    
    dates = set()
    
    # [V20260318_1015] Use a specific directory if product_type is provided
    if product_type and product_type != 'all':
        json_dir = ROOT_PATH / "json" / mode / product_type
        if json_dir.exists():
            for item in json_dir.iterdir():
                if item.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}$', item.name):
                    # [V20260318_1055] Only add if file exists
                    if not required_file or (item / required_file).exists():
                        dates.add(item.name)
    else:
        # Fallback recursive search for all dates
        json_root = ROOT_PATH / "json" / mode
        if json_root.exists():
            for item in json_root.iterdir():
                if not item.is_dir():
                    continue
                # Level 1: json/live/2026-01-01
                if re.match(r'^\d{4}-\d{2}-\d{2}$', item.name):
                    if not required_file or (item / required_file).exists():
                        dates.add(item.name)
                    continue
                # Level 2: json/live/indices/2026-01-01
                for child in item.iterdir():
                    if child.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}$', child.name):
                        if not required_file or (child / required_file).exists():
                            dates.add(child.name)
    
    sorted_dates = sorted(dates, reverse=True)
    
    return jsonify({
        "success": True,
        "dates": sorted_dates
    })

@app.route('/api/trades', methods=['GET'])
def get_trades():
    """
    [V20260128_1500] Load trade JSON files for a given mode and date.
    Optimized: Uses filename pattern matching to reduce file scanning when filters are provided.
    """
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
            
        strategy_filter = request.args.get('strategy', 'all')
        req_strategy = strategy_filter # Alias for loop logic
        req_product = request.args.get('product')
        req_product_type = request.args.get('product_type')
        req_params = request.args.get('params')
        live_only = request.args.get('live_only', 'false').lower() == 'true'
        since_time = request.args.get('since_time') # [V20260205_1640] Filter by entry time
        bucket_context = request.args.get('bucket_name') # [V20260320_1230] Context for L-Trade identification
        
        since_dt = None
        if since_time:
            try:
                # Handle potential space/T differences in ISO strings
                since_dt = datetime.fromisoformat(since_time.replace('Z', '').replace(' ', 'T'))
            except: pass
        
        day_dirs = _iter_day_dirs_for(run_mode, date, req_product_type)
        
        print(f"[API] get_trades: mode={run_mode}, date={date}, strategy={strategy_filter}, product={req_product}, params={req_params}, live={live_only}")
        
        if not day_dirs:
            return jsonify({
                'success': False,
                'message': f'Directory not found for mode={run_mode} date={date}',
                'trades': []
            })
        
        # [V20260130_1420] Capture Session Max Net from summary metadata
        session_max_net = 0.0
        for trade_dir in day_dirs:
            summary_path = trade_dir / "_summary_net.json"
            if not summary_path.exists():
                continue
            try:
                with open(summary_path, 'r') as f:
                    s_data = json.load(f)
                    session_max_net = max(session_max_net, float(s_data.get('session_max_net', 0.0)))
            except:
                pass

        # [V20260205_1710] HIGH PERFORMANCE PATH: Use central trades summary if available
        indexed_trades = []
        for trade_dir in day_dirs:
            trades_summary_path = trade_dir / "_trades_summary.json"
            if not trades_summary_path.exists():
                continue
            try:
                with open(trades_summary_path, 'r') as f:
                    index_data = json.load(f)
                    indexed_trades.extend(index_data.get('trades', []))
            except Exception as e:
                print(f"[API] Failed to use trades index from {trades_summary_path}: {e}")
        if indexed_trades:
            # [V20260320_1230] Load leadership data if bucket context is provided
            leadership_map = {}
            if bucket_context:
                all_leadership = _load_tb_leadership(run_mode, date, req_product_type)
                # Map by bucket name for easier lookup
                leadership_map = {bl['bucket']: bl for bl in all_leadership}

            filtered = []
            for t in indexed_trades:
                        # 1. Product Filter
                        if req_product and req_product != 'all' and req_product != 'undefined':
                            if t.get('product', '').upper() != req_product.upper():
                                continue
                                
                        # 2. Strategy Filter
                        # The dashboard table key is often 'breakout' (app_name)
                        # or 'breakout_params' (app_name + params).
                        # req_strategy from table rows is usually {appName}_{params}
                        t_app = t.get('app_name', '')
                        t_params = t.get('strategy', '')
                        t_full_key = f"{t_app}_{t_params}" if t_params else t_app
                        
                        if req_strategy and req_strategy != 'all' and req_strategy != 'undefined':
                            # Match against app_name OR app_name_params OR full key
                            if req_strategy != t_app and req_strategy != t_full_key and req_strategy != t_params:
                                # Substring match for broader compatibility
                                if req_strategy not in t_full_key and t_app not in req_strategy:
                                    continue

                        # 2b. Params Filter (Explicitly requested by some views)
                        # [V20260205_2200] Broaden match to check full key if explicit field doesn't match
                        if req_params and req_params not in ('all', 'undefined', ''):
                            if req_params != t_params and req_params not in t_params and req_params not in t_full_key:
                                continue
                        
                        # 3. Live Only Filter
                        # [V20260205_2215] Robust live match (checks summarized is_live OR raw flags if indexed)
                        if live_only:
                            is_l = (
                                t.get('is_live') == True or 
                                t.get('is_live_trade') == True or 
                                t.get('order_sent_net') in (True, 'true')
                            )
                            if not is_l:
                                continue
                            
                        # 4. Since Time Filter
                        if since_dt:
                            e_time = t.get('entry_time')
                            if e_time:
                                try:
                                    e_dt = datetime.fromisoformat(e_time.replace('Z', '').replace(' ', 'T'))
                                    if e_dt < since_dt:
                                        continue
                                except: pass
                        
                        # [V20260320_1230] Tag L-Trades
                        if bucket_context and bucket_context in leadership_map:
                            if _is_trade_in_leader_window(t, leadership_map[bucket_context]):
                                t['is_l_trade'] = True
                                
                        filtered.append(t)

            return jsonify({
                'success': True,
                'count': len(filtered),
                'trades': filtered,
                'mode': run_mode,
                'date': date,
                'session_max_net': session_max_net,
                'indexed': True,
                'version': VERSION
            })

        trades = []
        
        file_count = 0
        product_hint = req_product if req_product and req_product not in ('all', 'undefined') else None
        for trade_dir in day_dirs:
            for json_file in _iter_trade_json_files(
                trade_dir,
                include_archived_closed=True,
                product_hint=product_hint,
            ):
                file_count += 1
                if file_count > 5000:
                    print(f"[API] /api/trades: Hit 5000 file limit, stopping scan")
                    break

                try:
                    # [V20260128_0415] Optimization: Parse filename first to pre-filter before reading file content
                    raw_filename = json_file.name
                    normalized_filename = _strip_trade_suffix(raw_filename)
                    filename = Path(normalized_filename).stem
                    parts = filename.split('_')
                    
                    # Check for product/app_name in filename
                    f_app_name = None
                    f_product_code = None
                    f_strategy_params = None
                    
                    if len(parts) >= 6:
                        timestamp_idx = None
                        for i, part in enumerate(parts):
                            if len(part) == 8 and part.isdigit():
                                timestamp_idx = i
                                break
                        
                        if timestamp_idx is not None:
                            # Parsing logic mirrors that in get_stats_summary and previous get_trades
                            candidate_idx = timestamp_idx - 1
                            if candidate_idx >= 0:
                                val = parts[candidate_idx]
                                if len(val) <= 2 and val.isalpha() and val.isupper():
                                    product_idx = candidate_idx - 1
                                    if product_idx >= 0:
                                        potential_product = parts[product_idx]
                                        if len(potential_product) >= 3 and potential_product.isalpha() and potential_product.isupper():
                                            f_app_name = '_'.join(parts[:product_idx])
                                            f_product_code = potential_product
                                        else:
                                            f_app_name = '_'.join(parts[:candidate_idx])
                                    else:
                                        f_app_name = '_'.join(parts[:candidate_idx])
                                else:
                                    if len(val) >= 3 and val.isalpha() and val.isupper():
                                        f_app_name = '_'.join(parts[:candidate_idx])
                                        f_product_code = val
                                    else:
                                        f_app_name = '_'.join(parts[:timestamp_idx])
                            else:
                                f_app_name = '_'.join(parts[:timestamp_idx])
                                
                            window = parts[timestamp_idx + 2] if timestamp_idx + 2 < len(parts) else '5'
                            buffer = parts[timestamp_idx + 3] if timestamp_idx + 3 < len(parts) else '0.0001'
                            tp = parts[timestamp_idx + 4].replace('.json', '') if timestamp_idx + 4 < len(parts) else '10.0'
                            sl = parts[timestamp_idx + 5].replace('.json', '') if timestamp_idx + 5 < len(parts) else '6.0'
                            
                            # Normalize params to match summary_net format (window_tpX_slY)
                            f_strategy_params = f"{window}_tp{tp}_sl{sl}"

                    # Server-Side Filter Check (Optimization)
                    # [V20260128_1555] Relaxed pre-filter: allow f_app_name to start with req_strategy
                    # This handles cases where f_app_name includes product components (e.g. GBPAUD_C)
                    if req_strategy and req_strategy != 'all' and req_strategy != 'undefined' and f_app_name:
                        if req_strategy != f_app_name and not f_app_name.startswith(req_strategy):
                            continue
                        
                    if req_product and req_product != 'all' and req_product != 'undefined' and f_product_code and req_product != f_product_code.upper():
                        pass 

                    with open(json_file, 'r') as f:
                        trade_data = json.load(f)
                        
                        status_suffix = None
                        raw_lower = raw_filename.lower()
                        if '_op' in raw_lower:
                            status_suffix = 'OPEN'
                        elif '_cl' in raw_lower or '_cld' in raw_lower:
                            status_suffix = 'CLOSED'
                        
                        # [V20260128_1555] Normalize App Name from JSON content (matches summary_net_generator)
                        # This ensures the Drill-down matches the table row accurately.
                        internal_app_name = trade_data.get('source_strategy') or trade_data.get('script_name') or trade_data.get('app_name') or f_app_name or 'unknown'
                        
                        # Apply logic to standardize fields
                        trade_data['app_name'] = internal_app_name
                        trade_data['script_name'] = internal_app_name # Compatibility
                        
                        # Strategy (Params) resolution
                        # Try to get from JSON first
                        strategy_params = trade_data.get('strategy') or f_strategy_params or ''
                        trade_data['strategy'] = strategy_params
                        trade_data['strategy_key'] = strategy_params # Compatibility
                        
                        # Product resolution
                        if 'product' not in trade_data:
                            trade_data['product'] = f_product_code or 'UNKNOWN'
                        
                        trade_data['filename'] = raw_filename
                        if status_suffix:
                            trade_data['status'] = status_suffix
                            
                        # Final Filter Checks
                        if req_product and req_product not in ('all', 'undefined', 'null'):
                            if trade_data.get('product', '').upper() != req_product.upper():
                                continue

                        target_id = req_strategy
                        if target_id in ('all', 'undefined', 'null', None):
                            target_id = ''
                        
                        if req_params and req_params not in ('all', 'undefined', 'null', ''):
                            if not target_id:
                                target_id = req_params
                            elif req_params not in target_id:
                                sep = '' if target_id.endswith('_') else '_'
                                target_id = f"{target_id}{sep}{req_params}"
                        
                        if target_id and target_id != 'all':
                            match = False
                            target_norm = str(target_id or '').strip().lower()
                            internal_norm = str(internal_app_name or '').strip().lower()
                            trade_params = str(trade_data.get('strategy') or req_params or '').strip()
                            params_norm = trade_params.lower()
                            derived_full_norm = f"{internal_norm}_{params_norm}" if params_norm else internal_norm

                            if target_norm in (internal_norm, params_norm, derived_full_norm):
                                match = True
                            elif internal_norm and (target_norm.startswith(f"{internal_norm}_") or internal_norm in target_norm):
                                match = True
                            elif params_norm and (target_norm.endswith(params_norm) or params_norm in target_norm):
                                match = True
                            elif derived_full_norm and (target_norm in derived_full_norm or derived_full_norm in target_norm):
                                match = True

                            if not match:
                                continue
                                
                        if req_product and req_product != 'all' and req_product != 'undefined':
                            if trade_data.get('product') != req_product:
                                continue

                        if live_only:
                            is_l = (
                                trade_data.get('is_live_trade') == True or 
                                trade_data.get('live_trade_executed') == True or 
                                trade_data.get('order_sent_net') in [True, 'true']
                            )
                            if not is_l:
                                continue
                                
                        if since_dt:
                            entry_time_str = trade_data.get('entry_time')
                            if entry_time_str:
                                try:
                                    entry_dt = datetime.fromisoformat(entry_time_str.replace('Z', '').replace(' ', 'T'))
                                    if entry_dt < since_dt:
                                        continue
                                except:
                                    pass

                        trades.append(trade_data)
                            
                except json.JSONDecodeError as e:
                    print(f"Error parsing {json_file}: {e}")
                    continue
                except Exception as e:
                    print(f"Error loading {json_file}: {e}")
                    continue
            if file_count > 5000:
                break
        
        return jsonify({
            'success': True,
            'count': len(trades),
            'trades': trades,
            'mode': run_mode,
            'date': date,
            'session_max_net': session_max_net,
            'version': VERSION
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'trades': []
        }), 500


@app.route('/api/top20', methods=['GET'])
def get_top20():
    try:
        run_mode = request.args.get('mode', 'live')
        product_type = request.args.get('product_type')
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        merged = []
        last_update = None
        for top20_path in [day_dir / "_top20.json" for day_dir in _iter_day_dirs_for(run_mode, date, product_type)]:
            if not top20_path.exists():
                continue
            with open(top20_path, 'r') as f:
                data = json.load(f)
            merged.extend(data.get('top20', []))
            candidate_last_update = data.get('last_update')
            if candidate_last_update and (last_update is None or str(candidate_last_update) > str(last_update)):
                last_update = candidate_last_update
        if merged:
            return jsonify({
                'success': True,
                'top20': merged,
                'last_update': last_update,
                'version': VERSION
            })
        return jsonify({
            'success': False,
            'message': 'Top 20 data not yet generated for today.'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/push_to_grid_v2', methods=['POST'])
def push_to_grid_v2():
    """
    [V20260205_1900] Pushes a top-performing strategy to grid_live.json.
    Ensures that Top 20 source supersedes any other existing source for that strategy.
    [V20260205_2100] Enforces automated_trade_source: Top20
    [V20260215_0001] Enforces automated_trade_sources allowlist from config UI.
    """
    try:
        data = request.json
        mode = data.get('mode', 'live')
        strategy = data.get('strategy')
        product = data.get('product')
        metric = data.get('metric', 'net')
        group = data.get('group') # [V20260210_1355] Support set-based grouping
        source = data.get('source', 'PSB') # [V20260210_1603] Allow custom source from UI

        if not strategy or not product:
            return jsonify({'success': False, 'message': 'Strategy and Product required.'})

        source_str = str(source).strip()

        # Normalize runtime source labels to config allowlist keys.
        if source_str.startswith('PSB_Family'):
            requested_source = 'PSB_Family'
        elif source_str.startswith('PSB'):
            requested_source = 'PSB'
        elif source_str.startswith('Top20'):
            requested_source = 'Top20'
        elif source_str.startswith('Trade Bucket'):
            requested_source = 'Trade Bucket'
        elif source_str.startswith(('Frequency', 'frequency', 'rank_alert')):
            requested_source = 'Frequency'
        else:
            requested_source = source_str

        if not _is_source_allowed(requested_source):
            print(f"[GRID-LIVE] REJECTED: source='{source_str}' blocked by config allowlist (requested='{requested_source}').")
            return jsonify({'success': True, 'message': 'Skipped (Source Overrule)'})

        grid_file = ROOT_PATH / "grid_live.json"

        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            if grid_file.exists():
                try:
                    with open(grid_file, "r") as f:
                        full_data = json.load(f)
                    if isinstance(full_data, list): # Migrate legacy
                        full_data = {'live': full_data, 'sim': []}
                except: pass

            mode_list = full_data.get(mode, [])

            # Remove any existing entry for this strategy/product (Override Logic)
            new_mode_list = []
            for item in mode_list:
                if item.get('model') == strategy and item.get('product') == product:
                    continue
                new_mode_list.append(item)

            # Add new top20 entry
            new_mode_list.append({
                "model": strategy,
                "product": product,
                "metric": metric,
                "activated_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                "group": group if group else f"{strategy} | {product}",
                "source": source_str if source_str != 'PSB' else f"PSB_{strategy}" # [V20260210_1603] Use provided source or default
            })

            full_data[mode] = new_mode_list

            with open(grid_file, "w") as f:
                json.dump(full_data, f, indent=4)
            
            # [V20260210_1630] Sync with activations (Activation Explorer)
            _sync_grid_to_activations(new_mode_list, mode=mode)

        return jsonify({'success': True, 'message': f'Strategy {strategy} promoted to grid via Top 20'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})



@app.route('/api/stats_summary', methods=['GET'])
def get_stats_summary():
    """
    [V20260128_1448] FAST Strategy Performance Stats.
    Reads from pre-generated _summary_net.json instead of iterating through thousands of trade files.
    """
    try:
        run_mode = request.args.get('mode', 'live')
        product_type = request.args.get('product_type')
        if product_type == 'all':
            product_type = None

        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        summary_files = [day_dir / "_summary_net.json" for day_dir in _iter_day_dirs_for(run_mode, date, product_type)]
        print(f"[API] stats_summary for mode={run_mode}, date={date}, paths={summary_files}")

        if not summary_files:
            return jsonify({
                'success': False,
                'message': f'Summary file not found for {date} ({run_mode}). Run summary_net_generator.py.',
                'data': []
            })

        strategies = {}
        for summary_file in summary_files:
            if not summary_file.exists():
                continue
            with open(summary_file, 'r') as f:
                summary_data = json.load(f)
            for strategy_name, products in (summary_data.get('strategies', {}) or {}).items():
                existing = strategies.setdefault(strategy_name, {})
                if isinstance(products, dict):
                    existing.update(products)
        limit_arg = request.args.get('limit')
        view_mode = request.args.get('view', '').lower()
        sort_key = request.args.get('sort_key', '').lower()
        sort_dir = request.args.get('sort_dir', '').lower()
        apply_sorting = any([limit_arg, view_mode, sort_key, sort_dir])
        limit = None
        if limit_arg:
            try:
                limit = max(1, min(int(limit_arg), 1000))
            except ValueError:
                limit = None
        
        # Build aggregated stats from summary_net structure
        # Structure: { "strategy_name": { "PRODUCT": [ {t, net, buy_net, sell_net, b_c, s_c, ...}, ... ] } }
        
        result = []
        global_dist = {f"{h:02d}": 0 for h in range(24)}
        
        for strategy_name, products in strategies.items():
            for product, data_points in products.items():
                if not data_points:
                    continue
                
                # [V20260210_1415] Hourly distribution for timebar
                # delta of trade counts across data points
                local_dist = {f"{h:02d}": 0 for h in range(24)}
                last_total_count = 0
                
                # Check if data_points is a list (historical snapshots)
                series = data_points if isinstance(data_points, list) else [data_points]
                
                for pt in series:
                    try:
                        ts = datetime.fromisoformat(pt['t'])
                        hr = ts.strftime('%H')
                        curr_total = pt.get('b_c', 0) + pt.get('s_c', 0)
                        delta = max(0, curr_total - last_total_count)
                        if delta > 0:
                            local_dist[hr] += delta
                            global_dist[hr] += delta
                        last_total_count = curr_total
                    except: continue

                # Get the LAST data point (most recent aggregation)
                last = series[-1]
                
                # [V20260129_1603] Try to extract params from strategy name if empty
                params = last.get('params', '')
                display_strategy = strategy_name
                if not params:
                    if '_' in strategy_name:
                         for prefix in ['breakout_R_Rev_v2_', 'breakout_R_Rev_', 'breakout_Rev_', 'breakout_R_', 'breakout_']:
                             if strategy_name.startswith(prefix):
                                 display_strategy = prefix.rstrip('_')
                                 params = strategy_name[len(prefix):]
                                 break
                         
                result.append({
                    'product': product,
                    'strategy': display_strategy,
                    'params': params,
                    'trade_count': last.get('b_c', 0) + last.get('s_c', 0),
                    'total_net': round(last.get('net', 0), 2),
                    'buy_count': last.get('b_c', 0),
                    'buy_net': round(last.get('buy_net', 0), 2),
                    'sell_count': last.get('s_c', 0),
                    'sell_net': round(last.get('sell_net', 0), 2),
                    'buyPercent': last.get('buyPercent', 0),
                    'sellPercent': last.get('sellPercent', 0),
                    'buy_alt': round(last.get('buy_alt', 0), 2),
                    'sell_alt': round(last.get('sell_alt', 0), 2),
                    'live_buy_net': round(last.get('live_buy', 0), 2),
                    'live_sell_net': round(last.get('live_sell', 0), 2),
                    'time_dist': local_dist # [V20260210_1415]
                })

        # ... (Global dist added below)


        if apply_sorting:
            allowed_keys = {
                'product': 'product',
                'strategy': 'strategy',
                'parm': 'params',
                'params': 'params',
                'total_net': 'total_net',
                'trade_count': 'trade_count',
                'buy_count': 'buy_count',
                'buy_net': 'buy_net',
                'buy_alt': 'buy_alt',
                'sell_count': 'sell_count',
                'sell_net': 'sell_net',
                'sell_alt': 'sell_alt',
                'live_buy': 'live_buy_net',
                'live_sell': 'live_sell_net',
                'buypercent': 'buyPercent',
                'sellpercent': 'sellPercent',
                'buyPercent': 'buyPercent',
                'sellPercent': 'sellPercent'
            }
            key = allowed_keys.get(sort_key, 'total_net')
            numeric_keys = {
                'total_net', 'trade_count', 'buy_count', 'buy_net', 'buy_alt',
                'sell_count', 'sell_net', 'sell_alt', 'live_buy_net', 'live_sell_net',
                'buyPercent', 'sellPercent'
            }
            is_numeric = key in numeric_keys

            result_sorted = sorted(result, key=lambda item: float(item.get(key, 0) or 0) if is_numeric else str(item.get(key, '')).lower())

            if limit:
                view = view_mode if view_mode in ('top', 'bottom') else 'top'
                if view == 'bottom':
                    result_sorted = result_sorted[:limit]
                else:
                    result_sorted = result_sorted[-limit:]

            if sort_dir == 'desc':
                result_sorted.reverse()

            result = result_sorted

        return jsonify({
            'success': True,
            'data': result,
            'snapshot': strategies, # [V20260210_1537] Raw series for playback
            'global_time_dist': global_dist, # [V20260210_1415]
            'mode': run_mode,
            'date': date,
            'source': 'summary_net'
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e),
            'data': []
        }), 500


@app.route('/api/portfolio_stats', methods=['GET'])
def get_portfolio_stats():
    """
    [V20260323_1945] Hierarchical Performance Stats for Treemap.
    Optimized: Backend filtering by product_type + efficient parsing.
    Part of task: hierarchical_treemap_filters
    """
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date')
        product_type_filter = request.args.get('product_type')
        
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        # Handle 'all' as None for _iter_day_dirs_for
        p_type_req = None if product_type_filter == 'all' else product_type_filter

        cfg = _load_layout_runtime_config()
        type_mapping = cfg.get("product_type_by_product", {})

        # Get relevant product types
        day_dirs = _iter_day_dirs_for(run_mode, date, p_type_req)
        
        all_items = []
        
        for d_dir in day_dirs:
            # Fallback product type from directory
            dir_product_type = d_dir.parent.name
            if dir_product_type.lower() in ('live', 'sim'):
                dir_product_type = "forex" 
                
            summary_file = d_dir / "_summary_net.json"
            if not summary_file.exists():
                continue
                
            try:
                with open(summary_file, "r") as f:
                    data = json.load(f)
            except:
                continue
                
            strategies = data.get("strategies", {})
            for strat_name, products in strategies.items():
                # [V20260323_1945] PARSE ONCE PER STRATEGY (Optimization)
                parts = strat_name.split('_')
                s_name = "breakout"
                s_window = "unknown"
                s_params = "none"
                window_idx = -1
                param_idx = -1
                for i, p in enumerate(parts):
                    if p in ('2', '3', '4'): window_idx = i
                    if p.lower().startswith('tp'):
                        param_idx = i
                        break
                if param_idx != -1:
                    s_params = "_".join(parts[param_idx:])
                    if window_idx != -1:
                        s_name = "_".join(parts[:window_idx])
                        s_window = parts[window_idx]
                    else:
                        s_name = "_".join(parts[:param_idx])
                else:
                    s_name = strat_name
                s_name = s_name.lower()

                for prod, entries in products.items():
                    if not entries: continue
                    
                    # [V20260323_1900] Definitive categorization
                    p_upper = str(prod).upper()
                    p_type = product_type_for_product(p_upper, cfg)
                    
                    mapping = cfg.get("product_type_by_product", {})
                    if p_upper not in mapping and p_upper.lower() not in mapping:
                        if dir_product_type != "forex":
                            p_type = dir_product_type

                    # Backend Filtering: Skip if it doesn't match requested type
                    if p_type_req and p_type != p_type_req:
                        continue

                    last = entries[-1]
                    net = round(float(last.get('net', 0.0) or 0.0), 2)
                    
                    all_items.append({
                        "product_type": p_type,
                        "product": p_upper,
                        "strategy_name": s_name,
                        "strategy_window": s_window,
                        "strategy_params": s_params,
                        "full_strategy": strat_name,
                        "net": net,
                        "trades": last.get('b_c', 0) + last.get('s_c', 0)
                    })
                    
        return jsonify({
            "success": True,
            "date": date,
            "mode": run_mode,
            "count": len(all_items),
            "items": all_items
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/virtual_trades', methods=['GET'])
def get_virtual_trades():
    """Load virtual trade JSON files for the given run mode/date."""
    try:
        run_mode = request.args.get('mode', 'live')
        date = request.args.get('date')
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        trades = []
        for day_dir in _iter_day_dirs_for(run_mode, date):
            virtual_dir = day_dir / 'virtual'
            if not virtual_dir.exists():
                continue
            for json_file in virtual_dir.glob('vt_*.json'):
                try:
                    with open(json_file, 'r') as handle:
                        trade_data = json.load(handle)
                        trade_data['filename'] = json_file.name
                        trades.append(trade_data)
                except Exception as exc:  # pylint: disable=broad-except
                    print(f"[WARN] Failed to read {json_file}: {exc}")
                    continue
        trades.sort(key=lambda entry: entry.get('entry_time') or entry.get('exit_time') or '', reverse=True)
        return jsonify({
            'success': True,
            'trades': trades,
            'session_max_net': session_max_net
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'trades': []
        }), 500



@app.route("/api/activations", methods=["POST"])
def update_activations():
    """Update activations for specified mode. [V20251230_2336]"""
    payload = request.json or {}
    mode = payload.get('mode', 'live').lower()  # Get mode from payload
    activations_data = payload.get('activations', payload)  # Support both formats
    
    # Remove 'mode' key if it exists in activations_data
    if 'mode' in activations_data:
        del activations_data['mode']
    
    now = datetime.utcnow().isoformat()
    trade_products = _load_trade_products()

    # Load all activations (mode-segmented)
    all_activations = _load_activations()
    
    # Get activations for current mode
    mode_activations = all_activations.get(mode, {})

    for raw_key, value in activations_data.items():
        base_key, derived_product = _normalize_key(str(raw_key), trade_products)
        entry = mode_activations.get(base_key, {
            "active": False,
            "manual": False,
            "activated_at": None,
            "source": "ui",
            "products": []
        })

        if isinstance(value, dict):
            requested_active = bool(value.get("active"))
            manual = bool(value.get("manual"))
            source = value.get("source") or entry.get("source", "ui")
            products = value.get("products") or value.get("product") or []
        else:
            requested_active = bool(value)
            manual = False
            source = "ui"
            products = []

        if derived_product:
            products = list(products) + [derived_product]

        products = {p.upper() for p in products if isinstance(p, str)}

        if products:
            if requested_active:
                entry["products"] = sorted(set(entry["products"]) | products)
                entry["active"] = True
                entry["activated_at"] = entry["activated_at"] or now
            else:
                entry["products"] = sorted(set(entry["products"]) - products)
                entry["active"] = bool(entry["products"])
                if not entry["active"]:
                    entry["activated_at"] = None
        else:
            entry["active"] = requested_active
            entry["activated_at"] = now if requested_active else None

        entry["manual"] = manual
        entry["source"] = source
        
        # [V20251230_2351] Remove entry if it becomes inactive
        if entry["active"]:
            mode_activations[base_key] = entry
        elif base_key in mode_activations:
            # Remove the entry if it's being deactivated
            del mode_activations[base_key]

    # Update the mode section
    all_activations[mode] = mode_activations

    # Save all activations
    with open(ACTIVATIONS_FILE, "w") as f:
        json.dump(all_activations, f, indent=4)

    return jsonify({
        "success": True,
        "activations": mode_activations  # Return only current mode's activations
    })


@app.route("/api/activations/remove", methods=["POST"])
def remove_activation():
    """Remove a specific activation key entirely. [V20260105_0025]"""
    try:
        payload = request.json or {}
        mode = payload.get('mode', 'live').lower()
        key = payload.get('key')

        if not key:
            return jsonify({"success": False, "message": "Key is required"}), 400

        all_activations = _load_activations()
        
        if mode not in all_activations:
            return jsonify({"success": False, "message": f"Mode {mode} not found"}), 404
            
        if key not in all_activations[mode]:
             return jsonify({"success": False, "message": f"Key {key} not found in {mode}"}), 404

        # Remove the key
        del all_activations[mode][key]

        # Save the updated file
        with open(ACTIVATIONS_FILE, "w") as f:
            json.dump(all_activations, f, indent=4)
        return jsonify({
            "success": True,
            "message": f"Successfully removed {key} from {mode}"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/activations/remove_all", methods=["POST"])
def remove_all_activations():
    """Removes all activation keys for the specified mode. [V20260205_2125]"""
    try:
        payload = request.json or {}
        mode = payload.get('mode', 'live').lower()

        # 1. Clear Activations
        all_activations = _load_activations()
        if mode in all_activations:
            all_activations[mode] = {}
            with open(ACTIVATIONS_FILE, "w") as f:
                json.dump(all_activations, f, indent=4)
        
        # 2. Clear Grid-Live for that mode (to prevent auto-resync)
        # [V20260205_2125] Added to ensure deletions stick
        grid_live_file = ROOT_PATH / "grid_live.json"
        if grid_live_file.exists():
            try:
                with open(grid_live_file, "r") as f:
                    grid_data = json.load(f)
                
                if isinstance(grid_data, dict) and mode in grid_data:
                    grid_data[mode] = []
                    _archive_grid_live(mode) # Archive before clearing
                    with open(grid_live_file, "w") as f:
                        json.dump(grid_data, f, indent=4)
                    print(f"[CLEANUP] grid_live.json ({mode}) cleared via Remove All.")
                elif isinstance(grid_data, list) and mode == 'live':
                    _archive_grid_live(mode)
                    with open(grid_live_file, "w") as f:
                        json.dump([], f, indent=4)
            except Exception as ge:
                print(f"[ERROR] Failed to clear grid_live during remove_all: {ge}")

        return jsonify({
            "success": True,
            "message": f"Successfully cleared all activations and grid_live entries for {mode}"
        })
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Trade Promotion Helpers [V20260127_1610]
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _scan_open_trades(mode: str, date_str: str) -> List[Dict[str, Any]]:
    """Scan and load all open trade JSON files for a given mode/date.
    
    Returns:
        List of dicts with 'path' and 'data' keys
    """
    json_dir = ROOT_PATH / "json" / mode / date_str
    if not json_dir.exists():
        return []
    
    open_trades = []
    for file_path in json_dir.glob("*_op.json"):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                open_trades.append({
                    'path': file_path,
                    'data': data
                })
        except Exception as e:
            print(f"[WARN] Failed to load {file_path}: {e}")
    
    return open_trades


def _match_trade(trade_data: Dict[str, Any], strategy: str, product: str, direction: str, parm: str) -> bool:
    """Check if a trade matches the given criteria.
    
    Args:
        trade_data: Trade JSON data
        strategy: Strategy name (e.g., 'breakout_2_tp20.0_sl10.0')
        product: Product name (e.g., 'GBPEUR_C')
        direction: 'buy' or 'sell'
        parm: Parameter string (e.g., '2_0.00015_20.0_10.0')
    
    Returns:
        True if trade matches all criteria
    """
    # Match strategy name
    trade_strategy = trade_data.get('script_name', trade_data.get('app_name', ''))
    if trade_strategy != strategy:
        return False
    
    # Match product
    trade_product = trade_data.get('product', '')
    if trade_product != product:
        return False
    
    # Match direction
    trade_direction = trade_data.get('direction', '').upper()
    if direction == 'buy' and trade_direction not in ('LONG', 'BUY'):
        return False
    if direction == 'sell' and trade_direction not in ('SHORT', 'SELL'):
        return False
    
    # Match parameters (optional - if parm is provided)
    if parm:
        trade_parm = trade_data.get('strategy', '')  # Parameters are stored in 'strategy' field
        if trade_parm != parm:
            return False
    
    return True


def _promote_trade_to_live(trade_path: Path, trade_data: Dict[str, Any], mode_type: str = 'net') -> bool:
    """Promote a single trade to live status by creating tradeable order and updating flags.
    
    Args:
        trade_path: Path to the open trade JSON file
        trade_data: Trade data dict
        mode_type: 'net' or 'alt'
    
    Returns:
        True if promotion succeeded
    """
    try:
        # Check if already promoted
        flag_key = f'order_sent_{mode_type}'
        if trade_data.get(flag_key):
            print(f"[PROMOTE] Trade {trade_path.name} already has {flag_key}=True")
            return False
        
        # Create tradeable order JSON
        tradeable_dir = trade_path.parent / "tradeable"
        tradeable_dir.mkdir(exist_ok=True)
        
        # Generate tradeable filename
        base_name = trade_path.stem.replace('_opn', '')
        tradeable_name = f"{base_name}_{mode_type}_opn.json"
        tradeable_path = tradeable_dir / tradeable_name
        
        # Create tradeable order content
        tradeable_order = {
            'trade_id': trade_data.get('id', trade_data.get('trade_id')),
            'product': trade_data.get('product'),
            'direction': trade_data.get('direction'),
            'entry_price': trade_data.get('entry_price'),
            'entry_time': trade_data.get('entry_time'),
            'tp_pips': trade_data.get('tp_pips'),
            'sl_pips': trade_data.get('sl_pips'),
            'mode': mode_type,
            'promoted_at': datetime.utcnow().isoformat(),
            'promoted_by': 'activation_toggle',
            'status': 'OPEN'
        }
        
        # Write tradeable order
        with open(tradeable_path, 'w') as f:
            json.dump(tradeable_order, f, indent=2)
        
        # Update open trade JSON with live flag
        trade_data[flag_key] = True
        trade_data['promoted_at'] = datetime.utcnow().isoformat()
        
        with open(trade_path, 'w') as f:
            json.dump(trade_data, f, indent=2)
        
        print(f"[PROMOTE] Successfully promoted {trade_path.name} to {mode_type.upper()} L-trade")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to promote trade {trade_path}: {e}")
        return False


@app.route("/api/promote_trades", methods=["POST"])
def promote_trades():
    """Promote existing open trades to L-trades when activation is toggled.
    
    This endpoint scans for open trades matching the given criteria and promotes
    them to live status by creating tradeable orders.
    """
    try:
        payload = request.json or {}
        mode = payload.get('mode', 'live').lower()
        strategy = payload.get('strategy', '')
        product = payload.get('product', '')
        direction = payload.get('direction', '')  # 'buy' or 'sell'
        parm = payload.get('parm', '')
        date_str = payload.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        if not all([strategy, product, direction]):
            return jsonify({
                "success": False,
                "message": "Missing required parameters: strategy, product, direction"
            }), 400
        
        # Scan for open trades
        open_trades = _scan_open_trades(mode, date_str)
        
        # Find matching trades
        matching_trades = []
        for trade_info in open_trades:
            if _match_trade(trade_info['data'], strategy, product, direction, parm):
                matching_trades.append(trade_info)
        
        # Promote matching trades
        promoted_count = 0
        failed_count = 0
        
        for trade_info in matching_trades:
            # Promote to 'net' mode (can be extended to support 'alt' as well)
            if _promote_trade_to_live(trade_info['path'], trade_info['data'], mode_type='net'):
                promoted_count += 1
            else:
                failed_count += 1
        
        return jsonify({
            "success": True,
            "promoted": promoted_count,
            "failed": failed_count,
            "total_matched": len(matching_trades),
            "message": f"Promoted {promoted_count} trade(s) to live status"
        })
        
    except Exception as e:
        print(f"[ERROR] Promotion failed: {e}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/api/config", methods=["GET"])
def get_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return jsonify({"success": True, "config": json.load(f)})
    except Exception:
        return jsonify({"success": True, "config": {}})


@app.route("/api/config", methods=["POST"])
def update_config():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid config"}), 400

    # [V20260204_1410] 2026-02-04 14:10: Catch re-enabling Frequency Notifier to deactivate buckets
    try:
        with open(CONFIG_FILE, "r") as f:
            old_cfg = json.load(f)
        
        # If rank_alert_suspended was true and is now false (or missing/false)
        was_suspended = old_cfg.get('rank_alert_suspended', False)
        is_suspended = data.get('rank_alert_suspended', False)
        
        if was_suspended and not is_suspended:
            print("[CONFIG] Frequency Notifier re-enabled. Deactivating Trade Buckets (Mutual Exclusion).")
            _deactivate_all_trade_buckets('live')
            _deactivate_all_trade_buckets('sim')
            # [V20260205_2100] Set automated source to Frequency
            _update_automated_source('Frequency')
            # Trigger grid sync for clean state
            _sync_bucket_to_grid_live({'name': 'cleanup', 'live': False}, 'live', datetime.now().strftime('%Y-%m-%d'))
    except:
        pass

    # Normalize automated source fields (backward compatible single + new multi)
    src_multi = data.get('automated_trade_sources')
    if isinstance(src_multi, list):
        normalized = []
        for s in src_multi:
            if isinstance(s, str) and s.strip():
                sv = s.strip()
                if sv not in normalized:
                    normalized.append(sv)
        data['automated_trade_sources'] = normalized
        if normalized:
            data['automated_trade_source'] = normalized[0]
    elif isinstance(data.get('automated_trade_source'), str) and data.get('automated_trade_source').strip():
        data['automated_trade_source'] = data['automated_trade_source'].strip()
        data['automated_trade_sources'] = [data['automated_trade_source']]

    normalized_product_type = default_product_type(data)
    data['product_type'] = normalized_product_type
    data['product_types'] = configured_product_types(data)
    raw_trade_products = data.get('trade_products', [])
    if isinstance(raw_trade_products, list):
        normalized_trade_products = []
        for raw_product in raw_trade_products:
            product_value = str(raw_product or '').strip().upper()
            if product_value and product_value not in normalized_trade_products:
                normalized_trade_products.append(product_value)
        data['trade_products'] = normalized_trade_products
    raw_mapping = data.get('product_type_by_product', {})
    normalized_mapping = {}
    if isinstance(raw_mapping, dict):
        for raw_key, raw_value in raw_mapping.items():
            key = str(raw_key or '').strip().upper()
            if not key:
                continue
            normalized_mapping[key] = product_type_for_product(key, {
                'product_type': normalized_product_type,
                'product_type_by_product': raw_mapping,
            })
    data['product_type_by_product'] = normalized_mapping
    if data.get('default_min_value') is None:
        data['default_min_value'] = 10.0
    raw_min_by_type = data.get('min_value_by_product_type', {})
    normalized_min_by_type = {}
    if isinstance(raw_min_by_type, dict):
        for raw_key, raw_value in raw_min_by_type.items():
            key = str(raw_key or '').strip().lower()
            if not key:
                continue
            try:
                normalized_min_by_type[key] = float(raw_value)
            except (TypeError, ValueError):
                continue
    if not normalized_min_by_type and data.get('default_min_value') is not None:
        normalized_min_by_type[normalized_product_type] = float(data['default_min_value'])
    data['min_value_by_product_type'] = normalized_min_by_type
    raw_min_by_product = data.get('min_value_by_product', {})
    normalized_min_by_product = {}
    if isinstance(raw_min_by_product, dict):
        for raw_key, raw_value in raw_min_by_product.items():
            key = str(raw_key or '').strip().upper()
            if not key:
                continue
            try:
                normalized_min_by_product[key] = float(raw_value)
            except (TypeError, ValueError):
                continue
    data['min_value_by_product'] = normalized_min_by_product
    raw_move_by_product = data.get('min_move_by_product', {})
    normalized_move_by_product = {}
    if isinstance(raw_move_by_product, dict):
        for raw_key, raw_value in raw_move_by_product.items():
            key = str(raw_key or '').strip().upper()
            if not key:
                continue
            try:
                normalized_move_by_product[key] = float(raw_value)
            except (TypeError, ValueError):
                continue
    data['min_move_by_product'] = normalized_move_by_product
    if data.get('crypto_trade_qty_percent') is None:
        data['crypto_trade_qty_percent'] = data.get('trade_qty_percent', 45.0)

    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return jsonify({"success": True})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "ts": datetime.utcnow().isoformat()})


@app.route("/multi_chart.html")
def serve_multi_chart():
    return send_from_directory(ROOT_PATH, "multi_chart.html")


# [V20260225] Live Hub routes for IP-based hosting
LANDING_PATH = Path(__file__).parent.parent / "piphunter" / "landing"

@app.route("/live")
@app.route("/live/")
def serve_live_hub():
    """Serve the PipHunter Live Hub website"""
    return send_from_directory(LANDING_PATH, "breakout-live-hub.html")

@app.route("/live/<path:subpath>")
def serve_live_assets(subpath):
    """Serve Live Hub static assets (styles, images, etc.)"""
    return send_from_directory(LANDING_PATH, subpath)


@app.route("/multi_chart.js")
def serve_multi_chart_js():
    return send_from_directory(ROOT_PATH, "multi_chart.js")


@app.route('/', defaults={'path': 'trade_viewer.html'})
@app.route('/<path:path>')
def serve_static(path):
    """Serve any static file from ROOT_PATH, fallback to trade_viewer.html"""
    try:
        # Prevent accessing files outside of ROOT_PATH
        if Path(ROOT_PATH / path).exists() and Path(ROOT_PATH / path).is_file():
            return send_from_directory(ROOT_PATH, path)
        return send_from_directory(ROOT_PATH, "trade_viewer.html")
    except:
        return send_from_directory(ROOT_PATH, "trade_viewer.html")


@app.route("/api/top_one", methods=["GET"])
def get_top_one():
    """Load _top_one.json for a given mode and date [V20260105_1532]"""
    try:
        run_mode = request.args.get('mode', 'live')
        product_type = request.args.get('product_type')
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        for file_path in [day_dir / "_top_one.json" for day_dir in _iter_day_dirs_for(run_mode, date, product_type)]:
            if not file_path.exists():
                continue
            with open(file_path, 'r') as f:
                content = json.load(f)
            return jsonify({
                'success': True,
                'content': content
            })
        return jsonify({
            'success': False,
            'message': f'Summary file not found for {date} ({run_mode})',
            'content': None
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route("/api/frequency", methods=["GET"])
def get_frequency():
    """Proxy for the SQL frequency API [V20260105_2355]"""
    try:
        mode = request.args.get('mode', 'live')
        db = 'tradedb_sim2' if mode == 'sim' else 'tradedb'
        
        # Call the port 8000 API
        url = f"http://127.0.0.1:8000/api/vw_top_one_frequency?db={db}"
        print(f"[PROXY] Fetching: {url}")
        
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status == 200:
                raw_data = response.read().decode('utf-8')
                data = json.loads(raw_data)
                rows = data.get('data', [])
                return jsonify({
                    'success': True,
                    'data': rows
                })
            else:
                return jsonify({
                    'success': False,
                    'message': f"SQL API returned status {response.status}"
                }), response.status
                
    except Exception as e:
        print(f"[ERROR] Proxy failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route("/sidebar.css")
def serve_sidebar_css():
    return send_from_directory(ROOT_PATH, "sidebar.css")


@app.route("/pnl_graph.css")
def serve_pnl_graph_css():
    return send_from_directory(ROOT_PATH, "pnl_graph.css")


@app.route("/sidebar.html")
def serve_sidebar_html():
    return send_from_directory(ROOT_PATH, "sidebar.html")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Trade Buckets Activation Sync [V20260122_2230]
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _parse_strategy_key(key: str) -> Optional[dict]:
    """Parse a strategy key like 'breakout_Rev_3_tp20.0_sl10.0 | GBPEUR_C'."""
    if not key or ' | ' not in key:
        return None
    try:
        strat_part, product = key.split(' | ')
        product = product.strip()
        
        # Defaults
        tp = 5.0
        sl = 6.0
        window = 3
        buffer = 0.00015
        
        # Extract TP/SL using regex
        tp_m = re.search(r'_tp(\d+\.?\d*)', strat_part)
        sl_m = re.search(r'_sl(\d+\.?\d*)', strat_part)
        
        if tp_m: tp = float(tp_m.group(1))
        if sl_m: sl = float(sl_m.group(1))
        
        # Extract base name (strip params)
        base = strat_part
        if tp_m: base = strat_part[:tp_m.start()]
        elif sl_m: base = strat_part[:sl_m.start()]
        base = base.strip('_')
        
        # Try to infer window size from name (e.g. Rev_3 -> 3)
        win_m = re.search(r'_([1-9])$', base)
        if not win_m:
            win_m = re.search(r'_([1-9])_', base)
        if win_m:
            window = int(win_m.group(1))
            
        return {
            'product': product,
            'strategy': base,
            'parm': {
                'window_size': window,
                'pip_buffer': buffer,
                'tp': tp,
                'sl': sl
            }
        }
    except Exception as e:
        print(f"[PARSER] Error parsing key {key}: {e}")
        return None


def _archive_grid_live(mode):
    """[V20260205_2130] Archive grid_live.json to individual files in grid_live_history directory."""
    try:
        source_file = ROOT_PATH / "grid_live.json"
        if not source_file.exists():
            return
        
        # [V20260205_2130] Dedicated history directory
        history_dir = ROOT_PATH / "grid_live_history"
        if not history_dir.exists():
            try:
                history_dir.mkdir(parents=True, exist_ok=True)
            except: pass
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        history_file = history_dir / f"grid_live_{mode}_{timestamp}.json"
            
        with open(source_file, "r") as f:
            current_data = json.load(f)
            
        with open(history_file, "w") as f:
            json.dump(current_data, f, indent=4)
        print(f"[ARCHIVE] grid_live archived to {history_file}")
    except Exception as e:
        print(f"[ARCHIVE-ERROR] Failed to archive grid_live: {e}")

def _prune_grid_live_siblings(model: str, product: str, mode: str, reason: str = '') -> Dict[str, Any]:
    """
    Remove sibling products for the same model after a live execution.
    Keeps only entries that match the executed product for the model.
    """
    try:
        if not model or not product:
            return {"success": False, "removed": 0, "message": "model/product required"}

        grid_live_file = ROOT_PATH / "grid_live.json"
        if not grid_live_file.exists():
            return {"success": True, "removed": 0, "message": "grid_live.json missing"}

        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            try:
                with open(grid_live_file, "r") as f:
                    loaded = json.load(f)
                if isinstance(loaded, list):
                    full_data['live'] = loaded
                elif isinstance(loaded, dict):
                    full_data = loaded
            except Exception as e:
                return {"success": False, "removed": 0, "message": f"load failed: {e}"}

            mode_list = full_data.get(mode, [])
            removed = []
            kept = []
            for item in mode_list:
                if item.get('model') == model and str(item.get('product', '')).upper() != str(product).upper():
                    removed.append(item)
                else:
                    kept.append(item)

            if not removed:
                return {"success": True, "removed": 0}

            _archive_grid_live(mode)

            full_data[mode] = kept
            with open(grid_live_file, "w") as f:
                json.dump(full_data, f, indent=4)

            _sync_grid_to_activations(kept, mode=mode)

        if removed:
            print(f"[PRUNE] Removed {len(removed)} sibling entries for {model} on {mode} (reason={reason})")
        return {"success": True, "removed": len(removed)}
    except Exception as e:
        print(f"[PRUNE-ERROR] {e}")
        return {"success": False, "removed": 0, "message": str(e)}

def _load_config_safe() -> Dict[str, Any]:
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _parse_summary_point_ts(value: Any) -> Optional[datetime]:
    """Parse summary point timestamp into a timezone-aware datetime (UTC)."""
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None

def _derive_bias_from_summary(mode: str, date_str: str, recent_window_minutes: int = 60, product_type: str | None = None) -> Dict[str, Any]:
    """
    Canonical bias derivation from _summary_net.json only.

    Returned fields (for strategy_performance bias display):
    - timestamp: summary last_update
    - bias: day bias from signed totals (BUY if total_buy_net >= total_sell_net else SELL)
    - market_condition: CHOPPY/TRENDING from configured thresholds
    - status: STRONG when recent bias aligns with day bias, else MIXED
    - recent_buy_pnl / recent_sell_pnl: trailing-window deltas from cumulative buy/sell nets
    - recent_buy_count / recent_sell_count: trailing-window deltas from cumulative counts
    - total_buy_net / total_sell_net: full current signed totals at summary timestamp
    """
    summary_file = _resolve_day_dir(mode, date_str, product_type=product_type) / "_summary_net.json"
    if not summary_file.exists():
        return {
            "success": False,
            "error": f"missing summary file: {summary_file}"
        }

    try:
        with open(summary_file, "r") as f:
            summary = json.load(f) or {}
    except Exception as e:
        return {"success": False, "error": f"failed reading summary: {e}"}

    raw_last_update = summary.get("last_update")
    cut_dt = _parse_summary_point_ts(raw_last_update) or datetime.now(timezone.utc)
    window_start = cut_dt - timedelta(minutes=max(1, int(recent_window_minutes or 60)))

    strategies = summary.get("strategies", {})
    if not isinstance(strategies, dict):
        strategies = {}

    total_buy_net = 0.0
    total_sell_net = 0.0
    recent_buy_pnl = 0.0
    recent_sell_pnl = 0.0
    recent_buy_count = 0
    recent_sell_count = 0
    latest_point_dt: Optional[datetime] = None

    for _model, products in strategies.items():
        if not isinstance(products, dict):
            continue
        for _product, points in products.items():
            if not isinstance(points, list) or not points:
                continue

            # Keep points that can be timestamped and are <= cutoff
            typed_points: List[Tuple[datetime, Dict[str, Any]]] = []
            for p in points:
                if not isinstance(p, dict):
                    continue
                p_dt = _parse_summary_point_ts(p.get("t"))
                if p_dt is None or p_dt > cut_dt:
                    continue
                typed_points.append((p_dt, p))

            if not typed_points:
                continue

            typed_points.sort(key=lambda x: x[0])
            last_dt, last_pt = typed_points[-1]
            if latest_point_dt is None or last_dt > latest_point_dt:
                latest_point_dt = last_dt

            last_buy = float(last_pt.get("buy_net", 0.0) or 0.0)
            last_sell = float(last_pt.get("sell_net", 0.0) or 0.0)
            last_bc = int(last_pt.get("b_c", 0) or 0)
            last_sc = int(last_pt.get("s_c", 0) or 0)

            base_buy = 0.0
            base_sell = 0.0
            base_bc = 0
            base_sc = 0
            for p_dt, p in typed_points:
                if p_dt <= window_start:
                    base_buy = float(p.get("buy_net", 0.0) or 0.0)
                    base_sell = float(p.get("sell_net", 0.0) or 0.0)
                    base_bc = int(p.get("b_c", 0) or 0)
                    base_sc = int(p.get("s_c", 0) or 0)
                else:
                    break

            total_buy_net += last_buy
            total_sell_net += last_sell
            recent_buy_pnl += (last_buy - base_buy)
            recent_sell_pnl += (last_sell - base_sell)
            recent_buy_count += max(0, last_bc - base_bc)
            recent_sell_count += max(0, last_sc - base_sc)

    day_bias = "BUY" if total_buy_net >= total_sell_net else "SELL"
    if recent_buy_pnl == recent_sell_pnl:
        recent_bias = day_bias
    else:
        recent_bias = "BUY" if recent_buy_pnl > recent_sell_pnl else "SELL"
    status = "STRONG" if day_bias == recent_bias else "MIXED"

    cfg = _load_config_safe()
    pnl_threshold = float(cfg.get("picker_pnl_spread_threshold", 2000) or 2000)
    count_threshold = float(cfg.get("picker_count_diff_threshold", 0.05) or 0.05)
    pnl_spread = abs(recent_buy_pnl - recent_sell_pnl)
    total_recent = recent_buy_count + recent_sell_count
    count_diff_pct = abs(recent_buy_count - recent_sell_count) / max(1, total_recent)
    is_choppy = (count_diff_pct <= count_threshold) or (pnl_spread < pnl_threshold)
    market_condition = "CHOPPY" if is_choppy else "TRENDING"

    return {
        "success": True,
        "source": "_summary_net.json",
        "timestamp": cut_dt.isoformat(),
        "last_update": raw_last_update,
        "latest_series_point": latest_point_dt.isoformat() if latest_point_dt else None,
        "run_mode": mode,
        "date": date_str,
        "product_type": product_type or default_product_type(_load_layout_runtime_config()),
        "bias": day_bias,
        "day_bias": day_bias,
        "recent_bias": recent_bias,
        "status": status,
        "market_condition": market_condition,
        "total_buy_net": round(total_buy_net, 2),
        "total_sell_net": round(total_sell_net, 2),
        "recent_buy_pnl": round(recent_buy_pnl, 2),
        "recent_sell_pnl": round(recent_sell_pnl, 2),
        "recent_buy_count": int(recent_buy_count),
        "recent_sell_count": int(recent_sell_count),
        "recent_window_minutes": int(max(1, int(recent_window_minutes or 60))),
    }

@app.route('/api/bias_from_summary', methods=['GET'])
def api_bias_from_summary():
    """Return canonical bias fields derived only from _summary_net.json."""
    try:
        mode = str(request.args.get('mode', 'live')).lower()
        date_str = request.args.get('date') or datetime.now(timezone.utc).strftime('%Y-%m-%d')
        product_type = request.args.get('product_type')
        recent_window_minutes = int(request.args.get('window_minutes', 60) or 60)
        payload = _derive_bias_from_summary(mode, date_str, recent_window_minutes, product_type)
        if not payload.get("success"):
            return jsonify(payload), 404
        return jsonify(payload)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def _get_current_bias(mode: str, date_str: str) -> Optional[str]:
    try:
        bias_file = _resolve_day_dir(mode, date_str) / "_targeted_strategies.json"
        if not bias_file.exists():
            return None
        with open(bias_file, "r") as f:
            data = json.load(f)
        bias = data.get("bias")
        if bias:
            return str(bias).upper()
    except Exception:
        return None
    return None

def _select_psb_siblings(mode: str, date_str: str, bias: str, max_items: int) -> List[Dict[str, Any]]:
    summary_file = _resolve_day_dir(mode, date_str) / "_summary_net.json"
    if not summary_file.exists():
        return []
    try:
        with open(summary_file, "r") as f:
            summary_data = json.load(f)
    except Exception:
        return []

    strategies = summary_data.get("strategies", {})
    if not isinstance(strategies, dict):
        return []

    metric_key = "buy_net" if bias == "BUY" else "sell_net"
    count_key = "b_c" if bias == "BUY" else "s_c"
    total_key = "net"

    best_model = None
    best_metric = -float("inf")
    best_count = -1

    for model_name, products in strategies.items():
        if not isinstance(products, dict):
            continue
        for product, points in products.items():
            if not isinstance(points, list) or not points:
                continue
            last = points[-1]
            metric_val = float(last.get(metric_key, 0) or 0)
            count_val = int(last.get(count_key, 0) or 0)
            total_val = float(last.get(total_key, 0) or 0)
            if metric_val > 0 and count_val > 0 and total_val > 0:
                if metric_val > best_metric or (metric_val == best_metric and count_val > best_count):
                    best_metric = metric_val
                    best_count = count_val
                    best_model = model_name

    if not best_model:
        return []

    siblings = []
    products = strategies.get(best_model, {})
    if not isinstance(products, dict):
        return []
    for product, points in products.items():
        if not isinstance(points, list) or not points:
            continue
        last = points[-1]
        metric_val = float(last.get(metric_key, 0) or 0)
        count_val = int(last.get(count_key, 0) or 0)
        total_val = float(last.get(total_key, 0) or 0)
        # Enforce bias-specific profitability per strategy/product, not just at model selection stage.
        if metric_val <= 0 or count_val <= 0 or total_val <= 0:
            continue
        siblings.append({
            "model": best_model,
            "product": product,
            "metric": "buy_net" if bias == "BUY" else "sell_net",
            "metric_val": metric_val,
            "count_val": count_val
        })

    siblings.sort(key=lambda x: (x["metric_val"], x["count_val"]), reverse=True)
    return siblings[:max_items]

def _select_psb_family_entries(mode: str, date_str: str, bias: str, max_items: int) -> List[Dict[str, Any]]:
    """
    Select strategy/product candidates from the highest-priority family
    that matches market bias.

    BUY  -> family side 'buy'
    SELL -> family side 'sell'
    """
    priority_file = ROOT_PATH / "json" / "strategy_profile" / "priority_strategy_list.json"
    members_file = ROOT_PATH / "json" / "strategy_profile" / "strategy_profile_equivalent_family_members.json"
    summary_file = _resolve_day_dir(mode, date_str) / "_summary_net.json"

    if not priority_file.exists() or not members_file.exists() or not summary_file.exists():
        return []

    try:
        with open(priority_file, "r") as f:
            priority_data = json.load(f)
        with open(members_file, "r") as f:
            family_members = json.load(f)
        with open(summary_file, "r") as f:
            summary_data = json.load(f)
    except Exception:
        return []

    priorities = []
    if isinstance(priority_data, list):
        priorities = priority_data
    elif isinstance(priority_data, dict):
        priorities = priority_data.get("priorities", [])

    if not isinstance(priorities, list) or not isinstance(family_members, list):
        return []

    target_side = "buy" if str(bias).upper() == "BUY" else "sell"
    selected_family = None
    for item in priorities:
        if str(item.get("side", "")).lower() == target_side:
            selected_family = str(item.get("family_id", "")).strip()
            if selected_family:
                break
    if not selected_family:
        return []

    strategies = {
        str(m.get("strategy", "")).strip()
        for m in family_members
        if str(m.get("family_id", "")).strip() == selected_family
        and str(m.get("side", "")).lower() == target_side
    }
    if not strategies:
        return []

    strategies_blob = summary_data.get("strategies", {})
    if not isinstance(strategies_blob, dict):
        return []

    metric_key = "buy_net" if target_side == "buy" else "sell_net"
    count_key = "b_c" if target_side == "buy" else "s_c"
    total_key = "net"

    entries = []
    for model_name in strategies:
        products = strategies_blob.get(model_name, {})
        if not isinstance(products, dict):
            continue
        for product, points in products.items():
            if not isinstance(points, list) or not points:
                continue
            last = points[-1]
            metric_val = float(last.get(metric_key, 0) or 0)
            count_val = int(last.get(count_key, 0) or 0)
            total_val = float(last.get(total_key, 0) or 0)
            # Enforce per-product positivity for execution candidates.
            if metric_val <= 0 or count_val <= 0 or total_val <= 0:
                continue
            entries.append({
                "family_id": selected_family,
                "model": model_name,
                "product": product,
                "metric": metric_key,
                "metric_val": metric_val,
                "count_val": count_val
            })

    entries.sort(key=lambda x: (x["metric_val"], x["count_val"]), reverse=True)
    return entries[:max_items]

def _grid_is_empty(mode: str) -> bool:
    grid_live_file = ROOT_PATH / "grid_live.json"
    if not grid_live_file.exists():
        return True
    try:
        with open(grid_live_file, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            return len(data) == 0
        if isinstance(data, dict):
            return len(data.get(mode, [])) == 0
    except Exception:
        return True
    return True

_GRID_AUTO_LAST_FILL = 0.0
_GRID_AUTO_COOLDOWN = 60.0
_WORKFLOW_LAST_RUN: Dict[str, float] = {}
_MARKET_UPDATE_LAST_RUN: Dict[str, float] = {}


def _load_live_trades_for_day(mode: str, date_str: str) -> List[dict]:
    rows: list[dict] = []
    for day_dir in _iter_day_dirs_for(mode, date_str):
        live_file = day_dir / "_live_trades.json"
        if not live_file.exists():
            continue
        try:
            with open(live_file, "r") as f:
                data = json.load(f) or {}
            live_rows = data.get("trades", [])
            if isinstance(live_rows, list):
                rows.extend(r for r in live_rows if isinstance(r, dict))
        except Exception:
            continue
    if rows:
        return rows
    return []


def _generate_market_update(mode: str, date_str: str) -> dict:
    now = datetime.now()
    now_ts = now.timestamp()
    trades = _load_live_trades_for_day(mode, date_str)
    targeted = {}
    targeted_file = _resolve_day_dir(mode, date_str) / "_targeted_strategies.json"
    if targeted_file.exists():
        try:
            with open(targeted_file, "r") as f:
                targeted = json.load(f) or {}
        except Exception:
            targeted = {}

    bias = str(targeted.get("bias") or "N/A").upper()
    total_buy = float(targeted.get("total_buy_net", 0.0) or 0.0)
    total_sell = float(targeted.get("total_sell_net", 0.0) or 0.0)
    status = str(targeted.get("status") or "UNKNOWN")
    market_condition = str(targeted.get("market_condition") or "UNKNOWN")

    closed = [t for t in trades if str(t.get("status", "")).upper() == "CLOSED"]
    open_trades = [t for t in trades if str(t.get("status", "")).upper() == "OPEN"]
    last_window_sec = 30 * 60
    prev_window_sec = 60 * 60

    def _trade_ts(t: dict) -> float:
        ts = t.get("exit_time") or t.get("entry_time")
        if not ts:
            return 0.0
        try:
            return datetime.fromisoformat(str(ts).replace("Z", "")).timestamp()
        except Exception:
            return 0.0

    recent = [t for t in closed if (now_ts - _trade_ts(t)) <= last_window_sec]
    previous = [t for t in closed if last_window_sec < (now_ts - _trade_ts(t)) <= prev_window_sec]

    def _side(t: dict) -> str:
        d = str(t.get("direction") or "LONG").upper()
        return "SELL" if "SHORT" in d else "BUY"

    def _side_net(rows: List[dict], side: str) -> float:
        return sum(float(r.get("net_return", 0.0) or 0.0) for r in rows if _side(r) == side)

    recent_buy = _side_net(recent, "BUY")
    recent_sell = _side_net(recent, "SELL")
    prev_buy = _side_net(previous, "BUY")
    prev_sell = _side_net(previous, "SELL")
    open_net = sum(float(t.get("net_return", 0.0) or 0.0) for t in open_trades)

    imbalance = total_buy - total_sell
    if bias in ("BUY", "SELL"):
        lead_side = bias
    else:
        lead_side = "BUY" if total_buy >= total_sell else "SELL"

    momentum_side = "BUY" if recent_buy >= recent_sell else "SELL"
    momentum_delta = abs(recent_buy - recent_sell)
    forecast = (
        f"Next period likely favors {lead_side} continuation."
        if momentum_side == lead_side
        else f"Next period risk of rotation toward {momentum_side}."
    )

    def _product_impacts(rows: List[dict]) -> Dict[str, float]:
        net_by_product: Dict[str, float] = {}
        for r in rows:
            product = str(r.get("product") or "").strip().upper()
            if not product:
                continue
            net_by_product[product] = net_by_product.get(product, 0.0) + float(r.get("net_return", 0.0) or 0.0)
        return net_by_product

    def _faction_impacts(rows: List[dict]) -> Dict[str, float]:
        net_by_faction: Dict[str, float] = {}
        for r in rows:
            model = str(r.get("model") or "").strip().lower()
            if not model:
                continue
            faction = model.split("_tp")[0].upper() if "_tp" in model else model.upper()
            net_by_faction[faction] = net_by_faction.get(faction, 0.0) + float(r.get("net_return", 0.0) or 0.0)
        return net_by_faction

    product_impacts = _product_impacts(recent if recent else closed)
    faction_impacts = _faction_impacts(recent if recent else closed)
    top_product = "N/A"
    top_product_net = 0.0
    weak_product = "N/A"
    weak_product_net = 0.0
    top_faction = "N/A"
    top_faction_net = 0.0
    if product_impacts:
        ranked = sorted(product_impacts.items(), key=lambda x: x[1], reverse=True)
        top_product, top_product_net = ranked[0]
        weak_product, weak_product_net = ranked[-1]
    if faction_impacts:
        faction_ranked = sorted(faction_impacts.items(), key=lambda x: x[1], reverse=True)
        top_faction, top_faction_net = faction_ranked[0]

    likely_winner = lead_side
    if momentum_side != lead_side and momentum_delta > 0:
        likely_winner = momentum_side

    winner_confidence = "HIGH" if momentum_side == lead_side else "MEDIUM"
    if abs(imbalance) < 1e-9 and momentum_delta < 1e-9:
        winner_confidence = "LOW"

    headline = f"{mode.upper()} Battle Pulse {now.strftime('%H:%M:%S')} | Bias {bias}"
    beats = [
        f"Bell: BUY {total_buy:,.2f} vs SELL {total_sell:,.2f}.",
        f"{lead_side} presses. Imbalance {imbalance:,.2f}.",
        f"30m score: BUY {recent_buy:,.2f} | SELL {recent_sell:,.2f}.",
        f"Faction lead: {top_faction} {top_faction_net:,.2f}.",
        f"Likely winner: {likely_winner} ({winner_confidence}).",
        f"Product impact: {top_product} {top_product_net:,.2f}; weak {weak_product} {weak_product_net:,.2f}.",
        f"Open heat: {len(open_trades)} trades, net {open_net:,.2f}.",
        forecast,
    ]
    narrative = " ".join(beats)

    return {
        "created_at": now.isoformat(),
        "mode": mode,
        "date": date_str,
        "bias": bias,
        "market_condition": market_condition,
        "status": status,
        "totals": {
            "buy_net": round(total_buy, 2),
            "sell_net": round(total_sell, 2),
            "imbalance": round(imbalance, 2)
        },
        "windows": {
            "last_30m": {"buy_net": round(recent_buy, 2), "sell_net": round(recent_sell, 2), "closed_count": len(recent)},
            "prev_30m": {"buy_net": round(prev_buy, 2), "sell_net": round(prev_sell, 2), "closed_count": len(previous)}
        },
        "open": {"count": len(open_trades), "net": round(open_net, 2)},
        "forecast": forecast,
        "likely_winner": likely_winner,
        "winner_confidence": winner_confidence,
        "narrative_style": "strategy-boxing-battle-pulse",
        "faction_impact": {
            "top_faction": top_faction,
            "top_faction_net": round(top_faction_net, 2)
        },
        "product_impact": {
            "top_product": top_product,
            "top_product_net": round(top_product_net, 2),
            "weakest_product": weak_product,
            "weakest_product_net": round(weak_product_net, 2)
        },
        "narrative_beats": beats,
        "headline": headline,
        "narrative": narrative
    }


def _maybe_generate_market_update(mode: str, date_str: str, cfg: dict) -> None:
    enabled = bool(cfg.get("market_update_enabled", False))
    if not enabled:
        return
    try:
        interval_min = int(cfg.get("market_update_interval_minutes", 5) or 5)
    except Exception:
        interval_min = 5
    interval_sec = max(60, interval_min * 60)
    now_ts = time.time()
    key = f"{mode}:{date_str}"
    last = _MARKET_UPDATE_LAST_RUN.get(key, 0.0)
    if now_ts - last < interval_sec:
        return

    payload = _generate_market_update(mode, date_str)
    day_dir = _ensure_day_dir(mode, date_str)
    latest_file = day_dir / "_market_update.json"
    history_file = day_dir / "_market_update_history.json"

    try:
        with open(latest_file, "w") as f:
            json.dump(payload, f, indent=2)
        history = []
        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    history = json.load(f) or []
                if not isinstance(history, list):
                    history = []
            except Exception:
                history = []
        history.append(payload)
        history = history[-500:]
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)
        _MARKET_UPDATE_LAST_RUN[key] = now_ts
    except Exception as e:
        print(f"[MARKET-UPDATE] Failed to write market update: {e}")

def _auto_fill_grid_if_empty() -> None:
    global _GRID_AUTO_LAST_FILL
    cfg = _load_config_safe()
    run_mode = str(cfg.get("run_mode", "live")).lower()
    # [V20260211_1415] Optional kill switch for automatic grid refill when empty.
    # Keep default behavior (enabled) if key is missing.
    grid_auto_refil = bool(cfg.get("grid_auto_refil", cfg.get("grid_auto_refill", True)))
    if not grid_auto_refil:
        return
    automated_sources = cfg.get("automated_trade_sources")
    if isinstance(automated_sources, list):
        sources = [str(s).strip() for s in automated_sources if isinstance(s, str) and str(s).strip()]
    else:
        sources = [str(cfg.get("automated_trade_source", "PSB")).strip()]
    eligible_sources = [s for s in sources if s in ("PSB", "PSB_Family")]
    if not eligible_sources:
        return

    now = time.time()
    if now - _GRID_AUTO_LAST_FILL < _GRID_AUTO_COOLDOWN:
        return

    if not _grid_is_empty(run_mode):
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    bias = _get_current_bias(run_mode, date_str)
    if not bias:
        return

    # Prefer family source when both enabled.
    chosen_source = "PSB_Family" if "PSB_Family" in eligible_sources else "PSB"
    if not _is_source_allowed(chosen_source):
        return

    if chosen_source == "PSB_Family":
        candidates = _select_psb_family_entries(run_mode, date_str, bias, max_items=10)
    else:
        candidates = _select_psb_siblings(run_mode, date_str, bias, max_items=10)

    if not candidates:
        return

    _archive_grid_live(run_mode)

    with GRID_LIVE_LOCK:
        full_data = {'live': [], 'sim': []}
        grid_live_file = ROOT_PATH / "grid_live.json"
        if grid_live_file.exists():
            try:
                with open(grid_live_file, "r") as f:
                    loaded = json.load(f)
                if isinstance(loaded, list):
                    full_data['live'] = loaded
                elif isinstance(loaded, dict):
                    full_data = loaded
            except Exception:
                pass

        entries = []
        for item in candidates:
            source_tag = (
                f"PSB_FAMILY_{item.get('family_id', 'NA')}_{item['model']}"
                if automated_source == "PSB_Family"
                else f"PSB_{item['model']}"
            )
            group_tag = (
                f"PSB_FAMILY_AUTO|GRID_EMPTY|{bias}|{item.get('family_id', 'NA')}"
                if automated_source == "PSB_Family"
                else f"PSB_AUTO|GRID_EMPTY|{bias}|{item['model']}"
            )
            entries.append({
                "model": item["model"],
                "product": item["product"],
                "metric": item["metric"],
                "group": group_tag,
                "source": source_tag,
                "activated_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            })

        full_data[run_mode] = entries
        with open(grid_live_file, "w") as f:
            json.dump(full_data, f, indent=4)

        _sync_grid_to_activations(entries, mode=run_mode)

    _GRID_AUTO_LAST_FILL = now
    print(f"[PSB-AUTO] Source={automated_source} Grid empty -> populated {len(entries)} entries for bias {bias}")

def _prune_from_live_trades(mode: str, date_str: str) -> int:
    trade_dir = _resolve_day_dir(mode, date_str)
    live_file = trade_dir / "_live_trades.json"
    if not live_file.exists():
        return 0
    try:
        with open(live_file, "r") as f:
            data = json.load(f)
    except Exception:
        return 0
    trades = data.get("trades", [])
    removed_total = 0
    seen = set()
    for t in trades:
        if t.get("is_live_trade") is not True:
            continue
        model = t.get("source_strategy") or t.get("script_name") or t.get("app_name")
        product = t.get("product")
        if not model or not product:
            continue
        key = (model, str(product).upper())
        if key in seen:
            continue
        seen.add(key)
        res = _prune_grid_live_siblings(model, product, mode, reason="PERIODIC_SWEEP")
        removed_total += int(res.get("removed", 0) or 0)
    return removed_total

def _grid_auto_worker() -> None:
    while True:
        try:
            cfg = _load_config_safe()
            run_mode = str(cfg.get("run_mode", "live")).lower()
            date_str = datetime.now().strftime("%Y-%m-%d")
            _maybe_generate_market_update(run_mode, date_str, cfg)
            _auto_fill_grid_if_empty()
            _prune_from_live_trades(run_mode, date_str)
            _sync_open_trade_bias(run_mode, date_str)
            _force_close_wrong_bias_trades(run_mode, date_str)
            # [V20260214_1945] Ensure bucket leaders are promoted/synced
            _reconcile_active_buckets(mode=run_mode)
            _run_enabled_workflows(run_mode, date_str)
        except Exception as e:
            print(f"[GRID-AUTO] Error: {e}")
        time.sleep(15)


def _run_enabled_workflows(mode: str, date_str: str) -> None:
    data = _load_workflows()
    workflows = data.get("workflows", [])
    now_ts = time.time()

    for wf in workflows:
        if not isinstance(wf, dict):
            continue
        wf_id = str(wf.get("id") or "").strip()
        if not wf_id:
            continue
        if not _workflow_active_now(wf):
            continue

        cfg = wf.get("config", {}) if isinstance(wf.get("config"), dict) else {}
        run_interval = int(cfg.get("run_interval_sec", 900) or 900)

        last_ts = _WORKFLOW_LAST_RUN.get(wf_id, 0.0)
        if now_ts - last_ts < max(60, run_interval):
            continue

        if wf_id == "TB_workflow":
            max_buckets = int(cfg.get("max_buckets_per_day", 3) or 3)
            try:
                buckets_data = _load_trade_buckets(mode=mode, date_str=date_str)
                auto_count = len([
                    b for b in buckets_data.get("buckets", [])
                    if str(b.get("name", "")).startswith("AUTO_TB_")
                ])
            except Exception:
                auto_count = 0
            if auto_count >= max_buckets:
                continue
            result = _run_tb_workflow_once(mode, date_str, wf)
        elif wf_id == "profile_match_workflow":
            result = _run_profile_match_workflow_once(mode, date_str, wf)
        elif wf_id == "multi_chart_prune_negative_non_live":
            result = {"success": True, "message": "client-side workflow tick"}
        elif wf_id == "tb_prune_all_negative":
            result = _run_tb_prune_all_negative_once(mode, date_str, wf)
        elif wf_id == "top_x_multi_chart_workflow":
            result = _run_top_x_multi_chart_workflow(mode, date_str, wf)
        else:
            continue
        _WORKFLOW_LAST_RUN[wf_id] = now_ts
        if result.get("success"):
            print(f"[WORKFLOW] {wf_id} executed: {result}")
        else:
            print(f"[WORKFLOW] {wf_id} skipped/fail: {result.get('message')}")

def _sync_open_trade_bias(mode: str, date_str: str) -> int:
    """
    Force-sync market_bias_latest on open trade files to current targeted bias.
    This prevents stale bias values inside trade records.
    """
    bias = _get_current_bias(mode, date_str)
    if not bias:
        return 0
    changed = 0
    for day_dir in _iter_day_dirs_for(mode, date_str):
        for fp in day_dir.glob('*_op.json'):
            try:
                with open(fp, 'r') as f:
                    d = json.load(f) or {}
            except Exception:
                continue
            if str(d.get('status', '')).upper() != 'OPEN':
                continue
            if not bool(d.get('is_live_trade') or d.get('order_sent_net') or d.get('order_sent_alt')):
                continue
            if str(d.get('market_bias_latest') or '').upper() == bias:
                continue
            d['market_bias_latest'] = bias
            try:
                _atomic_write_json(fp, d, indent=2)
                changed += 1
            except Exception:
                continue
    return changed

def _force_close_wrong_bias_trades(mode: str, date_str: str) -> int:
    """
    Hard safety net: generate CLOSE tradeable orders for any open live trades
    that are misaligned with current market bias.
    """
    cfg = _load_config_safe()
    if not bool(cfg.get("enforce_market_bias_exit", False)):
        return 0

    bias = _get_current_bias(mode, date_str)
    if bias not in ("BUY", "SELL"):
        return 0
    order_dir = cfg.get("send_json_files_sim") if mode == "sim" else cfg.get("send_json_files")
    if not order_dir:
        order_dir = r"C:\Users\edebe\eds\trades_rt3_sim\orders" if mode == "sim" else r"C:\Users\edebe\eds\trades_rt3\orders"
    order_path = Path(order_dir)
    order_path.mkdir(parents=True, exist_ok=True)

    forced = 0
    now_iso = datetime.now().isoformat()
    now_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    for day_dir in _iter_day_dirs_for(mode, date_str):
        for fp in day_dir.glob('*_op.json'):
            try:
                with open(fp, 'r') as f:
                    d = json.load(f) or {}
            except Exception:
                continue
            if str(d.get('status', '')).upper() != 'OPEN':
                continue
            if not bool(d.get('is_live_trade') or d.get('order_sent_net') or d.get('order_sent_alt')):
                continue
            if d.get('bias_exit_close_sent_at'):
                continue

            direction = str(d.get('direction') or '').upper()
            aligned = ((bias == 'BUY' and direction in ('LONG', 'BUY')) or (bias == 'SELL' and direction in ('SHORT', 'SELL')))
            if aligned:
                continue

            action = 'SELL' if direction in ('LONG', 'BUY') else 'BUY'
            product = str(d.get('product') or '').upper()
            strategy = str(d.get('script_name') or d.get('source_strategy') or 'unknown')
            trade_id = d.get('trade_id') or d.get('id') or 0
            close_filename = f"{product}_{strategy}_{action}_{now_tag}_bias_exit_close_tradeable.json"
            close_file = order_path / close_filename
            order_payload = {
                "symbol": product,
                "secType": "CASH",
                "exchange": "IDEALPRO",
                "currency": "USD",
                "action": action,
                "orderType": "MKT",
                "quantity": _trade_quantity_for_product(product, cfg),
                "guidePrice": float(d.get("current_price") or d.get("entry_price") or 0.0),
                "comment": f"{strategy} NET CLOSE #{trade_id} (Bias Exit API)",
                "source": d.get("source_screen") or "grid_live",
                "source_group": d.get("source_group"),
                "guid": d.get("guid") or "unknown"
            }
            try:
                _atomic_write_json(close_file, order_payload, indent=2)
                d['market_bias_latest'] = bias
                d['bias_exit_close_sent_at'] = now_iso
                d['bias_exit_target_bias'] = bias
                d['bias_exit_close_file'] = close_filename
                _atomic_write_json(fp, d, indent=2)
                forced += 1
                print(f"[BIAS-FORCE-CLOSE] {fp.name} -> {close_filename} (bias={bias}, direction={direction})")
            except Exception as e:
                print(f"[BIAS-FORCE-CLOSE-ERROR] {fp.name}: {e}")
                continue
    return forced

def _start_grid_auto_worker() -> None:
    t = threading.Thread(target=_grid_auto_worker, daemon=True, name="grid-auto-worker")
    t.start()

def _any_trade_bucket_is_live(mode):
    """[V20260204_1410] Check if any bucket in the current run mode is Live."""
    try:
        data = _load_trade_buckets(mode=mode)
        buckets = data.get('buckets', [])
        return any(b.get('live') for b in buckets)
    except:
        return False

def _deactivate_all_trade_buckets(mode):
    """[V20260204_1410] For mutual exclusion: deactivate all buckets when Frequency is re-enabled."""
    try:
        data = _load_trade_buckets(mode=mode)
        buckets = data.get('buckets', [])
        changed = False
        for b in buckets:
            if b.get('live'):
                b['live'] = False
                changed = True
        if changed:
            _save_trade_buckets(data, mode=mode)
            print(f"[BUCKET] Deactivated all {mode} buckets due to Frequency overrule.")
    except Exception as e:
        print(f"[BUCKET-ERROR] Deactivation failed: {e}")

def _normalize_tb_metric(metric_raw: Any) -> str:
    raw = str(metric_raw or 'net').strip().lower()
    if raw in ('buy', 'buy_net', 'buy_net_return_sum'):
        return 'buy_net'
    if raw in ('sell', 'sell_net', 'sell_net_return_sum'):
        return 'sell_net'
    if raw in ('alt', 'alt_net', 'alt_net_return_sum'):
        return 'alt_net'
    return 'net'


def _tb_metric_value(point: dict, metric_raw: Any) -> float:
    metric_key = _normalize_tb_metric(metric_raw)
    try:
        return float(point.get(metric_key, point.get('net', 0.0)) or 0.0)
    except Exception:
        return 0.0


def _normalize_delta_type(delta_type_raw: Any) -> str:
    raw = str(delta_type_raw or "delta2").strip().lower()
    return "delta1" if raw == "delta1" else "delta2"


def _calculate_bucket_strat_perf(strat_entry, baseline_time_str, summary_net, delta_type='delta2'):
    """[V20260320_1300] Respect delta_type for leadership calculation."""
    try:
        if isinstance(strat_entry, dict):
            strat_key = str(strat_entry.get('key') or '').strip()
            metric_raw = strat_entry.get('metric', 'net')
        else:
            strat_key = str(strat_entry or '').strip()
            metric_raw = 'net'
        if not strat_key:
            return -999999.0
        strat_name_only = strat_key.split(' | ')[0]
        product_only = strat_key.split(' | ')[1]
        series = summary_net.get(strat_name_only, {}).get(product_only, [])
        
        current_total = 0.0
        if series:
            current_total = _tb_metric_value(series[-1], metric_raw)
        
        # [V20260320_1300] Handle Delta 1 (Profit since Midnight)
        if delta_type == 'delta1':
            day_baseline = 0.0
            if series:
                day_baseline = _tb_metric_value(series[0], metric_raw)
            return round(current_total - day_baseline, 2)

        # Default: Delta 2 (Profit since creation/baseline)
        baseline = 0.0
        if baseline_time_str and series:
            try:
                clean_start = baseline_time_str.replace('Z', '').replace(' ', 'T')
                start_dt = datetime.fromisoformat(clean_start)
                for point in series:
                    p_time = point.get('t', '').replace('Z', '').replace(' ', 'T')
                    p_dt = datetime.fromisoformat(p_time)
                    if p_dt <= start_dt:
                        baseline = _tb_metric_value(point, metric_raw)
                    else: break
            except: pass
        return round(current_total - baseline, 2)
    except: return -999999.0

def _get_bucket_top2_stats(bucket: dict, summary_net: dict, start_time_str: str, delta_type='delta2'):
    """
    Return top-2 leaderboard stats for a bucket using net-diff since the        
    canonical chart baseline/start_from time.
    """
    scored = []
    for s in bucket.get('strategies', []):
        k = s.get('key')
        if not k:
            continue
        # [V20260320_1300] Propagate delta_type to perf calc
        diff = _calculate_bucket_strat_perf(s, start_time_str, summary_net, delta_type=delta_type)     
        scored.append((k, diff, s))
    if not scored:
        return None, -999999.0, -999999.0, -999999.0, 0, None
    scored.sort(key=lambda x: x[1], reverse=True)
    top_key, top_diff, top_entry = scored[0]
    second_diff = scored[1][1] if len(scored) > 1 else None
    gap = (top_diff - second_diff) if second_diff is not None else None
    return top_key, top_diff, second_diff, gap, len(scored), top_entry

def _bucket_passes_threshold(top_diff: float, second_diff: float, gap_diff: float, min_diff: float) -> bool:
    """
    Threshold rule:
    - 2+ strategies: require gap(top-second) >= min_diff
    - 1 strategy only: require top_diff >= min_diff
    """
    if second_diff is None:
        return top_diff >= min_diff
    return (gap_diff is not None) and (gap_diff >= min_diff)


def _resolve_tb_metric(bucket: dict, leader_entry: Optional[dict] = None) -> str:
    """
    Resolve Trade Bucket metric for grid promotion.
    Rules:
    - If TB explicitly selected buy_net/sell_net, preserve it.
    - If TB selected total_net/net, preserve as net (both sides).
    - Fallback to net when unknown.
    """
    if not isinstance(bucket, dict):
        return "net"

    def _norm_metric(val: Any) -> Optional[str]:
        raw = str(val or "").strip().lower()
        if raw in ("buy_net", "sell_net", "net", "total_net"):
            return "net" if raw == "total_net" else raw
        return None

    if isinstance(leader_entry, dict):
        m = _norm_metric(leader_entry.get("metric"))
        if m:
            return m

    for key in ("metric", "selected_metric", "selection_metric", "leader_metric"):
        m = _norm_metric(bucket.get(key))
        if m:
            return m

    return "net"

def _sync_bucket_to_grid_live(bucket: dict, mode: str, date_str: str):
    """[V20260204_1410] Replaces _sync_bucket_to_activations. Updates grid_live.json instead."""
    try:
        bucket_name = bucket.get('name')
        bucket_live = bucket.get('live', False)
        
        # [V20260205_2100] Check if Trade Bucket source is allowed for automated sync
        if bucket_live and not _is_source_allowed('Trade Bucket'):
            print(f"[BUCKET] Sync skipped for '{bucket_name}': Trade Bucket is not the current automated source.")
            return

        # [V20260216_0001] Enforce same-day bucket rule:
        # only buckets from today's date can be promoted to grid_live.
        today_str = datetime.now().strftime('%Y-%m-%d')
        if bucket_live and str(date_str) != today_str:
            print(f"[BUCKET] Skip promotion for '{bucket_name}': bucket date={date_str} != today={today_str}.")
            bucket_live = False

        # 1. Archive current state (already done in update_trade_bucket but good to be safe)
        _archive_grid_live(mode)
        
        grid_live_file = ROOT_PATH / "grid_live.json"
        
        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            if grid_live_file.exists():
                try:
                    with open(grid_live_file, "r") as f:
                        full_data = json.load(f)
                    if isinstance(full_data, list): # Migrate legacy
                        full_data = {'live': full_data, 'sim': []}
                except: pass
            
            # 2. Remove previous items from THIS bucket AND ALL Frequency items (Mutual Exclusion)
            # [V20260204_2130] Prefix with TB_
            source_tag = f"TB_{bucket_name}"
            target_list = full_data.get(mode, [])
            
            # Clean list: remove this bucket's items (handle both raw and TB_ prefixed for transition)
            new_target_list = [m for m in target_list if m.get('source') not in (source_tag, bucket_name)]
            if bucket_live:
                 # If activating bucket, clear ALL frequency/rank_alert items
                 new_target_list = [m for m in new_target_list 
                                   if not str(m.get('source', '')).startswith(('rank_alert', 'frequency'))]
            
            # 3. If bucket live, find and add Leader
            if bucket_live:
                summary_file = _resolve_day_dir(mode, date_str) / "_summary_net.json"
                summary_net = {}
                if summary_file.exists():
                    try:
                        with open(summary_file, 'r') as f:
                            summary_net = json.load(f).get('strategies', {})
                    except: pass
                
                min_diff = float(bucket.get('minimum_difference', 5.0))
                start_time_str = bucket.get('chart_start_time') or bucket.get('start_time')
                # [V20260320_1300] Pass bucket-level delta_type to leader stats
                b_delta_type = _normalize_delta_type(bucket.get('delta_type'))
                top_strat_key, max_diff, second_diff, gap_diff, n_scored, top_entry = _get_bucket_top2_stats(
                    bucket, summary_net, start_time_str, delta_type=b_delta_type
                )

                if top_strat_key and _bucket_passes_threshold(max_diff, second_diff, gap_diff, min_diff):
                    parsed = _parse_strategy_key(top_strat_key)
                    if parsed:
                        tb_metric = _resolve_tb_metric(bucket, top_entry)
                        print(f"[BUCKET] Promoting Leader from '{bucket_name}': {top_strat_key} (Top={max_diff}, Second={second_diff}, Gap={gap_diff})")
                        now_local = datetime.now().isoformat().split('.')[0]
                        new_entry = {
                            "model": top_strat_key.split(' | ')[0],
                            "product": parsed['product'],
                            "metric": tb_metric,
                            "group": bucket_name,
                            "source": source_tag,
                            "activated_at": now_local
                        }
                        new_target_list.append(new_entry)
                else:
                    print(
                        f"[BUCKET] No candidate meets threshold in '{bucket_name}' "
                        f"(Top={max_diff}, Second={second_diff}, Gap={gap_diff}, MinGap={min_diff}, N={n_scored})"
                    )
            
            # 4. Save and Sync
            full_data[mode] = new_target_list
            with open(grid_live_file, "w") as f:
                json.dump(full_data, f, indent=4)
            
            _sync_grid_to_activations(new_target_list, mode=mode)
            
    except Exception as e:
        print(f"[BUCKET-SYNC-ERROR] {e}")

def _reconcile_active_buckets(mode: str = 'live'):
    """
    [V20260204_2120] Background/Periodic reconciler for Trade Buckets.
    Ensures that if buckets are live:
    1. Stale frequency/rank_alert items are purged from grid_live.json (Mutual Exclusion).
    2. Bucket leaders meeting threshold are automatically promoted to grid_live.json if missing.
    """
    try:
        date_str = datetime.now().strftime('%Y-%m-%d')
        buckets_data = _load_trade_buckets(mode=mode, date_str=date_str)
        buckets = buckets_data.get('buckets', [])
        auto_deactivated, cap = _enforce_max_live_tb_inplace(buckets)
        if auto_deactivated:
            _save_trade_buckets(buckets_data, mode=mode, date_str=date_str)
            for b in auto_deactivated:
                _sync_bucket_to_grid_live({'name': b.get('name'), 'live': False}, mode, date_str)
            print(f"[RECONCILE] max_live_tb={cap} enforced; auto-deactivated {len(auto_deactivated)} bucket(s).")

        def _bucket_is_same_day(bucket: dict, day_str: str) -> bool:
            # Primary: use bucket start_time date when parseable
            start_time = str(bucket.get('start_time') or '').strip()
            if start_time:
                try:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', ''))
                    return start_dt.strftime('%Y-%m-%d') == day_str
                except Exception:
                    pass
            # Fallback: if unparseable, trust file scope date only.
            return True

        live_buckets_all = [b for b in buckets if b.get('live')]
        live_buckets = [b for b in live_buckets_all if _bucket_is_same_day(b, date_str)]
        
        if not live_buckets:
            return # No active buckets to reconcile
            
        # [V20260205_2100] Check if Trade Bucket source is allowed for automated sync
        if not _is_source_allowed('Trade Bucket'):
            return

        grid_live_file = ROOT_PATH / "grid_live.json"
        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            if grid_live_file.exists():
                try:
                    with open(grid_live_file, "r") as f:
                        full_data = json.load(f)
                    if isinstance(full_data, list):
                        full_data = {'live': full_data, 'sim': []}
                except: pass
            
            target_list = full_data.get(mode, [])
            changed = False
            
            # 1. Mutual Exclusion: Clear ALL frequency/rank_alert AND manual UI items if buckets are live
            # [V20260204_2155] Added 'ui' to purge list to ensure bucket priority.
            original_len = len(target_list)
            target_list = [m for m in target_list 
                          if not str(m.get('source', '')).startswith(('rank_alert', 'frequency', 'ui'))]
            if len(target_list) != original_len:
                print(f"[RECONCILE] Purged {original_len - len(target_list)} stale frequency/UI items (Buckets active)")
                changed = True

            # [V20260216_0001] Same-day rule + stale TB purge:
            # keep TB entries only for currently live buckets from today's bucket set.
            allowed_tb_sources = set()
            for b in live_buckets:
                bn = b.get('name')
                if bn:
                    allowed_tb_sources.add(f"TB_{bn}")
                    allowed_tb_sources.add(str(bn))
            before_tb = len(target_list)
            target_list = [
                m for m in target_list
                if (not str(m.get('source', '')).startswith('TB_')) or (str(m.get('source', '')) in allowed_tb_sources)
            ]
            if len(target_list) != before_tb:
                print(f"[RECONCILE] Purged {before_tb - len(target_list)} stale TB entries (date mismatch/non-live).")
                changed = True
                
            # 2. Evaluate and Promote Leaders for each live bucket
            summary_file = _resolve_day_dir(mode, date_str) / "_summary_net.json"
            summary_net = {}
            if summary_file.exists():
                try:
                    with open(summary_file, 'r') as f:
                        summary_net = json.load(f).get('strategies', {})
                except: pass
            
            for bucket in live_buckets:
                bucket_name = bucket.get('name')
                # [V20260204_2130] Prefix with TB_
                source_tag = f"TB_{bucket_name}"
                min_diff = float(bucket.get('minimum_difference', 5.0))
                start_time_str = bucket.get('chart_start_time') or bucket.get('start_time')
                
                # [V20260320_1300] Pass bucket-level delta_type to leader stats
                b_delta_type = _normalize_delta_type(bucket.get('delta_type'))
                # Find current leader in THIS bucket (top-2 gap logic)
                top_strat_key, max_diff, second_diff, gap_diff, n_scored, top_entry = _get_bucket_top2_stats(
                    bucket, summary_net, start_time_str, delta_type=b_delta_type
                )
                
                # Check if this bucket already has an item in the grid (Check both raw and TB_)
                existing_for_bucket = [m for m in target_list if m.get('source') in (source_tag, bucket_name)]
                
                if top_strat_key and _bucket_passes_threshold(max_diff, second_diff, gap_diff, min_diff):
                    parsed = _parse_strategy_key(top_strat_key)
                    if parsed:
                        tb_metric = _resolve_tb_metric(bucket, top_entry)
                        # Check if matched model/product is already in grid for THIS bucket
                        already_promoted = any(
                            m.get('model') == parsed['strategy'] and 
                            m.get('product') == parsed['product'] 
                            for m in existing_for_bucket
                        )
                        
                        if not already_promoted:
                            # Remove any OLD leaders from this same bucket (both formats)
                            target_list = [m for m in target_list if m.get('source') not in (source_tag, bucket_name)]
                            
                            now_local = datetime.now().isoformat().split('.')[0]
                            new_entry = {
                                "model": top_strat_key.split(' | ')[0],
                                "product": parsed['product'],
                                "metric": tb_metric,
                                "group": bucket_name,
                                "source": source_tag,
                                "activated_at": now_local
                            }
                            target_list.append(new_entry)
                            print(f"[RECONCILE] Promoting new leader from '{bucket_name}': {top_strat_key} (Top={max_diff}, Second={second_diff}, Gap={gap_diff})")
                            changed = True
                else:
                    if existing_for_bucket:
                        # Remove if no longer meeting threshold (both formats)
                        target_list = [m for m in target_list if m.get('source') not in (source_tag, bucket_name)]
                        print(
                            f"[RECONCILE] Removing member for '{bucket_name}' - no strategy meets threshold "
                            f"(Top={max_diff}, Second={second_diff}, Gap={gap_diff}, MinGap={min_diff}, N={n_scored})."
                        )
                        changed = True

            # 3. Save if changed
            if changed:
                full_data[mode] = target_list
                with open(grid_live_file, "w") as f:
                    json.dump(full_data, f, indent=4)
                _sync_grid_to_activations(target_list, mode=mode)
                
    except Exception as e:
        print(f"[RECONCILE-ERROR] Failed to reconcile buckets: {e}")


def _bucket_sort_ts(bucket: dict) -> float:
    """Best-effort timestamp for deterministic live-bucket cap ordering."""
    for key in ('start_time', 'chart_start_time'):
        raw = str(bucket.get(key) or '').strip()
        if not raw:
            continue
        try:
            return datetime.fromisoformat(raw.replace('Z', '')).timestamp()
        except Exception:
            continue
    return 0.0


def _get_max_live_tb() -> int:
    """Read max live trade-bucket cap from config with safe default."""
    cfg = _load_config_safe()
    try:
        value = int(cfg.get('max_live_tb', 5) or 5)
    except Exception:
        value = 5
    return max(1, value)


def _enforce_max_live_tb_inplace(buckets: List[dict], preferred_live_name: Optional[str] = None) -> Tuple[List[dict], int]:
    """
    Enforce max live TB cap in-place on bucket list.
    Keeps preferred bucket live (if requested), then keeps newest by start_time.
    Returns (auto_deactivated_buckets, max_live_tb).
    """
    cap = _get_max_live_tb()
    live = [b for b in buckets if bool(b.get('live'))]
    if len(live) <= cap:
        return [], cap

    live_sorted = sorted(
        live,
        key=lambda b: (_bucket_sort_ts(b), str(b.get('name') or '')),
        reverse=True
    )
    keep_names: List[str] = []
    if preferred_live_name:
        pref = str(preferred_live_name)
        if any(str(b.get('name')) == pref for b in live_sorted):
            keep_names.append(pref)
    for b in live_sorted:
        name = str(b.get('name') or '')
        if not name or name in keep_names:
            continue
        if len(keep_names) >= cap:
            break
        keep_names.append(name)

    keep_set = set(keep_names)
    auto_deactivated: List[dict] = []
    for b in buckets:
        if bool(b.get('live')) and str(b.get('name') or '') not in keep_set:
            b['live'] = False
            auto_deactivated.append(b)
    return auto_deactivated, cap


@app.route("/sidebar-loader.js")
def serve_sidebar_loader_js():
    return send_from_directory(ROOT_PATH, "sidebar-loader.js")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Trade Buckets API (File-Based) [V20260122_FS]
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _get_trade_buckets_path(mode: str, date_str: str, product_type: str | None = None) -> Path:
    """Get path to trade buckets file."""
    return _resolve_day_dir(mode, date_str, product_type=product_type) / "_trade_buckets.json"


def _load_trade_buckets(mode: str = 'live', date_str: str = None, product_type: str | None = None) -> dict:
    """Load trade buckets from JSON file."""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    bucket_file = _get_trade_buckets_path(mode, date_str, product_type=product_type)

    if bucket_file.exists():
        try:
            with open(bucket_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading trade buckets: {e}")

    return {"buckets": []}


def _log_top10_history_snapshot(mode: str, date_str: str, product_type: str | None, top_x_list: List[dict]):
    """
    [V20260323_1645] Append Top 10 snapshot to history every 5 minutes.
    Part of task: historical_top10_logging
    """
    if not top_x_list:
        return

    day_dirs = _iter_day_dirs_for(mode, date_str, product_type)
    if not day_dirs:
        return
    
    target_file = day_dirs[0] / "_top10_history.json"
    now_dt = datetime.now()
    
    # Load existing history
    history_data = {"version": "V20260323_1645", "history": []}
    if target_file.exists():
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
        except: pass

    # Ensure 5-minute interval
    if history_data.get("history"):
        last_entry = history_data["history"][-1]
        try:
            last_ts = datetime.fromisoformat(last_entry["timestamp"])
            if (now_dt - last_ts).total_seconds() < 290: # Slightly under 300s to allow for slight jitter
                return
        except: pass

    # Prepare Top 10 (ensure exactly 10 and only key fields)
    top10 = []
    for e in top_x_list[:10]:
        top10.append({
            "strategy": e.get("strategy"),
            "product": e.get("product"),
            "net": float(e.get("total_net", 0.0) or 0.0),
            "pick_now": bool(e.get("pick_now", False))
        })

    history_data["history"].append({
        "timestamp": now_dt.isoformat(),
        "top10": top10
    })
    history_data["updated_at"] = now_dt.isoformat()
    history_data["date"] = date_str

    try:
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to update Top 10 history: {e}")

@app.route('/api/top10_history', methods=['GET'])
def get_top10_history():
    """Returns the historical Top 10 snapshots for evaluation."""
    try:
        mode = request.args.get('mode', 'live').lower()
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = request.args.get('product_type')
        
        day_dirs = _iter_day_dirs_for(mode, date_str, product_type)
        if not day_dirs:
            return jsonify({'success': False, 'message': 'No data directory found'}), 404
            
        target_file = day_dirs[0] / "_top10_history.json"
        if not target_file.exists():
            return jsonify({'success': False, 'message': '_top10_history.json not found'}), 404
            
        with open(target_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return jsonify({
            'success': True,
            'history': data.get('history', [])
        })
    except Exception as e:
        print(f"[ERROR] get_top10_history: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def _save_trade_buckets(data: dict, mode: str = 'live', date_str: str = None, product_type: str | None = None):
    """Save trade buckets to JSON file."""
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    bucket_file = _get_trade_buckets_path(mode, date_str, product_type=product_type)

    # Ensure directory exists
    bucket_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(bucket_file, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving trade buckets: {e}")


@app.route('/api/trade_buckets', methods=['GET'])
def get_trade_buckets():
    """
    Get all trade buckets with stats.
    [V20260214_2000] Enhanced logging and robust parsing.
    """
    try:
        raw_mode = request.args.get('mode', 'live')
        mode = raw_mode.lower()
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = request.args.get('product_type')

        # Log request parameters for debugging
        print(f"[TRADE-BUCKETS] Request: mode='{mode}' (raw='{raw_mode}'), date='{date_str}', product_type='{product_type}'")

        data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        buckets = data.get('buckets', [])

        
        if not buckets:
            print(f"[TRADE-BUCKETS] No buckets found for {mode}/{date_str}")

        def _load_summary_strategies_for_date(_mode: str, _date: str, _product_type: str | None) -> dict:
            fpath = _resolve_day_dir(_mode, _date, product_type=_product_type) / "_summary_net.json"
            if not fpath.exists():
                return {}
            try:
                with open(fpath, 'r') as f:
                    return (json.load(f) or {}).get('strategies', {}) or {}
            except Exception as e:
                print(f"[TRADE-BUCKETS-ERROR] Failed to load summary_net from {fpath}: {e}")
                return {}

        def _latest_mode_date(_mode: str, _product_type: str | None) -> str:
            try:
                base = _resolve_day_dir(_mode, date_str, product_type=_product_type).parent
                if not base.exists():
                    return date_str
                dates = []
                for p in base.iterdir():
                    if p.is_dir():
                        n = p.name
                        if len(n) == 10 and n[4] == '-' and n[7] == '-':
                            dates.append(n)
                if not dates:
                    return date_str
                return sorted(dates)[-1]
            except Exception:
                return date_str

        # Baseline compatibility uses requested date; current net uses latest available date.
        summary_net_baseline = _load_summary_strategies_for_date(mode, date_str, product_type)
        latest_date = _latest_mode_date(mode, product_type)
        summary_net_current = _load_summary_strategies_for_date(mode, latest_date, product_type)
        if not summary_net_current:
            summary_net_current = summary_net_baseline

        def _normalize_bucket_metric(metric_raw: str) -> str:
            raw = str(metric_raw or 'net').strip().lower()
            if raw in ('buy', 'buy_net', 'buy_net_return_sum'):
                return 'buy_net'
            if raw in ('sell', 'sell_net', 'sell_net_return_sum'):
                return 'sell_net'
            if raw in ('alt', 'alt_net', 'alt_net_return_sum'):
                return 'alt_net'
            return 'net'

        def _metric_value(point: dict, metric_raw: str) -> float:
            key = _normalize_bucket_metric(metric_raw)
            try:
                return float(point.get(key, point.get('net', 0.0)) or 0.0)
            except Exception:
                return 0.0

        # Update bucket stats from summary data
        for bucket in buckets:
            if 'open_trades' not in bucket:
                bucket['open_trades'] = False
            if 'open_trade_count' not in bucket:
                bucket['open_trade_count'] = 0
            if 'live' not in bucket:
                bucket['live'] = False
            bucket_delta_type = _normalize_delta_type(bucket.get('delta_type'))

            start_dt = None
            chart_start_dt = None
            start_time_str = bucket.get('start_time')
            chart_start_time_str = bucket.get('chart_start_time')
            
            if start_time_str:
                try:
                    start_dt = datetime.fromisoformat(start_time_str.replace('Z', ''))
                except:
                    pass
            if chart_start_time_str:
                try:
                    chart_start_dt = datetime.fromisoformat(chart_start_time_str.replace('Z', ''))
                except:
                    pass

            for strat in bucket.get('strategies', []):
                strat_key = strat.get('key', '')
                metric_raw = str(strat.get('metric', 'net') or 'net')
                
                # Robust parsing: try ' | ' first, then '|'
                parts = strat_key.split(' | ')
                if len(parts) != 2:
                    parts = strat_key.split('|')
                
                if len(parts) == 2:
                    strategy_name = parts[0].strip()
                    product = parts[1].strip()
                    
                    # Current net should reflect latest available summary data for this mode.
                    series = summary_net_current.get(strategy_name, {}).get(product, [])
                    if not series and summary_net_current:
                        # Log missing strategy/product only if summary exists but key is missing
                        # print(f"[TRADE-BUCKETS-DEBUG] Missing series for {strategy_name} | {product}")
                        pass

                    current_total = 0.0
                    if series:
                        current_total = _metric_value(series[-1], metric_raw)

                    # [V20260319_2115] Determine day-start baseline to normalize display to '0.00' start
                    day_baseline = 0.0
                    baseline_series = summary_net_baseline.get(strategy_name, {}).get(product, [])
                    if baseline_series:
                        day_baseline = _metric_value(baseline_series[0], metric_raw)

                    # Prefer immutable baseline captured at bucket creation.
                    baseline_val = strat.get('net_at_creation', None)
                    if baseline_val is None:
                        # Backward compatibility for legacy buckets without snapshot baseline.
                        baseline_val = 0.0
                        if start_dt and baseline_series:
                            for point in baseline_series:
                                point_time_str = point.get('t', '')
                                try:
                                    point_dt = datetime.fromisoformat(point_time_str.replace('Z', ''))
                                    if point_dt <= start_dt:
                                        baseline_val = _metric_value(point, metric_raw)
                                    else:
                                        break
                                except:
                                    pass

                    # [V20260319_2115] Chart start baseline for 'Start' column normalization
                    chart_baseline_val = 0.0
                    if chart_start_dt and baseline_series:
                        for point in baseline_series:
                            point_dt_str = point.get('t', '')
                            try:
                                p_dt = datetime.fromisoformat(point_dt_str.replace('Z', ''))
                                if p_dt <= chart_start_dt:
                                    chart_baseline_val = _metric_value(point, metric_raw)
                                else: break
                            except: pass
                    else:
                        chart_baseline_val = day_baseline

                    # [V20260319_2135] Map metrics to Delta1 and Delta2 for UI standardization
                    strat['start_from_net'] = 0.0
                    strat['net_at_creation'] = round(float(baseline_val) - day_baseline, 2)
                    strat['current_total_net'] = round(float(current_total) - day_baseline, 2)
                    strat['delta1'] = strat['current_total_net'] # Profit since Midnight
                    strat['delta2'] = round(strat['current_total_net'] - strat['net_at_creation'], 2) # Profit since Creation
                    strat['delta_type'] = _normalize_delta_type(strat.get('delta_type') or bucket_delta_type)
                    strat['total_net'] = strat['delta1'] if bucket_delta_type == 'delta1' else strat['delta2']

        return jsonify({
            'success': True,
            'buckets': buckets,
            'max_strategies': 5
        })
    except Exception as e:
        print(f"[TRADE-BUCKETS-CRITICAL] Error in get_trade_buckets: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets', methods=['POST'])
def create_trade_bucket():
    """Create a new trade bucket."""
    try:
        import uuid
        payload = request.json
        name = payload.get('name')
        strategies = payload.get('strategies', [])
        mode = payload.get('mode', 'live')
        product_type = payload.get('product_type')
        delta_type = _normalize_delta_type(payload.get('delta_type'))

        start_time_str = payload.get('start_time')
        chart_start_time_str = payload.get('chart_start_time')
        payload_date = str(payload.get('date', '')).strip()
        current_date_str = datetime.now().strftime('%Y-%m-%d')

        # Prefer explicit UI-selected trade date when provided.
        if payload_date:
            try:
                datetime.strptime(payload_date, '%Y-%m-%d')
                current_date_str = payload_date
            except Exception:
                pass

        if start_time_str and not payload_date:
            try:
                if start_time_str.endswith('Z'):
                    dt = datetime.fromisoformat(start_time_str[:-1])
                else:
                    dt = datetime.fromisoformat(start_time_str)
                current_date_str = dt.strftime('%Y-%m-%d')
            except:
                pass
        bias_at_creation = _get_current_bias(mode, current_date_str) or "UNKNOWN"

        data = _load_trade_buckets(mode=mode, date_str=current_date_str, product_type=product_type)
        buckets = data.get('buckets', [])

        # Snapshot summary_net at bucket creation time so baseline is static.
        summary_file = _resolve_day_dir(mode, current_date_str, product_type=product_type) / "_summary_net.json"
        summary_net = {}
        if summary_file.exists():
            try:
                with open(summary_file, 'r') as f:
                    summary_data = json.load(f)
                    summary_net = summary_data.get('strategies', {})
            except Exception as e:
                print(f"[TRADE-BUCKETS-WARN] create snapshot load failed: {e}")

        chart_start_dt = None
        if chart_start_time_str:
            try:
                chart_start_dt = datetime.fromisoformat(str(chart_start_time_str).replace('Z', ''))
            except Exception:
                chart_start_dt = None

        creation_dt = None
        if start_time_str:
            try:
                creation_dt = datetime.fromisoformat(str(start_time_str).replace('Z', ''))
            except Exception:
                creation_dt = None

        def _normalize_bucket_metric(metric_raw: str) -> str:
            raw = str(metric_raw or 'net').strip().lower()
            if raw in ('buy', 'buy_net', 'buy_net_return_sum'):
                return 'buy_net'
            if raw in ('sell', 'sell_net', 'sell_net_return_sum'):
                return 'sell_net'
            if raw in ('alt', 'alt_net', 'alt_net_return_sum'):
                return 'alt_net'
            return 'net'

        def _metric_value(point: dict, metric_raw: str) -> float:
            key = _normalize_bucket_metric(metric_raw)
            try:
                return float(point.get(key, point.get('net', 0.0)) or 0.0)
            except Exception:
                return 0.0

        def _net_at_or_before(series: list, target_dt: datetime, metric_raw: str):
            if not series or not target_dt:
                return None
            val = None
            for p in series:
                ts = p.get('t')
                if not ts:
                    continue
                try:
                    p_dt = datetime.fromisoformat(str(ts).replace('Z', ''))
                except Exception:
                    continue
                if p_dt <= target_dt:
                    val = _metric_value(p, metric_raw)
                else:
                    break
            return val

        def _creation_net_for_key(strat_key: str, metric_raw: str) -> float:
            parts = str(strat_key or '').split(' | ')
            if len(parts) != 2:
                parts = str(strat_key or '').split('|')
            if len(parts) != 2:
                return 0.0
            strategy_name = parts[0].strip()
            product = parts[1].strip()
            series = summary_net.get(strategy_name, {}).get(product, [])
            if not series:
                return 0.0
            # [V20260319_2125] Use creation_dt (the Cyan Dot logic) to find the exact baseline net
            if creation_dt:
                v = _net_at_or_before(series, creation_dt, metric_raw)
                if v is not None:
                    return float(v)
            return _metric_value(series[-1], metric_raw)

        def _start_from_net_for_key(strat_key: str, fallback_creation: float, metric_raw: str) -> float:
            if not chart_start_dt:
                return float(fallback_creation)
            parts = str(strat_key or '').split(' | ')
            if len(parts) != 2:
                parts = str(strat_key or '').split('|')
            if len(parts) != 2:
                return float(fallback_creation)
            strategy_name = parts[0].strip()
            product = parts[1].strip()
            series = summary_net.get(strategy_name, {}).get(product, [])
            v = _net_at_or_before(series, chart_start_dt, metric_raw)
            if v is None:
                # [V20260319_1445] If no history before chart start, assume 0.0 baseline to allow delta calculation
                return 0.0
            return float(v)

        if not name:
            return jsonify({'success': False, 'message': 'Bucket name is required'}), 400

        if any(b['name'] == name for b in buckets):
            return jsonify({'success': False, 'message': 'Bucket with this name already exists'}), 400

        bucket_guid = str(uuid.uuid4())

        processed_strategies = []
        for strat in strategies:
            strategy_id = str(uuid.uuid4())
            if isinstance(strat, dict):
                strat_key = strat.get('key') or strat.get('strategy') or ''
                metric_raw = str(strat.get('metric', 'net') or 'net')
                creation_net = round(_creation_net_for_key(strat_key, metric_raw), 2)
                start_from_net = round(_start_from_net_for_key(strat_key, creation_net, metric_raw), 2)
                strat['strategy_id'] = strategy_id
                strat['bias_at_creation'] = bias_at_creation
                strat['start_from_net'] = start_from_net
                strat['net_at_creation'] = creation_net
                strat['current_total_net'] = creation_net
                strat['net_delta_from_creation'] = 0.0
                strat['total_net'] = 0.0
                strat['delta_type'] = delta_type
                processed_strategies.append(strat)
            else:
                raw_strat = str(strat or '')
                parts = raw_strat.split(' | ')
                if len(parts) < 3:
                    parts = [p.strip() for p in raw_strat.split('|')]
                metric_raw = parts[2] if len(parts) >= 3 else 'net'
                key_only = ' | '.join(parts[:2]) if len(parts) >= 2 else raw_strat
                creation_net = round(_creation_net_for_key(key_only, metric_raw), 2)
                start_from_net = round(_start_from_net_for_key(key_only, creation_net, metric_raw), 2)
                processed_strategies.append({
                    'strategy_id': strategy_id,
                    'key': key_only,
                    'metric': metric_raw,
                    'bias_at_creation': bias_at_creation,
                    'start_from_net': start_from_net,
                    'net_at_creation': creation_net,
                    'current_total_net': creation_net,
                    'net_delta_from_creation': 0.0,
                    'total_net': 0.0,  # backward-compatible alias for net delta
                    'delta_type': delta_type,
                    'live_trade_net': 0.0
                })

        if len(processed_strategies) < 2:
            return jsonify({'success': False, 'message': 'Minimum 2 strategies/metrics required for a Trade Bucket [V20260311_1215]'}), 400

        new_bucket = {
            'bucket_id': bucket_guid,
            'name': name,
            'start_time': payload.get('start_time') or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chart_start_time': chart_start_time_str,
            'mode': mode,
            'product_type': product_type or default_product_type(_load_layout_runtime_config()),
            'delta_type': delta_type,
            'market_bias_at_creation': bias_at_creation,
            'strategies': processed_strategies,
            'live': False,
            'open_trades': False,
            'open_trade_count': 0,
            'minimum_difference': float(payload.get('minimum_difference', 5.0))
        }

        buckets.append(new_bucket)
        data['buckets'] = buckets

        _save_trade_buckets(data, mode=mode, date_str=current_date_str, product_type=product_type)

        return jsonify({'success': True, 'bucket': new_bucket})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets/update', methods=['POST'])
def update_trade_bucket():
    """Update bucket status (live/not live) or other fields."""
    try:
        payload = request.json
        name = payload.get('name')
        mode = payload.get('mode', 'live')
        date_str = payload.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = payload.get('product_type')

        if not name:
            return jsonify({'success': False, 'message': 'Bucket name is required'}), 400

        data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        buckets = data.get('buckets', [])

        updated = False
        target_bucket = None
        auto_deactivated: List[dict] = []
        max_live_tb = _get_max_live_tb()

        for b in buckets:
            if b['name'] == name:
                target_bucket = b
                if 'live' in payload:
                    b['live'] = bool(payload['live'])
                    updated = True
                if 'minimum_difference' in payload:
                    b['minimum_difference'] = float(payload['minimum_difference'])
                    updated = True
                if 'delta_type' in payload:
                    b['delta_type'] = _normalize_delta_type(payload['delta_type'])
                    updated = True
                break

        if not target_bucket:
            return jsonify({'success': False, 'message': 'Bucket not found'}), 404

        if updated:
            if target_bucket.get('live'):
                auto_deactivated, max_live_tb = _enforce_max_live_tb_inplace(
                    buckets, preferred_live_name=name
                )
            _save_trade_buckets(data, mode=mode, date_str=date_str, product_type=product_type)
            
            # [V20260204_1410] 2026-02-04 14:10: Workflow Refinement
            # If a bucket is toggled live, suspend Frequency Notifier and sync to Grid Live
            if target_bucket.get('live'):
                # [V20260205_2100] Set automated source to Trade Bucket
                _update_automated_source('Trade Bucket')
                
                # 1. Update Config to suspend alerts
                try:
                    with open(CONFIG_FILE, "r") as f:
                        cfg = json.load(f)
                    cfg['rank_alert_suspended'] = True
                    # [V20260205_2100] Also ensure config sync
                    cfg['automated_trade_source'] = 'Trade Bucket'
                    srcs = cfg.get('automated_trade_sources')
                    if not isinstance(srcs, list):
                        srcs = []
                    srcs = [str(s).strip() for s in srcs if isinstance(s, str) and str(s).strip()]
                    if 'Trade Bucket' not in srcs:
                        srcs.append('Trade Bucket')
                    cfg['automated_trade_sources'] = srcs
                    with open(CONFIG_FILE, "w") as f:
                        json.dump(cfg, f, indent=4)
                    print("[BUCKET] Frequency Notifier SUSPENDED (Config updated)")
                except: pass
                
                # 2. Sync Leader to Grid Live (includes archiving)
                _sync_bucket_to_grid_live(target_bucket, mode, date_str)
            else:
                # If bucket deactivated, just ensure grid_live state is updated
                _sync_bucket_to_grid_live(target_bucket, mode, date_str)

            # Ensure any bucket auto-deactivated by max_live_tb cap is removed from grid.
            for b in auto_deactivated:
                if str(b.get('name') or '') != str(target_bucket.get('name') or ''):
                    _sync_bucket_to_grid_live({'name': b.get('name'), 'live': False}, mode, date_str)
            
        return jsonify({
            'success': True,
            'bucket': target_bucket,
            'max_live_tb': max_live_tb,
            'auto_deactivated': [str(b.get('name') or '') for b in auto_deactivated if b.get('name')]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets/<path:bucket_name>', methods=['DELETE'])
def delete_trade_bucket(bucket_name):
    """Delete a trade bucket."""
    try:
        mode = request.args.get('mode', 'live')
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = request.args.get('product_type')

        data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        buckets = data.get('buckets', [])

        initial_len = len(buckets)
        buckets = [b for b in buckets if b['name'] != bucket_name]

        if len(buckets) < initial_len:
            data['buckets'] = buckets
            _save_trade_buckets(data, mode=mode, date_str=date_str, product_type=product_type)
            # [V20260122_2230] Clear records from activations by syncing empty/dead state
            # [V20260204_1410] Replaced _sync_bucket_to_activations with _sync_bucket_to_grid_live
            _sync_bucket_to_grid_live({'name': bucket_name, 'live': False}, mode, date_str)
            return jsonify({'success': True, 'message': 'Bucket deleted'})
        else:
            return jsonify({'success': False, 'message': 'Bucket not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trade_buckets/remove_all', methods=['POST'])
def remove_all_trade_buckets():
    """Remove all trade buckets for a given mode and date. [V20260206_1145]"""
    try:
        payload = request.json or {}
        mode = payload.get('mode', 'live').lower()
        date_str = payload.get('date', datetime.now().strftime('%Y-%m-%d'))
        product_type = payload.get('product_type')

        # 1. Load data
        data = _load_trade_buckets(mode=mode, date_str=date_str, product_type=product_type)
        buckets = data.get('buckets', [])
        
        if not buckets:
            return jsonify({'success': True, 'message': 'No buckets to remove.'})

        # 2. Sync all live buckets to OFF state in grid before clearing
        for b in buckets:
            if b.get('live'):
                 _sync_bucket_to_grid_live({'name': b['name'], 'live': False}, mode, date_str)

        # 3. Clear and save
        data['buckets'] = []
        _save_trade_buckets(data, mode=mode, date_str=date_str, product_type=product_type)
        
        print(f"[BUCKET] Cleared {len(buckets)} buckets for {mode} on {date_str}.")
        return jsonify({
            'success': True, 
            'message': f'Successfully removed {len(buckets)} buckets.'
        })

    except Exception as e:
        print(f"[BUCKET-ERROR] Remove all failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def _get_health_status(mode: str) -> dict:
    """Internal helper to get health status for a specific mode."""
    # 1. Check Trade Files & Recency
    today_str = datetime.now().strftime('%Y-%m-%d')
    # [V20260316_0150] Use resolve_day_dir to account for product type subfolder (e.g. /forex/)
    trade_dir = _resolve_day_dir(mode, today_str)
    trade_files_exist = False
    trade_recency_ok = True
    latest_trade_age_min = -1
    
    # Load config
    trade_file_max_age = 30
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            trade_file_max_age = cfg.get("trade_file_min_age_minutes", 30)
    except: pass

    if trade_dir.exists():
        json_files = list(trade_dir.glob('*.json'))
        # Filter out metadata files starting with _
        actual_trades = [f for f in json_files if not f.name.startswith('_')]
        trade_files_exist = len(actual_trades) > 0
        
        if trade_files_exist:
            # Get latest file based on modification time
            # [V20260312_0222] Robustness: Handle WinError 2 (missing file) and long path issues
            try:
                latest_file = max(actual_trades, key=lambda f: f.stat().st_mtime if f.exists() else 0)
                latest_ts = latest_file.stat().st_mtime
                age_min = (datetime.now().timestamp() - latest_ts) / 60
                latest_trade_age_min = int(age_min)
                
                if age_min > trade_file_max_age:
                    trade_recency_ok = False
                    print(f"[HEALTH] Trade files stale! Oldest is {age_min:.1f} min old (Limit: {trade_file_max_age})")
            except Exception as ex:
                print(f"[HEALTH-ERROR] Failed to stat latest trade file: {ex}")
                trade_files_exist = False

    # 2. Check Price Feed
    price_feed_ok = False
    feed_latency_sec = -1
    try:
        import subprocess
        target_db = 'tradedb_sim2' if mode == 'sim' else 'tradedb'
        if mode == 'live':
            urls = [
                "http://127.0.0.1:8001/api/vw_000_fx_quotes",
                "http://127.0.0.1:8002/api/vw_000_fx_quotes",
                "http://127.0.0.1:8000/api/vw_000_fx_quotes?db=tradedb",
            ]
        else:
            urls = [f"http://127.0.0.1:8001/api/vw_000_fx_quotes?db={target_db}"]

        for url in urls:
            result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=5)
            
            if result.returncode != 0:
                print(f"[HEALTH-DEBUG] Curl failed for {url} with code {result.returncode}. Stderr: {result.stderr}")
                continue

            try:
                data = json.loads(result.stdout)
            except Exception as parse_err:
                print(f"[HEALTH-DEBUG] Invalid JSON from {url}: {parse_err}")
                continue

            rows = data.get('data', [])
            if not rows:
                print(f"[HEALTH-DEBUG] No data rows in response from {url}")
                continue

            # [V20260202_0150] User overridden: If we get data, connection is Active.
            # Latency checks will just inform the second row.
            price_feed_ok = True

            ts_str = rows[0].get('timestamp', '')
            if ts_str:
                # [V20260130_1357] Robust timestamp parsing (handles 'T' or ' ' separator)
                clean_ts = ts_str.replace('T', ' ').split('.')[0] # Remove fractional seconds
                feed_dt = datetime.strptime(clean_ts, '%Y-%m-%d %H:%M:%S')
                
                # [V20260202_0145] Check against both Local and UTC time to handle timezone mismatches
                latency_local = (datetime.now() - feed_dt).total_seconds()
                latency_utc = (datetime.utcnow() - feed_dt).total_seconds()
                
                # Use the smaller positive latency (assuming feed can't be in future)
                # If local is negative (feed in future vs local), maybe UTC is better match
                candidates = []
                if latency_local > -300: candidates.append(latency_local)
                if latency_utc > -300: candidates.append(latency_utc)
                
                latency = min(candidates) if candidates else latency_local
                feed_latency_sec = int(latency)
                
                if latency < 900: # Increased to 15 mins to be more tolerant of drift/weekend gaps
                    price_feed_ok = True
                elif 3300 < latency < 3900: # ~1 hour offset detection (3600s)
                    price_feed_ok = True
                    feed_latency_sec = int(latency - 3600) # Adjust display
                elif 4600 < latency < 4900: # ~1h 20m offset (likely what we saw 4670s)
                    # This implies feed is legitimately 1h+ old OR serious timezone skew.
                    # If user says "fine", we might just trust the connectivity.
                    pass
            break
    except Exception as e:
        print(f"[HEALTH] Price feed unavailable/error: {e}")

    is_healthy = trade_files_exist and price_feed_ok and trade_recency_ok
    
    return {
        'healthy': is_healthy,
        'checks': {
            'trade_files': trade_files_exist,
            'trade_recency': trade_recency_ok,
            'latest_trade_age_min': latest_trade_age_min,
            'price_feed': price_feed_ok,
            'feed_latency_sec': feed_latency_sec
        }
    }


@app.route('/api/system_health', methods=['GET'])
def health_check():
    """
    [V20260130_1315] System health check:
    1. Check for trade files in today's folder.
    2. Check if price feed is responsive and < 5 mins old.
    [V20260201_2330] Updated to support mode='all' for dual status.
    """
    try:
        mode = request.args.get('mode', 'live').lower()
        
        if mode == 'all':
             return jsonify({
                'success': True,
                'live': _get_health_status('live'),
                'sim': _get_health_status('sim'),
                'timestamp': datetime.now().isoformat()
            })
            
        status = _get_health_status(mode)
        
        return jsonify({
            'success': True,
            'healthy': status['healthy'],
            'checks': status['checks'],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"[HEALTH-ERROR] Global health check failed: {e}")
        return jsonify({'success': False, 'healthy': False, 'message': str(e)}), 500

@app.route('/api/promotion_blocks', methods=['GET'])
def promotion_blocks():
    """
    Return trades with block reasons for promotion to L-trade,
    plus current grid entries for context.
    """
    try:
        mode = request.args.get('mode', 'live').lower()
        date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        include_closed = str(request.args.get('include_closed', 'true')).lower() in ('1', 'true', 'yes')
        q = str(request.args.get('q', '') or '').strip().lower()
        try:
            limit = int(request.args.get('limit', 50))
        except Exception:
            limit = 50
        if limit <= 0:
            limit = 50

        day_dirs = _iter_day_dirs_for(mode, date_str)
        if not day_dirs:
            return jsonify({
                'success': True,
                'mode': mode,
                'date': date_str,
                'count': 0,
                'blocks': [],
                'grid_live': []
            })

        patterns = ['*_op.json']
        if include_closed:
            patterns.extend(['*_cl.json', '*_cld.json'])

        files = []
        product_hint = q.upper() if q and q.isalpha() and len(q) <= 10 else None
        for day_dir in day_dirs:
            for fp in _iter_trade_json_files(
                day_dir,
                include_archived_closed=include_closed,
                product_hint=product_hint,
            ):
                if any(fp.name.endswith(pat.replace('*', '')) for pat in patterns):
                    files.append(fp)

        blocks = []
        for fp in files:
            try:
                with open(fp, 'r') as f:
                    d = json.load(f)
            except Exception:
                continue

            reason = d.get('trade_block_reason')
            if not reason:
                continue

            script_name = d.get('script_name') or d.get('source_strategy') or d.get('app_name')
            product = d.get('product')
            reason_text = f"{reason} {d.get('trade_block_reason_detail') or ''}".strip()
            if q:
                hay = f"{product or ''} {script_name or ''} {reason_text}".lower()
                if q not in hay:
                    continue

            blocks.append({
                'filename': fp.name,
                'status': d.get('status'),
                'trade_id': d.get('trade_id'),
                'product': product,
                'script_name': script_name,
                'source_strategy': d.get('source_strategy'),
                'direction': d.get('direction'),
                'entry_time': d.get('entry_time'),
                'exit_time': d.get('exit_time'),
                'entry_price': d.get('entry_price'),
                'current_price': d.get('current_price'),
                'exit_price': d.get('exit_price'),
                'net_return': d.get('net_return'),
                'alt_net': d.get('alt_net'),
                'is_live_trade': bool(d.get('is_live_trade', False)),
                'order_sent_net': bool(d.get('order_sent_net', False)),
                'order_sent_alt': bool(d.get('order_sent_alt', False)),
                'source_screen': d.get('source_screen'),
                'trade_block_reason': reason,
                'trade_block_reason_detail': d.get('trade_block_reason_detail'),
                'grid_live_context_at_block': d.get('grid_live_context_at_block'),
            })

        blocks.sort(key=lambda x: (str(x.get('entry_time') or ''), str(x.get('filename') or '')), reverse=True)
        blocks = blocks[:limit]

        grid_file = ROOT_PATH / 'grid_live.json'
        grid_live = []
        if grid_file.exists():
            try:
                with open(grid_file, 'r') as f:
                    g = json.load(f)
                if isinstance(g, dict):
                    grid_live = g.get(mode, [])
                elif isinstance(g, list):
                    grid_live = g
            except Exception:
                grid_live = []

        return jsonify({
            'success': True,
            'mode': mode,
            'date': date_str,
            'query': q,
            'limit': limit,
            'count': len(blocks),
            'blocks': blocks,
            'grid_live': grid_live
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Main
# -----------------------------------------------------------
@app.route('/api/grid_live', methods=['GET'])
def get_grid_live():
    """
    [V20260128_1428] Returns the current grid_live.json state for frontend restoration.
    [V20260131_0300] Supports 'mode' param (live/sim) and separated storage.
    [V20260204_2120] Added automatic bucket reconciliation.
    """
    try:
        mode = request.args.get('mode', 'live').lower()
        
        # [V20260204_2120] Periodically ensure buckets are promoted / frequency cleared
        _reconcile_active_buckets(mode=mode)
        
        grid_live_file = ROOT_PATH / "grid_live.json"
        
        if grid_live_file.exists():
            with open(grid_live_file, "r") as f:
                data = json.load(f)
            
            # [V20260131_0300] Handle legacy List format transparently
            if isinstance(data, list):
                # If legacy list, assume it's 'live' data
                if mode == 'live':
                    return jsonify({'success': True, 'data': data})
                else:
                    return jsonify({'success': True, 'data': []})
            elif isinstance(data, dict):
                # New Dict format
                return jsonify({'success': True, 'data': data.get(mode, [])})
            
            return jsonify({'success': True, 'data': []})
        else:
            return jsonify({'success': True, 'data': []})
    except Exception as e:
        print(f"[API-ERROR] GET /api/grid_live failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/grid_live', methods=['POST'])
def update_grid_live():
    """
    [V20260129_1055] Receives live monitoring state from the multi_chart UI.
    [V20260130_1720] Added replace_all flag for "Monitor Only" feature.
    [V20260131_0300] Support 'mode' (live/sim) separation and format migration.
    """
    try:
        payload = request.json
        group = payload.get('group') # Card name source
        models = payload.get('models') # List of {model, product, metric}
        replace_all = bool(payload.get('replace_all', False))
        mode = payload.get('mode', 'live').lower() # [V20260131_0300]
        source = payload.get('source', 'ui')
        source_str = str(source).strip()

        if not group:
            return jsonify({'success': False, 'message': 'Group name is required'}), 400

        grid_live_file = ROOT_PATH / "grid_live.json"
        
        # [V20260205_2100] Handle automated_trade_source for Frequency
        if source_str == 'rank_alert_ui' or source_str == 'frequency_ui':
            # Manual trigger from Frequency screen
            _update_automated_source('Frequency')
        
        if source_str.startswith(('rank_alert', 'frequency')):
            # [V20260205_2100] Check if Frequency is the current automated source
            if not _is_source_allowed('Frequency'):
                 print(f"[GRID-LIVE] REJECTED: source='{source_str}' blocked. Current source is not Frequency.")
                 return jsonify({'success': True, 'message': 'Skipped (Source Overrule)'})

        # [V20260215_0004] Gate breakout/grid UI source by config allowlist.
        # Live-trades groups like 'breakout|...' originate from this path.
        if source_str in ('ui', 'grid_live', 'breakout'):
            if not _is_source_allowed('Breakout'):
                print(f"[GRID-LIVE] REJECTED: source='{source_str}' blocked by config allowlist (requested='Breakout').")
                return jsonify({'success': True, 'message': 'Skipped (Source Overrule)'})

        # [V20260204_2200] Block Manual UI updates if a Trade Bucket is Live
        # Enforces absolute bucket priority: "NO MORE - SOURCE:UI"
        if source_str in ('ui',):
            if _any_trade_bucket_is_live(mode):
                print(f"[GRID-LIVE] REJECTED: source='{source_str}' update blocked because a Trade Bucket is LIVE.")
                return jsonify({'success': True, 'message': 'Skipped (Bucket Live Overrule)'})

        with GRID_LIVE_LOCK:
            full_data = {'live': [], 'sim': []}
            
            if grid_live_file.exists():
                try:
                    with open(grid_live_file, "r") as f:
                        loaded = json.load(f)
                    
                    if isinstance(loaded, list):
                        # [V20260131_0300] Migration: Move legacy list to 'live'
                        full_data['live'] = loaded
                        print("[API] Migrating grid_live.json from List to Dict format.")
                    elif isinstance(loaded, dict):
                        full_data = loaded
                        # Ensure keys exist
                        if 'live' not in full_data: full_data['live'] = []
                        if 'sim' not in full_data: full_data['sim'] = []
                except Exception:
                    pass
            
            # Target the specific list for this mode
            target_list = full_data.get(mode, [])
            
            # [V20260130_1640] Absolute Strategy Persistence Guard (Per Mode)
            master_timestamps = { (m.get('model'), m.get('product')): m.get('activated_at') 
                                 for m in target_list if m.get('activated_at') }
            
            def _srcgrp(entry: Dict[str, Any]) -> Tuple[str, str]:
                src = str(entry.get('source') or 'ui')
                grp = str(entry.get('group') or '')
                return (src, grp)

            # 1. Isolate existing entries within this mode
            if replace_all:
                other_groups = []
                print(f"[API] replace_all=True ({mode}). Clearing previous items.")
            else:
                incoming_srcgrp = (str(source_str or 'ui'), str(group or ''))
                # Append semantics across different source-groups:
                # only replace entries for the exact same (source, group)
                other_groups = [m for m in target_list if _srcgrp(m) != incoming_srcgrp]
            
            # 2. Build updated state
            new_target_list = list(other_groups)
            if models:
                now_local = datetime.now().isoformat().split('.')[0] 
                for m in models:
                    m_model = m.get('model')
                    m_product = m.get('product')
                    
                    # [V20260202_0220] Fix: Ensure group is persisted in the model object
                    m['group'] = group
                    # [V20260204_1410] Ensure source is persisted
                    if 'source' not in m:
                        m['source'] = source_str

                    # Restore original timestamp if exists
                    original_ts = master_timestamps.get((m_model, m_product))
                    if m.get('activated_at'):
                        pass # Keep what's sent
                    elif original_ts:
                         m['activated_at'] = original_ts # Restore
                    else:
                         m['activated_at'] = now_local # New
                         
                    new_target_list.append(m)
            
            # Update the full structure
            def _material_signature(items: List[Dict[str, Any]]) -> List[Tuple[str, str, str]]:
                # Material change criteria: strategy/model, product, metric only.
                return sorted(
                    (
                        str(x.get('model', '')),
                        str(x.get('product', '')),
                        str(x.get('metric', ''))
                    )
                    for x in items
                )

            if _material_signature(target_list) == _material_signature(new_target_list):
                print(f"[GRID-LIVE] source={source} no material change for {mode} group={group}; skipped archive/write.")
                return jsonify({'success': True, 'count': len(target_list), 'message': 'No material change'})

            # [V20260215_0003] Archive only when material state changes.
            _archive_grid_live(mode)

            full_data[mode] = new_target_list
            
            with open(grid_live_file, "w") as f:
                json.dump(full_data, f, indent=4)
            if models:
                print(f"[GRID-LIVE] source={source_str} updated {mode} entries from group={group}: {[m.get('model') for m in models]}")
                
            # [V20260131_0305] Sync activations for this mode
            _sync_grid_to_activations(new_target_list, mode=mode)
                
        return jsonify({'success': True, 'count': len(full_data[mode])})

    except Exception as e:
        print(f"[API-ERROR] POST /api/grid_live failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/grid_live/prune_siblings', methods=['POST'])
def prune_grid_live_siblings():
    """Prune sibling products for a model after live execution."""
    try:
        payload = request.json or {}
        mode = str(payload.get('mode', 'live')).lower()
        model = payload.get('model')
        product = payload.get('product')
        reason = payload.get('reason', '')
        result = _prune_grid_live_siblings(model, product, mode, reason=reason)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/grid_live/prune_from_live_trades', methods=['POST'])
def prune_from_live_trades():
    """Periodic sweep: prune sibling products for any executed live trades."""
    try:
        payload = request.json or {}
        mode = str(payload.get('mode', 'live')).lower()
        date = payload.get('date') or datetime.now().strftime('%Y-%m-%d')
        trade_dir = BASE_PATH / mode / date
        live_file = trade_dir / "_live_trades.json"
        if not live_file.exists():
            return jsonify({'success': True, 'removed': 0, 'message': 'no live trades file'})

        with open(live_file, 'r') as f:
            data = json.load(f)
        trades = data.get('trades', [])

        removed_total = 0
        seen = set()
        for t in trades:
            if t.get('is_live_trade') is not True:
                continue
            model = t.get('source_strategy') or t.get('script_name') or t.get('app_name')
            product = t.get('product')
            if not model or not product:
                continue
            key = (model, str(product).upper())
            if key in seen:
                continue
            seen.add(key)
            res = _prune_grid_live_siblings(model, product, mode, reason='PERIODIC_SWEEP')
            removed_total += int(res.get('removed', 0) or 0)

        return jsonify({'success': True, 'removed': removed_total, 'checked': len(seen)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def _sync_grid_to_activations(grid_data: list, mode: str = 'live'):
    """
    Rebuilds the specified mode section of activations.json based on current grid_live.json state.
    Preserves manual flags where possible.
    """
    try:
        # 1. Load current activations
        full_activations = _load_activations()
        
        # 2. Prepare new state for this mode
        new_mode_section = {}
        active_definitions = {} # key -> { 'products': set(), 'source': str, 'manual': bool }
        
        # 3. Iterate Grid Data to build definitions
        for m in grid_data:
            model = m.get('model')
            product = m.get('product')
            metric = m.get('metric', 'net')
            source = m.get('source', 'ui')
            manual = m.get('manual', False)
            
            # Determine target activation keys based on metric
            target_keys = []
            if metric == 'net':
                target_keys = [f"{model}_buy_net", f"{model}_sell_net"]
            elif metric == 'buy_net':
                target_keys = [f"{model}_buy_net"]
            elif metric == 'sell_net':
                target_keys = [f"{model}_sell_net"]
            else:
                target_keys = [model] # Fallback (e.g. valid for some older formats)

            for key in target_keys:
                if key not in active_definitions:
                    # Initialize
                    # Try to preserve source/manual/time from existing activation if available
                    existing = full_activations.get(mode, {}).get(key, {})
                    active_definitions[key] = {
                        'products': set(),
                        'source': source if source != 'ui' else existing.get('source', 'ui'), 
                        'manual': manual or existing.get('manual', False),
                        'activated_at': existing.get('activated_at') # Preserve time
                    }
                
                # Add product
                if product:
                    active_definitions[key]['products'].add(product)
                
                # Update metadata if this grid entry is more specific/newer
                if source != 'ui':
                    active_definitions[key]['source'] = source
                if manual:
                    active_definitions[key]['manual'] = True

        # 4. Finalize Entries
        now = datetime.utcnow().isoformat()
        for key, defs in active_definitions.items():
            entry = {
                "active": True,
                "manual": defs['manual'],
                "activated_at": defs['activated_at'] or now,
                "source": defs['source'],
                "products": sorted(list(defs['products']))
            }
            new_mode_section[key] = entry
            
        # 5. Atomic Update
        full_activations[mode] = new_mode_section
        
        with open(ACTIVATIONS_FILE, "w") as f:
            json.dump(full_activations, f, indent=4)
            
        print(f"[SYNC] activations.json ({mode}) synced with grid_live.json. Active keys: {len(new_mode_section)}")

    except Exception as e:
        print(f"[SYNC-ERROR] Failed to sync activations: {e}")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# [V20260209_1010] Bias-Flip Notification System
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
NOTIFICATION_LOG_FILE = ROOT_PATH / "notification_log.json"

@app.route('/api/notification_action', methods=['POST'])
def log_notification_action():
    """Log a bias-flip notification action [V20260209_1010]"""
    try:
        data = request.json
        
        # Load existing log
        if NOTIFICATION_LOG_FILE.exists():
            with open(NOTIFICATION_LOG_FILE, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"logs": []}
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "bias_from": data.get('bias_from'),
            "bias_to": data.get('bias_to'),
            "recommended_strategy": data.get('recommended_strategy'),
            "recommended_product": data.get('recommended_product'),
            "action": data.get('action'),  # activated|dismissed|auto_activate|suspended
            "run_mode": data.get('run_mode', 'live')
        }
        
        # Append to logs
        log_data["logs"].insert(0, log_entry)  # Most recent first
        
        # Keep only last 100 entries
        log_data["logs"] = log_data["logs"][:100]
        
        # Save
        with open(NOTIFICATION_LOG_FILE, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # If action is to update config, do it
        if data.get('action') == 'auto_activate':
            # Set ai_picker_prompt to false
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                config['ai_picker_prompt'] = False
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
        
        elif data.get('action') == 'suspended':
            # Set bias_notifications_suspended to true
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                config['bias_notifications_suspended'] = True
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
        
        return jsonify({"success": True, "message": "Action logged successfully"})
    
    except Exception as e:
        print(f"[NOTIFICATION-LOG-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/notification_log', methods=['GET'])
def get_notification_log():
    """Retrieve notification log entries [V20260209_1010]"""
    try:
        if not NOTIFICATION_LOG_FILE.exists():
            return jsonify({"success": True, "logs": []})
        
        with open(NOTIFICATION_LOG_FILE, 'r') as f:
            log_data = json.load(f)
        
        # Optional filtering by run_mode
        mode = request.args.get('mode')
        logs = log_data.get("logs", [])
        
        if mode:
            logs = [log for log in logs if log.get('run_mode') == mode]
        
        return jsonify({"success": True, "logs": logs})
    
    except Exception as e:
        print(f"[NOTIFICATION-LOG-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# [V20260209_1335] Bias History Tracking
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BIAS_HISTORY_SESSION_FILE = ROOT_PATH / "bias_history_session.json"

def _get_bias_history_file(mode: str, date_str: str) -> Path:
    day_dir = _ensure_day_dir(str(mode or 'live').lower(), str(date_str or datetime.now().strftime('%Y-%m-%d')))
    return day_dir / "_bias_history.json"


def _load_tb_leadership(mode: str, date_str: str, product_type: str | None = None) -> list:
    """Load the persistent leadership report for a given date."""
    day_dirs = _iter_day_dirs_for(mode, date_str, product_type)
    
    all_leadership = []
    for day_dir in day_dirs:
        lb_file = day_dir / "_tb_leadership.json"
        if lb_file.exists():
            try:
                with open(lb_file, 'r') as f:
                    all_leadership.extend(json.load(f))
            except:
                pass
    return all_leadership


def _is_trade_in_leader_window(trade: dict, bucket_leadership: dict) -> bool:
    """Check if a trade was executed while its strategy was the leader in a specific bucket."""
    strategy = trade.get('app_name', '') or trade.get('script_name', '')
    product = trade.get('product', '')
    full_key = f"{strategy}:{product}"
    
    # Try alternate matching from trade metadata
    # (some trades store source_strategy instead of script_name)
    alt_keys = [full_key]
    if trade.get('source_strategy'):
        alt_keys.append(f"{trade['source_strategy']}:{product}")
    
    entry_time = trade.get('entry_time') or trade.get('time')
    if not entry_time:
        return False
        
    try:
        # Handle Z suffix if present
        entry_dt = datetime.fromisoformat(entry_time.replace('Z', '').replace(' ', 'T'))
    except:
        return False
        
    for window in bucket_leadership.get('windows', []):
        w_strat = window.get('strategy')
        if any(ak == w_strat or ak.startswith(w_strat + ":") for ak in alt_keys):
            start_dt = datetime.fromisoformat(window.get('start').replace(' ', 'T'))
            end_val = window.get('end')
            if end_val:
                end_dt = datetime.fromisoformat(end_val.replace(' ', 'T'))
                if start_dt <= entry_dt < end_dt:
                    return True
            else:
                # Active window
                if entry_dt >= start_dt:
                    return True
    return False


@app.route('/api/tb_leadership', methods=['GET'])
def get_tb_leadership_route():
    mode = request.args.get('mode', 'live')
    date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
    product_type = request.args.get('product_type')
    return jsonify({
        "success": True,
        "leadership": _load_tb_leadership(mode, date, product_type)
    })

def _load_bias_history_safe(mode: str, date_str: str) -> dict:
    target_file = _get_bias_history_file(mode, date_str)
    if target_file.exists():
        try:
            with open(target_file, 'r') as f:
                data = json.load(f) or {}
            if not isinstance(data, dict):
                return {"history": []}
            if not isinstance(data.get("history"), list):
                data["history"] = []
            return data
        except Exception:
            try:
                stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup = target_file.with_name(f"_bias_history.corrupt_{stamp}.json")
                shutil.copy2(target_file, backup)
            except Exception:
                pass
            return {"history": []}

    return {"history": []}

def _load_bias_sessions_safe() -> dict:
    if not BIAS_HISTORY_SESSION_FILE.exists():
        return {}
    try:
        with open(BIAS_HISTORY_SESSION_FILE, 'r') as f:
            data = json.load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def _save_bias_sessions(data: dict) -> None:
    with open(BIAS_HISTORY_SESSION_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def _atomic_write_json(path: Path, data: Any, indent: int = 2) -> None:
    tmp = path.with_suffix(f".{uuid.uuid4().hex}.tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=indent)
    os.replace(tmp, path)

def _parse_iso_ts(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except Exception:
        return None

@app.route('/api/bias_history', methods=['POST'])
def log_bias_history():
    """Log bias history entry every 5 minutes [V20260209_1335]"""
    try:
        data = request.json or {}
        mode = str(data.get('run_mode', 'live')).lower()
        timestamp = data.get('timestamp') or datetime.now(timezone.utc).isoformat()
        ts_dt = _parse_iso_ts(timestamp) or datetime.now(timezone.utc)
        date_str = ts_dt.strftime('%Y-%m-%d')
        reset_session = bool(data.get('reset_session', False))
        session_start = data.get('session_start')

        history_data = _load_bias_history_safe(mode, date_str)
        sessions = _load_bias_sessions_safe()
        if mode not in sessions:
            sessions[mode] = {"session_start": timestamp}
        if session_start:
            sessions[mode]["session_start"] = session_start
        if reset_session:
            sessions[mode]["session_start"] = timestamp
            history_data["history"] = [
                h for h in history_data.get("history", [])
                if str(h.get("run_mode", "live")).lower() != mode
            ]

        # Create history entry
        history_entry = {
            "timestamp": timestamp,
            "bias": data.get('bias'),
            "market_condition": data.get('market_condition'),
            "status": data.get('status'),
            "recent_buy_pnl": data.get('recent_buy_pnl'),
            "recent_sell_pnl": data.get('recent_sell_pnl'),
            "recent_buy_count": data.get('recent_buy_count'),
            "recent_sell_count": data.get('recent_sell_count'),
            "run_mode": mode
        }
        
        # Append to history
        history_data["history"].insert(0, history_entry)  # Most recent first
        
        # Keep only last 500 entries (covers ~41 hours at 5min intervals)
        history_data["history"] = history_data["history"][:500]
        
        # Save
        _atomic_write_json(_get_bias_history_file(mode, date_str), history_data, indent=2)
        _save_bias_sessions(sessions)
        
        return jsonify({
            "success": True,
            "message": "Bias history logged",
            "session_start": sessions.get(mode, {}).get("session_start"),
            "run_mode": mode
        })
    
    except Exception as e:
        print(f"[BIAS-HISTORY-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/bias_history', methods=['GET'])
def get_bias_history():
    """Retrieve bias history [V20260209_1335]"""
    try:
        mode = request.args.get('mode', 'live')
        date_str = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
        history_data = _load_bias_history_safe(str(mode).lower(), date_str)
        sessions = _load_bias_sessions_safe()
        
        # Optional filtering
        limit = request.args.get('limit', type=int, default=100)
        since_session = request.args.get('since_session', 'false').lower() in ('1', 'true', 'yes', 'on')
        
        history = history_data.get("history", [])
        
        session_start = None
        start_dt = None

        if mode:
            mode_l = str(mode).lower()
            history = [h for h in history if str(h.get('run_mode', 'live')).lower() == mode_l]
            if since_session:
                session_start = (sessions.get(mode_l) or {}).get("session_start")
                start_dt = _parse_iso_ts(session_start)
                if start_dt:
                    history = [h for h in history if (_parse_iso_ts(h.get("timestamp")) or datetime.min.replace(tzinfo=timezone.utc)) >= start_dt]
        
        # Compute flip summary in chronological order.
        chrono = sorted(history, key=lambda h: _parse_iso_ts(h.get("timestamp")) or datetime.min.replace(tzinfo=timezone.utc))
        start_bias = chrono[0].get("bias") if chrono else None
        first_flip_at = None
        flip_count = 0
        if chrono:
            prev_bias = str(chrono[0].get("bias") or "").upper()
            for h in chrono[1:]:
                b = str(h.get("bias") or "").upper()
                if b and prev_bias and b != prev_bias:
                    flip_count += 1
                    if first_flip_at is None:
                        first_flip_at = h.get("timestamp")
                    prev_bias = b

        history = history[:limit]
        
        return jsonify({
            "success": True,
            "history": history,
            "session_start": session_start if mode else None,
            "since_session": since_session,
            "start_bias": start_bias,
            "first_flip_at": first_flip_at,
            "flip_count": flip_count
        })
    
    except Exception as e:
        print(f"[BIAS-HISTORY-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/bias_audit', methods=['GET'])
def bias_audit():
    """Audit current open trades against latest targeted bias."""
    try:
        mode = str(request.args.get('mode', 'live')).lower()
        date_str = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
        bias = _get_current_bias(mode, date_str)
        if not bias:
            return jsonify({"success": False, "message": "No current bias available", "mode": mode, "date": date_str}), 404
        day_dirs = _iter_day_dirs_for(mode, date_str)
        if not day_dirs:
            return jsonify({"success": True, "mode": mode, "date": date_str, "bias": bias, "open_count": 0, "mismatch_count": 0, "mismatches": []})
        mismatches = []
        open_count = 0
        for day_dir in day_dirs:
            for fp in day_dir.glob('*_op.json'):
                try:
                    with open(fp, 'r') as f:
                        d = json.load(f) or {}
                except Exception:
                    continue
                if str(d.get('status', '')).upper() != 'OPEN':
                    continue
                if not bool(d.get('is_live_trade') or d.get('order_sent_net') or d.get('order_sent_alt')):
                    continue
                open_count += 1
                direction = str(d.get('direction') or '').upper()
                aligned = ((bias == 'BUY' and direction == 'LONG') or (bias == 'SELL' and direction == 'SHORT'))
                if not aligned:
                    mismatches.append({
                        "file": fp.name,
                        "entry_time": d.get("entry_time"),
                        "strategy": d.get("script_name") or d.get("source_strategy"),
                        "product": d.get("product"),
                        "direction": direction,
                        "market_bias_latest": d.get("market_bias_latest"),
                        "market_bias_at_open": d.get("market_bias_at_open")
                    })
        return jsonify({
            "success": True,
            "mode": mode,
            "date": date_str,
            "bias": bias,
            "open_count": open_count,
            "mismatch_count": len(mismatches),
            "mismatches": mismatches
        })
    except Exception as e:
        print(f"[BIAS-AUDIT-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# [V20260209_1900] Bias-Aligned Strategy Switching - Smart Target Activation
@app.route('/api/smart_target/activate', methods=['POST'])
def smart_target_activate():
    """Activate a strategy in grid_live.json with bias tagging"""
    try:
        data = request.json
        strategy = data.get('strategy')
        product = data.get('product')
        metric = data.get('metric', 'buy_net')  # 'buy_net' or 'sell_net'
        mode = data.get('mode', 'live')
        bias = data.get('bias')  # NEW: BUY or SELL
        
        if not strategy or not product:
            return jsonify({"success": False, "error": "Strategy and product required"}), 400

        # [V20260215_0002] Gate Smart Target automation by config allowlist.
        if not _is_source_allowed('AI Target'):
            print("[SMART-TARGET] REJECTED: 'AI Target' is not enabled in automated_trade_sources.")
            return jsonify({"success": True, "message": "Skipped (Source Overrule)"})
        
        # Load grid_live.json
        grid_file = Path('grid_live.json')
        if grid_file.exists():
            with open(grid_file, 'r') as f:
                grid_data = json.load(f)
        else:
            grid_data = {"live": [], "sim": []}
        
        # Determine which list to update
        target_list = grid_data.get(mode, [])
        
        # Check if already exists [V20260210_1223]
        # Fix: keys in grid_live are 'model' and 'product', not 'strategy'
        existing = next((item for item in target_list 
                        if item.get('model') == strategy and item.get('product') == product), None)
        
        if existing:
            # Update existing entry
            existing['metric'] = metric
            existing['activated_for_bias'] = bias  # [V20260209_1900] Tag with bias
            existing['activated_at'] = datetime.now().isoformat()
            existing['source'] = 'ai_target' # Ensure source is set
        else:
            # Add new entry [V20260210_1223] Correct structure
            target_list.append({
                "model": strategy,
                "product": product,
                "metric": metric,
                "source": "ai_target",
                "manual": False,
                "group": product, # Default group to product
                "activated_for_bias": bias, 
                "activated_at": datetime.now().isoformat()
            })
        
        grid_data[mode] = target_list
        
        # Save grid_live.json
        with open(grid_file, 'w') as f:
            json.dump(grid_data, f, indent=2)
            
        # [V20260210_1645] Sync with activations (Activation Explorer)
        _sync_grid_to_activations(target_list, mode=mode)
        
        print(f"[SMART-TARGET] Activated {strategy} on {product} ({metric}) for {bias} bias")
        return jsonify({"success": True, "message": f"Activated {strategy} on {product}"})
    
    except Exception as e:
        print(f"[SMART-TARGET-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# [V20260209_1900] Deactivate strategies with opposite bias
@app.route('/api/deactivate_wrong_bias', methods=['POST'])
def deactivate_wrong_bias():
    """Deactivate all strategies that don't match the current bias"""
    try:
        data = request.json
        current_bias = data.get('current_bias')  # 'BUY' or 'SELL'
        mode = data.get('mode', 'live')
        
        if not current_bias:
            return jsonify({"success": False, "error": "current_bias required"}), 400
            
        # [V20260210_0400] 2026-02-10 04:20 - Archive existing state before deactivating
        _archive_grid_live(mode)
        
        opposite_bias = 'SELL' if current_bias == 'BUY' else 'BUY'
        
        # Load grid_live.json
        grid_file = Path('grid_live.json')
        if not grid_file.exists():
            return jsonify({"success": True, "deactivated": 0, "message": "No grid_live.json found"})
        
        with open(grid_file, 'r') as f:
            grid_data = json.load(f)
        
        target_list = grid_data.get(mode, [])
        deactivated_count = 0
        deactivated_strategies = []
        
        # [V20260210_0400] 2026-02-10 04:20 - Find and deactivate/remove opposite-bias strategies
        new_list = []
        for item in target_list:
            if item.get('activated_for_bias') == opposite_bias:
                if item.get('source') == 'ai_target':
                    # REMOVE AI-targeted strategies to enforce "Switching"
                    deactivated_count += 1
                    deactivated_strategies.append(f"REMOVED: {item.get('model', item.get('strategy'))} on {item.get('product')}") # [V20260210_1236] Fix: use 'model' key
                    continue 
                else:
                    # Deactivate regular activations
                    item['buy'] = False
                    item['sell'] = False
                    item['deactivated_at'] = datetime.now().isoformat()
                    item['deactivation_reason'] = f"Bias changed to {current_bias}"
                    deactivated_count += 1
                    deactivated_strategies.append(f"DISABLED: {item.get('model', item.get('strategy'))} on {item.get('product')}") # [V20260210_1236] Fix: use 'model' key
            
            new_list.append(item)
        
        grid_data[mode] = new_list
        
        # Save updated grid_live.json
        with open(grid_file, 'w') as f:
            json.dump(grid_data, f, indent=4)
            
        # [V20260210_1645] Sync with activations (Activation Explorer)
        _sync_grid_to_activations(new_list, mode=mode)
        
        print(f"[DEACTIVATE-WRONG-BIAS] Deactivated {deactivated_count} {opposite_bias}-bias strategies")
        for strat in deactivated_strategies:
            print(f"  - {strat}")
        
        return jsonify({
            "success": True,
            "deactivated": deactivated_count,
            "strategies": deactivated_strategies,
            "message": f"Deactivated {deactivated_count} {opposite_bias}-bias strategies"
        })
    
    except Exception as e:
        print(f"[DEACTIVATE-WRONG-BIAS-ERROR] {e}")
        return jsonify({"success": False, "error": str(e)}), 500


def _start_market_update_worker():
    def worker():
        time.sleep(10)  # wait for startup
        while True:
            try:
                # Always generate for live. The generator internally determines the latest date
                generate_market_update("live")
            except Exception as e:
                print(f"[MarketUpdateWorker] Error generating update: {e}")
            time.sleep(300)
    t = threading.Thread(target=worker, daemon=True)
    t.start()


# [V20260325_1745] API for Weekly Performance Dashboard
@app.route("/api/weekly_performance")
def get_weekly_performance():
    product_type = request.args.get("product_type", "forex").lower()
    target_date = request.args.get("target_date")  # Expected YYYY-MM-DD

    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")

    from tools.aggregate_top_strategies import aggregate_for_product_type, get_week_bounds

    week_start, week_end = get_week_bounds(target_date)
    week_start_str = week_start.strftime("%Y-%m-%d")
    week_end_str = week_end.strftime("%Y-%m-%d")

    stats_dir = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\json\live") / product_type / "stats" / "weekly"
    stats_dir.mkdir(parents=True, exist_ok=True)
    stats_file = stats_dir / f"{week_start_str}.json"

    # Always refresh for now so navigation consistently reflects the aligned week.
    is_recent = True

    if not stats_file.exists() or is_recent:
        try:
            aggregate_for_product_type(
                product_type,
                target_date=week_start_str,
                output_file=stats_file,
            )
        except Exception as e:
            print(f"Error generating weekly stats: {e}")

    if not stats_file.exists():
        return jsonify({"error": f"Stats file not found for aligned week {week_start_str} to {week_end_str}"}), 404

    try:
        with open(stats_file, "r") as f:
            data = json.load(f)
        data["requested_target_date"] = target_date
        data["week_start"] = data.get("week_start", week_start_str)
        data["week_end"] = data.get("week_end", week_end_str)
        data["date_range"] = [data["week_start"], data["week_end"]]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Trade Viewer API V1315 (activation v2)")
    try:
        # Avoid double-start in Flask reloader
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
            _start_grid_auto_worker()
            _start_market_update_worker()
            print("[GRID-AUTO] Background workers started")
    except Exception as e:
        print(f"[GRID-AUTO] Failed to start worker: {e}")
    app.run(host="0.0.0.0", port=5000, debug=True)


 succeeded in 11546ms:
C:\Users\edebe\eds\TradeApps\breakout\fs\generate_twitter_summary.py:90:    with open("temp_tweet.txt", "w", encoding="utf-8") as f:
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py:12:TEMP_TWEET = ROOT / "temp_tweet.txt"
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py:14:WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py:90:        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py:94:        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post.py:12:    tweet_file = Path("temp_tweet.txt")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post.py:14:        print("[ERROR] temp_tweet.txt not found.")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v2.py:14:    tweet_file = Path("temp_tweet.txt")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v2.py:16:        print("[ERROR] temp_tweet.txt not found.")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v3.py:15:TWEET_FILE = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v3.py:177:        print("[ERROR] temp_tweet.txt not found.")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v3.py:178:        _mark_step(status, "load_tweet", False, "temp_tweet.txt not found")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v3.py:183:        print("[ERROR] temp_tweet.txt is empty.")
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v3.py:184:        _mark_step(status, "load_tweet", False, "temp_tweet.txt is empty")
C:\Users\edebe\eds\TradeApps\breakout\fs\social_publisher.py:709:    @app.route('/api/social/x_api_post', methods=['POST'])
C:\Users\edebe\eds\TradeApps\breakout\fs\social_publisher.py:710:    def publish_x_api_post():
C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_social_publisher.py:12:import social_publisher as sp  # noqa: E402
C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py:22:TEMP_TWEET_PATH = FS_ROOT / "temp_tweet.txt"
C:\Users\edebe\eds\TradeApps\breakout\fs\trade_viewer_api.py:26:from social_publisher import add_social_routes
C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_post_status.json:3:  "tweet_file": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\temp_tweet.txt",
C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_workflow_status.json:13:      "artifact": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\temp_tweet.txt"
C:\Users\edebe\eds\TradeApps\breakout\fs\update_temp_tweet.py:7:OUTPUT_PATH = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt")
C:\Users\edebe\eds\TradeApps\breakout\fs\update_temp_tweet.py:20:            print(f"[SUCCESS] Updated temp_tweet.txt with latest canonical data.")

codex
I have enough context to make the change. Next I’m tracing where the recurring workflow is invoked and then I’ll patch the canonical workflow script and the lifecycle file together so the recorded evidence matches the new X API route behavior.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"run_twitter_canonical_workflow\\.py|twitter summary returns every 4 hours|x_api_post\" 'C:\\Users\\edebe\\eds\\TradeApps' 'C:\\Users\\edebe\\eds\\workstream' 'C:\\Users\\edebe\\eds\\tests'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_social_publisher.py'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\twitter_workflow_status.json'" in C:\Users\edebe\eds
 succeeded in 1449ms:
import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch


FS_DIR = Path(__file__).resolve().parents[1]
if str(FS_DIR) not in sys.path:
    sys.path.insert(0, str(FS_DIR))

import social_publisher as sp  # noqa: E402


class SocialPublisherTests(unittest.TestCase):
    def make_publisher(self, config: dict | None = None, post_log: dict | None = None) -> sp.SocialPublisher:
        with (
            patch.object(sp.SocialPublisher, "_load_config", return_value=config or {}),
            patch.object(sp.SocialPublisher, "_load_post_log", return_value=post_log or {"posts": [], "last_post_time": None}),
            patch.object(sp.SocialPublisher, "_save_post_log", return_value=None),
        ):
            return sp.SocialPublisher()

    def test_compact_best_strategy_stays_within_142_chars(self) -> None:
        publisher = self.make_publisher()
        metrics = {
            "top_strategy": "super_long_strategy_name_" * 10,
            "top_strategy_net": 123.4,
            "bias": "BUY",
            "confidence": "HIGH",
        }

        post = publisher.format_compact_best_strategy(metrics)

        self.assertLessEqual(len(post), publisher.COMPACT_CHAR_LIMIT)
        self.assertIn("..", post)
        self.assertTrue(post.endswith(f"piphunter.io {publisher.COMPACT_HASHTAG}"))

    def test_configured_summary_interval_does_not_block_trade_updates(self) -> None:
        now = datetime.now().isoformat()
        publisher = self.make_publisher(
            config={
                "twitter_post_interval_minutes": 15,
                "twitter_trade_update_interval_seconds": 0,
            },
            post_log={"posts": [], "last_post_time": now},
        )

        can_post_summary, reason_summary = publisher.can_post(trigger="compact_best")
        can_post_trade, reason_trade = publisher.can_post(trigger="trade_update")

        self.assertFalse(can_post_summary)
        self.assertIn("minutes", reason_summary)
        self.assertTrue(can_post_trade, reason_trade)

    def test_publish_trade_update_suppresses_duplicates(self) -> None:
        publisher = self.make_publisher()
        publisher.publish_to_twitter = Mock(return_value={"success": True})
        trade = {"trade_id": "t-1", "strategy_name": "Alpha", "product": "EURUSD", "direction": "BUY", "net_return": 1.2}

        first = publisher.publish_trade_update(trade)
        second = publisher.publish_trade_update(trade)

        self.assertTrue(first["success"])
        self.assertFalse(second["success"])
        self.assertIn("Duplicate", second["error"])
        publisher.publish_to_twitter.assert_called_once()

    def test_get_best_strategy_trades_filters_current_leader(self) -> None:
        publisher = self.make_publisher()
        publisher.narrative_gen.load_data = Mock(
            return_value={
                "grid_live": {
                    "trades": [
                        {"id": "1", "strategy_name": "Alpha"},
                        {"id": "2", "strategy_name": "Beta"},
                        {"id": "3", "strategy_name": "Alpha"},
                    ]
                }
            }
        )
        publisher.narrative_gen.extract_metrics = Mock(return_value={"top_strategy": "Alpha"})

        trades = publisher.get_best_strategy_trades()

        self.assertEqual([trade["id"] for trade in trades], ["1", "3"])

    def test_publish_to_twitter_retries_before_success(self) -> None:
        publisher = self.make_publisher(config={"twitter_retry_attempts": 3, "twitter_retry_backoff_seconds": 1})
        publisher.api_enabled = True
        publisher._send_tweet = Mock(
            side_effect=[
                {"success": False, "error": "temporary"},
                {"success": False, "error": "temporary"},
                {"success": True, "tweet_id": "123"},
            ]
        )

        with patch.object(sp.time, "sleep") as sleep_mock:
            result = publisher.publish_to_twitter("hello world", trigger="compact_best")

        self.assertTrue(result["success"])
        self.assertEqual(result["attempts"], 3)
        self.assertEqual(publisher._send_tweet.call_count, 3)
        self.assertEqual(sleep_mock.call_count, 2)


if __name__ == "__main__":
    unittest.main()


 succeeded in 1613ms:
{
  "timestamp": "2026-04-02T23:28:50.504177",
  "run_date": "2026-04-02",
  "steps": {
    "verify_login": {
      "ok": false,
      "details": "Session is not authenticated. Current URL: https://x.com/i/flow/login?redirect_after_login=%2Fhome",
      "artifact": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\check_login.png"
    },
    "generate_content": {
      "ok": false,
      "details": "",
      "artifact": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\temp_tweet.txt"
    },
    "submit_post": {
      "ok": false,
      "details": "",
      "artifact": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\twitter_post_status.json"
    },
    "verify_audit_log": {
      "ok": false,
      "details": "",
      "artifact": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\posted_tweets.log"
    }
  },
  "final_status": "failed"
}

2026-04-03T00:01:34.398047Z ERROR codex_core::tools::router: error=Exit code: 124
Wall time: 20.6 seconds
Output:
command timed out after 20642 milliseconds
C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:15:Task Summary: Every 4 hours, regenerate the latest Strategy Warehouse summary payload into `temp_tweet.txt`, then submit that prepared text through `POST /api/social/x_api_post`, recording the exact live response.


C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:21:- X API route: `http://localhost:5000/api/social/x_api_post`


C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:25:  - `C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md`


C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:29:Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:44:  - [ ] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.


C:\Users\edebe\eds\TradeApps\breakout\fs\social_publisher.py:709:    @app.route('/api/social/x_api_post', methods=['POST'])
C:\Users\edebe\eds\TradeApps\breakout\fs\social_publisher.py:710:    def publish_x_api_post():
C:\Users\edebe\eds\workstream\300_complete\20260403_003225_breakout_retry_x_api_post_with_corrected_dated_payload.md:8:- Posting route: `http://localhost:5000/api/social/x_api_post`
C:\Users\edebe\eds\workstream\300_complete\20260403_003225_breakout_retry_x_api_post_with_corrected_dated_payload.md:31:- 2026-04-03 00:32:43 Validation: `POST /api/social/x_api_post` with trigger `manual_api_dated_payload` returned `{"success": true, "message": "Tweet posted successfully", "tweet_id": "2039848585395683426"}`.
C:\Users\edebe\eds\workstream\300_complete\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md:3:Run an immediate end-to-end test of the newly combined recurring workflow defined by `20260402_233618_workstream_replace_recurring_twitter_summary_with_combined_x_api_workflow.md` by regenerating the latest payload and posting it through `POST /api/social/x_api_post`.
C:\Users\edebe\eds\workstream\300_complete\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md:10:- Posting route: `http://localhost:5000/api/social/x_api_post`
C:\Users\edebe\eds\workstream\300_complete\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md:24:3. Submit the prepared payload to `POST /api/social/x_api_post`.
C:\Users\edebe\eds\workstream\300_complete\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md:33:- 2026-04-02 23:44:59 Validation: `POST http://localhost:5000/api/social/x_api_post` with trigger `recurring_combined_test` returned `{"success": false, "error": "Rate limit: wait 10 more minutes"}`.
C:\Users\edebe\eds\workstream\300_complete\20260402_233618_workstream_replace_recurring_twitter_summary_with_combined_x_api_workflow.md:9:- X API post reference: `C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md`
C:\Users\edebe\eds\workstream\300_complete\20260402_233618_workstream_replace_recurring_twitter_summary_with_combined_x_api_workflow.md:30:- 2026-04-02 23:37:09 Replaced `workstream/100_backlog/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md` with a combined recurring definition that regenerates `temp_tweet.txt` and then posts it through `POST /api/social/x_api_post`.
C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md:3:Rerun `POST /api/social/x_api_post` with the current prepared summary payload after refreshing `workstream/.env` so the live response shows whether the new X OAuth 1.0 credentials are now accepted.
C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md:24:3. Call `POST /api/social/x_api_post` and capture the exact response.
C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md:32:- 2026-04-02 18:51:03 Validation: `POST http://localhost:5000/api/social/x_api_post` returned HTTP `200` with `{"success": true, "message": "Tweet posted successfully", "tweet_id": "2039762743595569627"}`.
C:\Users\edebe\eds\workstream\300_complete\20260402_175437_breakout_refresh_workstream_x_env_credentials.md:3:Refresh the active workstream-scoped X/Twitter API credentials from the newly generated values in `workstream/access_key.txt` so `POST /api/social/x_api_post` uses the current OAuth 1.0 token set.
C:\Users\edebe\eds\workstream\300_complete\20260402_164430_breakout_rerun_x_api_post_permission_test.md:23:- 2026-04-02 16:53:12 Validation: `POST /api/social/x_api_post` returned:
C:\Users\edebe\eds\workstream\300_complete\20260402_163950_breakout_install_tweepy_and_retest_x_api_post.md:17:3. Retest `POST /api/social/x_api_post` with the current summary payload.
C:\Users\edebe\eds\workstream\300_complete\20260402_163950_breakout_install_tweepy_and_retest_x_api_post.md:27:- 2026-04-02 16:41:27 Route retest against `POST /api/social/x_api_post` reached X and returned:
C:\Users\edebe\eds\workstream\300_complete\20260402_163225_breakout_wire_x_api_credentials_via_workstream_env.md:3:Wire X API credentials into the breakout social publishing flow via a workstream-scoped `.env` path instead of `config.json`, then verify `POST /api/social/x_api_post` can use the same summary payload without dry-run fallback.
C:\Users\edebe\eds\workstream\300_complete\20260402_163225_breakout_wire_x_api_credentials_via_workstream_env.md:7:- Current route: `POST /api/social/x_api_post`
C:\Users\edebe\eds\workstream\300_complete\20260402_163225_breakout_wire_x_api_credentials_via_workstream_env.md:38:- 2026-04-02 16:35:49 Validation: direct publish and `POST /api/social/x_api_post` now fail with `tweepy library not installed. Run: pip install tweepy`.
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:7:- Test `POST /api/social/x_api_post` with the current summary returns payload.
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:12:- [x] 2. Send the current summary returns text to `POST /api/social/x_api_post`.`r`n  - [x] Test: Route returns either live-post success or a concrete config/runtime error.`r`n  - Evidence: Route returned `{ "dry_run": true, "message": "API not configured - dry run mode", "success": true }` when called with the current `temp_tweet.txt` payload.
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:18:- Evidence-Type: test_output`r`n  - Artifact: `Invoke-WebRequest http://127.0.0.1:5000/api/health`; `POST http://127.0.0.1:5000/api/social/x_api_post``r`n  - Objective-Proved: Proves the route is callable and reports its real posting state.`r`n  - Status: complete
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:27:- 2026-04-02 16:02 Europe/London: Posted the current summary returns payload to /api/social/x_api_post; route responded in dry-run mode because API credentials are not configured.
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:35:- /api/social/x_api_post returned dry-run success with message API not configured - dry run mode`r
C:\Users\edebe\eds\workstream\300_complete\20260402_155549_breakout_add_x_api_posting_route.md:16:  - Evidence: Added `publish_direct_text()` plus `POST /api/social/x_api_post`, which validates non-empty text, enforces character limit, and routes through the existing API-backed publisher logic rather than Playwright/browser posting.
C:\Users\edebe\eds\workstream\300_complete\20260402_155549_breakout_add_x_api_posting_route.md:36:- 2026-04-02 15:58 Europe/London: Added `publish_direct_text()` and the new `POST /api/social/x_api_post` endpoint.
C:\Users\edebe\eds\workstream\300_complete\20260402_155549_breakout_add_x_api_posting_route.md:41:- Added `POST /api/social/x_api_post` to the Flask social routes.
C:\Users\edebe\eds\workstream\300_complete\20260402_153439_breakout_retest_hardened_twitter_workflow.md:11:- [x] 1. Execute `run_twitter_canonical_workflow.py` for the target date.
C:\Users\edebe\eds\workstream\300_complete\20260402_153439_breakout_retest_hardened_twitter_workflow.md:25:  - Artifact: sandboxed run output; unrestricted run of `run_twitter_canonical_workflow.py 2026-04-02`
C:\Users\edebe\eds\workstream\300_complete\20260402_153439_breakout_retest_hardened_twitter_workflow.md:40:- 2026-04-02 15:35 Europe/London: Unrestricted rerun of `run_twitter_canonical_workflow.py 2026-04-02` executed and produced gated status artefacts.
C:\Users\edebe\eds\workstream\300_complete\20260402_153439_breakout_retest_hardened_twitter_workflow.md:49:- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-02`
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:18:  - Evidence: Added `run_twitter_canonical_workflow.py` with explicit gates for login verification, content generation, post execution, and audit-log verification; each step fails closed.
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:28:  - Evidence: The skill now points recurring runs at the strict wrapper workflow, and recurring task normalization now embeds `Execution Workflow: python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`.
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:31:  - Evidence: `py_compile` passed for `run_twitter_post_v3.py`, `run_twitter_canonical_workflow.py`, and the updated `workstream/run_agent.py`.
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:37:  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v3.py`; `C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py`; `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`; `C:\Users\edebe\eds\workstream\run_agent.py`
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:70:- 2026-04-02 15:26 Europe/London: Added `run_twitter_canonical_workflow.py` to gate the full workflow: login -> content generation -> post -> audit-log verification.
C:\Users\edebe\eds\workstream\300_complete\gemini\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md:24:Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`



C:\Users\edebe\eds\workstream\run_agent.py:38:TWITTER_CANONICAL_WORKFLOW_SCRIPT = r"C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py"
C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260402_210000_breakout_twitter_summary_returns_every_4_hours.md:24:Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md.result.md:2025:I will read the `run_twitter_canonical_workflow.py` script to understand its gated logic and how it handles session verification before proceeding with the data refresh and posting.
C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md.result.md:2289:I will now execute the `run_twitter_canonical_workflow.py` script for the date `2026-04-02`, which will automatically handle the data generation and the Twitter/X posting process.
C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md.result.md:3249:I will now re-run the `run_twitter_canonical_workflow.py` script for `2026-04-02` to see if the `headless=True` modification resolves the previous posting issue.
rg: C:\Users\edebe\eds\workstream\artefacts\epic_decomp_4rbio_0v: Access is denied. (os error 5)
rg: C:\Users\edebe\eds\workstream\artefacts\epic_decomp_yxt48izg: Access is denied. (os error 5)

 exited 124 in 20642ms:
C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:15:Task Summary: Every 4 hours, regenerate the latest Strategy Warehouse summary payload into `temp_tweet.txt`, then submit that prepared text through `POST /api/social/x_api_post`, recording the exact live response.


C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:21:- X API route: `http://localhost:5000/api/social/x_api_post`


C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:25:  - `C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md`


C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:29:Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_050000_breakout_twitter_summary_returns_every_4_hours.md:44:  - [ ] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.


C:\Users\edebe\eds\TradeApps\breakout\fs\social_publisher.py:709:    @app.route('/api/social/x_api_post', methods=['POST'])
C:\Users\edebe\eds\TradeApps\breakout\fs\social_publisher.py:710:    def publish_x_api_post():
C:\Users\edebe\eds\workstream\300_complete\20260403_003225_breakout_retry_x_api_post_with_corrected_dated_payload.md:8:- Posting route: `http://localhost:5000/api/social/x_api_post`
C:\Users\edebe\eds\workstream\300_complete\20260403_003225_breakout_retry_x_api_post_with_corrected_dated_payload.md:31:- 2026-04-03 00:32:43 Validation: `POST /api/social/x_api_post` with trigger `manual_api_dated_payload` returned `{"success": true, "message": "Tweet posted successfully", "tweet_id": "2039848585395683426"}`.
C:\Users\edebe\eds\workstream\300_complete\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md:3:Run an immediate end-to-end test of the newly combined recurring workflow defined by `20260402_233618_workstream_replace_recurring_twitter_summary_with_combined_x_api_workflow.md` by regenerating the latest payload and posting it through `POST /api/social/x_api_post`.
C:\Users\edebe\eds\workstream\300_complete\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md:10:- Posting route: `http://localhost:5000/api/social/x_api_post`
C:\Users\edebe\eds\workstream\300_complete\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md:24:3. Submit the prepared payload to `POST /api/social/x_api_post`.
C:\Users\edebe\eds\workstream\300_complete\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md:33:- 2026-04-02 23:44:59 Validation: `POST http://localhost:5000/api/social/x_api_post` with trigger `recurring_combined_test` returned `{"success": false, "error": "Rate limit: wait 10 more minutes"}`.
C:\Users\edebe\eds\workstream\300_complete\20260402_233618_workstream_replace_recurring_twitter_summary_with_combined_x_api_workflow.md:9:- X API post reference: `C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md`
C:\Users\edebe\eds\workstream\300_complete\20260402_233618_workstream_replace_recurring_twitter_summary_with_combined_x_api_workflow.md:30:- 2026-04-02 23:37:09 Replaced `workstream/100_backlog/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md` with a combined recurring definition that regenerates `temp_tweet.txt` and then posts it through `POST /api/social/x_api_post`.
C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md:3:Rerun `POST /api/social/x_api_post` with the current prepared summary payload after refreshing `workstream/.env` so the live response shows whether the new X OAuth 1.0 credentials are now accepted.
C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md:24:3. Call `POST /api/social/x_api_post` and capture the exact response.
C:\Users\edebe\eds\workstream\300_complete\20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md:32:- 2026-04-02 18:51:03 Validation: `POST http://localhost:5000/api/social/x_api_post` returned HTTP `200` with `{"success": true, "message": "Tweet posted successfully", "tweet_id": "2039762743595569627"}`.
C:\Users\edebe\eds\workstream\300_complete\20260402_175437_breakout_refresh_workstream_x_env_credentials.md:3:Refresh the active workstream-scoped X/Twitter API credentials from the newly generated values in `workstream/access_key.txt` so `POST /api/social/x_api_post` uses the current OAuth 1.0 token set.
C:\Users\edebe\eds\workstream\300_complete\20260402_164430_breakout_rerun_x_api_post_permission_test.md:23:- 2026-04-02 16:53:12 Validation: `POST /api/social/x_api_post` returned:
C:\Users\edebe\eds\workstream\300_complete\20260402_163950_breakout_install_tweepy_and_retest_x_api_post.md:17:3. Retest `POST /api/social/x_api_post` with the current summary payload.
C:\Users\edebe\eds\workstream\300_complete\20260402_163950_breakout_install_tweepy_and_retest_x_api_post.md:27:- 2026-04-02 16:41:27 Route retest against `POST /api/social/x_api_post` reached X and returned:
C:\Users\edebe\eds\workstream\300_complete\20260402_163225_breakout_wire_x_api_credentials_via_workstream_env.md:3:Wire X API credentials into the breakout social publishing flow via a workstream-scoped `.env` path instead of `config.json`, then verify `POST /api/social/x_api_post` can use the same summary payload without dry-run fallback.
C:\Users\edebe\eds\workstream\300_complete\20260402_163225_breakout_wire_x_api_credentials_via_workstream_env.md:7:- Current route: `POST /api/social/x_api_post`
C:\Users\edebe\eds\workstream\300_complete\20260402_163225_breakout_wire_x_api_credentials_via_workstream_env.md:38:- 2026-04-02 16:35:49 Validation: direct publish and `POST /api/social/x_api_post` now fail with `tweepy library not installed. Run: pip install tweepy`.
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:7:- Test `POST /api/social/x_api_post` with the current summary returns payload.
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:12:- [x] 2. Send the current summary returns text to `POST /api/social/x_api_post`.`r`n  - [x] Test: Route returns either live-post success or a concrete config/runtime error.`r`n  - Evidence: Route returned `{ "dry_run": true, "message": "API not configured - dry run mode", "success": true }` when called with the current `temp_tweet.txt` payload.
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:18:- Evidence-Type: test_output`r`n  - Artifact: `Invoke-WebRequest http://127.0.0.1:5000/api/health`; `POST http://127.0.0.1:5000/api/social/x_api_post``r`n  - Objective-Proved: Proves the route is callable and reports its real posting state.`r`n  - Status: complete
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:27:- 2026-04-02 16:02 Europe/London: Posted the current summary returns payload to /api/social/x_api_post; route responded in dry-run mode because API credentials are not configured.
C:\Users\edebe\eds\workstream\300_complete\20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md:35:- /api/social/x_api_post returned dry-run success with message API not configured - dry run mode`r
C:\Users\edebe\eds\workstream\300_complete\20260402_155549_breakout_add_x_api_posting_route.md:16:  - Evidence: Added `publish_direct_text()` plus `POST /api/social/x_api_post`, which validates non-empty text, enforces character limit, and routes through the existing API-backed publisher logic rather than Playwright/browser posting.
C:\Users\edebe\eds\workstream\300_complete\20260402_155549_breakout_add_x_api_posting_route.md:36:- 2026-04-02 15:58 Europe/London: Added `publish_direct_text()` and the new `POST /api/social/x_api_post` endpoint.
C:\Users\edebe\eds\workstream\300_complete\20260402_155549_breakout_add_x_api_posting_route.md:41:- Added `POST /api/social/x_api_post` to the Flask social routes.
C:\Users\edebe\eds\workstream\300_complete\20260402_153439_breakout_retest_hardened_twitter_workflow.md:11:- [x] 1. Execute `run_twitter_canonical_workflow.py` for the target date.
C:\Users\edebe\eds\workstream\300_complete\20260402_153439_breakout_retest_hardened_twitter_workflow.md:25:  - Artifact: sandboxed run output; unrestricted run of `run_twitter_canonical_workflow.py 2026-04-02`
C:\Users\edebe\eds\workstream\300_complete\20260402_153439_breakout_retest_hardened_twitter_workflow.md:40:- 2026-04-02 15:35 Europe/London: Unrestricted rerun of `run_twitter_canonical_workflow.py 2026-04-02` executed and produced gated status artefacts.
C:\Users\edebe\eds\workstream\300_complete\20260402_153439_breakout_retest_hardened_twitter_workflow.md:49:- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-02`
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:18:  - Evidence: Added `run_twitter_canonical_workflow.py` with explicit gates for login verification, content generation, post execution, and audit-log verification; each step fails closed.
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:28:  - Evidence: The skill now points recurring runs at the strict wrapper workflow, and recurring task normalization now embeds `Execution Workflow: python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`.
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:31:  - Evidence: `py_compile` passed for `run_twitter_post_v3.py`, `run_twitter_canonical_workflow.py`, and the updated `workstream/run_agent.py`.
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:37:  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_post_v3.py`; `C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py`; `C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md`; `C:\Users\edebe\eds\workstream\run_agent.py`
C:\Users\edebe\eds\workstream\300_complete\20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md:70:- 2026-04-02 15:26 Europe/London: Added `run_twitter_canonical_workflow.py` to gate the full workflow: login -> content generation -> post -> audit-log verification.
C:\Users\edebe\eds\workstream\300_complete\gemini\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md:24:Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`



C:\Users\edebe\eds\workstream\run_agent.py:38:TWITTER_CANONICAL_WORKFLOW_SCRIPT = r"C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py"
C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260402_210000_breakout_twitter_summary_returns_every_4_hours.md:24:Execution Workflow: `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py YYYY-MM-DD`
C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md.result.md:2025:I will read the `run_twitter_canonical_workflow.py` script to understand its gated logic and how it handles session verification before proceeding with the data refresh and posting.
C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md.result.md:2289:I will now execute the `run_twitter_canonical_workflow.py` script for the date `2026-04-02`, which will automatically handle the data generation and the Twitter/X posting process.
C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260402_170000_breakout_twitter_summary_returns_every_4_hours.md.result.md:3249:I will now re-run the `run_twitter_canonical_workflow.py` script for `2026-04-02` to see if the `headless=True` modification resolves the previous posting issue.
rg: C:\Users\edebe\eds\workstream\artefacts\epic_decomp_4rbio_0v: Access is denied. (os error 5)
rg: C:\Users\edebe\eds\workstream\artefacts\epic_decomp_yxt48izg: Access is denied. (os error 5)

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -TotalCount 260 'C:\\Users\\edebe\\eds\\workstream\\run_agent.py'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"TWITTER_CANONICAL_WORKFLOW_SCRIPT|twitter_workflow_status|verify_login|verify_audit_log|submit_post\" 'C:\\Users\\edebe\\eds\\workstream\\run_agent.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests'" in C:\Users\edebe\eds
 succeeded in 1239ms:
C:\Users\edebe\eds\workstream\run_agent.py:38:TWITTER_CANONICAL_WORKFLOW_SCRIPT = r"C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py"
C:\Users\edebe\eds\workstream\run_agent.py:329:        f"`python {TWITTER_CANONICAL_WORKFLOW_SCRIPT} YYYY-MM-DD`",

 succeeded in 1326ms:
#!/usr/bin/env python3
import atexit
import datetime
import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo

WORKSTREAM_DIR = Path(__file__).resolve().parent
EDS_ROOT = WORKSTREAM_DIR.parent
SKILLS_DIR = EDS_ROOT / "skills"
LIFECYCLE_FILE = SKILLS_DIR / "workstream-task-lifecycle" / "SKILL.md"

TODO_ROOT = WORKSTREAM_DIR / "100_backlog"
WORKING_ROOT = WORKSTREAM_DIR / "200_inprogress"
COMPLETE_ROOT = WORKSTREAM_DIR / "300_complete"
FAILED_ROOT = WORKSTREAM_DIR / "400_failed"
LOG_ROOT = WORKSTREAM_DIR / "logs"
AGENT_LOCK = WORKSTREAM_DIR / "agent.lock"
WORKER_LOG = LOG_ROOT / "agent_worker.log"
CONTROLLER_LOG = LOG_ROOT / "agent_controller_py.log"

AGENTS = ["gemini", "codex", "claude"]
MAX_CONCURRENT_PER_DATE = 1
EXCLUDED_WORKERS_FILE = WORKSTREAM_DIR / "excluded_workers.txt"
MAX_MODEL_BACKLOG_PER_LANE = 1
MAX_MODEL_INPROGRESS_PER_LANE = 1
TWITTER_SUMMARY_RECURRING_TOKEN = "breakout_twitter_summary_returns_every_4_hours"
TWITTER_CANONICAL_POSTING_SKILL = r"C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md"
TWITTER_CANONICAL_WORKFLOW_SCRIPT = r"C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py"


def _is_task_markdown_name(name: str) -> bool:
    lowered = str(name or "").lower()
    return lowered.endswith(".md") and not lowered.endswith(".result.md") and not lowered.startswith(".")


def _is_task_markdown_path(path: str | Path) -> bool:
    return _is_task_markdown_name(Path(path).name)


def _read_markdown_text(path: str | Path, *, errors: str = "replace") -> str:
    path_obj = Path(path)
    raw = path_obj.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors=errors)


def is_worker_excluded(agent: str) -> bool:
    """Check if worker is excluded via file-based config."""
    if not EXCLUDED_WORKERS_FILE.exists():
        return False
    try:
        excluded = EXCLUDED_WORKERS_FILE.read_text(encoding="utf-8").strip().lower().split()
        return agent.lower() in excluded
    except Exception:
        return False


def _resolve_agent_binary(agent: str) -> str:
    """Resolve the specific binary/CLI for a given agent. [2026-03-17 V20260317_1530]"""
    agent_lower = agent.lower()
    
    # Try system PATH first
    found = shutil.which(agent_lower) or shutil.which(f"{agent_lower}.cmd") or shutil.which(f"{agent_lower}.exe")
    if found:
        return found
        
    # Fallback to known npm global path
    npm_path = Path.home() / "AppData" / "Roaming" / "npm" / f"{agent_lower}.cmd"
    if npm_path.exists():
        return str(npm_path)
        
    # Final fallback to codex if everything else fails (legacy behavior)
    return shutil.which("codex") or shutil.which("codex.cmd") or str(Path.home() / "AppData" / "Roaming" / "npm" / "codex.cmd")

LOG_ROOT.mkdir(exist_ok=True)
WORKING_ROOT.mkdir(exist_ok=True)
FAILED_ROOT.mkdir(exist_ok=True)
COMPLETE_ROOT.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler(CONTROLLER_LOG, encoding="utf-8"), logging.StreamHandler(sys.stdout)],
)


def write_worker_log(agent: str, message: str) -> None:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{agent.upper()}] {message}\n"
    with open(WORKER_LOG, "a", encoding="utf-8") as fh:
        fh.write(line)


def acquire_lock() -> None:
    if AGENT_LOCK.exists():
        try:
            existing = int(AGENT_LOCK.read_text().strip())
        except ValueError:
            existing = None
        if existing:
            try:
                check = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {existing}"],
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                if "No tasks are running" in check.stdout:
                    existing = None
            except Exception:
                existing = None
        if existing:
            logging.error("Another controller instance is running (PID %s).", existing)
            sys.exit(1)
        AGENT_LOCK.unlink(missing_ok=True)
    AGENT_LOCK.write_text(str(os.getpid()))
    atexit.register(release_lock)


def release_lock() -> None:
    AGENT_LOCK.unlink(missing_ok=True)


def load_workflow() -> str:
    if not LIFECYCLE_FILE.exists():
        return ""
    return LIFECYCLE_FILE.read_text(encoding="utf-8")


def load_support_skills() -> str:
    builder = []
    for md in SKILLS_DIR.rglob("*.md"):
        try:
            relative = md.relative_to(SKILLS_DIR)
        except ValueError:
            continue
        if md == LIFECYCLE_FILE:
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except OSError:
            continue
        builder.append(f"----- SKILL: {relative} -----\n{content}")
    return "\n".join(builder)


def build_agent_execution_command(agent: str, task_path: str) -> list[str] | None:
    key_specific = f"KANBAN_AGENT_EXEC_CMD_{agent.upper()}"
    tpl = os.environ.get(key_specific, "").strip() or os.environ.get("KANBAN_AGENT_EXEC_CMD", "").strip()
    if tpl:
        formatted = tpl.format(
            agent=agent,
            task_path=task_path,
            task_file=os.path.basename(task_path),
        )
        return shlex.split(formatted, posix=False)
    if not tpl:
        agent_lower = agent.lower()
        if agent_lower in {"codex", "gemini", "claude"}:
            # [2026-03-17 V20260317_1715] Use agent-specific binary and syntax
            agent_bin = _resolve_agent_binary(agent)
            prompt = (
                "Execute this task file end-to-end. "
                "Read and follow C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md first. "
                "Then read and follow any additional skill files explicitly referenced by the task. "
                f"Task file: {task_path}. "
                "Implement required changes in the workspace, run validations, and update checklist items."
            )
            
            # Agent-specific command structures
            if agent_lower == "gemini":
                return [agent_bin, "--prompt", prompt, "--yolo"]
            elif agent_lower == "claude":
                return [agent_bin, "-p", prompt, "--permission-mode", "acceptEdits"]
            else: # codex
                return [agent_bin, "exec", "-C", str(EDS_ROOT), prompt]
        return None


@dataclass
class TaskMetadata:
    path: Path
    priority: int
    epic: str
    epic_sequence: str
    depends_on: list[str]
    readiness: str
    suggested_agent: str
    lane: str
    major_layer: int
    sequence_sort_key: str
    date_prefix: str | None
    scheduled_for: datetime.datetime | None
    recurring_task: bool
    recurrence_interval_hours: int | None
    mtime: float
    state: str


def _local_tzinfo() -> datetime.tzinfo:
    return datetime.datetime.now().astimezone().tzinfo or ZoneInfo("UTC")


def _parse_scheduled_for(raw: str) -> datetime.datetime | None:
    value = str(raw or "").strip().strip("`")
    if not value or value.lower() == "none":
        return None

    candidates = [value]
    if value.endswith("Z"):
        candidates.append(value[:-1] + "+00:00")

    timezone_match = re.match(r"^(.*?)(?:\s+([A-Za-z_]+/[A-Za-z_]+|UTC))$", value)
    if timezone_match:
        base_value = timezone_match.group(1).strip()
        tz_name = timezone_match.group(2).strip()
        try:
            tzinfo = ZoneInfo(tz_name)
        except Exception:
            tzinfo = None
        if tzinfo is not None:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    return datetime.datetime.strptime(base_value, fmt).replace(tzinfo=tzinfo)
                except ValueError:
                    continue

    for candidate in candidates:
        try:
            parsed = datetime.datetime.fromisoformat(candidate)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=_local_tzinfo())
            return parsed
        except ValueError:
            continue

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.datetime.strptime(value, fmt).replace(tzinfo=_local_tzinfo())
        except ValueError:
            continue

    return None


def _parse_bool_metadata(text: str, key: str) -> bool:

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\20260403_003225_breakout_retry_x_api_post_with_corrected_dated_payload.md'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md'" in C:\Users\edebe\eds
 succeeded in 1100ms:
## Objective

Run an immediate end-to-end test of the newly combined recurring workflow defined by `20260402_233618_workstream_replace_recurring_twitter_summary_with_combined_x_api_workflow.md` by regenerating the latest payload and posting it through `POST /api/social/x_api_post`.

## Context

- Combined recurring task definition: `C:\Users\edebe\eds\workstream\100_backlog\codex\20260403_010000_breakout_twitter_summary_returns_every_4_hours.md`
- Payload generator: `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- Prepared payload file: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
- Posting route: `http://localhost:5000/api/social/x_api_post`

## Task Attributes

- project: breakout
- task_type: verification
- area: social_publisher
- priority: high
- status: complete

## Plan

1. Regenerate the latest payload for the current date.
2. Verify `temp_tweet.txt` was refreshed and is non-empty.
3. Submit the prepared payload to `POST /api/social/x_api_post`.
4. Record the exact response and whether the combined workflow succeeds end to end.

## Progress Log

- 2026-04-02 23:44:09 Created lifecycle task.
- 2026-04-02 23:44:09 Validation: `GET http://localhost:5000/api/health` returned `{"status":"ok"}` before running the combined workflow test.
- 2026-04-02 23:44:31 Validation: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-02` completed successfully and rewrote the dated social posting package outputs.
- 2026-04-02 23:44:31 Validation: `TradeApps\breakout\fs\temp_tweet.txt` was non-empty after generation and contained the refreshed `Update at 2026-04-02 23:59` payload.
- 2026-04-02 23:44:59 Validation: `POST http://localhost:5000/api/social/x_api_post` with trigger `recurring_combined_test` returned `{"success": false, "error": "Rate limit: wait 10 more minutes"}`.
- 2026-04-02 23:45:03 Validation: `GET http://localhost:5000/api/social/status` confirmed `api_enabled=true`, `can_post=false`, `reason="Rate limit: wait 10 more minutes"`, and logged the attempted `recurring_combined_test` payload.

## Outcome

Completed. The new combined recurring workflow works through payload generation and route invocation, but the immediate live-post test is currently blocked by the social publisher's 10-minute rate limit rather than by payload generation or X API credential issues.


 succeeded in 1158ms:
## Objective

Retry a live X API post using the corrected dated payload format now that the rate limit window has cleared.

## Context

- Payload file: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
- Posting route: `http://localhost:5000/api/social/x_api_post`
- Current format uses explicit source-date labels (`2026-04-02 results`, `Week to 2026-04-02`)

## Task Attributes

- project: breakout
- task_type: verification
- area: social_publisher
- priority: high
- status: complete

## Plan

1. Confirm the local social publisher can currently post.
2. Submit the corrected payload via the X API route.
3. Capture the exact response.
4. Record whether the corrected dated payload posts successfully.

## Progress Log

- 2026-04-03 00:32:25 Created lifecycle task.
- 2026-04-03 00:32:25 Validation: `GET /api/social/status` returned `api_enabled=true`, `can_post=true`, `reason=OK`.
- 2026-04-03 00:32:25 Loaded the corrected payload from `TradeApps\breakout\fs\temp_tweet.txt`.
- 2026-04-03 00:32:43 Validation: `POST /api/social/x_api_post` with trigger `manual_api_dated_payload` returned `{"success": true, "message": "Tweet posted successfully", "tweet_id": "2039848585395683426"}`.

## Outcome

Completed. The corrected dated payload posted successfully through the X API route.


codex
I’m about to edit the workflow implementation and the task record. The code change will swap the browser-login/post path for an API-health, payload-validation, and `x_api_post` submission flow, while keeping the same entrypoint the scheduler already calls.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Invoke-WebRequest -UseBasicParsing 'http://localhost:5000/api/social/status' | Select-Object -ExpandProperty Content" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Invoke-WebRequest -UseBasicParsing 'http://localhost:5000/api/health' | Select-Object -ExpandProperty Content" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git status --short' in C:\Users\edebe\eds
 succeeded in 1972ms:
 M .gitignore
 M DataInsights/src/Constants.py
 m TradeApps
 M api_server_sql/main.py
 D grid_live_monitor.py
 M workstream/.process/pipeline_focus.json
 D workstream/000_epic/20260316_135212_trading_strategy_warehouse_marketing_engine_processed.md
 M workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine_processed.md
 D workstream/050_review/codex/20260316_135213_general_trading_strategy_warehouse_build_landing_page_and_subscribe_funnel.md
 D workstream/100_backlog/claude/20260305_192700_bizpa_mvp_pivot_phase06_voice_micro_decisions.md
 D workstream/100_backlog/claude/20260317_140505_gemini_BLOCKER_20260317_135511_gemini_BLOCKER_20260317_135402_gemini_BLOCKER_20260316_232302_strategy_warehouse_marketing_engine_workstreamZ_create_environment_template_and_readme.md.result.md
 D workstream/100_backlog/claude/20260317_171500_agent_cli_syntax_fix.md.result.md
 D workstream/100_backlog/claude/20260317_173000_kanban_add_delivered_epic_backlog_column.md.result.md.result.md
 D workstream/100_backlog/claude/20260317_194500_kanban_refine_delivered_column_grouping.md.result.md.result.md
 D workstream/100_backlog/claude/20260317_230402_gemini_BLOCKER_20260317_173000_kanban_add_delivered_epic_backlog_column.md.result.md.result.md
 D workstream/100_backlog/claude/20260317_230402_gemini_BLOCKER_20260317_173000_kanban_add_delivered_epic_backlog_column.md.result.md.result.md.result.md
 D workstream/100_backlog/claude/20260318_172607_claude_BLOCKER_20260314_210743_breakout_fs_add_product_type_view_selection_across_performance_screens.md.result.md
 D workstream/100_backlog/claude/20260318_172613_claude_BLOCKER_20260314_224854_build_secure_token_storage_and_refresh_lifecycle_s_2.md.result.md
 D workstream/100_backlog/claude/20260318_172620_claude_BLOCKER_20260314_224854_define_open_banking_consent_contract_and_provider__0.md.result.md
 D workstream/100_backlog/claude/20260318_172626_claude_BLOCKER_20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_docker_and_compose_scaffolding.md.result.md
 D workstream/100_backlog/claude/20260318_172632_claude_BLOCKER_20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_operator_and_developer_usage.md.result.md
 D workstream/100_backlog/claude/20260318_172637_claude_BLOCKER_20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md
 D workstream/100_backlog/claude/20260318_172651_claude_BLOCKER_20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_root_readme_and_documentation.md.result.md
 D workstream/100_backlog/claude/20260318_172656_claude_BLOCKER_20260314_034035_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_build_quarter_model_readiness_metrics_and_blocking_queue_ordering.md
 D workstream/100_backlog/claude/20260318_172712_claude_BLOCKER_20260316_135215_trading_strategy_warehouse_automate_distribution_and_scheduler.md.result.md.result.md
 D workstream/100_backlog/claude/20260318_172731_claude_BLOCKER_20260316_161933_skills_make_task_dependency_mandatory.md
 D workstream/100_backlog/claude/20260318_172739_claude_BLOCKER_20260316_161933_skills_make_task_dependency_mandatory.md.result.md
 D workstream/100_backlog/claude/20260318_172746_claude_BLOCKER_20260316_162650_trading_strategy_warehouse_retrofit_task_dependencies.md.result.md
 D workstream/100_backlog/claude/20260318_172752_claude_BLOCKER_20260316_211200_workstream_document_agent_controller_timestamp_entry.md
 D workstream/100_backlog/claude/20260318_172800_claude_BLOCKER_20260316_211200_workstream_document_agent_controller_timestamp_entry.md.result.md
 D workstream/100_backlog/claude/20260318_172807_claude_BLOCKER_20260317_100000_breakout_silence_workflow_prompts.md.result.md
 D workstream/100_backlog/claude/20260318_172813_claude_BLOCKER_20260317_135330_codex_BLOCKER_20260309_120092_autonomous_trading_signal_platform_workstreamJ_release_mobile_app.md.result.md
 D workstream/100_backlog/claude/20260318_172820_claude_BLOCKER_20260317_135343_claude_BLOCKER_20260316_135217_claude_trading_strategy_warehouse_build_growth_analytics_dashboard.md.result.md
 D workstream/100_backlog/claude/20260318_172826_claude_BLOCKER_20260317_135343_claude_BLOCKER_20260316_135217_claude_trading_strategy_warehouse_build_growth_analytics_dashboard.md.result.md.result.md
 D workstream/100_backlog/claude/20260318_172846_claude_BLOCKER_20260318_172600_claude_BLOCKER_20260309_120092_autonomous_trading_signal_platform_workstreamJ_release_mobile_app.md.result.md.result.md
 D workstream/100_backlog/claude/20260318_172850_claude_BLOCKER_20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md
 D workstream/100_backlog/claude/20260318_172904_claude_BLOCKER_20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline.md
 D workstream/100_backlog/claude/20260318_172918_claude_BLOCKER_20260314_034041_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_persist_evidence_links_and_unmatched_states_with_user_confirmation.md
 D workstream/100_backlog/claude/20260318_172933_claude_BLOCKER_20260314_034042_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_mobile_inbox_exception_queue_screen.md
 D workstream/100_backlog/claude/20260318_172947_claude_BLOCKER_20260314_034043_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_quarter_readiness_and_finish_now_screen.md
 D workstream/100_backlog/claude/20260318_173006_claude_BLOCKER_20260314_034044_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_evidence_capture_and_match_confirmation_ui_flow.md
 D workstream/100_backlog/claude/20260318_173023_claude_BLOCKER_20260314_034045_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_implement_voice_intents_confirmation_chip_and_undo_flow.md
 D workstream/100_backlog/claude/20260318_173040_claude_BLOCKER_20260314_034047_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamF_harden_security_performance_and_legal_disclaimers_for_mvp_release.md
 D workstream/100_backlog/claude/20260318_183811_codex_BLOCKER_20260316_232321_strategy_warehouse_marketing_engine_workstreamB_implement_discord_connector.md.result.md.result.md
 D workstream/100_backlog/claude/20260318_183824_codex_BLOCKER_20260316_232322_strategy_warehouse_marketing_engine_workstreamB_implement_telegram_connector.md.result.md.result.md
 D workstream/100_backlog/claude/20260318_183836_codex_BLOCKER_20260317_171500_agent_cli_syntax_fix.md.result.md.result.md
 D workstream/100_backlog/claude/20260318_183839_codex_BLOCKER_20260316_232323_strategy_warehouse_marketing_engine_workstreamB_implement_linkedin_connector.md.result.md
 D workstream/100_backlog/claude/20260318_183852_codex_BLOCKER_20260317_173000_kanban_add_delivered_epic_backlog_column.md.result.md.result.md.result.md
 D workstream/100_backlog/gemini/20260309_120092_autonomous_trading_signal_platform_workstreamJ_release_mobile_app.md.result.md
 D workstream/100_backlog/gemini/20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md
 D workstream/100_backlog/gemini/20260314_034031_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_transaction_classification_model_with_full_audit_trail.md
 D workstream/100_backlog/gemini/20260314_034032_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_build_inbox_micro_decision_actions_and_suggestion_application.md
 D workstream/100_backlog/gemini/20260314_034033_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_blocker_evaluation_and_transaction_resolution_rules.md
 D workstream/100_backlog/gemini/20260314_034034_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_simple_merchant_rules_for_recurring_categorisation_defaults.md
 D workstream/100_backlog/gemini/20260314_034035_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_build_quarter_model_readiness_metrics_and_blocking_queue_ordering.md
 D workstream/100_backlog/gemini/20260314_034036_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_transactions_csv_and_evidenceindex_csv_exports.md
 D workstream/100_backlog/gemini/20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md
 D workstream/100_backlog/gemini/20260314_034038_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_assemble_final_quarterly_pack_and_export_delivery_flow.md
 D workstream/100_backlog/gemini/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline.md
 D workstream/100_backlog/gemini/20260314_034040_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_build_confirm_first_evidence_matching_candidate_service.md
 D workstream/100_backlog/gemini/20260314_034041_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_persist_evidence_links_and_unmatched_states_with_user_confirmation.md
 D workstream/100_backlog/gemini/20260314_034044_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_evidence_capture_and_match_confirmation_ui_flow.md
 D workstream/100_backlog/gemini/20260314_034045_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_implement_voice_intents_confirmation_chip_and_undo_flow.md
 D workstream/100_backlog/gemini/20260314_034047_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamF_harden_security_performance_and_legal_disclaimers_for_mvp_release.md
 D workstream/100_backlog/gemini/20260314_034048_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamF_build_end_to_end_mvp_acceptance_and_regression_suite.md
 D workstream/100_backlog/gemini/20260314_210743_breakout_fs_add_product_type_view_selection_across_performance_screens.md.result.md
 D workstream/100_backlog/gemini/20260314_210850_breakout_fs_add_product_to_product_type_allocation_workflow.md
 D workstream/100_backlog/gemini/20260314_214342_20260314_epic_review_extended_decomposition_and_delete.md
 D workstream/100_backlog/gemini/20260314_224854_build_secure_token_storage_and_refresh_lifecycle_s_2.md.result.md
 D workstream/100_backlog/gemini/20260314_224854_define_open_banking_consent_contract_and_provider__0.md.result.md
 D workstream/100_backlog/gemini/20260314_224854_establish_connection_status_and_reconnect_lifecycl_3.md
 D workstream/100_backlog/gemini/20260314_224854_implement_connection_callback_handling_and_bank_ac_1.md
 D workstream/100_backlog/gemini/20260314_234338_breakout_fs_map_products_to_product_type.md
 D workstream/100_backlog/gemini/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_root_readme_and_documentation.md.result.md
 D workstream/100_backlog/gemini/20260316_135215_trading_strategy_warehouse_automate_distribution_and_scheduler.md.result.md.result.md
 D workstream/100_backlog/gemini/20260316_135216_trading_strategy_warehouse_build_subscriber_lifecycle_backend.md
 D workstream/100_backlog/gemini/20260316_135217_claude_trading_strategy_warehouse_build_growth_analytics_dashboard.md.result.md
 D workstream/100_backlog/gemini/20260316_135219_general_trading_strategy_warehouse_define_autonomy_and_safety_guardrails.md
 D workstream/100_backlog/gemini/20260316_161933_skills_make_task_dependency_mandatory.md
 D workstream/100_backlog/gemini/20260316_161933_skills_make_task_dependency_mandatory.md.result.md
 D workstream/100_backlog/gemini/20260316_162650_trading_strategy_warehouse_retrofit_task_dependencies.md.result.md
 D workstream/100_backlog/gemini/20260316_211200_workstream_document_agent_controller_timestamp_entry.md
 D workstream/100_backlog/gemini/20260316_211200_workstream_document_agent_controller_timestamp_entry.md.result.md
 D workstream/100_backlog/gemini/20260316_220223_claude_BLOCKER_20260314_214342_20260314_epic_review_extended_decomposition_and_delete.md.result.md
 D workstream/100_backlog/gemini/20260316_220223_general_BLOCKER_20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md.result.md.result.md
 D workstream/100_backlog/gemini/20260316_232301_general_strategy_warehouse_marketing_engine_workstreamZ_create_docker_compose_configuration.md.result.md
 D workstream/100_backlog/gemini/20260317_010000_breakout_futures_config_updates.md
 D workstream/100_backlog/gemini/20260317_095132_gemini_BLOCKER_20260317_101000_breakout_silence_workflow_prompts.md
 D workstream/100_backlog/gemini/20260317_100000_breakout_silence_workflow_prompts.md.result.md
 D workstream/100_backlog/gemini/20260317_110256_gemini_BLOCKER_20260317_110200_breakout_add_product_type_to_workflows.md
 D workstream/100_backlog/gemini/20260317_135330_claude_BLOCKER_20260316_135216_trading_strategy_warehouse_build_subscriber_lifecycle_backend.md.result.md
 D workstream/100_backlog/gemini/20260317_135330_codex_BLOCKER_20260309_120092_autonomous_trading_signal_platform_workstreamJ_release_mobile_app.md.result.md
 D workstream/100_backlog/gemini/20260317_135343_claude_BLOCKER_20260316_135217_claude_trading_strategy_warehouse_build_growth_analytics_dashboard.md.result.md
 D workstream/100_backlog/gemini/20260317_135343_claude_BLOCKER_20260316_135217_claude_trading_strategy_warehouse_build_growth_analytics_dashboard.md.result.md.result.md
 D workstream/100_backlog/gemini/20260317_135349_claude_BLOCKER_20260317_135330_claude_BLOCKER_20260316_135216_trading_strategy_warehouse_build_subscriber_lifecycle_backend.md.result.md.result.md
 D workstream/100_backlog/gemini/20260317_135357_claude_BLOCKER_20260316_135219_general_trading_strategy_warehouse_define_autonomy_and_safety_guardrails.md
 D workstream/100_backlog/gemini/20260317_135357_claude_BLOCKER_20260316_135219_general_trading_strategy_warehouse_define_autonomy_and_safety_guardrails.md.result.md
 D workstream/100_backlog/gemini/20260317_135409_claude_BLOCKER_20260316_220223_claude_BLOCKER_20260314_214342_20260314_epic_review_extended_decomposition_and_delete.md.result.md.result.md
 D workstream/100_backlog/gemini/20260317_135416_claude_BLOCKER_20260317_135349_claude_BLOCKER_20260317_135330_claude_BLOCKER_20260316_135216_trading_strategy_warehouse_build_subscriber_lifecycle_backend.md.result.md.result.md.result.md
 D workstream/100_backlog/gemini/20260318_172546_claude_BLOCKER_20260314_034028_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_implement_secure_sign_up_and_sole_trader_onboarding_flow.md.result.md
 D workstream/100_backlog/gemini/20260318_172600_claude_BLOCKER_20260309_120092_autonomous_trading_signal_platform_workstreamJ_release_mobile_app.md.result.md.result.md
 D workstream/100_backlog/general/20260316_232327_strategy_warehouse_marketing_engine_workstreamB_create_engagement_tracking_collector.md
 D workstream/100_backlog/general/20260316_232328_strategy_warehouse_marketing_engine_workstreamB_implement_follower_reach_metrics_collector.md
 D workstream/100_backlog/general/20260316_232330_strategy_warehouse_marketing_engine_workstreamC_design_and_build_landing_page.md
 D workstream/100_backlog/general/20260316_232331_strategy_warehouse_marketing_engine_workstreamC_build_subscription_capture_flow.md
 D workstream/100_backlog/general/20260316_232332_strategy_warehouse_marketing_engine_workstreamC_implement_subscriber_database.md
 D workstream/100_backlog/general/20260316_232333_strategy_warehouse_marketing_engine_workstreamC_create_conversion_tracking.md
 D workstream/100_backlog/general/20260316_232334_strategy_warehouse_marketing_engine_workstreamC_build_subscriber_growth_dashboard.md
 D workstream/100_backlog/general/20260316_232340_strategy_warehouse_marketing_engine_workstreamD_build_autonomous_scheduler.md
 D workstream/100_backlog/general/20260316_232341_strategy_warehouse_marketing_engine_workstreamD_create_performance_feedback_loop.md
 D workstream/100_backlog/general/20260316_232342_strategy_warehouse_marketing_engine_workstreamD_build_manual_override_and_kill_switch.md
 D workstream/100_backlog/general/20260316_232343_gemini_strategy_warehouse_marketing_engine_workstreamD_create_weekly_metrics_report_generator.md
 D workstream/100_backlog/general/20260316_232344_gemini_strategy_warehouse_marketing_engine_workstreamD_implement_health_monitoring_and_alerting.md
 D workstream/100_backlog/pending/claude/20260313_220646_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_build_shock_simulation_and_scenario_validation_harness.md
 D workstream/100_backlog/pending/claude/20260313_221233_workstream_move_decomposed_epic_root_tasks_to_general_backlog.md.result.md
 D workstream/100_backlog/pending/claude/20260314_034028_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_implement_secure_sign_up_and_sole_trader_onboarding_flow.md
 D workstream/100_backlog/pending/claude/20260314_034030_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_build_idempotent_transaction_import_and_90_day_backfill.md
 D workstream/100_backlog/pending/claude/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md.result.md
 D workstream/100_backlog/pending/claude/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_contract_first_api_documentation_for.md.result.md
 D workstream/100_backlog/pending/claude/20260316_232320_strategy_warehouse_marketing_engine_workstreamB_implement_twitter_connector.md
 D workstream/100_backlog/pending/claude/20260316_232321_strategy_warehouse_marketing_engine_workstreamB_implement_discord_connector.md.result.md
 D workstream/100_backlog/pending/claude/20260316_232322_strategy_warehouse_marketing_engine_workstreamB_implement_telegram_connector.md.result.md
 D workstream/100_backlog/pending/claude/20260316_232323_strategy_warehouse_marketing_engine_workstreamB_implement_linkedin_connector.md
 D workstream/100_backlog/pending/claude/20260316_232323_strategy_warehouse_marketing_engine_workstreamB_implement_linkedin_connector.md.result.md
 D workstream/100_backlog/pending/claude/20260316_232325_strategy_warehouse_marketing_engine_workstreamB_implement_tiktok_connector.md.result.md
 D workstream/100_backlog/pending/claude/20260316_232326_strategy_warehouse_marketing_engine_workstreamB_build_posting_rules_engine.md.result.md
 D workstream/200_inprogress/20260317_205500_strategy_warehouse_marketing_engine_workstreamB_refine_tiktok_connector.md
 D workstream/200_inprogress/blocker/codex/20260318_183857_codex_BLOCKER_20260318_183811_codex_BLOCKER_20260316_232321_strategy_warehouse_marketing_engine_workstreamB_implement_discord_connector.md.result.md.result.md
 D workstream/200_inprogress/blocker/codex/20260318_183901_codex_BLOCKER_20260318_183824_codex_BLOCKER_20260316_232322_strategy_warehouse_marketing_engine_workstreamB_implement_telegram_connector.md.result.md.result.md
 D workstream/200_inprogress/blocker/codex/20260318_183908_codex_BLOCKER_20260316_232323_strategy_warehouse_marketing_engine_workstreamB_implement_linkedin_connector.md.result.md
 D workstream/200_inprogress/blocker/codex/20260318_183921_codex_BLOCKER_20260316_232325_strategy_warehouse_marketing_engine_workstreamB_implement_tiktok_connector.md.result.md
 D workstream/200_inprogress/blocker/codex/20260318_183934_codex_BLOCKER_20260316_232326_strategy_warehouse_marketing_engine_workstreamB_build_posting_rules_engine.md.result.md
 D workstream/200_inprogress/blocker/codex/20260318_184007_codex_BLOCKER_20260316_232320_strategy_warehouse_marketing_engine_workstreamB_implement_twitter_connector.md
 D workstream/200_inprogress/blocker/codex/20260318_184316_codex_BLOCKER_20260318_183839_codex_BLOCKER_20260316_232323_strategy_warehouse_marketing_engine_workstreamB_implement_linkedin_connector.md.result.md
 D workstream/200_inprogress/claude/20260309_120043_autonomous_trading_signal_platform_workstreamE_implement_discord_connector.md
 D workstream/200_inprogress/claude/20260309_120044_autonomous_trading_signal_platform_workstreamE_create_posting_rules.md
 D workstream/200_inprogress/codex/20260227_220000_claude_fxpilot_frontend_data_integration.md.result.md
 D workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md.result.md
 D workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md.result.md
 D workstream/200_inprogress/codex/20260302_035617_claude_pipHunter_drilldown_exit_time_column.md.result.md
 D workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md.result.md
 D workstream/200_inprogress/codex/20260308_162720_trading_signal_social_templates.md.result.md
 D workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md.result.md
 D workstream/200_inprogress/codex/20260310_120000_workstream_orchestrator_epic_task_review_screen.md.result.md
 D workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md.result.md.result.md
 D workstream/200_inprogress/codex/20260314_034028_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_implement_secure_sign_up_and_sole_trader_onboarding_flow.md.result.md
 D workstream/200_inprogress/codex/20260314_034042_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_mobile_inbox_exception_queue_screen.md.result.md
 D workstream/200_inprogress/codex/20260314_034043_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_quarter_readiness_and_finish_now_screen.md.result.md
 D workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_local_setup_scripts_and.md.result.md
 D workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md.result.md
 D workstream/200_inprogress/codex/20260316_135218_gemini_trading_strategy_warehouse_build_growth_optimization_loop.md.result.md.result.md
 D workstream/200_inprogress/codex/20260316_232320_strategy_warehouse_marketing_engine_workstreamB_implement_twitter_connector.md.result.md.result.md
 D workstream/200_inprogress/codex/20260317_101000_breakout_silence_workflow_prompts.md.result.md
 D workstream/200_inprogress/gemini/20260309_120041_autonomous_trading_signal_platform_workstreamE_implement_x_connector.md.result.md
 M workstream/300_complete/20260317_010000_breakout_futures_config_updates.md
 M workstream/300_complete/claude/20260309_120043_autonomous_trading_signal_platform_workstreamE_implement_discord_connector.md
 M workstream/300_complete/claude/20260309_120044_autonomous_trading_signal_platform_workstreamE_create_posting_rules.md
 D workstream/300_complete/claude/20260316_161933_skills_make_task_dependency_mandatory.md
 M workstream/300_complete/claude/20260316_211200_workstream_document_agent_controller_timestamp_entry.md
 D workstream/400_failed/claude/20260224_130300_breakout_phase2_deployment.md.result.md
 D workstream/400_failed/codex/20260319_222632_breakout_profile_topx_delta_type_tb.md
 M workstream/agent.lock
 M workstream/excluded_workers.txt
 M workstream/kanban_dashboard.py
 M workstream/run_agent.py
?? .adal/
?? .agent/
?? .agents/
?? .augment/
?? .augmentignore
?? .claude/
?? .codebuddy/
?? .commandcode/
?? .continue/
?? .cortex/
?? .crush/
?? .factory/
?? .gemini/
?? .goose/
?? .iflow/
?? .junie/
?? .kilocode/
?? .kiro/
?? .kode/
?? .mcpjam/
?? .mux/
?? .neovate/
?? .openhands/
?? .pi/
?? .playwright-cli/
?? .playwright-mcp/
?? .pochi/
?? .qoder/
?? .qwen/
?? .roo/
?? .trae/
?? .venv/
?? .vibe/
?? .vscode/
?? .windsurf/
?? .zencoder/
?? AGENTS.md
?? AI_trades_agents/
?? AI_voice/
?? APPS/
?? Content/
?? DESIGN.md
?? DataInsights/.env.example
?? DataInsights/.venv/
?? DataInsights/AGENTS.md
?? DataInsights/alembic.ini
?? DataInsights/alembic/
?? DataInsights/dashboard.html
?? DataInsights/db/
?? DataInsights/prd/
?? DataInsights/pyproject.toml
?? DataInsights/src/__init__.py
?? DataInsights/src/config.py
?? DataInsights/src/db.py
?? DataInsights/src/local_insight_engine.egg-info/
?? DataInsights/src/main.py
?? DataInsights/src/models.py
?? DataInsights/src/observability/
?? DataInsights/src/pipelines/
?? DataInsights/src/routers/
?? DataInsights/src/scheduler.py
?? DataInsights/src/schemas.py
?? DataInsights/src/services/
?? DataInsights/src/templates/
?? DataInsights/tests/
?? Database/
?? Database_20250609_1432.zip
?? GEMINI.md
?? Game_trader_backup_20251022_163839.zip
?? Game_trader_backup_20251022_163839/
?? Game_trader_ms/
?? SL/
?? SP/
?? Test/
?? "TradeApps - Copy.zip"
?? TradeApps.zip
?? TradeApps_20251220_0455.zip
?? TradeApps_20251222_0125.zip
?? TradeDbApp/
?? Trades/
?? Trades_20251124_2335.zip
?? Trades_20251209_1615.zip
?? Trades_20251210.zip
?? TradingDashboard/
?? TradingDashboard3/
?? _codex_dump_log.py
?? _codex_leader_check.py
?? _codex_tmp.py
?? _codex_tmp2.py
?? _codex_tmp3.py
?? _tmp_api_test.py
?? _tmp_file
?? _tmp_patch.diff
?? access_token/
?? advanced_forex_signal_generator.py
?? algo/
?? algo_crypto/
?? algo_forex/
?? algo_simulate/
?? algo_viewer_20250726_0114.zip
?? algo_viewer_20250726_0154_refactor.zip
?? "algo_viewer_20250727_2056.zip(current version)"
?? algo_viewer_20250728_0024.zip
?? algo_viewer_20250728_1449.zip
?? algo_viewer_20250728_2141.zip
?? algo_viewer_20250729_0309_64_3_10.zip
?? algo_viewer_20250807_0356.zip
?? algo_viewer_20250824_0009.zip
?? algo_viewer_20251201_0107.zip
?? algo_viewer_20251201_1517.zip
?? algo_viewer_20251202_1632.zip
?? algo_viewer_20251202_2048.zip
?? algo_viewer_20251208_2228.zip
?? algo_viewer_64_2_10_20250826_1452.zip
?? algo_viewer_64_2_7_20250825_0359.zip
?? algo_zone_viewer.zip
?? algo_zone_viewer/
?? analyse_extract_model_output_to_csv2.py
?? analyze_recent_performance.py
?? api/
?? api_server.py
?? api_server_pg/
?? api_server_sql.zip
?? "api_server_sql/main copy.py"
?? api_server_sql/main.py.bak
?? api_server_sql/main.py.bak_20251208_170758
?? api_server_sql/run_server.bat
?? api_server_sql_copy/
?? app.py
?? apply_breach_logic.sql
?? apply_core_views.sql
?? apply_final_triggers.sql
?? arc_count.txt
?? basic-windows-setup.bat
?? batch_migrate_logic.py
?? bizAfroExchange/
?? bizETRM/
?? bizPA/
?? bizPhoneApp/
?? bizpa_data_cloud.sql
?? bizpa_full_migration.sql
?? bizpa_schema_cloud.sql
?? builds/
?? chats/
?? check_bytes.js
?? check_cols.txt
?? check_latest_pg_data.py
?? check_sp9006.txt
?? check_tables.py
?? cleanup_cache.py
?? cols.txt
?? combined_trade_algo_202560406.zip
?? combined_trades_closed_help.txt
?? combined_trades_open_help.txt
?? common_types.txt
?? compare_dbs.py
?? copy.bat
?? crash2.txt
?? crash_log.txt
?? crash_log2.txt
?? crypto_quotes.txt
?? daksheen_redesign.html
?? dashboard.html
?? data/
?? data_migration/
?? data_migration2/
?? db_analysis/
?? db_comparison_report.md
?? db_dependencies
?? db_scripts/
?? db_scripts_20251001_0110.zip
?? db_scripts_20251007_2229.zip
?? db_scripts_20251104.zip
?? db_scripts_20251115_0239.zip
?? debug_bias_summary.py
?? debug_cat_bias.py
?? debug_closed_bias.py
?? debug_db_check.py
?? debug_fs_totals.py
?? debug_join.txt
?? debug_sum_trades.py
?? debug_summary.txt
?? debug_summary_net.py
?? debug_top300_bias.py
?? dna_100007_20260123.txt
?? dna_100216_20260123.txt
?? dna_100216_data.txt
?? dna_pnl_stream_cache.txt
?? eds.code-workspace
?? eds.lnk
?? env/
?? ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/
?? epics/
?? error_log.txt
?? event_log.jsonl
?? exports/
?? final_col_check.txt
?? final_fx_check.txt
?? final_sp_output.txt
?? find_open_l_trades.py
?? fix_pg_errors.sql
?? fn_legs_src.sql
?? forex-data-viewer.zip
?? forex-data-viewer/
?? forex_data_download/
?? forex_signal_generator.py
?? funcuts_redesign.html
?? futures_quotes.txt
?? fx_quotes_check.txt
?? gbp_trading_app/
?? get-pip.py
?? get_procs.ps1
?? get_views.ps1
?? groq/
?? grouped_test.txt
?? hotfix_common.py
?? hotfix_summary_gen.py
?? identified_outputs.txt
?? implementation_plan.md
?? inspect_db.py
?? interactive_dashboard.html
?? interactive_profitability_dashboard.html
?? jar/
?? job_scraper/
?? json/
?? key.json
?? list_views.py
?? live_market_data/
?? logs/
?? market_prices_api/
?? market_prices_api_with_options/
?? market_simulator.py
?? migrate/
?? migrate_tables_to_pg.py
?? migrate_triggers_to_pg.py
?? migrate_views_to_pg.py
?? mismatches.txt
?? missing_objects_report.md
?? mobile_app_repo/
?? model_check.txt
?? move_trade_RT2_files.py
?? move_trade_RT_files.py
?? n8n/
?? obs/
?? online_db_schema.sql
?? parity_check.txt
?? patch.diff
?? performance_rankings.txt
?? pg_arc_count.txt
?? pg_counts.txt
?? pg_data_check.txt
?? pg_final.txt
?? pg_triggers_list.txt
?? plans/20260128_1555_V20260128_1555_CHART_STABILIZATION_PLAN.md
?? plans/20260128_1917_V20260128_1900_GRID_MONITOR_AND_UI_SYNC_RESCUE.md
?? plans/20260128_2120_V20260128_2120_freq_explorer_consistency.md
?? plans/20260128_2125_V20260128_2125_multichart_top_x_ui.md
?? plans/20260128_2135_V20260128_2135_card_management_reordering_transfer.md
?? plans/20260128_2140_V20260128_2140_reorder_dom_sync_fix.md
?? plans/20260128_2145_V20260128_2145_multi_view_sync.md
?? plans/20260128_2300_V20260128_2300_multichart_drilldown_fix.md
?? plans/20260128_ltrade_adjustment.md
?? plans/20260129_0130_V20260129_0130_overtrading_fix.md
?? plans/20260129_0245_V20260129_0245_atomic_sync_ui_fix.md
?? plans/20260129_0325_V20260129_0325_hardware_safety_plan.md
?? plans/20260129_0435_V20260129_0435_guid_integration_plan.md
?? plans/20260129_1038_V20260129_1038_grid_live_simplification.md
?? plans/20260129_1042_V20260129_1042_snap_leader_plan.md
?? plans/20260129_1055_V20260129_1055_periodic_leader_plan.md
?? plans/20260129_1200_V20260129_1200_disable_trading_monitor_plan.md
?? plans/20260129_1400_V20260129_1400_reduce_card_height_plan.md
?? plans/20260129_1610_V20260129_1615_fix_performance_drilldown_plan.md
?? plans/20260129_2330_V20260129_2330_remove_dots_plan.md
?? plans/20260130_0410_V20260130_0415_Rank1_Appearances.md
?? plans/20260130_0910_V20260130_0915_Freq_Drilldown.md
?? plans/20260130_1000_V20260130_1000_Global_Menu_Integration.md
?? plans/20260130_1010_V20260130_1010_Activation_Column.md
?? plans/20260130_1130_V20260130_1135_GridLive_Activation_Fix.md
?? plans/20260130_1310_V20260130_1315_AppHealthMonitor.md
?? plans/20260130_1410_V1410_Features_Health_PNL.md
?? plans/20260130_1515_V1515_Grid_Duplicates_Dots.md
?? plans/20260130_1550_V1550_All_Local_Time.md
?? plans/20260130_1710_Rank1_Alert_Feature.md
?? plans/20260130_2040_V20260130_2045_Rank_Improvement_Alert.md
?? plans/20260131_0450_V20260131_0450_Rank_Improvement_Alert_Impl.md
?? plans/20260201_0230_V20260201_0230_DNA_Frequency_Extraction_Update.md
?? plans/20260201_0449_bypass_notifier_plan.md
?? plans/20260201_1505_notifier_requirements.md
?? plans/20260201_2345_V20260201_2345_System_Health_Dashboard.md
?? plans/20260202_1200_V20260202_1200_Show_All_Live_Trades.md
?? plans/20260202_1215_V20260202_1215_Show_All_Live_Trades_FS.md
?? plans/20260202_1230_V20260202_1230_Restore_Live_Filter_FS.md
?? plans/20260202_1235_V20260202_1235_Optimize_Live_Trades_Refresh.md
?? plans/20260202_1245_V20260202_1245_Frequency_Explorer_Past_Data.md
?? plans/20260202_1250_V20260202_1250_Restore_Frequency_Explorer.md
?? plans/20260202_1330_V20260202_1330_Fix_Frequency_Explorer_Script.md
?? plans/20260202_1345_V20260202_1345_MultiChart_Rank1_Loader.md
?? plans/20260202_1520_V20260202_1520_Rank1_V2_V3.md
?? plans/20260202_1650_V20260202_1650_Generate_Live_Trades_JSON.md
?? plans/20260202_1740_V20260202_1740_Cumulative_Col.md
?? plans/20260203_0130_V20260203_0130_fix_weighted_race.md
?? plans/20260203_0150_V20260203_0200_weighted_race_rank_filter.md
?? plans/20260203_0940_V20260203_0940_live_trades_cumulative.md
?? plans/20260203_1000_V20260203_1000_Fix_Trade_Extraction_Collision.md
?? plans/20260203_1100_V20260203_1100_Fix_Live_Trade_Counting.md
?? plans/20260203_1105_V20260203_1105_Revert_Live_Trade_Counting.md
?? plans/20260203_1200_V20260203_1200_Rank_Score_Column.md
?? plans/20260203_1215_rank_metric_selector_plan.md
?? plans/20260204_1245_V20260204_1245_fix_l_trade_metadata_leak.md
?? plans/20260204_1255_V20260204_1255_save_to_trade_bucket_and_metadata_fix.md
?? plans/20260204_1410_V20260204_1410_trade_bucket_workflow_refinement.md
?? plans/20260204_1440_V20260204_1440_trade_bucket_restoration_fix.md
?? plans/20260204_1610_V20260204_1610_trade_bucket_preset_integration.md
?? plans/20260204_1630_V20260204_1630_multi_chart_visibility_fix.md
?? plans/20260204_1640_V20260204_1640_grid_live_source_persistence.md
?? plans/20260204_1650_V20260204_1650_dynamic_source_attribution.md
?? plans/20260204_1940_V20260204_1940_activation_explorer_source.md
?? plans/20260204_2000_V20260204_2000_frequency_blocking_source_fix.md
?? plans/20260204_2120_V20260204_2120_bucket_auto_promotion.md
?? plans/20260204_2125_V20260204_2130_bucket_tb_prefix.md
?? plans/20260204_2155_V20260204_2155_no_more_ui.md
?? plans/20260204_2158_V20260204_2200_hard_block_ui.md
?? plans/20260204_2235_V20260204_2235_drilldown_alt_net.md
?? plans/20260205_0945_V20260205_0945_drilldown_csv_export.md
?? plans/20260205_0955_V20260205_0955_model_filter_all_tables.md
?? plans/20260205_1230_V20260205_1230_batch_chart_generation.md
?? plans/20260205_2054_V20260205_2100_AUTOMATED_TRADE_SOURCE_PLAN.md
?? plans/20260205_2120_V20260205_2120_ACTIVATION_REMOVE_ALL_PLAN.md
?? plans/20260205_2120_V20260205_2125_ACTIVATION_REMOVE_ALL_PLAN.md
?? plans/20260205_2120_V20260205_2130_ACTIVATION_REMOVE_ALL_PLAN.md
?? plans/20260205_2142_V20260205_2145_TOP20_DIRECTIONAL_AUTO_PLAN.md
?? plans/20260205_2155_V20260205_2200_DRILLDOWN_FIX_PLAN.md
?? plans/20260205_2255_V20260205_2300_UI_OPS_PLAN.md
?? plans/20260206_0230_V20260206_1000_STRATEGY_SELECTOR_PLAN.md
?? plans/20260206_0300_V20260206_1100_WINRATE_SELECTION_PLAN.md
?? plans/20260206_1200_V20260206_1200_TIMELINE_PLAYBACK_PLAN.md
?? plans/20260206_1930_V20260206_1930_PICKER_OPEN_TIME_PLAN.md
?? plans/20260206_1935_V20260206_1935_PICKER_MENU_PLAN.md
?? plans/20260206_2030_V20260206_2030_PICKER_REFINEMENT_PLAN.md
?? plans/20260206_2040_V20260206_2040_SOURCE_TAGGING_PLAN.md
?? plans/20260207_1615_V20260207_1615_PICKER_MODE_DIRECTION_PLAN.md
?? plans/20260208_1400_V20260208_1400_PICKER_SCALPER_ONLY.md
?? plans/20260208_1730_V20260208_1730_INCREASE_VIEW_300.md
?? plans/20260208_1910_V20260208_1910_AI_PICKER_REVISIT.md
?? plans/20260208_2200_V20260208_2200_SMART_TARGET_PROMPT.md
?? plans/20260209_1010_TESTING_GUIDE.md
?? plans/20260209_1010_V20260209_1010_BIAS_NOTIFICATION_INTEGRATION.md
?? plans/20260209_1720_V20260209_1720_BIAS_ALIGNED_SWITCHING.md
?? plans/20260209_1725_BIAS_SWITCHING_SUMMARY.md
?? plans/20260209_1725_V20260209_1725_bias_switching_plan.md
?? plans/20260209_1900_DEPLOYED.md
?? plans/20260209_1900_FINAL_VERIFICATION.md
?? plans/20260209_1900_V20260209_1900_IMPLEMENTATION_COMPLETE.md
?? plans/20260209_2220_V20260209_2220_fix_playback_and_picker_stats.md
?? plans/20260210_0225_V20260210_0230_performance_breakdown_plan.md
?? plans/20260210_0235_V20260210_0245_DNA_Breakdown_Modal_Plan.md
?? plans/20260210_0235_V20260210_0245_Performance_Summary_Modal_Plan.md
?? plans/20260210_0345_V20260210_0400_bias_flip_fix_plan.md
?? plans/20260210_0428_V20260210_0400_Bias_Flip_Fix_Commit.md
?? plans/20260210_0615_V20260210_0615_Persist_Hierarchy_State.md
?? plans/20260210_1130_V20260210_1130_Fix_DrillDown.md
?? plans/20260210_1140_V20260210_1140_Leaderboard_Opt.md
?? plans/20260210_1145_V20260210_1145_Leaderboard_DrillDown.md
?? plans/20260210_1155_V20260210_1155_Fix_Toggle_Error.md
?? plans/20260210_1210_V20260210_1210_Fix_Modal_ZIndex.md
?? plans/20260210_1223_V20260210_1223_Fix_Grid_Sync.md
?? plans/20260210_1305_V20260210_1305_Fix_Bias_Alignment.md
?? plans/20260210_1311_V20260210_1311_Revert_Bias_Logic.md
?? plans/20260210_1415_V20260210_1415_Summary_Timebar.md
?? plans/20260210_1445_V20260210_1450_Bias_Scrub_Playback_Fix.md
?? plans/20260211_1515_V20260211_1515_Fix_Summary_Expansion.md
?? plans/20260211_1520_V20260211_1520_Grid_Monitor_Disabled_Investigation.md
?? plans/20260211_1525_V20260211_1525_Re_Enable_Grid_Monitor.md
?? plans/20260211_1530_Auto_Buy_Execution_Flow.md
?? plans/20260211_1540_V20260211_1540_Auto_Buy_Fix_Summary.md
?? plans/20260212_2055_V20260212_2055_Session_Change_Log.md
?? plans/20260213_0942_advanced_trading_ideas.md
?? plans/20260213_0945_PipHunter_Extension_Ideas.md
?? plans/20260213_0945_trading_ideas.md
?? plans/20260213_1048_V20260213_1048_Promotion_Blocks_Screen.md
?? plans/20260213_1311_V20260213_1311_Multi_Source_Grouped_LTrade_Requirements.md
?? plans/20260214_2000_V20260214_2000_Fixing_Trade_Bucket_PnL.md
?? plans/20260215_0005_V20260215_0005_Health_Alarm_Sim_Fix.md
?? plans/20260215_1440_V20260215_1440_Collapse_Live_Trades_Sections.md
?? plans/20260216_1530_V20260216_1530_PipHunter_Supabase_Setup.md
?? plans/20260217_2345_V20260217_2345_bizPA_WS2_Data_API_Plan.md
?? plans/20260218_0000_V20260218_0000_bizPA_WS4_Security_Ops_Plan.md
?? plans/20260218_0035_V20260218_0035_bizPA_Imp_1.1_Scaffolding_Plan.md
?? plans/20260218_0050_V20260218_0050_bizPA_Imp_1.1_Backend_Plan.md
?? plans/20260219_1500_V20260219_1500_bizPA_Imp_1.2_Schema_Plan.md
?? plans/20260219_1530_V20260219_1530_bizPA_Imp_1.3_Voice_API_Plan.md
?? plans/20260219_1600_V20260219_1600_bizPA_Imp_1.4_Item_CRUD_Plan.md
?? plans/20260219_1630_V20260219_1630_bizPA_Imp_1.5_Undo_Plan.md
?? plans/20260219_1700_V20260219_1700_bizPA_Imp_2.1_Search_Plan.md
?? plans/20260220_0036_V20260220_0036_Add_All_Windows.md
?? plans/20260222_1347_V20260222_1347_remove_trade_bucket_create_panel.md
?? plans/20260224_1340_V20260224_1340_periodic_market_update.md
?? plans/20260226_1148_V20260226_1148_add_scalper_filters_top20.md
?? plans/20260226_1253_V20260226_1253_breakout_tb_strategy_live_net_sum.md
?? plans/20260226_1520_V20260226_1520_breakout_add_top_x_multi_chart.md
?? plans/20260301_1925_v1.2.9_bizPA_Public_Tunnel_Verification.md
?? plans/20260304_1400_V1.1.8_Trading_Trainer_UI.md
?? plans/20260305_1800_V20260305_1800_SQL_TO_PG_MIGRATION.md
?? plans/20260306_1845_V20260306_1845_topx_metric_type_selector.md
?? plans/20260308_1941_V20260308_1941_add_metrics_related_strategies.md
?? plans/20260308_2137_V20260308_2137_trade_bucket_metric_display.md
?? plans/20260310_2151_V20260310_2151_Single_Canvas_Auto_Split_Chart.md
?? plans/20260311_1215_V20260311_1215_TB_VALIDATION_RULES.md
?? plans/20260311_132200_V20260311_1330_SignalFilter_Drilldown.md
?? plans/20260311_1345_V20260311_1345_TB_Validation_Permanent_Fix.md
?? plans/20260312_1405_V20260312_1405_Top_X_Workflow_Documentation.md
?? plans/20260312_1410_V20260312_1410_Add_Positive_Net_Filter.md
?? plans/20260312_1445_V20260312_1445_DrillDown_Optimization.md
?? plans/20260314_1630_V20260314_1630_git_commit_tradeapp_workstream.md
?? plans/20260316_0155_V20260316_0155_Modify_Health_Check_Path.md
?? plans/20260316_1430_V20260316_1430_Dynamic_Pip_Multiplier.md
?? plans/20260317_0025_V20260317_0025_UI_Visibility_Fix.md
?? plans/20260317_0100_V20260317_0100_Futures_Config_Updates.md
?? plans/20260317_1530_V20260317_1530_Kanban_Agent_Routing_Fix.md
?? plans/20260317_1715_V20260317_1715_Agent_CLI_Syntax_Fix.md
?? plans/20260317_1730_V20260317_1730_Kanban_Delivered_Column.md
?? plans/20260317_1945_V20260317_1945_Refine_Delivered_Column_Grouping.md
?? plans/20260318_1010_V20260318_1010_Frequency_Explorer_Product_Filter.md
?? plans/20260318_1055_V20260318_1055_Frequency_Explorer_Data_Fix.md
?? plans/20260319_1245_V20260319_1245_Creation_Net_Column.md
?? plans/20260320_1230_V20260320_1230_TB_Leadership_LTrades.md
?? plans/20260320_1245_V20260320_1245_TB_Leadership_Tracking.md
?? plans/20260320_1250_V20260320_1250_Rename_Leadership_Json.md
?? plans/20260321_0244_V1_landing_page_layout.md
?? plans/20260321_0345_V20260321_0345_Implement_double_opt_in_and_subscriber_lifecycle_backend.md
?? plans/20260321_0930_V20260321_0930_B1_implement_transaction_classification_model.md
?? plans/20260321_1000_V20260321_1000_inbox_micro_decision_actions.md
?? plans/20260321_1100_V20260321_1100_Add_Product_Type_To_Workflows.md
?? plans/20260321_1200_V20260321_1200_build_quarter_model_readiness_metrics.md
?? plans/20260321_1445_V20260321_1445_C7_Conversion_Tracking.md
?? plans/20260322_1730_V20260322_1730_Implement_Merchant_Rules.md
?? plans/20260322_1745_V20260322_1745_generate_export_csvs.md
?? plans/20260322_1900_V20260322_1900_Generate_Quarterly_Summary_and_Pack.md
?? plans/20260323_1500_V20260323_1500_TopX_Positive_Total_Net_Requirement.md
?? plans/20260323_1510_V20260323_1510_TopX_Expansion_Filter_Fix.md
?? plans/20260323_1650_V20260323_1700_multi_chart_green_dots_logic.md
?? plans/20260325_1300_V20260325_1300_Add_Chart_Button_Strategy_Perf.md
?? plans/20260327_0113_V20260327_0115_build_confirm_first_evidence_matching_candidate_service.md
?? plans/20260331_1445_V20260331_1445_Install_Specific_Skills.md
?? plans/20260401_1840_V20260401_1840_verify_twitter_summary_returns.md
?? plans/20260401_2330_V20260401_2330_Correct_Weekly_Aggregation.md
?? plans/20260402_0110_V20260402_0110_Twitter_Summary_Returns_Post.md
?? plans/APK/
?? plans/chats/20260219_1028_codex_chat.txt
?? plans/chats/chat_claude_20260128_0233.txt
?? plans/chats/chat_codex_20260210_2010.txt
?? plans/chats/chat_gemini_20260220_1309.txt
?? plans/chats/chat_gemini_20260221_0345.txt
?? plans/chats/chat_gemini_20260221_1430.txt
?? plans/chats/chat_gemini_20260325_1200.txt
?? plans/code_change/20260218_0900_V20260215_2105_Widen_Top20_Modal.md
?? plans/ideas/
?? plans/marketing/
?? plumbers_se19_se20_without_websites.csv
?? postgres_inventory.txt
?? postgres_raw.txt
?? price-differential-dashboard/
?? price_generator/
?? prices/
?? python_trading_dashboard/
?? quant-trading-dashboard/
?? rebuild_core_tables.py
?? research_dashboard.html
?? rest_api/
?? rest_api_plan.md
?? run_all_apis.bat
?? run_final_diff.py
?? run_simulation.bat
?? run_sp_000.sql
?? saas/
?? scrape_plumbers.py
?? scrape_plumbers_v2.py
?? scrape_plumbers_v3.py
?? scrape_plumbers_v4.py
?? scrape_salons.py
?? screenshots/
?? simulate_trades.py
?? skills-lock.json
?? skills/
?? social_media_trade_blocks_sample.md
?? sp_001_create_trades_pg.sql
?? sp_001_v2_pg.sql
?? sp_001_v2_src.sql
?? sp_001_v3_src.sql
?? sp_003_close_pg.sql
?? sp_003_src.sql
?? sp_9004_src.sql
?? sp_9006_help.txt
?? sp_check.txt
?? sp_def.txt
?? sp_def_full.sql
?? sp_load_quotes_src.sql
?? sp_output_after_snapshot.txt
?? sp_output_before_first_insert.txt
?? sp_output_first_log_print.txt
?? sp_output_rowcount_check.txt
?? sp_output_with_print_snapshot.txt
?? sp_refresh_dna_pnl_cache.sql
?? sp_refresh_dna_pnl_cache_clean.sql
?? sp_test_result_set_output.txt
?? sql_scripts/
?? sql_server_inventory.txt
?? sql_server_inventory_v2.txt
?? sql_server_inventory_v3.txt
?? sql_server_raw.txt
?? sql_triggers.txt
?? sqlserver_to_postgre/
?? ss_counts.txt
?? ss_data_check.txt
?? ss_final.txt
?? start_all_trading_apps.bat
?? start_breakout_db_services.bat
?? stop_all_trading_apps.bat
?? stub_missing_objects.py
?? stub_missing_objects_pyodbc.py
?? sync_all_data_to_pg.py
?? sync_data_to_pg.py
?? sync_engine/
?? sync_resume.py
?? sync_tradedb.py
?? synthetic-trading-platform-roo/
?? synthetic-trading-platform/
?? tbl_105_trade_lifecycle_snapshots.txt
?? tbl_archive_dynamic_leadership.txt
?? tbl_top_one_archive.txt
?? temp_analysis_script.py
?? temp_backfill_strategy_names.sql
?? temp_check_latest_closed_tradeable_status_output.txt
?? temp_close_test_trades_output_4.txt
?? temp_close_test_trades_output_5.txt
?? temp_edit.py
?? temp_fix_spacing2.py
?? temp_insert_test_trade_output_4.txt
?? temp_insert_test_trade_s_output_4.txt
?? temp_inspect.py
?? temp_inspect_arrow.py
?? temp_replace_functions.py
?? temp_report.py
?? temp_sum_alt_net_by_direction.py
?? temp_sum_net_return.py
?? temp_sum_net_return_by_direction.py
?? temp_test.py
?? temp_test_archive.py
?? temp_test_rt_metrics_output.txt
?? temp_trigger_update_output_2.txt
?? temp_update_script.py
?? test.txt
?? test_log.txt
?? test_path_resolution.py
?? test_write.txt
?? testenv/
?? tests/
?? tmp_backend_log.txt
?? tmp_inspect.py
?? tmp_old.txt
?? tmp_patch.ps1
?? tmp_patch.txt
?? tmp_segment_repr.txt
?? tmp_snippet.txt
?? tmp_summary.js
?? tmp_weighted_top.py
?? tools/
?? trade_dashboard/
?? trade_monitor_sim.err
?? trade_monitor_stderr.txt
?? trade_monitor_stdout.txt
?? trade_monitor_test.err
?? trade_monitor_test.out
?? trade_workflows/
?? tradedb/
?? tradepanel.log.1
?? tradepanel.log.2
?? tradepanel.log.5
?? trades_rt/
?? trades_rt2/
?? trades_rt3/
?? trades_rt3_sim/
?? trading_agent_model.zip
?? trading_dashboard.py
?? trading_forensics_20260323.mp4
?? trading_podcast_20260323.wav
?? trading_summary_20260323.mp4
?? transpiler_sql_to_pg.py
?? trg_rt_src.sql
?? twitter_snapshot.md
?? tws_fetch_bid_ask5_refactored.py
?? tws_monitor_and_place_trade02.py
?? type_diffs.txt
?? update_sp_staging.sql
?? view_count.txt
?? vwCombined_trades_closed_src.txt
?? vw_106_src.sql
?? vw_113_combined_trades_all_src.txt
?? vw_def.txt
?? web_apps/
?? workstream/.env.example
?? workstream/.gitignore
?? workstream/000_epic/20260327_143000_epic_high_end_landing_page_redesign_series.md
?? workstream/000_epic/20260330_163957_trade_panel.md
?? workstream/100_backlog/claude/20260314_034048_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamF_build_end_to_end_mvp_acceptance_and_regression_suite.md
?? workstream/100_backlog/codex/20260403_050000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/100_backlog/general/20260224_130300_breakout_phase2_deployment.md.result.md
?? workstream/100_backlog/general/20260313_220646_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_build_shock_simulation_and_scenario_validation_harness.md.result.md.result.md
?? workstream/100_todo/
?? workstream/200_inprogress/20260320_000130_breakout_multichart_leadership_change_dots.md
?? workstream/200_inprogress/20260320_102214_breakout_tb_strategy_drilldown.md
?? workstream/200_inprogress/20260320_104126_breakout_tb_leader_crown.md
?? workstream/200_inprogress/20260320_110503_breakout_tb_leader_definition.md
?? workstream/200_inprogress/20260320_125500_breakout_mark_l_trades.md
?? workstream/200_inprogress/20260322_011037_workstream_fix_epic_reconciliation_epic_list.md
?? workstream/200_inprogress/20260322_021456_workstream_backfill_strategy_warehouse_manifest_and_require_manifest_rule.md
?? workstream/200_inprogress/20260322_024422_workstream_split_reconciliation_planned_vs_execution_health.md
?? workstream/200_inprogress/20260322_025250_workstream_verify_and_enforce_max_one_inprogress_task_per_model_lane.md
?? workstream/200_inprogress/20260322_204814_ep_strategy_warehouse_marketing_run_test.md
?? workstream/200_inprogress/20260327_134134_funcuts_modern_homepage_redesign.md
?? workstream/200_inprogress/20260327_215333_tools_scrape_hairdressers_barbers_emails.md
?? workstream/200_inprogress/20260331_134840_workstream_twitter_draft_automation_twice_daily.md
?? workstream/200_inprogress/20260331_150216_breakout_social_posting_frontend_data_alignment.md
?? workstream/200_inprogress/20260331_153911_workstream_twitter_post_automation_twice_daily.md
?? workstream/200_inprogress/20260331_154605_breakout_implement_twitter_posting_automation.md
?? workstream/200_inprogress/20260402_153752_breakout_diagnose_twitter_post_submit_failure_after_verified_login.md
?? workstream/200_inprogress/blocker/gemini/
?? workstream/200_inprogress/claude/20260309_120043_autonomous_trading_signal_platform_workstreamE_implement_discord_connector.md.result.md
?? workstream/200_inprogress/claude/20260309_120044_autonomous_trading_signal_platform_workstreamE_create_posting_rules.md.result.md
?? workstream/200_inprogress/claude/20260314_034028_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_implement_secure_sign_up_and_sole_trader_onboarding_flow.md.result.md
?? workstream/200_inprogress/claude/20260314_034030_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_build_idempotent_transaction_import_and_90_day_backfill.md.result.md
?? workstream/200_inprogress/claude/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline_20260322_191355.md.result.md
?? workstream/200_inprogress/claude/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline_20260322_191455.md.result.md
?? workstream/200_inprogress/claude/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline_20260322_191656.md.result.md
?? workstream/200_inprogress/claude/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline_20260322_191755.md.result.md
?? workstream/200_inprogress/claude/20260314_034047_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamF_harden_security_performance_and_legal_disclaimers_for_mvp_release.md.result.md
?? workstream/200_inprogress/claude/20260314_210850_breakout_fs_add_product_to_product_type_allocation_workflow.md.result.md
?? workstream/200_inprogress/claude/20260316_161933_skills_make_task_dependency_mandatory_20260321_112843.md.result.md
?? workstream/200_inprogress/claude/20260316_161933_skills_make_task_dependency_mandatory_20260321_112930.md.result.md
?? workstream/200_inprogress/claude/20260316_161933_skills_make_task_dependency_mandatory_20260321_113001.md.result.md
?? workstream/200_inprogress/claude/20260318_172850_claude_BLOCKER_20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md.result.md
?? workstream/200_inprogress/claude/20260318_172933_claude_BLOCKER_20260314_034042_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_mobile_inbox_exception_queue_screen.md.result.md
?? workstream/200_inprogress/claude/20260318_172947_claude_BLOCKER_20260314_034043_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_quarter_readiness_and_finish_now_screen.md.result.md
?? workstream/200_inprogress/claude/20260318_173006_claude_BLOCKER_20260314_034044_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_evidence_capture_and_match_confirmation_ui_flow.md.result.md
?? workstream/200_inprogress/claude/20260318_173023_claude_BLOCKER_20260314_034045_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_implement_voice_intents_confirmation_chip_and_undo_flow.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_a6_implement_content_variation_and_a_b_testing_service.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_c10_add_frontend_responsive_polish_and_cross_route_smoke_coverage.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_c9_build_subscriber_growth_dashboard_ui.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_codex_strategy_warehouse_marketing_engine_b8_create_engagement_metrics_collector.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_gemini_strategy_warehouse_marketing_engine_d2_create_performance_feedback_loop_service.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_gemini_strategy_warehouse_marketing_engine_d6_build_weekly_report_review_ui.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_general_strategy_warehouse_marketing_engine_c5_implement_subscription_form_ui_and_success_states.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_general_strategy_warehouse_marketing_engine_d1_build_autonomous_scheduler_service.md.result.md
?? workstream/200_inprogress/claude/20260320_233148_general_strategy_warehouse_marketing_engine_d4_build_admin_control_panel_ui.md.result.md
?? workstream/200_inprogress/claude/20260321_100139_task_b2.md.result.md
?? workstream/200_inprogress/claude/20260321_120828_test_write.md.result.md
?? workstream/200_inprogress/claude/20260321_120924_test_with_outfile.md.result.md
?? workstream/200_inprogress/claude/20260323_004916_breakout_config_ui_full_field_coverage.md.result.md
?? workstream/200_inprogress/claude/20260324_233200_breakout_golden_pick_now_filter.md.result.md
?? workstream/200_inprogress/claude/20260325_001200_breakout_array_strategy_exclusions.md.result.md
?? workstream/200_inprogress/claude/20260325_172300_breakout_weekly_strategy_performance_screen.md.result.md
?? workstream/200_inprogress/claude/20260325_172300_breakout_weekly_strategy_performance_screen_20260325_193622.md.result.md
?? workstream/200_inprogress/claude/20260325_233035_breakout_add_crypto_to_weekly_dashboard.md.result.md
?? workstream/200_inprogress/claude/20260329_025428_ep_website_rebuilds_redesign_legacy_hairdresser_landing_pages.md.result.md
?? workstream/200_inprogress/claude/20260329_173911_general_general_revisit__20260329_025428_ep_website_rebuilds_redesign_legacy_hairdresser_landing_pages_md.md.result.md
?? workstream/200_inprogress/claude/20260330_004826_breakout_daily_system_full_solution_build.md.result.md
?? workstream/200_inprogress/claude/20260331_113035_marketing_build_product_showcase_website.md.result.md
?? workstream/200_inprogress/codex/20260314_034044_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_evidence_capture_and_match_confirmation_ui_flow.md.result.md
?? workstream/200_inprogress/codex/20260314_034045_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_implement_voice_intents_confirmation_chip_and_undo_flow.md.result.md
?? workstream/200_inprogress/codex/20260318_172637_claude_BLOCKER_20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md.result.md
?? workstream/200_inprogress/codex/20260318_172850_claude_BLOCKER_20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md.result.md
?? workstream/200_inprogress/codex/20260328_163446_breakout_weekly_performance_full_week_navigation_layout.md.result.md
?? workstream/200_inprogress/codex/20260328_184931_market_prices_api_fastapi_starlette_startup_compatibility.md.result.md
?? workstream/200_inprogress/codex/20260328_201416_ep_website_rebuilds_se_london_legacy_hairdressers.md.result.md
?? workstream/200_inprogress/codex/20260329_025428_ep_website_rebuilds_redesign_legacy_hairdresser_landing_pages.md.result.md
?? workstream/200_inprogress/codex/20260330_004209_breakout_daily_system_commercial_reposition.md.result.md
?? workstream/200_inprogress/codex/20260330_011103_breakout_gen_strategy_name_trade_json_and_backfill.md.result.md
?? workstream/200_inprogress/codex/20260330_101001_breakout_strategy_performance_today_date_selector_fix.md.result.md
?? workstream/200_inprogress/codex/20260330_132827_workstream_task_type_schema_update.md.result.md
?? "workstream/200_inprogress/codex/20260330_164250_20260330_164250_TradePanel \342\200\224 Dev Task.md.result.md"
?? workstream/200_inprogress/codex/20260401_155057_claude_breakout_weekly_performance_make_all_columns_sortable.md.result.md
?? workstream/200_inprogress/codex/20260401_155058_breakout_weekly_performance_restore_product_strategy_column_and_add_gen_strategy_name.md.result.md
?? workstream/200_inprogress/codex/20260402_010000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/200_inprogress/gemini/20260314_034027_task_b1.md.result.md
?? workstream/200_inprogress/gemini/20260314_034031_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_transaction_classification_model_with_full_audit_trail_20260321_092037.md.result.md
?? workstream/200_inprogress/gemini/20260314_034032_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_build_inbox_micro_decision_actions_and_suggestion_application_20260321_095123.md.result.md
?? workstream/200_inprogress/gemini/20260314_034032_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_build_inbox_micro_decision_actions_and_suggestion_application_20260321_100112.md.result.md
?? workstream/200_inprogress/gemini/20260314_034033_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_blocker_evaluation_and_transaction_resolution_rules.md.result.md
?? workstream/200_inprogress/gemini/20260314_034034_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_simple_merchant_rules_for_recurring_categorisation_defaults.md.result.md
?? workstream/200_inprogress/gemini/20260314_034036_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_transactions_csv_and_evidenceindex_csv_exports.md.result.md
?? workstream/200_inprogress/gemini/20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md.result.md
?? workstream/200_inprogress/gemini/20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf_20260322_185855.md.result.md
?? workstream/200_inprogress/gemini/20260314_034038_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_assemble_final_quarterly_pack_and_export_delivery_flow.md.result.md
?? workstream/200_inprogress/gemini/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline.md.result.md
?? workstream/200_inprogress/gemini/20260314_034040_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_build_confirm_first_evidence_matching_candidate_service.md.result.md
?? workstream/200_inprogress/gemini/20260314_034041_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_persist_evidence_links_and_unmatched_states_with_user_confirmation.md.result.md
?? workstream/200_inprogress/gemini/20260314_214342_20260314_epic_review_extended_decomposition_and_delete.md.result.md
?? workstream/200_inprogress/gemini/20260314_224854_establish_connection_status_and_reconnect_lifecycl_3.md.result.md
?? workstream/200_inprogress/gemini/20260314_224854_implement_connection_callback_handling_and_bank_ac_1.md.result.md
?? workstream/200_inprogress/gemini/20260314_234338_breakout_fs_map_products_to_product_type.md.result.md
?? workstream/200_inprogress/gemini/20260318_172752_claude_BLOCKER_20260316_211200_workstream_document_agent_controller_timestamp_entry.md.result.md
?? workstream/200_inprogress/gemini/20260320_233148_claude_strategy_warehouse_marketing_engine_c2_build_landing_page_layout_and_brand_presentation.md.result.md
?? workstream/200_inprogress/gemini/20260320_233148_gemini_strategy_warehouse_marketing_engine_d4_build_admin_control_panel_ui.md.result.md
?? workstream/200_inprogress/gemini/20260328_201416_ep_website_rebuilds_se_london_legacy_hairdressers.md.result.md
?? workstream/200_inprogress/gemini/20260329_025428_ep_website_rebuilds_redesign_legacy_hairdresser_landing_pages.md.result.md
?? workstream/200_inprogress/gemini/20260329_230222_breakout_subscriber_business_plan.md.result.md
?? workstream/200_inprogress/gemini/20260330_005618_breakout_delivery_bat_wrappers.md.result.md
?? workstream/200_inprogress/gemini/20260330_154024_breakout_weekly_perf_last_update_age.md.result.md
?? workstream/200_inprogress/gemini/20260401_010000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260401_022404_workstream_add_task_completion_status_bars.md.result.md
?? workstream/200_inprogress/gemini/20260401_030508_funcuts_full_site_rebuild_loop.md.result.md
?? workstream/200_inprogress/gemini/20260401_041332_funcuts_add_light_dark_theme_switch.md.result.md
?? workstream/200_inprogress/gemini/20260401_042158_platform_accounts_create_and_credentials_loop.md.result.md
?? workstream/200_inprogress/gemini/20260401_050000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260401_090000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260401_170000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260401_210000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260401_210000_general_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260401_234500_breakout_recurring_social_posting_package_generation.md.result.md
?? workstream/200_inprogress/gemini/20260402_010000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_010000_general_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_015000_tools_scrape_uk_hairdressers_barbers_emails_expansion.md.result.md
?? workstream/200_inprogress/gemini/20260402_050000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_050000_general_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_090000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_090000_general_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_130000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_130000_general_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_170000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/200_inprogress/gemini/20260402_210000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/20260314_034027_task_c1_processed.md
?? workstream/300_complete/20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md
?? workstream/300_complete/20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md
?? workstream/300_complete/20260314_034040_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_build_confirm_first_evidence_matching_candidate_service.md
?? workstream/300_complete/20260314_034041_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_persist_evidence_links_and_unmatched_states_with_user_confirmation.md
?? workstream/300_complete/20260316_135212_trading_strategy_warehouse_marketing_engine_processed.md
?? workstream/300_complete/20260316_161933_skills_make_task_dependency_mandatory.md
?? workstream/300_complete/20260318_172656_claude_BLOCKER_20260314_034035_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_build_quarter_model_readiness_metrics_and_blocking_queue_ordering.md
?? workstream/300_complete/20260320_124500_breakout_tb_leadership_tracking.md
?? workstream/300_complete/20260320_125000_breakout_rename_leadership_json.md
?? workstream/300_complete/20260320_161049_breakout_trade_bucket_readthrough.md
?? workstream/300_complete/20260320_162513_breakout_validate_ltrade_window_matching.md
?? workstream/300_complete/20260320_210114_workstream_kanban_dashboard_workflow_diagram.md
?? workstream/300_complete/20260320_221637_workstream_fix_epic_focus_dropdown_lifecycle_epics.md
?? workstream/300_complete/20260320_223352_strategy_warehouse_marketing_compare_deliverable_to_epic.md
?? workstream/300_complete/20260320_224747_strategy_warehouse_marketing_merge_epics_into_single_replacement.md
?? workstream/300_complete/20260320_231647_strategy_warehouse_marketing_run_full_lifecycle_from_consolidated_epic.md
?? workstream/300_complete/20260320_233148_claude_strategy_warehouse_marketing_engine_a1_map_strategy_warehouse_source_feeds_to_marketing_inputs.md
?? workstream/300_complete/20260320_233148_claude_strategy_warehouse_marketing_engine_c4_build_subscription_capture_api_and_persistence_contract.md
?? workstream/300_complete/20260320_233148_claude_strategy_warehouse_marketing_engine_c6_implement_double_opt_in_and_subscriber_lifecycle_backend.md
?? workstream/300_complete/20260320_233148_claude_strategy_warehouse_marketing_engine_c7_implement_conversion_tracking_pipeline.md
?? workstream/300_complete/20260320_234947_strategy_warehouse_confirm_backlog_general_state.md
?? workstream/300_complete/20260321_004911_workstream_fix_controller_path_and_result_file_handling.md
?? workstream/300_complete/20260321_120841_test_write_complete.md
?? workstream/300_complete/20260321_210937_workstream_move_strategy_warehouse_gemini_backlog_tasks_to_general.md
?? workstream/300_complete/20260321_213103_strategy_warehouse_add_tiktok_to_posting_platform_targets.md
?? workstream/300_complete/20260321_214504_workstream_reduce_kanban_task_loading_to_single_slot.md
?? workstream/300_complete/20260321_215310_workstream_move_strategy_warehouse_pinned_backlog_tasks_to_general.md
?? workstream/300_complete/20260321_222047_strategy_warehouse_validate_c2_landing_page_deliverable.md
?? workstream/300_complete/20260321_224405_workstream_add_ui_visual_evidence_gate.md
?? workstream/300_complete/20260322_000500_workstream_review_single_slot_worker_refill_behavior.md
?? workstream/300_complete/20260322_001400_workstream_add_review_lane_user_decision_actions.md
?? workstream/300_complete/20260322_001900_workstream_fix_single_slot_worker_refill_behavior.md
?? workstream/300_complete/20260322_004000_workstream_enforce_max_one_task_per_model_backlog_lane.md
?? workstream/300_complete/20260322_005500_strategy_warehouse_refresh_landing_page_visual_direction.md
?? workstream/300_complete/20260322_155424_workstream_enforce_max_one_inprogress_and_fix_throttle.md
?? workstream/300_complete/20260322_204814_ep_strategy_warehouse_marketing_run_test.md
?? workstream/300_complete/20260323_040702_strategy_warehouse_twitter_tiktok_content_generator_mvp.md
?? workstream/300_complete/20260323_110641_breakout_social_content_generator_exclude_dna.md
?? workstream/300_complete/20260323_121725_breakout_social_content_modest_account_messaging.md
?? workstream/300_complete/20260323_122227_breakout_social_content_remove_product_suffix.md
?? workstream/300_complete/20260323_122930_breakout_social_content_warehouse_coming_soon.md
?? workstream/300_complete/20260323_161500_breakout_notebooklm_video_generation.md
?? workstream/300_complete/20260323_165000_multi_chart_green_dots_logic.md
?? workstream/300_complete/20260323_191500_breakout_add_product_type_cost_config.md
?? workstream/300_complete/20260324_120127_breakout_strategy_persistence_predictor.md
?? workstream/300_complete/20260324_160103_breakout_top10_history_evaluation_screen.md
?? workstream/300_complete/20260324_191410_breakout_strategy_predictor_configurable_thresholds.md
?? workstream/300_complete/20260324_193936_breakout_config_ui_pick_now_thresholds.md
?? workstream/300_complete/20260324_205051_breakout_backfill_top10_history.md
?? workstream/300_complete/20260324_220656_breakout_pick_now_effectiveness_analysis.md
?? workstream/300_complete/20260324_233200_breakout_golden_pick_now_filter.md
?? workstream/300_complete/20260325_130000_breakout_add_chart_button.md
?? workstream/300_complete/20260325_233721_breakout_verify_product_type_cost_application.md
?? workstream/300_complete/20260325_235941_breakout_update_btc_pip_multiplier.md
?? workstream/300_complete/20260326_000842_breakout_revert_pip_value_changes.md
?? workstream/300_complete/20260326_002651_breakout_fix_product_specific_pnl_from_min_move_value.md
?? workstream/300_complete/20260326_095056_breakout_investigate_missing_forex_live_trades.md
?? workstream/300_complete/20260326_105223_breakout_trace_missing_forex_quotes.md
?? workstream/300_complete/20260326_114837_breakout_verify_gc_bz_product_type_config.md
?? workstream/300_complete/20260326_125609_breakout_twitter_weekly_forex_top5_post.md
?? workstream/300_complete/20260326_125820_breakout_social_posting_package_top5_multi_product_types.md
?? workstream/300_complete/20260326_131307_breakout_document_social_posting_workflow_and_create_skill.md
?? workstream/300_complete/20260326_133336_breakout_notebooklm_weekly_returns_audio_video_workflow_and_skills.md
?? workstream/300_complete/20260326_141130_notebooklm_update_skill_paths_and_weekly_returns_refs.md
?? workstream/300_complete/20260326_142018_notebooklm_reinstall_cli_python313.md
?? workstream/300_complete/20260326_143855_breakout_generate_notebooklm_weekly_returns_audio_video.md
?? workstream/300_complete/20260326_174209_breakout_twitter_post_preparation_top5_multi_product_types.md
?? workstream/300_complete/20260326_192248_breakout_post_twitter_thread_multi_product_types.md
?? workstream/300_complete/20260326_222658_breakout_verify_indices_metals_net_returns_cld.md
?? workstream/300_complete/20260326_224010_breakout_verify_individual_indices_metals_trade_net_return_formula.md
?? workstream/300_complete/20260326_230800_market_prices_spy_options_fetcher.md
?? workstream/300_complete/20260326_231159_breakout_verify_energy_trade_net_return_formula.md
?? workstream/300_complete/20260326_234006_breakout_verify_no_overlapping_metals_trades_selected_strategy_product.md
?? workstream/300_complete/20260327_000552_breakout_explain_system_health_price_feed_offline.md
?? workstream/300_complete/20260327_002500_market_prices_multi_product_options.md
?? workstream/300_complete/20260327_004615_breakout_update_system_health_live_feed_check_multiple_fx_endpoints.md
?? workstream/300_complete/20260327_013221_breakout_fix_constants_py_null_bytes_syntaxerror.md
?? workstream/300_complete/20260327_124839_market_prices_api_fix_fastapi_starlette_startup_compat.md
?? workstream/300_complete/20260327_130000_breakout_rty_net_return_validation.md
?? workstream/300_complete/20260327_133000_breakout_rty_historic_trades_fix.md
?? workstream/300_complete/20260327_135000_breakout_indices_summary_regeneration.md
?? workstream/300_complete/20260327_171743_stitch_mcp_setup_and_funcuts_requirement_package.md
?? workstream/300_complete/20260329_170000_breakout_daily_twitter_social_posting.md
?? workstream/300_complete/20260330_173722_ep_breakout_daily_system_commercial_reposition_trade_panel_landing_page.md
?? workstream/300_complete/20260330_201900_ep_breakout_daily_system_commercial_reposition_trade_panel_landing_page_revision.md
?? workstream/300_complete/20260331_000156_ep_breakout_daily_system_commercial_reposition_archive_trading_marketing_page.md
?? workstream/300_complete/20260331_000841_ep_breakout_daily_system_commercial_reposition_archive_trading_refinement.md
?? workstream/300_complete/20260331_001432_ep_breakout_daily_system_commercial_reposition_alignment_fix.md
?? workstream/300_complete/20260331_001506_ep_breakout_daily_system_commercial_reposition_real_product_data.md
?? workstream/300_complete/20260331_002149_ep_breakout_daily_system_commercial_reposition_landing_page_skill.md
?? workstream/300_complete/20260331_004736_breakout_trace_fs_json_live_date_folder_creation.md
?? workstream/300_complete/20260331_030540_skills_create_task_orchestrator_skill.md
?? workstream/300_complete/20260331_032444_skills_update_task_orchestrator_for_task_type_interpretation.md
?? workstream/300_complete/20260331_032737_review_task_type_implementation_gaps.md
?? workstream/300_complete/20260331_033358_workstream_make_task_type_mandatory.md
?? workstream/300_complete/20260331_040109_task_orchestrator_single_owner_lock.md
?? workstream/300_complete/20260331_135140_repo_twice_daily_x_drafting_reference_scan.md
?? workstream/300_complete/20260331_151500_marketing_rebuild_showcase_with_web_design_guidelines.md
?? workstream/300_complete/20260331_152755_breakout_social_posting_canonical_product_return_calc.md
?? workstream/300_complete/20260331_155500_workstream_capture_skill_integration_and_showcase_rebuild.md
?? workstream/300_complete/20260331_160500_ep_website_rebuilds_hairdresser_sales_redesign_with_web_guidelines.md
?? workstream/300_complete/20260331_162500_breakout_twitter_browser_post.md
?? workstream/300_complete/20260331_235814_workstream_create_gemini_recurring_twitter_summary_returns_task.md
?? workstream/300_complete/20260401_022404_workstream_add_task_completion_status_bars.md
?? workstream/300_complete/20260401_114530_workstream_fix_recurring_task_reschedule_after_blocked_run.md
?? workstream/300_complete/20260401_120431_workstream_fix_kanban_dashboard_client_disconnect_traceback.md
?? workstream/300_complete/20260401_120620_workstream_fix_recurring_task_expected_slot_anchor.md
?? workstream/300_complete/20260401_143807_workstream_mark_successful_twitter_post_task_workflow_ready.md
?? workstream/300_complete/20260401_144949_workstream_mark_social_posting_frontend_alignment_workflow_ready.md
?? workstream/300_complete/20260401_164115_workstream_fix_date_bucket_limit_to_per_model_lane.md
?? workstream/300_complete/20260402_014756_workstream_fix_recurring_twitter_task_next_copy_and_skill_usage.md
?? workstream/300_complete/20260402_020854_breakout_fix_constants_py_null_bytes_encoding.md
?? workstream/300_complete/20260402_090000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/20260402_094804_breakout_fix_constants_py_escaped_quotes_regression.md
?? workstream/300_complete/20260402_145346_workstream_fix_double_spawn_of_recurring_twitter_slots.md
?? workstream/300_complete/20260402_150114_breakout_rerun_twitter_summary_slot_20260402_130000.md
?? workstream/300_complete/20260402_150737_breakout_fix_false_positive_twitter_post_success_detection.md
?? workstream/300_complete/20260402_151640_breakout_harden_twitter_posting_workflow_with_strict_step_gates.md
?? workstream/300_complete/20260402_153439_breakout_retest_hardened_twitter_workflow.md
?? workstream/300_complete/20260402_153818_breakout_reduce_twitter_automation_detection_on_submit.md
?? workstream/300_complete/20260402_155549_breakout_add_x_api_posting_route.md
?? workstream/300_complete/20260402_160105_breakout_test_x_api_post_route_with_summary_returns_payload.md
?? workstream/300_complete/20260402_163225_breakout_wire_x_api_credentials_via_workstream_env.md
?? workstream/300_complete/20260402_163700_workstream_add_gitignore_for_workstream_env.md
?? workstream/300_complete/20260402_163950_breakout_install_tweepy_and_retest_x_api_post.md
?? workstream/300_complete/20260402_164430_breakout_rerun_x_api_post_permission_test.md
?? workstream/300_complete/20260402_175437_breakout_refresh_workstream_x_env_credentials.md
?? workstream/300_complete/20260402_184957_breakout_rerun_x_api_post_after_env_refresh.md
?? workstream/300_complete/20260402_233618_workstream_replace_recurring_twitter_summary_with_combined_x_api_workflow.md
?? workstream/300_complete/20260402_234409_breakout_immediate_test_combined_recurring_x_api_workflow.md
?? workstream/300_complete/20260403_001605_breakout_remove_fabricated_social_post_timestamp_and_force_temp_tweet_refresh.md
?? workstream/300_complete/20260403_002651_breakout_use_iso_dates_in_social_post_labels.md
?? workstream/300_complete/20260403_003225_breakout_retry_x_api_post_with_corrected_dated_payload.md
?? workstream/300_complete/claude/20260314_034028_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_implement_secure_sign_up_and_sole_trader_onboarding_flow.md
?? workstream/300_complete/claude/20260314_034030_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_build_idempotent_transaction_import_and_90_day_backfill.md
?? workstream/300_complete/claude/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline_20260322_191355.md
?? workstream/300_complete/claude/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline_20260322_191455.md
?? workstream/300_complete/claude/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline_20260322_191656.md
?? workstream/300_complete/claude/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline_20260322_191755.md
?? workstream/300_complete/claude/20260314_034047_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamF_harden_security_performance_and_legal_disclaimers_for_mvp_release.md
?? workstream/300_complete/claude/20260314_210850_breakout_fs_add_product_to_product_type_allocation_workflow.md
?? workstream/300_complete/claude/20260316_161933_skills_make_task_dependency_mandatory_20260321_112843.md
?? workstream/300_complete/claude/20260316_161933_skills_make_task_dependency_mandatory_20260321_112930.md
?? workstream/300_complete/claude/20260316_161933_skills_make_task_dependency_mandatory_20260321_113001.md
?? workstream/300_complete/claude/20260318_172933_claude_BLOCKER_20260314_034042_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_mobile_inbox_exception_queue_screen.md
?? workstream/300_complete/claude/20260318_172947_claude_BLOCKER_20260314_034043_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_quarter_readiness_and_finish_now_screen.md
?? workstream/300_complete/claude/20260318_173006_claude_BLOCKER_20260314_034044_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_evidence_capture_and_match_confirmation_ui_flow.md
?? workstream/300_complete/claude/20260318_173023_claude_BLOCKER_20260314_034045_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_implement_voice_intents_confirmation_chip_and_undo_flow.md
?? workstream/300_complete/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_a6_implement_content_variation_and_a_b_testing_service.md
?? workstream/300_complete/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_c10_add_frontend_responsive_polish_and_cross_route_smoke_coverage.md
?? workstream/300_complete/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_c9_build_subscriber_growth_dashboard_ui.md
?? workstream/300_complete/claude/20260320_233148_codex_strategy_warehouse_marketing_engine_b8_create_engagement_metrics_collector.md
?? workstream/300_complete/claude/20260320_233148_gemini_strategy_warehouse_marketing_engine_d2_create_performance_feedback_loop_service.md
?? workstream/300_complete/claude/20260320_233148_gemini_strategy_warehouse_marketing_engine_d6_build_weekly_report_review_ui.md
?? workstream/300_complete/claude/20260320_233148_general_strategy_warehouse_marketing_engine_c5_implement_subscription_form_ui_and_success_states.md
?? workstream/300_complete/claude/20260320_233148_general_strategy_warehouse_marketing_engine_d1_build_autonomous_scheduler_service.md
?? workstream/300_complete/claude/20260321_100139_task_b2.md
?? workstream/300_complete/claude/20260321_120828_test_write.md
?? workstream/300_complete/claude/20260321_120924_test_with_outfile.md
?? workstream/300_complete/claude/20260323_004916_breakout_config_ui_full_field_coverage.md
?? workstream/300_complete/claude/20260324_233200_breakout_golden_pick_now_filter.md
?? workstream/300_complete/claude/20260325_001200_breakout_array_strategy_exclusions.md
?? workstream/300_complete/claude/20260325_172300_breakout_weekly_strategy_performance_screen.md
?? workstream/300_complete/claude/20260325_172300_breakout_weekly_strategy_performance_screen_20260325_193622.md
?? workstream/300_complete/claude/20260325_233035_breakout_add_crypto_to_weekly_dashboard.md
?? workstream/300_complete/claude/20260329_173911_general_general_revisit__20260329_025428_ep_website_rebuilds_redesign_legacy_hairdresser_landing_pages_md.md
?? workstream/300_complete/claude/20260330_004826_breakout_daily_system_full_solution_build.md
?? workstream/300_complete/claude/20260331_113035_marketing_build_product_showcase_website.md
?? workstream/300_complete/codex/20260314_034044_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_deliver_evidence_capture_and_match_confirmation_ui_flow.md
?? workstream/300_complete/codex/20260314_034045_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_implement_voice_intents_confirmation_chip_and_undo_flow.md
?? workstream/300_complete/codex/20260318_172637_claude_BLOCKER_20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md
?? workstream/300_complete/codex/20260318_172850_claude_BLOCKER_20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md
?? workstream/300_complete/codex/20260318_172904_claude_BLOCKER_20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline.md
?? workstream/300_complete/codex/20260318_172918_claude_BLOCKER_20260314_034041_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_persist_evidence_links_and_unmatched_states_with_user_confirmation.md
?? workstream/300_complete/codex/20260320_233148_claude_strategy_warehouse_marketing_engine_a5_implement_content_queue_and_scheduling_engine.md
?? workstream/300_complete/codex/20260320_233148_claude_strategy_warehouse_marketing_engine_c3_integrate_social_proof_and_performance_modules_on_landing_page.md
?? workstream/300_complete/codex/20260320_233148_gemini_strategy_warehouse_marketing_engine_d3_implement_manual_override_and_kill_switch_backend.md
?? workstream/300_complete/codex/20260320_233148_gemini_strategy_warehouse_marketing_engine_d7_implement_health_monitoring_and_alerting_service.md
?? workstream/300_complete/codex/20260320_233148_gemini_strategy_warehouse_marketing_engine_z5_automate_database_initialization_and_seed_data.md
?? workstream/300_complete/codex/20260328_163446_breakout_weekly_performance_full_week_navigation_layout.md
?? workstream/300_complete/codex/20260328_184931_market_prices_api_fastapi_starlette_startup_compatibility.md
?? workstream/300_complete/codex/20260328_201416_ep_website_rebuilds_se_london_legacy_hairdressers.md
?? workstream/300_complete/codex/20260329_025428_ep_website_rebuilds_redesign_legacy_hairdresser_landing_pages.md
?? workstream/300_complete/codex/20260330_004209_breakout_daily_system_commercial_reposition.md
?? workstream/300_complete/codex/20260330_011103_breakout_gen_strategy_name_trade_json_and_backfill.md
?? workstream/300_complete/codex/20260330_101001_breakout_strategy_performance_today_date_selector_fix.md
?? workstream/300_complete/codex/20260330_132827_workstream_task_type_schema_update.md
?? "workstream/300_complete/codex/20260330_164250_20260330_164250_TradePanel \342\200\224 Dev Task.md"
?? workstream/300_complete/codex/20260401_155057_claude_breakout_weekly_performance_make_all_columns_sortable.md
?? workstream/300_complete/codex/20260401_155058_breakout_weekly_performance_restore_product_strategy_column_and_add_gen_strategy_name.md
?? workstream/300_complete/gemini/20260305_192700_bizpa_mvp_pivot_phase06_voice_micro_decisions.md
?? workstream/300_complete/gemini/20260313_220646_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_build_shock_simulation_and_scenario_validation_harness.md
?? workstream/300_complete/gemini/20260313_221233_workstream_move_decomposed_epic_root_tasks_to_general_backlog.md
?? workstream/300_complete/gemini/20260313_221233_workstream_move_decomposed_epic_root_tasks_to_general_backlog.md.result.md
?? workstream/300_complete/gemini/20260313_221233_workstream_move_decomposed_epic_root_tasks_to_general_backlog.md.result.md.result.md
?? workstream/300_complete/gemini/20260314_034027_task_b1.md
?? workstream/300_complete/gemini/20260314_034031_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_transaction_classification_model_with_full_audit_trail.md
?? workstream/300_complete/gemini/20260314_034031_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_transaction_classification_model_with_full_audit_trail_20260321_092037.md
?? workstream/300_complete/gemini/20260314_034032_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_build_inbox_micro_decision_actions_and_suggestion_application.md
?? workstream/300_complete/gemini/20260314_034032_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_build_inbox_micro_decision_actions_and_suggestion_application_20260321_095123.md
?? workstream/300_complete/gemini/20260314_034032_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_build_inbox_micro_decision_actions_and_suggestion_application_20260321_100112.md
?? workstream/300_complete/gemini/20260314_034033_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_blocker_evaluation_and_transaction_resolution_rules.md
?? workstream/300_complete/gemini/20260314_034034_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamB_implement_simple_merchant_rules_for_recurring_categorisation_defaults.md
?? workstream/300_complete/gemini/20260314_034036_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_transactions_csv_and_evidenceindex_csv_exports.md
?? workstream/300_complete/gemini/20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf.md
?? workstream/300_complete/gemini/20260314_034037_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_generate_quarterlysummary_csv_and_quarterlypack_pdf_20260322_185855.md
?? workstream/300_complete/gemini/20260314_034038_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamC_assemble_final_quarterly_pack_and_export_delivery_flow.md
?? workstream/300_complete/gemini/20260314_034039_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_implement_evidence_capture_storage_and_metadata_extraction_pipeline.md
?? workstream/300_complete/gemini/20260314_034040_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamD_build_confirm_first_evidence_matching_candidate_service.md
?? workstream/300_complete/gemini/20260314_214342_20260314_epic_review_extended_decomposition_and_delete.md
?? workstream/300_complete/gemini/20260314_224854_establish_connection_status_and_reconnect_lifecycl_3.md
?? workstream/300_complete/gemini/20260314_224854_implement_connection_callback_handling_and_bank_ac_1.md
?? workstream/300_complete/gemini/20260314_234338_breakout_fs_map_products_to_product_type.md
?? workstream/300_complete/gemini/20260316_161933_skills_make_task_dependency_mandatory.md
?? workstream/300_complete/gemini/20260317_101000_breakout_silence_workflow_prompts.md
?? workstream/300_complete/gemini/20260318_172637_claude_BLOCKER_20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md
?? workstream/300_complete/gemini/20260318_172752_claude_BLOCKER_20260316_211200_workstream_document_agent_controller_timestamp_entry.md
?? workstream/300_complete/gemini/20260319_222632_breakout_profile_topx_delta_type_tb.md
?? workstream/300_complete/gemini/20260320_224500_workstream_move_decomposed_epic_root_tasks_to_general_backlog.result.md
?? workstream/300_complete/gemini/20260320_231500_workstream_move_decomposed_epic_root_tasks_to_general_backlog.transcript.md
?? workstream/300_complete/gemini/20260320_232000_workstream_move_decomposed_epic_root_tasks_to_general_backlog.result.md
?? workstream/300_complete/gemini/20260320_233148_claude_strategy_warehouse_marketing_engine_a5_implement_content_queue_and_scheduling_engine.md
?? workstream/300_complete/gemini/20260320_233148_claude_strategy_warehouse_marketing_engine_c1_scaffold_landing_page_frontend_application.md
?? workstream/300_complete/gemini/20260320_233148_claude_strategy_warehouse_marketing_engine_c2_build_landing_page_layout_and_brand_presentation.md
?? workstream/300_complete/gemini/20260320_233148_claude_strategy_warehouse_marketing_engine_c5_implement_subscription_form_ui_and_success_states.md
?? workstream/300_complete/gemini/20260320_233148_gemini_strategy_warehouse_marketing_engine_d4_build_admin_control_panel_ui.md
?? workstream/300_complete/gemini/20260321_110000_breakout_add_product_type_to_workflows.md
?? workstream/300_complete/gemini/20260325_234723_breakout_add_energy_to_weekly_dashboard.md
?? workstream/300_complete/gemini/20260329_025428_ep_website_rebuilds_redesign_legacy_hairdresser_landing_pages.md
?? workstream/300_complete/gemini/20260329_230222_breakout_subscriber_business_plan.md
?? workstream/300_complete/gemini/20260330_005618_breakout_delivery_bat_wrappers.md
?? workstream/300_complete/gemini/20260330_154024_breakout_weekly_perf_last_update_age.md
?? workstream/300_complete/gemini/20260401_030508_funcuts_full_site_rebuild_loop.md
?? workstream/300_complete/gemini/20260401_041332_funcuts_add_light_dark_theme_switch.md
?? workstream/300_complete/gemini/20260401_042158_platform_accounts_create_and_credentials_loop.md
?? workstream/300_complete/gemini/20260401_050000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260401_130000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260401_130000_breakout_twitter_summary_returns_every_4_hours.md.result.md
?? workstream/300_complete/gemini/20260401_170000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260401_210000_general_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260401_234500_breakout_recurring_social_posting_package_generation.md
?? workstream/300_complete/gemini/20260402_010000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260402_010000_general_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260402_015000_tools_scrape_uk_hairdressers_barbers_emails_expansion.md
?? workstream/300_complete/gemini/20260402_050000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260402_050000_general_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260402_090000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260402_090000_general_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260402_130000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260402_130000_general_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/gemini/20260402_170000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/300_complete/general/20260326_113738_breakout_add_quote_freshness_guard.md
?? workstream/300_complete/general/20260326_122251_breakout_add_min_move_config_ui.md
?? workstream/300_complete/general/20260330_011551_breakout_landing_page_redesign.md
?? workstream/300_complete/general/20260330_011953_breakout_landing_page_rework.md
?? workstream/300_complete/general/20260331_122508_workstream_kanban_today_date_selector_fix.md
?? workstream/300_complete/general/20260331_142632_breakout_twitter_posting_format_update.md
?? workstream/300_complete/general/20260331_194347_market_prices_api_fix_local_time_output.md
?? workstream/300_complete/general/20260331_213249_workstream_add_kanban_scheduled_for_execution.md
?? workstream/300_complete/general/20260331_232812_workstream_add_kanban_recurring_task_rescheduling.md
?? workstream/300_complete/general/20260401_001105_workstream_fix_scheduled_task_orphan_resume_bypass.md
?? workstream/400_failed/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_a4_create_media_asset_and_visual_snippet_generator.md
?? workstream/400_failed/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_a5_implement_content_queue_and_scheduling_engine.md
?? workstream/400_failed/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_c4_build_subscription_capture_api_and_persistence_contract.md
?? workstream/400_failed/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_c6_implement_double_opt_in_and_subscriber_lifecycle_backend.md
?? workstream/400_failed/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_c7_implement_conversion_tracking_pipeline.md
?? workstream/400_failed/claude/20260320_233148_claude_strategy_warehouse_marketing_engine_c8_build_subscriber_growth_dashboard_backend_apis.md
?? workstream/400_failed/claude/20260320_233148_codex_strategy_warehouse_marketing_engine_b3_implement_telegram_connector.md
?? workstream/400_failed/claude/20260320_233148_codex_strategy_warehouse_marketing_engine_b9_create_follower_and_reach_metrics_collector.md
?? workstream/400_failed/claude/20260320_233148_gemini_strategy_warehouse_marketing_engine_d3_implement_manual_override_and_kill_switch_backend.md
?? workstream/400_failed/claude/20260320_233148_gemini_strategy_warehouse_marketing_engine_d5_create_weekly_metrics_report_generator.md
?? workstream/400_failed/claude/20260320_233148_gemini_strategy_warehouse_marketing_engine_d7_implement_health_monitoring_and_alerting_service.md
?? workstream/400_failed/claude/20260320_233148_gemini_strategy_warehouse_marketing_engine_z6_implement_service_health_endpoint_and_smoke_test.md
?? workstream/400_failed/codex/20260318_173040_claude_BLOCKER_20260314_034047_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamF_harden_security_performance_and_legal_disclaimers_for_mvp_release.md
?? workstream/400_failed/codex/20260320_233148_gemini_strategy_warehouse_marketing_engine_z5_automate_database_initialization_and_seed_data.md
?? workstream/500_dump/20260401_131445_workstream_prevent_recurring_same_slot_blocker_retry.md
?? workstream/500_dump/20260401_132500_workstream_deploy_product_showcase_rebuild_to_vercel.md
?? workstream/500_dump/codex/20260402_010000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/500_dump/dedupe_recurring_20260402_170000/
?? workstream/500_dump/gemini/20260401_010000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/500_dump/gemini/20260401_090000_breakout_twitter_summary_returns_every_4_hours.md
?? workstream/500_dump/orphaned_results/
?? workstream/500_dump/strategy_warehouse_marketing_reset_20260320_231647/
?? workstream/access_key.txt
?? workstream/artefacts/backlog_lane_limit_validation/
?? workstream/artefacts/backlog_lane_limit_validation_revert/
?? workstream/artefacts/epic_decomp_20260320_232433_925540/
?? workstream/artefacts/epic_decomp_20260320_232511_982872/
?? workstream/artefacts/epic_decomp_20260320_232723_696675/
?? workstream/artefacts/single_slot_fix_validation/
?? workstream_backup_20260313/
?? zone_counts_dashboard/
warning: could not open directory 'workstream/artefacts/epic_decomp_4rbio_0v/': Permission denied
warning: could not open directory 'workstream/artefacts/epic_decomp_yxt48izg/': Permission denied

 succeeded in 4022ms:
{
  "status": "ok",
  "ts": "2026-04-03T00:02:26.293168"
}


 succeeded in 3984ms:
{
  "api_enabled": true,
  "can_post": true,
  "last_post_time": "2026-04-03T00:32:48.569242",
  "reason": "OK",
  "recent_posts": [
    {
      "date": "2026-04-03T00:32:48.569207",
      "dry_run": false,
      "success": true,
      "text": "Update at 2026-04-03 00:00\n\n2026-04-02 results\n1. SI 7050\n2. NQ 4035\n3. CL 3635\n4. ES 2675\n5. HG 178...",
      "trigger": "manual_api_dated_payload"
    },
    {
      "date": "2026-04-02T23:44:59.474025",
      "dry_run": false,
      "success": false,
      "text": "Update at 2026-04-02 23:59\r\n\r\nToday\r\n1. SI 6915\r\n2. NQ 3195\r\n3. CL 3045\r\n4. ES 1550\r\n5. RTY 1475\r\n\r\n...",
      "trigger": "recurring_combined_test"
    },
    {
      "date": "2026-04-02T18:51:43.145765",
      "dry_run": false,
      "success": true,
      "text": "Update at 2026-04-02 23:59\r\n\r\nToday\r\n1. SI 6915\r\n2. NQ 3195\r\n3. CL 3045\r\n4. ES 1550\r\n5. RTY 1475\r\n\r\n...",
      "trigger": "manual_api"
    },
    {
      "date": "2026-04-02T17:28:24.862017",
      "dry_run": false,
      "success": false,
      "text": "\ud83d\udfe2 --- +0 BUY | HI | piphunter.io #PH",
      "trigger": "compact_best"
    },
    {
      "date": "2026-04-02T16:59:05.355831",
      "dry_run": false,
      "success": false,
      "text": "Update at 2026-04-02 09:29\n\nToday\n1. SI 6315\n2. NQ 2735\n3. CL 2435\n4. ES 1005\n5. YM 975\n\nWeekly so f...",
      "trigger": "trade_update"
    },
    {
      "date": "2026-04-02T16:52:55.896250",
      "dry_run": false,
      "success": false,
      "text": "Update at 2026-04-02 09:29\n\nToday\n1. SI 6315\n2. NQ 2735\n3. CL 2435\n4. ES 1005\n5. YM 975\n\nWeekly so f...",
      "trigger": "trade_update"
    },
    {
      "date": "2026-04-02T16:35:13.029977",
      "dry_run": false,
      "success": false,
      "text": "Update at 2026-04-02 09:29\n\nToday\n1. SI 6315\n2. NQ 2735\n3. CL 2435\n4. ES 1005\n5. YM 975\n\nWeekly so f...",
      "trigger": "trade_update"
    },
    {
      "date": "2026-04-02T16:34:27.040822",
      "dry_run": false,
      "success": false,
      "text": "Update at 2026-04-02 09:29\n\nToday\n1. SI 6315\n2. NQ 2735\n3. CL 2435\n4. ES 1005\n5. YM 975\n\nWeekly so f...",
      "trigger": "manual_api_test"
    },
    {
      "date": "2026-04-02T16:03:13.653433",
      "dry_run": true,
      "success": true,
      "text": "Update at 2026-04-02 09:29\n\nToday\n1. SI 6315\n2. NQ 2735\n3. CL 2435\n4. ES 1005\n5. YM 975\n\nWeekly so f...",
      "trigger": "manual_api_test"
    }
  ]
}


codex
I’ve verified the API is up and currently allowed to post. I’m patching the workflow now to use the live route, persist the raw route response, and validate that `temp_tweet.txt` matches the generated consolidated payload before posting.
apply patch
patch: completed
C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)

apply patch
patch: completed
C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..f77578c019ddb1c0913b78ddba241a4fa042868d
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,66 @@
+import json
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+            temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": tweet_text}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": "different tweet"}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+
+if __name__ == "__main__":
+    unittest.main()

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..f77578c019ddb1c0913b78ddba241a4fa042868d
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,66 @@
+import json
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+            temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": tweet_text}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": "different tweet"}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+
+if __name__ == "__main__":
+    unittest.main()

codex
The shared skill file is stale relative to this task’s intended workflow, so I’m updating it too. That keeps the scheduler instructions, the skill, and the script aligned instead of leaving two conflicting “canonical” paths in the repo.
apply patch
patch: completed
C:\Users\edebe\eds\skills\twitter-canonical-posting\SKILL.md
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..f77578c019ddb1c0913b78ddba241a4fa042868d
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,66 @@
+import json
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+            temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": tweet_text}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": "different tweet"}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..f77578c019ddb1c0913b78ddba241a4fa042868d
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,66 @@
+import json
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+            temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": tweet_text}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": "different tweet"}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

codex
The code path is patched. I’m running validations in the same order the task expects: compile, unit checks, then the actual dated workflow for `2026-04-03` so I can capture the live route response and update the task evidence from real outputs.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -m py_compile 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\run_twitter_canonical_workflow.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_run_twitter_canonical_workflow.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tools\\social_posting_package\\generate_posting_package.py'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -m unittest 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_social_publisher.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_run_twitter_canonical_workflow.py'" in C:\Users\edebe\eds
 succeeded in 1317ms:
2026-04-03T00:04:19.326629Z ERROR codex_core::tools::router: error=Exit code: 1
Wall time: 2.3 seconds
Output:
.....EE
======================================================================
ERROR: test_validate_payload_accepts_matching_generated_payload (TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow.RunTwitterCanonicalWorkflowTests.test_validate_payload_accepts_matching_generated_payload)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz\\json\\live\\social_posting_package\\2026-04-03'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz\\json\\live\\social_posting_package'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz\\json\\live'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 22, in test_validate_payload_accepts_matching_generated_payload
    package_root.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz\\json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen os>", line 368, in walk
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 18, in test_validate_payload_accepts_matching_generated_payload
    with tempfile.TemporaryDirectory() as tmp:
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 946, in __exit__
    self.cleanup()
    ~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 950, in cleanup
    self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 930, in _rmtree
    _shutil.rmtree(name, onexc=onexc)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\shutil.py", line 790, in rmtree
    return _rmtree_unsafe(path, onexc)
  File "C:\Python313\Lib\shutil.py", line 613, in _rmtree_unsafe
    for dirpath, dirnames, filenames in results:
                                        ^^^^^^^
  File "<frozen os>", line 371, in walk
  File "C:\Python313\Lib\shutil.py", line 611, in onerror
    onexc(os.scandir, err.filename, err)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 902, in onexc
    _resetperms(path)
    ~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 286, in _resetperms
    _dont_follow_symlinks(_os.chmod, path, 0o700)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 275, in _dont_follow_symlinks
    func(path, *args, follow_symlinks=False)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz'

======================================================================
ERROR: test_validate_payload_rejects_mismatch (TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow.RunTwitterCanonicalWorkflowTests.test_validate_payload_rejects_mismatch)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3\\json\\live\\social_posting_package\\2026-04-03'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3\\json\\live\\social_posting_package'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3\\json\\live'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 46, in test_validate_payload_rejects_mismatch
    package_root.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3\\json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen os>", line 368, in walk
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 42, in test_validate_payload_rejects_mismatch
    with tempfile.TemporaryDirectory() as tmp:
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 946, in __exit__
    self.cleanup()
    ~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 950, in cleanup
    self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 930, in _rmtree
    _shutil.rmtree(name, onexc=onexc)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\shutil.py", line 790, in rmtree
    return _rmtree_unsafe(path, onexc)
  File "C:\Python313\Lib\shutil.py", line 613, in _rmtree_unsafe
    for dirpath, dirnames, filenames in results:
                                        ^^^^^^^
  File "<frozen os>", line 371, in walk
  File "C:\Python313\Lib\shutil.py", line 611, in onerror
    onexc(os.scandir, err.filename, err)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 902, in onexc
    _resetperms(path)
    ~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 286, in _resetperms
    _dont_follow_symlinks(_os.chmod, path, 0o700)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 275, in _dont_follow_symlinks
    func(path, *args, follow_symlinks=False)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3'

----------------------------------------------------------------------
Ran 7 tests in 0.122s

FAILED (errors=2)

 exited 1 in 2274ms:
.....EE
======================================================================
ERROR: test_validate_payload_accepts_matching_generated_payload (TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow.RunTwitterCanonicalWorkflowTests.test_validate_payload_accepts_matching_generated_payload)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz\\json\\live\\social_posting_package\\2026-04-03'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz\\json\\live\\social_posting_package'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz\\json\\live'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 22, in test_validate_payload_accepts_matching_generated_payload
    package_root.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz\\json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen os>", line 368, in walk
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 18, in test_validate_payload_accepts_matching_generated_payload
    with tempfile.TemporaryDirectory() as tmp:
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 946, in __exit__
    self.cleanup()
    ~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 950, in cleanup
    self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 930, in _rmtree
    _shutil.rmtree(name, onexc=onexc)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\shutil.py", line 790, in rmtree
    return _rmtree_unsafe(path, onexc)
  File "C:\Python313\Lib\shutil.py", line 613, in _rmtree_unsafe
    for dirpath, dirnames, filenames in results:
                                        ^^^^^^^
  File "<frozen os>", line 371, in walk
  File "C:\Python313\Lib\shutil.py", line 611, in onerror
    onexc(os.scandir, err.filename, err)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 902, in onexc
    _resetperms(path)
    ~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 286, in _resetperms
    _dont_follow_symlinks(_os.chmod, path, 0o700)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 275, in _dont_follow_symlinks
    func(path, *args, follow_symlinks=False)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmplw5k5clz'

======================================================================
ERROR: test_validate_payload_rejects_mismatch (TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow.RunTwitterCanonicalWorkflowTests.test_validate_payload_rejects_mismatch)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3\\json\\live\\social_posting_package\\2026-04-03'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3\\json\\live\\social_posting_package'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3\\json\\live'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 46, in test_validate_payload_rejects_mismatch
    package_root.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3\\json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen os>", line 368, in walk
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 42, in test_validate_payload_rejects_mismatch
    with tempfile.TemporaryDirectory() as tmp:
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 946, in __exit__
    self.cleanup()
    ~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 950, in cleanup
    self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 930, in _rmtree
    _shutil.rmtree(name, onexc=onexc)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\shutil.py", line 790, in rmtree
    return _rmtree_unsafe(path, onexc)
  File "C:\Python313\Lib\shutil.py", line 613, in _rmtree_unsafe
    for dirpath, dirnames, filenames in results:
                                        ^^^^^^^
  File "<frozen os>", line 371, in walk
  File "C:\Python313\Lib\shutil.py", line 611, in onerror
    onexc(os.scandir, err.filename, err)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 902, in onexc
    _resetperms(path)
    ~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 286, in _resetperms
    _dont_follow_symlinks(_os.chmod, path, 0o700)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 275, in _dont_follow_symlinks
    func(path, *args, follow_symlinks=False)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\AppData\\Local\\Temp\\tmpbgfkxii3'

----------------------------------------------------------------------
Ran 7 tests in 0.122s

FAILED (errors=2)

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..f77578c019ddb1c0913b78ddba241a4fa042868d
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,66 @@
+import json
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+            temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": tweet_text}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        with tempfile.TemporaryDirectory() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": "different tweet"}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

codex
The new unit tests hit a Windows temp-directory permission quirk in this sandbox. I’m switching those tests to a workspace-local temp folder so the validation stays deterministic and doesn’t depend on `%TEMP%` permissions.
apply patch
patch: completed
C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..3367b8931cfe310d6bd115d19700f903d51fc064
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,76 @@
+import json
+import shutil
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_workspace_tempdir(self) -> tempfile.TemporaryDirectory:
+        base_dir = FS_DIR / "tests" / "_tmp"
+        base_dir.mkdir(parents=True, exist_ok=True)
+        return tempfile.TemporaryDirectory(dir=base_dir)
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        with self.make_workspace_tempdir() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+            temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": tweet_text}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        with self.make_workspace_tempdir() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": "different tweet"}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..3367b8931cfe310d6bd115d19700f903d51fc064
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,76 @@
+import json
+import shutil
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_workspace_tempdir(self) -> tempfile.TemporaryDirectory:
+        base_dir = FS_DIR / "tests" / "_tmp"
+        base_dir.mkdir(parents=True, exist_ok=True)
+        return tempfile.TemporaryDirectory(dir=base_dir)
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        with self.make_workspace_tempdir() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+            temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": tweet_text}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        with self.make_workspace_tempdir() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": "different tweet"}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\run_twitter_canonical_workflow.py' 2026-04-03" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -m unittest 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_social_publisher.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_run_twitter_canonical_workflow.py'" in C:\Users\edebe\eds
2026-04-03T00:04:41.738047Z ERROR codex_core::tools::router: error=Exit code: 1
Wall time: 2 seconds
Output:
.....EE
======================================================================
ERROR: test_validate_payload_accepts_matching_generated_payload (TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow.RunTwitterCanonicalWorkflowTests.test_validate_payload_accepts_matching_generated_payload)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn\\json\\live\\social_posting_package\\2026-04-03'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn\\json\\live\\social_posting_package'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn\\json\\live'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 28, in test_validate_payload_accepts_matching_generated_payload
    package_root.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn\\json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen os>", line 368, in walk
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 24, in test_validate_payload_accepts_matching_generated_payload
    with self.make_workspace_tempdir() as tmp:
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 946, in __exit__
    self.cleanup()
    ~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 950, in cleanup
    self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 930, in _rmtree
    _shutil.rmtree(name, onexc=onexc)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\shutil.py", line 790, in rmtree
    return _rmtree_unsafe(path, onexc)
  File "C:\Python313\Lib\shutil.py", line 613, in _rmtree_unsafe
    for dirpath, dirnames, filenames in results:
                                        ^^^^^^^
  File "<frozen os>", line 371, in walk
  File "C:\Python313\Lib\shutil.py", line 611, in onerror
    onexc(os.scandir, err.filename, err)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 902, in onexc
    _resetperms(path)
    ~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 286, in _resetperms
    _dont_follow_symlinks(_os.chmod, path, 0o700)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 275, in _dont_follow_symlinks
    func(path, *args, follow_symlinks=False)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn'

======================================================================
ERROR: test_validate_payload_rejects_mismatch (TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow.RunTwitterCanonicalWorkflowTests.test_validate_payload_rejects_mismatch)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1\\json\\live\\social_posting_package\\2026-04-03'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1\\json\\live\\social_posting_package'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1\\json\\live'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 52, in test_validate_payload_rejects_mismatch
    package_root.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1\\json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen os>", line 368, in walk
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 48, in test_validate_payload_rejects_mismatch
    with self.make_workspace_tempdir() as tmp:
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 946, in __exit__
    self.cleanup()
    ~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 950, in cleanup
    self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 930, in _rmtree
    _shutil.rmtree(name, onexc=onexc)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\shutil.py", line 790, in rmtree
    return _rmtree_unsafe(path, onexc)
  File "C:\Python313\Lib\shutil.py", line 613, in _rmtree_unsafe
    for dirpath, dirnames, filenames in results:
                                        ^^^^^^^
  File "<frozen os>", line 371, in walk
  File "C:\Python313\Lib\shutil.py", line 611, in onerror
    onexc(os.scandir, err.filename, err)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 902, in onexc
    _resetperms(path)
    ~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 286, in _resetperms
    _dont_follow_symlinks(_os.chmod, path, 0o700)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 275, in _dont_follow_symlinks
    func(path, *args, follow_symlinks=False)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1'

----------------------------------------------------------------------
Ran 7 tests in 0.061s

FAILED (errors=2)

 exited 1 in 2036ms:
.....EE
======================================================================
ERROR: test_validate_payload_accepts_matching_generated_payload (TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow.RunTwitterCanonicalWorkflowTests.test_validate_payload_accepts_matching_generated_payload)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn\\json\\live\\social_posting_package\\2026-04-03'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn\\json\\live\\social_posting_package'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn\\json\\live'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 28, in test_validate_payload_accepts_matching_generated_payload
    package_root.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn\\json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen os>", line 368, in walk
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 24, in test_validate_payload_accepts_matching_generated_payload
    with self.make_workspace_tempdir() as tmp:
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 946, in __exit__
    self.cleanup()
    ~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 950, in cleanup
    self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 930, in _rmtree
    _shutil.rmtree(name, onexc=onexc)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\shutil.py", line 790, in rmtree
    return _rmtree_unsafe(path, onexc)
  File "C:\Python313\Lib\shutil.py", line 613, in _rmtree_unsafe
    for dirpath, dirnames, filenames in results:
                                        ^^^^^^^
  File "<frozen os>", line 371, in walk
  File "C:\Python313\Lib\shutil.py", line 611, in onerror
    onexc(os.scandir, err.filename, err)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 902, in onexc
    _resetperms(path)
    ~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 286, in _resetperms
    _dont_follow_symlinks(_os.chmod, path, 0o700)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 275, in _dont_follow_symlinks
    func(path, *args, follow_symlinks=False)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmpajaojnkn'

======================================================================
ERROR: test_validate_payload_rejects_mismatch (TradeApps.breakout.fs.tests.test_run_twitter_canonical_workflow.RunTwitterCanonicalWorkflowTests.test_validate_payload_rejects_mismatch)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1\\json\\live\\social_posting_package\\2026-04-03'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1\\json\\live\\social_posting_package'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1\\json\\live'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 52, in test_validate_payload_rejects_mismatch
    package_root.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 726, in mkdir
    self.parent.mkdir(parents=True, exist_ok=True)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\pathlib\_local.py", line 722, in mkdir
    os.mkdir(self, mode)
    ~~~~~~~~^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1\\json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen os>", line 368, in walk
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py", line 48, in test_validate_payload_rejects_mismatch
    with self.make_workspace_tempdir() as tmp:
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 946, in __exit__
    self.cleanup()
    ~~~~~~~~~~~~^^
  File "C:\Python313\Lib\tempfile.py", line 950, in cleanup
    self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 930, in _rmtree
    _shutil.rmtree(name, onexc=onexc)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\shutil.py", line 790, in rmtree
    return _rmtree_unsafe(path, onexc)
  File "C:\Python313\Lib\shutil.py", line 613, in _rmtree_unsafe
    for dirpath, dirnames, filenames in results:
                                        ^^^^^^^
  File "<frozen os>", line 371, in walk
  File "C:\Python313\Lib\shutil.py", line 611, in onerror
    onexc(os.scandir, err.filename, err)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 902, in onexc
    _resetperms(path)
    ~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 286, in _resetperms
    _dont_follow_symlinks(_os.chmod, path, 0o700)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\tempfile.py", line 275, in _dont_follow_symlinks
    func(path, *args, follow_symlinks=False)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\_tmp\\tmp_ws0dls1'

----------------------------------------------------------------------
Ran 7 tests in 0.061s

FAILED (errors=2)

 succeeded in 9073ms:
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..3367b8931cfe310d6bd115d19700f903d51fc064
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,76 @@
+import json
+import shutil
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_workspace_tempdir(self) -> tempfile.TemporaryDirectory:
+        base_dir = FS_DIR / "tests" / "_tmp"
+        base_dir.mkdir(parents=True, exist_ok=True)
+        return tempfile.TemporaryDirectory(dir=base_dir)
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        with self.make_workspace_tempdir() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+            temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": tweet_text}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        with self.make_workspace_tempdir() as tmp:
+            root = Path(tmp)
+            temp_tweet = root / "temp_tweet.txt"
+            package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+            package_root.mkdir(parents=True, exist_ok=True)
+
+            temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+            (package_root / "top5_weekly_posting_package.json").write_text(
+                json.dumps({"consolidated_twitter_post": "different tweet"}),
+                encoding="utf-8",
+            )
+
+            with (
+                patch.object(workflow, "TEMP_TWEET", temp_tweet),
+                patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+            ):
+                ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

codex
The end-to-end workflow run has already completed successfully. I still need clean automated validation, so I’m removing `tempfile` from the unit tests entirely and replacing it with fixed workspace test directories to avoid the sandbox’s directory-creation restrictions.
apply patch
patch: completed
C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..ff2f3933df6ea5e6f9ece41905b2198788a2c8de
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,74 @@
+import json
+import shutil
+import sys
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_case_root(self, case_name: str) -> Path:
+        root = FS_DIR / "tests" / "_tmp" / case_name
+        shutil.rmtree(root, ignore_errors=True)
+        root.mkdir(parents=True, exist_ok=True)
+        return root
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        root = self.make_case_root("validate_payload_accepts")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+        temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": tweet_text}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        root = self.make_case_root("validate_payload_rejects")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": "different tweet"}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..ff2f3933df6ea5e6f9ece41905b2198788a2c8de
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,74 @@
+import json
+import shutil
+import sys
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_case_root(self, case_name: str) -> Path:
+        root = FS_DIR / "tests" / "_tmp" / case_name
+        shutil.rmtree(root, ignore_errors=True)
+        root.mkdir(parents=True, exist_ok=True)
+        return root
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        root = self.make_case_root("validate_payload_accepts")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+        temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": tweet_text}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        root = self.make_case_root("validate_payload_rejects")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": "different tweet"}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -m unittest 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_social_publisher.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_run_twitter_canonical_workflow.py'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\twitter_x_api_post_response.json'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\temp_tweet.txt'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\twitter_workflow_status.json'" in C:\Users\edebe\eds
 succeeded in 1588ms:
{
  "timestamp": "2026-04-03T01:04:47.670969",
  "run_date": "2026-04-03",
  "request": {
    "url": "http://localhost:5000/api/social/x_api_post",
    "trigger": "recurring_summary_returns_every_4_hours",
    "text_length": 233,
    "text": "Update at 2026-04-03 00:00\n\nToday\n1. SI 7050\n2. NQ 4035\n3. CL 3635\n4. ES 2675\n5. HG 1780\n\nWeekly so far\n1. SI 18410\n2. NQ 10990\n3. CL 9205\n4. ES 7770\n5. YM 4110\n\nFull details to follow.\n#StrategyWarehouse #FuturesTrading #AlgoTrading"
  },
  "response": {
    "status_code": 200,
    "payload": {
      "message": "Tweet posted successfully",
      "success": true,
      "tweet_id": "2039856634994852247"
    }
  }
}

 succeeded in 1558ms:
Update at 2026-04-03 00:00

Today
1. SI 7050
2. NQ 4035
3. CL 3635
4. ES 2675
5. HG 1780

Weekly so far
1. SI 18410
2. NQ 10990
3. CL 9205
4. ES 7770
5. YM 4110

Full details to follow.
#StrategyWarehouse #FuturesTrading #AlgoTrading


 succeeded in 1653ms:
{
  "timestamp": "2026-04-03T01:04:40.208896",
  "run_date": "2026-04-03",
  "steps": {
    "verify_api": {
      "ok": true,
      "details": "API reachable on http://localhost:5000/api/health: {'status': 'ok', 'ts': '2026-04-03T00:04:42.333167'}",
      "artifact": "http://localhost:5000/api/health"
    },
    "generate_content": {
      "ok": true,
      "details": "[INFO] JSON package written to C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\social_posting_package\\2026-04-03\\top5_weekly_posting_package.json\n[INFO] Markdown package written to C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\social_posting_package\\2026-04-03\\top5_weekly_posting_package.md",
      "artifact": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\temp_tweet.txt"
    },
    "validate_payload": {
      "ok": true,
      "details": "Validated payload (233 chars) matches C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\social_posting_package\\2026-04-03\\top5_weekly_posting_package.json",
      "artifact": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\social_posting_package\\2026-04-03\\top5_weekly_posting_package.json"
    },
    "submit_post": {
      "ok": true,
      "details": "POST http://localhost:5000/api/social/x_api_post returned HTTP 200: {'message': 'Tweet posted successfully', 'success': True, 'tweet_id': '2039856634994852247'}",
      "artifact": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\twitter_x_api_post_response.json"
    }
  },
  "final_status": "success"
}

 succeeded in 2197ms:
.......
----------------------------------------------------------------------
Ran 7 tests in 0.126s

OK

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..ff2f3933df6ea5e6f9ece41905b2198788a2c8de
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,74 @@
+import json
+import shutil
+import sys
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_case_root(self, case_name: str) -> Path:
+        root = FS_DIR / "tests" / "_tmp" / case_name
+        shutil.rmtree(root, ignore_errors=True)
+        root.mkdir(parents=True, exist_ok=True)
+        return root
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        root = self.make_case_root("validate_payload_accepts")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+        temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": tweet_text}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        root = self.make_case_root("validate_payload_rejects")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": "different tweet"}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

codex
I have the live evidence now: the recurring `2026-04-03` run regenerated the payload and the route returned tweet ID `2039856634994852247`. I’m updating the lifecycle file next with the exact commands, artifacts, and an `Awaiting user verification` completion state because the task rules require an operator pass/fail before it can move to complete.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "(Get-Item 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\temp_tweet.txt').LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss K')" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'Get-Date -Format "yyyy-MM-dd HH:mm:ss K"' in C:\Users\edebe\eds
 succeeded in 1305ms:
2026-04-03 01:04:42 +01:00

 succeeded in 1364ms:
2026-04-03 01:05:49 +01:00

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..ff2f3933df6ea5e6f9ece41905b2198788a2c8de
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,74 @@
+import json
+import shutil
+import sys
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_case_root(self, case_name: str) -> Path:
+        root = FS_DIR / "tests" / "_tmp" / case_name
+        shutil.rmtree(root, ignore_errors=True)
+        root.mkdir(parents=True, exist_ok=True)
+        return root
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        root = self.make_case_root("validate_payload_accepts")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+        temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": tweet_text}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        root = self.make_case_root("validate_payload_rejects")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": "different tweet"}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.

apply patch
patch: completed
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..ff2f3933df6ea5e6f9ece41905b2198788a2c8de
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,74 @@
+import json
+import shutil
+import sys
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_case_root(self, case_name: str) -> Path:
+        root = FS_DIR / "tests" / "_tmp" / case_name
+        shutil.rmtree(root, ignore_errors=True)
+        root.mkdir(parents=True, exist_ok=True)
+        return root
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        root = self.make_case_root("validate_payload_accepts")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+        temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": tweet_text}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        root = self.make_case_root("validate_payload_rejects")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": "different tweet"}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.
diff --git a/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md b/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
index bb25f91e955080811ce731ee2883b6813bf2ec2f..a7af9eed926646b8a2a562d92766874fc3f0ad93
--- a/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
+++ b/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
@@ -61,109 +61,78 @@
 
 
 
-## Plan
-
-
-
-- [ ] 1. Regenerate the latest summary returns payload for the current run window.
-
-  - [ ] Test: `generate_posting_package.py --date YYYY-MM-DD` completes successfully and refreshes `temp_tweet.txt`.
-
-  - Evidence:
-
-
-
-- [ ] 2. Validate the prepared post body without inventing unsupported figures.
-
-  - [ ] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
-
-  - Evidence:
-
-
-
-- [ ] 3. Submit the prepared payload through the X API route.
-
-  - [ ] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.
-
-  - Evidence:
-
-
-
-## Evidence
-
-
-
-Objective-Delivery-Coverage: 0%
-
-Auto-Acceptance: false
-
-- Evidence-Type: file_output
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.
-
-  - Status: planned
-
-- Evidence-Type: route_output
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Proves the X API posting attempt outcome for this run.
-
-  - Status: planned
-
-- Evidence-Type: manual_verification
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.
-
-  - Status: planned
-
-
-
-## Implementation Log
-
-
-
-- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
-
-
-
-## Changes Made
-
-
-
-- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
-
-
-
-## Validation
-
-
-
-- Pending execution.
-
-
-
-## Risks/Notes
-
-
-
-- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
-
-- Use local data only; do not invent returns or write new market figures without a source artifact.
-
-- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
-
+## Plan
+
+- [x] 1. Regenerate the latest summary returns payload for the current run window.
+  - [x] Test: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03` completes successfully and refreshes `temp_tweet.txt`.
+  - Evidence: `temp_tweet.txt` last-write time moved to `2026-04-03 01:04:42 +01:00`, and the dated package outputs were regenerated under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\`.
+
+- [x] 2. Validate the prepared post body without inventing unsupported figures.
+  - [x] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
+  - Evidence: `twitter_workflow_status.json` recorded `Validated payload (233 chars)` and confirmed `temp_tweet.txt` matches `json\live\social_posting_package\2026-04-03\top5_weekly_posting_package.json`.
+
+- [x] 3. Submit the prepared payload through the X API route.
+  - [x] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.
+  - Evidence: `twitter_x_api_post_response.json` captured HTTP `200` with `{"message":"Tweet posted successfully","success":true,"tweet_id":"2039856634994852247"}` for trigger `recurring_summary_returns_every_4_hours`.
 
 
-## Completion Status
-
-
-
-- State: TODO
-
-- Timestamp:
-
+## Evidence
+
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
+  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
+  - Objective-Proved: Proves the X API posting attempt outcome for this run.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: Pending operator verification request for live tweet ID `2039856634994852247` and workflow artefacts `twitter_workflow_status.json` plus `twitter_x_api_post_response.json`
+  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.
+  - Status: planned
+
+## Implementation Log
+
+- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
+- 2026-04-03 01:01 Europe/London: Read `skills/workstream-task-lifecycle/` and the required `skills/twitter-canonical-posting/` skill, then inspected the existing workflow script and X API route implementation.
+- 2026-04-03 01:03 Europe/London: Updated `run_twitter_canonical_workflow.py` to verify local API health, regenerate the posting package, validate `temp_tweet.txt` against `consolidated_twitter_post`, submit via `POST /api/social/x_api_post`, and persist the exact route response to `twitter_x_api_post_response.json`.
+- 2026-04-03 01:03 Europe/London: Updated `skills/twitter-canonical-posting/SKILL.md` so the documented scheduled workflow matches the X API route path instead of the browser posting path.
+- 2026-04-03 01:04 Europe/London: Added workflow unit coverage in `tests/test_run_twitter_canonical_workflow.py` for matching and mismatched payload validation.
+- 2026-04-03 01:04 Europe/London: Executed `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`; the run succeeded and posted tweet ID `2039856634994852247`.
+
+## Changes Made
+
+- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
+- Updated `TradeApps\breakout\fs\run_twitter_canonical_workflow.py` to use the local X API route as the posting gate and to capture the exact HTTP response in `twitter_x_api_post_response.json`.
+- Updated `skills\twitter-canonical-posting\SKILL.md` so the documented canonical workflow matches the implemented route-based posting path.
+- Added `TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` to cover payload-validation behavior.
+
+## Validation
+
+- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/health`
+  - Result: `{"status":"ok","ts":"2026-04-03T00:02:26.293168"}`
+- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/social/status`
+  - Result: `api_enabled=true`, `can_post=true`, `reason="OK"` before the run.
+- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
+  - Result: passed with no output.
+- `python -m unittest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_social_publisher.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
+  - Result: `Ran 7 tests in 0.126s` and `OK`.
+- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`
+  - Result: generated `temp_tweet.txt`, validated a `233`-character payload, and recorded HTTP `200` with tweet ID `2039856634994852247` in `twitter_x_api_post_response.json`.
+- User verification requested in assistant final response for:
+  - Confirm the live post for tweet ID `2039856634994852247` is acceptable.
+  - Confirm the route-based recurring workflow and captured artefacts are the expected behavior.
+
+## Risks/Notes
+
+- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
+- Use local data only; do not invent returns or write new market figures without a source artifact.
+- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
+- This task remains in `200_inprogress` until operator verification outcome is captured per the lifecycle completion gate.
+
+## Completion Status
+
+- State: Awaiting user verification
+- Timestamp: 2026-04-03 01:05:49 +01:00

diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..ff2f3933df6ea5e6f9ece41905b2198788a2c8de
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,74 @@
+import json
+import shutil
+import sys
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_case_root(self, case_name: str) -> Path:
+        root = FS_DIR / "tests" / "_tmp" / case_name
+        shutil.rmtree(root, ignore_errors=True)
+        root.mkdir(parents=True, exist_ok=True)
+        return root
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        root = self.make_case_root("validate_payload_accepts")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+        temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": tweet_text}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        root = self.make_case_root("validate_payload_rejects")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": "different tweet"}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.
diff --git a/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md b/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
index bb25f91e955080811ce731ee2883b6813bf2ec2f..a7af9eed926646b8a2a562d92766874fc3f0ad93
--- a/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
+++ b/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
@@ -61,109 +61,78 @@
 
 
 
-## Plan
-
-
-
-- [ ] 1. Regenerate the latest summary returns payload for the current run window.
-
-  - [ ] Test: `generate_posting_package.py --date YYYY-MM-DD` completes successfully and refreshes `temp_tweet.txt`.
-
-  - Evidence:
-
-
-
-- [ ] 2. Validate the prepared post body without inventing unsupported figures.
-
-  - [ ] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
-
-  - Evidence:
-
-
-
-- [ ] 3. Submit the prepared payload through the X API route.
-
-  - [ ] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.
-
-  - Evidence:
-
-
-
-## Evidence
-
-
-
-Objective-Delivery-Coverage: 0%
-
-Auto-Acceptance: false
-
-- Evidence-Type: file_output
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.
-
-  - Status: planned
-
-- Evidence-Type: route_output
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Proves the X API posting attempt outcome for this run.
-
-  - Status: planned
-
-- Evidence-Type: manual_verification
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.
-
-  - Status: planned
-
-
-
-## Implementation Log
-
-
-
-- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
-
-
-
-## Changes Made
-
-
-
-- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
-
-
-
-## Validation
-
-
-
-- Pending execution.
-
-
-
-## Risks/Notes
-
-
-
-- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
-
-- Use local data only; do not invent returns or write new market figures without a source artifact.
-
-- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
-
+## Plan
+
+- [x] 1. Regenerate the latest summary returns payload for the current run window.
+  - [x] Test: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03` completes successfully and refreshes `temp_tweet.txt`.
+  - Evidence: `temp_tweet.txt` last-write time moved to `2026-04-03 01:04:42 +01:00`, and the dated package outputs were regenerated under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\`.
+
+- [x] 2. Validate the prepared post body without inventing unsupported figures.
+  - [x] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
+  - Evidence: `twitter_workflow_status.json` recorded `Validated payload (233 chars)` and confirmed `temp_tweet.txt` matches `json\live\social_posting_package\2026-04-03\top5_weekly_posting_package.json`.
+
+- [x] 3. Submit the prepared payload through the X API route.
+  - [x] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.
+  - Evidence: `twitter_x_api_post_response.json` captured HTTP `200` with `{"message":"Tweet posted successfully","success":true,"tweet_id":"2039856634994852247"}` for trigger `recurring_summary_returns_every_4_hours`.
 
 
-## Completion Status
-
-
-
-- State: TODO
-
-- Timestamp:
-
+## Evidence
+
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
+  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
+  - Objective-Proved: Proves the X API posting attempt outcome for this run.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: Pending operator verification request for live tweet ID `2039856634994852247` and workflow artefacts `twitter_workflow_status.json` plus `twitter_x_api_post_response.json`
+  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.
+  - Status: planned
+
+## Implementation Log
+
+- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
+- 2026-04-03 01:01 Europe/London: Read `skills/workstream-task-lifecycle/` and the required `skills/twitter-canonical-posting/` skill, then inspected the existing workflow script and X API route implementation.
+- 2026-04-03 01:03 Europe/London: Updated `run_twitter_canonical_workflow.py` to verify local API health, regenerate the posting package, validate `temp_tweet.txt` against `consolidated_twitter_post`, submit via `POST /api/social/x_api_post`, and persist the exact route response to `twitter_x_api_post_response.json`.
+- 2026-04-03 01:03 Europe/London: Updated `skills/twitter-canonical-posting/SKILL.md` so the documented scheduled workflow matches the X API route path instead of the browser posting path.
+- 2026-04-03 01:04 Europe/London: Added workflow unit coverage in `tests/test_run_twitter_canonical_workflow.py` for matching and mismatched payload validation.
+- 2026-04-03 01:04 Europe/London: Executed `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`; the run succeeded and posted tweet ID `2039856634994852247`.
+
+## Changes Made
+
+- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
+- Updated `TradeApps\breakout\fs\run_twitter_canonical_workflow.py` to use the local X API route as the posting gate and to capture the exact HTTP response in `twitter_x_api_post_response.json`.
+- Updated `skills\twitter-canonical-posting\SKILL.md` so the documented canonical workflow matches the implemented route-based posting path.
+- Added `TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` to cover payload-validation behavior.
+
+## Validation
+
+- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/health`
+  - Result: `{"status":"ok","ts":"2026-04-03T00:02:26.293168"}`
+- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/social/status`
+  - Result: `api_enabled=true`, `can_post=true`, `reason="OK"` before the run.
+- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
+  - Result: passed with no output.
+- `python -m unittest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_social_publisher.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
+  - Result: `Ran 7 tests in 0.126s` and `OK`.
+- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`
+  - Result: generated `temp_tweet.txt`, validated a `233`-character payload, and recorded HTTP `200` with tweet ID `2039856634994852247` in `twitter_x_api_post_response.json`.
+- User verification requested in assistant final response for:
+  - Confirm the live post for tweet ID `2039856634994852247` is acceptable.
+  - Confirm the route-based recurring workflow and captured artefacts are the expected behavior.
+
+## Risks/Notes
+
+- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
+- Use local data only; do not invent returns or write new market figures without a source artifact.
+- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
+- This task remains in `200_inprogress` until operator verification outcome is captured per the lifecycle completion gate.
+
+## Completion Status
+
+- State: Awaiting user verification
+- Timestamp: 2026-04-03 01:05:49 +01:00

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git status --short -- 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\run_twitter_canonical_workflow.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_run_twitter_canonical_workflow.py' 'C:\\Users\\edebe\\eds\\skills\\twitter-canonical-posting\\SKILL.md' 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260403_010000_breakout_twitter_summary_returns_every_4_hours.md' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\twitter_workflow_status.json' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\twitter_x_api_post_response.json' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\temp_tweet.txt'" in C:\Users\edebe\eds
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git diff -- 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\run_twitter_canonical_workflow.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\tests\\test_run_twitter_canonical_workflow.py' 'C:\\Users\\edebe\\eds\\skills\\twitter-canonical-posting\\SKILL.md' 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260403_010000_breakout_twitter_summary_returns_every_4_hours.md'" in C:\Users\edebe\eds
 succeeded in 1349ms:
?? skills/twitter-canonical-posting/SKILL.md
?? workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md

 succeeded in 1472ms:
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..ff2f3933df6ea5e6f9ece41905b2198788a2c8de
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,74 @@
+import json
+import shutil
+import sys
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_case_root(self, case_name: str) -> Path:
+        root = FS_DIR / "tests" / "_tmp" / case_name
+        shutil.rmtree(root, ignore_errors=True)
+        root.mkdir(parents=True, exist_ok=True)
+        return root
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        root = self.make_case_root("validate_payload_accepts")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+        temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": tweet_text}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        root = self.make_case_root("validate_payload_rejects")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": "different tweet"}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.
diff --git a/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md b/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
index bb25f91e955080811ce731ee2883b6813bf2ec2f..a7af9eed926646b8a2a562d92766874fc3f0ad93
--- a/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
+++ b/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
@@ -61,109 +61,78 @@
 
 
 
-## Plan
-
-
-
-- [ ] 1. Regenerate the latest summary returns payload for the current run window.
-
-  - [ ] Test: `generate_posting_package.py --date YYYY-MM-DD` completes successfully and refreshes `temp_tweet.txt`.
-
-  - Evidence:
-
-
-
-- [ ] 2. Validate the prepared post body without inventing unsupported figures.
-
-  - [ ] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
-
-  - Evidence:
-
-
-
-- [ ] 3. Submit the prepared payload through the X API route.
-
-  - [ ] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.
-
-  - Evidence:
-
-
-
-## Evidence
-
-
-
-Objective-Delivery-Coverage: 0%
-
-Auto-Acceptance: false
-
-- Evidence-Type: file_output
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.
-
-  - Status: planned
-
-- Evidence-Type: route_output
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Proves the X API posting attempt outcome for this run.
-
-  - Status: planned
-
-- Evidence-Type: manual_verification
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.
-
-  - Status: planned
-
-
-
-## Implementation Log
-
-
-
-- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
-
-
-
-## Changes Made
-
-
-
-- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
-
-
-
-## Validation
-
-
-
-- Pending execution.
-
-
-
-## Risks/Notes
-
-
-
-- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
-
-- Use local data only; do not invent returns or write new market figures without a source artifact.
-
-- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
-
+## Plan
+
+- [x] 1. Regenerate the latest summary returns payload for the current run window.
+  - [x] Test: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03` completes successfully and refreshes `temp_tweet.txt`.
+  - Evidence: `temp_tweet.txt` last-write time moved to `2026-04-03 01:04:42 +01:00`, and the dated package outputs were regenerated under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\`.
+
+- [x] 2. Validate the prepared post body without inventing unsupported figures.
+  - [x] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
+  - Evidence: `twitter_workflow_status.json` recorded `Validated payload (233 chars)` and confirmed `temp_tweet.txt` matches `json\live\social_posting_package\2026-04-03\top5_weekly_posting_package.json`.
+
+- [x] 3. Submit the prepared payload through the X API route.
+  - [x] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.
+  - Evidence: `twitter_x_api_post_response.json` captured HTTP `200` with `{"message":"Tweet posted successfully","success":true,"tweet_id":"2039856634994852247"}` for trigger `recurring_summary_returns_every_4_hours`.
 
 
-## Completion Status
-
-
-
-- State: TODO
-
-- Timestamp:
-
+## Evidence
+
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
+  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
+  - Objective-Proved: Proves the X API posting attempt outcome for this run.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: Pending operator verification request for live tweet ID `2039856634994852247` and workflow artefacts `twitter_workflow_status.json` plus `twitter_x_api_post_response.json`
+  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.
+  - Status: planned
+
+## Implementation Log
+
+- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
+- 2026-04-03 01:01 Europe/London: Read `skills/workstream-task-lifecycle/` and the required `skills/twitter-canonical-posting/` skill, then inspected the existing workflow script and X API route implementation.
+- 2026-04-03 01:03 Europe/London: Updated `run_twitter_canonical_workflow.py` to verify local API health, regenerate the posting package, validate `temp_tweet.txt` against `consolidated_twitter_post`, submit via `POST /api/social/x_api_post`, and persist the exact route response to `twitter_x_api_post_response.json`.
+- 2026-04-03 01:03 Europe/London: Updated `skills/twitter-canonical-posting/SKILL.md` so the documented scheduled workflow matches the X API route path instead of the browser posting path.
+- 2026-04-03 01:04 Europe/London: Added workflow unit coverage in `tests/test_run_twitter_canonical_workflow.py` for matching and mismatched payload validation.
+- 2026-04-03 01:04 Europe/London: Executed `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`; the run succeeded and posted tweet ID `2039856634994852247`.
+
+## Changes Made
+
+- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
+- Updated `TradeApps\breakout\fs\run_twitter_canonical_workflow.py` to use the local X API route as the posting gate and to capture the exact HTTP response in `twitter_x_api_post_response.json`.
+- Updated `skills\twitter-canonical-posting\SKILL.md` so the documented canonical workflow matches the implemented route-based posting path.
+- Added `TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` to cover payload-validation behavior.
+
+## Validation
+
+- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/health`
+  - Result: `{"status":"ok","ts":"2026-04-03T00:02:26.293168"}`
+- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/social/status`
+  - Result: `api_enabled=true`, `can_post=true`, `reason="OK"` before the run.
+- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
+  - Result: passed with no output.
+- `python -m unittest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_social_publisher.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
+  - Result: `Ran 7 tests in 0.126s` and `OK`.
+- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`
+  - Result: generated `temp_tweet.txt`, validated a `233`-character payload, and recorded HTTP `200` with tweet ID `2039856634994852247` in `twitter_x_api_post_response.json`.
+- User verification requested in assistant final response for:
+  - Confirm the live post for tweet ID `2039856634994852247` is acceptable.
+  - Confirm the route-based recurring workflow and captured artefacts are the expected behavior.
+
+## Risks/Notes
+
+- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
+- Use local data only; do not invent returns or write new market figures without a source artifact.
+- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
+- This task remains in `200_inprogress` until operator verification outcome is captured per the lifecycle completion gate.
+
+## Completion Status
+
+- State: Awaiting user verification
+- Timestamp: 2026-04-03 01:05:49 +01:00

codex
Implemented the route-based recurring workflow and executed the `2026-04-03` run end to end. The workflow entrypoint at [run_twitter_canonical_workflow.py](C:/Users/edebe/eds/TradeApps/breakout/fs/run_twitter_canonical_workflow.py) now does API health check -> payload generation -> payload validation against the generated package -> `POST /api/social/x_api_post`, and it writes the exact live response to [twitter_x_api_post_response.json](C:/Users/edebe/eds/TradeApps/breakout/fs/twitter_x_api_post_response.json). I also aligned the shared skill in [SKILL.md](C:/Users/edebe/eds/skills/twitter-canonical-posting/SKILL.md) and added unit coverage in [test_run_twitter_canonical_workflow.py](C:/Users/edebe/eds/TradeApps/breakout/fs/tests/test_run_twitter_canonical_workflow.py).

Validation passed: `py_compile`, `python -m unittest ...` (`Ran 7 tests ... OK`), and the live workflow run. The run regenerated [temp_tweet.txt](C:/Users/edebe/eds/TradeApps/breakout/fs/temp_tweet.txt), validated a 233-character payload, and posted successfully through the route with tweet ID `2039856634994852247`. The status trail is in [twitter_workflow_status.json](C:/Users/edebe/eds/TradeApps/breakout/fs/twitter_workflow_status.json), and the lifecycle file was updated at [20260403_010000_breakout_twitter_summary_returns_every_4_hours.md](C:/Users/edebe/eds/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md).

Per the lifecycle rules, I left the task in `Awaiting user verification`. Verify these two points and reply pass/fail:
1. The live post for tweet ID `2039856634994852247` is the expected content.
2. The new route-based recurring workflow and captured artefacts are the expected behavior.
diff --git a/breakout/fs/run_twitter_canonical_workflow.py b/breakout/fs/run_twitter_canonical_workflow.py
index 57ad91ddf10a16bc34c9acb8b104a5fc011387ae..bcadeaa9f83a97952ab0a9b33178515ed0b5b4ca
--- a/breakout/fs/run_twitter_canonical_workflow.py
+++ b/breakout/fs/run_twitter_canonical_workflow.py
@@ -3,16 +3,17 @@
 import json
 import subprocess
 import sys
-
-from twitter_browser import TwitterBrowser
+import time
+from urllib import error, request
 
 ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
 GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
-POST_SCRIPT = ROOT / "run_twitter_post_v3.py"
 TEMP_TWEET = ROOT / "temp_tweet.txt"
-POSTED_LOG = ROOT / "posted_tweets.log"
 WORKFLOW_STATUS = ROOT / "twitter_workflow_status.json"
-LOGIN_CHECK_SCREENSHOT = ROOT / "check_login.png"
+API_HEALTH_URL = "http://localhost:5000/api/health"
+API_POST_URL = "http://localhost:5000/api/social/x_api_post"
+API_RESPONSE_ARTIFACT = ROOT / "twitter_x_api_post_response.json"
+PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
 
 
 def _write_status(status: dict) -> None:
@@ -24,10 +25,10 @@
         "timestamp": datetime.datetime.now().isoformat(),
         "run_date": run_date,
         "steps": {
-            "verify_login": {"ok": False, "details": "", "artifact": str(LOGIN_CHECK_SCREENSHOT)},
+            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
             "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
-            "submit_post": {"ok": False, "details": "", "artifact": str(ROOT / "twitter_post_status.json")},
-            "verify_audit_log": {"ok": False, "details": "", "artifact": str(POSTED_LOG)},
+            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json")},
+            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
         },
         "final_status": "failed",
     }
@@ -39,20 +40,39 @@
     _write_status(status)
 
 
-def _posted_log_tail() -> str:
-    if not POSTED_LOG.exists():
-        return ""
-    return POSTED_LOG.read_text(encoding="utf-8", errors="replace")
+def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
+    body = None
+    headers = {}
+    if payload is not None:
+        body = json.dumps(payload).encode("utf-8")
+        headers["Content-Type"] = "application/json"
 
+    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
+    try:
+        with request.urlopen(req, timeout=30) as response:
+            raw = response.read().decode("utf-8", errors="replace")
+            return int(response.status), json.loads(raw)
+    except error.HTTPError as exc:
+        raw = exc.read().decode("utf-8", errors="replace")
+        try:
+            payload_json = json.loads(raw)
+        except json.JSONDecodeError:
+            payload_json = {"success": False, "error": raw or str(exc)}
+        return int(exc.code), payload_json
 
-def _verify_login() -> tuple[bool, str]:
-    with TwitterBrowser(headless=True) as tb:
-        logged_in = tb.is_logged_in()
-        tb.page.screenshot(path=LOGIN_CHECK_SCREENSHOT)
-        if not logged_in:
-            return False, f"Session is not authenticated. Current URL: {tb.page.url}"
-        return True, f"Authenticated session verified. Current URL: {tb.page.url}"
 
+def _verify_api_health() -> tuple[bool, str]:
+    try:
+        status_code, payload = _request_json(API_HEALTH_URL)
+    except Exception as exc:
+        return False, f"Health check failed: {exc}"
+
+    if status_code != 200:
+        return False, f"Health check returned HTTP {status_code}: {payload}"
+    if payload.get("status") != "ok":
+        return False, f"Health check returned unexpected payload: {payload}"
+    return True, f"API reachable on {API_HEALTH_URL}: {payload}"
+
 
 def _run_command(command: list[str]) -> subprocess.CompletedProcess:
     return subprocess.run(
@@ -66,17 +86,69 @@
     )
 
 
+def _load_package_json(run_date: str) -> dict:
+    package_path = PACKAGE_ROOT / run_date / "top5_weekly_posting_package.json"
+    if not package_path.exists():
+        raise FileNotFoundError(f"Posting package not found: {package_path}")
+    return json.loads(package_path.read_text(encoding="utf-8"))
+
+
+def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
+    if not TEMP_TWEET.exists():
+        return False, "temp_tweet.txt was not created", ""
+
+    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
+    if not tweet_text:
+        return False, "temp_tweet.txt is empty after generation", ""
+
+    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
+        return False, "temp_tweet.txt was not rewritten by the current generator run", tweet_text
+
+    package = _load_package_json(run_date)
+    consolidated = str(package.get("consolidated_twitter_post", "")).strip()
+    if not consolidated:
+        return False, "Posting package is missing consolidated_twitter_post", tweet_text
+
+    if tweet_text != consolidated:
+        return False, "temp_tweet.txt does not match consolidated_twitter_post", tweet_text
+
+    if len(tweet_text) > 280:
+        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text
+
+    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / 'top5_weekly_posting_package.json'}"
+    return True, details, tweet_text
+
+
+def _write_api_response_artifact(run_date: str, tweet_text: str, status_code: int, response_payload: dict) -> None:
+    artifact = {
+        "timestamp": datetime.datetime.now().isoformat(),
+        "run_date": run_date,
+        "request": {
+            "url": API_POST_URL,
+            "trigger": "recurring_summary_returns_every_4_hours",
+            "text_length": len(tweet_text),
+            "text": tweet_text,
+        },
+        "response": {
+            "status_code": status_code,
+            "payload": response_payload,
+        },
+    }
+    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
+
+
 def main() -> int:
     run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
     status = _new_status(run_date)
     _write_status(status)
 
-    logged_in, login_details = _verify_login()
-    if not logged_in:
-        _mark_step(status, "verify_login", False, login_details)
+    api_ok, api_details = _verify_api_health()
+    if not api_ok:
+        _mark_step(status, "verify_api", False, api_details)
         return 1
-    _mark_step(status, "verify_login", True, login_details)
+    _mark_step(status, "verify_api", True, api_details)
 
+    generate_started_at = time.time()
     generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
     if generate_result.returncode != 0:
         _mark_step(
@@ -86,32 +158,46 @@
             f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
         )
         return 1
-    if not TEMP_TWEET.exists():
-        _mark_step(status, "generate_content", False, "temp_tweet.txt was not created")
+    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")
+
+    try:
+        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
+    except Exception as exc:
+        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
         return 1
-    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
-    if not tweet_text:
-        _mark_step(status, "generate_content", False, "temp_tweet.txt is empty after generation")
+    if not payload_ok:
+        _mark_step(status, "validate_payload", False, payload_details)
         return 1
-    _mark_step(status, "generate_content", True, f"Generated tweet content ({len(tweet_text)} chars)")
+    _mark_step(status, "validate_payload", True, payload_details)
 
-    before_log = _posted_log_tail()
-    post_result = _run_command(["python", str(POST_SCRIPT)])
-    if post_result.returncode != 0:
+    try:
+        status_code, response_payload = _request_json(
+            API_POST_URL,
+            {
+                "text": tweet_text,
+                "trigger": "recurring_summary_returns_every_4_hours",
+            },
+        )
+    except Exception as exc:
         _mark_step(
             status,
             "submit_post",
             False,
-            f"Poster failed with code {post_result.returncode}: {post_result.stdout}\n{post_result.stderr}",
+            f"POST {API_POST_URL} failed: {exc}",
         )
         return 1
-    _mark_step(status, "submit_post", True, post_result.stdout.strip() or "Poster returned success")
 
-    after_log = _posted_log_tail()
-    if after_log == before_log:
-        _mark_step(status, "verify_audit_log", False, "posted_tweets.log did not gain a fresh entry")
+    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload)
+
+    if status_code != 200 or not response_payload.get("success"):
+        _mark_step(
+            status,
+            "submit_post",
+            False,
+            f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}",
+        )
         return 1
-    _mark_step(status, "verify_audit_log", True, "posted_tweets.log gained a fresh entry for this run")
+    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
 
     status["final_status"] = "success"
     _write_status(status)
diff --git a/breakout/fs/tests/test_run_twitter_canonical_workflow.py b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
new file mode 100644
index 0000000000000000000000000000000000000000..ff2f3933df6ea5e6f9ece41905b2198788a2c8de
--- /dev/null
+++ b/breakout/fs/tests/test_run_twitter_canonical_workflow.py
@@ -0,0 +1,74 @@
+import json
+import shutil
+import sys
+import unittest
+from pathlib import Path
+from unittest.mock import patch
+
+
+FS_DIR = Path(__file__).resolve().parents[1]
+if str(FS_DIR) not in sys.path:
+    sys.path.insert(0, str(FS_DIR))
+
+import run_twitter_canonical_workflow as workflow  # noqa: E402
+
+
+class RunTwitterCanonicalWorkflowTests(unittest.TestCase):
+    def make_case_root(self, case_name: str) -> Path:
+        root = FS_DIR / "tests" / "_tmp" / case_name
+        shutil.rmtree(root, ignore_errors=True)
+        root.mkdir(parents=True, exist_ok=True)
+        return root
+
+    def test_validate_payload_accepts_matching_generated_payload(self) -> None:
+        root = self.make_case_root("validate_payload_accepts")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        tweet_text = "Update at 2026-04-03 00:00\n\nToday\n1. SI 10"
+        temp_tweet.write_text(tweet_text + "\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": tweet_text}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertTrue(ok)
+        self.assertIn("Validated payload", details)
+        self.assertEqual(loaded_tweet, tweet_text)
+
+    def test_validate_payload_rejects_mismatch(self) -> None:
+        root = self.make_case_root("validate_payload_rejects")
+        temp_tweet = root / "temp_tweet.txt"
+        package_root = root / "json" / "live" / "social_posting_package" / "2026-04-03"
+        package_root.mkdir(parents=True, exist_ok=True)
+
+        temp_tweet.write_text("actual tweet\n", encoding="utf-8")
+        (package_root / "top5_weekly_posting_package.json").write_text(
+            json.dumps({"consolidated_twitter_post": "different tweet"}),
+            encoding="utf-8",
+        )
+
+        with (
+            patch.object(workflow, "TEMP_TWEET", temp_tweet),
+            patch.object(workflow, "PACKAGE_ROOT", root / "json" / "live" / "social_posting_package"),
+        ):
+            ok, details, loaded_tweet = workflow._validate_payload("2026-04-03", temp_tweet.stat().st_mtime)
+
+        self.assertFalse(ok)
+        self.assertIn("does not match", details)
+        self.assertEqual(loaded_tweet, "actual tweet")
+
+    @classmethod
+    def tearDownClass(cls) -> None:
+        shutil.rmtree(FS_DIR / "tests" / "_tmp", ignore_errors=True)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/skills/twitter-canonical-posting/SKILL.md b/skills/twitter-canonical-posting/SKILL.md
index 8aa01c0fd3da079ff35d52016d0aeec56430c9ac..9956659ef0c3be6ba09658a8843448940f76d83a
--- a/skills/twitter-canonical-posting/SKILL.md
+++ b/skills/twitter-canonical-posting/SKILL.md
@@ -21,11 +21,12 @@
 
 ## 3. Background Posting Workflow
 Use a strict gated workflow for scheduled updates. Every step depends on the previous step succeeding:
-1. **Verify Login First:** Confirm the saved session is authenticated before attempting any post.
+1. **Verify Local API First:** Confirm `GET http://localhost:5000/api/health` returns `{"status":"ok"}` before attempting any post.
 2. **Refresh Data:** Run `generate_posting_package.py --date YYYY-MM-DD` to update `temp_tweet.txt`.
-3. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
-4. **Posting Internals:** The workflow delegates to `run_twitter_post_v3.py`, which uses `Control+Enter` to submit the tweet and now refuses to log success unless post-confirmation checks pass.
-5. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
+3. **Validate Prepared Payload:** Confirm `temp_tweet.txt` is non-empty, matches the generated `consolidated_twitter_post`, and remains within X length limits.
+4. **Execute Gated Workflow:** `python run_twitter_canonical_workflow.py YYYY-MM-DD`
+5. **Posting Internals:** The workflow submits the prepared text to `POST /api/social/x_api_post` and writes the exact live response to `TradeApps/breakout/fs/twitter_x_api_post_response.json`.
+6. **Failure Rule:** If any step is unverified or ambiguous, the whole run fails and must not be marked complete.
 
 ## 4. Troubleshooting
 - **Locked Profile:** If you see "Profile in use," run `taskkill /F /IM chrome.exe`.
@@ -34,6 +35,6 @@
 
 ## 5. Verification
 - **Workflow Status:** Check `TradeApps/breakout/fs/twitter_workflow_status.json` for per-step gated status.
-- **Post Status:** Check `TradeApps/breakout/fs/twitter_post_status.json` for login, submit, and publication checks inside the poster.
-- **Logs:** Check `TradeApps/breakout/fs/posted_tweets.log` for a timestamped audit trail, but only treat it as valid when the gated workflow returns success.
-- **Screenshots:** Use `twitter_login_check.png`, `twitter_post_success.png`, and `twitter_post_error.png` as evidence for login, success confirmation, and failure diagnostics.
+- **Route Response:** Check `TradeApps/breakout/fs/twitter_x_api_post_response.json` for the exact HTTP status and X API route payload used by the scheduled run.
+- **Social Status:** Check `GET http://localhost:5000/api/social/status` for postability and recent post history when diagnosing blockers such as rate limits.
+- **Browser Fallback:** If the X API path is unavailable and the task explicitly requires browser posting, fall back to the login and posting scripts above and record that deviation clearly.
diff --git a/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md b/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
index bb25f91e955080811ce731ee2883b6813bf2ec2f..a7af9eed926646b8a2a562d92766874fc3f0ad93
--- a/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
+++ b/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md
@@ -61,109 +61,78 @@
 
 
 
-## Plan
-
-
-
-- [ ] 1. Regenerate the latest summary returns payload for the current run window.
-
-  - [ ] Test: `generate_posting_package.py --date YYYY-MM-DD` completes successfully and refreshes `temp_tweet.txt`.
-
-  - Evidence:
-
-
-
-- [ ] 2. Validate the prepared post body without inventing unsupported figures.
-
-  - [ ] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
-
-  - Evidence:
-
-
-
-- [ ] 3. Submit the prepared payload through the X API route.
-
-  - [ ] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.
-
-  - Evidence:
-
-
-
-## Evidence
-
-
-
-Objective-Delivery-Coverage: 0%
-
-Auto-Acceptance: false
-
-- Evidence-Type: file_output
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.
-
-  - Status: planned
-
-- Evidence-Type: route_output
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Proves the X API posting attempt outcome for this run.
-
-  - Status: planned
-
-- Evidence-Type: manual_verification
-
-  - Artifact: not_applicable
-
-  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.
-
-  - Status: planned
-
-
-
-## Implementation Log
-
-
-
-- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
-
-
-
-## Changes Made
-
-
-
-- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
-
-
-
-## Validation
-
-
-
-- Pending execution.
-
-
-
-## Risks/Notes
-
-
-
-- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
-
-- Use local data only; do not invent returns or write new market figures without a source artifact.
-
-- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
-
+## Plan
+
+- [x] 1. Regenerate the latest summary returns payload for the current run window.
+  - [x] Test: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py --date 2026-04-03` completes successfully and refreshes `temp_tweet.txt`.
+  - Evidence: `temp_tweet.txt` last-write time moved to `2026-04-03 01:04:42 +01:00`, and the dated package outputs were regenerated under `TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\`.
+
+- [x] 2. Validate the prepared post body without inventing unsupported figures.
+  - [x] Test: Confirm `temp_tweet.txt` is non-empty, was rewritten by the current generator run, matches the current `consolidated_twitter_post`, and remains within X posting constraints.
+  - Evidence: `twitter_workflow_status.json` recorded `Validated payload (233 chars)` and confirmed `temp_tweet.txt` matches `json\live\social_posting_package\2026-04-03\top5_weekly_posting_package.json`.
+
+- [x] 3. Submit the prepared payload through the X API route.
+  - [x] Test: `POST /api/social/x_api_post` returns either a success response with a tweet ID or a concrete API/runtime blocker.
+  - Evidence: `twitter_x_api_post_response.json` captured HTTP `200` with `{"message":"Tweet posted successfully","success":true,"tweet_id":"2039856634994852247"}` for trigger `recurring_summary_returns_every_4_hours`.
 
 
-## Completion Status
-
-
-
-- State: TODO
-
-- Timestamp:
-
+## Evidence
+
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\temp_tweet.txt`
+  - Objective-Proved: Proves which regenerated payload file was used for the recurring X post run.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\fs\twitter_x_api_post_response.json`
+  - Objective-Proved: Proves the X API posting attempt outcome for this run.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: Pending operator verification request for live tweet ID `2039856634994852247` and workflow artefacts `twitter_workflow_status.json` plus `twitter_x_api_post_response.json`
+  - Objective-Proved: Allows operator confirmation that the regenerated summary payload was posted or correctly blocked with an exact route response.
+  - Status: planned
+
+## Implementation Log
+
+- 2026-04-02 23:36:18 Europe/London: Recurring task definition replaced to combine payload generation with X API route posting every 4 hours.
+- 2026-04-03 01:01 Europe/London: Read `skills/workstream-task-lifecycle/` and the required `skills/twitter-canonical-posting/` skill, then inspected the existing workflow script and X API route implementation.
+- 2026-04-03 01:03 Europe/London: Updated `run_twitter_canonical_workflow.py` to verify local API health, regenerate the posting package, validate `temp_tweet.txt` against `consolidated_twitter_post`, submit via `POST /api/social/x_api_post`, and persist the exact route response to `twitter_x_api_post_response.json`.
+- 2026-04-03 01:03 Europe/London: Updated `skills/twitter-canonical-posting/SKILL.md` so the documented scheduled workflow matches the X API route path instead of the browser posting path.
+- 2026-04-03 01:04 Europe/London: Added workflow unit coverage in `tests/test_run_twitter_canonical_workflow.py` for matching and mismatched payload validation.
+- 2026-04-03 01:04 Europe/London: Executed `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`; the run succeeded and posted tweet ID `2039856634994852247`.
+
+## Changes Made
+
+- Replaced the prior browser-based recurring posting definition with a combined payload-generation plus X API posting workflow.
+- Updated `TradeApps\breakout\fs\run_twitter_canonical_workflow.py` to use the local X API route as the posting gate and to capture the exact HTTP response in `twitter_x_api_post_response.json`.
+- Updated `skills\twitter-canonical-posting\SKILL.md` so the documented canonical workflow matches the implemented route-based posting path.
+- Added `TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py` to cover payload-validation behavior.
+
+## Validation
+
+- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/health`
+  - Result: `{"status":"ok","ts":"2026-04-03T00:02:26.293168"}`
+- `Invoke-WebRequest -UseBasicParsing http://localhost:5000/api/social/status`
+  - Result: `api_enabled=true`, `can_post=true`, `reason="OK"` before the run.
+- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
+  - Result: passed with no output.
+- `python -m unittest C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_social_publisher.py C:\Users\edebe\eds\TradeApps\breakout\fs\tests\test_run_twitter_canonical_workflow.py`
+  - Result: `Ran 7 tests in 0.126s` and `OK`.
+- `python C:\Users\edebe\eds\TradeApps\breakout\fs\run_twitter_canonical_workflow.py 2026-04-03`
+  - Result: generated `temp_tweet.txt`, validated a `233`-character payload, and recorded HTTP `200` with tweet ID `2039856634994852247` in `twitter_x_api_post_response.json`.
+- User verification requested in assistant final response for:
+  - Confirm the live post for tweet ID `2039856634994852247` is acceptable.
+  - Confirm the route-based recurring workflow and captured artefacts are the expected behavior.
+
+## Risks/Notes
+
+- If the local API server is not reachable on `localhost:5000`, stop and record the concrete connectivity blocker.
+- Use local data only; do not invent returns or write new market figures without a source artifact.
+- After successful completion, the Kanban scheduler should spawn the next occurrence 4 hours later.
+- This task remains in `200_inprogress` until operator verification outcome is captured per the lifecycle completion gate.
+
+## Completion Status
+
+- State: Awaiting user verification
+- Timestamp: 2026-04-03 01:05:49 +01:00

tokens used
180,363
Implemented the route-based recurring workflow and executed the `2026-04-03` run end to end. The workflow entrypoint at [run_twitter_canonical_workflow.py](C:/Users/edebe/eds/TradeApps/breakout/fs/run_twitter_canonical_workflow.py) now does API health check -> payload generation -> payload validation against the generated package -> `POST /api/social/x_api_post`, and it writes the exact live response to [twitter_x_api_post_response.json](C:/Users/edebe/eds/TradeApps/breakout/fs/twitter_x_api_post_response.json). I also aligned the shared skill in [SKILL.md](C:/Users/edebe/eds/skills/twitter-canonical-posting/SKILL.md) and added unit coverage in [test_run_twitter_canonical_workflow.py](C:/Users/edebe/eds/TradeApps/breakout/fs/tests/test_run_twitter_canonical_workflow.py).

Validation passed: `py_compile`, `python -m unittest ...` (`Ran 7 tests ... OK`), and the live workflow run. The run regenerated [temp_tweet.txt](C:/Users/edebe/eds/TradeApps/breakout/fs/temp_tweet.txt), validated a 233-character payload, and posted successfully through the route with tweet ID `2039856634994852247`. The status trail is in [twitter_workflow_status.json](C:/Users/edebe/eds/TradeApps/breakout/fs/twitter_workflow_status.json), and the lifecycle file was updated at [20260403_010000_breakout_twitter_summary_returns_every_4_hours.md](C:/Users/edebe/eds/workstream/200_inprogress/codex/20260403_010000_breakout_twitter_summary_returns_every_4_hours.md).

Per the lifecycle rules, I left the task in `Awaiting user verification`. Verify these two points and reply pass/fail:
1. The live post for tweet ID `2039856634994852247` is the expected content.
2. The new route-based recurring workflow and captured artefacts are the expected behavior.
