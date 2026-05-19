Source: `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`

Task Summary
Define the F1 isolated-margin and per-instrument containment model for the Synthetic Frontier sFX venue, producing a launch-time specification that makes margin scope, vault boundaries, loss containment, and shared systemic dependencies explicit for the phase-1 instruments.

Context
- Epic brief: `C:\Users\edebe\eds\workstream\000_epic\20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Task file: `C:\Users\edebe\eds\workstream\300_complete\gemini\20260313_220644_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_define_isolated_margin_and_per_instrument_containment_model.md`
- Deliverable path: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
- Dependency references available only as generated task stubs:
  - `C:\Users\edebe\eds\workstream\400_failed\claude\20260313_220631_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_define_perpetual_instrument_and_market_configuration_model.md`
  - `C:\Users\edebe\eds\workstream\400_failed\gemini\20260313_220634_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamC_define_vault_accounting_and_exposure_cap_model.md`

Dependency: B1 and C1 are declared upstream dependencies, but no completed artifacts existed in the workspace. This task derives the containment model from the epic brief plus the dependency task definitions and records that assumption explicitly.

Plan
- [x] 1. Author the F1 isolation model specification with the required containment fields and phase-1 instrument coverage.
  - [x] Test: `rg -n "margin_scope|vault_scope|loss_containment_boundary|shared_dependency_exception|NGN_VOL|KES_VOL|GHS_VOL|ZAR_VOL" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`; pass if the spec includes all required containment fields and all four phase-1 instrument entries.
  - Evidence: PASS. `rg` returned the isolation-domain table header at line 19, explicit rows for `NGN_VOL`/`KES_VOL`/`GHS_VOL`/`ZAR_VOL` at lines 21-24, and the required containment fields again in the transparency outputs at lines 99-102.
- [x] 2. Add explicit failure-containment scenarios that prove losses remain instrument-local under stressed conditions.
  - [x] Test: `rg -n "Scenario 1|Scenario 2|Scenario 3|liquidation cascade|exposure cap|oracle instability|NGN_VOL|GHS_VOL" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`; pass if the spec contains multiple named stress scenarios with expected containment behavior.
  - Evidence: PASS. `rg` returned `Scenario 1` at line 66, `Scenario 2` at line 74, `Scenario 3` at line 82, with NGN and GHS stress triggers plus containment outcomes recorded at lines 67-80.
- [x] 3. Enumerate the shared dependencies outside the containment boundary and record technical validation evidence for full delivery.
  - [x] Test: `rg -n "Shared Services Outside The Containment Boundary|Index/oracle publication stack|Sequencer, matching engine, and API gateway|Governance controls|USDC custody/settlement rail|Transparency publication layer|No cross-collateralization|No inter-vault borrowing" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`; pass if the shared-service exceptions and launch-time isolation rules are explicitly listed.
  - Evidence: PASS. `rg` returned the shared-services section header at line 53, five explicit shared-service rows at lines 58-62, and the launch-time containment prohibitions `No cross-collateralization` and `No inter-vault borrowing` at lines 91-92.

Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
  - Objective-Proved: The F1 containment specification exists at the declared epic output path with the isolation-domain table, economic state model, failure scenarios, and shared dependency exceptions.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `rg -n "margin_scope|vault_scope|loss_containment_boundary|shared_dependency_exception|NGN_VOL|KES_VOL|GHS_VOL|ZAR_VOL" ...` => lines 19, 21-24, 99-102; `rg -n "Scenario 1|Scenario 2|Scenario 3|liquidation cascade|exposure cap|oracle instability|NGN_VOL|GHS_VOL" ...` => lines 66-82; `rg -n "Shared Services Outside The Containment Boundary|Index/oracle publication stack|Sequencer, matching engine, and API gateway|Governance controls|USDC custody/settlement rail|Transparency publication layer|No cross-collateralization|No inter-vault borrowing" ...` => lines 53, 58-62, 91-92.
  - Objective-Proved: The authored spec includes all required containment fields, explicit instrument-local failure scenarios, and a concrete list of shared systemic dependencies and launch-time isolation rules.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `git status --short -- ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/F/f1_isolated_margin_and_per_instrument_containment_model.md workstream/300_complete/gemini/20260313_220644_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_define_isolated_margin_and_per_instrument_containment_model.md` => `??` for both files after authoring the deliverable and archiving the lifecycle record.
  - Objective-Proved: The workspace contains the new F1 deliverable and the archived lifecycle task record in its final complete location.
  - Status: captured

Implementation Log
- 2026-03-16 21:37:21 +00:00: Read `skills/workstream-task-lifecycle/SKILL.md`, located the requested F1 task in `workstream/400_failed/gemini`, reviewed the epic brief, and inspected the upstream B1/C1 dependency stubs.
- 2026-03-16 21:37:21 +00:00: Moved the F1 task into `workstream/200_inprogress/gemini` so execution could proceed under the required lifecycle state.
- 2026-03-16 21:37:21 +00:00: Authored `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/F/f1_isolated_margin_and_per_instrument_containment_model.md` with the phase-1 instrument isolation table, economic state model, shared-service exceptions, and launch-time control rules.
- 2026-03-16 21:37:21 +00:00: Validated that the F1 spec contains all required containment fields, all four phase-1 instruments, and three explicit failure-containment scenarios.
- 2026-03-16 21:39:58 +00:00: Validated the shared-service exception list and launch-time containment prohibitions, then captured path-specific `git status` evidence for the authored deliverable and lifecycle record.
- 2026-03-16 21:39:58 +00:00: Moved the lifecycle file from `workstream/200_inprogress/gemini` to `workstream/300_complete/gemini` after all checklist items, evidence items, and validation commands were complete.

Changes Made
- Added `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/F/f1_isolated_margin_and_per_instrument_containment_model.md` with explicit `margin_scope`, `vault_scope`, `loss_containment_boundary`, and `shared_dependency_exception` definitions for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`.
- Reworked the lifecycle file into the required workstream template with ordered checklist tests, evidence tracking, implementation log, and validation sections.

Validation
- `rg -n "margin_scope|vault_scope|loss_containment_boundary|shared_dependency_exception|NGN_VOL|KES_VOL|GHS_VOL|ZAR_VOL" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
  - Result: PASS. Returned the required containment fields plus explicit rows for all four phase-1 instruments.
- `rg -n "Scenario 1|Scenario 2|Scenario 3|liquidation cascade|exposure cap|oracle instability|NGN_VOL|GHS_VOL" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
  - Result: PASS. Returned three named failure scenarios with instrument-local containment expectations.
- `rg -n "Shared Services Outside The Containment Boundary|Index/oracle publication stack|Sequencer, matching engine, and API gateway|Governance controls|USDC custody/settlement rail|Transparency publication layer|No cross-collateralization|No inter-vault borrowing" C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\F\f1_isolated_margin_and_per_instrument_containment_model.md`
  - Result: PASS. Returned the explicit shared-service exception list and launch-time isolation prohibitions.
- `git status --short -- ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/F/f1_isolated_margin_and_per_instrument_containment_model.md workstream/300_complete/gemini/20260313_220644_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamF_define_isolated_margin_and_per_instrument_containment_model.md`
  - Result: PASS. Reported both paths as present in the workspace as newly authored/updated files.

Risks/Notes
- Upstream B1 and C1 deliverables are not yet completed in the workspace, so this F1 output is a launch-design specification derived from the epic plus dependency task definitions rather than from finalized upstream artifacts.
- The containment model intentionally preserves strict launch-time isolation; any future portfolio margin, shared insurance fund, or inter-vault borrowing model would require a new task because it changes the risk boundary materially.

Completion Status
Complete as of 2026-03-16 21:39:58 +00:00.
