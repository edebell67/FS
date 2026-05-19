# TASK A2: Specify source ingestion and normalization pipeline

## Source

- Source epic: `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Recovered from failed lane: `C:\Users\edebe\eds\workstream\400_failed\gemini\20260313_220628_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_specify_source_ingestion_and_normalization_pipeline.md`

## Task Summary

Produce a deterministic source-ingestion and normalization design for the Synthetic Frontier macro volatility index layer, including source adapters, canonical quote normalization, anomaly handling, freshness thresholds, and fallback ordering that can feed later index-calculation and oracle-health tasks.

## Context

- Epic output folder: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Target deliverables will be created under `solution\`.
- The source epic requires official rates, offshore pricing, proxy feeds, medianisation, smoothing, and source observability.
- The assigned task references A1 as an input, but the epic solution folder currently has no A1 artifact to bind the pipeline to.

## Dependency

Dependency: `20260313_220627_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_define_macro_volatility_index_schema_and_source_contract.md` was not present in the epic solution output, so this task will create the minimal canonical source contract artifact required to make the ingestion pipeline concrete and testable.

## Plan

- [x] 1. Establish the canonical source contract and field mapping required by the ingestion pipeline.
  - [x] Test: Review `workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md` and confirm the lifecycle file records the source categories, canonical fields, and fallback objectives needed by the pipeline.
  - Evidence: Epic lines 32-34 explicitly require official reference rates, offshore pricing, parallel market proxies, volatility weighting, smoothing, and medianisation; the created contract and spec map those into canonical source categories plus required fields `source_id`, `source_type`, `poll_interval`, `normalization_rule`, `staleness_threshold`, `fallback_priority`, and `anomaly_flag`.
- [x] 2. Create the machine-readable source contract and the human-readable ingestion/normalization pipeline design in the epic `solution\` tree.
  - [x] Test: `Test-Path 'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\json\macro_volatility_source_contract.json'; Test-Path 'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\source_ingestion_normalization_pipeline.md'`; pass if both commands return `True`.
  - Evidence: Both file existence checks returned `True` after creating `solution\json\macro_volatility_source_contract.json` and `solution\source_ingestion_normalization_pipeline.md`.
- [x] 3. Run structural validation on the created artifacts and capture proof in this lifecycle file.
  - [x] Test: `python -m json.tool C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\json\macro_volatility_source_contract.json` and `rg -n "source_id|source_type|poll_interval|normalization_rule|staleness_threshold|fallback_priority|anomaly_flag|Ingestion Stages|Quality Gates|Fallback" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\source_ingestion_normalization_pipeline.md`; pass if JSON parses and the markdown includes all required sections and fields.
  - Evidence: `python -m json.tool` parsed the contract successfully and `rg -n` matched all required field names and control sections in the markdown spec, including `Ingestion Stages`, `Quality Gates`, and `Fallback Behavior`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\json\macro_volatility_source_contract.json` and `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\source_ingestion_normalization_pipeline.md`
  - Objective-Proved: The epic solution folder contains a canonical source contract and pipeline design deliverable for this task.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `Test-Path ... -> True / True`; `python -m json.tool ...` parsed successfully; `rg -n ...` matched required fields and sections at lines 13-19, 30, 56, 106, 127, and 129.
  - Objective-Proved: The source contract parses as valid JSON and the pipeline spec contains the required normalized fields and control sections.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `git status --short -- ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/json/macro_volatility_source_contract.json ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/source_ingestion_normalization_pipeline.md workstream/200_inprogress/gemini/20260313_220628_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_specify_source_ingestion_and_normalization_pipeline.md` -> all three files reported as `??` prior to completion move.
  - Objective-Proved: The workspace changes for this task are limited to the synthetic frontier solution artifacts and this lifecycle file.
  - Status: captured

## Implementation Log

- 2026-03-16 21:37:37+00:00 - Read `skills\workstream-task-lifecycle\SKILL.md`, located the referenced task in `workstream\400_failed\gemini`, and moved it into `workstream\200_inprogress\gemini` to resume execution in the active lane.
- 2026-03-16 21:37:37+00:00 - Reviewed the source epic and confirmed that the synthetic frontier epic output tree was empty, so this task must create the actual deliverables rather than patch existing artifacts.
- 2026-03-16 21:37:37+00:00 - Rewrote the task file into the required lifecycle format with explicit dependency handling, sequential tests, and normalized evidence placeholders before editing solution files.
- 2026-03-16 21:38:00+00:00 - Created `solution\json\macro_volatility_source_contract.json` with canonical field definitions, source profiles, and selection policy to satisfy the missing A1 dependency at the solution-artifact level.
- 2026-03-16 21:39:00+00:00 - Created `solution\source_ingestion_normalization_pipeline.md` defining ingestion stages, deterministic normalization rules, quality gates, freshness policy, anomaly semantics, and fallback ordering for official, offshore, and proxy feeds.
- 2026-03-16 21:40:04+00:00 - Ran the planned validations: epic requirement grep, file existence checks, JSON parsing, markdown structural scan, and scoped git status capture.

## Changes Made

- Added `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\json\macro_volatility_source_contract.json`
  - Defined the canonical source envelope for the index data layer.
  - Added required fields for source identity, timing, normalization, freshness, fallback ranking, and anomaly classification.
  - Added baseline source profiles for official reference, offshore spot, parallel proxy, and derived proxy feeds.
  - Added a deterministic selection policy for blocking anomalies, soft degradation, and minimum live-source count.
- Added `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\source_ingestion_normalization_pipeline.md`
  - Documented source categories, pipeline stages, normalization recipes, quality gates, freshness thresholds, fallback order, and anomaly semantics.
  - Defined direct handoff assumptions for downstream weighting/smoothing and oracle-health tasks.
- Updated `C:\Users\edebe\eds\workstream\200_inprogress\gemini\20260313_220628_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_specify_source_ingestion_and_normalization_pipeline.md`
  - Converted the task into the required lifecycle template.
  - Recorded ordered test execution, evidence, validation outputs, and completion metadata.

## Validation

- Executed: `rg -n "Official reference rates|Offshore pricing|Parallel market proxies|Medianisation" C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
  - Result: Pass. Matched epic lines 32-34, confirming the required upstream source categories and downstream weighting/smoothing context.
- Executed: `Test-Path 'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\json\macro_volatility_source_contract.json'; Test-Path 'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\source_ingestion_normalization_pipeline.md'`
  - Result: Pass. Output was `True` and `True`.
- Executed: `python -m json.tool C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\json\macro_volatility_source_contract.json`
  - Result: Pass. JSON parsed successfully and echoed the normalized structure.
- Executed: `rg -n "source_id|source_type|poll_interval|normalization_rule|staleness_threshold|fallback_priority|anomaly_flag|Ingestion Stages|Quality Gates|Fallback" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\source_ingestion_normalization_pipeline.md`
  - Result: Pass. Matches included lines 13-19, 30, 56, 106, 127, and 129.
- Executed: `git status --short -- ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/json/macro_volatility_source_contract.json ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/source_ingestion_normalization_pipeline.md workstream/200_inprogress/gemini/20260313_220628_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_specify_source_ingestion_and_normalization_pipeline.md`
  - Result: Pass. Scoped status showed only the three task files as newly added prior to lifecycle completion move.

## Risks/Notes

- This task is design-focused and non-UI, so auto-acceptance is allowed if the captured evidence reaches full coverage.
- The source contract created here is intentionally minimal and scoped to unblock deterministic ingestion; later A1/A3/A4 tasks may extend it but should remain backward compatible with the canonical fields defined here.
- The source profiles and thresholds are baseline configuration defaults, not production-calibrated market data values.

## Completion Status

Complete as of 2026-03-16 21:40:04+00:00. Objective delivered with 100% evidence coverage and auto-acceptance enabled.
