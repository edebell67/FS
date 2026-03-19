# Task: Define Macro Volatility Index Schema and Source Contract

## Source
- Source epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`

## Task Summary
- Define the canonical phase-1 macro volatility index source contract for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`, including versioned schema fields, source taxonomy, publication semantics, nullable rules, precision, freshness thresholds, and a worked example suitable for downstream market-control consumers.

## Context
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams`
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification`
- `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`

## Dependency
Dependency: None

## Plan
- [x] 1. Recover the failed task into active lifecycle tracking and align the deliverable target paths with the epic output folder.
  - [x] Test: verify the task file exists under `workstream/200_inprogress/gemini` and the epic output folder contains writable `solution` and `verification` subfolders.
  - [x] Evidence: task recovered to `workstream/200_inprogress/gemini/20260313_220627_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamA_define_macro_volatility_index_schema_and_source_contract.md`; epic output folder confirmed at `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`.
- [x] 2. Author the macro volatility index contract artifacts covering required fields, source taxonomy, per-instrument rules, and a worked phase-1 example.
  - [x] Test: confirm the solution and verification artifacts exist and contain the required field set, worked example, and downstream use-case coverage.
  - [x] Evidence: created `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema_and_source_contract.md`, `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema.json`, and `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/workstream_a1_ngn_vol_example.json`.
- [x] 3. Validate the artifacts, capture proof, and close the lifecycle task.
  - [x] Test: parse both JSON files successfully and run content checks proving required fields, the worked example, and funding/liquidation/circuit-breaker support are present.
  - [x] Evidence: `JSON_OK solution/workstreams/workstream_a1_macro_volatility_index_schema.json`; `JSON_OK verification/workstream_a1_ngn_vol_example.json`; `required_fields_present=True`; `worked_example_present=True`; `use_cases_present=True`.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema_and_source_contract.md`
  - Objective-Proved: proves the human-readable contract defines field types, units, nullable rules, freshness expectations, publication semantics, source taxonomy, and per-instrument dictionaries.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema.json`
  - Objective-Proved: proves the contract has a machine-readable schema for normalized input observations and published index outputs.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/workstream_a1_ngn_vol_example.json`
  - Objective-Proved: proves a worked phase-1 `NGN_VOL` example exists with raw inputs and resulting normalized output.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python json.load` validation output: `JSON_OK solution/workstreams/workstream_a1_macro_volatility_index_schema.json`; `JSON_OK verification/workstream_a1_ngn_vol_example.json`
  - Objective-Proved: proves both JSON artifacts are syntactically valid and loadable.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: content check output: `required_fields_present=True`; `worked_example_present=True`; `use_cases_present=True`
  - Objective-Proved: proves the specification covers the required field set, includes a worked example, and explicitly supports funding, liquidation, and circuit-breaker use cases.
  - Status: captured

## Implementation Log
- 2026-03-16 21:27 Europe/London: loaded `skills/workstream-task-lifecycle/SKILL.md` and verified the user-supplied task path did not exist in `200_inprogress`.
- 2026-03-16 21:29 Europe/London: located the task in `workstream/400_failed/gemini`, inspected the source epic, and confirmed the epic output folder existed but had no A1 deliverables.
- 2026-03-16 21:34 Europe/London: recovered the task into `workstream/200_inprogress/gemini` for active lifecycle tracking.
- 2026-03-16 21:42 Europe/London: authored the A1 schema contract markdown, machine-readable JSON schema, and `NGN_VOL` worked example under the epic output folder.
- 2026-03-16 21:44 Europe/London: validated JSON syntax and ran targeted content checks for required fields, worked example coverage, and downstream use-case support.
- 2026-03-16 21:46 Europe/London: updated this lifecycle file with completed checklist items, captured evidence, and completion status.

## Changes Made
- Added `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema_and_source_contract.md`
  - defines publication semantics, freshness thresholds, canonical input and output records, source taxonomy, phase-1 instrument matrix, per-instrument field dictionary, and a worked `NGN_VOL` example.
- Added `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema.json`
  - defines a machine-readable contract for `input_observation` and `published_index_output` payloads under version `a1.v1`.
- Added `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/workstream_a1_ngn_vol_example.json`
  - provides a concrete validation payload aligned to the schema and markdown example.
- Updated this lifecycle file to convert the original generated task stub into a lifecycle-compliant completion record.

## Validation
- Command: `@' ... json.load(...) ... '@ | python -`
  - Result: `JSON_OK solution/workstreams/workstream_a1_macro_volatility_index_schema.json`
  - Result: `JSON_OK verification/workstream_a1_ngn_vol_example.json`
- Command: `@' ... content checks ... '@ | python -`
  - Result: `required_fields_present=True`
  - Result: `worked_example_present=True`
  - Result: `use_cases_present=True`
- Manual check: listed `solution/workstreams` and `verification` contents under the epic output folder.
  - Result: confirmed the new A1 deliverables exist at the expected paths.

## Risks/Notes
- The contract uses source classes and abstract feed identifiers rather than vendor-specific production integrations; A2 should bind these classes to concrete adapters and failure handling.
- The JSON schema is structural validation only; weighting, smoothing, and divergence logic remain downstream responsibilities for A3 and A4.
- Freshness thresholds and smoothing windows are design defaults and should be revisited once real source latency distributions are measured.

## Completion Status
- Complete — 2026-03-16 21:46 Europe/London
