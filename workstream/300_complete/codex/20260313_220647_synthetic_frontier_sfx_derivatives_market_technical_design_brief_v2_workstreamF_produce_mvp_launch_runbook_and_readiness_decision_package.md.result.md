OpenAI Codex v0.115.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019d070b-0faf-7e40-862e-7358637d6a8c
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress\codex\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
codex
I’m starting by loading the required lifecycle skill and the specified task file, then I’ll inspect the workspace to determine the concrete deliverables, implement them, run validation, and update the task checklist in place.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md'" in C:\Users\edebe\eds succeeded in 6.62s:
# TASK F4: Produce MVP launch runbook and readiness decision package

**Workstream:** F — Launch Readiness and Validation
**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
**Priority:** 2
**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
**Suggested Agent:** general
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.

---

## Purpose

Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.

## Input

 succeeded in 6.63s:
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
 succeeded in 7.56s:

    Directory: C:\Users\edebe\eds

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          10/03/2026    02:47                [44;1m__pycache__[0m
d----          12/03/2026    14:04                [44;1m.agent[0m
d----          24/02/2026    10:05                [44;1m.android[0m
d----          18/03/2026    10:41                [44;1m.claude[0m
d----          08/03/2025    18:23                [44;1m.edsLaptop[0m
d----          21/01/2026    10:23                [44;1m.gemini[0m
d----          01/03/2026    20:00                [44;1m.playwright-mcp[0m
d----          27/11/2025    23:13                [44;1m.pytest_cache[0m
d----          24/04/2025    10:45                [44;1m.roo[0m
d----          04/01/2026    15:30                [44;1m.venv[0m
d----          14/01/2026    10:16                [44;1m.vscode[0m
d----          30/12/2025    17:07                [44;1ma2ui[0m
d----          14/04/2025    13:02                [44;1mAI_trades_agents[0m
d----          14/01/2026    15:48                [44;1mAI_voice[0m
d----          10/04/2025    03:03                [44;1malgo[0m
codex
The task file is still in the older generated format, so I’m mapping it onto the required lifecycle template and locating the upstream F/E deliverables it depends on before I add any artifacts.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg --files 'workstream' | rg '(_e1_|_e2_|_e3_|_f1_|_f2_|_f3_|workstream[a-f]|synthetic_frontier|sfx)'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Recurse 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2' | Select-Object FullName,Length,LastWriteTime" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git status --short' in C:\Users\edebe\eds exited 1 in 3.95s:

[32;1mFullName[0m
[32;1m--------                                                                                                               [0m
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy                       
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\pytest-cache-files-0tcs5n_g  
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\pytest-cache-files-48d1gul1  
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution                     
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification                 
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams                  
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\a4_oracle_health_and_index_d…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\d1_stress_event_schem…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\d1_stress_thresholds.…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\__pycache__         
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\json                
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\shock_simulation_ha…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\stress_response_orc…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\tests               
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency        
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams         
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\a3_index_calculatio…
 exited 1 in 4.57s:
workstream\200_inprogress\codex\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
workstream\100_backlog\gemini\20260316_220223_general_BLOCKER_20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md.result.md.result.md
workstream\100_backlog\claude\20260313_220646_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_build_shock_simulation_and_scenario_validation_harness.md
workstream\400_failed\codex\20260313_220646_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_build_shock_simulation_and_scenario_validation_harness.md.result.md
workstream\000_epic\codex\20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md
workstream\050_review\claude\20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md
workstream\300_complete\20260313_220642_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamE_specify_governance_parameter_band_and_emergency_override_framework.md
workstream\300_complete\20260313_220630_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_define_oracle_health_and_index_divergence_monitoring_rules.md
workstream\300_complete\20260313_220627_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_define_macro_volatility_index_schema_and_source_contract.md
workstream\300_complete\gemini\20260313_220629_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_design_index_calculation_weighting_and_smoothing_engine.md
workstream\300_complete\gemini\20260313_220628_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_specify_source_ingestion_and_normalization_pipeline.md
workstream\300_complete\gemini\20260313_220635_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamC_design_dynamic_leverage_band_engine.md
workstream\300_complete\gemini\20260313_220634_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamC_define_vault_accounting_and_exposure_cap_model.md
workstream\300_complete\gemini\20260313_220636_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamC_design_spread_elasticity_and_quoting_protection_rules.md
workstream\300_complete\gemini\20260313_220638_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamD_define_stress_detection_metrics_and_event_thresholds.md
workstream\300_complete\codex\20260313_220646_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_build_shock_simulation_and_scenario_validation_harness.md
workstream\300_complete\codex\20260313_220631_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_define_perpetual_instrument_and_market_configuration_model.md
workstream\300_complete\claude\20260313_220641_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamE_define_public_transparency_data_contract_and_disclosure_pack.md
workstream\300_complete\claude\20260313_220640_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamD_design_circuit_breaker_state_machine_and_staged_reopening_rules.md
workstream\300_complete\claude\20260313_220639_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamD_design_automated_response_orchestrator_for_stress_events.md
 succeeded in 5.86s:
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
codex
I’ve confirmed the repo is already dirty, so I’m isolating this task to the sFX epic folder and its lifecycle file without touching unrelated changes. Next I’m pulling the upstream artifacts the runbook has to cite.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F' -Recurse -File | Select-Object FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams' -Recurse -File | Select-Object FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n --glob '*.md' --glob '*.json' --glob '*.py' --glob '*.yaml' --glob '*.yml' 'governance|transparency|shock|isolated margin|instrument listing|runbook|readiness|launch|phase 1' 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2'" in C:\Users\edebe\eds succeeded in 2.59s:

[32;1mFullName[0m
[32;1m--------[0m
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_ma…

 exited 1 in 2.77s:
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:4:Define a complete per-market configuration contract for the MVP synthetic frontier perpetual venue. The model supports listing, execution, margining, liquidation reference selection, vault containment, funding linkage, and public transparency without introducing cross-margin or redeemable token balances.
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:24:| `status` | enum | yes | `draft`, `prelaunch`, `active`, `reduce_only`, `halted`, `retired`. |
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:25:| `launch_phase` | enum | yes | `phase_1` or later. |
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:35:| `initial_leverage_max` | number | yes | Initial launch cap, typically `2.0`. |
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:36:| `governance_leverage_ceiling` | number | yes | Hard upper band governance may not exceed without a new listing action. |
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:60:| `open_interest_cap_usdc` | number | yes | Instrument-level notional cap for launch containment. |
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:84:| `transparency_fields` | array[string] | yes | Public fields emitted for market status, caps, leverage band, funding, and vault state. |
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:85:| `governance_parameters` | array[string] | yes | Parameters governance may tune within approved bands. |
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:107:- `governance_leverage_ceiling`
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:134:- `transparency_fields`
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:135:- `governance_parameters`
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:142:- Phase 1 leverage must remain within the epic's conservative launch posture, with launch defaults at `1.0x` to `2.0x`.
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:143:- Every instrument must expose transparency fields sufficient for public publication of leverage, funding, open interest, and market status.
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:146:Use one listing object per market. The phase 1 pack should instantiate:
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:152:Shared launch defaults:
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:170:  "status": "prelaunch",
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:171:  "launch_phase": "phase_1",
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:178:  "governance_leverage_ceiling": 5.0,
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:209:    "transparency_feed"
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md:222:  "transparency_fields": [
 succeeded in 3.40s:

[32;1mFullName[0m
[32;1m--------[0m
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstr…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\D\d3_ci…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\__pycac…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\__pycac…

codex
I’ve found the core sFX artifact set under the epic folder. The next step is to extract the authoritative numbers and operating constraints from E/F deliverables so the runbook and decision package are concrete rather than generic.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f1_isolated_margin_and_per_instrument_containment_model.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_instrument_listing_and_cap_configuration_pack.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams' -File | Select-Object Name,FullName" in C:\Users\edebe\eds exited 1 in 2.21s:
[31;1mGet-Content: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-Content -Raw 'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_deriva[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mCannot find path 'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f1_isolated_margin_and_per_instrument_containment_model.md' because it does not exist.[0m
 succeeded in 2.13s:

[32;1mName                                                                     [0m[32;1m FullName[0m
[32;1m----                                                                     [0m [32;1m--------[0m
workstream_a1_macro_volatility_index_schema_and_source_contract.md        C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstream_a1_macro_volatility_index_schema.json                          C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstream_b3_funding_rate_calculation_and_settlement_model.md            C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstream_f2_phase_1_listing_pack.json                                   C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstream_f2_validate_phase_1_listing_pack.py                            C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstream_f3_shock_scenario_library.json                                 C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstream_f3_shock_scorecard_template.md                                 C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstream_f3_shock_simulation_and_scenario_validation_harness.md         C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstream_f3_shock_validation_harness.py                                 C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstreamC_liquidation_workflow_and_vault_backstop_rules.json            C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstreamC_liquidation_workflow_and_vault_backstop_spec.md               C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstreamE_governance_parameter_band_and_emergency_override_framework.md C:\Users\edebe\eds\ep_synthetic_frontier_sfx…
workstreamE_governance_parameter_band_registry.json                       C:\Users\edebe\eds\ep_synthetic_frontier_sfx…

 exited 1 in 2.36s:
[31;1mGet-Content: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-Content -Raw 'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_deriva[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mCannot find path 'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_instrument_listing_and_cap_configuration_pack.md' because it does not exist.[0m
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\claude\\20260313_220645_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_prepare_phase_1_instrument_listing_and_cap_configuration_pack.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\gemini\\20260313_220644_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_define_isolated_margin_and_per_instrument_containment_model.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex\\20260313_220646_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_build_shock_simulation_and_scenario_validation_harness.md'" in C:\Users\edebe\eds succeeded in 6.64s:
# TASK F2: Prepare phase-1 instrument listing and cap configuration pack

**Workstream:** F — Launch Readiness and Validation
**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
**Status:** [x] Complete

## Source

- `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`

## Task Summary

Assemble the initial launch configuration pack for the phase-1 sFX instruments with conservative leverage bands, exposure caps, funding base parameters, spread floors, and explicit launch assumptions.

## Context

- Epic output folder: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Existing upstream artifact available in workspace:
  - `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema_and_source_contract.md`
  - `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema.json`
 succeeded in 6.58s:
Source: `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`

Task Summary
Define the F1 isolated-margin and per-instrument containment model for the Synthetic Frontier sFX venue, producing a launch-time specification that makes margin scope, vault boundaries, loss containment, and shared systemic dependencies explicit for the phase-1 instruments.

Context
- Epic brief: `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Task file: `C:\Users\edebe\eds\workstream\300_complete\gemini\20260313_220644_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_define_isolated_margin_and_per_instrument_containment_model.md`
- Deliverable path: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
- Dependency references available only as generated task stubs:
  - `C:\Users\edebe\eds\workstream\400_failed\claude\20260313_220631_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_define_perpetual_instrument_and_market_configuration_model.md`
  - `C:\Users\edebe\eds\workstream\400_failed\gemini\20260313_220634_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamC_define_vault_accounting_and_exposure_cap_model.md`

Dependency: B1 and C1 are declared upstream dependencies, but no completed artifacts existed in the workspace. This task derives the containment model from the epic brief plus the dependency task definitions and records that assumption explicitly.

Plan
- [x] 1. Author the F1 isolation model specification with the required containment fields and phase-1 instrument coverage.
  - [x] Test: `rg -n "margin_scope|vault_scope|loss_containment_boundary|shared_dependency_exception|NGN_VOL|KES_VOL|GHS_VOL|ZAR_VOL" C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`; pass if the spec includes all required containment fields and all four phase-1 instrument entries.
  - Evidence: PASS. `rg` returned the isolation-domain table header at line 19, explicit rows for `NGN_VOL`/`KES_VOL`/`GHS_VOL`/`ZAR_VOL` at lines 21-24, and the required containment fields again in the transparency outputs at lines 99-102.
- [x] 2. Add explicit failure-containment scenarios that prove losses remain instrument-local under stressed conditions.
 succeeded in 5.55s:
Priority: 1

# Source
- Epic task stub derived from `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`.
- User request in chat on 2026-03-18 to execute this task end-to-end and follow `skills/workstream-task-lifecycle/SKILL.md`.

# Task Summary
Build and validate a repeatable macro-shock scenario harness for the sFX MVP venue, proving whether phase-1 markets can survive 30% to 50% shock conditions with functioning liquidity, intact vault capital, stabilizing funding behavior, transparent control outputs, and governance-safe control reactions.

# Context
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b2_central_limit_order_book_and_price_formation_rules.md`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_b3_funding_rate_calculation_and_settlement_model.md`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\C\vault_accounting_and_exposure_cap_model.md`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\C\dynamic_leverage_band_engine.md`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\C\c3_spread_elasticity_and_quoting_protection_rules.md`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\D\d1_stress_detection_metrics_spec.md`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\D\d2_automated_response_orchestrator_design.md`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\D\d3_circuit_breaker_state_machine_and_staged_reopening_rules.md`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\dynamic_leverage_band_engine.py`
- `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\stress_response_orchestrator\engine.py`
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\20260313_220642_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamE_specify_governance_parameter_band_and_emergency_override_framework.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\claude\\20260313_220641_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamE_define_public_transparency_data_contract_and_disclosure_pack.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex\\20260316_220223_general_BLOCKER_20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md'" in C:\Users\edebe\eds succeeded in 3.56s:
# Source
- Epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Source task seed: `workstream/400_failed/claude/20260313_220642_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamE_specify_governance_parameter_band_and_emergency_override_framework.md`

## Task Summary
Define the governance-adjustable parameter set for the synthetic frontier sFX derivatives market, bind each control to immutable safety rails, and codify emergency overrides as a closed, auditable rule set rather than discretionary operator intervention.

## Context
- Epic output root: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Intended deliverables:
  - `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamE_governance_parameter_band_and_emergency_override_framework.md`
  - `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamE_governance_parameter_band_registry.json`
- Upstream conceptual references only: Workstream C control models (`C1`, `C2`, `C3`), Workstream D circuit-breaker design (`D3`), and epic sections 4 through 7.

## Dependency
Dependency: Conceptual dependency on `C1`, `C2`, `C3`, and `D3`. No completed upstream implementation artifacts for those tasks are present in the workspace, so this task derives governance constraints directly from the epic and the generated task briefs.

## Plan
- [x] 1. Rehydrate the assigned task into the active lifecycle lane and replace the seed stub with a lifecycle-compliant execution record.
  - [x] Test: `Test-Path 'workstream\200_inprogress\claude\20260313_220642_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamE_specify_governance_parameter_band_and_emergency_override_framework.md'` returns `True`.
 succeeded in 3.27s:
Source:
- Epic task derived from [workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md](C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md).
- Recovered from failed lane execution request on 2026-03-16 and executed end-to-end in the workspace.

Task Summary:
- Define the sFX public transparency contract, disclosure wording, and publication field catalog covering the live system state fields named in epic section 6: `vault_capital`, `long_short_imbalance`, `open_interest`, `current_leverage_band`, `funding_rate`, `volatility_metric`, `risk_parameter_band`, and `market_status`.

Context:
- Epic source: [20260227_022357_sFX_Technical_Design_Brief_v2.md](C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md)
- Epic output folder: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Upstream interface assumptions taken from the task stubs for `B3`, `C1`, `C2`, `C3`, `D2`, and `D3`.

Dependency:
- `A3`, `B3`, `C1`, `C2`, `C3`, `D2`, and `D3` are logical upstream design dependencies. This task defines the public contract from their stated outputs because those upstream artifacts were not yet implemented in the epic output folder.

Plan:
- [x] 1. Recover the failed task into the active lifecycle lane and normalize it to the required lifecycle format.
  - [x] Test: Confirm the lifecycle file exists in `workstream/200_inprogress/claude` and contains `Source`, `Dependency`, ordered `Plan`, `Evidence`, and `Completion Status` sections.
  - Evidence: Task file moved from `workstream/400_failed/claude` to `workstream/200_inprogress/claude` and rewritten into the current lifecycle format.
- [x] 2. Implement the transparency deliverables in the synthetic frontier epic output folder.
 succeeded in 3.26s:
# Task Summary
Blocker encountered while executing `20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md` via `codex` agent.

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
session id: 019cf8ab-e670-7fb3-a0b0-5fb6d23c4352
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/codex\20260313_220643_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreame_build_public_market_state_transparency_dashboard_mvp.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
ERROR: You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at Mar 18th, 2026 4:51 PM.
codex
I’ve got the upstream E/F records now. There’s enough implemented material to assemble the launch package; the main remaining work is to synthesize those artifacts into an operator runbook, readiness checklist, dependency register, and explicit go/no-go memo with cited evidence.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json'" in C:\Users\edebe\eds succeeded in 2.39s:
{
  "pack_id": "f2.phase_1.v1",
  "generated_on": "2026-03-16",
  "objective": "Conservative MVP launch configuration for phase-1 sFX macro volatility instruments.",
  "launch_assumptions": {
    "launch_mode": "conservative_mvp",
    "liquidity_priority": "quality_over_volume",
    "cross_margin_enabled": false,
    "per_instrument_vault_isolation": true,
    "governance_hard_max_leverage": 5.0,
    "phase_1_operational_max_leverage": 2.0,
    "aggregate_phase_1_exposure_cap_fraction": 0.55,
    "reserve_buffer_fraction": 0.45,
    "stress_response_order": [
      "leverage_compression",
      "funding_multiplier_increase",
      "spread_widening",
      "position_size_cap_tightening",
      "open_interest_cap_enforcement"
    ]
 succeeded in 2.84s:
[
  {
    "scenario_id": "zar_30pct_macro_dislocation",
    "instrument_id": "ZAR_VOL",
    "shock_size": 0.3,
    "stress_level": "emergency",
    "metric_values": {
      "volatility_acceleration": 0.47,
      "imbalance_slope_change": 27.0,
      "liquidation_cluster_density": 0.024,
      "order_book_thinning_rate": 0.29
    },
    "metric_severities": {
      "volatility_acceleration": "elevated",
      "imbalance_slope_change": "elevated",
      "liquidation_cluster_density": "warning",
      "order_book_thinning_rate": "warning"
    },
    "circuit_state": "ELEVATED_WATCH",
    "vault_state": {
 succeeded in 2.91s:
{
  "registry_version": "2026-03-16",
  "epic": "Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)",
  "workstream": "E",
  "parameters": [
    {
      "governed_parameter": "launch_base_leverage_min",
      "category": "risk",
      "unit": "multiple",
      "min_value": 1.0,
      "max_value": 2.0,
      "default_value": 1.5,
      "change_authority": "dao_risk_vote",
      "timelock_rule": "48h_public_timelock",
      "emergency_override_condition": "control_integrity_failure",
      "emergency_action": "revert_parameter_to_last_good",
      "audit_requirement": "proposal_id,vote_hash,old_value,new_value,activation_time"
    },
    {
      "governed_parameter": "absolute_leverage_cap",
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\D\\d3_circuit_breaker_state_machine_and_staged_reopening_rules.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_and_emergency_override_framework.md'" in C:\Users\edebe\eds succeeded in 2.30s:
# D3 Circuit Breaker State Machine And Staged Reopening Rules

## Purpose

Define the deterministic per-instrument halt lifecycle used when index anchoring, source health, or executable liquidity deteriorate beyond safe operating limits.

## Design Principles

- Circuit logic is per instrument. A halt in one market does not freeze unrelated instruments.
- Trigger classes are objective and machine-evaluated. No operator may halt or reopen a market outside the predefined emergency path.
- Reopening is staged. Each stage restores a limited subset of functionality only after explicit recovery checks pass.
- A market must fail closed. Missing health inputs, ambiguous state, or stale recovery data keep the instrument halted.
- All state changes are emitted to the transparency layer and operator console with trigger reason, timestamp, and next eligible transition time.

## Integration Contract

This design consumes the following upstream signals:

- `index_divergence_bps`: absolute divergence between executable mid price and the approved macro-volatility index anchor.
- `source_health_score`: normalized oracle stability score from A4.
 succeeded in 2.28s:
# Public Transparency Data Contract And Disclosure Pack

## Scope

This pack defines the publishable market-state contract for the sFX transparency layer described in epic section 6. It covers the exact public metrics, their source systems, update cadences, disclosure wording, and the redaction boundary between deterministic formulas and proprietary implementation detail.

## Publication Model

- Publish one `PublicTransparencySnapshot` payload for the venue at a deterministic cadence.
- Emit immediate republish events when `market_status` changes state.
- Keep field names stable across versions and increment `schema_version` on breaking changes.
- Expose per-instrument arrays for instrument-level controls and venue-level objects for shared state.

## Update Cadence

| Public metric | Cadence | Trigger |
| --- | --- | --- |
| `long_short_imbalance` | 30 seconds | Scheduled snapshot or material imbalance refresh |
| `open_interest` | 30 seconds | Scheduled snapshot or material open-interest refresh |
| `market_status` | 60 seconds max | Immediate on halt, degrade, or reopen transition |
 succeeded in 1.68s:
# Workstream E Governance Parameter Band and Emergency Override Framework

## Objective
Define exactly what governance may change in production, the immutable bounds that keep the market inside the epic's safety envelope, and the small closed set of emergency actions that may be invoked without introducing discretionary market intervention.

## Design Principles
1. Governance can tune only predeclared parameters.
2. Every governed parameter has an immutable minimum, maximum, and named authority.
3. Routine changes are timelocked and publicly auditable before activation.
4. Emergency actions may only apply enumerated overrides tied to objective trigger conditions.
5. Emergency overrides are temporary, automatically expiring, and require retrospective ratification or rollback.
6. No override may create fiat exposure, cross-margin, unbounded leverage, or hidden pricing discretion.

## Immutable Safety Invariants
- Collateral and settlement remain stablecoin-denominated only.
- Instruments remain isolated; no cross-margin is introduced through governance.
- Trading price remains order-flow determined; the index remains a reference input for funding, liquidation, and circuit-breakers only.
- Effective leverage can never exceed `5.0x`.
- Governance cannot disable audit logging, timelock publication, or public transparency outputs.
- Emergency logic can restrict trading conditions, but cannot force-fill, reprice user orders, or selectively intervene in individual accounts.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency' -File | Select-Object Name,FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\deploy' -Recurse -File | Select-Object Name,FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification' -File | Select-Object Name,FullName" in C:\Users\edebe\eds succeeded in 1.80s:

[32;1mName                                          [0m[32;1m FullName[0m
[32;1m----                                          [0m [32;1m--------[0m
20260316_sfx_dashboard_smoke.txt               C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
20260316_sfx_market_state_dashboard.png        C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
20260316_sfx_market_state_snapshot.html        C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
20260316_sfx_market_state_snapshot.png         C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
a3_index_calculation_test_vectors.json         C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
c3_spread_elasticity_scenarios.json            C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
shock_scenarios.json                           C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
validate_public_transparency_contract.py       C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
validate_shock_scenarios.py                    C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
verify_dynamic_leverage_band_engine.py         C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
workstream_a1_ngn_vol_example.json             C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
workstream_b3_funding_examples.json            C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
workstream_f3_shock_scorecard_template.csv     C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
workstream_f3_shock_validation_results.json    C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
workstream_f3_test_first.json                  C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
workstream_f3_test_results.json                C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
workstream_f3_test_second.json                 C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technic…
 succeeded in 1.87s:

[32;1mName                       [0m[32;1m FullName[0m
[32;1m----                       [0m [32;1m--------[0m
d1_stress_event_schema.json C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\…
d1_stress_thresholds.json   C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\…

 succeeded in 1.84s:

[32;1mName                                     [0m[32;1m FullName[0m
[32;1m----                                     [0m [32;1m--------[0m
public_transparency_contract.schema.json  C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_de…
public_transparency_disclosure_pack.md    C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_de…
public_transparency_field_catalog.csv     C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_de…
public_transparency_snapshot.example.json C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_de…

codex
I’ve got enough context to execute the package build. I’m about to do three things in order:

1. Normalize the active lifecycle file so it reflects the actual implementation steps and acceptance tests.
2. Add the launch package artifacts under the sFX epic output folder: runbook, readiness checklist, dependency register, decision memo, and a validator.
3. Run the package validator plus the linked upstream validators, then update evidence/checklists and archive the lifecycle file to `300_complete` if everything passes.
Plan update
  → Normalize the F4 lifecycle task file to the required template with ordered plan steps and evidence placeholders.
  • Implement the MVP launch package artifacts in the sFX epic output folder.
  • Run technical validations, capture evidence, update the lifecycle file, and move it to complete.
codex
Before I write the package, I’m checking whether the transparency dashboard dependency is actually present in the epic output folder or only exists as a blocked task record. That decides whether the decision memo lands on `go`, `conditional_go`, or `no_go`.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n --glob '*.py' --glob '*.html' --glob '*.md' --glob '*.json' 'dashboard|market state dashboard|transparency dashboard' 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2' -Recurse -File | Where-Object { "'$_.Name -match '"'dashboard|snapshot' } | Select-Object FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt'" in C:\Users\edebe\eds exited 1 in 3.00s:

[32;1mFullName[0m
[32;1m--------[0m
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_da…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_ma…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_ma…
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_ma…

[31;1mGet-ChildItem: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-ChildItem 'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivativ[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mAccess to the path 'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\pytest-cache-files-0tcs5n_g' is denied.[0m
[31;1mGet-ChildItem: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-ChildItem 'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivativ[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mAccess to the path 'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\pytest-cache-files-48d1gul1' is denied.[0m
[31;1mGet-ChildItem: [0m
 succeeded in 3.36s:
Smoke test passed.
Dashboard URL: http://localhost:3002
Backend URL: http://localhost:3002
Health status: 200
Market-state status: 200

 exited 1 in 9.54s:
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html:29:    <h1>Public market-state dashboard</h1>
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html:35:    <div>Live database input is unavailable, so the dashboard is using deterministic mock transparency data.</div>
C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\C\vault_accounting_and_exposure_cap_model.md:239:| `absolute_net_exposure` | liquidation and risk dashboards |
rg: C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\pytest-cache-files-0tcs5n_g: Access is denied. (os error 5)
rg: C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\pytest-cache-files-48d1gul1: Access is denied. (os error 5)
rg: C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\pytest_tmp\tmp0irv4m6e: Access is denied. (os error 5)
rg: C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\pytest_tmp\tmpqr9_ga0a: Access is denied. (os error 5)
codex
I’ve resolved the main decision point: the transparency dependency is only evidenced through a mock-backed dashboard snapshot and smoke test, not a live-integrated operator surface. I’m writing the package with that reflected explicitly, which means the memo will land on a conservative `no_go` for external MVP launch until that gap is closed.
file update
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv
dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md
# F4 MVP Launch Runbook

## Purpose

Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.

## Launch Scope

- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data

## Roles

| Role | Owner | Responsibility |
|---|---|---|
| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |

## Startup Procedure

1. Confirm the approved listing pack is the active phase-1 configuration:
   - `workstream_f2_phase_1_listing_pack.json`
   - All four instruments present and marked `launch_ready`
   - Operational leverage does not exceed `2.0x`
2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
   - `workstreamE_governance_parameter_band_registry.json`
   - `emergency_policy.restrictive_only = true`
   - At least the 13 declared bounded parameters are present
3. Confirm isolation model remains unchanged:
   - `f1_isolated_margin_and_per_instrument_containment_model.md`
   - No cross-instrument margining or inter-vault borrowing
4. Confirm transparency contract validation passes:
   - `validate_public_transparency_contract.py`
   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
5. Confirm shock validation remains green:
   - `validate_shock_scenarios.py`
   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
6. Confirm operator visibility surface is reachable:
   - `verification/20260316_sfx_dashboard_smoke.txt`
   - Document whether the surface is live-backed or mock-backed before any launch decision

Release gate:
- Public MVP launch requires all checks above plus a live-backed transparency surface.
- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.

## Runtime Monitoring Procedure

Monitor every 60 seconds or faster during the first trading hour:

| Signal | Source | Threshold or expectation | Owner |
|---|---|---|---|
| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |

Escalation triggers:
- Any missing required transparency field
- `market_status` transition without corresponding operator alert
- Emergency-level stress with no leverage compression, spread widening, or cap tightening
- Any evidence of cross-instrument loss transfer
- Any emergency request that would widen risk instead of tighten it

## Halt Procedure

Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:

1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
2. Confirm the trigger family:
   - `index_divergence_breach`
   - `oracle_quorum_failure`
   - `depth_collapse_event`
   - `liquidation_cluster_emergency`
   - `control_integrity_failure`
3. Validate the matching protective actions are present:
   - leverage compressed toward floor
   - funding multiplier increased
   - spread widened to stressed or emergency floor
   - position-size and open-interest caps tightened
4. Publish or verify immediate public state update:
   - `market_status`
   - `risk_parameter_band`
   - incident timestamp
5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
   - `force_reduce_only`
   - `tighten_leverage_to_floor`
   - `tighten_spread_to_emergency_floor`
   - `tighten_position_and_oi_caps`
   - `freeze_oracle_weights_to_fallback`
   - `revert_parameter_to_last_good`
6. Record incident id, trigger metrics, signers, and expiry immediately.

## Reopen Procedure

Reopen only through the D3 staged flow:

1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
2. Confirm all recovery requirements are true for the full stability window:
   - depth recovery
   - source stability
   - divergence recovery
3. Permit `REOPEN_STAGE_1` only:
   - cancel and passive-only quoting
   - no market orders
   - no leverage increases
4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.

## Incident Escalation Procedure

1. Launch Commander opens incident command and names the affected instrument scope.
2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
4. Transparency Operator confirms public disclosure completeness and freshness.
5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.

## Launch-Day Stop Conditions

- Transparency surface still uses deterministic mock data instead of live publication inputs
- Governance registry missing, altered outside bounds, or not restrictive-only
- Any upstream validator fails
- Any instrument exceeds the approved launch leverage or cap posture
- Inability to prove per-instrument isolation and local loss containment

## Evidence References

- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
Source:
- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`

Task Summary:
- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.

Context:
- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Upstream implementation artifacts:
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
- Target F4 deliverables:
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`

Dependency:
Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.

Plan:
- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
  - Evidence: pending
- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
  - Evidence: pending
- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
  - Evidence: pending

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `not_applicable`
  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
  - Status: planned
- Evidence-Type: test_output
  - Artifact: `not_applicable`
  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
  - Status: planned
- Evidence-Type: diff
  - Artifact: `not_applicable`
  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
  - Status: planned

Implementation Log:
- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.

Changes Made:
- In progress.

Validation:
- Pending execution.

Risks/Notes:
- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.

Completion Status:
- In progress.
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md
# F4 Go/No-Go Decision Memo

Decision Date: 2026-03-19
Decision: `no_go`
Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`

## Executive Summary

The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.

## Positive Readiness Signals

- Configuration posture is conservative and validated through the F2 pack.
- Emergency governance remains bounded and restrictive-only.
- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
- Per-instrument containment and local loss boundaries are documented.
- Transparency contract fields, cadences, and redaction boundaries are defined and validated.

## Blocking Findings

1. `E3` remains a launch blocker for a public release.
   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
2. The current package proves deterministic validation, not live operating rehearsal.
   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.

## Supporting Evidence

- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`

## Required Exit Criteria To Move To Go

1. Replace the mock-backed transparency surface with a live-backed publication flow.
2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.

## Owner And Follow-Up

- Blocking owner: Transparency Operator
- Decision owner: Launch Commander
- Next review trigger: completion of live-backed dashboard validation artifacts
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json
{
  "package_id": "f4.mvp_launch_readiness.v1",
  "generated_on": "2026-03-19",
  "decision_status": "no_go",
  "checklist": [
    {
      "check_id": "phase_1_config",
      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
      "owner": "Launch Commander",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
    },
    {
      "check_id": "governance_safety",
      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
      "owner": "Governance Liaison",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
    },
    {
      "check_id": "transparency_contract",
      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
      "owner": "Transparency Operator",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
    },
    {
      "check_id": "shock_resilience",
      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
      "owner": "Risk Duty Officer",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
    },
    {
      "check_id": "isolation_containment",
      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
      "owner": "Risk Duty Officer",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
    },
    {
      "check_id": "dashboard_operability",
      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
      "owner": "Transparency Operator",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
    }
  ],
  "unresolved_risks": [
    {
      "risk_id": "r1",
      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
      "owner": "Transparency Operator",
      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
    },
    {
      "risk_id": "r2",
      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
      "owner": "Launch Commander",
      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
    }
  ]
}
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPLOY = ROOT / "deploy"

RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load_text(path: Path) -> str:
    _assert(path.exists(), f"missing_file:{path}")
    return path.read_text(encoding="utf-8")


def validate_runbook() -> None:
    text = _load_text(RUNBOOK_PATH)
    required_sections = [
        "## Startup Procedure",
        "## Runtime Monitoring Procedure",
        "## Halt Procedure",
        "## Reopen Procedure",
        "## Incident Escalation Procedure",
    ]
    for section in required_sections:
        _assert(section in text, f"missing_runbook_section:{section}")


def validate_checklist() -> int:
    data = json.loads(_load_text(CHECKLIST_PATH))
    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
    required_fields = {
        "prelaunch_check",
        "runtime_monitor",
        "halt_procedure",
        "reopen_procedure",
        "owner",
        "evidence_link",
    }
    checklist = data["checklist"]
    _assert(len(checklist) >= 6, "insufficient_checklist_items")
    for item in checklist:
        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
        evidence_path = Path(item["evidence_link"])
        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
    return len(checklist)


def validate_dependency_register() -> int:
    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
    actual = {row["dependency_id"] for row in rows}
    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
    for row in rows:
        evidence_path = Path(row["evidence_link"])
        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
    return len(rows)


def validate_decision_memo() -> str:
    text = _load_text(DECISION_MEMO_PATH)
    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
    required_markers = [
        "Configuration evidence link:",
        "Governance evidence link:",
        "Transparency evidence link:",
        "Shock-test evidence link:",
        "## Blocking Findings",
        "## Required Exit Criteria To Move To Go",
    ]
    for marker in required_markers:
        _assert(marker in text, f"missing_decision_marker:{marker}")
    if "Decision: `no_go`" in text:
        return "no_go"
    if "Decision: `conditional_go`" in text:
        return "conditional_go"
    return "go"


def main() -> None:
    validate_runbook()
    checklist_items = validate_checklist()
    dependency_rows = validate_dependency_register()
    decision = validate_decision_memo()
    print(
        f"f4_launch_package_ok decision={decision} "
        f"checklist_items={checklist_items} dependencies={dependency_rows}"
    )


if __name__ == "__main__":
    main()
apply_patch(auto_approved=true) exited 1 in 879ms:
codex
I hit a patch application issue on the first pass. I’m retrying with repo-relative paths and then I’ll move straight to validation once the artifacts are on disk.
file update
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
# F4 MVP Launch Runbook

## Purpose

Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.

## Launch Scope

- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data

## Roles

| Role | Owner | Responsibility |
|---|---|---|
| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |

## Startup Procedure

1. Confirm the approved listing pack is the active phase-1 configuration:
   - `workstream_f2_phase_1_listing_pack.json`
   - All four instruments present and marked `launch_ready`
   - Operational leverage does not exceed `2.0x`
2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
   - `workstreamE_governance_parameter_band_registry.json`
   - `emergency_policy.restrictive_only = true`
   - At least the 13 declared bounded parameters are present
3. Confirm isolation model remains unchanged:
   - `f1_isolated_margin_and_per_instrument_containment_model.md`
   - No cross-instrument margining or inter-vault borrowing
4. Confirm transparency contract validation passes:
   - `validate_public_transparency_contract.py`
   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
5. Confirm shock validation remains green:
   - `validate_shock_scenarios.py`
   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
6. Confirm operator visibility surface is reachable:
   - `verification/20260316_sfx_dashboard_smoke.txt`
   - Document whether the surface is live-backed or mock-backed before any launch decision

Release gate:
- Public MVP launch requires all checks above plus a live-backed transparency surface.
- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.

## Runtime Monitoring Procedure

Monitor every 60 seconds or faster during the first trading hour:

| Signal | Source | Threshold or expectation | Owner |
|---|---|---|---|
| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |

Escalation triggers:
- Any missing required transparency field
- Any `market_status` transition without corresponding operator alert
- Emergency-level stress with no leverage compression, spread widening, or cap tightening
- Any evidence of cross-instrument loss transfer
- Any emergency request that would widen risk instead of tighten it

## Halt Procedure

Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:

1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
2. Confirm the trigger family:
   - `index_divergence_breach`
   - `oracle_quorum_failure`
   - `depth_collapse_event`
   - `liquidation_cluster_emergency`
   - `control_integrity_failure`
3. Validate the matching protective actions are present:
   - leverage compressed toward floor
   - funding multiplier increased
   - spread widened to stressed or emergency floor
   - position-size and open-interest caps tightened
4. Publish or verify immediate public state update:
   - `market_status`
   - `risk_parameter_band`
   - incident timestamp
5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
   - `force_reduce_only`
   - `tighten_leverage_to_floor`
   - `tighten_spread_to_emergency_floor`
   - `tighten_position_and_oi_caps`
   - `freeze_oracle_weights_to_fallback`
   - `revert_parameter_to_last_good`
6. Record incident id, trigger metrics, signers, and expiry immediately.

## Reopen Procedure

Reopen only through the D3 staged flow:

1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
2. Confirm all recovery requirements are true for the full stability window:
   - depth recovery
   - source stability
   - divergence recovery
3. Permit `REOPEN_STAGE_1` only:
   - cancel and passive-only quoting
   - no market orders
   - no leverage increases
4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.

## Incident Escalation Procedure

1. Launch Commander opens incident command and names the affected instrument scope.
2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
4. Transparency Operator confirms public disclosure completeness and freshness.
5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.

## Launch-Day Stop Conditions

- Transparency surface still uses deterministic mock data instead of live publication inputs
- Governance registry missing, altered outside bounds, or not restrictive-only
- Any upstream validator fails
- Any instrument exceeds the approved launch leverage or cap posture
- Inability to prove per-instrument isolation and local loss containment

## Evidence References

- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
A C:\Users\edebe\eds\workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
Source:
- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`

Task Summary:
- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.

Context:
- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Upstream implementation artifacts:
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
- Target F4 deliverables:
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`

Dependency:
Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.

Plan:
- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
  - Evidence: pending
- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
  - Evidence: pending
- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
  - Evidence: pending

Evidence:
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `not_applicable`
  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
  - Status: planned
- Evidence-Type: test_output
  - Artifact: `not_applicable`
  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
  - Status: planned
- Evidence-Type: diff
  - Artifact: `not_applicable`
  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
  - Status: planned

Implementation Log:
- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.

Changes Made:
- In progress.

Validation:
- Pending execution.

Risks/Notes:
- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.

Completion Status:
- In progress.
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
{
  "package_id": "f4.mvp_launch_readiness.v1",
  "generated_on": "2026-03-19",
  "decision_status": "no_go",
  "checklist": [
    {
      "check_id": "phase_1_config",
      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
      "owner": "Launch Commander",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
    },
    {
      "check_id": "governance_safety",
      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
      "owner": "Governance Liaison",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
    },
    {
      "check_id": "transparency_contract",
      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
      "owner": "Transparency Operator",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
    },
    {
      "check_id": "shock_resilience",
      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
      "owner": "Risk Duty Officer",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
    },
    {
      "check_id": "isolation_containment",
      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
      "owner": "Risk Duty Officer",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
    },
    {
      "check_id": "dashboard_operability",
      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
      "owner": "Transparency Operator",
      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
    }
  ],
  "unresolved_risks": [
    {
      "risk_id": "r1",
      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
      "owner": "Transparency Operator",
      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
    },
    {
      "risk_id": "r2",
      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
      "owner": "Launch Commander",
      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
    }
  ]
}
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPLOY = ROOT / "deploy"

RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load_text(path: Path) -> str:
    _assert(path.exists(), f"missing_file:{path}")
    return path.read_text(encoding="utf-8")


def validate_runbook() -> None:
    text = _load_text(RUNBOOK_PATH)
    required_sections = [
        "## Startup Procedure",
        "## Runtime Monitoring Procedure",
        "## Halt Procedure",
        "## Reopen Procedure",
        "## Incident Escalation Procedure",
    ]
    for section in required_sections:
        _assert(section in text, f"missing_runbook_section:{section}")


def validate_checklist() -> int:
    data = json.loads(_load_text(CHECKLIST_PATH))
    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
    required_fields = {
        "prelaunch_check",
        "runtime_monitor",
        "halt_procedure",
        "reopen_procedure",
        "owner",
        "evidence_link",
    }
    checklist = data["checklist"]
    _assert(len(checklist) >= 6, "insufficient_checklist_items")
    for item in checklist:
        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
        evidence_path = Path(item["evidence_link"])
        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
    return len(checklist)


def validate_dependency_register() -> int:
    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
    actual = {row["dependency_id"] for row in rows}
    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
    for row in rows:
        evidence_path = Path(row["evidence_link"])
        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
    return len(rows)


def validate_decision_memo() -> str:
    text = _load_text(DECISION_MEMO_PATH)
    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
    required_markers = [
        "Configuration evidence link:",
        "Governance evidence link:",
        "Transparency evidence link:",
        "Shock-test evidence link:",
        "## Blocking Findings",
        "## Required Exit Criteria To Move To Go",
    ]
    for marker in required_markers:
        _assert(marker in text, f"missing_decision_marker:{marker}")
    if "Decision: `no_go`" in text:
        return "no_go"
    if "Decision: `conditional_go`" in text:
        return "conditional_go"
    return "go"


def main() -> None:
    validate_runbook()
    checklist_items = validate_checklist()
    dependency_rows = validate_dependency_register()
    decision = validate_decision_memo()
    print(
        f"f4_launch_package_ok decision={decision} "
        f"checklist_items={checklist_items} dependencies={dependency_rows}"
    )


if __name__ == "__main__":
    main()
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
# F4 Go/No-Go Decision Memo

Decision Date: 2026-03-19
Decision: `no_go`
Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`

## Executive Summary

The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.

## Positive Readiness Signals

- Configuration posture is conservative and validated through the F2 pack.
- Emergency governance remains bounded and restrictive-only.
- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
- Per-instrument containment and local loss boundaries are documented.
- Transparency contract fields, cadences, and redaction boundaries are defined and validated.

## Blocking Findings

1. `E3` remains a launch blocker for a public release.
   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
2. The current package proves deterministic validation, not live operating rehearsal.
   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.

## Supporting Evidence

- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`

## Required Exit Criteria To Move To Go

1. Replace the mock-backed transparency surface with a live-backed publication flow.
2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.

## Owner And Follow-Up

- Blocking owner: Transparency Operator
- Decision owner: Launch Commander
- Next review trigger: completion of live-backed dashboard validation artifacts
A C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
apply_patch(auto_approved=true) exited 0 in 2.36s:
Success. Updated the following files:
A workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
A ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
A ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
A ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
A ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
A ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
D workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..f86ede6f9134e816e3e47f38d98121c2f60036c1
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,72 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: pending
+- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: pending
+- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 0%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
+  - Status: planned
+- Evidence-Type: diff
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+
+Changes Made:
+- In progress.
+
+Validation:
+- Pending execution.
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- In progress.

file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..f86ede6f9134e816e3e47f38d98121c2f60036c1
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,72 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: pending
+- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: pending
+- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 0%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
+  - Status: planned
+- Evidence-Type: diff
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+
+Changes Made:
+- In progress.
+
+Validation:
+- Pending execution.
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- In progress.

codex
The package artifacts are now in place. I’m running the new F4 validator plus the linked upstream validations next, then I’ll fold the results back into the lifecycle record and archive it if everything is clean.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\validate_f4_launch_package.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\validate_public_transparency_contract.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_validate_phase_1_listing_pack.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\validate_shock_scenarios.py'" in C:\Users\edebe\eds succeeded in 3.72s:
f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6
 succeeded in 3.56s:
validation_passed
 exited 1 in 3.57s:
Traceback (most recent call last):
  File "C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py", line 92, in <module>
    main()
    ~~~~^^
  File "C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py", line 82, in main
    instrument_count, total_cap, max_operational_leverage = validate_pack(load_pack())
                                                            ~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py", line 43, in validate_pack
    assert Path(reference["artifact_path"]).exists(), reference["artifact_path"]
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
AssertionError: C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md
 succeeded in 3.25s:
shock_validation_passed scenarios=4 scenario_ids=zar_30pct_macro_dislocation,kes_35pct_proxy_liquidity_shock,ghs_45pct_anchor_dislocation,ngn_50pct_macro_dislocation checks=vault_capital_integrity,liquidity_continuity,funding_stabilization,transparency_outputs,governance_stability artifact=C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..f86ede6f9134e816e3e47f38d98121c2f60036c1
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,72 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: pending
+- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: pending
+- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 0%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
+  - Status: planned
+- Evidence-Type: diff
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+
+Changes Made:
+- In progress.
+
+Validation:
+- Pending execution.
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- In progress.

codex
One upstream validation exposed a real workspace inconsistency: the F2 validator is failing because its listing-pack reference points at an epic path that no longer exists. I’m fixing that reference now so the readiness package can cite a clean validation chain instead of a known-bad artifact.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Test-Path 'C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\workstream\\000_epic' -Recurse -File | Where-Object { "'$_.Name -like '"'*sFX*Technical*Design*Brief*v2*' } | Select-Object FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_validate_phase_1_listing_pack.py'" in C:\Users\edebe\eds succeeded in 2.52s:
False
 succeeded in 2.65s:

[32;1mFullName[0m
[32;1m--------[0m
C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md

 succeeded in 2.62s:
from __future__ import annotations

import json
from pathlib import Path


PACK_PATH = Path(
    r"C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json"
)

EXPECTED_INSTRUMENTS = {"NGN_VOL", "KES_VOL", "GHS_VOL", "ZAR_VOL"}
EXPECTED_SMOOTHING_WINDOWS = {
    "NGN_VOL": 900,
    "KES_VOL": 600,
    "GHS_VOL": 900,
    "ZAR_VOL": 300,
}
REQUIRED_INSTRUMENT_FIELDS = {
    "instrument_id",
    "launch_enabled",
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..f86ede6f9134e816e3e47f38d98121c2f60036c1
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,72 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: pending
+- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: pending
+- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 0%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
+  - Status: planned
+- Evidence-Type: diff
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+
+Changes Made:
+- In progress.
+
+Validation:
+- Pending execution.
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- In progress.

codex
I found the source of the failure: the pack still points at the pre-rename epic filename, while the actual epic artifact is `..._processed.md`. I’m updating the pack reference and then rerunning the full validation chain.
file update
M C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -42,3 +42,3 @@
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
@@ -48,3 +48,3 @@
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
apply_patch(auto_approved=true) exited 0 in 1.14s:
Success. Updated the following files:
M ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..f86ede6f9134e816e3e47f38d98121c2f60036c1
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,72 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: pending
+- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: pending
+- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 0%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
+  - Status: planned
+- Evidence-Type: diff
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+
+Changes Made:
+- In progress.
+
+Validation:
+- Pending execution.
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- In progress.

file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..f86ede6f9134e816e3e47f38d98121c2f60036c1
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,72 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: pending
+- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: pending
+- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 0%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
+  - Status: planned
+- Evidence-Type: diff
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+
+Changes Made:
+- In progress.
+
+Validation:
+- Pending execution.
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- In progress.

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\validate_f4_launch_package.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_validate_phase_1_listing_pack.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\validate_shock_scenarios.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python 'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\validate_public_transparency_contract.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -c \"import json, pathlib; data=json.loads(pathlib.Path(r'C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))\"" in C:\Users\edebe\eds succeeded in 3.49s:
f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6
 succeeded in 3.60s:
phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git status --short -- 'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy' 'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py' 'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json' 'workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md'" in C:\Users\edebe\eds succeeded in 3.47s:
validation_passed
 succeeded in 3.16s:
governance_registry_ok parameters=13
 succeeded in 4.18s:
shock_validation_passed scenarios=4 scenario_ids=zar_30pct_macro_dislocation,kes_35pct_proxy_liquidity_shock,ghs_45pct_anchor_dislocation,ngn_50pct_macro_dislocation checks=vault_capital_integrity,liquidity_continuity,funding_stabilization,transparency_outputs,governance_stability artifact=C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json
 succeeded in 5.55s:
?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/
?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
?? workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..f86ede6f9134e816e3e47f38d98121c2f60036c1
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,72 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: pending
+- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: pending
+- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 0%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
+  - Status: planned
+- Evidence-Type: diff
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+
+Changes Made:
+- In progress.
+
+Validation:
+- Pending execution.
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- In progress.

codex
The validation chain is clean now. I’m doing the final lifecycle bookkeeping: recording the F2 reference fix, capturing the exact pass outputs, and moving this task from `200_inprogress` to `300_complete`.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'Get-Date -Format o' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md'" in C:\Users\edebe\eds succeeded in 1.58s:
Source:
- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`

Task Summary:
- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.

Context:
- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Upstream implementation artifacts:
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
- Target F4 deliverables:
  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
 succeeded in 1.67s:
2026-03-19T17:11:13.1142503+00:00
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..f86ede6f9134e816e3e47f38d98121c2f60036c1
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,72 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: pending
+- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: pending
+- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 0%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
+  - Status: planned
+- Evidence-Type: diff
+  - Artifact: `not_applicable`
+  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+
+Changes Made:
+- In progress.
+
+Validation:
+- Pending execution.
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- In progress.

file update
M C:\Users\edebe\eds\workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,3 +1,3 @@
 Source:
-- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`
 - Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
@@ -29,27 +29,27 @@
 Plan:
-- [ ] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
-  - [ ] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
-  - Evidence: pending
-- [ ] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
-  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
-  - Evidence: pending
-- [ ] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
-  - [ ] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
-  - Evidence: pending
+- [x] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [x] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: PASS. The lifecycle record was rewritten into the required template before implementation and updated with the final artifact set and validation results.
+- [x] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [x] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: PASS. Validator output was `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`.
+- [x] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [x] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: PASS. Outputs were `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`, `validation_passed`, `shock_validation_passed ...`, and `governance_registry_ok parameters=13`.
 
 Evidence:
-Objective-Delivery-Coverage: 0%
+Objective-Delivery-Coverage: 100%
 Auto-Acceptance: true
 - Evidence-Type: file_output
-  - Artifact: `not_applicable`
-  - Objective-Proved: Placeholder until the F4 deploy artifacts are written.
-  - Status: planned
+  - Artifact: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - Objective-Proved: The full F4 launch package exists in the epic output folder with the required runbook, readiness checklist, dependency register, and decision memo.
+  - Status: captured
 - Evidence-Type: test_output
-  - Artifact: `not_applicable`
-  - Objective-Proved: Placeholder until the F4 package validator and upstream validators are executed.
-  - Status: planned
+  - Artifact: `python ...\validate_f4_launch_package.py` => `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`; `python ...\workstream_f2_validate_phase_1_listing_pack.py` => `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`; `python ...\validate_public_transparency_contract.py` => `validation_passed`; `python ...\validate_shock_scenarios.py` => `shock_validation_passed scenarios=4 ...`; governance inline check => `governance_registry_ok parameters=13`
+  - Objective-Proved: The new F4 package validates cleanly and its linked configuration, transparency, governance, and shock-evidence inputs all pass technical validation in the current workspace.
+  - Status: captured
 - Evidence-Type: diff
-  - Artifact: `not_applicable`
-  - Objective-Proved: Placeholder until the package files and lifecycle record are updated.
-  - Status: planned
+  - Artifact: `git status --short -- ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md` => `??` for the new deploy and validator artifacts plus the updated F2 pack and lifecycle file before archival move.
+  - Objective-Proved: The workspace changes for this task are limited to the F4 package artifacts, the F4 validator, the required F2 reference fix, and the lifecycle record.
+  - Status: captured
 
@@ -59,8 +59,28 @@
 - 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+- 2026-03-19T17:11:13.1142503+00:00: Added the F4 deploy artifacts under `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\` and implemented `verification\validate_f4_launch_package.py`.
+- 2026-03-19T17:11:13.1142503+00:00: Ran the F4 validator and linked upstream validators. The first F2 validation failed because the listing pack still referenced the pre-rename epic path.
+- 2026-03-19T17:11:13.1142503+00:00: Updated `workstream_f2_phase_1_listing_pack.json` to point at `20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`, then reran the full validation chain successfully.
+- 2026-03-19T17:11:13.1142503+00:00: Recorded the conservative readiness outcome as `no_go` for public launch until the dashboard evidence is live-backed rather than mock-backed.
 
 Changes Made:
-- In progress.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md` with startup, monitoring, halt, reopen, escalation, and stop-condition procedures tied to F1/F2/E1/E2/F3 evidence.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json` with the required `prelaunch_check`, `runtime_monitor`, `halt_procedure`, `reopen_procedure`, `owner`, and `evidence_link` fields plus unresolved launch risks.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv` to normalize E1/E2/E3/F1/F2/F3 readiness status, blockers, evidence links, and follow-up actions.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md` with a dated readiness decision package and explicit exit criteria to move from `no_go` to `go`.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py` to validate runbook sections, checklist fields, dependency coverage, and decision memo structure.
+- Updated `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json` so its epic references follow the current `_processed.md` path and the upstream validator passes again.
 
 Validation:
-- Pending execution.
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+  - Result: `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`
+  - Result: `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`
+  - Result: `validation_passed`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`
+  - Result: `shock_validation_passed scenarios=4 scenario_ids=zar_30pct_macro_dislocation,kes_35pct_proxy_liquidity_shock,ghs_45pct_anchor_dislocation,ngn_50pct_macro_dislocation checks=vault_capital_integrity,liquidity_continuity,funding_stabilization,transparency_outputs,governance_stability artifact=C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"`
+  - Result: `governance_registry_ok parameters=13`
+- `git status --short -- ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+  - Result: `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py`, `?? workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
 
@@ -68,2 +88,3 @@
 - The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- The package is complete and validated as documentation plus technical evidence, but its substantive decision is intentionally conservative: internal rehearsal is supportable, public MVP launch is not yet approved.
 - This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
@@ -71,2 +92,2 @@
 Completion Status:
-- In progress.
+- Complete as of 2026-03-19T17:11:13.1142503+00:00. Auto-acceptance criteria met with 100% evidence coverage.
apply_patch(auto_approved=true) exited 0 in 2.99s:
Success. Updated the following files:
M workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..01e4143a006639e105e6b6f83993df26a039c84a
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,93 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [x] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [x] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: PASS. The lifecycle record was rewritten into the required template before implementation and updated with the final artifact set and validation results.
+- [x] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [x] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: PASS. Validator output was `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`.
+- [x] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [x] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: PASS. Outputs were `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`, `validation_passed`, `shock_validation_passed ...`, and `governance_registry_ok parameters=13`.
+
+Evidence:
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - Objective-Proved: The full F4 launch package exists in the epic output folder with the required runbook, readiness checklist, dependency register, and decision memo.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python ...\validate_f4_launch_package.py` => `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`; `python ...\workstream_f2_validate_phase_1_listing_pack.py` => `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`; `python ...\validate_public_transparency_contract.py` => `validation_passed`; `python ...\validate_shock_scenarios.py` => `shock_validation_passed scenarios=4 ...`; governance inline check => `governance_registry_ok parameters=13`
+  - Objective-Proved: The new F4 package validates cleanly and its linked configuration, transparency, governance, and shock-evidence inputs all pass technical validation in the current workspace.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `git status --short -- ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md` => `??` for the new deploy and validator artifacts plus the updated F2 pack and lifecycle file before archival move.
+  - Objective-Proved: The workspace changes for this task are limited to the F4 package artifacts, the F4 validator, the required F2 reference fix, and the lifecycle record.
+  - Status: captured
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+- 2026-03-19T17:11:13.1142503+00:00: Added the F4 deploy artifacts under `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\` and implemented `verification\validate_f4_launch_package.py`.
+- 2026-03-19T17:11:13.1142503+00:00: Ran the F4 validator and linked upstream validators. The first F2 validation failed because the listing pack still referenced the pre-rename epic path.
+- 2026-03-19T17:11:13.1142503+00:00: Updated `workstream_f2_phase_1_listing_pack.json` to point at `20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`, then reran the full validation chain successfully.
+- 2026-03-19T17:11:13.1142503+00:00: Recorded the conservative readiness outcome as `no_go` for public launch until the dashboard evidence is live-backed rather than mock-backed.
+
+Changes Made:
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md` with startup, monitoring, halt, reopen, escalation, and stop-condition procedures tied to F1/F2/E1/E2/F3 evidence.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json` with the required `prelaunch_check`, `runtime_monitor`, `halt_procedure`, `reopen_procedure`, `owner`, and `evidence_link` fields plus unresolved launch risks.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv` to normalize E1/E2/E3/F1/F2/F3 readiness status, blockers, evidence links, and follow-up actions.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md` with a dated readiness decision package and explicit exit criteria to move from `no_go` to `go`.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py` to validate runbook sections, checklist fields, dependency coverage, and decision memo structure.
+- Updated `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json` so its epic references follow the current `_processed.md` path and the upstream validator passes again.
+
+Validation:
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+  - Result: `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`
+  - Result: `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`
+  - Result: `validation_passed`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`
+  - Result: `shock_validation_passed scenarios=4 scenario_ids=zar_30pct_macro_dislocation,kes_35pct_proxy_liquidity_shock,ghs_45pct_anchor_dislocation,ngn_50pct_macro_dislocation checks=vault_capital_integrity,liquidity_continuity,funding_stabilization,transparency_outputs,governance_stability artifact=C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"`
+  - Result: `governance_registry_ok parameters=13`
+- `git status --short -- ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+  - Result: `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py`, `?? workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- The package is complete and validated as documentation plus technical evidence, but its substantive decision is intentionally conservative: internal rehearsal is supportable, public MVP launch is not yet approved.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- Complete as of 2026-03-19T17:11:13.1142503+00:00. Auto-acceptance criteria met with 100% evidence coverage.

file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..01e4143a006639e105e6b6f83993df26a039c84a
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -1,65 +1,93 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source:
+- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`
+- Derived task seed previously located at `C:\Users\edebe\eds\workstream\100_backlog\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Task Summary:
+- Produce the operator-facing MVP launch package for the sFX venue by assembling a concrete runbook, readiness checklist, dependency register, and go/no-go memo that cite the implemented F/E evidence and surface any remaining release blockers.
+
+Context:
+- Epic output root: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
+- Upstream implementation artifacts:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+- Target F4 deliverables:
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+
+Dependency:
+Dependency: `E1`, `E2`, `E3`, `F1`, `F2`, and `F3` artifacts listed in Context. This task consumes their delivered files and readiness evidence; it does not replace their validation.
+
+Plan:
+- [x] 1. Normalize the active task record and define the F4 package structure against the implemented upstream evidence.
+  - [x] Test: Confirm this lifecycle file includes `Source`, `Dependency`, ordered `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Risks/Notes`, and `Completion Status` sections with the F4 deliverable paths recorded in `Context`.
+  - Evidence: PASS. The lifecycle record was rewritten into the required template before implementation and updated with the final artifact set and validation results.
+- [x] 2. Implement the MVP launch package artifacts in the epic output folder with explicit startup, monitoring, halt, reopening, dependency, ownership, evidence-link, and unresolved-risk coverage.
+  - [x] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`; pass if the validator reports `f4_launch_package_ok` and confirms runbook procedures, checklist fields, dependency coverage, and decision memo evidence links.
+  - Evidence: PASS. Validator output was `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`.
+- [x] 3. Re-run the linked upstream validations, capture results in this task record, and finalize the readiness decision package.
+  - [x] Test: `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`, `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`, and `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` all pass.
+  - Evidence: PASS. Outputs were `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`, `validation_passed`, `shock_validation_passed ...`, and `governance_registry_ok parameters=13`.
+
+Evidence:
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv`, `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md`
+  - Objective-Proved: The full F4 launch package exists in the epic output folder with the required runbook, readiness checklist, dependency register, and decision memo.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python ...\validate_f4_launch_package.py` => `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`; `python ...\workstream_f2_validate_phase_1_listing_pack.py` => `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`; `python ...\validate_public_transparency_contract.py` => `validation_passed`; `python ...\validate_shock_scenarios.py` => `shock_validation_passed scenarios=4 ...`; governance inline check => `governance_registry_ok parameters=13`
+  - Objective-Proved: The new F4 package validates cleanly and its linked configuration, transparency, governance, and shock-evidence inputs all pass technical validation in the current workspace.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `git status --short -- ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md` => `??` for the new deploy and validator artifacts plus the updated F2 pack and lifecycle file before archival move.
+  - Objective-Proved: The workspace changes for this task are limited to the F4 package artifacts, the F4 validator, the required F2 reference fix, and the lifecycle record.
+  - Status: captured
+
+Implementation Log:
+- 2026-03-19 Europe/London: Read `C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md`, the assigned F4 task file, and the existing sFX workspace structure.
+- 2026-03-19 Europe/London: Reviewed completed upstream E1, E2, F1, F2, and F3 lifecycle records plus the concrete transparency, governance, listing-pack, circuit-breaker, and shock-validation artifacts to determine what the launch package can cite.
+- 2026-03-19 Europe/London: Confirmed the transparency dashboard evidence present in the workspace is a smoke-tested mock-backed snapshot rather than a demonstrated live-integrated production dashboard, which must be reflected in the readiness decision.
+- 2026-03-19T17:11:13.1142503+00:00: Added the F4 deploy artifacts under `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\` and implemented `verification\validate_f4_launch_package.py`.
+- 2026-03-19T17:11:13.1142503+00:00: Ran the F4 validator and linked upstream validators. The first F2 validation failed because the listing pack still referenced the pre-rename epic path.
+- 2026-03-19T17:11:13.1142503+00:00: Updated `workstream_f2_phase_1_listing_pack.json` to point at `20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`, then reran the full validation chain successfully.
+- 2026-03-19T17:11:13.1142503+00:00: Recorded the conservative readiness outcome as `no_go` for public launch until the dashboard evidence is live-backed rather than mock-backed.
+
+Changes Made:
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md` with startup, monitoring, halt, reopen, escalation, and stop-condition procedures tied to F1/F2/E1/E2/F3 evidence.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_readiness_checklist.json` with the required `prelaunch_check`, `runtime_monitor`, `halt_procedure`, `reopen_procedure`, `owner`, and `evidence_link` fields plus unresolved launch risks.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_dependency_register.csv` to normalize E1/E2/E3/F1/F2/F3 readiness status, blockers, evidence links, and follow-up actions.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_go_no_go_decision_memo.md` with a dated readiness decision package and explicit exit criteria to move from `no_go` to `go`.
+- Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py` to validate runbook sections, checklist fields, dependency coverage, and decision memo structure.
+- Updated `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json` so its epic references follow the current `_processed.md` path and the upstream validator passes again.
+
+Validation:
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py`
+  - Result: `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`
+  - Result: `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`
+  - Result: `validation_passed`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`
+  - Result: `shock_validation_passed scenarios=4 scenario_ids=zar_30pct_macro_dislocation,kes_35pct_proxy_liquidity_shock,ghs_45pct_anchor_dislocation,ngn_50pct_macro_dislocation checks=vault_capital_integrity,liquidity_continuity,funding_stabilization,transparency_outputs,governance_stability artifact=C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"`
+  - Result: `governance_registry_ok parameters=13`
+- `git status --short -- ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+  - Result: `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py`, `?? workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
+
+Risks/Notes:
+- The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
+- The package is complete and validated as documentation plus technical evidence, but its substantive decision is intentionally conservative: internal rehearsal is supportable, public MVP launch is not yet approved.
+- This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
+
+Completion Status:
+- Complete as of 2026-03-19T17:11:13.1142503+00:00. Auto-acceptance criteria met with 100% evidence coverage.

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Move-Item 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md' 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex\\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md'" in C:\Users\edebe\eds succeeded in 2.06s:

file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
deleted file mode 100644
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ /dev/null
@@ -1,65 +0,0 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29

file update
M C:\Users\edebe\eds\workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -63,2 +63,3 @@
 - 2026-03-19T17:11:13.1142503+00:00: Recorded the conservative readiness outcome as `no_go` for public launch until the dashboard evidence is live-backed rather than mock-backed.
+- 2026-03-19T17:11:13.1142503+00:00: Moved this lifecycle record from `workstream/200_inprogress/codex/` to `workstream/300_complete/codex/` after all checklist items, evidence items, and validations were complete.
 
apply_patch(auto_approved=true) exited 0 in 2.51s:
Success. Updated the following files:
M workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
deleted file mode 100644
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ /dev/null
@@ -1,65 +0,0 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 01e4143a006639e105e6b6f83993df26a039c84a..48bf720274005d7e684a692944376e9d3a92242e
--- a/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -61,6 +61,7 @@
 - 2026-03-19T17:11:13.1142503+00:00: Ran the F4 validator and linked upstream validators. The first F2 validation failed because the listing pack still referenced the pre-rename epic path.
 - 2026-03-19T17:11:13.1142503+00:00: Updated `workstream_f2_phase_1_listing_pack.json` to point at `20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`, then reran the full validation chain successfully.
 - 2026-03-19T17:11:13.1142503+00:00: Recorded the conservative readiness outcome as `no_go` for public launch until the dashboard evidence is live-backed rather than mock-backed.
+- 2026-03-19T17:11:13.1142503+00:00: Moved this lifecycle record from `workstream/200_inprogress/codex/` to `workstream/300_complete/codex/` after all checklist items, evidence items, and validations were complete.
 
 Changes Made:
 - Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md` with startup, monitoring, halt, reopen, escalation, and stop-condition procedures tied to F1/F2/E1/E2/F3 evidence.

file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
deleted file mode 100644
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ /dev/null
@@ -1,65 +0,0 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 01e4143a006639e105e6b6f83993df26a039c84a..48bf720274005d7e684a692944376e9d3a92242e
--- a/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -61,6 +61,7 @@
 - 2026-03-19T17:11:13.1142503+00:00: Ran the F4 validator and linked upstream validators. The first F2 validation failed because the listing pack still referenced the pre-rename epic path.
 - 2026-03-19T17:11:13.1142503+00:00: Updated `workstream_f2_phase_1_listing_pack.json` to point at `20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`, then reran the full validation chain successfully.
 - 2026-03-19T17:11:13.1142503+00:00: Recorded the conservative readiness outcome as `no_go` for public launch until the dashboard evidence is live-backed rather than mock-backed.
+- 2026-03-19T17:11:13.1142503+00:00: Moved this lifecycle record from `workstream/200_inprogress/codex/` to `workstream/300_complete/codex/` after all checklist items, evidence items, and validations were complete.
 
 Changes Made:
 - Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md` with startup, monitoring, halt, reopen, escalation, and stop-condition procedures tied to F1/F2/E1/E2/F3 evidence.

Plan update
The F4 package artifacts were added, the broken F2 reference was corrected, all validators passed, and the lifecycle record was archived to 300_complete.
  ✓ Normalize the F4 lifecycle task file to the required template with ordered plan steps and evidence placeholders.
  ✓ Implement the MVP launch package artifacts in the sFX epic output folder.
  ✓ Run technical validations, capture evidence, update the lifecycle file, and move it to complete.
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
deleted file mode 100644
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ /dev/null
@@ -1,65 +0,0 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 01e4143a006639e105e6b6f83993df26a039c84a..48bf720274005d7e684a692944376e9d3a92242e
--- a/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -61,6 +61,7 @@
 - 2026-03-19T17:11:13.1142503+00:00: Ran the F4 validator and linked upstream validators. The first F2 validation failed because the listing pack still referenced the pre-rename epic path.
 - 2026-03-19T17:11:13.1142503+00:00: Updated `workstream_f2_phase_1_listing_pack.json` to point at `20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`, then reran the full validation chain successfully.
 - 2026-03-19T17:11:13.1142503+00:00: Recorded the conservative readiness outcome as `no_go` for public launch until the dashboard evidence is live-backed rather than mock-backed.
+- 2026-03-19T17:11:13.1142503+00:00: Moved this lifecycle record from `workstream/200_inprogress/codex/` to `workstream/300_complete/codex/` after all checklist items, evidence items, and validations were complete.
 
 Changes Made:
 - Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md` with startup, monitoring, halt, reopen, escalation, and stop-condition procedures tied to F1/F2/E1/E2/F3 evidence.

codex
Implemented the F4 launch package and archived the lifecycle task to [workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md). The new package is in [f4_mvp_launch_runbook.md](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md), [f4_mvp_readiness_checklist.json](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json), [f4_dependency_register.csv](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv), and [f4_go_no_go_decision_memo.md](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md). I also added [validate_f4_launch_package.py](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py).

The readiness decision is `no_go` for a public MVP launch as of 2026-03-19 because the dashboard evidence in the workspace is still mock-backed, not live-backed. While validating the package, I found and fixed a broken F2 upstream reference in [workstream_f2_phase_1_listing_pack.json](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json), which restored the full validation chain.

Validation passed:
- `python ...\validate_f4_launch_package.py` -> `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`
- `python ...\workstream_f2_validate_phase_1_listing_pack.py` -> `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`
- `python ...\validate_public_transparency_contract.py` -> `validation_passed`
- `python ...\validate_shock_scenarios.py` -> `shock_validation_passed ...`
- governance registry check -> `governance_registry_ok parameters=13`
file update:
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
new file mode 100644
index 0000000000000000000000000000000000000000..095b266dbeee7951d451be70bcac1cc203175349
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv
@@ -0,0 +1,7 @@
+dependency_id,artifact_type,owner,readiness_state,evidence_link,blocking_gap,follow_up_action
+E1,public_transparency_contract,Transparency Operator,ready_with_constraints,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md,No live-backed dashboard evidence in the package,Keep E1 contract and live publisher aligned and rerun validation with live inputs
+E2,governance_registry_and_framework,Governance Liaison,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json,None,Retain restrictive-only emergency policy and bounded registry before launch
+E3,operator_market_state_surface,Transparency Operator,blocked,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt,Smoke evidence states the surface is using deterministic mock transparency data,Complete live publication integration and capture a fresh live-backed smoke artifact
+F1,isolation_containment_model,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md,None,Keep cross-margin and inter-vault borrowing disabled
+F2,phase_1_listing_pack,Launch Commander,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json,None,Revalidate the pack before the next launch window
+F3,shock_validation_results,Risk Duty Officer,ready,C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json,None,Repeat deterministic shock validation after any control-band or listing-pack change
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
new file mode 100644
index 0000000000000000000000000000000000000000..dd7684bb1e3689eecdb836f805d8ac1979e12c80
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md
@@ -0,0 +1,48 @@
+# F4 Go/No-Go Decision Memo
+
+Decision Date: 2026-03-19
+Decision: `no_go`
+Release Scope Evaluated: public phase-1 MVP launch for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
+
+## Executive Summary
+
+The workspace contains sufficient design-time evidence to support a controlled internal rehearsal of the phase-1 sFX launch package. The public external MVP launch should not proceed on 2026-03-19 because the only operator-surface evidence available in the workspace is a dashboard smoke test and snapshot that explicitly rely on deterministic mock transparency data rather than proven live publication inputs.
+
+## Positive Readiness Signals
+
+- Configuration posture is conservative and validated through the F2 pack.
+- Emergency governance remains bounded and restrictive-only.
+- Deterministic macro-shock scenarios from `30%` to `50%` all pass scorecard checks.
+- Per-instrument containment and local loss boundaries are documented.
+- Transparency contract fields, cadences, and redaction boundaries are defined and validated.
+
+## Blocking Findings
+
+1. `E3` remains a launch blocker for a public release.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
+   - Rationale: the snapshot states the dashboard is using deterministic mock transparency data, so the package does not yet prove a live production publication path.
+2. The current package proves deterministic validation, not live operating rehearsal.
+   - Evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+   - Rationale: the shock results are strong, but they validate control contracts and expected reactions rather than a live connected venue.
+
+## Supporting Evidence
+
+- Configuration evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- Governance evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json`
+- Transparency evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- Isolation evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- Shock-test evidence link: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+
+## Required Exit Criteria To Move To Go
+
+1. Replace the mock-backed transparency surface with a live-backed publication flow.
+2. Capture a fresh dashboard smoke test and snapshot proving live publication inputs.
+3. Re-run F2, E1, F3, and F4 validations against the live-backed operator surface.
+4. Execute at least one internal shadow launch rehearsal with incident, halt, and reopen drills.
+
+## Owner And Follow-Up
+
+- Blocking owner: Transparency Operator
+- Decision owner: Launch Commander
+- Next review trigger: completion of live-backed dashboard validation artifacts
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
new file mode 100644
index 0000000000000000000000000000000000000000..52e5a08f77671a9dd62219c43807579c7d81ea07
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md
@@ -0,0 +1,143 @@
+# F4 MVP Launch Runbook
+
+## Purpose
+
+Operate the phase-1 sFX MVP launch in a conservative mode that keeps each instrument isolated, publishes the required public state, and escalates immediately into deterministic protective controls if health degrades.
+
+## Launch Scope
+
+- Phase-1 instruments: `NGN_VOL`, `KES_VOL`, `GHS_VOL`, `ZAR_VOL`
+- Operating posture: conservative MVP with per-instrument vault isolation, no cross-margin, aggregate exposure cap fraction `0.55`, reserve buffer fraction `0.45`
+- Default decision status for this package on 2026-03-19: `no_go` for public external launch until the transparency surface is backed by live rather than deterministic mock data
+
+## Roles
+
+| Role | Owner | Responsibility |
+|---|---|---|
+| Launch Commander | Operations lead | Owns the go/no-go call, prelaunch checklist sign-off, and incident command |
+| Risk Duty Officer | Risk controls service owner | Monitors leverage, spread, funding, exposure utilization, and control-state drift |
+| Market Controls Engineer | D2/D3 controls owner | Confirms halt-state transitions and staged reopen eligibility |
+| Transparency Operator | Transparency service owner | Confirms snapshot publication freshness and public-state completeness |
+| Governance Liaison | DAO operations delegate | Coordinates any restrictive emergency override and ratification trail |
+
+## Startup Procedure
+
+1. Confirm the approved listing pack is the active phase-1 configuration:
+   - `workstream_f2_phase_1_listing_pack.json`
+   - All four instruments present and marked `launch_ready`
+   - Operational leverage does not exceed `2.0x`
+2. Confirm governance registry is loaded and restrictive-only emergency policy is intact:
+   - `workstreamE_governance_parameter_band_registry.json`
+   - `emergency_policy.restrictive_only = true`
+   - At least the 13 declared bounded parameters are present
+3. Confirm isolation model remains unchanged:
+   - `f1_isolated_margin_and_per_instrument_containment_model.md`
+   - No cross-instrument margining or inter-vault borrowing
+4. Confirm transparency contract validation passes:
+   - `validate_public_transparency_contract.py`
+   - Snapshot payload fields present with 60-second maximum staleness for required top-level values
+5. Confirm shock validation remains green:
+   - `validate_shock_scenarios.py`
+   - All scenarios pass scorecard checks for vault integrity, liquidity continuity, funding stabilization, transparency outputs, and governance stability
+6. Confirm operator visibility surface is reachable:
+   - `verification/20260316_sfx_dashboard_smoke.txt`
+   - Document whether the surface is live-backed or mock-backed before any launch decision
+
+Release gate:
+- Public MVP launch requires all checks above plus a live-backed transparency surface.
+- If the transparency surface remains mock-backed, limit activity to shadow rehearsal, dry run, or internal operational drills only.
+
+## Runtime Monitoring Procedure
+
+Monitor every 60 seconds or faster during the first trading hour:
+
+| Signal | Source | Threshold or expectation | Owner |
+|---|---|---|---|
+| `market_status` | Transparency snapshot plus D3 status | Immediate publish on any state change | Transparency Operator |
+| `current_leverage_band` | C2 output via transparency snapshot | Never above instrument launch cap; investigate any unexplained compression | Risk Duty Officer |
+| `funding_rate` | B3 funding output | Must remain inside model cap and show stabilizing sign | Risk Duty Officer |
+| `exposure_utilization` | F3 results pattern and vault controls | Escalate if utilization approaches emergency tightening zone | Risk Duty Officer |
+| `spread_floor_bps` | C3/D2 active risk band | Must widen under stress, never narrow via emergency path | Risk Duty Officer |
+| `halt_state` and `reopen_stage` | D3 operator model | No manual reopen allowed; only deterministic staged progression | Market Controls Engineer |
+| Transparency freshness | E1 contract | Required fields must remain within staleness budget | Transparency Operator |
+
+Escalation triggers:
+- Any missing required transparency field
+- Any `market_status` transition without corresponding operator alert
+- Emergency-level stress with no leverage compression, spread widening, or cap tightening
+- Any evidence of cross-instrument loss transfer
+- Any emergency request that would widen risk instead of tighten it
+
+## Halt Procedure
+
+Use this procedure for any instrument entering `HALTED` or `HALTED_LOCKDOWN`:
+
+1. Freeze the affected instrument to the published D3 state only. Do not manually reprice or selectively intervene in accounts.
+2. Confirm the trigger family:
+   - `index_divergence_breach`
+   - `oracle_quorum_failure`
+   - `depth_collapse_event`
+   - `liquidation_cluster_emergency`
+   - `control_integrity_failure`
+3. Validate the matching protective actions are present:
+   - leverage compressed toward floor
+   - funding multiplier increased
+   - spread widened to stressed or emergency floor
+   - position-size and open-interest caps tightened
+4. Publish or verify immediate public state update:
+   - `market_status`
+   - `risk_parameter_band`
+   - incident timestamp
+5. If automation failed or controls are inconsistent, Governance Liaison may invoke only a restrictive emergency override from the registry:
+   - `force_reduce_only`
+   - `tighten_leverage_to_floor`
+   - `tighten_spread_to_emergency_floor`
+   - `tighten_position_and_oi_caps`
+   - `freeze_oracle_weights_to_fallback`
+   - `revert_parameter_to_last_good`
+6. Record incident id, trigger metrics, signers, and expiry immediately.
+
+## Reopen Procedure
+
+Reopen only through the D3 staged flow:
+
+1. Confirm cooldown elapsed for `HALTED` or `HALTED_LOCKDOWN`.
+2. Confirm all recovery requirements are true for the full stability window:
+   - depth recovery
+   - source stability
+   - divergence recovery
+3. Permit `REOPEN_STAGE_1` only:
+   - cancel and passive-only quoting
+   - no market orders
+   - no leverage increases
+4. Advance to `REOPEN_STAGE_2` only after the dwell window passes with no trigger relapse.
+5. Advance to `ACTIVE_POST_RECOVERY` only if limited matching remains stable and D2 response lock is cooling down normally.
+6. Return to `ACTIVE` only after the full observation window completes without renewed trigger activation.
+7. If any original trigger reappears during any reopen stage, force `HALTED_LOCKDOWN`.
+
+## Incident Escalation Procedure
+
+1. Launch Commander opens incident command and names the affected instrument scope.
+2. Risk Duty Officer captures the active control state and confirms whether the issue is contained locally or systemic.
+3. Market Controls Engineer verifies D3 transition validity and next eligible transition time.
+4. Transparency Operator confirms public disclosure completeness and freshness.
+5. Governance Liaison is engaged only if the registry allows a restrictive emergency action and automation has failed or needs hardening.
+6. Publish a post-incident report within 24 hours and ratify or roll back any emergency action within 7 days.
+
+## Launch-Day Stop Conditions
+
+- Transparency surface still uses deterministic mock data instead of live publication inputs
+- Governance registry missing, altered outside bounds, or not restrictive-only
+- Any upstream validator fails
+- Any instrument exceeds the approved launch leverage or cap posture
+- Inability to prove per-instrument isolation and local loss containment
+
+## Evidence References
+
+- F1 isolation model: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
+- F2 listing pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json`
+- E1 transparency pack: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\transparency\public_transparency_disclosure_pack.md`
+- E2 governance framework: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_and_emergency_override_framework.md`
+- F3 shock results: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- Dashboard smoke evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_dashboard_smoke.txt`
+- Dashboard snapshot evidence: `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\20260316_sfx_market_state_snapshot.html`
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
new file mode 100644
index 0000000000000000000000000000000000000000..81e17889767149b219de8d10794955f2848790de
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json
@@ -0,0 +1,75 @@
+{
+  "package_id": "f4.mvp_launch_readiness.v1",
+  "generated_on": "2026-03-19",
+  "decision_status": "no_go",
+  "checklist": [
+    {
+      "check_id": "phase_1_config",
+      "prelaunch_check": "Validate the F2 listing pack is the approved phase-1 configuration for NGN_VOL, KES_VOL, GHS_VOL, and ZAR_VOL with operational leverage at or below 2.0x.",
+      "runtime_monitor": "Watch current_leverage_band, open_interest, and exposure_utilization every 60 seconds for drift outside the approved launch posture.",
+      "halt_procedure": "If any instrument breaches approved launch posture or cap logic, force reduce-only through the restrictive emergency path and hold the market in HALTED or HALTED_LOCKDOWN.",
+      "reopen_procedure": "Resume only through D3 staged reopening after the validated configuration has been restored and recovery checks remain green for the full stability window.",
+      "owner": "Launch Commander",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstream_f2_phase_1_listing_pack.json"
+    },
+    {
+      "check_id": "governance_safety",
+      "prelaunch_check": "Confirm the governance registry is present, bounded, and restrictive-only for emergency operation.",
+      "runtime_monitor": "Watch for any parameter activation outside published min or max bands and confirm immediate disclosure of any emergency action.",
+      "halt_procedure": "If governance integrity fails, revert the affected parameter to last-good value and keep the affected market in the protective halt path.",
+      "reopen_procedure": "Allow staged reopening only after the registry is revalidated, incident logging is complete, and no emergency override remains active beyond its expiry.",
+      "owner": "Governance Liaison",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\workstreamE_governance_parameter_band_registry.json"
+    },
+    {
+      "check_id": "transparency_contract",
+      "prelaunch_check": "Confirm required public fields, cadences, and redaction boundaries are validated and the operator surface is reachable.",
+      "runtime_monitor": "Watch market_status, funding_rate, current_leverage_band, volatility_metric, and risk_parameter_band for freshness and completeness every 60 seconds.",
+      "halt_procedure": "If required transparency fields are stale or missing, block external launch and fall back to internal drill mode until publication integrity is restored.",
+      "reopen_procedure": "Resume launch readiness only after contract validation passes and the operator surface is confirmed to be live-backed rather than mock-backed.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\transparency\\public_transparency_disclosure_pack.md"
+    },
+    {
+      "check_id": "shock_resilience",
+      "prelaunch_check": "Confirm the deterministic 30% to 50% macro-shock scenarios still pass vault integrity, liquidity continuity, funding stabilization, transparency output, and governance stability checks.",
+      "runtime_monitor": "Watch for live stress states or exposure-utilization patterns that resemble the validated 45% and 50% scenarios and confirm protective controls activate immediately.",
+      "halt_procedure": "If live stress enters emergency state without the expected control reactions, halt the affected instrument and escalate to Market Controls Engineer.",
+      "reopen_procedure": "Use the D3 staged path only after depth, source stability, and divergence recovery requirements stay green for the full window.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\workstream_f3_shock_validation_results.json"
+    },
+    {
+      "check_id": "isolation_containment",
+      "prelaunch_check": "Confirm per-instrument vault isolation remains in force with no cross-margin or inter-vault borrowing enabled.",
+      "runtime_monitor": "Watch incident scope and loss accounting to ensure losses remain instrument-local and unaffected markets remain operable.",
+      "halt_procedure": "If any evidence of cross-instrument loss transfer appears, halt the affected scope immediately and treat it as a global launch blocker.",
+      "reopen_procedure": "Do not reopen until the containment boundary is restored and a post-incident review proves local-only loss absorption.",
+      "owner": "Risk Duty Officer",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\workstreams\\F\\f1_isolated_margin_and_per_instrument_containment_model.md"
+    },
+    {
+      "check_id": "dashboard_operability",
+      "prelaunch_check": "Confirm the market-state dashboard is reachable and identify whether it is operating on live publication inputs or deterministic mock transparency data.",
+      "runtime_monitor": "Watch the dashboard for state changes, freshness, and incident visibility during the launch window.",
+      "halt_procedure": "If the operator surface is unavailable or mock-backed for a public launch, stop the release and continue only as an internal rehearsal.",
+      "reopen_procedure": "Reconsider launch only after a fresh smoke test proves live-backed dashboard operation with the required public fields.",
+      "owner": "Transparency Operator",
+      "evidence_link": "C:\\Users\\edebe\\eds\\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\verification\\20260316_sfx_dashboard_smoke.txt"
+    }
+  ],
+  "unresolved_risks": [
+    {
+      "risk_id": "r1",
+      "summary": "Dashboard evidence available in the workspace is smoke-tested but explicitly uses deterministic mock transparency data rather than proven live publication inputs.",
+      "owner": "Transparency Operator",
+      "follow_up_action": "Complete live data integration and rerun dashboard smoke plus snapshot validation before external launch."
+    },
+    {
+      "risk_id": "r2",
+      "summary": "The launch package relies on design-time and deterministic validation artifacts rather than a live exchange rehearsal with real production telemetry.",
+      "owner": "Launch Commander",
+      "follow_up_action": "Run an internal shadow launch using live publication and control services before any public MVP release."
+    }
+  ]
+}
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
index 1ce30c1d0ec7af73c676df8dff0f39b9bfb27d90..cc084934ba80ff248f3da0bbba2bf22276274f1e
--- a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json
@@ -40,13 +40,13 @@
     },
     {
       "reference_id": "epic_risk_controls",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 4-5 define the leverage model, funding inputs, spread elasticity, and automatic stress responses."
     },
     {
       "reference_id": "epic_governance_launch_scope",
-      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2.md",
+      "artifact_path": "C:\\Users\\edebe\\eds\\workstream\\000_epic\\20260227_022357_sFX_Technical_Design_Brief_v2_processed.md",
       "reference_type": "risk_control_artifact",
       "coverage": "Sections 7-9 define parameter bands, vault allocation caps, instrument isolation, and conservative phase-1 launch scope."
     }
diff --git a/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
new file mode 100644
index 0000000000000000000000000000000000000000..d38ca2e52d9dfcef4651b78e9c7fc77d524c0e3f
--- /dev/null
+++ b/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+import csv
+import json
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[1]
+DEPLOY = ROOT / "deploy"
+
+RUNBOOK_PATH = DEPLOY / "f4_mvp_launch_runbook.md"
+CHECKLIST_PATH = DEPLOY / "f4_mvp_readiness_checklist.json"
+DEPENDENCY_PATH = DEPLOY / "f4_dependency_register.csv"
+DECISION_MEMO_PATH = DEPLOY / "f4_go_no_go_decision_memo.md"
+
+
+def _assert(condition: bool, message: str) -> None:
+    if not condition:
+        raise AssertionError(message)
+
+
+def _load_text(path: Path) -> str:
+    _assert(path.exists(), f"missing_file:{path}")
+    return path.read_text(encoding="utf-8")
+
+
+def validate_runbook() -> None:
+    text = _load_text(RUNBOOK_PATH)
+    required_sections = [
+        "## Startup Procedure",
+        "## Runtime Monitoring Procedure",
+        "## Halt Procedure",
+        "## Reopen Procedure",
+        "## Incident Escalation Procedure",
+    ]
+    for section in required_sections:
+        _assert(section in text, f"missing_runbook_section:{section}")
+
+
+def validate_checklist() -> int:
+    data = json.loads(_load_text(CHECKLIST_PATH))
+    _assert(data["decision_status"] in {"go", "conditional_go", "no_go"}, "invalid_decision_status")
+    required_fields = {
+        "prelaunch_check",
+        "runtime_monitor",
+        "halt_procedure",
+        "reopen_procedure",
+        "owner",
+        "evidence_link",
+    }
+    checklist = data["checklist"]
+    _assert(len(checklist) >= 6, "insufficient_checklist_items")
+    for item in checklist:
+        _assert(required_fields.issubset(item), f"missing_checklist_fields:{item.get('check_id', 'unknown')}")
+        evidence_path = Path(item["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_evidence_link:{evidence_path}")
+    return len(checklist)
+
+
+def validate_dependency_register() -> int:
+    with DEPENDENCY_PATH.open("r", encoding="utf-8", newline="") as handle:
+        rows = list(csv.DictReader(handle))
+    expected = {"E1", "E2", "E3", "F1", "F2", "F3"}
+    actual = {row["dependency_id"] for row in rows}
+    _assert(actual == expected, f"dependency_mismatch:{sorted(actual)}")
+    for row in rows:
+        evidence_path = Path(row["evidence_link"])
+        _assert(evidence_path.exists(), f"missing_dependency_evidence:{evidence_path}")
+    return len(rows)
+
+
+def validate_decision_memo() -> str:
+    text = _load_text(DECISION_MEMO_PATH)
+    _assert("Decision: `no_go`" in text or "Decision: `go`" in text or "Decision: `conditional_go`" in text, "missing_decision")
+    required_markers = [
+        "Configuration evidence link:",
+        "Governance evidence link:",
+        "Transparency evidence link:",
+        "Shock-test evidence link:",
+        "## Blocking Findings",
+        "## Required Exit Criteria To Move To Go",
+    ]
+    for marker in required_markers:
+        _assert(marker in text, f"missing_decision_marker:{marker}")
+    if "Decision: `no_go`" in text:
+        return "no_go"
+    if "Decision: `conditional_go`" in text:
+        return "conditional_go"
+    return "go"
+
+
+def main() -> None:
+    validate_runbook()
+    checklist_items = validate_checklist()
+    dependency_rows = validate_dependency_register()
+    decision = validate_decision_memo()
+    print(
+        f"f4_launch_package_ok decision={decision} "
+        f"checklist_items={checklist_items} dependencies={dependency_rows}"
+    )
+
+
+if __name__ == "__main__":
+    main()
diff --git a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
deleted file mode 100644
index 00639236f6f91c9f4553c41297880dd0c3f52ec2..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ /dev/null
@@ -1,65 +0,0 @@
-# TASK F4: Produce MVP launch runbook and readiness decision package
-
-**Workstream:** F — Launch Readiness and Validation
-**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
-**Priority:** 2
-**Source Epic Path:** workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
-**Epic Output Folder:** C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2
-**Suggested Agent:** general
-**UI Deliverable:** No
-**Status:** [ ] Not Started
-**Workstream Goal:** Prepare an MVP launch package that is conservative, testable, and resilient under shock conditions.
-
----
-
-## Purpose
-
-Consolidate the design, configs, scenarios, and operator checks into a single decision-ready package for MVP launch approval.
-
-## Input
-
-E1-E3 transparency deliverables; E2 governance policy; F1-F3 isolation, config, and simulation outputs.
-
-## Output
-
-Launch runbook, readiness checklist, dependency register, and go/no-go decision memo.
-
-## Fields / Components
-
-- prelaunch_check
-- runtime_monitor
-- halt_procedure
-- reopen_procedure
-- owner
-- evidence_link
-
-## Dependencies
-
-- E1
-- E2
-- E3
-- F1
-- F2
-- F3
-
-## Action
-
-Assemble the operational procedures, readiness checklist, evidence links, and unresolved-risk register required for a controlled MVP release.
-
-## Verification
-
-- [ ] Runbook includes startup, monitoring, halt, reopening, and incident-escalation procedures.
-- [ ] Readiness package links to configuration, transparency, governance, and shock-test evidence.
-- [ ] Open risks and assumptions are explicitly listed with owners or follow-up actions.
-
----
-
-## Notes
-
-- Generated from source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
-- This task is intended for Epic Review allocation before execution.
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md b/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
index 01e4143a006639e105e6b6f83993df26a039c84a..48bf720274005d7e684a692944376e9d3a92242e
--- a/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
+++ b/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md
@@ -61,6 +61,7 @@
 - 2026-03-19T17:11:13.1142503+00:00: Ran the F4 validator and linked upstream validators. The first F2 validation failed because the listing pack still referenced the pre-rename epic path.
 - 2026-03-19T17:11:13.1142503+00:00: Updated `workstream_f2_phase_1_listing_pack.json` to point at `20260227_022357_sFX_Technical_Design_Brief_v2_processed.md`, then reran the full validation chain successfully.
 - 2026-03-19T17:11:13.1142503+00:00: Recorded the conservative readiness outcome as `no_go` for public launch until the dashboard evidence is live-backed rather than mock-backed.
+- 2026-03-19T17:11:13.1142503+00:00: Moved this lifecycle record from `workstream/200_inprogress/codex/` to `workstream/300_complete/codex/` after all checklist items, evidence items, and validations were complete.
 
 Changes Made:
 - Added `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\deploy\f4_mvp_launch_runbook.md` with startup, monitoring, halt, reopen, escalation, and stop-condition procedures tied to F1/F2/E1/E2/F3 evidence.

tokens used
223,127
Implemented the F4 launch package and archived the lifecycle task to [workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md). The new package is in [f4_mvp_launch_runbook.md](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md), [f4_mvp_readiness_checklist.json](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json), [f4_dependency_register.csv](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv), and [f4_go_no_go_decision_memo.md](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md). I also added [validate_f4_launch_package.py](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py).

The readiness decision is `no_go` for a public MVP launch as of 2026-03-19 because the dashboard evidence in the workspace is still mock-backed, not live-backed. While validating the package, I found and fixed a broken F2 upstream reference in [workstream_f2_phase_1_listing_pack.json](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json), which restored the full validation chain.

Validation passed:
- `python ...\validate_f4_launch_package.py` -> `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`
- `python ...\workstream_f2_validate_phase_1_listing_pack.py` -> `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`
- `python ...\validate_public_transparency_contract.py` -> `validation_passed`
- `python ...\validate_shock_scenarios.py` -> `shock_validation_passed ...`
- governance registry check -> `governance_registry_ok parameters=13`


## Execution Evidence
- Agent lane: codex
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/codex\20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md.result.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
The F4 task was already implemented in the workspace, so this execution was a revalidation and documentation refresh rather than a new feature build. I updated the canonical lifecycle record at [20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md) to capture this rerun and confirm the checklist remains complete.

The existing F4 deliverables are present and validated:
[f4_mvp_launch_runbook.md](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_launch_runbook.md), [f4_mvp_readiness_checklist.json](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_mvp_readiness_checklist.json), [f4_dependency_register.csv](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_dependency_register.csv), [f4_go_no_go_decision_memo.md](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/f4_go_no_go_decision_memo.md), and [validate_f4_launch_package.py](C:/Users/edebe/eds/ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py).

Validation passed:
- `python ...\validate_f4_launch_package.py` -> `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`
- `python ...\workstream_f2_validate_phase_1_listing_pack.py` -> `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`
- `python ...\validate_public_transparency_contract.py` -> `validation_passed`
- `python ...\validate_shock_scenarios.py` -> `shock_validation_passed scenarios=4 ...`
- governance inline check -> `governance_registry_ok parameters=13`

Current readiness decision remains `no_go` for public MVP launch because the available dashboard evidence is still mock-backed rather than live-backed.
```
- Stderr:
```text
ification\validate_f4_launch_package.py`
+  - Result: `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`
+  - Result: `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py`
+  - Result: `validation_passed`
+- `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py`
+  - Result: `shock_validation_passed scenarios=4 scenario_ids=zar_30pct_macro_dislocation,kes_35pct_proxy_liquidity_shock,ghs_45pct_anchor_dislocation,ngn_50pct_macro_dislocation checks=vault_capital_integrity,liquidity_continuity,funding_stabilization,transparency_outputs,governance_stability artifact=C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
+- `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"`
+  - Result: `governance_registry_ok parameters=13`
+- `git status --short -- ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md.result.md`
+  - Result: `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py`, `?? workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md.result.md`, `?? workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
 
 Risks/Notes:
 - The available dashboard smoke evidence states the market-state surface is using deterministic mock transparency data. Unless contradicted by stronger live evidence, the readiness memo must treat that as a launch blocker for a public MVP release.
 - The package is complete and validated as documentation plus technical evidence, but its substantive decision is intentionally conservative: internal rehearsal is supportable, public MVP launch is not yet approved.
+- Revalidation on 2026-03-19 found the package still internally consistent; no further code or document changes were required beyond refreshing this lifecycle record.
 - This task is non-UI documentation and packaging work, so no user verification gate is required if technical evidence reaches 100% and auto-acceptance criteria are met.
 
 Completion Status:

tokens used
37,774
```
- Retry scheduled at 2026-03-19 17:33:21

## Execution Evidence
- Execution timestamp: `2026-03-19T17:37:03.8516485+00:00`
- Outcome: Revalidated the existing F4 deliverables end-to-end. No additional implementation changes were required, and the checklist remained complete in the canonical lifecycle record at [20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md).
- Validation:
  - `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_f4_launch_package.py` -> `f4_launch_package_ok decision=no_go checklist_items=6 dependencies=6`
  - `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py` -> `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`
  - `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_public_transparency_contract.py` -> `validation_passed`
  - `python C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\validate_shock_scenarios.py` -> `shock_validation_passed scenarios=4 scenario_ids=zar_30pct_macro_dislocation,kes_35pct_proxy_liquidity_shock,ghs_45pct_anchor_dislocation,ngn_50pct_macro_dislocation checks=vault_capital_integrity,liquidity_continuity,funding_stabilization,transparency_outputs,governance_stability artifact=C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_f3_shock_validation_results.json`
  - `python -c "import json, pathlib; data=json.loads(pathlib.Path(r'C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamE_governance_parameter_band_registry.json').read_text()); assert data['emergency_policy']['restrictive_only'] is True; assert len(data['parameters']) >= 10; print('governance_registry_ok parameters=%d' % len(data['parameters']))"` -> `governance_registry_ok parameters=13`
- Git scope: `git status --short -- ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md.result.md` -> `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/deploy/`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json`, `?? ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/validate_f4_launch_package.py`, `?? workstream/200_inprogress/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md.result.md`, `?? workstream/300_complete/codex/20260313_220647_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_produce_mvp_launch_runbook_and_readiness_decision_package.md`
- Readiness decision: Still `no_go` for public MVP launch because the transparency dashboard evidence in the workspace remains mock-backed rather than live-backed.
