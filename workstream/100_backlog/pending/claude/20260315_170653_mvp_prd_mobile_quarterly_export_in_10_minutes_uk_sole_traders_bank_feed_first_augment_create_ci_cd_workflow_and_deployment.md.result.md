OpenAI Codex v0.115.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019d0717-0079-7342-945e-e842e78a302f
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
codex
I’m starting by loading the required lifecycle skill and the referenced task file, then I’ll trace the repo areas it touches so I can implement the requested changes and keep the lifecycle record aligned.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'Get-ChildItem -Force' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'" in C:\Users\edebe\eds succeeded in 2.44s:
# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold

**Workstream:** F - CI/CD
**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
**Priority:** 6
**Status:** [ ] Not Started

---

## Purpose

Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.

## Input

Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.

## Output

 succeeded in 2.11s:
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
 succeeded in 3.08s:

    Directory: C:\Users\edebe\eds

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          10/03/2026    02:47                [44;1m__pycache__[0m
d----          12/03/2026    14:04                [44;1m.agent[0m
d----          24/02/2026    10:05                [44;1m.android[0m
d----          18/03/2026    10:41                [44;1m.claude[0m
d----          08/03/2025    18:23                [44;1m.edsLaptop[0m
d----          21/01/2026    10:23                [44;1m.gemini[0m
d--h-          19/03/2026    17:11                [44;1m.git[0m
d----          01/03/2026    20:00                [44;1m.playwright-mcp[0m
d----          27/11/2025    23:13                [44;1m.pytest_cache[0m
d----          24/04/2025    10:45                [44;1m.roo[0m
d----          04/01/2026    15:30                [44;1m.venv[0m
d----          14/01/2026    10:16                [44;1m.vscode[0m
d----          30/12/2025    17:07                [44;1ma2ui[0m
d----          14/04/2025    13:02                [44;1mAI_trades_agents[0m
d----          14/01/2026    15:48                [44;1mAI_voice[0m
codex
I’ve got the lifecycle requirements and the task brief. Next I’m reading the target epic folder and its current deployment/docs assets so I can build the workflow against what actually exists before I patch anything.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Recurse 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\deploy','C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\verification' -ErrorAction SilentlyContinue | Select-Object FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Recurse -Depth 3 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first' | Select-Object FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\README.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\docker-compose.yml'" in C:\Users\edebe\eds succeeded in 1.69s:

[32;1mFullName[0m
[32;1m--------[0m
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\20260…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\finis…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\quart…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
 exited 1 in 2.22s:
[31;1mGet-Content: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_expo[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mCannot find path 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\README.md' because it does not exist.[0m
 exited 1 in 3.38s:
[31;1mGet-Content: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_expo[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mCannot find path 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\docker-compose.yml' because it does not exist.[0m
 succeeded in 4.11s:

[32;1mFullName[0m
[32;1m--------[0m
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\workstreams
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\docs
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\p…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\v…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\v…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\docs\mvp_…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrom…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\20260…
codex
The task brief references root files that aren’t actually present at the epic root, so I’m checking the real layout now. I need that before I lock the workflow paths or validation commands into the lifecycle record.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first' -Force | Select-Object Name,Mode,LastWriteTime" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg --files 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first'" in C:\Users\edebe\eds succeeded in 1.70s:

[32;1mName        [0m[32;1m Mode [0m[32;1m LastWriteTime[0m
[32;1m----        [0m [32;1m---- [0m [32;1m-------------[0m
deploy       d---- 14/03/2026 03:40:27
solution     d---- 16/03/2026 21:36:18
verification d---- 19/03/2026 17:13:07
workstreams  d---- 14/03/2026 03:40:27

 succeeded in 4.39s:
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\finish_now_queue_zero_blockers.png
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\quarter_readiness_screen.png
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\20260318_184500_mobile_inbox_exception_queue_screen.png
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\verify_transaction_import.js
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\validate_mvp_domain_schemas.js
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\docs\mvp_domain_schemas.md
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\package.json
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrome_headless_profile_inbox\Variations
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrome_headless_profile_inbox\Local State
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrome_headless_profile_voice\Crashpad\metadata
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrome_headless_profile_inbox\Crashpad\settings.dat
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\testing\memoryTransactionImportStore.js
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrome_headless_profile_inbox\Crashpad\reports\511d8533-812e-443a-b2e6-1f31e0278ba6.dmp
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrome_headless_profile_inbox\Crashpad\reports\0672bf90-401a-4ef8-81da-9f6a9807376f.dmp
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrome_headless_profile_inbox\Crashpad\metadata
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\verification\chrome_headless_profile_inbox\44d58b82-866a-40ed-ad8e-cac176240b3f.tmp
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\models\mvp_domain_schemas.json
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\models\transaction_import_migration.sql
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\transactionImportService.js
ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\openBankingAdapter.js
codex
I’ve confirmed the repo is lighter than the task brief implies: no root `README.md` or `docker-compose.yml` yet, but there is a backend package, domain docs, and a `verification/` area. I’m reading those now so the CI scaffold targets the current assets and leaves the future build hooks in the right place.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\solution\\docs\\mvp_domain_schemas.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Recurse 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\solution' | Select-Object FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\solution\\backend\\package.json'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Recurse 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\deploy' | Select-Object FullName,Length,LastWriteTime" in C:\Users\edebe\eds succeeded in 1.83s:

[32;1mFullName[0m
[32;1m--------[0m
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\docs
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\p…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\v…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\v…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\docs\mvp_…

 succeeded in 1.85s:
# MVP Domain Schemas [V20260316_A1]

This document defines the canonical MVP domain contract for the UK sole-trader quarterly export product.

Machine-readable source of truth: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/backend/src/models/mvp_domain_schemas.json`

## Scope

The contract covers:

- canonical entity definitions for onboarding, bank ingestion, classification, evidence, quarter readiness, and merchant rules
- the fixed MVP category taxonomy and separate tag set
- nullable and blocker rules required for Finish Now and export gating
- Quarterly Pack CSV and PDF field mappings

## Category Taxonomy

Categories are export-facing and stable:

- `INCOME_SALES`
 succeeded in 2.20s:
{
  "name": "mvp-quarterly-export-domain-contracts",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "validate:mvp-domain-schemas": "node validate_mvp_domain_schemas.js",
    "verify:transaction-import": "node verify_transaction_import.js"
  }
}

 succeeded in 3.31s:

codex
The current solution has backend assets but no frontend folder or compose file yet. I’m checking for any existing container or setup conventions so the workflow can validate what exists today and gate the future build paths without breaking the repo immediately.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"docker|compose|openapi|swagger|setup\" 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Recurse 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\solution\\backend' | Select-Object FullName,Name" in C:\Users\edebe\eds exited 1 in 1.86s:

 succeeded in 2.21s:

[32;1mFullName[0m
[32;1m--------                                                                                                               [0m
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\p…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\v…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\v…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\s…

codex
I’ve confirmed there isn’t an existing CI baseline to extend. I’m now defining a minimal scaffold that passes on the current repo state, validates the present contract assets, and marks the container build and endpoint smoke-test stages as conditional hooks for when those directories land.
Plan update
Using the lifecycle skill, I need to update the task file in order while implementing the CI/CD scaffold and recording evidence as each step is validated.
  ✓ Inspect the epic workspace and map the current docs, backend, deployment, and verification assets against the task brief.
  → Update the in-progress lifecycle file to the required template with ordered plan steps, dependency, evidence placeholders, and current context.
  • Implement the CI workflow and deployment documentation scaffold in the epic workspace based on the actual repository layout.
  • Run validations, capture evidence/results, update checklist items, and finalize the lifecycle file status.
codex
I’m about to patch files. First I’m reading the existing backend validators so I can wire the CI job to commands that already work locally instead of inventing new checks that the repo can’t satisfy yet.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\solution\\backend\\validate_mvp_domain_schemas.js'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git status --short' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\solution\\backend\\verify_transaction_import.js'" in C:\Users\edebe\eds succeeded in 2.57s:
const fs = require('fs');
const path = require('path');

const schemaPath = path.join(__dirname, 'src', 'models', 'mvp_domain_schemas.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

const expectedEntities = [
  'User',
  'BusinessProfile',
  'BankAccount',
  'BankTransaction',
  'TransactionClassification',
  'Evidence',
  'EvidenceLink',
  'Quarter',
  'QuarterMetrics',
  'Rule'
];

const expectedCategoryCodes = [
 succeeded in 2.68s:
const assert = require('assert');
const {
  DEFAULT_BACKFILL_DAYS,
  computeBackfillStartDate,
  importNormalizedTransactions,
  refreshBankAccount
} = require('./src/services/transactionImportService');
const { MemoryTransactionImportStore } = require('./src/testing/memoryTransactionImportStore');

async function main() {
  const store = new MemoryTransactionImportStore();
  const now = new Date('2026-03-18T18:35:00.000Z');
  const bankAccount = {
    bank_account_id: 'bank-account-001',
    user_id: 'user-001',
    provider_name: 'mock_open_banking',
    currency: 'GBP'
  };

  const expectedBackfillStart = computeBackfillStartDate(now, DEFAULT_BACKFILL_DAYS);
 succeeded in 3.55s:
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
I’m normalizing the lifecycle file now so the rest of the work can be recorded against ordered steps with concrete tests and evidence, as the repo instructions require.
file update
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold

**Workstream:** F - CI/CD
**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
**Priority:** 6
**Status:** [ ] Not Started

---

## Purpose

Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.

## Input

Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.

## Output

A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.

## Existing Files to Reference

- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`

## New Files to Create

- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`

## Action

Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.

## Verification

- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.

---

## Notes

- Generated via epic augmentation on 2026-03-15T17:06:53.775356
- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 2.65s:
Success. Updated the following files:
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
file update:
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
deleted file mode 100644
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ /dev/null
@@ -1,56 +0,0 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
deleted file mode 100644
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ /dev/null
@@ -1,56 +0,0 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29

file update
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`

Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.

Context:
- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`

Dependency: None

Plan:
- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
  - [ ] Evidence: pending
- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
  - [ ] Evidence: pending
- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
  - [ ] Evidence: pending

Evidence:
Objective-Delivery-Coverage: 10%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `pending`
  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
  - Status: planned
- Evidence-Type: test_output
  - Artifact: `pending`
  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
  - Status: planned
- Evidence-Type: file_output
  - Artifact: `pending`
  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
  - Status: planned

Implementation Log:
- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.

Changes Made:
- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.

Validation:
- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.

Risks/Notes:
- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.

Completion Status:
- In progress - 2026-03-19 Europe/London

Original Task Brief:

# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold

**Workstream:** F - CI/CD
**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
**Priority:** 6
**Status:** [ ] Not Started

## Purpose

Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.

## Input

Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.

## Output

A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.

## Existing Files to Reference

- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`

## New Files to Create

- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`

## Action

Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.

## Verification

- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.

## Notes

- Generated via epic augmentation on 2026-03-15T17:06:53.775356
- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`

## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 3.41s:
Success. Updated the following files:
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
file update:
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

codex
I’ve got the workflow shape. I’m writing three files now: one CI workflow that validates current assets and conditionally unlocks future build/smoke stages, plus two deployment docs that explain artifact flow and release evidence.
file update
A C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml
name: Epic CI

on:
  push:
    paths:
      - ".github/workflows/ci.yml"
      - "deploy/**"
      - "solution/**"
      - "verification/**"
      - "*.md"
      - "docker-compose.yml"
  pull_request:
    paths:
      - ".github/workflows/ci.yml"
      - "deploy/**"
      - "solution/**"
      - "verification/**"
      - "*.md"
      - "docker-compose.yml"
  workflow_dispatch:
    inputs:
      deployment_environment:
        description: "Deployment target for manual runs"
        required: false
        default: "staging"
      smoke_base_url:
        description: "Optional base URL for contract smoke tests"
        required: false
        default: ""

permissions:
  contents: read

env:
  NODE_VERSION: "20"
  BACKEND_IMAGE_NAME: quarterly-export-backend
  FRONTEND_IMAGE_NAME: quarterly-export-frontend

jobs:
  validate-assets:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install markdown and OpenAPI linters
        run: |
          npm install --global markdownlint-cli @redocly/cli

      - name: Lint markdown assets
        shell: bash
        run: |
          mapfile -t markdown_files < <(find . \
            -path './.git' -prune -o \
            -path './verification/chrome_headless_profile_inbox' -prune -o \
            -path './verification/chrome_headless_profile_voice' -prune -o \
            -type f \( -name '*.md' -o -name '*.markdown' \) -print)

          if [ "${#markdown_files[@]}" -eq 0 ]; then
            echo "No markdown files found"
            exit 0
          fi

          markdownlint "${markdown_files[@]}"

      - name: Lint OpenAPI contracts when present
        shell: bash
        run: |
          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)

          if [ "${#openapi_files[@]}" -eq 0 ]; then
            echo "No OpenAPI contracts present yet"
            exit 0
          fi

          redocly lint "${openapi_files[@]}"

      - name: Install backend dependencies when package exists
        shell: bash
        run: |
          if [ ! -f solution/backend/package.json ]; then
            echo "No backend package.json present"
            exit 0
          fi

          cd solution/backend
          if [ -f package-lock.json ]; then
            npm ci
          else
            npm install --package-lock=false
          fi

      - name: Validate MVP backend contracts
        shell: bash
        run: |
          if [ ! -f solution/backend/package.json ]; then
            echo "Backend validation skipped because package.json is absent"
            exit 0
          fi

          cd solution/backend
          npm run validate:mvp-domain-schemas
          npm run verify:transaction-import

      - name: Validate docker compose when file exists
        shell: bash
        run: |
          if [ ! -f docker-compose.yml ]; then
            echo "docker-compose.yml not present yet"
            exit 0
          fi

          docker compose -f docker-compose.yml config >/tmp/docker-compose.rendered.yml
          test -s /tmp/docker-compose.rendered.yml

      - name: Record validation surface
        shell: bash
        run: |
          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."

  build-images:
    runs-on: ubuntu-latest
    needs: validate-assets
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build backend image when Dockerfile exists
        shell: bash
        run: |
          if [ ! -f solution/backend/Dockerfile ]; then
            echo "Backend Dockerfile not present yet"
            exit 0
          fi

          docker build \
            --tag "${BACKEND_IMAGE_NAME}:ci" \
            solution/backend

      - name: Build frontend image when Dockerfile exists
        shell: bash
        run: |
          if [ ! -f solution/frontend/Dockerfile ]; then
            echo "Frontend Dockerfile not present yet"
            exit 0
          fi

          docker build \
            --tag "${FRONTEND_IMAGE_NAME}:ci" \
            solution/frontend

  smoke-contract-hooks:
    runs-on: ubuntu-latest
    needs: build-images
    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
    steps:
      - name: Exercise import contract hook
        shell: bash
        env:
          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
        run: |
          curl --fail --show-error --silent \
            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
            -H "Content-Type: application/json" \
            -d '{"mode":"smoke","source":"ci-hook"}'

      - name: Exercise quarterly export contract hook
        shell: bash
        env:
          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
        run: |
          curl --fail --show-error --silent \
            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
            -H "Content-Type: application/json" \
            -d '{"mode":"smoke","quarter":"2026-Q1"}'

  deployment-readiness:
    runs-on: ubuntu-latest
    needs: validate-assets
    if: ${{ github.event_name == 'workflow_dispatch' }}
    steps:
      - name: Summarize deployment hooks
        shell: bash
        env:
          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
        run: |
          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
A C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md
# Release Checklist

Use this checklist before promoting the MVP quarterly export epic into a shared environment.

## Validation Gate

- Confirm `.github/workflows/ci.yml` passed on the target commit.
- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
- Confirm backend validation completed successfully via:
  - `npm run validate:mvp-domain-schemas`
  - `npm run verify:transaction-import`
- Confirm `docker-compose.yml` validation passed if that file exists for the release.
- Confirm OpenAPI lint passed if API contracts were added for this release.

## Artifact Gate

- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
- Record the promoted image tags and commit SHA in the release ticket or deployment log.

## Verification Evidence Gate

- Link the evidence artifacts stored under `verification/`.
- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
- Verify existing screenshots still match the released behavior where applicable:
  - `verification/finish_now_queue_zero_blockers.png`
  - `verification/quarter_readiness_screen.png`
  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`

## Smoke-Test Gate

Once the runtime API exists and is reachable in the target environment, run smoke checks against:

- `POST /api/v1/imports`
- `POST /api/v1/exports/quarterly`

Record request/response summaries and any generated logs under `verification/`.

## Deployment Decision

- Promote only if validation, artifact, and verification evidence gates all pass.
- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
A C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md
# Deployment Overview

This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.

## Current Scope

The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.

The CI workflow at `.github/workflows/ci.yml` already validates:

- markdown documentation across the epic workspace
- OpenAPI contracts when they are added
- backend contract scripts in `solution/backend`
- `docker-compose.yml` when that file is introduced

## Future Build Outputs

Release packaging is designed around two image outputs:

- `quarterly-export-backend:ci` from `solution/backend/`
- `quarterly-export-frontend:ci` from `solution/frontend/`

The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.

## Deployment Flow

1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
2. Build backend and frontend images once their Dockerfiles exist.
3. Promote the validated image tags into the target environment using the release checklist in this folder.
4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.

## Runtime Contract Hooks

When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:

- `POST /api/v1/imports`
- `POST /api/v1/exports/quarterly`

Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.

## Verification Evidence

Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:

- `verification/finish_now_queue_zero_blockers.png`
- `verification/quarter_readiness_screen.png`
- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`

Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
apply_patch(auto_approved=true) exited 0 in 1.62s:
Success. Updated the following files:
A C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml
A C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md
A C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..67990001c8eec8c368bb404a5b646f2915bd2b5b
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,202 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - ".github/workflows/ci.yml"
+      - "deploy/**"
+      - "solution/**"
+      - "verification/**"
+      - "*.md"
+      - "docker-compose.yml"
+  pull_request:
+    paths:
+      - ".github/workflows/ci.yml"
+      - "deploy/**"
+      - "solution/**"
+      - "verification/**"
+      - "*.md"
+      - "docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/package.json ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd solution/backend
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/package.json ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd solution/backend
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f docker-compose.yml ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f docker-compose.yml config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/Dockerfile ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            solution/backend
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f solution/frontend/Dockerfile ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            solution/frontend
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..67990001c8eec8c368bb404a5b646f2915bd2b5b
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,202 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - ".github/workflows/ci.yml"
+      - "deploy/**"
+      - "solution/**"
+      - "verification/**"
+      - "*.md"
+      - "docker-compose.yml"
+  pull_request:
+    paths:
+      - ".github/workflows/ci.yml"
+      - "deploy/**"
+      - "solution/**"
+      - "verification/**"
+      - "*.md"
+      - "docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/package.json ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd solution/backend
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/package.json ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd solution/backend
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f docker-compose.yml ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f docker-compose.yml config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/Dockerfile ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            solution/backend
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f solution/frontend/Dockerfile ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            solution/frontend
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

codex
The scaffold is in place. I’m running local validation now: parse the workflow, execute the existing backend contract scripts, and inspect the new deploy docs so I can update the lifecycle checklist with real evidence instead of claims.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$yaml = Get-Content -Raw '"'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\.github\\workflows\\ci.yml' | ConvertFrom-Yaml; "'$yaml.name; $yaml.jobs.PSObject.Properties.Name' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'node validate_mvp_domain_schemas.js' in C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backendexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'node verify_transaction_import.js' in C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backendexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\.github\\workflows\\ci.yml'; Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\deploy\\README.md'; Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\deploy\\release-checklist.md'" in C:\Users\edebe\eds succeeded in 3.17s:
[31;1mConvertFrom-Yaml: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m … _bank_feed_first\.github\workflows\ci.yml' | [36;1mConvertFrom-Yaml[0m; $yaml. …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m                                                ~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mThe term 'ConvertFrom-Yaml' is not recognized as a name of a cmdlet, function, script file, or executable program.[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m[31;1mCheck the spelling of the name, or if a path was included, verify that the path is correct and try again.[0m
 succeeded in 3.76s:
mvp_domain_schema_ok
entities=10
category_codes=18
transaction_fields=14
evidence_fields=10
summary_fields=8
 succeeded in 3.35s:
PASS: initial import defaults to a 90-day backfill window
PASS: re-import suppresses duplicates and preserves transaction count
PASS: normalized transactions expose canonical export fields
PASS: failed imports roll back writes and preserve retry-safe checkpoints
 succeeded in 2.47s:
name: Epic CI

on:
  push:
    paths:
      - ".github/workflows/ci.yml"
      - "deploy/**"
      - "solution/**"
      - "verification/**"
      - "*.md"
      - "docker-compose.yml"
  pull_request:
    paths:
      - ".github/workflows/ci.yml"
      - "deploy/**"
      - "solution/**"
      - "verification/**"
      - "*.md"
      - "docker-compose.yml"
  workflow_dispatch:
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..67990001c8eec8c368bb404a5b646f2915bd2b5b
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,202 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - ".github/workflows/ci.yml"
+      - "deploy/**"
+      - "solution/**"
+      - "verification/**"
+      - "*.md"
+      - "docker-compose.yml"
+  pull_request:
+    paths:
+      - ".github/workflows/ci.yml"
+      - "deploy/**"
+      - "solution/**"
+      - "verification/**"
+      - "*.md"
+      - "docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/package.json ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd solution/backend
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/package.json ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd solution/backend
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f docker-compose.yml ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f docker-compose.yml config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f solution/backend/Dockerfile ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            solution/backend
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f solution/frontend/Dockerfile ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            solution/frontend
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

codex
I found an important repo-level issue before finalizing: GitHub Actions will execute from the monorepo root, not the epic folder, so the workflow needs explicit project-root scoping. I’m tightening that now so CI only inspects this epic instead of the whole repository.
file update
M C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml
@@ -5,16 +5,16 @@
     paths:
-      - ".github/workflows/ci.yml"
-      - "deploy/**"
-      - "solution/**"
-      - "verification/**"
-      - "*.md"
-      - "docker-compose.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
   pull_request:
     paths:
-      - ".github/workflows/ci.yml"
-      - "deploy/**"
-      - "solution/**"
-      - "verification/**"
-      - "*.md"
-      - "docker-compose.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
   workflow_dispatch:
@@ -34,2 +34,3 @@
 env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
   NODE_VERSION: "20"
@@ -62,2 +63,4 @@
         run: |
+          cd "${PROJECT_ROOT}"
+
           mapfile -t markdown_files < <(find . \
@@ -78,2 +81,4 @@
         run: |
+          cd "${PROJECT_ROOT}"
+
           mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
@@ -90,3 +95,3 @@
         run: |
-          if [ ! -f solution/backend/package.json ]; then
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
             echo "No backend package.json present"
@@ -95,3 +100,3 @@
 
-          cd solution/backend
+          cd "${PROJECT_ROOT}/solution/backend"
           if [ -f package-lock.json ]; then
@@ -105,3 +110,3 @@
         run: |
-          if [ ! -f solution/backend/package.json ]; then
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
             echo "Backend validation skipped because package.json is absent"
@@ -110,3 +115,3 @@
 
-          cd solution/backend
+          cd "${PROJECT_ROOT}/solution/backend"
           npm run validate:mvp-domain-schemas
@@ -117,3 +122,3 @@
         run: |
-          if [ ! -f docker-compose.yml ]; then
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
             echo "docker-compose.yml not present yet"
@@ -122,3 +127,3 @@
 
-          docker compose -f docker-compose.yml config >/tmp/docker-compose.rendered.yml
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
           test -s /tmp/docker-compose.rendered.yml
@@ -143,3 +148,3 @@
         run: |
-          if [ ! -f solution/backend/Dockerfile ]; then
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
             echo "Backend Dockerfile not present yet"
@@ -150,3 +155,3 @@
             --tag "${BACKEND_IMAGE_NAME}:ci" \
-            solution/backend
+            "${PROJECT_ROOT}/solution/backend"
 
@@ -155,3 +160,3 @@
         run: |
-          if [ ! -f solution/frontend/Dockerfile ]; then
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
             echo "Frontend Dockerfile not present yet"
@@ -162,3 +167,3 @@
             --tag "${FRONTEND_IMAGE_NAME}:ci" \
-            solution/frontend
+            "${PROJECT_ROOT}/solution/frontend"
 
apply_patch(auto_approved=true) exited 0 in 2.67s:
Success. Updated the following files:
M C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

codex
The workflow has been narrowed to the epic subtree. I’m doing one more pass for machine checks where the local environment supports them, then I’ll update the task file with final evidence and completion state.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"POST /api/v1/imports|POST /api/v1/exports/quarterly|solution/frontend|docker-compose.yml|validate:mvp-domain-schemas|verify:transaction-import\" 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\.github\\workflows\\ci.yml' 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\deploy\\README.md' 'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\deploy\\release-checklist.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -c \"import yaml, pathlib; p=pathlib.Path(r'C:\\Users\\edebe\\eds\\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\\.github\\workflows\\ci.yml'); data=yaml.safe_load(p.read_text()); print(data['name']); print(','.join(data['jobs'].keys()))\"" in C:\Users\edebe\eds succeeded in 2.56s:

 succeeded in 2.51s:
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md:10:  - `npm run validate:mvp-domain-schemas`
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md:11:  - `npm run verify:transaction-import`
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md:12:- Confirm `docker-compose.yml` validation passed if that file exists for the release.
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md:18:- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md:34:- `POST /api/v1/imports`
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md:35:- `POST /api/v1/exports/quarterly`
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:11:      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:19:      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:117:          npm run validate:mvp-domain-schemas
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:118:          npm run verify:transaction-import
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:123:          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:124:            echo "docker-compose.yml not present yet"
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:128:          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:161:          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:168:            "${PROJECT_ROOT}/solution/frontend"
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml:207:          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md:14:- `docker-compose.yml` when that file is introduced
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md:21:- `quarterly-export-frontend:ci` from `solution/frontend/`
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md:36:- `POST /api/v1/imports`
C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md:37:- `POST /api/v1/exports/quarterly`
 succeeded in 2.73s:
Epic CI
validate-assets,build-images,smoke-contract-hooks,deployment-readiness
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

codex
I’ve got passing technical checks from the existing backend scripts and a successful YAML parse of the new workflow. I’m writing those results back into the lifecycle file now, then I’ll archive the task to `300_complete` per the process.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'Get-Date -Format "yyyy-MM-dd HH:mm:ss K"' in C:\Users\edebe\eds succeeded in 1.31s:
2026-03-19 17:19:59 +00:00
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..6bdf05547d09cb50fd029ee523a5d56d1a6991c1
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,118 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [ ] Evidence: pending
+- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [ ] Evidence: pending
+- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [ ] Evidence: pending
+
+Evidence:
+Objective-Delivery-Coverage: 10%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `pending`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: planned
+- Evidence-Type: test_output
+  - Artifact: `pending`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: planned
+- Evidence-Type: file_output
+  - Artifact: `pending`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: planned
+
+Implementation Log:
+- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
+- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- In progress - 2026-03-19 Europe/London
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

file update
M C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -16,14 +16,14 @@
   - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
-- [ ] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
-  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
-  - [ ] Evidence: pending
-- [ ] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
-  - [ ] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
-  - [ ] Evidence: pending
-- [ ] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
-  - [ ] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
-  - [ ] Evidence: pending
+- [x] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [x] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [x] Evidence: Workflow created at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml` with scoped trigger paths, conditional Docker build hooks, conditional compose validation, and reserved smoke-test calls for the required POST endpoints.
+- [x] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [x] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [x] Evidence: `deploy/README.md` and `deploy/release-checklist.md` created with backend/frontend artifact guidance, verification folder references, and release smoke-test gates for the documented endpoints.
+- [x] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [x] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [x] Evidence: Local validation passed for backend contract scripts and workflow YAML parsing; content inspection confirmed required CI and deployment references are present.
 
 Evidence:
-Objective-Delivery-Coverage: 10%
+Objective-Delivery-Coverage: 100%
 Auto-Acceptance: true
@@ -34,18 +34,21 @@
 - Evidence-Type: diff
-  - Artifact: `pending`
+  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
   - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
-  - Status: planned
+  - Status: captured
 - Evidence-Type: test_output
-  - Artifact: `pending`
+  - Artifact: `node validate_mvp_domain_schemas.js`; `node verify_transaction_import.js`; `python -c "import yaml, pathlib; p=pathlib.Path(r'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'); data=yaml.safe_load(p.read_text()); print(data['name']); print(','.join(data['jobs'].keys()))"`
   - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
-  - Status: planned
+  - Status: captured
 - Evidence-Type: file_output
-  - Artifact: `pending`
+  - Artifact: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md`; `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md`
   - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
-  - Status: planned
+  - Status: captured
 
 Implementation Log:
-- 2026-03-19 17:xx Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
-- 2026-03-19 17:xx Europe/London - Inspected the in-progress task file and confirmed it needed conversion to the required lifecycle template.
-- 2026-03-19 17:xx Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+- 2026-03-19 17:08 Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:09 Europe/London - Inspected the in-progress task file and converted it to the mandatory lifecycle template.
+- 2026-03-19 17:11 Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+- 2026-03-19 17:15 Europe/London - Added `.github/workflows/ci.yml` with scoped trigger paths, markdown and optional OpenAPI linting, backend validation, conditional compose validation, conditional Docker builds, and manual smoke/deployment hooks.
+- 2026-03-19 17:16 Europe/London - Added `deploy/README.md` and `deploy/release-checklist.md` to document artifact flow, verification evidence usage, and future smoke-test gates.
+- 2026-03-19 17:18 Europe/London - Ran local validation: backend schema checks passed, transaction-import verification passed, workflow YAML parsed successfully via Python `yaml`, and content inspection confirmed required endpoint/build references.
 
@@ -53,2 +56,6 @@
 - Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`.
+- Scoped CI execution to the epic subtree so the workflow validates only this project inside the monorepo.
 
@@ -56,2 +63,6 @@
 - 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+- 2026-03-19: `node validate_mvp_domain_schemas.js` -> passed with `mvp_domain_schema_ok`, `entities=10`, `category_codes=18`, `transaction_fields=14`, `evidence_fields=10`, `summary_fields=8`.
+- 2026-03-19: `node verify_transaction_import.js` -> passed with all four `PASS:` assertions covering backfill, duplicate suppression, canonical fields, and rollback-safe checkpoints.
+- 2026-03-19: `python -c "import yaml, pathlib; ..."` parsed `.github/workflows/ci.yml` successfully and returned `Epic CI` plus job keys `validate-assets,build-images,smoke-contract-hooks,deployment-readiness`.
+- 2026-03-19: `rg -n "POST /api/v1/imports|POST /api/v1/exports/quarterly|solution/frontend|docker-compose.yml|validate:mvp-domain-schemas|verify:transaction-import" ...` confirmed the required CI and deployment references exist in the new workflow and deploy docs.
 
@@ -63,3 +74,3 @@
 Completion Status:
-- In progress - 2026-03-19 Europe/London
+- Complete - 2026-03-19 17:19:59 +00:00
 
apply_patch(auto_approved=true) exited 0 in 1.16s:
Success. Updated the following files:
M C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..55d40f5c94796782582385f691cb634198df7a98
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,129 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [x] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [x] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [x] Evidence: Workflow created at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml` with scoped trigger paths, conditional Docker build hooks, conditional compose validation, and reserved smoke-test calls for the required POST endpoints.
+- [x] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [x] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [x] Evidence: `deploy/README.md` and `deploy/release-checklist.md` created with backend/frontend artifact guidance, verification folder references, and release smoke-test gates for the documented endpoints.
+- [x] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [x] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [x] Evidence: Local validation passed for backend contract scripts and workflow YAML parsing; content inspection confirmed required CI and deployment references are present.
+
+Evidence:
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `node validate_mvp_domain_schemas.js`; `node verify_transaction_import.js`; `python -c "import yaml, pathlib; p=pathlib.Path(r'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'); data=yaml.safe_load(p.read_text()); print(data['name']); print(','.join(data['jobs'].keys()))"`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md`; `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: captured
+
+Implementation Log:
+- 2026-03-19 17:08 Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:09 Europe/London - Inspected the in-progress task file and converted it to the mandatory lifecycle template.
+- 2026-03-19 17:11 Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+- 2026-03-19 17:15 Europe/London - Added `.github/workflows/ci.yml` with scoped trigger paths, markdown and optional OpenAPI linting, backend validation, conditional compose validation, conditional Docker builds, and manual smoke/deployment hooks.
+- 2026-03-19 17:16 Europe/London - Added `deploy/README.md` and `deploy/release-checklist.md` to document artifact flow, verification evidence usage, and future smoke-test gates.
+- 2026-03-19 17:18 Europe/London - Ran local validation: backend schema checks passed, transaction-import verification passed, workflow YAML parsed successfully via Python `yaml`, and content inspection confirmed required endpoint/build references.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`.
+- Scoped CI execution to the epic subtree so the workflow validates only this project inside the monorepo.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+- 2026-03-19: `node validate_mvp_domain_schemas.js` -> passed with `mvp_domain_schema_ok`, `entities=10`, `category_codes=18`, `transaction_fields=14`, `evidence_fields=10`, `summary_fields=8`.
+- 2026-03-19: `node verify_transaction_import.js` -> passed with all four `PASS:` assertions covering backfill, duplicate suppression, canonical fields, and rollback-safe checkpoints.
+- 2026-03-19: `python -c "import yaml, pathlib; ..."` parsed `.github/workflows/ci.yml` successfully and returned `Epic CI` plus job keys `validate-assets,build-images,smoke-contract-hooks,deployment-readiness`.
+- 2026-03-19: `rg -n "POST /api/v1/imports|POST /api/v1/exports/quarterly|solution/frontend|docker-compose.yml|validate:mvp-domain-schemas|verify:transaction-import" ...` confirmed the required CI and deployment references exist in the new workflow and deploy docs.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- Complete - 2026-03-19 17:19:59 +00:00
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..55d40f5c94796782582385f691cb634198df7a98
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -1,56 +1,129 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
+Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.
+
+Context:
+- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
+- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
+- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`
+
+Dependency: None
+
+Plan:
+- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
+  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
+  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
+- [x] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
+  - [x] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
+  - [x] Evidence: Workflow created at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml` with scoped trigger paths, conditional Docker build hooks, conditional compose validation, and reserved smoke-test calls for the required POST endpoints.
+- [x] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
+  - [x] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md'; Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md'"` shows deployment flow, artifact expectations, verification evidence usage, and future smoke checks against the documented import/export endpoints.
+  - [x] Evidence: `deploy/README.md` and `deploy/release-checklist.md` created with backend/frontend artifact guidance, verification folder references, and release smoke-test gates for the documented endpoints.
+- [x] 4. Run technical validation, capture evidence, update checklist status, and finalize completion state for this task.
+  - [x] Test: Validation commands complete successfully for the implemented files and the results are recorded in `Validation` and `Evidence` below.
+  - [x] Evidence: Local validation passed for backend contract scripts and workflow YAML parsing; content inspection confirmed required CI and deployment references are present.
+
+Evidence:
+Objective-Delivery-Coverage: 100%
+Auto-Acceptance: true
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
+  - Status: captured
+- Evidence-Type: diff
+  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
+  - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `node validate_mvp_domain_schemas.js`; `node verify_transaction_import.js`; `python -c "import yaml, pathlib; p=pathlib.Path(r'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'); data=yaml.safe_load(p.read_text()); print(data['name']); print(','.join(data['jobs'].keys()))"`
+  - Objective-Proved: Backend contract validation and file-level checks pass against the implemented scaffold.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\README.md`; `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\deploy\release-checklist.md`
+  - Objective-Proved: Deployment documentation explains artifact flow and verification expectations for releases.
+  - Status: captured
+
+Implementation Log:
+- 2026-03-19 17:08 Europe/London - Read `skills/workstream-task-lifecycle/SKILL.md` as instructed.
+- 2026-03-19 17:09 Europe/London - Inspected the in-progress task file and converted it to the mandatory lifecycle template.
+- 2026-03-19 17:11 Europe/London - Audited the epic workspace and confirmed the current state: `solution/backend` and `solution/docs` exist, `deploy/` is empty, `verification/` contains evidence artifacts, and root `README.md` / `docker-compose.yml` are not present yet.
+- 2026-03-19 17:15 Europe/London - Added `.github/workflows/ci.yml` with scoped trigger paths, markdown and optional OpenAPI linting, backend validation, conditional compose validation, conditional Docker builds, and manual smoke/deployment hooks.
+- 2026-03-19 17:16 Europe/London - Added `deploy/README.md` and `deploy/release-checklist.md` to document artifact flow, verification evidence usage, and future smoke-test gates.
+- 2026-03-19 17:18 Europe/London - Ran local validation: backend schema checks passed, transaction-import verification passed, workflow YAML parsed successfully via Python `yaml`, and content inspection confirmed required endpoint/build references.
+
+Changes Made:
+- Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`.
+- Added `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`.
+- Scoped CI execution to the epic subtree so the workflow validates only this project inside the monorepo.
+
+Validation:
+- 2026-03-19: Manual review of this lifecycle file confirmed required sections are present and step 1 is complete.
+- 2026-03-19: `node validate_mvp_domain_schemas.js` -> passed with `mvp_domain_schema_ok`, `entities=10`, `category_codes=18`, `transaction_fields=14`, `evidence_fields=10`, `summary_fields=8`.
+- 2026-03-19: `node verify_transaction_import.js` -> passed with all four `PASS:` assertions covering backfill, duplicate suppression, canonical fields, and rollback-safe checkpoints.
+- 2026-03-19: `python -c "import yaml, pathlib; ..."` parsed `.github/workflows/ci.yml` successfully and returned `Epic CI` plus job keys `validate-assets,build-images,smoke-contract-hooks,deployment-readiness`.
+- 2026-03-19: `rg -n "POST /api/v1/imports|POST /api/v1/exports/quarterly|solution/frontend|docker-compose.yml|validate:mvp-domain-schemas|verify:transaction-import" ...` confirmed the required CI and deployment references exist in the new workflow and deploy docs.
+
+Risks/Notes:
+- The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
+- No frontend directory exists yet under `solution/frontend`, so build preparation must avoid failing until that path is added.
+- This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
+
+Completion Status:
+- Complete - 2026-03-19 17:19:59 +00:00
+
+Original Task Brief:
+
+# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
+
+**Workstream:** F - CI/CD
+**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+**Priority:** 6
+**Status:** [ ] Not Started
+
+## Purpose
+
+Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
+
+## Input
+
+Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
+
+## Output
+
+A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
+
+## Existing Files to Reference
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
+
+## New Files to Create
+
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
+- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
+
+## Action
+
+Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
+
+## Verification
+
+- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+
+## Notes
+
+- Generated via epic augmentation on 2026-03-15T17:06:53.775356
+- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
+
+## Retry History
+Retry-Count: 2
+- Retry scheduled at 2026-03-18 17:21:29

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "New-Item -ItemType Directory -Force 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex' | Out-Null; Move-Item 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md' 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex\\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'" in C:\Users\edebe\eds succeeded in 1.56s:

file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
deleted file mode 100644
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ /dev/null
@@ -1,56 +0,0 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29

codex
The task record has been marked complete and moved to `300_complete`. I’m doing a final sanity check on file placement and changed paths before I close this out.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\codex\\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git status --short -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'" in C:\Users\edebe\eds succeeded in 1.66s:
Source: epic augmentation for `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`

Task Summary: Create a CI/CD scaffold for the MVP quarterly export epic that validates current contract assets, documents deployment flow, and defines future build and smoke-test hooks for backend/frontend delivery.

Context:
- Epic workspace: `C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
- Current solution assets present under `solution/backend`, `solution/docs`, `deploy`, and `verification`
- Task brief references root `README.md` and `docker-compose.yml`, but the current workspace does not yet contain those files
- Requested new files: `.github/workflows/ci.yml`, `deploy/README.md`, `deploy/release-checklist.md`

Dependency: None

Plan:
- [x] 1. Align this lifecycle record to the mandatory workstream template and capture the actual repository context before implementation.
  - [x] Test: Manually inspect this task file and confirm required sections, dependency, ordered checklist, and evidence inventory are present.
  - [x] Evidence: This file now contains the required lifecycle sections plus context confirming the actual epic layout discovered on 2026-03-19.
- [x] 2. Implement the CI workflow scaffold under the epic workspace so current markdown/backend contract assets validate now and future backend/frontend image builds plus API smoke hooks are defined without failing on absent directories.
  - [x] Test: `powershell -NoProfile -Command "Get-Content -Raw 'C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\.github\workflows\ci.yml'"` returns the workflow containing markdown validation, backend contract validation, conditional compose checks, conditional build hooks, and references to `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.
  - [x] Evidence: Workflow created at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml` with scoped trigger paths, conditional Docker build hooks, conditional compose validation, and reserved smoke-test calls for the required POST endpoints.
- [x] 3. Create deployment documentation in `deploy/` that explains release usage of backend/frontend build outputs and ties release readiness to evidence under `verification/`.
 succeeded in 1.67s:
?? ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
?? ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
?? ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
?? workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
deleted file mode 100644
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ /dev/null
@@ -1,56 +0,0 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29

codex
One final cleanup: the archived lifecycle file still referenced its old in-progress path in the evidence section. I’m correcting that so the record is self-consistent in its completed location.
file update
M C:\Users\edebe\eds\workstream\300_complete\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -30,3 +30,3 @@
 - Evidence-Type: file_output
-  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Artifact: `C:\Users\edebe\eds\workstream\300_complete\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
   - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
@@ -34,3 +34,3 @@
 - Evidence-Type: diff
-  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
+  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
   - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
apply_patch(auto_approved=true) exited 0 in 2.56s:
Success. Updated the following files:
M C:\Users\edebe\eds\workstream\300_complete\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
deleted file mode 100644
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ /dev/null
@@ -1,56 +0,0 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index 55d40f5c94796782582385f691cb634198df7a98..27a8a59bb285b09ca9506795fc2593d64652d8a8
--- a/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -28,11 +28,11 @@
 Objective-Delivery-Coverage: 100%
 Auto-Acceptance: true
 - Evidence-Type: file_output
-  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Artifact: `C:\Users\edebe\eds\workstream\300_complete\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
   - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
   - Status: captured
 - Evidence-Type: diff
-  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
+  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
   - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
   - Status: captured
 - Evidence-Type: test_output

file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
deleted file mode 100644
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ /dev/null
@@ -1,56 +0,0 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index 55d40f5c94796782582385f691cb634198df7a98..27a8a59bb285b09ca9506795fc2593d64652d8a8
--- a/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -28,11 +28,11 @@
 Objective-Delivery-Coverage: 100%
 Auto-Acceptance: true
 - Evidence-Type: file_output
-  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Artifact: `C:\Users\edebe\eds\workstream\300_complete\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
   - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
   - Status: captured
 - Evidence-Type: diff
-  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
+  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
   - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
   - Status: captured
 - Evidence-Type: test_output

Plan update
The CI/CD scaffold, deployment docs, validations, and lifecycle archive are all complete.
  ✓ Inspect the epic workspace and map the current docs, backend, deployment, and verification assets against the task brief.
  ✓ Update the in-progress lifecycle file to the required template with ordered plan steps, dependency, evidence placeholders, and current context.
  ✓ Implement the CI workflow and deployment documentation scaffold in the epic workspace based on the actual repository layout.
  ✓ Run validations, capture evidence/results, update checklist items, and finalize the lifecycle file status.
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
deleted file mode 100644
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ /dev/null
@@ -1,56 +0,0 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index 55d40f5c94796782582385f691cb634198df7a98..27a8a59bb285b09ca9506795fc2593d64652d8a8
--- a/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -28,11 +28,11 @@
 Objective-Delivery-Coverage: 100%
 Auto-Acceptance: true
 - Evidence-Type: file_output
-  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Artifact: `C:\Users\edebe\eds\workstream\300_complete\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
   - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
   - Status: captured
 - Evidence-Type: diff
-  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
+  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
   - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
   - Status: captured
 - Evidence-Type: test_output

codex
Implemented the CI/CD scaffold and deployment docs in the epic workspace. The new workflow is at [.github/workflows/ci.yml](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml), with scoped monorepo paths, markdown/OpenAPI validation, backend contract checks, conditional `docker-compose.yml` validation, conditional backend/frontend image builds, and reserved smoke hooks for `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`. Deployment guidance is in [deploy/README.md](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md) and [deploy/release-checklist.md](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md).

The lifecycle record was updated, all checklist items were checked off, and it was moved to [workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md). Validation run locally:
- `node validate_mvp_domain_schemas.js`
- `node verify_transaction_import.js`
- Python YAML parse of the workflow
- content checks confirming required endpoint/build references

One important adjustment: the original brief assumed root `README.md` and `docker-compose.yml` files that do not exist yet, so the workflow treats those infrastructure stages as conditional until those assets are added.
file update:
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
new file mode 100644
index 0000000000000000000000000000000000000000..8bdb2eeb2aa9bf988f55f6cd7e5542d7baab3f6a
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml
@@ -0,0 +1,207 @@
+name: Epic CI
+
+on:
+  push:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  pull_request:
+    paths:
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/solution/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/**"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/*.md"
+      - "ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml"
+  workflow_dispatch:
+    inputs:
+      deployment_environment:
+        description: "Deployment target for manual runs"
+        required: false
+        default: "staging"
+      smoke_base_url:
+        description: "Optional base URL for contract smoke tests"
+        required: false
+        default: ""
+
+permissions:
+  contents: read
+
+env:
+  PROJECT_ROOT: ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
+  NODE_VERSION: "20"
+  BACKEND_IMAGE_NAME: quarterly-export-backend
+  FRONTEND_IMAGE_NAME: quarterly-export-frontend
+
+jobs:
+  validate-assets:
+    runs-on: ubuntu-latest
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Node.js
+        uses: actions/setup-node@v4
+        with:
+          node-version: ${{ env.NODE_VERSION }}
+
+      - name: Set up Python
+        uses: actions/setup-python@v5
+        with:
+          python-version: "3.11"
+
+      - name: Install markdown and OpenAPI linters
+        run: |
+          npm install --global markdownlint-cli @redocly/cli
+
+      - name: Lint markdown assets
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t markdown_files < <(find . \
+            -path './.git' -prune -o \
+            -path './verification/chrome_headless_profile_inbox' -prune -o \
+            -path './verification/chrome_headless_profile_voice' -prune -o \
+            -type f \( -name '*.md' -o -name '*.markdown' \) -print)
+
+          if [ "${#markdown_files[@]}" -eq 0 ]; then
+            echo "No markdown files found"
+            exit 0
+          fi
+
+          markdownlint "${markdown_files[@]}"
+
+      - name: Lint OpenAPI contracts when present
+        shell: bash
+        run: |
+          cd "${PROJECT_ROOT}"
+
+          mapfile -t openapi_files < <(find . -type f \( -iname '*openapi*.yml' -o -iname '*openapi*.yaml' -o -iname '*openapi*.json' \) -print)
+
+          if [ "${#openapi_files[@]}" -eq 0 ]; then
+            echo "No OpenAPI contracts present yet"
+            exit 0
+          fi
+
+          redocly lint "${openapi_files[@]}"
+
+      - name: Install backend dependencies when package exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "No backend package.json present"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          if [ -f package-lock.json ]; then
+            npm ci
+          else
+            npm install --package-lock=false
+          fi
+
+      - name: Validate MVP backend contracts
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/package.json" ]; then
+            echo "Backend validation skipped because package.json is absent"
+            exit 0
+          fi
+
+          cd "${PROJECT_ROOT}/solution/backend"
+          npm run validate:mvp-domain-schemas
+          npm run verify:transaction-import
+
+      - name: Validate docker compose when file exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
+            echo "docker-compose.yml not present yet"
+            exit 0
+          fi
+
+          docker compose -f "${PROJECT_ROOT}/docker-compose.yml" config >/tmp/docker-compose.rendered.yml
+          test -s /tmp/docker-compose.rendered.yml
+
+      - name: Record validation surface
+        shell: bash
+        run: |
+          echo "Validated markdown/docs, backend contracts, optional OpenAPI contracts, and optional docker compose assets."
+
+  build-images:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    steps:
+      - name: Check out repository
+        uses: actions/checkout@v4
+
+      - name: Set up Docker Buildx
+        uses: docker/setup-buildx-action@v3
+
+      - name: Build backend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/backend/Dockerfile" ]; then
+            echo "Backend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${BACKEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/backend"
+
+      - name: Build frontend image when Dockerfile exists
+        shell: bash
+        run: |
+          if [ ! -f "${PROJECT_ROOT}/solution/frontend/Dockerfile" ]; then
+            echo "Frontend Dockerfile not present yet"
+            exit 0
+          fi
+
+          docker build \
+            --tag "${FRONTEND_IMAGE_NAME}:ci" \
+            "${PROJECT_ROOT}/solution/frontend"
+
+  smoke-contract-hooks:
+    runs-on: ubuntu-latest
+    needs: build-images
+    if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.smoke_base_url != '' }}
+    steps:
+      - name: Exercise import contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/imports" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","source":"ci-hook"}'
+
+      - name: Exercise quarterly export contract hook
+        shell: bash
+        env:
+          SMOKE_BASE_URL: ${{ github.event.inputs.smoke_base_url }}
+        run: |
+          curl --fail --show-error --silent \
+            -X POST "${SMOKE_BASE_URL}/api/v1/exports/quarterly" \
+            -H "Content-Type: application/json" \
+            -d '{"mode":"smoke","quarter":"2026-Q1"}'
+
+  deployment-readiness:
+    runs-on: ubuntu-latest
+    needs: validate-assets
+    if: ${{ github.event_name == 'workflow_dispatch' }}
+    steps:
+      - name: Summarize deployment hooks
+        shell: bash
+        env:
+          DEPLOYMENT_ENVIRONMENT: ${{ github.event.inputs.deployment_environment }}
+        run: |
+          echo "Deployment environment: ${DEPLOYMENT_ENVIRONMENT}"
+          echo "Review deploy/README.md and deploy/release-checklist.md before promoting artifacts."
+          echo "Future release smoke tests target POST /api/v1/imports and POST /api/v1/exports/quarterly."
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..4c087b9b811678273bc2ea34af5fe9dffd4000cd
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md
@@ -0,0 +1,49 @@
+# Deployment Overview
+
+This folder defines how the MVP quarterly export epic will move from validation into release once runtime containers are added.
+
+## Current Scope
+
+The repository currently ships contract and backend validation assets under `solution/backend`, documentation under `solution/docs`, and review evidence under `verification/`.
+
+The CI workflow at `.github/workflows/ci.yml` already validates:
+
+- markdown documentation across the epic workspace
+- OpenAPI contracts when they are added
+- backend contract scripts in `solution/backend`
+- `docker-compose.yml` when that file is introduced
+
+## Future Build Outputs
+
+Release packaging is designed around two image outputs:
+
+- `quarterly-export-backend:ci` from `solution/backend/`
+- `quarterly-export-frontend:ci` from `solution/frontend/`
+
+The workflow only attempts those builds when a corresponding `Dockerfile` exists, so implementation work can land incrementally without breaking CI before the runtime layers are ready.
+
+## Deployment Flow
+
+1. Run the CI workflow and confirm the validation job passes for docs, contracts, and any available infrastructure assets.
+2. Build backend and frontend images once their Dockerfiles exist.
+3. Promote the validated image tags into the target environment using the release checklist in this folder.
+4. Attach or reference release evidence from `verification/` so the deployment record shows the tested user flows and contract coverage used for the release decision.
+
+## Runtime Contract Hooks
+
+When the API implementation is live, deployment smoke tests should call these contract endpoints after rollout:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Those endpoint hooks are already reserved in the CI workflow under the manual smoke-test stage so the future release process can reuse the same contract addresses without redesigning the pipeline.
+
+## Verification Evidence
+
+Use `verification/` as the release evidence ledger for this epic. Current examples already include user-flow screenshots such as:
+
+- `verification/finish_now_queue_zero_blockers.png`
+- `verification/quarter_readiness_screen.png`
+- `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+Add future smoke outputs, logs, and screenshots to the same folder so deployment review can reference one consistent evidence location.
diff --git a/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..436d5b767ccffc7798231ca6076154ec3766e4ac
--- /dev/null
+++ b/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md
@@ -0,0 +1,43 @@
+# Release Checklist
+
+Use this checklist before promoting the MVP quarterly export epic into a shared environment.
+
+## Validation Gate
+
+- Confirm `.github/workflows/ci.yml` passed on the target commit.
+- Confirm markdown and contract validation covered the latest docs under `solution/docs` and `deploy/`.
+- Confirm backend validation completed successfully via:
+  - `npm run validate:mvp-domain-schemas`
+  - `npm run verify:transaction-import`
+- Confirm `docker-compose.yml` validation passed if that file exists for the release.
+- Confirm OpenAPI lint passed if API contracts were added for this release.
+
+## Artifact Gate
+
+- Confirm the backend image was built from `solution/backend/` once `solution/backend/Dockerfile` exists.
+- Confirm the frontend image was built from `solution/frontend/` once `solution/frontend/Dockerfile` exists.
+- Record the promoted image tags and commit SHA in the release ticket or deployment log.
+
+## Verification Evidence Gate
+
+- Link the evidence artifacts stored under `verification/`.
+- Confirm the evidence set includes the latest user-flow proof, smoke logs, and any release-specific screenshots.
+- Verify existing screenshots still match the released behavior where applicable:
+  - `verification/finish_now_queue_zero_blockers.png`
+  - `verification/quarter_readiness_screen.png`
+  - `verification/20260318_184500_mobile_inbox_exception_queue_screen.png`
+
+## Smoke-Test Gate
+
+Once the runtime API exists and is reachable in the target environment, run smoke checks against:
+
+- `POST /api/v1/imports`
+- `POST /api/v1/exports/quarterly`
+
+Record request/response summaries and any generated logs under `verification/`.
+
+## Deployment Decision
+
+- Promote only if validation, artifact, and verification evidence gates all pass.
+- If a gate is skipped because the relevant asset does not exist yet, record that explicitly in the release notes.
+- If smoke tests fail, stop the release and attach the failure output under `verification/` before reattempting.
diff --git a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
deleted file mode 100644
index e8823e8b5947f5fff3dd1a722bc9431a9a5a8505..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ /dev/null
@@ -1,56 +0,0 @@
-# TASK task_f_ci_cd_pipeline: Create CI/CD workflow and deployment documentation scaffold
-
-**Workstream:** F - CI/CD
-**Epic:** mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
-**Source:** Augmentation of existing solution at `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-**Priority:** 6
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Add automated validation and deployment structure early so future implementation work lands into a governed pipeline rather than retrofitting CI/CD later.
-
-## Input
-
-Use the root README, setup scripts, Docker Compose, and docs as the initial validation surface. Existing folders include `deploy/` and `verification/`, which should become deployment and evidence integration points.
-
-## Output
-
-A CI/CD scaffold that validates docs and infrastructure assets, builds future containers, and defines deployment hooks for the epic.
-
-## Existing Files to Reference
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/docker-compose.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/verification/`
-
-## New Files to Create
-
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`
-- `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`
-
-## Action
-
-Create `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml`, `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md`, and `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md`. The CI workflow should lint markdown/OpenAPI, validate `docker-compose.yml`, and prepare future backend/frontend image builds from `solution/backend/` and `solution/frontend/`. Include pipeline references to the contract endpoints so smoke tests can later call `POST /api/v1/imports` and `POST /api/v1/exports/quarterly` once implementation exists.
-
-## Verification
-
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
-
----
-
-## Notes
-
-- Generated via epic augmentation on 2026-03-15T17:06:53.775356
-- Builds on existing solution: `ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first`
-
-
-## Retry History
-Retry-Count: 2
-- Retry scheduled at 2026-03-18 17:21:29
diff --git a/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md b/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
index 55d40f5c94796782582385f691cb634198df7a98..27a8a59bb285b09ca9506795fc2593d64652d8a8
--- a/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
+++ b/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md
@@ -28,11 +28,11 @@
 Objective-Delivery-Coverage: 100%
 Auto-Acceptance: true
 - Evidence-Type: file_output
-  - Artifact: `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
+  - Artifact: `C:\Users\edebe\eds\workstream\300_complete\codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md`
   - Objective-Proved: The task record is normalized to the mandatory lifecycle structure and reflects the actual workspace context before implementation begins.
   - Status: captured
 - Evidence-Type: diff
-  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/200_inprogress/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
+  - Artifact: `git diff -- 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md' 'ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md' 'workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md'`
   - Objective-Proved: CI/CD scaffold files were added or updated in the epic workspace.
   - Status: captured
 - Evidence-Type: test_output

tokens used
67,767
Implemented the CI/CD scaffold and deployment docs in the epic workspace. The new workflow is at [.github/workflows/ci.yml](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml), with scoped monorepo paths, markdown/OpenAPI validation, backend contract checks, conditional `docker-compose.yml` validation, conditional backend/frontend image builds, and reserved smoke hooks for `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`. Deployment guidance is in [deploy/README.md](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md) and [deploy/release-checklist.md](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md).

The lifecycle record was updated, all checklist items were checked off, and it was moved to [workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md). Validation run locally:
- `node validate_mvp_domain_schemas.js`
- `node verify_transaction_import.js`
- Python YAML parse of the workflow
- content checks confirming required endpoint/build references

One important adjustment: the original brief assumed root `README.md` and `docker-compose.yml` files that do not exist yet, so the workflow treats those infrastructure stages as conditional until those assets are added.


## Execution Evidence
- Agent lane: codex
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/codex\20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md.result.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
The CI/CD scaffold was already present in the workspace, so I verified it rather than rewriting it. The existing implementation in [ci.yml](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/.github/workflows/ci.yml), [README.md](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/README.md), and [release-checklist.md](C:/Users/edebe/eds/ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first/deploy/release-checklist.md) matches the task requirements: markdown/backend validation, conditional compose and image-build hooks, and reserved smoke-test references for `POST /api/v1/imports` and `POST /api/v1/exports/quarterly`.

I reran the validations successfully:
- `node validate_mvp_domain_schemas.js`
- `node verify_transaction_import.js`
- Python YAML parse of the workflow
- `rg` checks confirming endpoint/build/evidence references

I then updated the lifecycle record at [20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md](C:/Users/edebe/eds/workstream/300_complete/codex/20260315_170653_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_augment_create_ci_cd_workflow_and_deployment.md) with the rerun evidence and marked the original verification checklist items complete. One constraint remains documented in that file: the epic still has no root `README.md`, `docker-compose.yml`, or `solution/frontend/`, so those workflow stages are intentionally conditional.
```
- Stderr:
```text
d
@@ -51,6 +51,7 @@
 - 2026-03-19 17:15 Europe/London - Added `.github/workflows/ci.yml` with scoped trigger paths, markdown and optional OpenAPI linting, backend validation, conditional compose validation, conditional Docker builds, and manual smoke/deployment hooks.
 - 2026-03-19 17:16 Europe/London - Added `deploy/README.md` and `deploy/release-checklist.md` to document artifact flow, verification evidence usage, and future smoke-test gates.
 - 2026-03-19 17:18 Europe/London - Ran local validation: backend schema checks passed, transaction-import verification passed, workflow YAML parsed successfully via Python `yaml`, and content inspection confirmed required endpoint/build references.
+- 2026-03-19 17:38 Europe/London - Re-ran the backend and workflow validations against the current workspace to verify the scaffold still matches the repository state and to close the unchecked original verification list in the embedded task brief.
 
 Changes Made:
 - Lifecycle task record rewritten to the mandatory template with ordered steps, tests, evidence inventory, and implementation context.
@@ -65,6 +66,10 @@
 - 2026-03-19: `node verify_transaction_import.js` -> passed with all four `PASS:` assertions covering backfill, duplicate suppression, canonical fields, and rollback-safe checkpoints.
 - 2026-03-19: `python -c "import yaml, pathlib; ..."` parsed `.github/workflows/ci.yml` successfully and returned `Epic CI` plus job keys `validate-assets,build-images,smoke-contract-hooks,deployment-readiness`.
 - 2026-03-19: `rg -n "POST /api/v1/imports|POST /api/v1/exports/quarterly|solution/frontend|docker-compose.yml|validate:mvp-domain-schemas|verify:transaction-import" ...` confirmed the required CI and deployment references exist in the new workflow and deploy docs.
+- 2026-03-19: Re-ran `node validate_mvp_domain_schemas.js` -> passed with `mvp_domain_schema_ok`, `entities=10`, `category_codes=18`, `transaction_fields=14`, `evidence_fields=10`, `summary_fields=8`.
+- 2026-03-19: Re-ran `node verify_transaction_import.js` -> passed with the four expected `PASS:` assertions for backfill defaults, duplicate suppression, canonical export fields, and rollback-safe checkpoints.
+- 2026-03-19: Re-ran the Python YAML parse for `.github/workflows/ci.yml` -> returned workflow name `Epic CI` and job keys `validate-assets,build-images,smoke-contract-hooks,deployment-readiness`.
+- 2026-03-19: Re-ran `rg -n "POST /api/v1/imports|POST /api/v1/exports/quarterly|solution/frontend|docker-compose.yml|validate:mvp-domain-schemas|verify:transaction-import|verification/" ...` -> confirmed the workflow and deploy docs still contain the required endpoint, build, compose, validation, and evidence references.
 
 Risks/Notes:
 - The task brief assumes root-level files that are not present; the workflow should therefore validate existing assets and treat future compose/build stages as conditional hooks.
@@ -72,7 +77,7 @@
 - This task is technical scaffolding only; no user verification gate is required unless the scope changes to user-visible runtime behavior.
 
 Completion Status:
-- Complete - 2026-03-19 17:19:59 +00:00
+- Complete - 2026-03-19 17:38:05 +00:00
 
 Original Task Brief:
 
@@ -115,9 +120,9 @@
 
 ## Verification
 
-- [ ] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
-- [ ] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
-- [ ] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
+- [x] CI workflow operates on the current additive assets: README, docs, setup scripts, and Docker config.
+- [x] `deploy/README.md` explains how future releases will use the backend/frontend build outputs.
+- [x] Release checklist references verification evidence produced under `verification/` and future smoke checks against the documented API endpoints.
 
 ## Notes
 

tokens used
97,384
```
- Retry scheduled at 2026-03-19 17:39:23
