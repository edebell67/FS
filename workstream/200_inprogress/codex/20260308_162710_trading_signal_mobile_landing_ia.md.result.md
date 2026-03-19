OpenAI Codex v0.115.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019d06fc-2315-7db1-8978-81354237796d
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
codex
I’m loading the lifecycle skill and the specified task file first, then I’ll inspect the affected code paths, implement the required changes, run the validations, and update the task checklist in place.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260308_162710_trading_signal_mobile_landing_ia.md'" in C:\Users\edebe\eds succeeded in 1.94s:
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
 succeeded in 2.15s:
Source: trading_signal_miniapp epic

Task Summary
Define mobile IA/component layout for mini-app using miniapp_feed fields.

Context
- Feed: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
- Evidence folder: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal

Plan
- [x] 1. Validate feed keys used by UI
  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs counts dict
  - [x] Evidence: `clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
- [ ] 2. Draft IA sections and card specs
  - [ ] Test: Section map includes Hero/KPIs/Top Strategies/Open Trades/Next Actions/CTA
  - [ ] Evidence: IA doc saved under clawd_originated\artefacts\projects

Implementation Log
- 2026-03-08 18:15: Lifecycle template enforced; evidence path set to clawd_originated folder.

codex
I’ve got the task scope. Next I’m checking the feed structure and existing artifact folders so I can generate the IA deliverable in the right place and normalize the lifecycle file to the required template before marking anything complete.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts\\miniapp_feed_2026-03-06.json'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Force 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Recurse -Force 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts\\projects'" in C:\Users\edebe\eds succeeded in 1.79s:

    Directory: C:\Users\edebe\eds\workstream\clawd_originated\artefacts

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          08/03/2026    18:13                [44;1mevidence[0m
d----          18/03/2026    18:23                [44;1mprojects[0m
-a---          18/03/2026    18:24           1681 activity_log.md
-a---          08/03/2026    18:13          16129 miniapp_feed_2026-03-06.json
-a---          08/03/2026    16:47           5444 [32;1mminiapp_feed_extractor.py[0m

 succeeded in 1.97s:
{
  "meta": {
    "generated_at_utc": "2026-03-08T18:13:40.484589+00:00",
    "source_day_dir": "C:\\Users\\edebe\\eds\\TradeApps\\breakout\\fs\\json\\live\\2026-03-06",
    "counts": {
      "strategies": 163,
      "open_trades": 1,
      "signals": 4
    }
  },
  "top_one": {
    "strategy": "unknown",
    "pair": "unknown",
    "net_today": 0
  },
  "strategies": [
    {
      "strategy_id": "breakout_R_Rev_3_tp20.0_sl20.0:unknown",
      "strategy_name": "breakout_R_Rev_3_tp20.0_sl20.0",
      "pair": "unknown",
 succeeded in 1.39s:

    Directory: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects

[32;1mMode   [0m[32;1m              LastWriteTime[0m[32;1m         Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
-a---          08/03/2026    22:14           2354 20260308_221600_trading_signal_landing_demo_index.html
-a---          18/03/2026    18:23           3567 20260318_181500_trading_signal_social_templates.md
-a---          08/03/2026    18:13          16129 miniapp_feed_2026-03-06.json

codex
The feed is sparse and mostly placeholder-heavy, so the IA needs to explicitly handle missing values. I’m checking for adjacent trading-signal artifacts to keep naming and structure consistent before I write the deliverable and update the lifecycle evidence.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"trading_signal|miniapp|landing\" 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts\\activity_log.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts\\projects\\20260318_181500_trading_signal_social_templates.md'" in C:\Users\edebe\eds succeeded in 2.29s:
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_extractor.py:145:    out = args.out or os.path.join(args.day_dir, 'miniapp_feed.json')
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md:10:- [2026-03-08 19:05 UTC] DONE | Data feed | `miniapp_feed_extractor.py` executed for sample day | `.../clawd_originated/artefacts/miniapp_feed_2026-03-06.json`
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md:11:- [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md:14:- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md:15:- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md:16:- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260308_221600_trading_signal_landing_demo_index.html:37:fetch('./miniapp_feed_2026-03-06.json').then(r=>r.json()).then(d=>{
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md:3:Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md:21:- Keep the CTA pointed at the miniapp feed or landing demo.
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md:32:`Today’s miniapp snapshot compresses the desk into one glance: ranked strategies, live trade context, and the next trigger to watch. Current live position bias is {{open_trade_side}} with entry around {{open_trade_entry}}. Risk stays first: {{signal_risk_note}}.`
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md:35:`Open the miniapp feed to review the live board before the next candle prints.`
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md:49:`Tap into the miniapp and check the live feed before you place the next trade.`
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md:60:`The trading miniapp closed the day with {{strategies_count}} ranked strategies in the stack, {{open_trades_count}} open trade still active, and {{signals_count}} setups ready for follow-up. The current feed still has placeholder pair labels in places, so this recap should emphasize system coverage, live exposure, and risk discipline over specific instrument claims. Close with {{signal_risk_note}} to keep the recap compliant and useful.`
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt:1:C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\social_templates_validation.txt:1:C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\landing_demo_build.txt:7:08/03/2026  22:14             2,354 20260308_221600_trading_signal_landing_demo_index.html
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\landing_demo_build.txt:15:08/03/2026  18:13            16,129 miniapp_feed_2026-03-06.json
 succeeded in 2.36s:
# Trading Signal Social Templates

Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`

## Feed Snapshot

- Strategies available: `163`
- Open trades available: `1`
- Signals available: `4`
- Top strategy label fallback: `unknown`
- Open trade side fallback-ready sample: `SHORT` at `2.038825`

## Placeholder Rules

- Use `{{generated_at_utc}}` for freshness.
- Use `{{strategies_count}}`, `{{open_trades_count}}`, and `{{signals_count}}` for headline stats.
- Use `{{top_strategy_name}}` and `{{top_strategy_pair}}`; if the feed value is `unknown`, replace with `Top ranked strategy` and `multi-pair setup`.
- Use `{{open_trade_side}}` and `{{open_trade_entry}}`; if missing, replace with `live position` and `feed price`.
- Use `{{signal_trigger_text}}` and `{{signal_risk_note}}`; if the feed is generic, keep the copy outcome-focused instead of overclaiming.
 succeeded in 2.00s:
# Activity Log (continuous)

Format:
- `[YYYY-MM-DD HH:MM UTC] STATUS | Area | Action | Output/Evidence`

---

- [2026-03-08 19:05 UTC] STARTED | Logging | Continuous activity log initialized | `clawd_originated/artefacts/activity_log.md`
- [2026-03-08 19:05 UTC] INFO | Rule | Auto-proceed for build/create tasks; ask for destructive actions | user rule acknowledged
- [2026-03-08 19:05 UTC] DONE | Data feed | `miniapp_feed_extractor.py` executed for sample day | `.../clawd_originated/artefacts/miniapp_feed_2026-03-06.json`
- [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
- [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
- [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt

codex
I have enough context now. I’m going to create the IA artifact in `clawd_originated/artefacts/projects`, capture a validation artifact that proves the required section map exists, then I’ll update the lifecycle file so the plan, evidence inventory, validation log, and completion state all match the actual work.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Force 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts\\evidence\\trading_signal'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git status --short' in C:\Users\edebe\eds succeeded in 1.38s:

    Directory: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal

[32;1mMode   [0m[32;1m              LastWriteTime[0m[32;1m         Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
-a---          08/03/2026    18:13            140 extractor_run.txt
-a---          08/03/2026    22:15            800 landing_demo_build.txt
-a---          09/03/2026    17:13         149116 signal_card.png
-a---          09/03/2026    17:05         102634 signal_chart.png
-a---          18/03/2026    18:24            204 social_templates_validation.txt

 succeeded in 1.86s:
M  DataInsights/src/Constants.py
 M TradeApps
 M api_server_sql/main.py
 D grid_live_monitor.py
R  workstream/000_backlog/.keep -> workstream/000_epic/.keep
RD "workstream/000_backlog/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md" -> "workstream/000_epic/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md"
RD workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md -> workstream/000_epic/20260225_104010_live_market_data_pipeline_prompt.md
RD workstream/000_backlog/20260227_022357_sFX_Technical_Design_Brief_v2.md -> workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
AD workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
AD workstream/000_epic/20260313_165611_bizPA_epic.md
AD "workstream/000_epic/20260313_165611_unassigned_Autonomous Trading Signal Platform.md"
AD workstream/000_epic/20260313_165611_unassigned_bizPA.md
A  workstream/000_epic/bizPA_disccussion.txt
R  workstream/000_backlog/claude/.keep -> workstream/000_epic/claude/.keep
A  workstream/000_epic/claude/20260305_100142_claude_etrmui_etrui_processed.md
R  workstream/000_backlog/codex/.keep -> workstream/000_epic/codex/.keep
R  workstream/000_backlog/codex/20260303_152309_codex_afrix_build_prompt_processed.md -> workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_processed.md
A  workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_review.md
R  workstream/000_backlog/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md -> workstream/000_epic/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md
R  workstream/000_backlog/codex/20260304_142350_codex_linkage_verification_processed.md -> workstream/000_epic/codex/20260304_142350_codex_linkage_verification_processed.md
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"20260308_162710_trading_signal_mobile_landing_ia|mobile_landing_ia|trading_signal.*epic\" 'C:\\Users\\edebe\\eds\\workstream'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Force 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex' | Where-Object { "'$_.Name -like '"'*trading_signal*' } | Select-Object Name,LastWriteTime" in C:\Users\edebe\eds exited 1 in 2.59s:
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:41:Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:153:C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md:1:Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:721:Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:814:-Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:860:+Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1025:-Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1071:+Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1236:Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1274:-Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1320:+Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1509:-Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1555:+Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1735:-Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162720_trading_signal_social_templates.md.result.md:1781:+Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md:1:Source: trading_signal_miniapp epic
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md:36:- Command: cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md:40:claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
C:\Users\edebe\eds\workstream\100_backlog\gemini\20260310_120000_workstream_orchestrator_epic_task_review_screen.md:25:  - [x] Evidence: `workstream/verification/validate_epic_review.ps1` validated the updated handler on `http://127.0.0.1:8091`; output saved to `workstream/verification/epic_review_validation.json` shows `RootHasEpicReviewButton=true`, `EpicReviewHasBackLink=true`, `EpicReviewHasAllocateAction=true`, `EpicCount=3`, and a successful sample task payload for epic `autonomous_trading_signal_platform`. Access helper created at `workstream/verification/open_epic_review.ps1`, but direct `Start-Process` URL launch is denied in this sandbox.
C:\Users\edebe\eds\workstream\300_complete\20260319_162730_general_extract_backlog_unique_epics.md:19:  - Unique normalized references excluding placeholders (`Others`, `Direct user request in this session.`, `SKILL`, `trading_signal_miniapp epic`): `66`
C:\Users\edebe\eds\workstream\300_complete\codex\20260308_162720_trading_signal_social_templates.md:1:Source: trading_signal_miniapp epic
 succeeded in 2.51s:

[32;1mName                                                                                            [0m[32;1m LastWriteTime[0m
[32;1m----                                                                                            [0m [32;1m-------------[0m
20260308_162700_trading_signal_miniapp_feed_extractor.md                                         08/03/2026 16:47:50
20260308_162720_trading_signal_social_templates.md                                               18/03/2026 18:25:00
20260309_120060_autonomous_trading_signal_platform_workstreamG_initialize_mobile_project.md      10/03/2026 15:06:15
20260309_120061_autonomous_trading_signal_platform_workstreamG_implement_signal_feed.md          10/03/2026 11:04:28
20260309_120062_autonomous_trading_signal_platform_workstreamG_implement_strategy_leaderboard.md 10/03/2026 03:15:27
20260309_120063_autonomous_trading_signal_platform_workstreamG_implement_trade_history.md        10/03/2026 11:03:51
20260309_120064_autonomous_trading_signal_platform_workstreamG_implement_push_notifications.md   10/03/2026 11:03:35
20260309_120070_autonomous_trading_signal_platform_workstreamH_implement_event_tracking.md       10/03/2026 11:02:04
20260309_120071_autonomous_trading_signal_platform_workstreamH_create_growth_dashboard.md        10/03/2026 11:01:48
20260309_120080_autonomous_trading_signal_platform_workstreamI_create_system_dashboard.md        10/03/2026 02:59:32
20260309_120090_autonomous_trading_signal_platform_workstreamJ_enable_marketing_engine.md        10/03/2026 02:45:06
20260309_120091_autonomous_trading_signal_platform_workstreamJ_launch_landing_page.md            09/03/2026 23:23:28

codex
I found the sibling completed task for social templates. I’m using that as the baseline for how this lifecycle file should be structured and completed, then I’ll mirror the same standard for the IA artifact and completion metadata.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex\\20260308_162720_trading_signal_social_templates.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260308_162700_trading_signal_miniapp_feed_extractor.md'" in C:\Users\edebe\eds succeeded in 1.71s:
Source: trading_signal_miniapp epic

Task Summary
Create social templates for X, TikTok, and a daily recap tied to the miniapp feed, with copy that remains usable when the feed contains placeholder values.

Context
- Feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
- Evidence folder: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal`
- Project artefacts: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects`

Dependency
None

Plan
- [x] 1. Validate available feed counts for content placeholders
  - [x] Test: review `extractor_run.txt` contains strategies/open_trades/signals counts
  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` confirms `{"strategies": 163, "open_trades": 1, "signals": 4}`.
- [x] 2. Draft template set (X/TikTok/daily recap)
  - [x] Test: run a structural validation that each template section includes `Hook:`, `Data Slot:`, and `CTA:` and returns `overall=pass`
  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260318_181500_trading_signal_social_templates.md` created and `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\social_templates_validation.txt` recorded `overall=pass`.
 exited 1 in 1.70s:
[31;1mGet-Content: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-Content -Raw 'C:\Users\edebe\eds\workstream\200_inprogress\codex\[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mCannot find path 'C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162700_trading_signal_miniapp_feed_extractor.md' because it does not exist.[0m
codex
I’m at the edit step now. I’m adding a concrete IA/spec markdown artifact, then I’ll rewrite the lifecycle file so it records the deliverable path, captured evidence, validation command/results, and final state cleanly enough to move the task out of `200_inprogress`.
file update
A C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md
# Trading Signal Mobile Landing IA

Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`

## IA Goal

Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.

## Feed Snapshot

- Strategies available: `163`
- Open trades available: `1`
- Signals available: `4`
- Lead strategy fallback state: `unknown`
- Current open trade sample: `SHORT` at `2.038825`

## Placeholder Rules

- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
- Keep risk copy visible even when all commercial or performance fields are partial.
- Never present placeholder values as verified market claims.

## Section Map

### Hero

Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.

Primary content:
- Product label: `Trading Signal Miniapp`
- Timestamp: `meta.generated_at_utc`
- Summary line: derived from `meta.counts`
- Primary CTA: `Open live board`
- Secondary CTA: `Review next actions`

Component spec:
- Compact headline block with one-line positioning statement.
- Freshness chip showing last feed generation time.
- Two-button CTA row pinned above the fold.

Bound fields:
- `meta.generated_at_utc`
- `meta.counts.strategies`
- `meta.counts.open_trades`
- `meta.counts.signals`

### KPIs

Purpose: show the desk state in three compressed metric cards immediately below the hero.

Cards:
- `Strategies Scanned`: `meta.counts.strategies`
- `Open Trades`: `meta.counts.open_trades`
- `Signals Ready`: `meta.counts.signals`

Component spec:
- 3-card horizontal or 2x2 wrap layout for narrow screens.
- Large number, short label, and optional micro-caption.
- Use neutral/fallback wording when counts are zero.

Bound fields:
- `meta.counts.strategies`
- `meta.counts.open_trades`
- `meta.counts.signals`

### Top Strategies

Purpose: rank the most relevant setups and give enough context to decide whether to drill in.

Card count:
- Default: top 3 cards on landing, with link to full board.

Card fields:
- Strategy name: `strategies[].strategy_name`
- Pair: `strategies[].pair`
- Net today: `strategies[].net_today`
- Win rate: `strategies[].win_rate`
- Drawdown: `strategies[].drawdown`
- Confidence: `strategies[].confidence`
- Source badge: `strategies[].source`

Component spec:
- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
- Confidence and win rate become muted chips when null.
- A trailing chevron or `View setup` affordance signals navigation.

Fallback behavior:
- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.

### Open Trades

Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.

Card fields:
- Trade id: `open_trades[].trade_id`
- Strategy id: `open_trades[].strategy_id`
- Pair: `open_trades[].pair`
- Side: `open_trades[].side`
- Entry: `open_trades[].entry`
- Stop loss: `open_trades[].sl`
- Take profit: `open_trades[].tp`
- Unrealized PnL: `open_trades[].unrealized_pnl`
- Status: `open_trades[].status`

Component spec:
- Single prominent trade card when there is one active position.
- Side rendered as the primary badge (`LONG`/`SHORT`).
- Entry shown in large type, with SL/TP/PnL grouped below.
- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.

Empty state:
- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.

### Next Actions

Purpose: convert signals into a short list of follow-up actions without overclaiming precision.

Card count:
- Default: top 2 signal cards plus a `See all signals` affordance.

Card fields:
- Strategy id: `signals[].strategy_id`
- Pair: `signals[].pair`
- Bias: `signals[].bias`
- Trigger text: `signals[].trigger_text`
- Invalidation text: `signals[].invalidation_text`
- Risk note: `signals[].risk_note`
- Confidence: `signals[].confidence`

Component spec:
- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
- Trigger and invalidation copy stacked as short paragraphs.
- Risk note fixed at the bottom of each card.

Fallback behavior:
- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
- Null confidence should not block rendering; use `Analyst review required`.

### CTA

Purpose: close the landing page with a strong next step and product framing.

Primary CTA:
- `Open the live strategy board`

Secondary CTA:
- `Review risk notes before trading`

Component spec:
- Sticky bottom CTA bar or final full-width panel.
- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.

## Mobile Flow Order

1. Hero
2. KPIs
3. Top Strategies
4. Open Trades
5. Next Actions
6. CTA

## Card Design Rules

- Keep every card to one dominant data point and at most two secondary metrics.
- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
- Prefer progressive disclosure over dense tables.
- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
- Ensure all cards can collapse gracefully when fields are null or `unknown`.

## Data Binding Summary

| Section | Primary fields | Secondary fields | Fallback priority |
|---|---|---|---|
| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
| KPIs | `meta.counts.*` | none | Zero-state labels |
| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
| CTA | static copy | freshness/risk reminder | Validation reminder |

## Delivery Notes

- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.
apply_patch(auto_approved=true) exited 0 in 2.40s:
Success. Updated the following files:
A C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md
file update:
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

file update:
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

file update
M C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md
@@ -13,4 +13,5 @@
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
apply_patch(auto_approved=true) exited 0 in 1.03s:
Success. Updated the following files:
M C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md
file update:
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

file update:
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

codex
The IA artifact is in place. I’m running a structural validation now that checks the exact required sections and then I’ll fold that output back into the lifecycle evidence and completion state.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "@'
from pathlib import Path
path = Path(r'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts\\projects\\20260319_170500_trading_signal_mobile_landing_ia.md')
text = path.read_text(encoding='utf-8')
required = ['### Hero', '### KPIs', '### Top Strategies', '### Open Trades', '### Next Actions', '### CTA']
missing = [item for item in required if item not in text]
print(path)
for item in required:
    print(f'{item}: ' + ('ok' if item in text else 'missing'))
print('overall=' + ('pass' if not missing else 'fail'))
'@ | python - | Tee-Object -FilePath 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts\\evidence\\trading_signal\\mobile_landing_ia_validation.txt'" in C:\Users\edebe\eds succeeded in 2.20s:
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md
### Hero: ok
### KPIs: ok
### Top Strategies: ok
### Open Trades: ok
### Next Actions: ok
### CTA: ok
overall=pass
file update:
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

codex
I’ve got the pass artifact. I’m rewriting the task file now so every checklist item, evidence record, validation command, and completion timestamp is explicit before I move it into `300_complete`.
file update
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md
Source: trading_signal_miniapp epic

Task Summary
Define mobile IA/component layout for mini-app using miniapp_feed fields.

Context
- Feed: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
- Evidence folder: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal

Plan
- [x] 1. Validate feed keys used by UI
  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs counts dict
  - [x] Evidence: `clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
- [ ] 2. Draft IA sections and card specs
  - [ ] Test: Section map includes Hero/KPIs/Top Strategies/Open Trades/Next Actions/CTA
  - [ ] Evidence: IA doc saved under clawd_originated\artefacts\projects

Implementation Log
- 2026-03-08 18:15: Lifecycle template enforced; evidence path set to clawd_originated folder.

Changes Made
- Replaced placeholder with full lifecycle structure and explicit tests/evidence paths.

Validation
- Feed extractor run evidence recorded in clawd_originated evidence folder.

Risks/Notes
- Awaiting IA artifact generation.

Completion Status
- In progress


## Execution Evidence
- Agent lane: claude
- Command: cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
- Return code: 0
- Stdout:
```text
claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
```


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 1.49s:
Success. Updated the following files:
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md
file update:
diff --git a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
deleted file mode 100644
index 4b6d90ce24ac55c544bdee378f4b2773d4d022ec..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
+++ /dev/null
@@ -1,46 +0,0 @@
-Source: trading_signal_miniapp epic
-
-Task Summary
-Define mobile IA/component layout for mini-app using miniapp_feed fields.
-
-Context
-- Feed: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
-- Evidence folder: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal
-
-Plan
-- [x] 1. Validate feed keys used by UI
-  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs counts dict
-  - [x] Evidence: `clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
-- [ ] 2. Draft IA sections and card specs
-  - [ ] Test: Section map includes Hero/KPIs/Top Strategies/Open Trades/Next Actions/CTA
-  - [ ] Evidence: IA doc saved under clawd_originated\artefacts\projects
-
-Implementation Log
-- 2026-03-08 18:15: Lifecycle template enforced; evidence path set to clawd_originated folder.
-
-Changes Made
-- Replaced placeholder with full lifecycle structure and explicit tests/evidence paths.
-
-Validation
-- Feed extractor run evidence recorded in clawd_originated evidence folder.
-
-Risks/Notes
-- Awaiting IA artifact generation.
-
-Completion Status
-- In progress
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

file update:
diff --git a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
deleted file mode 100644
index 4b6d90ce24ac55c544bdee378f4b2773d4d022ec..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
+++ /dev/null
@@ -1,46 +0,0 @@
-Source: trading_signal_miniapp epic
-
-Task Summary
-Define mobile IA/component layout for mini-app using miniapp_feed fields.
-
-Context
-- Feed: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
-- Evidence folder: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal
-
-Plan
-- [x] 1. Validate feed keys used by UI
-  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs counts dict
-  - [x] Evidence: `clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
-- [ ] 2. Draft IA sections and card specs
-  - [ ] Test: Section map includes Hero/KPIs/Top Strategies/Open Trades/Next Actions/CTA
-  - [ ] Evidence: IA doc saved under clawd_originated\artefacts\projects
-
-Implementation Log
-- 2026-03-08 18:15: Lifecycle template enforced; evidence path set to clawd_originated folder.
-
-Changes Made
-- Replaced placeholder with full lifecycle structure and explicit tests/evidence paths.
-
-Validation
-- Feed extractor run evidence recorded in clawd_originated evidence folder.
-
-Risks/Notes
-- Awaiting IA artifact generation.
-
-Completion Status
-- In progress
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

file update
A C:\Users\edebe\eds\workstream\300_complete\codex\20260308_162710_trading_signal_mobile_landing_ia.md
Source: trading_signal_miniapp epic

Task Summary
Define the mobile information architecture and component layout for the trading signal mini-app landing experience using the extracted `miniapp_feed` fields, with explicit fallback behavior for sparse or placeholder data.

Context
- Feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
- Evidence folder: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal`
- Project artefacts: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects`

Dependency
None

Plan
- [x] 1. Validate feed keys used by UI
  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs the counts dict used by the landing summary and KPI cards.
  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` confirms `{"strategies": 163, "open_trades": 1, "signals": 4}`.
- [x] 2. Draft IA sections and card specs
  - [x] Test: run a structural validation that confirms the IA doc contains `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`, and returns `overall=pass`.
  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` created and `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` recorded `overall=pass`.

Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: manual_verification
  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
  - Objective-Proved: The IA deliverable exists at a stable review path and includes the requested mobile section map, component layout, field bindings, and fallback rules.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt`
  - Objective-Proved: The required landing sections and CTA structure were validated and the structural check passed.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
  - Objective-Proved: The IA was grounded in the extracted feed counts before the layout and card specs were drafted.
  - Status: captured

Implementation Log
- 2026-03-08 18:15: Lifecycle template initially enforced and evidence path set to the `clawd_originated` artefact folder.
- 2026-03-19 16:58: Reviewed the extracted `miniapp_feed_2026-03-06.json` structure and confirmed the landing layer needed to be count-driven because strategy and pair fields still contain placeholder `unknown` values.
- 2026-03-19 17:05: Created the mobile landing IA artefact with hero, KPI, top strategies, open trades, next actions, and CTA sections, plus data-binding and fallback rules.
- 2026-03-19 17:06: Ran structural validation against the IA artefact and saved the pass output in the trading signal evidence folder.
- 2026-03-19 17:07: Updated the lifecycle document with normalized evidence entries, validation results, and completion status, then moved the task into `300_complete`.

Changes Made
- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` with:
  - mobile landing section map for `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`
  - component/card specifications for each section
  - feed-field binding guidance for strategies, open trades, signals, and meta counts
  - explicit placeholder handling for `unknown`, `null`, and generic trigger content
  - mobile flow order and card design rules
- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` with structural validation output.
- Appended the IA delivery entry to `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md`.
- Moved this lifecycle file from `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md` to `C:\Users\edebe\eds\workstream\300_complete\codex\20260308_162710_trading_signal_mobile_landing_ia.md` after completion and validation.

Validation
- Reviewed `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` and confirmed the baseline feed counts used in the landing summary and KPI design.
- Ran:
  - `@' ... '@ | python - | Tee-Object -FilePath 'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt'`
  - Target file: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
  - Output summary: `### Hero: ok`, `### KPIs: ok`, `### Top Strategies: ok`, `### Open Trades: ok`, `### Next Actions: ok`, `### CTA: ok`, `overall=pass`
- Auto-acceptance criteria met:
  - `Objective-Delivery-Coverage: 100%`
  - `Auto-Acceptance: true`

Risks/Notes
- The current sample feed still contains repeated strategies, placeholder pair labels, and null performance fields, so the IA intentionally emphasizes desk state, risk framing, and graceful degradation instead of precise instrument claims.
- This task produced architecture and component guidance, not a rendered application implementation. The artefact is ready to drive downstream UI build work.

Completion Status
- Complete as of 2026-03-19 17:07

## Execution Evidence
- Agent lane: claude
- Command: `cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md`
- Return code: `0`
- Stdout:
```text
claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
```

## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 1.05s:
Success. Updated the following files:
A C:\Users\edebe\eds\workstream\300_complete\codex\20260308_162710_trading_signal_mobile_landing_ia.md
file update:
diff --git a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
deleted file mode 100644
index 4b6d90ce24ac55c544bdee378f4b2773d4d022ec..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
+++ /dev/null
@@ -1,46 +0,0 @@
-Source: trading_signal_miniapp epic
-
-Task Summary
-Define mobile IA/component layout for mini-app using miniapp_feed fields.
-
-Context
-- Feed: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
-- Evidence folder: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal
-
-Plan
-- [x] 1. Validate feed keys used by UI
-  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs counts dict
-  - [x] Evidence: `clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
-- [ ] 2. Draft IA sections and card specs
-  - [ ] Test: Section map includes Hero/KPIs/Top Strategies/Open Trades/Next Actions/CTA
-  - [ ] Evidence: IA doc saved under clawd_originated\artefacts\projects
-
-Implementation Log
-- 2026-03-08 18:15: Lifecycle template enforced; evidence path set to clawd_originated folder.
-
-Changes Made
-- Replaced placeholder with full lifecycle structure and explicit tests/evidence paths.
-
-Validation
-- Feed extractor run evidence recorded in clawd_originated evidence folder.
-
-Risks/Notes
-- Awaiting IA artifact generation.
-
-Completion Status
-- In progress
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..56ac037439179a595dfbdde2fc66efd4434b8742
--- /dev/null
+++ b/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,84 @@
+Source: trading_signal_miniapp epic
+
+Task Summary
+Define the mobile information architecture and component layout for the trading signal mini-app landing experience using the extracted `miniapp_feed` fields, with explicit fallback behavior for sparse or placeholder data.
+
+Context
+- Feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+- Evidence folder: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal`
+- Project artefacts: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects`
+
+Dependency
+None
+
+Plan
+- [x] 1. Validate feed keys used by UI
+  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs the counts dict used by the landing summary and KPI cards.
+  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` confirms `{"strategies": 163, "open_trades": 1, "signals": 4}`.
+- [x] 2. Draft IA sections and card specs
+  - [x] Test: run a structural validation that confirms the IA doc contains `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`, and returns `overall=pass`.
+  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` created and `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` recorded `overall=pass`.
+
+Evidence
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: true
+- Evidence-Type: manual_verification
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
+  - Objective-Proved: The IA deliverable exists at a stable review path and includes the requested mobile section map, component layout, field bindings, and fallback rules.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt`
+  - Objective-Proved: The required landing sections and CTA structure were validated and the structural check passed.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
+  - Objective-Proved: The IA was grounded in the extracted feed counts before the layout and card specs were drafted.
+  - Status: captured
+
+Implementation Log
+- 2026-03-08 18:15: Lifecycle template initially enforced and evidence path set to the `clawd_originated` artefact folder.
+- 2026-03-19 16:58: Reviewed the extracted `miniapp_feed_2026-03-06.json` structure and confirmed the landing layer needed to be count-driven because strategy and pair fields still contain placeholder `unknown` values.
+- 2026-03-19 17:05: Created the mobile landing IA artefact with hero, KPI, top strategies, open trades, next actions, and CTA sections, plus data-binding and fallback rules.
+- 2026-03-19 17:06: Ran structural validation against the IA artefact and saved the pass output in the trading signal evidence folder.
+- 2026-03-19 17:07: Updated the lifecycle document with normalized evidence entries, validation results, and completion status, then moved the task into `300_complete`.
+
+Changes Made
+- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` with:
+  - mobile landing section map for `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`
+  - component/card specifications for each section
+  - feed-field binding guidance for strategies, open trades, signals, and meta counts
+  - explicit placeholder handling for `unknown`, `null`, and generic trigger content
+  - mobile flow order and card design rules
+- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` with structural validation output.
+- Appended the IA delivery entry to `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md`.
+- Moved this lifecycle file from `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md` to `C:\Users\edebe\eds\workstream\300_complete\codex\20260308_162710_trading_signal_mobile_landing_ia.md` after completion and validation.
+
+Validation
+- Reviewed `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` and confirmed the baseline feed counts used in the landing summary and KPI design.
+- Ran:
+  - `@' ... '@ | python - | Tee-Object -FilePath 'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt'`
+  - Target file: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
+  - Output summary: `### Hero: ok`, `### KPIs: ok`, `### Top Strategies: ok`, `### Open Trades: ok`, `### Next Actions: ok`, `### CTA: ok`, `overall=pass`
+- Auto-acceptance criteria met:
+  - `Objective-Delivery-Coverage: 100%`
+  - `Auto-Acceptance: true`
+
+Risks/Notes
+- The current sample feed still contains repeated strategies, placeholder pair labels, and null performance fields, so the IA intentionally emphasizes desk state, risk framing, and graceful degradation instead of precise instrument claims.
+- This task produced architecture and component guidance, not a rendered application implementation. The artefact is ready to drive downstream UI build work.
+
+Completion Status
+- Complete as of 2026-03-19 17:07
+
+## Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md`
+- Return code: `0`
+- Stdout:
+```text
+claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
+```
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

file update:
diff --git a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
deleted file mode 100644
index 4b6d90ce24ac55c544bdee378f4b2773d4d022ec..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
+++ /dev/null
@@ -1,46 +0,0 @@
-Source: trading_signal_miniapp epic
-
-Task Summary
-Define mobile IA/component layout for mini-app using miniapp_feed fields.
-
-Context
-- Feed: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
-- Evidence folder: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal
-
-Plan
-- [x] 1. Validate feed keys used by UI
-  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs counts dict
-  - [x] Evidence: `clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
-- [ ] 2. Draft IA sections and card specs
-  - [ ] Test: Section map includes Hero/KPIs/Top Strategies/Open Trades/Next Actions/CTA
-  - [ ] Evidence: IA doc saved under clawd_originated\artefacts\projects
-
-Implementation Log
-- 2026-03-08 18:15: Lifecycle template enforced; evidence path set to clawd_originated folder.
-
-Changes Made
-- Replaced placeholder with full lifecycle structure and explicit tests/evidence paths.
-
-Validation
-- Feed extractor run evidence recorded in clawd_originated evidence folder.
-
-Risks/Notes
-- Awaiting IA artifact generation.
-
-Completion Status
-- In progress
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..56ac037439179a595dfbdde2fc66efd4434b8742
--- /dev/null
+++ b/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,84 @@
+Source: trading_signal_miniapp epic
+
+Task Summary
+Define the mobile information architecture and component layout for the trading signal mini-app landing experience using the extracted `miniapp_feed` fields, with explicit fallback behavior for sparse or placeholder data.
+
+Context
+- Feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+- Evidence folder: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal`
+- Project artefacts: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects`
+
+Dependency
+None
+
+Plan
+- [x] 1. Validate feed keys used by UI
+  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs the counts dict used by the landing summary and KPI cards.
+  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` confirms `{"strategies": 163, "open_trades": 1, "signals": 4}`.
+- [x] 2. Draft IA sections and card specs
+  - [x] Test: run a structural validation that confirms the IA doc contains `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`, and returns `overall=pass`.
+  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` created and `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` recorded `overall=pass`.
+
+Evidence
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: true
+- Evidence-Type: manual_verification
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
+  - Objective-Proved: The IA deliverable exists at a stable review path and includes the requested mobile section map, component layout, field bindings, and fallback rules.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt`
+  - Objective-Proved: The required landing sections and CTA structure were validated and the structural check passed.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
+  - Objective-Proved: The IA was grounded in the extracted feed counts before the layout and card specs were drafted.
+  - Status: captured
+
+Implementation Log
+- 2026-03-08 18:15: Lifecycle template initially enforced and evidence path set to the `clawd_originated` artefact folder.
+- 2026-03-19 16:58: Reviewed the extracted `miniapp_feed_2026-03-06.json` structure and confirmed the landing layer needed to be count-driven because strategy and pair fields still contain placeholder `unknown` values.
+- 2026-03-19 17:05: Created the mobile landing IA artefact with hero, KPI, top strategies, open trades, next actions, and CTA sections, plus data-binding and fallback rules.
+- 2026-03-19 17:06: Ran structural validation against the IA artefact and saved the pass output in the trading signal evidence folder.
+- 2026-03-19 17:07: Updated the lifecycle document with normalized evidence entries, validation results, and completion status, then moved the task into `300_complete`.
+
+Changes Made
+- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` with:
+  - mobile landing section map for `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`
+  - component/card specifications for each section
+  - feed-field binding guidance for strategies, open trades, signals, and meta counts
+  - explicit placeholder handling for `unknown`, `null`, and generic trigger content
+  - mobile flow order and card design rules
+- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` with structural validation output.
+- Appended the IA delivery entry to `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md`.
+- Moved this lifecycle file from `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md` to `C:\Users\edebe\eds\workstream\300_complete\codex\20260308_162710_trading_signal_mobile_landing_ia.md` after completion and validation.
+
+Validation
+- Reviewed `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` and confirmed the baseline feed counts used in the landing summary and KPI design.
+- Ran:
+  - `@' ... '@ | python - | Tee-Object -FilePath 'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt'`
+  - Target file: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
+  - Output summary: `### Hero: ok`, `### KPIs: ok`, `### Top Strategies: ok`, `### Open Trades: ok`, `### Next Actions: ok`, `### CTA: ok`, `overall=pass`
+- Auto-acceptance criteria met:
+  - `Objective-Delivery-Coverage: 100%`
+  - `Auto-Acceptance: true`
+
+Risks/Notes
+- The current sample feed still contains repeated strategies, placeholder pair labels, and null performance fields, so the IA intentionally emphasizes desk state, risk framing, and graceful degradation instead of precise instrument claims.
+- This task produced architecture and component guidance, not a rendered application implementation. The artefact is ready to drive downstream UI build work.
+
+Completion Status
+- Complete as of 2026-03-19 17:07
+
+## Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md`
+- Return code: `0`
+- Stdout:
+```text
+claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
+```
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

codex
The lifecycle file has been moved to `300_complete` and marked complete under auto-acceptance. I’m doing one last pass on the resulting files and git status so I can close this cleanly with the exact artifact paths and validation outcome.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\clawd_originated\\artefacts\\evidence\\trading_signal\\mobile_landing_ia_validation.txt'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git status --short -- 'workstream/clawd_originated/artefacts/activity_log.md' 'workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md' 'workstream/clawd_originated/artefacts/evidence/trading_signal/mobile_landing_ia_validation.txt' 'workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md' 'workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex\\20260308_162710_trading_signal_mobile_landing_ia.md'" in C:\Users\edebe\eds succeeded in 2.04s:
Source: trading_signal_miniapp epic

Task Summary
Define the mobile information architecture and component layout for the trading signal mini-app landing experience using the extracted `miniapp_feed` fields, with explicit fallback behavior for sparse or placeholder data.

Context
- Feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
- Evidence folder: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal`
- Project artefacts: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects`

Dependency
None

Plan
- [x] 1. Validate feed keys used by UI
  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs the counts dict used by the landing summary and KPI cards.
  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` confirms `{"strategies": 163, "open_trades": 1, "signals": 4}`.
- [x] 2. Draft IA sections and card specs
  - [x] Test: run a structural validation that confirms the IA doc contains `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`, and returns `overall=pass`.
  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` created and `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` recorded `overall=pass`.
 succeeded in 2.20s:
C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md
### Hero: ok
### KPIs: ok
### Top Strategies: ok
### Open Trades: ok
### Next Actions: ok
### CTA: ok
overall=pass

 succeeded in 2.34s:
AM workstream/clawd_originated/artefacts/activity_log.md
?? workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
?? workstream/clawd_originated/artefacts/evidence/trading_signal/mobile_landing_ia_validation.txt
?? workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
file update:
diff --git a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
deleted file mode 100644
index 4b6d90ce24ac55c544bdee378f4b2773d4d022ec..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
+++ /dev/null
@@ -1,46 +0,0 @@
-Source: trading_signal_miniapp epic
-
-Task Summary
-Define mobile IA/component layout for mini-app using miniapp_feed fields.
-
-Context
-- Feed: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
-- Evidence folder: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal
-
-Plan
-- [x] 1. Validate feed keys used by UI
-  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs counts dict
-  - [x] Evidence: `clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
-- [ ] 2. Draft IA sections and card specs
-  - [ ] Test: Section map includes Hero/KPIs/Top Strategies/Open Trades/Next Actions/CTA
-  - [ ] Evidence: IA doc saved under clawd_originated\artefacts\projects
-
-Implementation Log
-- 2026-03-08 18:15: Lifecycle template enforced; evidence path set to clawd_originated folder.
-
-Changes Made
-- Replaced placeholder with full lifecycle structure and explicit tests/evidence paths.
-
-Validation
-- Feed extractor run evidence recorded in clawd_originated evidence folder.
-
-Risks/Notes
-- Awaiting IA artifact generation.
-
-Completion Status
-- In progress
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..56ac037439179a595dfbdde2fc66efd4434b8742
--- /dev/null
+++ b/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,84 @@
+Source: trading_signal_miniapp epic
+
+Task Summary
+Define the mobile information architecture and component layout for the trading signal mini-app landing experience using the extracted `miniapp_feed` fields, with explicit fallback behavior for sparse or placeholder data.
+
+Context
+- Feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+- Evidence folder: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal`
+- Project artefacts: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects`
+
+Dependency
+None
+
+Plan
+- [x] 1. Validate feed keys used by UI
+  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs the counts dict used by the landing summary and KPI cards.
+  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` confirms `{"strategies": 163, "open_trades": 1, "signals": 4}`.
+- [x] 2. Draft IA sections and card specs
+  - [x] Test: run a structural validation that confirms the IA doc contains `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`, and returns `overall=pass`.
+  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` created and `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` recorded `overall=pass`.
+
+Evidence
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: true
+- Evidence-Type: manual_verification
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
+  - Objective-Proved: The IA deliverable exists at a stable review path and includes the requested mobile section map, component layout, field bindings, and fallback rules.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt`
+  - Objective-Proved: The required landing sections and CTA structure were validated and the structural check passed.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
+  - Objective-Proved: The IA was grounded in the extracted feed counts before the layout and card specs were drafted.
+  - Status: captured
+
+Implementation Log
+- 2026-03-08 18:15: Lifecycle template initially enforced and evidence path set to the `clawd_originated` artefact folder.
+- 2026-03-19 16:58: Reviewed the extracted `miniapp_feed_2026-03-06.json` structure and confirmed the landing layer needed to be count-driven because strategy and pair fields still contain placeholder `unknown` values.
+- 2026-03-19 17:05: Created the mobile landing IA artefact with hero, KPI, top strategies, open trades, next actions, and CTA sections, plus data-binding and fallback rules.
+- 2026-03-19 17:06: Ran structural validation against the IA artefact and saved the pass output in the trading signal evidence folder.
+- 2026-03-19 17:07: Updated the lifecycle document with normalized evidence entries, validation results, and completion status, then moved the task into `300_complete`.
+
+Changes Made
+- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` with:
+  - mobile landing section map for `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`
+  - component/card specifications for each section
+  - feed-field binding guidance for strategies, open trades, signals, and meta counts
+  - explicit placeholder handling for `unknown`, `null`, and generic trigger content
+  - mobile flow order and card design rules
+- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` with structural validation output.
+- Appended the IA delivery entry to `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md`.
+- Moved this lifecycle file from `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md` to `C:\Users\edebe\eds\workstream\300_complete\codex\20260308_162710_trading_signal_mobile_landing_ia.md` after completion and validation.
+
+Validation
+- Reviewed `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` and confirmed the baseline feed counts used in the landing summary and KPI design.
+- Ran:
+  - `@' ... '@ | python - | Tee-Object -FilePath 'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt'`
+  - Target file: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
+  - Output summary: `### Hero: ok`, `### KPIs: ok`, `### Top Strategies: ok`, `### Open Trades: ok`, `### Next Actions: ok`, `### CTA: ok`, `overall=pass`
+- Auto-acceptance criteria met:
+  - `Objective-Delivery-Coverage: 100%`
+  - `Auto-Acceptance: true`
+
+Risks/Notes
+- The current sample feed still contains repeated strategies, placeholder pair labels, and null performance fields, so the IA intentionally emphasizes desk state, risk framing, and graceful degradation instead of precise instrument claims.
+- This task produced architecture and component guidance, not a rendered application implementation. The artefact is ready to drive downstream UI build work.
+
+Completion Status
+- Complete as of 2026-03-19 17:07
+
+## Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md`
+- Return code: `0`
+- Stdout:
+```text
+claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
+```
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

codex
Executed end-to-end. The IA artifact is at [20260319_170500_trading_signal_mobile_landing_ia.md](C:/Users/edebe/eds/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md), the validation output is at [mobile_landing_ia_validation.txt](C:/Users/edebe/eds/workstream/clawd_originated/artefacts/evidence/trading_signal/mobile_landing_ia_validation.txt), and the lifecycle file was updated and moved to [20260308_162710_trading_signal_mobile_landing_ia.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md).

The deliverable now defines the mobile section map for Hero, KPIs, Top Strategies, Open Trades, Next Actions, and CTA, including field bindings and fallback rules for `unknown`/`null` feed data. I also appended the delivery to [activity_log.md](C:/Users/edebe/eds/workstream/clawd_originated/artefacts/activity_log.md).

Validation passed: `overall=pass` with all required sections present in the IA doc. I did not commit changes.
file update:
diff --git a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
deleted file mode 100644
index 4b6d90ce24ac55c544bdee378f4b2773d4d022ec..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260308_162710_trading_signal_mobile_landing_ia.md
+++ /dev/null
@@ -1,46 +0,0 @@
-Source: trading_signal_miniapp epic
-
-Task Summary
-Define mobile IA/component layout for mini-app using miniapp_feed fields.
-
-Context
-- Feed: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json
-- Evidence folder: C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal
-
-Plan
-- [x] 1. Validate feed keys used by UI
-  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs counts dict
-  - [x] Evidence: `clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
-- [ ] 2. Draft IA sections and card specs
-  - [ ] Test: Section map includes Hero/KPIs/Top Strategies/Open Trades/Next Actions/CTA
-  - [ ] Evidence: IA doc saved under clawd_originated\artefacts\projects
-
-Implementation Log
-- 2026-03-08 18:15: Lifecycle template enforced; evidence path set to clawd_originated folder.
-
-Changes Made
-- Replaced placeholder with full lifecycle structure and explicit tests/evidence paths.
-
-Validation
-- Feed extractor run evidence recorded in clawd_originated evidence folder.
-
-Risks/Notes
-- Awaiting IA artifact generation.
-
-Completion Status
-- In progress
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md b/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..56ac037439179a595dfbdde2fc66efd4434b8742
--- /dev/null
+++ b/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,84 @@
+Source: trading_signal_miniapp epic
+
+Task Summary
+Define the mobile information architecture and component layout for the trading signal mini-app landing experience using the extracted `miniapp_feed` fields, with explicit fallback behavior for sparse or placeholder data.
+
+Context
+- Feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+- Evidence folder: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal`
+- Project artefacts: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects`
+
+Dependency
+None
+
+Plan
+- [x] 1. Validate feed keys used by UI
+  - [x] Test: `python -c "import json;d=json.load(open(r'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json'));print(d['meta']['counts'])"` outputs the counts dict used by the landing summary and KPI cards.
+  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` confirms `{"strategies": 163, "open_trades": 1, "signals": 4}`.
+- [x] 2. Draft IA sections and card specs
+  - [x] Test: run a structural validation that confirms the IA doc contains `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`, and returns `overall=pass`.
+  - [x] Evidence: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` created and `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` recorded `overall=pass`.
+
+Evidence
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: true
+- Evidence-Type: manual_verification
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
+  - Objective-Proved: The IA deliverable exists at a stable review path and includes the requested mobile section map, component layout, field bindings, and fallback rules.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt`
+  - Objective-Proved: The required landing sections and CTA structure were validated and the structural check passed.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt`
+  - Objective-Proved: The IA was grounded in the extracted feed counts before the layout and card specs were drafted.
+  - Status: captured
+
+Implementation Log
+- 2026-03-08 18:15: Lifecycle template initially enforced and evidence path set to the `clawd_originated` artefact folder.
+- 2026-03-19 16:58: Reviewed the extracted `miniapp_feed_2026-03-06.json` structure and confirmed the landing layer needed to be count-driven because strategy and pair fields still contain placeholder `unknown` values.
+- 2026-03-19 17:05: Created the mobile landing IA artefact with hero, KPI, top strategies, open trades, next actions, and CTA sections, plus data-binding and fallback rules.
+- 2026-03-19 17:06: Ran structural validation against the IA artefact and saved the pass output in the trading signal evidence folder.
+- 2026-03-19 17:07: Updated the lifecycle document with normalized evidence entries, validation results, and completion status, then moved the task into `300_complete`.
+
+Changes Made
+- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md` with:
+  - mobile landing section map for `Hero`, `KPIs`, `Top Strategies`, `Open Trades`, `Next Actions`, and `CTA`
+  - component/card specifications for each section
+  - feed-field binding guidance for strategies, open trades, signals, and meta counts
+  - explicit placeholder handling for `unknown`, `null`, and generic trigger content
+  - mobile flow order and card design rules
+- Added `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt` with structural validation output.
+- Appended the IA delivery entry to `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\activity_log.md`.
+- Moved this lifecycle file from `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260308_162710_trading_signal_mobile_landing_ia.md` to `C:\Users\edebe\eds\workstream\300_complete\codex\20260308_162710_trading_signal_mobile_landing_ia.md` after completion and validation.
+
+Validation
+- Reviewed `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\extractor_run.txt` and confirmed the baseline feed counts used in the landing summary and KPI design.
+- Ran:
+  - `@' ... '@ | python - | Tee-Object -FilePath 'C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\mobile_landing_ia_validation.txt'`
+  - Target file: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\projects\20260319_170500_trading_signal_mobile_landing_ia.md`
+  - Output summary: `### Hero: ok`, `### KPIs: ok`, `### Top Strategies: ok`, `### Open Trades: ok`, `### Next Actions: ok`, `### CTA: ok`, `overall=pass`
+- Auto-acceptance criteria met:
+  - `Objective-Delivery-Coverage: 100%`
+  - `Auto-Acceptance: true`
+
+Risks/Notes
+- The current sample feed still contains repeated strategies, placeholder pair labels, and null performance fields, so the IA intentionally emphasizes desk state, risk framing, and graceful degradation instead of precise instrument claims.
+- This task produced architecture and component guidance, not a rendered application implementation. The artefact is ready to drive downstream UI build work.
+
+Completion Status
+- Complete as of 2026-03-19 17:07
+
+## Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260308_162710_trading_signal_mobile_landing_ia.md`
+- Return code: `0`
+- Stdout:
+```text
+claude processing 20260308_162710_trading_signal_mobile_landing_ia.md
+```
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/clawd_originated/artefacts/activity_log.md b/workstream/clawd_originated/artefacts/activity_log.md
index 7d2debafc06a1b45e41d2547872c062d2f2d65d0..42b8e943c8368b0f8b0d8ab8047aed4cf2bfc285
--- a/workstream/clawd_originated/artefacts/activity_log.md
+++ b/workstream/clawd_originated/artefacts/activity_log.md
@@ -11,6 +11,7 @@
 - [2026-03-08 19:05 UTC] EVIDENCE | Data feed | Extractor run output captured | `.../clawd_originated/artefacts/evidence/trading_signal/extractor_run.txt`
 - [2026-03-08 19:05 UTC] IN_PROGRESS | Landing page | Building first mobile demo page | target: `clawd_originated/artefacts/projects`
 - [2026-03-08 19:48 UTC] STATUS | Landing page | No demo artifact generated yet; extractor completed; resuming build now | blocker was execution lag, not infra
-- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
-- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
-- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-08 22:15 UTC] DONE | Landing page | Demo HTML created and feed copied to projects folder | EDS: clawd_originated/artefacts/projects/20260308_221600_trading_signal_landing_demo_index.html
+- [2026-03-08 22:15 UTC] EVIDENCE | Landing page | Build evidence captured with run command | EDS: clawd_originated/artefacts/evidence/trading_signal/landing_demo_build.txt
+- [2026-03-18 18:15 UTC] DONE | Social templates | Created X/TikTok/daily recap template pack and captured structural validation | EDS: clawd_originated/artefacts/projects/20260318_181500_trading_signal_social_templates.md; evidence: clawd_originated/artefacts/evidence/trading_signal/social_templates_validation.txt
+- [2026-03-19 17:05 UTC] DONE | Mobile IA | Created mobile landing IA and card specification doc for the trading signal miniapp | EDS: clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
diff --git a/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
new file mode 100644
index 0000000000000000000000000000000000000000..c903b109c92ea94b16c67cfbfc8390ebb57b788c
--- /dev/null
+++ b/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md
@@ -0,0 +1,188 @@
+# Trading Signal Mobile Landing IA
+
+Source feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
+Generated from feed timestamp: `2026-03-08T18:13:40.484589+00:00`
+
+## IA Goal
+
+Define a mobile-first landing structure that turns the extracted miniapp feed into a clear, swipeable summary of desk state. The layout prioritizes fast scan value, graceful fallback for placeholder data, and a direct path into the ranked strategy board.
+
+## Feed Snapshot
+
+- Strategies available: `163`
+- Open trades available: `1`
+- Signals available: `4`
+- Lead strategy fallback state: `unknown`
+- Current open trade sample: `SHORT` at `2.038825`
+
+## Placeholder Rules
+
+- Replace strategy or pair value `unknown` with `Top ranked setup` and `multi-pair coverage`.
+- Replace missing confidence, win rate, drawdown, or PnL with `Not available yet`.
+- Replace generic trigger copy (`See strategy conditions`) with action framing such as `Open details to review live trigger logic`.
+- Keep risk copy visible even when all commercial or performance fields are partial.
+- Never present placeholder values as verified market claims.
+
+## Section Map
+
+### Hero
+
+Purpose: establish what the product is, when the feed was last generated, and what the trader can do next.
+
+Primary content:
+- Product label: `Trading Signal Miniapp`
+- Timestamp: `meta.generated_at_utc`
+- Summary line: derived from `meta.counts`
+- Primary CTA: `Open live board`
+- Secondary CTA: `Review next actions`
+
+Component spec:
+- Compact headline block with one-line positioning statement.
+- Freshness chip showing last feed generation time.
+- Two-button CTA row pinned above the fold.
+
+Bound fields:
+- `meta.generated_at_utc`
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### KPIs
+
+Purpose: show the desk state in three compressed metric cards immediately below the hero.
+
+Cards:
+- `Strategies Scanned`: `meta.counts.strategies`
+- `Open Trades`: `meta.counts.open_trades`
+- `Signals Ready`: `meta.counts.signals`
+
+Component spec:
+- 3-card horizontal or 2x2 wrap layout for narrow screens.
+- Large number, short label, and optional micro-caption.
+- Use neutral/fallback wording when counts are zero.
+
+Bound fields:
+- `meta.counts.strategies`
+- `meta.counts.open_trades`
+- `meta.counts.signals`
+
+### Top Strategies
+
+Purpose: rank the most relevant setups and give enough context to decide whether to drill in.
+
+Card count:
+- Default: top 3 cards on landing, with link to full board.
+
+Card fields:
+- Strategy name: `strategies[].strategy_name`
+- Pair: `strategies[].pair`
+- Net today: `strategies[].net_today`
+- Win rate: `strategies[].win_rate`
+- Drawdown: `strategies[].drawdown`
+- Confidence: `strategies[].confidence`
+- Source badge: `strategies[].source`
+
+Component spec:
+- Each card shows strategy title, pair/fallback pair, one primary metric (`net_today`), and two secondary metrics.
+- Confidence and win rate become muted chips when null.
+- A trailing chevron or `View setup` affordance signals navigation.
+
+Fallback behavior:
+- If all metrics except name are null, keep the card but collapse to `Desk-ranked strategy awaiting enriched metrics`.
+- Deduplicate repeated strategy IDs before display if the UI layer supports it; otherwise cap repeated cards visually.
+
+### Open Trades
+
+Purpose: surface active exposure with direct awareness of side, entry, and missing risk controls.
+
+Card fields:
+- Trade id: `open_trades[].trade_id`
+- Strategy id: `open_trades[].strategy_id`
+- Pair: `open_trades[].pair`
+- Side: `open_trades[].side`
+- Entry: `open_trades[].entry`
+- Stop loss: `open_trades[].sl`
+- Take profit: `open_trades[].tp`
+- Unrealized PnL: `open_trades[].unrealized_pnl`
+- Status: `open_trades[].status`
+
+Component spec:
+- Single prominent trade card when there is one active position.
+- Side rendered as the primary badge (`LONG`/`SHORT`).
+- Entry shown in large type, with SL/TP/PnL grouped below.
+- If SL/TP are null, show `Protection levels not supplied` to avoid implying risk controls exist.
+
+Empty state:
+- If `meta.counts.open_trades == 0`, replace the section with `No live trades in flight`.
+
+### Next Actions
+
+Purpose: convert signals into a short list of follow-up actions without overclaiming precision.
+
+Card count:
+- Default: top 2 signal cards plus a `See all signals` affordance.
+
+Card fields:
+- Strategy id: `signals[].strategy_id`
+- Pair: `signals[].pair`
+- Bias: `signals[].bias`
+- Trigger text: `signals[].trigger_text`
+- Invalidation text: `signals[].invalidation_text`
+- Risk note: `signals[].risk_note`
+- Confidence: `signals[].confidence`
+
+Component spec:
+- Action-oriented cards with `Watch`, `Validate`, or `Stand by` labels derived from bias/confidence.
+- Trigger and invalidation copy stacked as short paragraphs.
+- Risk note fixed at the bottom of each card.
+
+Fallback behavior:
+- Generic `unknown` and `n/a` signals should render as desk-wide monitoring actions rather than pair-specific setups.
+- Null confidence should not block rendering; use `Analyst review required`.
+
+### CTA
+
+Purpose: close the landing page with a strong next step and product framing.
+
+Primary CTA:
+- `Open the live strategy board`
+
+Secondary CTA:
+- `Review risk notes before trading`
+
+Component spec:
+- Sticky bottom CTA bar or final full-width panel.
+- Include one sentence reminding the user that the feed may contain partial instrument labels and should be validated before execution.
+
+## Mobile Flow Order
+
+1. Hero
+2. KPIs
+3. Top Strategies
+4. Open Trades
+5. Next Actions
+6. CTA
+
+## Card Design Rules
+
+- Keep every card to one dominant data point and at most two secondary metrics.
+- Use chips for status-like values (`SHORT`, `top20`, `Not available yet`).
+- Prefer progressive disclosure over dense tables.
+- Reserve warning styling for missing protection levels, stale timestamps, or invalidation/risk copy.
+- Ensure all cards can collapse gracefully when fields are null or `unknown`.
+
+## Data Binding Summary
+
+| Section | Primary fields | Secondary fields | Fallback priority |
+|---|---|---|---|
+| Hero | `meta.generated_at_utc` | `meta.counts.*` | Count summary + freshness |
+| KPIs | `meta.counts.*` | none | Zero-state labels |
+| Top Strategies | `strategies[].strategy_name`, `net_today` | `pair`, `win_rate`, `drawdown`, `confidence`, `source` | Title + placeholder metric chips |
+| Open Trades | `open_trades[].side`, `entry`, `status` | `strategy_id`, `pair`, `sl`, `tp`, `unrealized_pnl` | Side + entry + missing protection warning |
+| Next Actions | `signals[].trigger_text`, `risk_note` | `bias`, `invalidation_text`, `confidence`, `pair` | Monitoring action copy |
+| CTA | static copy | freshness/risk reminder | Validation reminder |
+
+## Delivery Notes
+
+- This IA intentionally privileges counts, exposure state, and risk framing because the current sample feed has repeated strategies and placeholder labels.
+- The design should be implemented as a landing layer above the deeper strategy board rather than a full replacement for detailed analytics views.

tokens used
140,541
Executed end-to-end. The IA artifact is at [20260319_170500_trading_signal_mobile_landing_ia.md](C:/Users/edebe/eds/workstream/clawd_originated/artefacts/projects/20260319_170500_trading_signal_mobile_landing_ia.md), the validation output is at [mobile_landing_ia_validation.txt](C:/Users/edebe/eds/workstream/clawd_originated/artefacts/evidence/trading_signal/mobile_landing_ia_validation.txt), and the lifecycle file was updated and moved to [20260308_162710_trading_signal_mobile_landing_ia.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260308_162710_trading_signal_mobile_landing_ia.md).

The deliverable now defines the mobile section map for Hero, KPIs, Top Strategies, Open Trades, Next Actions, and CTA, including field bindings and fallback rules for `unknown`/`null` feed data. I also appended the delivery to [activity_log.md](C:/Users/edebe/eds/workstream/clawd_originated/artefacts/activity_log.md).

Validation passed: `overall=pass` with all required sections present in the IA doc. I did not commit changes.
