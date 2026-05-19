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
- [x] 1. Define content pillars, posting themes, and reusable content formats.
  - [x] Test: a documented content matrix exists for multiple campaign angles.
  - [x] Evidence: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` and generator-backed matrix output recorded in `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`.
- [x] 2. Implement asset or copy generation workflow.
  - [x] Test: sample posts/assets can be generated repeatably.
  - [x] Evidence: repeatable generator script, generated sample bundle, and schema artifact recorded under `ep_strategy_warehouse_marketing/solution/backend/src` and `ep_strategy_warehouse_marketing/verification`.

## Implementation Log
- Created from epic decomposition on 2026-03-16.
- 2026-03-18 18:20Z - Inspected dependency completion, epic outputs, and live Strategy Warehouse JSON feeds under `TradeApps/breakout/fs/json/live/forex`.
- 2026-03-18 18:29Z - Implemented content schema, reusable content matrix, Jinja templates, and `ContentGeneratorService` in `ep_strategy_warehouse_marketing/solution/backend/src`.
- 2026-03-18 18:31Z - Added repeatable sample-generation script and backend pytest coverage for matrix generation and campaign bundle validation.
- 2026-03-18 18:32Z - Generated live sample outputs and JSON schema artifacts from the 2026-03-18 warehouse snapshot.
- 2026-03-18 18:34Z - Requested manual review of generated copy quality before final lifecycle completion.

## Changes Made
- Added `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py` with `PublishableContent`, platform constraints, content matrix models, and campaign asset schema.
- Added `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py` to transform warehouse snapshots into reusable social posts, platform variants, and asset briefs.
- Added Jinja templates in `ep_strategy_warehouse_marketing/solution/backend/src/templates/` for signal alerts, performance summaries, and leaderboard posts.
- Added `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py` to emit repeatable sample content and `publishable_content_schema.json`.
- Added `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py` for matrix coverage and repeatable bundle generation tests.
- Added `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md` documenting content pillars, campaign angles, formats, and CTA rules.
- Generated `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.

## Validation
- `python -m pytest tests\test_content_generation_service.py`
  - Result: pass, 2 tests passed in 0.43s.
- `python src\scripts\generate_social_content_samples.py`
  - Result: pass, wrote `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`.
- Manual review requested:
  - Review `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json` and confirm pass/fail for:
    1. content pillars/themes fit the Strategy Warehouse offer,
    2. sample copy tone is acceptable for publishing,
    3. campaign asset briefs are usable for downstream creative production.

## Evidence
- Objective-Delivery-Coverage: 95%
- Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: `ep_strategy_warehouse_marketing/workstreams/A/social_content_matrix.md`
  - Objective-Proved: reusable content pillars, campaign angles, formats, and CTA rules were defined and documented.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
  - Objective-Proved: the engine can generate reusable post variants and campaign asset briefs from live warehouse data.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/publishable_content_schema.json`
  - Objective-Proved: generated content is backed by a concrete publishable schema.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m pytest tests\test_content_generation_service.py` => `2 passed in 0.43s`
  - Objective-Proved: content matrix coverage and repeatable bundle generation were validated automatically.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `ep_strategy_warehouse_marketing/solution/backend/src/schemas/content_schema.py`, `ep_strategy_warehouse_marketing/solution/backend/src/services/contentGeneratorService.py`, `ep_strategy_warehouse_marketing/solution/backend/src/scripts/generate_social_content_samples.py`, `ep_strategy_warehouse_marketing/solution/backend/tests/test_content_generation_service.py`
  - Objective-Proved: the workspace now contains the social content engine implementation and verification harness.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: pending user review of `ep_strategy_warehouse_marketing/verification/generated_social_content_samples.json`
  - Objective-Proved: generated copy and asset briefs are acceptable for brand and publishing use.
  - Status: planned

## Risks/Notes
- Brand/output quality likely needs manual review.
- Current output produces structured asset briefs, not rendered media files; downstream design/video automation can consume those briefs.
- Generated copy is grounded in local 2026-03-18 snapshot files and should be regenerated when source data changes materially.

## Completion Status
- Awaiting user verification - 2026-03-18 18:34Z


## Execution Evidence
- Agent lane: gemini
- Command: cmd /c echo gemini processing 20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
- Return code: 0
- Stdout:
```text
gemini processing 20260316_135214_trading_strategy_warehouse_create_social_content_engine.md
```


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260316_135214_trading_strategy_warehouse_create_social_content_engine.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 1
- Stderr:
```text
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
```


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
