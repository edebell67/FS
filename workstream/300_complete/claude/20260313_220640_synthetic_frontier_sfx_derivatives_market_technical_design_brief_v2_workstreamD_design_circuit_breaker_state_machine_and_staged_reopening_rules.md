# TASK D3: Design circuit breaker state machine and staged reopening rules

Source: [C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md](C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md)

## Task Summary

Design the circuit-breaker state machine for sFX instruments, including halt triggers, deterministic transition rules, staged reopening checks, and operator-visible status outputs aligned to epic section 5.3.

## Context

- Epic output root: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Target artifact: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\D\d3_circuit_breaker_state_machine_and_staged_reopening_rules.md`
- Related upstream concepts referenced by the brief: A4 oracle/divergence monitoring, B2 order-book depth metrics, D1 stress thresholds, D2 automated response orchestration

## Dependency

Dependency: Epic section 5.3 and the generated task brief. Upstream task deliverables were not present in the workspace, so this design defines the integration contract they must satisfy.

## Plan

- [x] 1. Restore the failed task to the active lifecycle lane and normalize it to the required workstream template.
  - [x] Test: Confirm the task file exists under `workstream/200_inprogress/claude` and contains the required sections (`Source`, `Dependency`, `Plan`, `Evidence`, `Implementation Log`, `Validation`, `Completion Status`).
  - Evidence: File moved to `workstream/200_inprogress/claude/20260313_220640_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamD_design_circuit_breaker_state_machine_and_staged_reopening_rules.md` and rewritten with the lifecycle structure.
- [x] 2. Author the D3 design artifact with halt triggers, state machine transitions, staged reopening controls, and operator status outputs.
  - [x] Test: `rg -n "HALTED|REOPEN_STAGE_1|depth_recovery_requirement|source_stability_requirement|manual override" "C:\\Users\\edebe\\eds\\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\\solution\\workstreams\\D\\d3_circuit_breaker_state_machine_and_staged_reopening_rules.md"` returns matches covering the required design elements.
  - Evidence: Artifact created at `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/D/d3_circuit_breaker_state_machine_and_staged_reopening_rules.md`; validation matched state names, recovery requirement sections, and emergency-only manual override constraints.
- [x] 3. Validate the design against the task verification criteria, capture evidence, and archive the task to `300_complete`.
  - [x] Test: Run targeted `rg` checks over the artifact for divergence, source instability, depth collapse, staged reopening, and emergency-only override language; then move the task file to `workstream/300_complete/claude` when all evidence is captured.
  - Evidence: Validation output captured in the Validation section; lifecycle file prepared for move to `workstream/300_complete/claude`.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\D\d3_circuit_breaker_state_machine_and_staged_reopening_rules.md`
  - Objective-Proved: The D3 design artifact exists at the expected epic solution path.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `rg` validation results recorded in the Validation section for lifecycle sections and D3 artifact content coverage.
  - Objective-Proved: The artifact text covers the required trigger classes, staged reopening controls, and emergency-only override rules.
  - Status: captured
- Evidence-Type: diff
  - Artifact: This lifecycle file plus the new D3 design artifact.
  - Objective-Proved: The workspace contains the documented implementation changes required by the task.
  - Status: captured

## Implementation Log

- 2026-03-16 21:38: Read `skills/workstream-task-lifecycle/SKILL.md` and the failed D3 task stub.
- 2026-03-16 21:38: Located the task under `workstream/400_failed/claude`, confirmed the prompt path was stale, and restored it to `workstream/200_inprogress/claude`.
- 2026-03-16 21:38: Reviewed the source epic and the empty epic output scaffolding to determine the correct solution artifact location for Workstream D.
- 2026-03-16 21:38: Authored the D3 design artifact under the epic solution folder with trigger families, state transitions, cooldowns, staged reopening gates, operator status fields, and emergency-only manual override constraints.
- 2026-03-16 21:38: Ran targeted `rg` checks to verify lifecycle-section compliance and artifact coverage for halt triggers, staged reopening, and override restrictions.

## Changes Made

- Moved the D3 task file from `workstream/400_failed/claude` to `workstream/200_inprogress/claude`.
- Replaced the generated stub with a lifecycle-compliant task document that tracks plan steps, evidence, validation, and completion state.
- Added `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/D/d3_circuit_breaker_state_machine_and_staged_reopening_rules.md` as the Workstream D design deliverable for circuit-breaker behavior.

## Validation

- `rg -n "^Source:|^## Dependency|^## Plan|^## Evidence|^## Implementation Log|^## Validation|^## Completion Status" "C:\Users\edebe\eds\workstream\200_inprogress\claude\20260313_220640_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamD_design_circuit_breaker_state_machine_and_staged_reopening_rules.md"`
  - Result: matched `Source`, `Dependency`, `Plan`, `Evidence`, `Implementation Log`, `Validation`, and `Completion Status` headings at lines 3, 15, 19, 31, 49, 60, and 71.
- `rg -n "HALTED|REOPEN_STAGE_1|depth_recovery_requirement|source_stability_requirement|manual override" "C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\D\d3_circuit_breaker_state_machine_and_staged_reopening_rules.md"`
  - Result: matched halt states, allowed transition rows, recovery requirement sections, operator status fields, and manual override constraints.
- `rg -n "index divergence|source instability|depth collapse|staged reopening|automated staged rules|emergency override" "C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\D\d3_circuit_breaker_state_machine_and_staged_reopening_rules.md"`
  - Result: matched staged-reopening language plus explicit references to index divergence, source instability, depth collapse relapse, and emergency override behavior satisfying the task verification points.

## Risks/Notes

- Upstream D1/D2/A4/B2 task outputs were not present in the workspace, so numeric thresholds are expressed as contract-driven bands and gating rules rather than fixed production values.
- This task is documentation/design only; no executable market engine code was added.

## Completion Status

Complete - 2026-03-16 21:38:41
