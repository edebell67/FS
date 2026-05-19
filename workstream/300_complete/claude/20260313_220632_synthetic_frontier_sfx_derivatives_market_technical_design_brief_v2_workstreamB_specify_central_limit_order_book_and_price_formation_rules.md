# TASK B2: Specify central limit order book and price formation rules

**Workstream:** B — Trading Core
**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
**Priority:** 1
**Source Epic Path:** `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
**Epic Output Folder:** `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
**Suggested Agent:** codex
**UI Deliverable:** No
**Status:** [x] Complete
**Source:** `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`

## Task Summary

Specify the MVP central limit order book and price-formation behavior
for the synthetic frontier perpetual venue, including order lifecycle,
matching priority, visible depth publication, and derived market-state
metrics used by funding, risk, and stress modules.

## Context

- Epic sections 2, 3, 4, and 5 define the venue as order-book based and
  state that price is determined by order flow rather than pegged to the
  reference index.
- The epic output workspace at
  `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B`
  had no existing artifacts for Workstream B.
- The direct dependency task B1 has not been implemented yet, so this
  task uses the B1 field list from the decomposed task contract as the
  minimum dependency interface and records that assumption in the spec.

## Dependency

Dependency: B1 minimum market configuration contract
(`instrument_id`, `quote_collateral`, `index_reference`, `tick_size`,
`lot_size`, `max_leverage_band`, `position_size_cap`, `vault_id`,
`status`)

## Plan

- [x] 1. Restore the failed B2 task to the active lifecycle and define
  the target specification artifact for Workstream B.
  - [x] Test: `Test-Path 'C:\Users\edebe\eds\workstream\200_inprogress\claude\20260313_220632_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_specify_central_limit_order_book_and_price_formation_rules.md'`; pass if command returns `True`.
  - Evidence: Restored the lifecycle file to `workstream/200_inprogress/claude/...220632...md`; `Test-Path` returned `True`.
- [x] 2. Write the CLOB and price-formation specification covering order
  lifecycle, matching priority, market-state outputs, and derived depth
  metrics.
  - [x] Test: `rg -n "order-flow determined|price priority|time priority|depth_snapshot|book_thinning_metric|book_imbalance" "C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b2_central_limit_order_book_and_price_formation_rules.md"`; pass if all required sections are matched.
  - Evidence: Added `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b2_central_limit_order_book_and_price_formation_rules.md`; validation matched all required terms.
- [x] 3. Validate the spec against the task acceptance criteria and
  capture completion evidence.
  - [x] Test: `python -c "from pathlib import Path; text = Path(r'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b2_central_limit_order_book_and_price_formation_rules.md').read_text(); checks = {'order_flow_price': 'order-flow determined' in text and 'not a peg' in text, 'outputs_enumerated': all(term in text for term in ['depth_snapshot', 'book_imbalance', 'book_thinning_metric', 'best_bid', 'best_ask']), 'phase1_consistency': 'low-leverage MVP launch' in text and 'price-time priority' in text}; print(checks); assert all(checks.values())"`; pass if the script prints all checks as `True`.
  - Evidence: Python acceptance script passed with all three checks reported as `True`.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b2_central_limit_order_book_and_price_formation_rules.md`
  - Objective-Proved: The required B2 specification artifact exists in the epic output workspace and contains the CLOB, matching, and market-state design.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `rg -n "order-flow determined|price priority|time priority|depth_snapshot|book_thinning_metric|book_imbalance" "C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b2_central_limit_order_book_and_price_formation_rules.md"`
  - Objective-Proved: The document explicitly covers price formation, queue priority, visible depth, and derived metrics required by the task.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -c "from pathlib import Path; text = Path(r'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b2_central_limit_order_book_and_price_formation_rules.md').read_text(); checks = {'order_flow_price': 'order-flow determined' in text and 'not a peg' in text, 'outputs_enumerated': all(term in text for term in ['depth_snapshot', 'book_imbalance', 'book_thinning_metric', 'best_bid', 'best_ask']), 'phase1_consistency': 'low-leverage MVP launch' in text and 'price-time priority' in text}; print(checks); assert all(checks.values())"`
  - Objective-Proved: The spec satisfies all three explicit acceptance checks from the task.
  - Status: captured

## Implementation Log

- 2026-03-16T21:34:24+00:00 Read `skills/workstream-task-lifecycle/SKILL.md`, confirmed the requested task path was stale, and located the B2 task file in `workstream/400_failed/claude`.
- 2026-03-16T21:34:24+00:00 Reviewed the source epic and epic output workspace; confirmed the Workstream B output directory was empty and needed a new deliverable.
- 2026-03-16T21:34:24+00:00 Restored the B2 lifecycle file into `workstream/200_inprogress/claude` to resume execution in the correct lifecycle lane.
- 2026-03-16T21:34:24+00:00 Authored `b2_central_limit_order_book_and_price_formation_rules.md` with sections for dependency contract, order types, validation, price-time matching, order-flow-based execution pricing, depth visibility, and derived market-state metrics.
- 2026-03-16T21:40:32+00:00 Ran the three planned validation commands; all passed, including the acceptance script reporting `{'order_flow_price': True, 'outputs_enumerated': True, 'phase1_consistency': True}`.

## Changes Made

- Added
  `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b2_central_limit_order_book_and_price_formation_rules.md`
  containing:
  - MVP supported order types and exclusions
  - order validation and lifecycle rules
  - strict price-time priority rules
  - trade-price formation that explicitly separates order-flow pricing
    from the reference index
  - required market-state outputs for downstream funding, risk, and
    stress modules
  - transparent depth publication requirements and formulas for
    `book_imbalance` and `book_thinning_metric`
- Replaced the failed stub task file with a lifecycle-compliant record
  including ordered checklist steps, evidence inventory, implementation
  log, and validation outcomes.

## Validation

- Executed:
  - `Test-Path 'C:\Users\edebe\eds\workstream\200_inprogress\claude\20260313_220632_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_specify_central_limit_order_book_and_price_formation_rules.md'`
  - `rg -n "order-flow determined|price priority|time priority|depth_snapshot|book_thinning_metric|book_imbalance" "C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b2_central_limit_order_book_and_price_formation_rules.md"`
  - `python -c "from pathlib import Path; text = Path(r'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b2_central_limit_order_book_and_price_formation_rules.md').read_text(); checks = {'order_flow_price': 'order-flow determined' in text and 'not a peg' in text, 'outputs_enumerated': all(term in text for term in ['depth_snapshot', 'book_imbalance', 'book_thinning_metric', 'best_bid', 'best_ask']), 'phase1_consistency': 'low-leverage MVP launch' in text and 'price-time priority' in text}; print(checks); assert all(checks.values())"`
- Result:
  - Pass. `Test-Path` returned `True`.
  - Pass. `rg` matched `price priority`, `time priority`, `depth_snapshot`, `book_imbalance`, `book_thinning_metric`, and `order-flow determined`.
  - Pass. Python printed `{'order_flow_price': True, 'outputs_enumerated': True, 'phase1_consistency': True}` and exited successfully.
- User verification not required because this task produces a technical design specification and meets the lifecycle auto-acceptance gate with `Objective-Delivery-Coverage: 100%` and `Auto-Acceptance: true`.

## Risks/Notes

- B1 is still pending as a standalone deliverable. This B2 artifact
  therefore records the minimum B1 dependency interface explicitly so
  later tasks can align on the same contract.
- The spec intentionally limits phase-1 order types and advanced book
  features to preserve deterministic behavior in a thin-liquidity, low-
  leverage launch.

## Completion Status

Complete as of 2026-03-16T21:40:32+00:00. All checklist items, tests,
and required evidence are recorded.
