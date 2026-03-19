# Task: Synthetic Frontier A3 Index Calculation, Weighting, and Smoothing Engine

## Source
- Epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Derived task: `workstream/artefacts/epic_decomp_20260313_220421_135810/epic_decomp_output.json` item `A3`

## Task Summary
- Produce the deterministic A3 technical design for converting normalized source observations into the publishable macro volatility index used by funding, liquidation, and circuit-breaker modules.

## Context
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/a3_index_calculation_weighting_and_smoothing_engine.md`
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/a3_index_calculation_test_vectors.json`
- `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Upstream dependency references only exist as unimplemented task stubs:
  - `workstream/400_failed/gemini/20260313_220627_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_define_macro_volatility_index_schema_and_source_contract.md`
  - `workstream/400_failed/gemini/20260313_220628_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_specify_source_ingestion_and_normalization_pipeline.md`

## Dependency
Dependency: A1 schema and A2 ingestion specification are not implemented in the workspace; this task therefore records the minimum inferred normalized input contract required to complete A3 without inventing additional upstream files.

## Plan
- [x] 1. Reactivate the failed A3 task and rewrite it into the required lifecycle format with explicit dependency, plan, and evidence tracking.
  - [x] Test: `Test-Path .\workstream\200_inprogress\gemini\20260313_220629_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_design_index_calculation_weighting_and_smoothing_engine.md` returns `True`.
  - [x] Evidence: Task file was moved from `workstream/400_failed/gemini` to `workstream/200_inprogress/gemini` and rewritten with the required sections on 2026-03-16.
- [x] 2. Author the A3 design specification covering calculation sequence, weighting logic, medianization, smoothing, confidence scoring, edge cases, and downstream consumption.
  - [x] Test: `Select-String -Path .\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\a3_index_calculation_weighting_and_smoothing_engine.md -Pattern 'Algorithm Summary','Pseudocode','confidence_score','Funding Consumption','Liquidation Consumption','Circuit Breaker Consumption'` returns all required sections.
  - [x] Evidence: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/a3_index_calculation_weighting_and_smoothing_engine.md`
- [x] 3. Create deterministic test vectors for normal, source-conflict, and degraded-data scenarios and validate the artifact structure.
  - [x] Test: `@('normal','source_conflict','degraded_data') | ForEach-Object { Select-String -Path .\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\a3_index_calculation_test_vectors.json -Pattern ('\"scenario_id\": \"' + $_ + '\"') }` returns one match for each scenario.
  - [x] Evidence: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/a3_index_calculation_test_vectors.json`

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `workstream/300_complete/gemini/20260313_220629_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_design_index_calculation_weighting_and_smoothing_engine.md`
  - Objective-Proved: The task was reactivated and tracked using the mandated lifecycle structure.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/a3_index_calculation_weighting_and_smoothing_engine.md`
  - Objective-Proved: The deterministic calculation, weighting, smoothing, confidence, and downstream consumption design was delivered.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `Select-String` validation over the A3 solution document and scenario checks over the verification JSON, captured in the Validation section below.
  - Objective-Proved: Required sections and all three scenario classes exist in the produced artifacts.
  - Status: captured

## Implementation Log
- 2026-03-16 21:33 Europe/London: read `skills/workstream-task-lifecycle/SKILL.md` and the requested task path; located the actual A3 task under `workstream/400_failed/gemini` because the user-supplied `200_inprogress` path did not exist.
- 2026-03-16 21:36 Europe/London: reviewed the epic and decomposition artifact to confirm A3 output scope, dependencies, and required verification points.
- 2026-03-16 21:41 Europe/London: moved the A3 lifecycle file into `workstream/200_inprogress/gemini` and rewrote it into the required lifecycle format.
- 2026-03-16 21:47 Europe/London: authored the A3 design specification in the epic `solution` folder, including inferred normalized-input assumptions because A1 and A2 are still missing.
- 2026-03-16 21:50 Europe/London: created structured JSON test vectors for normal, source-conflict, and degraded-data scenarios in the epic `verification` folder.
- 2026-03-16 21:53 Europe/London: ran content validation checks against the solution and verification artifacts and recorded the results.
- 2026-03-16 21:54 Europe/London: moved the lifecycle file from `workstream/200_inprogress/gemini` to `workstream/300_complete/gemini` after validation passed and auto-acceptance criteria were satisfied.

## Changes Made
- Added `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/a3_index_calculation_weighting_and_smoothing_engine.md`
  - Defines inferred normalized input fields, calculation cadence, weighting formula, weighted-median medianization rule, EWMA smoothing, confidence score formula, degraded-mode handling, and downstream consumption contracts.
- Added `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/a3_index_calculation_test_vectors.json`
  - Provides deterministic phase-1 examples for NGN, KES, and GHS under normal, conflict, and degraded-data conditions with expected outputs.
- Updated this lifecycle file
  - Reactivated the task from `400_failed`, captured dependency gaps, evidence, implementation log, validation results, and archived it under `300_complete`.

## Validation
- `Test-Path .\workstream\200_inprogress\gemini\20260313_220629_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_design_index_calculation_weighting_and_smoothing_engine.md`
  - Result: `True`
- `Select-String -Path .\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\a3_index_calculation_weighting_and_smoothing_engine.md -Pattern 'Algorithm Summary','Pseudocode','confidence_score','Funding Consumption','Liquidation Consumption','Circuit Breaker Consumption'`
  - Result: matched all six required sections.
- `@('normal','source_conflict','degraded_data') | ForEach-Object { Select-String -Path .\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\a3_index_calculation_test_vectors.json -Pattern ('\"scenario_id\": \"' + $_ + '\"') }`
  - Result: one match each for `normal`, `source_conflict`, and `degraded_data`.
- `Test-Path .\workstream\300_complete\gemini\20260313_220629_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_design_index_calculation_weighting_and_smoothing_engine.md`
  - Result: `True`

## Risks/Notes
- A1 and A2 remain unresolved upstream dependencies. This A3 deliverable therefore includes an explicitly scoped inferred normalized-input contract instead of relying on missing upstream files.
- The artifact is a design specification and verification dataset, not an executable engine implementation. A later implementation task should convert the pseudocode and vectors into code.
- Because this task is non-UI and delivers a complete documented artifact set with 100% objective coverage, it qualifies for auto-acceptance under the lifecycle rules.

## Completion Status
Complete - 2026-03-16 21:53 Europe/London
