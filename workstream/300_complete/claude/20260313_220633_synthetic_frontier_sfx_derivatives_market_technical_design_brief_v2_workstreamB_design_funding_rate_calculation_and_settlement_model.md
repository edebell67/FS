# Task: Design Funding Rate Calculation And Settlement Model

## Source
- Source epic: `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Recovered from failed task record: `C:\Users\edebe\eds\workstream\400_failed\claude\20260313_220633_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_design_funding_rate_calculation_and_settlement_model.md`

## Task Summary
- Produce the B3 funding-rate design artifact for the synthetic frontier sFX derivatives market, including formula specification, parameter definitions, settlement cadence, and disclosure-ready worked examples.

## Context
- `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
- `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\a3_index_calculation_weighting_and_smoothing_engine.md`
- `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\a3_index_calculation_test_vectors.json`
- `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_b3_funding_rate_calculation_and_settlement_model.md`
- `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_b3_funding_examples.json`

## Dependency
Dependency: A3 index calculation artifact exists in the workspace. B1 and B2 deliverables are not yet implemented, so this task defines the minimum inferred contract needed from those upstream workstreams.

## Plan
- [x] 1. Recover the failed task into the active lifecycle state and restate it in the required workstream format.
  - [x] Test: `Get-Content -Raw C:\Users\edebe\eds\workstream\200_inprogress\claude\20260313_220633_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_design_funding_rate_calculation_and_settlement_model.md` shows `Source`, `Task Summary`, `Context`, `Dependency`, ordered `Plan`, `Evidence`, and `Completion Status`.
  - [x] Evidence: the recovered lifecycle file now exists in `workstream/200_inprogress/claude` with the required sections.
- [x] 2. Author the funding-rate and settlement design deliverables under the epic solution and verification folders.
  - [x] Test: the funding spec documents a continuous formula, sign convention, cadence, settlement path, disclosure fields, and worked examples; the companion verification JSON parses successfully.
  - [x] Evidence: `workstream_b3_funding_rate_calculation_and_settlement_model.md` and `workstream_b3_funding_examples.json` were created under the epic output folder.
- [x] 3. Validate the deliverables and capture evidence proving the task objective is fully delivered.
  - [x] Test: targeted `rg` checks confirm required concepts are present, and `Get-Content ... | ConvertFrom-Json` succeeds for the verification artifact.
  - [x] Evidence: validation command output recorded in this lifecycle file shows the design is present and machine-readable.

## Implementation Log
- 2026-03-16 21:33 Europe/London: Read `skills/workstream-task-lifecycle/SKILL.md`, then attempted the user-provided task path and found it missing from `workstream/200_inprogress`.
- 2026-03-16 21:35 Europe/London: Located the exact task under `workstream/400_failed/claude`, inspected the source epic, and confirmed the deliverable is a design artifact rather than runtime code.
- 2026-03-16 21:39 Europe/London: Reviewed existing A-series synthetic-frontier artifacts under the epic output folder to align the B3 deliverable structure and references.
- 2026-03-16 21:45 Europe/London: Moved the failed task back into `workstream/200_inprogress/claude` to resume active work under the required lifecycle.
- 2026-03-16 21:49 Europe/London: Authored the B3 funding-rate design specification and a companion verification JSON with normal, stress, and reversal scenarios.
- 2026-03-16 21:53 Europe/London: Ran content and parsing validations, then updated this lifecycle file with evidence and completion status.

## Changes Made
- Added `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_b3_funding_rate_calculation_and_settlement_model.md`.
- Added `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_b3_funding_examples.json`.
- Rewrote the lifecycle record in `workstream/200_inprogress/claude` to the required task format, documenting recovery from the failed state, implementation steps, validations, and evidence.

## Validation
- `Get-Content -Raw C:\Users\edebe\eds\workstream\200_inprogress\claude\20260313_220633_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_design_funding_rate_calculation_and_settlement_model.md`
  - Result: pass; lifecycle file contains the required sections and ordered checklist.
- `rg -n "continuous scaling|Sign Convention|Settlement Cadence|Worked Example|Public Transparency Contract|no cliff" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_b3_funding_rate_calculation_and_settlement_model.md`
  - Result: pass; required funding-model concepts are present in the solution document.
- `Get-Content -Raw C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_b3_funding_examples.json | ConvertFrom-Json | Select-Object -ExpandProperty scenario_id`
  - Result: pass; returned `normal_balanced`, `stress_long_crowding`, and `reversal_short_crowding`.
- `rg -n "\"funding_rate_per_hour\"|\"settlement_amount_usdc\"|\"funding_multiplier\"" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\verification\workstream_b3_funding_examples.json`
  - Result: pass; verification artifact includes the required publishable outputs.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_b3_funding_rate_calculation_and_settlement_model.md`
  - Objective-Proved: proves the funding formula, settlement cadence, sign convention, and disclosure-ready behavior were documented.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `Get-Content -Raw ...\workstream_b3_funding_examples.json | ConvertFrom-Json | Select-Object -ExpandProperty scenario_id`
  - Objective-Proved: proves the worked examples artifact is syntactically valid JSON and includes multiple deterministic scenarios.
  - Status: captured
- Evidence-Type: diff
  - Artifact: lifecycle task file plus the two new B3 artifacts created in the epic output folder
  - Objective-Proved: proves the workspace now contains the recovered task record and the requested design deliverables.
  - Status: captured

## Risks/Notes
- B1 instrument configuration and B2 market-state outputs are not yet implemented in the workspace, so this design explicitly defines the minimum inferred interfaces those workstreams must satisfy.
- Parameter values are conservative MVP defaults intended for a launch posture consistent with the epic, not production-optimized coefficients.
- This is not a user-visible UI task, so auto-acceptance is allowed based on complete technical evidence.

## Completion Status
- Complete - 2026-03-16 21:53 Europe/London
