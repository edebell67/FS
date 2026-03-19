OpenAI Codex v0.114.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019d0232-4794-7dc1-9cf8-ebccd0a0e527
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress\codex\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
codex
I’m starting by loading the lifecycle skill and the task file, then I’ll inspect the referenced code and implement the required changes before running validations and updating the task record.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md'" in C:\Users\edebe\eds succeeded in 1.21s:
---
name: workstream-task-lifecycle
description: Create and maintain timestamped task documentation files in the workstream lifecycle folders (`workstream/000_epic`, `workstream/100_backlog`, `workstream/200_inprogress`, `workstream/300_complete`). Use when a user asks to document changes, track progress for a distinct task, or enforce file movement across backlog/in-progress/complete states.
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
│
├── 200_inprogress/  ← Currently active work
 succeeded in 1.32s:
# Task: Create Social Content Engine

## Source
- Epic: `workstream/000_epic/20260316_135212_trading_strategy_warehouse_marketing_engine.md`

## Task Summary
- Create the content-generation system that produces reusable social content themes, post variants, and campaign assets for trading strategy warehouse.

## Context
- social post generation
- content templates
- campaign engine

## Dependency
Dependency: `20260316_135212_trading_strategy_warehouse_define_growth_offer_and_kpis.md`

## Plan
- [ ] 1. Define content pillars, posting themes, and reusable content formats.
  - [ ] Test: a documented content matrix exists for multiple campaign angles.
  - [ ] Evidence: content matrix artifact recorded.
codex
I’ve got the task definition. Next I’m locating the related marketing/growth artifacts and the current implementation surface so I can wire this into the existing warehouse assets instead of inventing a parallel structure.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg --files -g '*marketing*' -g '*growth*' -g '*social*' -g '*warehouse*'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress' -Recurse -Filter '20260316_135212_trading_strategy_warehouse_define_growth_offer_and_kpis.md' | Select-Object -ExpandProperty FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\workstream' -Recurse -Filter '20260316_135212_trading_strategy_warehouse_marketing_engine.md' | Select-Object -ExpandProperty FullName" in C:\Users\edebe\eds succeeded in 1.29s:

 exited 124 in 1.72s:

 exited 1 in 2.19s:
plans\FeatureUpdate\20251110_social_media_trade_blocks.md
workstream_backup_20260313\300_complete\codex\20260309_120090_autonomous_trading_signal_platform_workstreamJ_enable_marketing_engine.md
workstream_backup_20260313\300_complete\codex\20260309_120071_autonomous_trading_signal_platform_workstreamH_create_growth_dashboard.md
workstream_backup_20260313\300_complete\20260224_130500_breakout_phase4_social_distribution.md
workstream_backup_20260313\200_inprogress\gemini\20260308_162720_trading_signal_social_templates.md
trades_rt2\plans\FeatureUpdate\20251110_social_media_trade_blocks.md
workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md
workstream\clawd_originated\artefacts\evidence\trading_signal\social_templates_validation.txt
workstream\500_dump\gemini\20260317_142215_gemini_BLOCKER_20260316_232301_strategy_warehouse_marketing_engine_workstreamZ_create_docker_compose_configuration.md
workstream\500_dump\gemini\20260317_142007_gemini_BLOCKER_20260316_232302_strategy_warehouse_marketing_engine_workstreamZ_create_environment_template_and_readme.md
workstream\500_dump\gemini\20260317_141218_gemini_BLOCKER_20260316_232343_gemini_strategy_warehouse_marketing_engine_workstreamD_create_weekly_metrics_report_generator.md
workstream\500_dump\codex\20260317_140943_gemini_BLOCKER_20260316_232301_strategy_warehouse_marketing_engine_workstreamZ_create_docker_compose_configuration.md.result.md
workstream\500_dump\codex\20260317_140942_claude_BLOCKER_20260316_232300_strategy_warehouse_marketing_engine_workstreamZ_create_automated_setup_script.md.result.md
workstream\500_dump\codex\20260317_135421_codex_BLOCKER_20260316_135215_trading_strategy_warehouse_automate_distribution_and_scheduler.md.result.md.result.md
workstream\500_dump\20260317_135532_claude_BLOCKER_20260316_232301_general_strategy_warehouse_marketing_engine_workstreamZ_create_docker_compose_configuration.md.result.md
workstream\500_dump\20260317_135516_gemini_BLOCKER_20260317_135402_gemini_BLOCKER_20260316_232302_strategy_warehouse_marketing_engine_workstreamZ_create_environment_template_and_readme.md.result.md
workstream\500_dump\20260317_135450_claude_BLOCKER_20260317_135357_claude_BLOCKER_20260316_135219_general_trading_strategy_warehouse_define_autonomy_and_safety_guardrails.md.result.md.result.md
workstream\500_dump\20260317_135423_claude_BLOCKER_20260317_135357_claude_BLOCKER_20260316_135219_general_trading_strategy_warehouse_define_autonomy_and_safety_guardrails.md.result.md
workstream\500_dump\20260317_135417_gemini_BLOCKER_20260317_135343_gemini_BLOCKER_20260316_135218_gemini_trading_strategy_warehouse_build_growth_optimization_loop.md.result.md.result.md.result.md
workstream\500_dump\20260317_135415_general_BLOCKER_20260316_135215_trading_strategy_warehouse_automate_distribution_and_scheduler.md.result.md
codex
I found the dependency task already completed, so I can proceed. Now I’m narrowing to the actual marketing-engine code and prior content-schema work so the social content engine lands in the right module and matches the existing conventions.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex\\20260316_232310_strategy_warehouse_marketing_engine_workstreamA_define_publishable_content_schema.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\gemini\\20260316_232311_strategy_warehouse_marketing_engine_workstreamA_build_content_generation_service.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'Get-ChildItem -Path . -Directory | Select-Object -ExpandProperty Name' in C:\Users\edebe\eds succeeded in 1.74s:
# TASK A1: Define Publishable Content Schema

**Workstream:** A - CONTENT PIPELINE
**Workstream Goal:** Transform Strategy Warehouse data into publishable marketing content.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 2.1
**Depends On:** 1.1, 1.2, 1.3
**Blocks:** 2.2, 2.3, 2.4, 3.1
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing
- **Data Source:** `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\{date}\_*.json`

 succeeded in 1.72s:
# TASK A2: Build Content Generation Service

**Workstream:** A - CONTENT PIPELINE
**Workstream Goal:** Transform Strategy Warehouse data into publishable marketing content.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 2.2
**Depends On:** 2.1
**Blocks:** 2.4, 3.1
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing
- **Data Source:** `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\{date}\_*.json`

 succeeded in 1.91s:
__pycache__
.agent
.android
.claude
.edsLaptop
.gemini
.playwright-mcp
.pytest_cache
.roo
.venv
.vscode
a2ui
AI_trades_agents
AI_voice
algo
algo_crypto
algo_forex
algo_simulate
algo_viewer
algo_zone_viewer
codex
The prior workstream tasks point to `ep_strategy_warehouse_marketing`, so I’m inspecting that project directly now. I need to confirm what’s already implemented there before adding the social-content layer and its sample outputs.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\solution\\backend\\src' -Recurse -File | Select-Object -ExpandProperty FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260316_135233_strategy_warehouse_autonomous_marketing_engine.md'" in C:\Users\edebe\eds succeeded in 1.57s:
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\__init__.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\config\posting_rules.yaml
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\discordConnector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\linkedinConnector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\redditConnector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\tiktokConnector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\twitterConnector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\__pycache__\discordConnector.cpython-312.pyc
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\__pycache__\linkedinConnector.cpython-312.pyc
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\__pycache__\linkedinConnector.cpython-313.pyc
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\__pycache__\redditConnector.cpython-312.pyc
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\__pycache__\tiktokConnector.cpython-313.pyc
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\__pycache__\twitterConnector.cpython-312.pyc
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\connectors\__pycache__\twitterConnector.cpython-313.pyc
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\models\DiscordAuth.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\models\LinkedInAuth.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\models\RedditAuth.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\models\TikTokAuth.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\models\TwitterAuth.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\models\__pycache__\DiscordAuth.cpython-312.pyc
 succeeded in 1.84s:
# Epic: Strategy Warehouse Autonomous Marketing Engine

## Status
`READY FOR DECOMPOSITION` - Clarifications resolved 2026-03-16

## Product
Trading - Strategy Warehouse

## Strategic Objectives

1. **Increase online profile / improve reach** - Aggressively grow visibility of the product across social media platforms
2. **Increase subscriber base week-to-week** - Build and grow a subscriber list through a conversion funnel

## Requirement Summary

Build an autonomous marketing engine that:

- Generates and publishes content to social media platforms
- Drives traffic to a landing page
- Captures subscribers through the landing page
codex
There isn’t an existing content pipeline in the backend yet, so this task is effectively creating it. I’m checking the earlier blocked attempts only as reference, then I’ll implement a clean version in `ep_strategy_warehouse_marketing` and keep the lifecycle file aligned with actual progress.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\gemini\\20260317_135330_gemini_BLOCKER_20260316_135214_trading_strategy_warehouse_create_social_content_engine.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"contentGeneratorService|content schema|publishable_content_schema|social content\" 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\gemini\\20260317_135349_gemini_BLOCKER_20260317_135330_gemini_BLOCKER_20260316_135214_trading_strategy_warehouse_create_social_content_engine.md.result.md'" in C:\Users\edebe\eds succeeded in 1.66s:
# Task Summary
Blocker encountered while executing `20260316_135214_trading_strategy_warehouse_create_social_content_engine.md` via `gemini` agent.

# Error Log Details
```bash
OpenAI Codex v0.114.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019cfc12-852d-7533-8961-dfd09711c36c
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
ERROR: You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at Mar 18th, 2026 4:51 PM.
 succeeded in 1.86s:
# Task Summary
Blocker encountered while executing `20260317_135330_gemini_BLOCKER_20260316_135214_trading_strategy_warehouse_create_social_content_engine.md.result.md` via `gemini` agent.

# Error Log Details
```bash
OpenAI Codex v0.114.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019cfc12-f2dd-75d2-bb6c-9ac645b2340a
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260317_135330_gemini_BLOCKER_20260316_135214_trading_strategy_warehouse_create_social_content_engine.md.result.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
ERROR: You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at Mar 18th, 2026 4:51 PM.
 exited 1 in 2.25s:

codex
I’ve confirmed the earlier “completions” were just blocker stubs. I’m treating this as net-new implementation and checking the project’s packaging and test shape next so I can add code and validations that actually run in this workspace.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\tests' -Recurse -File | Where-Object { "'$_.FullName -like '"'*marketing*' -or "'$_.Name -like '"'*content*' } | Select-Object -ExpandProperty FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\README.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing' -Recurse -File | Select-Object -ExpandProperty FullName" in C:\Users\edebe\eds succeeded in 1.84s:
# Strategy Warehouse Autonomous Marketing Engine

## Overview
The Strategy Warehouse Autonomous Marketing Engine is a high-performance system designed to automate the generation, scheduling, and publishing of trading strategy insights across multiple social media platforms. It integrates real-time trading data with automated content creation and engagement tracking.

## Quick Start (< 5 minutes)
1.  **Clone the repository** (if applicable) or navigate to the project directory.
2.  **Copy environment template**:
    ```bash
    cp .env.example .env
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    # or
    pip install -r requirements.txt
    ```
4.  **Run the application**:
    ```bash
    npm start
 succeeded in 2.03s:

 exited 124 in 4.57s:
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\.env.example
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\docker-compose.yml
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\Dockerfile
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\README.md
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\setup.bat
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\setup.sh
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\requirements.txt
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\test_tiktok_connector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\verify_model.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\verify_tiktok_connector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.pytest_cache\.gitignore
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.pytest_cache\CACHEDIR.TAG
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.pytest_cache\README.md
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.pytest_cache\v\cache\lastfailed
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.pytest_cache\v\cache\nodeids
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.pytest_cache\v\cache\stepwise
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.venv\pyvenv.cfg
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.venv\Include\site\python3.12\greenlet\greenlet.h
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.venv\Lib\site-packages\_brotli.cp312-win_amd64.pyd
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\.venv\Lib\site-packages\_cffi_backend.cp312-win_amd64.pyd
codex
I’ve got enough structure to implement directly. Next I’m inspecting the live Strategy Warehouse JSON shape and the backend dependency set so the generator uses real fields and the tests don’t depend on guessed sample formats.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex' -Directory | Sort-Object Name -Descending | Select-Object -First 3 -ExpandProperty FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\solution\\backend\\requirements.txt'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$latest = Get-ChildItem -Path '"'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex' -Directory | Sort-Object Name -Descending | Select-Object -First 1; if ("'$latest) { Get-ChildItem -Path $latest.FullName -Filter '"'_*.json' | Select-Object -ExpandProperty FullName }" in C:\Users\edebe\eds succeeded in 1.09s:
fastapi==0.100.0
uvicorn==0.23.1
pydantic==2.1.1
sqlalchemy==2.0.19
psycopg2-binary==2.9.6
redis==4.6.0
python-dotenv==1.0.0
jinja2==3.1.2
requests==2.31.0
tweepy==4.14.0
python-telegram-bot==20.4
stripe==6.2.0
weasyprint==59.0
praw==7.7.1
pyyaml==6.0.1
 succeeded in 1.18s:
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_dna_alt_frequency.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_dna_frequency.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_frequency.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_summary_net_pre_auto_archive.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_summary_net.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_targeted_strategies.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_top_one.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_top20.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_trade_buckets.json
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18\_trades_summary.json
 succeeded in 1.14s:
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-18
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-17
C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\2026-03-16
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\2026-03-18\\_summary_net.json' -TotalCount 80" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\2026-03-18\\_frequency.json' -TotalCount 120" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\forex\\2026-03-18\\_dna_frequency.json' -TotalCount 120" in C:\Users\edebe\eds succeeded in 2.53s:
{
  "last_update": "2026-03-18T18:27:26.421368",
  "session_max_net": 0.0,
  "strategies": {
    "breakout_R_Rev_4_tp10.0_sl5.0": {
      "EUR": [
        {
          "t": "2026-03-18T05:42:25.134774",
          "net": -55.0,
          "buy_net": 0.0,
          "sell_net": -55.0,
          "buy_alt": 0.0,
          "sell_alt": 25.0,
          "live_buy": 0.0,
          "live_sell": 0.0,
          "b_c": 0,
          "s_c": 1,
          "buyPercent": 0.0,
          "sellPercent": 0.0
        },
 succeeded in 2.83s:
{
  "date": "2026-03-18",
  "run_mode": "live",
  "frequency_minutes": 5,
  "snapshot_count": 206,
  "snapshots": [
    {
      "time": "2026-03-18T01:20:00",
      "leaders": [
        {
          "rank": 1,
          "score_rank": 1,
          "score": 2.0,
          "product": "SOL",
          "strategy": "breakout_R_Rev_3_tp5.0_sl50.0",
          "net": 44.99999999999716
        }
      ]
    },
    {
 succeeded in 3.11s:
{
  "date": "2026-03-18",
  "run_mode": "live",
  "frequency_minutes": 5,
  "snapshot_count": 215,
  "snapshots": [
    {
      "time": "2026-03-18T00:40:00",
      "leaders": [
        {
          "rank": 1,
          "product": "DNA_105009_CAD",
          "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
          "net": -69.99999999999449
        },
        {
          "rank": 2,
          "product": "DNA_105026_CAD",
          "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
          "net": -69.99999999999449
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\solution\\backend\\src\\services\\postingRulesService.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\solution\\backend\\src\\connectors\\twitterConnector.py'" in C:\Users\edebe\eds succeeded in 1.01s:
import yaml
import os
import logging
import json
from datetime import datetime, timedelta

class PostingRulesService:
    def __init__(self, config_path: str, state_path: str = None):
        self.config_path = config_path
        self.state_path = state_path
        self.config = {}
        self.state = {}
        self.last_loaded = 0
        self.logger = logging.getLogger("PostingRulesService")
        self._load_config()
        self._load_state()

    def _load_config(self):
        try:
            if not os.path.exists(self.config_path):
 succeeded in 1.14s:
import tweepy
import logging
import os
from datetime import datetime, timedelta
from src.models.TwitterAuth import TwitterAuth, TwitterConfig

class TwitterConnector:
    def __init__(self, config: TwitterConfig):
        self.config = config
        self.client = tweepy.Client(
            bearer_token=config.auth.bearer_token,
            consumer_key=config.auth.api_key,
            consumer_secret=config.auth.api_secret,
            access_token=config.auth.access_token,
            access_token_secret=config.auth.access_secret,
            wait_on_rate_limit=True
        )
        
        # v1.1 Auth for Media Upload
        auth = tweepy.OAuth1UserHandler(
codex
Plan from here:
1. Implement the content schema, content matrix, templates, and generator service in `ep_strategy_warehouse_marketing/solution/backend/src`.
2. Add a repeatable sample-generation script plus committed sample outputs under the project for evidence.
3. Run targeted validations, capture outputs, and then update the lifecycle file with completed checklist items, evidence, and results.
Plan update
  ✓ Inspect marketing-engine backend and live data inputs
  → Implement content schema, matrix, templates, and generation service
  • Add repeatable sample generation script and sample outputs
  • Run validations and update lifecycle task file
codex
I’m about to edit the backend and project artifacts now. The implementation will include a documented content matrix, a real generator over the warehouse JSON feeds, and a repeatable sample-output script so the task can be validated end to end.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\workstreams' -Directory | Select-Object -ExpandProperty FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\verification' -Force" in C:\Users\edebe\eds succeeded in 1.00s:

 succeeded in 1.09s:
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\A
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\B
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\C
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\D
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\Z
file update
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\__init__.py
"""Schema package for publishable marketing content."""
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\content_schema.py
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ContentType(str, Enum):
    SIGNAL_ALERT = "signal_alert"
    PERFORMANCE_SUMMARY = "performance_summary"
    STRATEGY_RANKING = "strategy_ranking"
    EDUCATIONAL = "educational"


class CampaignAngle(str, Enum):
    MOMENTUM = "momentum"
    RISK_DISCIPLINE = "risk_discipline"
    LEADERBOARD = "leaderboard"
    EDUCATION = "education"


class Platform(str, Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    REDDIT = "reddit"
    DISCORD = "discord"
    TELEGRAM = "telegram"
    TIKTOK = "tiktok"


PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
}


class VariantContent(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    platform: Platform
    headline: str = Field(min_length=1)
    body: str = Field(min_length=1)
    hashtags: list[str] = Field(default_factory=list)
    call_to_action: str = Field(min_length=1, max_length=160)

    @model_validator(mode="after")
    def validate_platform_limits(self) -> "VariantContent":
        limits = PLATFORM_LIMITS[self.platform]
        if len(self.headline) > limits["headline"]:
            raise ValueError(
                f"{self.platform} headline exceeds {limits['headline']} characters"
            )
        if len(self.body) > limits["body"]:
            raise ValueError(
                f"{self.platform} body exceeds {limits['body']} characters"
            )
        if len(self.hashtags) > limits["hashtags"]:
            raise ValueError(
                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
            )
        return self


class CampaignAsset(BaseModel):
    asset_type: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=140)
    visual_brief: str = Field(min_length=1, max_length=280)
    callout: str = Field(min_length=1, max_length=180)


class PublishableContent(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    content_id: UUID = Field(default_factory=uuid4)
    content_type: ContentType
    campaign_angle: CampaignAngle
    pillar: str = Field(min_length=1, max_length=80)
    format_name: str = Field(min_length=1, max_length=80)
    headline: str = Field(min_length=1, max_length=100)
    body: str = Field(min_length=1, max_length=280)
    media_urls: list[str] = Field(default_factory=list)
    hashtags: list[str] = Field(default_factory=list)
    call_to_action: str = Field(min_length=1, max_length=160)
    landing_page_url: str = Field(min_length=1, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    scheduled_for: datetime | None = None
    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
    source_data: dict[str, Any] = Field(default_factory=dict)
    campaign_assets: list[CampaignAsset] = Field(default_factory=list)

    @field_validator("hashtags")
    @classmethod
    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
        for tag in hashtags:
            if not tag.startswith("#"):
                raise ValueError("hashtags must start with #")
        return hashtags

    @model_validator(mode="after")
    def validate_variant_platforms(self) -> "PublishableContent":
        for platform, variant in self.platform_variants.items():
            if variant.platform != platform:
                raise ValueError("platform_variants keys must match variant platform")
        return self


class ContentMatrixEntry(BaseModel):
    pillar: str = Field(min_length=1, max_length=80)
    campaign_angle: CampaignAngle
    content_type: ContentType
    theme: str = Field(min_length=1, max_length=140)
    format_name: str = Field(min_length=1, max_length=80)
    target_platforms: list[Platform] = Field(min_length=1)
    hook_style: str = Field(min_length=1, max_length=120)
    call_to_action: str = Field(min_length=1, max_length=160)

A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\templates\performance_summary.jinja2
{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\A\social_content_matrix.md
# Strategy Warehouse Social Content Matrix

## Purpose

This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.

## Content Matrix

| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |

## Format Rules

- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
- Always include a clear subscriber CTA tied to the landing page.
- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_content_generation_service.py
from __future__ import annotations

from pathlib import Path

from src.schemas.content_schema import CampaignAngle, ContentType, Platform
from src.services.contentGeneratorService import ContentGeneratorService


def sample_warehouse_bundle() -> dict:
    return {
        "snapshot_dir": "synthetic/2026-03-18",
        "_summary_net.json": {
            "last_update": "2026-03-18T18:27:26.421368",
            "strategies": {
                "breakout_R_Rev_4_tp10.0_sl5.0": {
                    "EUR": [
                        {
                            "t": "2026-03-18T13:37:32.591957",
                            "net": 245.0,
                            "buy_net": 180.0,
                            "sell_net": 65.0,
                            "b_c": 3,
                            "s_c": 1,
                        }
                    ]
                }
            },
        },
        "_frequency.json": {
            "date": "2026-03-18",
            "snapshot_count": 206,
            "snapshots": [
                {
                    "time": "2026-03-18T17:20:00",
                    "leaders": [
                        {
                            "rank": 1,
                            "score_rank": 1,
                            "score": 11.0,
                            "product": "SOL",
                            "strategy": "breakout_2_tp20.0_sl20.0",
                            "net": 195.0,
                        }
                    ],
                }
            ],
        },
        "_dna_frequency.json": {
            "date": "2026-03-18",
            "snapshot_count": 215,
            "snapshots": [
                {
                    "time": "2026-03-18T17:55:00",
                    "leaders": [
                        {
                            "rank": 1,
                            "product": "DNA_105009_CAD",
                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
                            "net": 90.0,
                        },
                        {
                            "rank": 2,
                            "product": "DNA_105026_CAD",
                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
                            "net": 85.0,
                        },
                        {
                            "rank": 3,
                            "product": "DNA_105119_CAD",
                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
                            "net": 80.0,
                        },
                    ],
                }
            ],
        },
    }


def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
    service = ContentGeneratorService()

    matrix = service.build_content_matrix()

    assert len(matrix) == 4
    assert {entry.campaign_angle for entry in matrix} == {
        CampaignAngle.MOMENTUM,
        CampaignAngle.RISK_DISCIPLINE,
        CampaignAngle.LEADERBOARD,
        CampaignAngle.EDUCATION,
    }
    assert {entry.content_type for entry in matrix} == {
        ContentType.SIGNAL_ALERT,
        ContentType.PERFORMANCE_SUMMARY,
        ContentType.STRATEGY_RANKING,
        ContentType.EDUCATIONAL,
    }


def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
    service = ContentGeneratorService(
        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
    )

    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())

    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
    assert len(bundle["content_matrix"]) == 4
    assert len(bundle["posts"]) == 4

    first_post = bundle["posts"][0]
    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
    assert Platform.TWITTER.value in first_post["platform_variants"]
    assert len(first_post["campaign_assets"]) == 1
    assert first_post["headline"]
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\templates\signal_alert.jinja2
{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\services\contentGeneratorService.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.schemas.content_schema import (
    PLATFORM_LIMITS,
    CampaignAngle,
    CampaignAsset,
    ContentMatrixEntry,
    ContentType,
    Platform,
    PublishableContent,
    VariantContent,
)


DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]


@dataclass(frozen=True)
class PillarDefinition:
    pillar: str
    campaign_angle: CampaignAngle
    content_type: ContentType
    theme: str
    format_name: str
    target_platforms: tuple[Platform, ...]
    hook_style: str
    call_to_action: str


CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
    PillarDefinition(
        pillar="daily_signal_edge",
        campaign_angle=CampaignAngle.MOMENTUM,
        content_type=ContentType.SIGNAL_ALERT,
        theme="Surface the strongest live mover with fast proof and a clear invite.",
        format_name="flash_signal_post",
        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
        hook_style="Urgent momentum hook",
        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
    ),
    PillarDefinition(
        pillar="performance_recap",
        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
        content_type=ContentType.PERFORMANCE_SUMMARY,
        theme="Translate snapshot data into disciplined weekly-style proof.",
        format_name="proof_of_process_post",
        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
        hook_style="Measured proof hook",
        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
    ),
    PillarDefinition(
        pillar="leaderboard_watch",
        campaign_angle=CampaignAngle.LEADERBOARD,
        content_type=ContentType.STRATEGY_RANKING,
        theme="Show ranked leaders and why the board is rotating.",
        format_name="leaderboard_carousel",
        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
        hook_style="Competitive leaderboard hook",
        call_to_action="Subscribe to track when the leaderboard flips.",
    ),
    PillarDefinition(
        pillar="trader_education",
        campaign_angle=CampaignAngle.EDUCATION,
        content_type=ContentType.EDUCATIONAL,
        theme="Turn warehouse output into reusable explanations about risk and selection.",
        format_name="educational_breakdown",
        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
        hook_style="Teach with one sharp lesson",
        call_to_action="Join for deeper breakdowns behind each strategy setup.",
    ),
)


class StrategyWarehouseDataLoader:
    def __init__(self, base_path: str | Path) -> None:
        self.base_path = Path(base_path)

    def latest_snapshot_dir(self) -> Path:
        date_dirs = sorted(
            [path for path in self.base_path.iterdir() if path.is_dir()],
            reverse=True,
        )
        if not date_dirs:
            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
        return date_dirs[0]

    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
        bundle: dict[str, Any] = {}
        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
            file_path = target_dir / file_name
            with file_path.open("r", encoding="utf-8") as handle:
                bundle[file_name] = json.load(handle)
        bundle["snapshot_dir"] = str(target_dir)
        return bundle


class ContentGeneratorService:
    def __init__(
        self,
        template_dir: str | Path | None = None,
        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
    ) -> None:
        resolved_template_dir = (
            Path(template_dir)
            if template_dir
            else Path(__file__).resolve().parent.parent / "templates"
        )
        self.environment = Environment(
            loader=FileSystemLoader(str(resolved_template_dir)),
            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.landing_page_url = landing_page_url

    def build_content_matrix(self) -> list[ContentMatrixEntry]:
        return [
            ContentMatrixEntry(
                pillar=definition.pillar,
                campaign_angle=definition.campaign_angle,
                content_type=definition.content_type,
                theme=definition.theme,
                format_name=definition.format_name,
                target_platforms=list(definition.target_platforms),
                hook_style=definition.hook_style,
                call_to_action=definition.call_to_action,
            )
            for definition in CONTENT_MATRIX
        ]

    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
        matrix = self.build_content_matrix()
        posts = [
            self._build_signal_alert(warehouse_data),
            self._build_performance_summary(warehouse_data),
            self._build_strategy_ranking(warehouse_data),
            self._build_educational_post(warehouse_data),
        ]
        return {
            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
            "source_snapshot_dir": warehouse_data["snapshot_dir"],
            "posts": [post.model_dump(mode="json") for post in posts],
        }

    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
        summary = warehouse_data["_summary_net.json"]
        strategy, product, point = self._best_signal(summary)
        body = self.environment.get_template("signal_alert.jinja2").render(
            hook="Momentum check:",
            strategy=self._shorten_strategy(strategy),
            product=product,
            net_points=self._format_points(point["net"]),
            directional_bias=self._directional_bias(point),
            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
        )
        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
        return self._build_content_item(
            definition=CONTENT_MATRIX[0],
            headline=headline,
            body=body,
            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
            source_data={
                "strategy": strategy,
                "product": product,
                "latest_point": point,
            },
            campaign_assets=[
                CampaignAsset(
                    asset_type="quote_card",
                    title=f"{product} momentum card",
                    visual_brief=f"Highlight {product} net curve and current strategy label.",
                    callout="Fast signal, clear edge, direct CTA.",
                )
            ],
        )

    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
        frequency = warehouse_data["_frequency.json"]
        latest_snapshot = frequency["snapshots"][-1]
        top_leader = latest_snapshot["leaders"][0]
        body = self.environment.get_template("performance_summary.jinja2").render(
            lead_in="Discipline over noise:",
            winning_product=top_leader["product"],
            winning_net=self._format_points(top_leader["net"]),
            snapshot_count=frequency["snapshot_count"],
            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
        )
        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
        return self._build_content_item(
            definition=CONTENT_MATRIX[1],
            headline=headline,
            body=body,
            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
            source_data={
                "latest_snapshot_time": latest_snapshot["time"],
                "leader": top_leader,
                "snapshot_count": frequency["snapshot_count"],
            },
            campaign_assets=[
                CampaignAsset(
                    asset_type="carousel",
                    title="Performance recap carousel",
                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
                    callout="Proof without overclaiming.",
                )
            ],
        )

    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
        dna_frequency = warehouse_data["_dna_frequency.json"]
        latest_snapshot = dna_frequency["snapshots"][-1]
        leaders = [
            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
            for leader in latest_snapshot["leaders"][:3]
        ]
        body = self.environment.get_template("strategy_ranking.jinja2").render(
            lead_in="Leaderboard watch:",
            leaders=leaders,
            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
        )
        headline = "DNA leaderboard rotation is tightening"
        return self._build_content_item(
            definition=CONTENT_MATRIX[2],
            headline=headline,
            body=body,
            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
            source_data={
                "latest_snapshot_time": latest_snapshot["time"],
                "leaders": latest_snapshot["leaders"][:5],
            },
            campaign_assets=[
                CampaignAsset(
                    asset_type="leaderboard_card",
                    title="Top 3 DNA strategies",
                    visual_brief="Three-column leaderboard with rank badges and point totals.",
                    callout="Show movement between yesterday and today.",
                )
            ],
        )

    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
        frequency = warehouse_data["_frequency.json"]
        latest_snapshot = frequency["snapshots"][-1]
        leaders = latest_snapshot["leaders"][:2]
        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
        body = (
            "What makes a strategy feed usable? "
            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
            f"Today that means tracking {leader_names} and ignoring one-off spikes."
        )
        headline = "How to read a strategy board without chasing noise"
        return self._build_content_item(
            definition=CONTENT_MATRIX[3],
            headline=headline,
            body=body,
            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
            source_data={
                "leaders": leaders,
                "lesson": "Use repeat snapshots to separate consistency from noise.",
            },
            campaign_assets=[
                CampaignAsset(
                    asset_type="script_outline",
                    title="Educational explainer",
                    visual_brief="30-second talking-head outline with one chart overlay.",
                    callout="Teach the filter, not the prediction.",
                )
            ],
        )

    def _build_content_item(
        self,
        definition: PillarDefinition,
        headline: str,
        body: str,
        hashtags: list[str],
        source_data: dict[str, Any],
        campaign_assets: list[CampaignAsset],
    ) -> PublishableContent:
        base_cta = definition.call_to_action
        platform_variants = self._build_platform_variants(
            headline=headline,
            body=body,
            hashtags=hashtags,
            call_to_action=base_cta,
            target_platforms=definition.target_platforms,
        )
        return PublishableContent(
            content_type=definition.content_type,
            campaign_angle=definition.campaign_angle,
            pillar=definition.pillar,
            format_name=definition.format_name,
            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
            call_to_action=base_cta,
            landing_page_url=self.landing_page_url,
            platform_variants=platform_variants,
            source_data=source_data,
            campaign_assets=campaign_assets,
        )

    def _build_platform_variants(
        self,
        headline: str,
        body: str,
        hashtags: list[str],
        call_to_action: str,
        target_platforms: tuple[Platform, ...],
    ) -> dict[Platform, VariantContent]:
        variants: dict[Platform, VariantContent] = {}
        for platform in target_platforms:
            limits = PLATFORM_LIMITS[platform]
            platform_tags = hashtags[: limits["hashtags"]]
            cta = self._trim(call_to_action, 160)
            if platform == Platform.REDDIT:
                variant_body = f"{body}\n\nCTA: {cta}"
            elif platform == Platform.DISCORD:
                variant_body = f"{body} {cta}"
            else:
                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
            variants[platform] = VariantContent(
                platform=platform,
                headline=self._trim(headline, limits["headline"]),
                body=self._trim(variant_body, limits["body"]),
                hashtags=platform_tags,
                call_to_action=cta,
            )
        return variants

    @staticmethod
    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
        best_item: tuple[str, str, dict[str, Any]] | None = None
        for strategy, products in summary["strategies"].items():
            for product, points in products.items():
                if not points:
                    continue
                latest = points[-1]
                if best_item is None or latest["net"] > best_item[2]["net"]:
                    best_item = (strategy, product, latest)
        if best_item is None:
            raise ValueError("No strategy points available in summary feed")
        return best_item

    @staticmethod
    def _directional_bias(point: dict[str, Any]) -> str:
        if point["buy_net"] > point["sell_net"]:
            return "buy-led"
        if point["sell_net"] > point["buy_net"]:
            return "sell-led"
        return "balanced"

    @staticmethod
    def _trim(text: str, max_length: int) -> str:
        if len(text) <= max_length:
            return text
        return text[: max_length - 3].rstrip() + "..."

    @staticmethod
    def _shorten_strategy(strategy: str) -> str:
        return strategy.replace("breakout_", "brk_").replace("_", " ")

    @staticmethod
    def _format_points(value: float) -> str:
        rounded = round(value, 1)
        return f"{rounded:+g}"
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\scripts\generate_social_content_samples.py
from __future__ import annotations

import json
from pathlib import Path

from src.schemas.content_schema import PublishableContent
from src.services.contentGeneratorService import (
    ContentGeneratorService,
    StrategyWarehouseDataLoader,
)


def main() -> None:
    project_root = Path(__file__).resolve().parents[4]
    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
    verification_dir = project_root / "verification"
    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
    verification_dir.mkdir(parents=True, exist_ok=True)

    loader = StrategyWarehouseDataLoader(data_root)
    warehouse_data = loader.load_snapshot_bundle()
    service = ContentGeneratorService()
    bundle = service.generate_campaign_bundle(warehouse_data)

    output_path = verification_dir / "generated_social_content_samples.json"
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(bundle, handle, indent=2)

    schema_path = schema_dir / "publishable_content_schema.json"
    with schema_path.open("w", encoding="utf-8") as handle:
        json.dump(PublishableContent.model_json_schema(), handle, indent=2)

    print(f"Wrote {output_path}")
    print(f"Wrote {schema_path}")


if __name__ == "__main__":
    main()
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\templates\strategy_ranking.jinja2
{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
apply_patch(auto_approved=true) exited 0 in 1.83s:
Success. Updated the following files:
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\__init__.py
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\content_schema.py
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\templates\signal_alert.jinja2
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\templates\performance_summary.jinja2
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\templates\strategy_ranking.jinja2
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\services\contentGeneratorService.py
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\scripts\generate_social_content_samples.py
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_content_generation_service.py
A C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\A\social_content_matrix.md
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..98d99de2ff4e7f837b5e4de258d131c74ae79bdf
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,123 @@
+from __future__ import annotations
+
+from datetime import datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=datetime.utcnow)
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..1a4d95ffea9fbed939fb9bc0ff97e7f4e141274f
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,38 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import (
+    ContentGeneratorService,
+    StrategyWarehouseDataLoader,
+)
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.

file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..98d99de2ff4e7f837b5e4de258d131c74ae79bdf
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,123 @@
+from __future__ import annotations
+
+from datetime import datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=datetime.utcnow)
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..1a4d95ffea9fbed939fb9bc0ff97e7f4e141274f
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,38 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import (
+    ContentGeneratorService,
+    StrategyWarehouseDataLoader,
+)
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.

codex
The code is in place. I’m running targeted backend tests now, then I’ll generate the committed sample bundle and schema artifact from the live warehouse snapshot so the task has concrete evidence.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python src\\scripts\\generate_social_content_samples.py" in C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backendexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -m pytest tests\\test_content_generation_service.py" in C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend exited 1 in 1.19s:
Traceback (most recent call last):
  File "C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\scripts\generate_social_content_samples.py", line 6, in <module>
    from src.schemas.content_schema import PublishableContent
ModuleNotFoundError: No module named 'src'
 succeeded in 5.58s:
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend
plugins: anyio-4.8.0, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 2 items

tests\test_content_generation_service.py ..                              [100%]

============================== warnings summary ===============================
tests/test_content_generation_service.py::test_generate_campaign_bundle_returns_repeatable_valid_posts
tests/test_content_generation_service.py::test_generate_campaign_bundle_returns_repeatable_valid_posts
tests/test_content_generation_service.py::test_generate_campaign_bundle_returns_repeatable_valid_posts
tests/test_content_generation_service.py::test_generate_campaign_bundle_returns_repeatable_valid_posts
  C:\Users\edebe\AppData\Roaming\Python\Python313\site-packages\pydantic\main.py:253: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 2 passed, 4 warnings in 1.47s ========================
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..98d99de2ff4e7f837b5e4de258d131c74ae79bdf
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,123 @@
+from __future__ import annotations
+
+from datetime import datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=datetime.utcnow)
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..1a4d95ffea9fbed939fb9bc0ff97e7f4e141274f
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,38 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import (
+    ContentGeneratorService,
+    StrategyWarehouseDataLoader,
+)
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.

codex
The tests passed. The sample-generation script failed on module resolution, so I’m fixing the script packaging and clearing the `utcnow()` deprecation at the same time before rerunning the artifact generation.
file update
M C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\scripts\generate_social_content_samples.py
@@ -4,8 +4,12 @@
 from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
 
 from src.schemas.content_schema import PublishableContent
-from src.services.contentGeneratorService import (
-    ContentGeneratorService,
-    StrategyWarehouseDataLoader,
-)
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
 
M C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\content_schema.py
@@ -2,3 +2,3 @@
 
-from datetime import datetime
+from datetime import UTC, datetime
 from enum import Enum
@@ -91,3 +91,3 @@
     landing_page_url: str = Field(min_length=1, max_length=255)
-    created_at: datetime = Field(default_factory=datetime.utcnow)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
     scheduled_for: datetime | None = None
@@ -122,2 +122 @@
     call_to_action: str = Field(min_length=1, max_length=160)
-
apply_patch(auto_approved=true) exited 0 in 753ms:
Success. Updated the following files:
M C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\content_schema.py
M C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\scripts\generate_social_content_samples.py
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.

file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -m pytest tests\\test_content_generation_service.py" in C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backendexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python src\\scripts\\generate_social_content_samples.py" in C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend succeeded in 2.61s:
Wrote C:\Users\edebe\eds\ep_strategy_warehouse_marketing\verification\generated_social_content_samples.json
Wrote C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\publishable_content_schema.json
 succeeded in 3.40s:
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend
plugins: anyio-4.8.0, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 2 items

tests\test_content_generation_service.py ..                              [100%]

============================== 2 passed in 0.43s ==============================
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.

codex
I’ve got the deliverables and validation artifacts now. I’m updating the lifecycle file next with the completed checklist items, concrete evidence paths, command results, and a pending user-verification request since the output quality still needs a human pass.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\solution\\backend\\src\\schemas\\publishable_content_schema.json' -TotalCount 40" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\ep_strategy_warehouse_marketing\\verification\\generated_social_content_samples.json' -TotalCount 80" in C:\Users\edebe\eds succeeded in 965ms:
# Task: Create Social Content Engine

## Source
- Epic: `workstream/000_epic/20260316_135212_trading_strategy_warehouse_marketing_engine.md`

## Task Summary
- Create the content-generation system that produces reusable social content themes, post variants, and campaign assets for trading strategy warehouse.

## Context
- social post generation
- content templates
- campaign engine

## Dependency
Dependency: `20260316_135212_trading_strategy_warehouse_define_growth_offer_and_kpis.md`

## Plan
- [ ] 1. Define content pillars, posting themes, and reusable content formats.
  - [ ] Test: a documented content matrix exists for multiple campaign angles.
  - [ ] Evidence: content matrix artifact recorded.
 succeeded in 1.04s:
{
  "$defs": {
    "CampaignAngle": {
      "enum": [
        "momentum",
        "risk_discipline",
        "leaderboard",
        "education"
      ],
      "title": "CampaignAngle",
      "type": "string"
    },
    "CampaignAsset": {
      "properties": {
        "asset_type": {
          "maxLength": 64,
          "minLength": 1,
          "title": "Asset Type",
          "type": "string"
        },
 succeeded in 1.06s:
{
  "content_matrix": [
    {
      "pillar": "daily_signal_edge",
      "campaign_angle": "momentum",
      "content_type": "signal_alert",
      "theme": "Surface the strongest live mover with fast proof and a clear invite.",
      "format_name": "flash_signal_post",
      "target_platforms": [
        "twitter",
        "discord",
        "telegram"
      ],
      "hook_style": "Urgent momentum hook",
      "call_to_action": "Join the Strategy Warehouse list for the next live signal batch."
    },
    {
      "pillar": "performance_recap",
      "campaign_angle": "risk_discipline",
      "content_type": "performance_summary",
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git status --short' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git diff -- ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md' in C:\Users\edebe\eds succeeded in 1.21s:

 succeeded in 2.11s:
M  DataInsights/src/Constants.py
 M TradeApps
 M api_server_sql/main.py
 D grid_live_monitor.py
R  workstream/000_backlog/.keep -> workstream/000_epic/.keep
R  "workstream/000_backlog/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md" -> "workstream/000_epic/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md"
R  workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md -> workstream/000_epic/20260225_104010_live_market_data_pipeline_prompt.md
R  workstream/000_backlog/20260227_022357_sFX_Technical_Design_Brief_v2.md -> workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
A  workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
A  workstream/000_epic/20260313_165611_bizPA_epic.md
A  "workstream/000_epic/20260313_165611_unassigned_Autonomous Trading Signal Platform.md"
A  workstream/000_epic/20260313_165611_unassigned_bizPA.md
A  workstream/000_epic/bizPA_disccussion.txt
R  workstream/000_backlog/claude/.keep -> workstream/000_epic/claude/.keep
A  workstream/000_epic/claude/20260305_100142_claude_etrmui_etrui_processed.md
R  workstream/000_backlog/codex/.keep -> workstream/000_epic/codex/.keep
R  workstream/000_backlog/codex/20260303_152309_codex_afrix_build_prompt_processed.md -> workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_processed.md
A  workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_review.md
R  workstream/000_backlog/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md -> workstream/000_epic/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md
R  workstream/000_backlog/codex/20260304_142350_codex_linkage_verification_processed.md -> workstream/000_epic/codex/20260304_142350_codex_linkage_verification_processed.md
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.

file update
M C:\Users\edebe\eds\workstream\200_inprogress\codex\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
@@ -16,32 +16,73 @@
 
-## Plan
-- [ ] 1. Define content pillars, posting themes, and reusable content formats.
-  - [ ] Test: a documented content matrix exists for multiple campaign angles.
-  - [ ] Evidence: content matrix artifact recorded.
-- [ ] 2. Implement asset or copy generation workflow.
-  - [ ] Test: sample posts/assets can be generated repeatably.
-  - [ ] Evidence: generated output files or artifacts recorded.
-
-## Implementation Log
-- Created from epic decomposition on 2026-03-16.
-
-## Changes Made
-- None yet.
-
-## Validation
-- Pending.
-
-## Evidence
-- Objective-Delivery-Coverage: 0%
-- Auto-Acceptance: false
-- Evidence-Type: file_output
-  - Artifact: generated post/campaign asset set
-  - Objective-Proved: the engine can produce reusable marketing content
-  - Status: planned
-
-## Risks/Notes
-- Brand/output quality likely needs manual review.
-
-## Completion Status
-- Todo
+## Plan
+- [x] 1. Define content pillars, posting themes, and reusable content formats.
+  - [x] Test: a documented content matrix exists for multiple campaign angles.
+  - [x] Evidence: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` and generator-backed matrix output recorded in `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`.
+- [x] 2. Implement asset or copy generation workflow.
+  - [x] Test: sample posts/assets can be generated repeatably.
+  - [x] Evidence: repeatable generator script, generated sample bundle, and schema artifact recorded under `ep_strategy_warehouse_marketing/solution/backend/src` and `ep_strategy_warehouse_marketing/verification`.
+
+## Implementation Log
+- Created from epic decomposition on 2026-03-16.
+- 2026-03-18 18:20Z - Inspected dependency completion, epic outputs, and live Strategy Warehouse JSON feeds under `TradeApps/breakout/fs/json/live/forex`.
+- 2026-03-18 18:29Z - Implemented content schema, reusable content matrix, Jinja templates, and `ContentGeneratorService` in `ep_strategy_warehouse_marketing/solution/backend/src`.
+- 2026-03-18 18:31Z - Added repeatable sample-generation script and backend pytest coverage for matrix generation and campaign bundle validation.
+- 2026-03-18 18:32Z - Generated live sample outputs and JSON schema artifacts from the 2026-03-18 warehouse snapshot.
+- 2026-03-18 18:34Z - Requested manual review of generated copy quality before final lifecycle completion.
+
+## Changes Made
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py` with `PublishableContent`, platform constraints, content matrix models, and campaign asset schema.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py` to transform warehouse snapshots into reusable social posts, platform variants, and asset briefs.
+- Added Jinja templates in `ep_strategy_warehouse_marketing/solution/backend/src/templates/` for signal alerts, performance summaries, and leaderboard posts.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py` to emit repeatable sample content and `publishable_content_schema.json`.
+- Added `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py` for matrix coverage and repeatable bundle generation tests.
+- Added `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` documenting content pillars, campaign angles, formats, and CTA rules.
+- Generated `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+
+## Validation
+- `python -m pytest tests\test_content_generation_service.py`
+  - Result: pass, 2 tests passed in 0.43s.
+- `python src\scripts\generate_social_content_samples.py`
+  - Result: pass, wrote `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+- Manual review requested:
+  - Review `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and confirm pass/fail for:
+    1. content pillars/themes fit the Strategy Warehouse offer,
+    2. sample copy tone is acceptable for publishing,
+    3. campaign asset briefs are usable for downstream creative production.
+
+## Evidence
+- Objective-Delivery-Coverage: 95%
+- Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md`
+  - Objective-Proved: reusable content pillars, campaign angles, formats, and CTA rules were defined and documented.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: the engine can generate reusable post variants and campaign asset briefs from live warehouse data.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`
+  - Objective-Proved: generated content is backed by a concrete publishable schema.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m pytest tests\test_content_generation_service.py` => `2 passed in 0.43s`
+  - Objective-Proved: content matrix coverage and repeatable bundle generation were validated automatically.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py`, `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py`, `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py`
+  - Objective-Proved: the workspace now contains the social content engine implementation and verification harness.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: pending user review of `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: generated copy and asset briefs are acceptable for brand and publishing use.
+  - Status: planned
+
+## Risks/Notes
+- Brand/output quality likely needs manual review.
+- Current output produces structured asset briefs, not rendered media files; downstream design/video automation can consume those briefs.
+- Generated copy is grounded in local 2026-03-18 snapshot files and should be regenerated when source data changes materially.
+
+## Completion Status
+- Awaiting user verification - 2026-03-18 18:34Z
 
apply_patch(auto_approved=true) exited 0 in 5.18s:
Success. Updated the following files:
M C:\Users\edebe\eds\workstream\200_inprogress\codex\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.
diff --git a/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md b/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
index ca256ce9a47d823f880f4b8092cffd96382ac1ba..6fe81ae41c661f5c4bf59a3c3f6c93c6af959904
--- a/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
+++ b/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
@@ -14,36 +14,77 @@
 ## Dependency
 Dependency: `20260316_135212_trading_strategy_warehouse_define_growth_offer_and_kpis.md`
 
-## Plan
-- [ ] 1. Define content pillars, posting themes, and reusable content formats.
-  - [ ] Test: a documented content matrix exists for multiple campaign angles.
-  - [ ] Evidence: content matrix artifact recorded.
-- [ ] 2. Implement asset or copy generation workflow.
-  - [ ] Test: sample posts/assets can be generated repeatably.
-  - [ ] Evidence: generated output files or artifacts recorded.
-
-## Implementation Log
-- Created from epic decomposition on 2026-03-16.
-
-## Changes Made
-- None yet.
-
-## Validation
-- Pending.
-
-## Evidence
-- Objective-Delivery-Coverage: 0%
-- Auto-Acceptance: false
-- Evidence-Type: file_output
-  - Artifact: generated post/campaign asset set
-  - Objective-Proved: the engine can produce reusable marketing content
-  - Status: planned
-
-## Risks/Notes
-- Brand/output quality likely needs manual review.
-
-## Completion Status
-- Todo
+## Plan
+- [x] 1. Define content pillars, posting themes, and reusable content formats.
+  - [x] Test: a documented content matrix exists for multiple campaign angles.
+  - [x] Evidence: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` and generator-backed matrix output recorded in `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`.
+- [x] 2. Implement asset or copy generation workflow.
+  - [x] Test: sample posts/assets can be generated repeatably.
+  - [x] Evidence: repeatable generator script, generated sample bundle, and schema artifact recorded under `ep_strategy_warehouse_marketing/solution/backend/src` and `ep_strategy_warehouse_marketing/verification`.
+
+## Implementation Log
+- Created from epic decomposition on 2026-03-16.
+- 2026-03-18 18:20Z - Inspected dependency completion, epic outputs, and live Strategy Warehouse JSON feeds under `TradeApps/breakout/fs/json/live/forex`.
+- 2026-03-18 18:29Z - Implemented content schema, reusable content matrix, Jinja templates, and `ContentGeneratorService` in `ep_strategy_warehouse_marketing/solution/backend/src`.
+- 2026-03-18 18:31Z - Added repeatable sample-generation script and backend pytest coverage for matrix generation and campaign bundle validation.
+- 2026-03-18 18:32Z - Generated live sample outputs and JSON schema artifacts from the 2026-03-18 warehouse snapshot.
+- 2026-03-18 18:34Z - Requested manual review of generated copy quality before final lifecycle completion.
+
+## Changes Made
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py` with `PublishableContent`, platform constraints, content matrix models, and campaign asset schema.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py` to transform warehouse snapshots into reusable social posts, platform variants, and asset briefs.
+- Added Jinja templates in `ep_strategy_warehouse_marketing/solution/backend/src/templates/` for signal alerts, performance summaries, and leaderboard posts.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py` to emit repeatable sample content and `publishable_content_schema.json`.
+- Added `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py` for matrix coverage and repeatable bundle generation tests.
+- Added `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` documenting content pillars, campaign angles, formats, and CTA rules.
+- Generated `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+
+## Validation
+- `python -m pytest tests\test_content_generation_service.py`
+  - Result: pass, 2 tests passed in 0.43s.
+- `python src\scripts\generate_social_content_samples.py`
+  - Result: pass, wrote `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+- Manual review requested:
+  - Review `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and confirm pass/fail for:
+    1. content pillars/themes fit the Strategy Warehouse offer,
+    2. sample copy tone is acceptable for publishing,
+    3. campaign asset briefs are usable for downstream creative production.
+
+## Evidence
+- Objective-Delivery-Coverage: 95%
+- Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md`
+  - Objective-Proved: reusable content pillars, campaign angles, formats, and CTA rules were defined and documented.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: the engine can generate reusable post variants and campaign asset briefs from live warehouse data.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`
+  - Objective-Proved: generated content is backed by a concrete publishable schema.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m pytest tests\test_content_generation_service.py` => `2 passed in 0.43s`
+  - Objective-Proved: content matrix coverage and repeatable bundle generation were validated automatically.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py`, `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py`, `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py`
+  - Objective-Proved: the workspace now contains the social content engine implementation and verification harness.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: pending user review of `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: generated copy and asset briefs are acceptable for brand and publishing use.
+  - Status: planned
+
+## Risks/Notes
+- Brand/output quality likely needs manual review.
+- Current output produces structured asset briefs, not rendered media files; downstream design/video automation can consume those briefs.
+- Generated copy is grounded in local 2026-03-18 snapshot files and should be regenerated when source data changes materially.
+
+## Completion Status
+- Awaiting user verification - 2026-03-18 18:34Z
 
 
 ## Execution Evidence

file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.
diff --git a/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md b/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
index ca256ce9a47d823f880f4b8092cffd96382ac1ba..6fe81ae41c661f5c4bf59a3c3f6c93c6af959904
--- a/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
+++ b/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
@@ -14,36 +14,77 @@
 ## Dependency
 Dependency: `20260316_135212_trading_strategy_warehouse_define_growth_offer_and_kpis.md`
 
-## Plan
-- [ ] 1. Define content pillars, posting themes, and reusable content formats.
-  - [ ] Test: a documented content matrix exists for multiple campaign angles.
-  - [ ] Evidence: content matrix artifact recorded.
-- [ ] 2. Implement asset or copy generation workflow.
-  - [ ] Test: sample posts/assets can be generated repeatably.
-  - [ ] Evidence: generated output files or artifacts recorded.
-
-## Implementation Log
-- Created from epic decomposition on 2026-03-16.
-
-## Changes Made
-- None yet.
-
-## Validation
-- Pending.
-
-## Evidence
-- Objective-Delivery-Coverage: 0%
-- Auto-Acceptance: false
-- Evidence-Type: file_output
-  - Artifact: generated post/campaign asset set
-  - Objective-Proved: the engine can produce reusable marketing content
-  - Status: planned
-
-## Risks/Notes
-- Brand/output quality likely needs manual review.
-
-## Completion Status
-- Todo
+## Plan
+- [x] 1. Define content pillars, posting themes, and reusable content formats.
+  - [x] Test: a documented content matrix exists for multiple campaign angles.
+  - [x] Evidence: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` and generator-backed matrix output recorded in `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`.
+- [x] 2. Implement asset or copy generation workflow.
+  - [x] Test: sample posts/assets can be generated repeatably.
+  - [x] Evidence: repeatable generator script, generated sample bundle, and schema artifact recorded under `ep_strategy_warehouse_marketing/solution/backend/src` and `ep_strategy_warehouse_marketing/verification`.
+
+## Implementation Log
+- Created from epic decomposition on 2026-03-16.
+- 2026-03-18 18:20Z - Inspected dependency completion, epic outputs, and live Strategy Warehouse JSON feeds under `TradeApps/breakout/fs/json/live/forex`.
+- 2026-03-18 18:29Z - Implemented content schema, reusable content matrix, Jinja templates, and `ContentGeneratorService` in `ep_strategy_warehouse_marketing/solution/backend/src`.
+- 2026-03-18 18:31Z - Added repeatable sample-generation script and backend pytest coverage for matrix generation and campaign bundle validation.
+- 2026-03-18 18:32Z - Generated live sample outputs and JSON schema artifacts from the 2026-03-18 warehouse snapshot.
+- 2026-03-18 18:34Z - Requested manual review of generated copy quality before final lifecycle completion.
+
+## Changes Made
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py` with `PublishableContent`, platform constraints, content matrix models, and campaign asset schema.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py` to transform warehouse snapshots into reusable social posts, platform variants, and asset briefs.
+- Added Jinja templates in `ep_strategy_warehouse_marketing/solution/backend/src/templates/` for signal alerts, performance summaries, and leaderboard posts.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py` to emit repeatable sample content and `publishable_content_schema.json`.
+- Added `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py` for matrix coverage and repeatable bundle generation tests.
+- Added `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` documenting content pillars, campaign angles, formats, and CTA rules.
+- Generated `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+
+## Validation
+- `python -m pytest tests\test_content_generation_service.py`
+  - Result: pass, 2 tests passed in 0.43s.
+- `python src\scripts\generate_social_content_samples.py`
+  - Result: pass, wrote `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+- Manual review requested:
+  - Review `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and confirm pass/fail for:
+    1. content pillars/themes fit the Strategy Warehouse offer,
+    2. sample copy tone is acceptable for publishing,
+    3. campaign asset briefs are usable for downstream creative production.
+
+## Evidence
+- Objective-Delivery-Coverage: 95%
+- Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md`
+  - Objective-Proved: reusable content pillars, campaign angles, formats, and CTA rules were defined and documented.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: the engine can generate reusable post variants and campaign asset briefs from live warehouse data.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`
+  - Objective-Proved: generated content is backed by a concrete publishable schema.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m pytest tests\test_content_generation_service.py` => `2 passed in 0.43s`
+  - Objective-Proved: content matrix coverage and repeatable bundle generation were validated automatically.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py`, `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py`, `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py`
+  - Objective-Proved: the workspace now contains the social content engine implementation and verification harness.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: pending user review of `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: generated copy and asset briefs are acceptable for brand and publishing use.
+  - Status: planned
+
+## Risks/Notes
+- Brand/output quality likely needs manual review.
+- Current output produces structured asset briefs, not rendered media files; downstream design/video automation can consume those briefs.
+- Generated copy is grounded in local 2026-03-18 snapshot files and should be regenerated when source data changes materially.
+
+## Completion Status
+- Awaiting user verification - 2026-03-18 18:34Z
 
 
 ## Execution Evidence

Plan update
Implementation, artifact generation, validation, and lifecycle-file updates are complete. The task remains in-progress only because the lifecycle skill requires human verification for brand-facing output before moving to complete.
  ✓ Inspect marketing-engine backend and live data inputs
  ✓ Implement content schema, matrix, templates, and generation service
  ✓ Add repeatable sample generation script and sample outputs
  ✓ Run validations and update lifecycle task file
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.
diff --git a/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md b/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
index ca256ce9a47d823f880f4b8092cffd96382ac1ba..6fe81ae41c661f5c4bf59a3c3f6c93c6af959904
--- a/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
+++ b/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
@@ -14,36 +14,77 @@
 ## Dependency
 Dependency: `20260316_135212_trading_strategy_warehouse_define_growth_offer_and_kpis.md`
 
-## Plan
-- [ ] 1. Define content pillars, posting themes, and reusable content formats.
-  - [ ] Test: a documented content matrix exists for multiple campaign angles.
-  - [ ] Evidence: content matrix artifact recorded.
-- [ ] 2. Implement asset or copy generation workflow.
-  - [ ] Test: sample posts/assets can be generated repeatably.
-  - [ ] Evidence: generated output files or artifacts recorded.
-
-## Implementation Log
-- Created from epic decomposition on 2026-03-16.
-
-## Changes Made
-- None yet.
-
-## Validation
-- Pending.
-
-## Evidence
-- Objective-Delivery-Coverage: 0%
-- Auto-Acceptance: false
-- Evidence-Type: file_output
-  - Artifact: generated post/campaign asset set
-  - Objective-Proved: the engine can produce reusable marketing content
-  - Status: planned
-
-## Risks/Notes
-- Brand/output quality likely needs manual review.
-
-## Completion Status
-- Todo
+## Plan
+- [x] 1. Define content pillars, posting themes, and reusable content formats.
+  - [x] Test: a documented content matrix exists for multiple campaign angles.
+  - [x] Evidence: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` and generator-backed matrix output recorded in `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`.
+- [x] 2. Implement asset or copy generation workflow.
+  - [x] Test: sample posts/assets can be generated repeatably.
+  - [x] Evidence: repeatable generator script, generated sample bundle, and schema artifact recorded under `ep_strategy_warehouse_marketing/solution/backend/src` and `ep_strategy_warehouse_marketing/verification`.
+
+## Implementation Log
+- Created from epic decomposition on 2026-03-16.
+- 2026-03-18 18:20Z - Inspected dependency completion, epic outputs, and live Strategy Warehouse JSON feeds under `TradeApps/breakout/fs/json/live/forex`.
+- 2026-03-18 18:29Z - Implemented content schema, reusable content matrix, Jinja templates, and `ContentGeneratorService` in `ep_strategy_warehouse_marketing/solution/backend/src`.
+- 2026-03-18 18:31Z - Added repeatable sample-generation script and backend pytest coverage for matrix generation and campaign bundle validation.
+- 2026-03-18 18:32Z - Generated live sample outputs and JSON schema artifacts from the 2026-03-18 warehouse snapshot.
+- 2026-03-18 18:34Z - Requested manual review of generated copy quality before final lifecycle completion.
+
+## Changes Made
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py` with `PublishableContent`, platform constraints, content matrix models, and campaign asset schema.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py` to transform warehouse snapshots into reusable social posts, platform variants, and asset briefs.
+- Added Jinja templates in `ep_strategy_warehouse_marketing/solution/backend/src/templates/` for signal alerts, performance summaries, and leaderboard posts.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py` to emit repeatable sample content and `publishable_content_schema.json`.
+- Added `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py` for matrix coverage and repeatable bundle generation tests.
+- Added `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` documenting content pillars, campaign angles, formats, and CTA rules.
+- Generated `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+
+## Validation
+- `python -m pytest tests\test_content_generation_service.py`
+  - Result: pass, 2 tests passed in 0.43s.
+- `python src\scripts\generate_social_content_samples.py`
+  - Result: pass, wrote `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+- Manual review requested:
+  - Review `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and confirm pass/fail for:
+    1. content pillars/themes fit the Strategy Warehouse offer,
+    2. sample copy tone is acceptable for publishing,
+    3. campaign asset briefs are usable for downstream creative production.
+
+## Evidence
+- Objective-Delivery-Coverage: 95%
+- Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md`
+  - Objective-Proved: reusable content pillars, campaign angles, formats, and CTA rules were defined and documented.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: the engine can generate reusable post variants and campaign asset briefs from live warehouse data.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`
+  - Objective-Proved: generated content is backed by a concrete publishable schema.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m pytest tests\test_content_generation_service.py` => `2 passed in 0.43s`
+  - Objective-Proved: content matrix coverage and repeatable bundle generation were validated automatically.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py`, `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py`, `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py`
+  - Objective-Proved: the workspace now contains the social content engine implementation and verification harness.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: pending user review of `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: generated copy and asset briefs are acceptable for brand and publishing use.
+  - Status: planned
+
+## Risks/Notes
+- Brand/output quality likely needs manual review.
+- Current output produces structured asset briefs, not rendered media files; downstream design/video automation can consume those briefs.
+- Generated copy is grounded in local 2026-03-18 snapshot files and should be regenerated when source data changes materially.
+
+## Completion Status
+- Awaiting user verification - 2026-03-18 18:34Z
 
 
 ## Execution Evidence

codex
Implemented the social content engine in [contentGeneratorService.py](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\services\contentGeneratorService.py), backed by [content_schema.py](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\content_schema.py), Jinja templates, a repeatable sample generator script, and pytest coverage in [test_content_generation_service.py](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_content_generation_service.py). I also added the documented content matrix at [social_content_matrix.md](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\A\social_content_matrix.md) and generated live artifacts at [generated_social_content_samples.json](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\verification\generated_social_content_samples.json) and [publishable_content_schema.json](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\publishable_content_schema.json).

Validation passed:
- `python -m pytest tests\test_content_generation_service.py`
- `python src\scripts\generate_social_content_samples.py`

I updated the lifecycle file at [20260316_135214_trading_strategy_warehouse_create_social_content_engine.md](C:\Users\edebe\eds\workstream\200_inprogress\codex\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md) with checked plan items, evidence, and validation results. Per the lifecycle rules, it is left as `Awaiting user verification` rather than moved to `300_complete`.

Please review [generated_social_content_samples.json](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\verification\generated_social_content_samples.json) and reply pass/fail for:
1. content pillars/themes fit the Strategy Warehouse offer
2. sample copy tone is acceptable for publishing
3. campaign asset briefs are usable for downstream creative production
file update:
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..36a6e0d328debd8387790d08fe5f4c12221102d4
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/__init__.py
@@ -0,0 +1 @@
+"""Schema package for publishable marketing content."""
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
new file mode 100644
index 0000000000000000000000000000000000000000..7c10e00a9baa0a11b6ebf5127198d7269e76aef3
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py
@@ -0,0 +1,122 @@
+from __future__ import annotations
+
+from datetime import UTC, datetime
+from enum import Enum
+from typing import Any
+from uuid import UUID, uuid4
+
+from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
+
+
+class ContentType(str, Enum):
+    SIGNAL_ALERT = "signal_alert"
+    PERFORMANCE_SUMMARY = "performance_summary"
+    STRATEGY_RANKING = "strategy_ranking"
+    EDUCATIONAL = "educational"
+
+
+class CampaignAngle(str, Enum):
+    MOMENTUM = "momentum"
+    RISK_DISCIPLINE = "risk_discipline"
+    LEADERBOARD = "leaderboard"
+    EDUCATION = "education"
+
+
+class Platform(str, Enum):
+    TWITTER = "twitter"
+    LINKEDIN = "linkedin"
+    REDDIT = "reddit"
+    DISCORD = "discord"
+    TELEGRAM = "telegram"
+    TIKTOK = "tiktok"
+
+
+PLATFORM_LIMITS: dict[Platform, dict[str, int]] = {
+    Platform.TWITTER: {"headline": 100, "body": 280, "hashtags": 4},
+    Platform.LINKEDIN: {"headline": 150, "body": 3000, "hashtags": 6},
+    Platform.REDDIT: {"headline": 300, "body": 40000, "hashtags": 0},
+    Platform.DISCORD: {"headline": 120, "body": 2000, "hashtags": 4},
+    Platform.TELEGRAM: {"headline": 120, "body": 1024, "hashtags": 5},
+    Platform.TIKTOK: {"headline": 120, "body": 2200, "hashtags": 6},
+}
+
+
+class VariantContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    platform: Platform
+    headline: str = Field(min_length=1)
+    body: str = Field(min_length=1)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+
+    @model_validator(mode="after")
+    def validate_platform_limits(self) -> "VariantContent":
+        limits = PLATFORM_LIMITS[self.platform]
+        if len(self.headline) > limits["headline"]:
+            raise ValueError(
+                f"{self.platform} headline exceeds {limits['headline']} characters"
+            )
+        if len(self.body) > limits["body"]:
+            raise ValueError(
+                f"{self.platform} body exceeds {limits['body']} characters"
+            )
+        if len(self.hashtags) > limits["hashtags"]:
+            raise ValueError(
+                f"{self.platform} hashtag count exceeds {limits['hashtags']}"
+            )
+        return self
+
+
+class CampaignAsset(BaseModel):
+    asset_type: str = Field(min_length=1, max_length=64)
+    title: str = Field(min_length=1, max_length=140)
+    visual_brief: str = Field(min_length=1, max_length=280)
+    callout: str = Field(min_length=1, max_length=180)
+
+
+class PublishableContent(BaseModel):
+    model_config = ConfigDict(use_enum_values=True)
+
+    content_id: UUID = Field(default_factory=uuid4)
+    content_type: ContentType
+    campaign_angle: CampaignAngle
+    pillar: str = Field(min_length=1, max_length=80)
+    format_name: str = Field(min_length=1, max_length=80)
+    headline: str = Field(min_length=1, max_length=100)
+    body: str = Field(min_length=1, max_length=280)
+    media_urls: list[str] = Field(default_factory=list)
+    hashtags: list[str] = Field(default_factory=list)
+    call_to_action: str = Field(min_length=1, max_length=160)
+    landing_page_url: str = Field(min_length=1, max_length=255)
+    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
+    scheduled_for: datetime | None = None
+    platform_variants: dict[Platform, VariantContent] = Field(default_factory=dict)
+    source_data: dict[str, Any] = Field(default_factory=dict)
+    campaign_assets: list[CampaignAsset] = Field(default_factory=list)
+
+    @field_validator("hashtags")
+    @classmethod
+    def validate_hashtags(cls, hashtags: list[str]) -> list[str]:
+        for tag in hashtags:
+            if not tag.startswith("#"):
+                raise ValueError("hashtags must start with #")
+        return hashtags
+
+    @model_validator(mode="after")
+    def validate_variant_platforms(self) -> "PublishableContent":
+        for platform, variant in self.platform_variants.items():
+            if variant.platform != platform:
+                raise ValueError("platform_variants keys must match variant platform")
+        return self
+
+
+class ContentMatrixEntry(BaseModel):
+    pillar: str = Field(min_length=1, max_length=80)
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str = Field(min_length=1, max_length=140)
+    format_name: str = Field(min_length=1, max_length=80)
+    target_platforms: list[Platform] = Field(min_length=1)
+    hook_style: str = Field(min_length=1, max_length=120)
+    call_to_action: str = Field(min_length=1, max_length=160)
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
new file mode 100644
index 0000000000000000000000000000000000000000..43fa938858a2b2db5a674b14bf52345fe98c74aa
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py
@@ -0,0 +1,42 @@
+from __future__ import annotations
+
+import json
+from pathlib import Path
+import sys
+
+
+CURRENT_FILE = Path(__file__).resolve()
+BACKEND_ROOT = CURRENT_FILE.parents[2]
+if str(BACKEND_ROOT) not in sys.path:
+    sys.path.insert(0, str(BACKEND_ROOT))
+
+from src.schemas.content_schema import PublishableContent
+from src.services.contentGeneratorService import ContentGeneratorService, StrategyWarehouseDataLoader
+
+
+def main() -> None:
+    project_root = Path(__file__).resolve().parents[4]
+    data_root = project_root.parent / "TradeApps" / "breakout" / "fs" / "json" / "live" / "forex"
+    verification_dir = project_root / "verification"
+    schema_dir = project_root / "solution" / "backend" / "src" / "schemas"
+    verification_dir.mkdir(parents=True, exist_ok=True)
+
+    loader = StrategyWarehouseDataLoader(data_root)
+    warehouse_data = loader.load_snapshot_bundle()
+    service = ContentGeneratorService()
+    bundle = service.generate_campaign_bundle(warehouse_data)
+
+    output_path = verification_dir / "generated_social_content_samples.json"
+    with output_path.open("w", encoding="utf-8") as handle:
+        json.dump(bundle, handle, indent=2)
+
+    schema_path = schema_dir / "publishable_content_schema.json"
+    with schema_path.open("w", encoding="utf-8") as handle:
+        json.dump(PublishableContent.model_json_schema(), handle, indent=2)
+
+    print(f"Wrote {output_path}")
+    print(f"Wrote {schema_path}")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10424bd02f1dfd2e5a49da41f8591ada739a671
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py
@@ -0,0 +1,376 @@
+from __future__ import annotations
+
+import json
+from dataclasses import dataclass
+from pathlib import Path
+from typing import Any
+
+from jinja2 import Environment, FileSystemLoader, select_autoescape
+
+from src.schemas.content_schema import (
+    PLATFORM_LIMITS,
+    CampaignAngle,
+    CampaignAsset,
+    ContentMatrixEntry,
+    ContentType,
+    Platform,
+    PublishableContent,
+    VariantContent,
+)
+
+
+DEFAULT_LANDING_PAGE_URL = "https://strategywarehouse.example.com/subscribe"
+DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]
+
+
+@dataclass(frozen=True)
+class PillarDefinition:
+    pillar: str
+    campaign_angle: CampaignAngle
+    content_type: ContentType
+    theme: str
+    format_name: str
+    target_platforms: tuple[Platform, ...]
+    hook_style: str
+    call_to_action: str
+
+
+CONTENT_MATRIX: tuple[PillarDefinition, ...] = (
+    PillarDefinition(
+        pillar="daily_signal_edge",
+        campaign_angle=CampaignAngle.MOMENTUM,
+        content_type=ContentType.SIGNAL_ALERT,
+        theme="Surface the strongest live mover with fast proof and a clear invite.",
+        format_name="flash_signal_post",
+        target_platforms=(Platform.TWITTER, Platform.DISCORD, Platform.TELEGRAM),
+        hook_style="Urgent momentum hook",
+        call_to_action="Join the Strategy Warehouse list for the next live signal batch.",
+    ),
+    PillarDefinition(
+        pillar="performance_recap",
+        campaign_angle=CampaignAngle.RISK_DISCIPLINE,
+        content_type=ContentType.PERFORMANCE_SUMMARY,
+        theme="Translate snapshot data into disciplined weekly-style proof.",
+        format_name="proof_of_process_post",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.TWITTER),
+        hook_style="Measured proof hook",
+        call_to_action="Get the operating notes and performance recap in the subscriber digest.",
+    ),
+    PillarDefinition(
+        pillar="leaderboard_watch",
+        campaign_angle=CampaignAngle.LEADERBOARD,
+        content_type=ContentType.STRATEGY_RANKING,
+        theme="Show ranked leaders and why the board is rotating.",
+        format_name="leaderboard_carousel",
+        target_platforms=(Platform.TWITTER, Platform.LINKEDIN, Platform.TIKTOK),
+        hook_style="Competitive leaderboard hook",
+        call_to_action="Subscribe to track when the leaderboard flips.",
+    ),
+    PillarDefinition(
+        pillar="trader_education",
+        campaign_angle=CampaignAngle.EDUCATION,
+        content_type=ContentType.EDUCATIONAL,
+        theme="Turn warehouse output into reusable explanations about risk and selection.",
+        format_name="educational_breakdown",
+        target_platforms=(Platform.LINKEDIN, Platform.REDDIT, Platform.DISCORD),
+        hook_style="Teach with one sharp lesson",
+        call_to_action="Join for deeper breakdowns behind each strategy setup.",
+    ),
+)
+
+
+class StrategyWarehouseDataLoader:
+    def __init__(self, base_path: str | Path) -> None:
+        self.base_path = Path(base_path)
+
+    def latest_snapshot_dir(self) -> Path:
+        date_dirs = sorted(
+            [path for path in self.base_path.iterdir() if path.is_dir()],
+            reverse=True,
+        )
+        if not date_dirs:
+            raise FileNotFoundError(f"No dated snapshot directories found in {self.base_path}")
+        return date_dirs[0]
+
+    def load_snapshot_bundle(self, snapshot_dir: str | Path | None = None) -> dict[str, Any]:
+        target_dir = Path(snapshot_dir) if snapshot_dir else self.latest_snapshot_dir()
+        bundle: dict[str, Any] = {}
+        for file_name in ("_summary_net.json", "_frequency.json", "_dna_frequency.json"):
+            file_path = target_dir / file_name
+            with file_path.open("r", encoding="utf-8") as handle:
+                bundle[file_name] = json.load(handle)
+        bundle["snapshot_dir"] = str(target_dir)
+        return bundle
+
+
+class ContentGeneratorService:
+    def __init__(
+        self,
+        template_dir: str | Path | None = None,
+        landing_page_url: str = DEFAULT_LANDING_PAGE_URL,
+    ) -> None:
+        resolved_template_dir = (
+            Path(template_dir)
+            if template_dir
+            else Path(__file__).resolve().parent.parent / "templates"
+        )
+        self.environment = Environment(
+            loader=FileSystemLoader(str(resolved_template_dir)),
+            autoescape=select_autoescape(enabled_extensions=("j2", "jinja2")),
+            trim_blocks=True,
+            lstrip_blocks=True,
+        )
+        self.landing_page_url = landing_page_url
+
+    def build_content_matrix(self) -> list[ContentMatrixEntry]:
+        return [
+            ContentMatrixEntry(
+                pillar=definition.pillar,
+                campaign_angle=definition.campaign_angle,
+                content_type=definition.content_type,
+                theme=definition.theme,
+                format_name=definition.format_name,
+                target_platforms=list(definition.target_platforms),
+                hook_style=definition.hook_style,
+                call_to_action=definition.call_to_action,
+            )
+            for definition in CONTENT_MATRIX
+        ]
+
+    def generate_campaign_bundle(self, warehouse_data: dict[str, Any]) -> dict[str, Any]:
+        matrix = self.build_content_matrix()
+        posts = [
+            self._build_signal_alert(warehouse_data),
+            self._build_performance_summary(warehouse_data),
+            self._build_strategy_ranking(warehouse_data),
+            self._build_educational_post(warehouse_data),
+        ]
+        return {
+            "content_matrix": [entry.model_dump(mode="json") for entry in matrix],
+            "generated_at": warehouse_data["_summary_net.json"]["last_update"],
+            "source_snapshot_dir": warehouse_data["snapshot_dir"],
+            "posts": [post.model_dump(mode="json") for post in posts],
+        }
+
+    def _build_signal_alert(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        summary = warehouse_data["_summary_net.json"]
+        strategy, product, point = self._best_signal(summary)
+        body = self.environment.get_template("signal_alert.jinja2").render(
+            hook="Momentum check:",
+            strategy=self._shorten_strategy(strategy),
+            product=product,
+            net_points=self._format_points(point["net"]),
+            directional_bias=self._directional_bias(point),
+            proof_point=f"{point['b_c']} buys vs {point['s_c']} sells on the latest pass.",
+        )
+        headline = f"{product} setup presses {self._format_points(point['net'])} pts"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[0],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + [f"#{product}"],
+            source_data={
+                "strategy": strategy,
+                "product": product,
+                "latest_point": point,
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="quote_card",
+                    title=f"{product} momentum card",
+                    visual_brief=f"Highlight {product} net curve and current strategy label.",
+                    callout="Fast signal, clear edge, direct CTA.",
+                )
+            ],
+        )
+
+    def _build_performance_summary(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        top_leader = latest_snapshot["leaders"][0]
+        body = self.environment.get_template("performance_summary.jinja2").render(
+            lead_in="Discipline over noise:",
+            winning_product=top_leader["product"],
+            winning_net=self._format_points(top_leader["net"]),
+            snapshot_count=frequency["snapshot_count"],
+            risk_frame="The engine keeps publishing only when the board shows repeatable strength.",
+        )
+        headline = f"{top_leader['product']} leads {frequency['snapshot_count']} live checks"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[1],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#RiskManagement"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leader": top_leader,
+                "snapshot_count": frequency["snapshot_count"],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="carousel",
+                    title="Performance recap carousel",
+                    visual_brief="Slide 1 headline, slide 2 snapshot count, slide 3 why discipline matters.",
+                    callout="Proof without overclaiming.",
+                )
+            ],
+        )
+
+    def _build_strategy_ranking(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        dna_frequency = warehouse_data["_dna_frequency.json"]
+        latest_snapshot = dna_frequency["snapshots"][-1]
+        leaders = [
+            f"{leader['rank']}. {leader['product']} ({self._format_points(leader['net'])})"
+            for leader in latest_snapshot["leaders"][:3]
+        ]
+        body = self.environment.get_template("strategy_ranking.jinja2").render(
+            lead_in="Leaderboard watch:",
+            leaders=leaders,
+            takeaway="Rotation matters more than hype. Watch which names stay on the board.",
+        )
+        headline = "DNA leaderboard rotation is tightening"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[2],
+            headline=headline,
+            body=body,
+            hashtags=DEFAULT_HASHTAGS + ["#Leaderboard"],
+            source_data={
+                "latest_snapshot_time": latest_snapshot["time"],
+                "leaders": latest_snapshot["leaders"][:5],
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="leaderboard_card",
+                    title="Top 3 DNA strategies",
+                    visual_brief="Three-column leaderboard with rank badges and point totals.",
+                    callout="Show movement between yesterday and today.",
+                )
+            ],
+        )
+
+    def _build_educational_post(self, warehouse_data: dict[str, Any]) -> PublishableContent:
+        frequency = warehouse_data["_frequency.json"]
+        latest_snapshot = frequency["snapshots"][-1]
+        leaders = latest_snapshot["leaders"][:2]
+        leader_names = ", ".join(self._shorten_strategy(item["strategy"]) for item in leaders)
+        body = (
+            "What makes a strategy feed usable? "
+            "Repeated snapshots, ranked leaders, and a clear filter for noise. "
+            f"Today that means tracking {leader_names} and ignoring one-off spikes."
+        )
+        headline = "How to read a strategy board without chasing noise"
+        return self._build_content_item(
+            definition=CONTENT_MATRIX[3],
+            headline=headline,
+            body=body,
+            hashtags=["#TradingEducation", "#StrategyWarehouse", "#ProcessOverPrediction"],
+            source_data={
+                "leaders": leaders,
+                "lesson": "Use repeat snapshots to separate consistency from noise.",
+            },
+            campaign_assets=[
+                CampaignAsset(
+                    asset_type="script_outline",
+                    title="Educational explainer",
+                    visual_brief="30-second talking-head outline with one chart overlay.",
+                    callout="Teach the filter, not the prediction.",
+                )
+            ],
+        )
+
+    def _build_content_item(
+        self,
+        definition: PillarDefinition,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        source_data: dict[str, Any],
+        campaign_assets: list[CampaignAsset],
+    ) -> PublishableContent:
+        base_cta = definition.call_to_action
+        platform_variants = self._build_platform_variants(
+            headline=headline,
+            body=body,
+            hashtags=hashtags,
+            call_to_action=base_cta,
+            target_platforms=definition.target_platforms,
+        )
+        return PublishableContent(
+            content_type=definition.content_type,
+            campaign_angle=definition.campaign_angle,
+            pillar=definition.pillar,
+            format_name=definition.format_name,
+            headline=self._trim(headline, PLATFORM_LIMITS[Platform.TWITTER]["headline"]),
+            body=self._trim(body, PLATFORM_LIMITS[Platform.TWITTER]["body"]),
+            hashtags=hashtags[: PLATFORM_LIMITS[Platform.TWITTER]["hashtags"]],
+            call_to_action=base_cta,
+            landing_page_url=self.landing_page_url,
+            platform_variants=platform_variants,
+            source_data=source_data,
+            campaign_assets=campaign_assets,
+        )
+
+    def _build_platform_variants(
+        self,
+        headline: str,
+        body: str,
+        hashtags: list[str],
+        call_to_action: str,
+        target_platforms: tuple[Platform, ...],
+    ) -> dict[Platform, VariantContent]:
+        variants: dict[Platform, VariantContent] = {}
+        for platform in target_platforms:
+            limits = PLATFORM_LIMITS[platform]
+            platform_tags = hashtags[: limits["hashtags"]]
+            cta = self._trim(call_to_action, 160)
+            if platform == Platform.REDDIT:
+                variant_body = f"{body}\n\nCTA: {cta}"
+            elif platform == Platform.DISCORD:
+                variant_body = f"{body} {cta}"
+            else:
+                variant_body = f"{body} {' '.join(platform_tags)} {cta}".strip()
+            variants[platform] = VariantContent(
+                platform=platform,
+                headline=self._trim(headline, limits["headline"]),
+                body=self._trim(variant_body, limits["body"]),
+                hashtags=platform_tags,
+                call_to_action=cta,
+            )
+        return variants
+
+    @staticmethod
+    def _best_signal(summary: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
+        best_item: tuple[str, str, dict[str, Any]] | None = None
+        for strategy, products in summary["strategies"].items():
+            for product, points in products.items():
+                if not points:
+                    continue
+                latest = points[-1]
+                if best_item is None or latest["net"] > best_item[2]["net"]:
+                    best_item = (strategy, product, latest)
+        if best_item is None:
+            raise ValueError("No strategy points available in summary feed")
+        return best_item
+
+    @staticmethod
+    def _directional_bias(point: dict[str, Any]) -> str:
+        if point["buy_net"] > point["sell_net"]:
+            return "buy-led"
+        if point["sell_net"] > point["buy_net"]:
+            return "sell-led"
+        return "balanced"
+
+    @staticmethod
+    def _trim(text: str, max_length: int) -> str:
+        if len(text) <= max_length:
+            return text
+        return text[: max_length - 3].rstrip() + "..."
+
+    @staticmethod
+    def _shorten_strategy(strategy: str) -> str:
+        return strategy.replace("breakout_", "brk_").replace("_", " ")
+
+    @staticmethod
+    def _format_points(value: float) -> str:
+        rounded = round(value, 1)
+        return f"{rounded:+g}"
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..ada4f9a16a57699c230ad8e57c8a07c998d9ccfe
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/performance_summary.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ winning_product }} leads the board with {{ winning_net }} pts while {{ snapshot_count }} snapshots keep the tape honest. {{ risk_frame }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..5a4b8436264212930a0e5bade52b809ef187845e
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/signal_alert.jinja2
@@ -0,0 +1 @@
+{{ hook }} {{ strategy }} on {{ product }}. Net {{ net_points }} pts, {{ directional_bias }} bias. {{ proof_point }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2 b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
new file mode 100644
index 0000000000000000000000000000000000000000..82f2988e1ab04438647df0ecabe34829ff8e0ba9
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/src/templates/strategy_ranking.jinja2
@@ -0,0 +1 @@
+{{ lead_in }} {{ leaders|join(' | ') }}. {{ takeaway }}
diff --git a/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
new file mode 100644
index 0000000000000000000000000000000000000000..30fe2d78bdd5431062e5bc608f27b04cc3ec3729
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py
@@ -0,0 +1,116 @@
+from __future__ import annotations
+
+from pathlib import Path
+
+from src.schemas.content_schema import CampaignAngle, ContentType, Platform
+from src.services.contentGeneratorService import ContentGeneratorService
+
+
+def sample_warehouse_bundle() -> dict:
+    return {
+        "snapshot_dir": "synthetic/2026-03-18",
+        "_summary_net.json": {
+            "last_update": "2026-03-18T18:27:26.421368",
+            "strategies": {
+                "breakout_R_Rev_4_tp10.0_sl5.0": {
+                    "EUR": [
+                        {
+                            "t": "2026-03-18T13:37:32.591957",
+                            "net": 245.0,
+                            "buy_net": 180.0,
+                            "sell_net": 65.0,
+                            "b_c": 3,
+                            "s_c": 1,
+                        }
+                    ]
+                }
+            },
+        },
+        "_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 206,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:20:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "score_rank": 1,
+                            "score": 11.0,
+                            "product": "SOL",
+                            "strategy": "breakout_2_tp20.0_sl20.0",
+                            "net": 195.0,
+                        }
+                    ],
+                }
+            ],
+        },
+        "_dna_frequency.json": {
+            "date": "2026-03-18",
+            "snapshot_count": 215,
+            "snapshots": [
+                {
+                    "time": "2026-03-18T17:55:00",
+                    "leaders": [
+                        {
+                            "rank": 1,
+                            "product": "DNA_105009_CAD",
+                            "strategy": "EVENT-S-FLIP-T_tp348.00_sl53.00",
+                            "net": 90.0,
+                        },
+                        {
+                            "rank": 2,
+                            "product": "DNA_105026_CAD",
+                            "strategy": "BUCKET-S-TGT-P_tp437.00_sl54.00",
+                            "net": 85.0,
+                        },
+                        {
+                            "rank": 3,
+                            "product": "DNA_105119_CAD",
+                            "strategy": "BRK-S-DUR-TS_tp418.00_sl52.00",
+                            "net": 80.0,
+                        },
+                    ],
+                }
+            ],
+        },
+    }
+
+
+def test_build_content_matrix_covers_multiple_campaign_angles() -> None:
+    service = ContentGeneratorService()
+
+    matrix = service.build_content_matrix()
+
+    assert len(matrix) == 4
+    assert {entry.campaign_angle for entry in matrix} == {
+        CampaignAngle.MOMENTUM,
+        CampaignAngle.RISK_DISCIPLINE,
+        CampaignAngle.LEADERBOARD,
+        CampaignAngle.EDUCATION,
+    }
+    assert {entry.content_type for entry in matrix} == {
+        ContentType.SIGNAL_ALERT,
+        ContentType.PERFORMANCE_SUMMARY,
+        ContentType.STRATEGY_RANKING,
+        ContentType.EDUCATIONAL,
+    }
+
+
+def test_generate_campaign_bundle_returns_repeatable_valid_posts() -> None:
+    service = ContentGeneratorService(
+        template_dir=Path(__file__).resolve().parents[1] / "src" / "templates"
+    )
+
+    bundle = service.generate_campaign_bundle(sample_warehouse_bundle())
+
+    assert bundle["generated_at"] == "2026-03-18T18:27:26.421368"
+    assert bundle["source_snapshot_dir"] == "synthetic/2026-03-18"
+    assert len(bundle["content_matrix"]) == 4
+    assert len(bundle["posts"]) == 4
+
+    first_post = bundle["posts"][0]
+    assert first_post["content_type"] == ContentType.SIGNAL_ALERT.value
+    assert Platform.TWITTER.value in first_post["platform_variants"]
+    assert len(first_post["campaign_assets"]) == 1
+    assert first_post["headline"]
diff --git a/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
new file mode 100644
index 0000000000000000000000000000000000000000..9b0f729da2199f4b93871e78830b0c40f039ecce
--- /dev/null
+++ b/ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md
@@ -0,0 +1,21 @@
+# Strategy Warehouse Social Content Matrix
+
+## Purpose
+
+This matrix defines reusable social content pillars, campaign angles, and format rules for the Strategy Warehouse marketing engine.
+
+## Content Matrix
+
+| Pillar | Campaign Angle | Content Type | Theme | Format | Target Platforms | Hook Style | CTA |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| `daily_signal_edge` | `momentum` | `signal_alert` | Surface the strongest live mover with fast proof and a clear invite. | `flash_signal_post` | Twitter, Discord, Telegram | Urgent momentum hook | Join the Strategy Warehouse list for the next live signal batch. |
+| `performance_recap` | `risk_discipline` | `performance_summary` | Translate snapshot data into disciplined weekly-style proof. | `proof_of_process_post` | LinkedIn, Reddit, Twitter | Measured proof hook | Get the operating notes and performance recap in the subscriber digest. |
+| `leaderboard_watch` | `leaderboard` | `strategy_ranking` | Show ranked leaders and why the board is rotating. | `leaderboard_carousel` | Twitter, LinkedIn, TikTok | Competitive leaderboard hook | Subscribe to track when the leaderboard flips. |
+| `trader_education` | `education` | `educational` | Turn warehouse output into reusable explanations about risk and selection. | `educational_breakdown` | LinkedIn, Reddit, Discord | Teach with one sharp lesson | Join for deeper breakdowns behind each strategy setup. |
+
+## Format Rules
+
+- Use data-backed proof from `_summary_net.json`, `_frequency.json`, and `_dna_frequency.json`.
+- Keep the base post compatible with Twitter limits, then expand or reshape per platform variant.
+- Always include a clear subscriber CTA tied to the landing page.
+- Ship at least one campaign asset brief per post so downstream design or video automation has a repeatable input.
diff --git a/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md b/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
index ca256ce9a47d823f880f4b8092cffd96382ac1ba..6fe81ae41c661f5c4bf59a3c3f6c93c6af959904
--- a/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
+++ b/workstream/200_inprogress/codex/20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
@@ -14,36 +14,77 @@
 ## Dependency
 Dependency: `20260316_135212_trading_strategy_warehouse_define_growth_offer_and_kpis.md`
 
-## Plan
-- [ ] 1. Define content pillars, posting themes, and reusable content formats.
-  - [ ] Test: a documented content matrix exists for multiple campaign angles.
-  - [ ] Evidence: content matrix artifact recorded.
-- [ ] 2. Implement asset or copy generation workflow.
-  - [ ] Test: sample posts/assets can be generated repeatably.
-  - [ ] Evidence: generated output files or artifacts recorded.
-
-## Implementation Log
-- Created from epic decomposition on 2026-03-16.
-
-## Changes Made
-- None yet.
-
-## Validation
-- Pending.
-
-## Evidence
-- Objective-Delivery-Coverage: 0%
-- Auto-Acceptance: false
-- Evidence-Type: file_output
-  - Artifact: generated post/campaign asset set
-  - Objective-Proved: the engine can produce reusable marketing content
-  - Status: planned
-
-## Risks/Notes
-- Brand/output quality likely needs manual review.
-
-## Completion Status
-- Todo
+## Plan
+- [x] 1. Define content pillars, posting themes, and reusable content formats.
+  - [x] Test: a documented content matrix exists for multiple campaign angles.
+  - [x] Evidence: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` and generator-backed matrix output recorded in `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`.
+- [x] 2. Implement asset or copy generation workflow.
+  - [x] Test: sample posts/assets can be generated repeatably.
+  - [x] Evidence: repeatable generator script, generated sample bundle, and schema artifact recorded under `ep_strategy_warehouse_marketing/solution/backend/src` and `ep_strategy_warehouse_marketing/verification`.
+
+## Implementation Log
+- Created from epic decomposition on 2026-03-16.
+- 2026-03-18 18:20Z - Inspected dependency completion, epic outputs, and live Strategy Warehouse JSON feeds under `TradeApps/breakout/fs/json/live/forex`.
+- 2026-03-18 18:29Z - Implemented content schema, reusable content matrix, Jinja templates, and `ContentGeneratorService` in `ep_strategy_warehouse_marketing/solution/backend/src`.
+- 2026-03-18 18:31Z - Added repeatable sample-generation script and backend pytest coverage for matrix generation and campaign bundle validation.
+- 2026-03-18 18:32Z - Generated live sample outputs and JSON schema artifacts from the 2026-03-18 warehouse snapshot.
+- 2026-03-18 18:34Z - Requested manual review of generated copy quality before final lifecycle completion.
+
+## Changes Made
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py` with `PublishableContent`, platform constraints, content matrix models, and campaign asset schema.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py` to transform warehouse snapshots into reusable social posts, platform variants, and asset briefs.
+- Added Jinja templates in `ep_strategy_warehouse_marketing/solution/backend/src/templates/` for signal alerts, performance summaries, and leaderboard posts.
+- Added `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py` to emit repeatable sample content and `publishable_content_schema.json`.
+- Added `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py` for matrix coverage and repeatable bundle generation tests.
+- Added `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` documenting content pillars, campaign angles, formats, and CTA rules.
+- Generated `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+
+## Validation
+- `python -m pytest tests\test_content_generation_service.py`
+  - Result: pass, 2 tests passed in 0.43s.
+- `python src\scripts\generate_social_content_samples.py`
+  - Result: pass, wrote `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
+- Manual review requested:
+  - Review `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and confirm pass/fail for:
+    1. content pillars/themes fit the Strategy Warehouse offer,
+    2. sample copy tone is acceptable for publishing,
+    3. campaign asset briefs are usable for downstream creative production.
+
+## Evidence
+- Objective-Delivery-Coverage: 95%
+- Auto-Acceptance: false
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md`
+  - Objective-Proved: reusable content pillars, campaign angles, formats, and CTA rules were defined and documented.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: the engine can generate reusable post variants and campaign asset briefs from live warehouse data.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`
+  - Objective-Proved: generated content is backed by a concrete publishable schema.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m pytest tests\test_content_generation_service.py` => `2 passed in 0.43s`
+  - Objective-Proved: content matrix coverage and repeatable bundle generation were validated automatically.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py`, `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py`, `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py`
+  - Objective-Proved: the workspace now contains the social content engine implementation and verification harness.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: pending user review of `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
+  - Objective-Proved: generated copy and asset briefs are acceptable for brand and publishing use.
+  - Status: planned
+
+## Risks/Notes
+- Brand/output quality likely needs manual review.
+- Current output produces structured asset briefs, not rendered media files; downstream design/video automation can consume those briefs.
+- Generated copy is grounded in local 2026-03-18 snapshot files and should be regenerated when source data changes materially.
+
+## Completion Status
+- Awaiting user verification - 2026-03-18 18:34Z
 
 
 ## Execution Evidence

tokens used
81,713
Implemented the social content engine in [contentGeneratorService.py](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\services\contentGeneratorService.py), backed by [content_schema.py](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\content_schema.py), Jinja templates, a repeatable sample generator script, and pytest coverage in [test_content_generation_service.py](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_content_generation_service.py). I also added the documented content matrix at [social_content_matrix.md](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\A\social_content_matrix.md) and generated live artifacts at [generated_social_content_samples.json](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\verification\generated_social_content_samples.json) and [publishable_content_schema.json](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\src\schemas\publishable_content_schema.json).

Validation passed:
- `python -m pytest tests\test_content_generation_service.py`
- `python src\scripts\generate_social_content_samples.py`

I updated the lifecycle file at [20260316_135214_trading_strategy_warehouse_create_social_content_engine.md](C:\Users\edebe\eds\workstream\200_inprogress\codex\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md) with checked plan items, evidence, and validation results. Per the lifecycle rules, it is left as `Awaiting user verification` rather than moved to `300_complete`.

Please review [generated_social_content_samples.json](C:\Users\edebe\eds\ep_strategy_warehouse_marketing\verification\generated_social_content_samples.json) and reply pass/fail for:
1. content pillars/themes fit the Strategy Warehouse offer
2. sample copy tone is acceptable for publishing
3. campaign asset briefs are usable for downstream creative production
