# TASK C4: Specify liquidation workflow and vault backstop intervention

**Workstream:** C — Vault and Risk Controls
**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
**Priority:** 1
**Source Epic Path:** `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
**Epic Output Folder:** `C:\Users\edebe\eds\ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
**Suggested Agent:** codex
**UI Deliverable:** No
**Status:** [x] Complete
**Source:** `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`

## Task Summary

Define a deterministic liquidation workflow for sFX perpetual positions, including maintenance margin triggers, partial liquidation sequencing, vault takeover conditions, penalty routing, and residual loss handling under stress.

## Context

- Epic sections 2 through 5 define that the market price is order-book driven while the index is limited to funding, liquidation reference, and circuit-breaker anchoring.
- The epic output folder did not yet contain upstream C-workstream implementation artifacts, so this task derives its specification directly from the epic constraints and the generated task stub.
- Deliverables for this task will be created in:
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/`
- `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/`
- Final solution artifacts were normalized under `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/` to match other completed Synthetic Frontier workstreams.

## Dependency

Dependency: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md` sections 2-5. Referenced upstream artifacts `A3`, `B1`, `C1`, and `C2` are not present in the epic output folder, so this task captures the deterministic design contract they must satisfy.

## Plan

- [x] 1. Convert the stub into an executable design task and define the target artifact set for liquidation and vault intervention.
  - [x] Test: `Test-Path 'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamC_liquidation_workflow_and_vault_backstop_spec.md'`; pass if command returns `True` after artifact creation.
  - Evidence: Command returned `True`, confirming the primary workstream C liquidation specification exists in the normalized epic solution path.
- [x] 2. Author the liquidation workflow specification and machine-readable rule set covering triggers, execution sequence, vault takeover, penalty routing, and residual loss handling.
  - [x] Test: `python -c "import json, pathlib; rules = json.loads(pathlib.Path(r'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamC_liquidation_workflow_and_vault_backstop_rules.json').read_text()); required = {'maintenance_margin','liquidation_reference_price','partial_liquidation_step','penalty_rate','vault_takeover_condition','residual_loss_handling'}; assert required <= set(rules['fields']); assert rules['liquidation_reference']['index_role'] == 'reference_only'; assert rules['vault_intervention']['mode'] == 'deterministic'; assert rules['stress_safeguards']['clustered_liquidations'] is True; print('rules_ok')"`; pass if command prints `rules_ok`.
  - Evidence: Command printed `rules_ok`, proving the machine-readable rules include all required fields, preserve reference-only index usage, use deterministic vault intervention, and enable clustered-liquidation safeguards.
- [x] 3. Validate the artifacts against the task verification criteria and capture the final evidence inventory.
  - [x] Test: `python -c "from pathlib import Path; spec = Path(r'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamC_liquidation_workflow_and_vault_backstop_spec.md').read_text(); assert 'index is never used to set executable trade price' in spec; assert 'Vault takeover is triggered automatically' in spec; assert 'Clustered Liquidation Safeguards' in spec; print('spec_ok')"`; pass if command prints `spec_ok`.
  - Evidence: Command printed `spec_ok`, confirming the delivered specification explicitly encodes the non-pegged reference-price rule, automatic vault takeover trigger language, and clustered-liquidation safeguards.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamC_liquidation_workflow_and_vault_backstop_spec.md`
  - Objective-Proved: Human-readable liquidation workflow design deliverable exists and documents trigger logic, state machine, partial liquidation, vault takeover, penalties, residual-loss handling, and clustered-liquidation safeguards.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamC_liquidation_workflow_and_vault_backstop_rules.json`
  - Objective-Proved: Machine-readable deterministic rule contract exists for downstream implementation and validation of required liquidation, penalty, vault, and residual-loss controls.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/workstreamC_liquidation_workflow_validation.md`
  - Objective-Proved: Validation outcomes are summarized alongside the task acceptance mapping in the epic verification folder.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `Test-Path=True; rules_ok; spec_ok`
  - Objective-Proved: The artifacts exist, parse successfully, and satisfy the task verification criteria around reference-only index usage, deterministic vault intervention, and stress safeguards.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `workstream/200_inprogress/claude/20260313_220637_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamC_specify_liquidation_workflow_and_vault_backstop_intervention.md` plus new files under `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/` and `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/`
  - Objective-Proved: Workspace changes are scoped to the lifecycle record and the intended workstream C design deliverables.
  - Status: captured

## Implementation Log

- 2026-03-16T21:36:10+00:00 Read `skills/workstream-task-lifecycle/SKILL.md`, then located the requested task file and found it had been parked under `workstream/400_failed` rather than the requested in-progress lane.
- 2026-03-16T21:36:10+00:00 Moved the task file from `workstream/400_failed/claude/` to `workstream/200_inprogress/claude/` so the lifecycle state matches active execution.
- 2026-03-16T21:36:10+00:00 Reviewed the epic brief and confirmed the epic output folder had the standard `solution`, `verification`, and `workstreams` directories but no existing C-workstream deliverables.
- 2026-03-16T21:38:00+00:00 Authored the liquidation workflow markdown specification and the machine-readable JSON rules contract.
- 2026-03-16T21:39:00+00:00 Normalized both solution artifacts under `solution/workstreams/` to match the existing Synthetic Frontier completion layout.
- 2026-03-16T21:39:46+00:00 Re-ran validation against the normalized paths, captured `True`, `rules_ok`, and `spec_ok`, and wrote the verification summary artifact.

## Changes Made

- Replaced the seed task stub with a lifecycle-compliant execution record in `workstream/200_inprogress/claude/20260313_220637_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamC_specify_liquidation_workflow_and_vault_backstop_intervention.md`.
- Added `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamC_liquidation_workflow_and_vault_backstop_spec.md` containing:
  - liquidation trigger formulas and side-specific breach evaluation
  - liquidation state machine and forced execution sequence
  - automatic vault takeover conditions and transfer-pricing rule
  - penalty routing, residual-loss waterfall, and clustered-liquidation safeguards
- Added `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamC_liquidation_workflow_and_vault_backstop_rules.json` containing:
  - required field inventory
  - deterministic liquidation-reference, partial-liquidation, and vault-intervention controls
  - penalty routing and residual-loss waterfall contract
  - clustered-liquidation safeguard flags for downstream machine consumption
- Added `ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/workstreamC_liquidation_workflow_validation.md` summarizing the acceptance checks and captured validation outputs.

## Validation

- `Test-Path 'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstreamC_liquidation_workflow_and_vault_backstop_spec.md'`
  - Pass: returned `True`.
- `python -c "import json, pathlib; rules = json.loads(pathlib.Path(r'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamC_liquidation_workflow_and_vault_backstop_rules.json').read_text()); required = {'maintenance_margin','liquidation_reference_price','partial_liquidation_step','penalty_rate','vault_takeover_condition','residual_loss_handling'}; assert required <= set(rules['fields']); assert rules['liquidation_reference']['index_role'] == 'reference_only'; assert rules['vault_intervention']['mode'] == 'deterministic'; assert rules['stress_safeguards']['clustered_liquidations'] is True; print('rules_ok')"`
  - Pass: printed `rules_ok`.
- `python -c "from pathlib import Path; spec = Path(r'ep_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstreamC_liquidation_workflow_and_vault_backstop_spec.md').read_text(); assert 'index is never used to set executable trade price' in spec; assert 'Vault takeover is triggered automatically' in spec; assert 'Clustered Liquidation Safeguards' in spec; print('spec_ok')"`
  - Pass: printed `spec_ok`.
- User verification not required because this task delivers a technical design artifact rather than a user-facing runtime behavior.

## Risks/Notes

- Upstream references `A3`, `B1`, `C1`, and `C2` are named in the stub but not yet materialized in the epic output folder, so this design intentionally defines the contract those artifacts must satisfy rather than importing concrete upstream parameters.
- This task is a technical design artifact, not a running engine implementation. Follow-on engineering tasks will still need to encode these rules in the matching trading/risk systems.

## Completion Status

Complete as of 2026-03-16T21:39:46+00:00. All ordered checklist items, validations, and required evidence have been captured.
