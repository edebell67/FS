# TASK F2: Prepare phase-1 instrument listing and cap configuration pack

**Workstream:** F — Launch Readiness and Validation
**Epic:** Synthetic Frontier sFX Derivatives Market -- Technical Design Brief (v2)
**Status:** [x] Complete

## Source

- `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`

## Task Summary

Assemble the initial launch configuration pack for the phase-1 sFX instruments with conservative leverage bands, exposure caps, funding base parameters, spread floors, and explicit launch assumptions.

## Context

- Epic output folder: `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Existing upstream artifact available in workspace:
  - `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema_and_source_contract.md`
  - `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_a1_macro_volatility_index_schema.json`
  - `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/verification/workstream_a1_ngn_vol_example.json`
- The task stub cites A3, B1, C1, and C2 as dependencies, but no completed synthetic-frontier artifacts for those IDs are present in the workspace. This implementation therefore uses the epic and A1 artifacts as the available source of truth and records that assumption explicitly in the pack.

## Dependency

Dependency: `A1` artifact available; `A3`, `B1`, `C1`, and `C2` are not yet materialized in the workspace, so this task proceeds using the epic's section 4, section 5, section 7, section 8, and section 9 controls as the authoritative fallback.

## Plan

- [x] 1. Define the phase-1 pack contract and generate the launch-ready listing artifact for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`.
  - [x] Test: `python -c "import json, pathlib; p = pathlib.Path(r'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json'); data = json.loads(p.read_text()); expected = {'NGN_VOL','KES_VOL','GHS_VOL','ZAR_VOL'}; assert {item['instrument_id'] for item in data['instruments']} == expected; required = {'instrument_id','launch_enabled','initial_leverage_band','exposure_cap','funding_base_params','spread_floor','status'}; assert all(required.issubset(item) for item in data['instruments']); print('listing_pack_fields_ok')"`; pass if command prints `listing_pack_fields_ok`.
  - Evidence: Command passed and printed `listing_pack_fields_ok`, confirming the pack covers all four phase-1 instruments and every required per-instrument field.
- [x] 2. Add executable validation logic that enforces conservative leverage and exposure posture plus upstream reference integrity.
  - [x] Test: `python C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`; pass if command prints `phase_1_pack_ok`.
  - Evidence: Command passed and printed `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`, confirming conservative pack posture and valid reference paths.
- [x] 3. Add automated regression coverage for the pack and capture final validation evidence.
  - [x] Test: `python -m pytest C:\Users\edebe\eds\tests\test_sfx_phase_1_listing_pack.py -q`; pass if pytest reports the suite passes.
  - Evidence: `pytest` passed with `3 passed in 0.88s`.

## Evidence

Objective-Delivery-Coverage: 100%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json`, `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_validate_phase_1_listing_pack.py`, `tests/test_sfx_phase_1_listing_pack.py`
  - Objective-Proved: The workspace now contains the concrete phase-1 pack, executable validator, and automated regression coverage required by the task.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `listing_pack_fields_ok`; `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`; `3 passed in 0.88s`
  - Objective-Proved: The pack is complete, references valid upstream artifacts, and enforces the intended conservative launch posture under automated validation.
  - Status: captured

## Implementation Log

- 2026-03-16 Europe/London: Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned F2 task file.
- 2026-03-16 Europe/London: Reviewed the epic and confirmed the governing launch constraints available in the workspace: initial leverage `1x-2x`, separate vault exposure per instrument, governance parameter bands, dynamic spread widening, and a phase-1 set of `NGN`, `KES`, `GHS`, and `ZAR`.
- 2026-03-16 Europe/London: Inspected `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2` and found the existing A1 schema and verification sample under `solution/workstreams` and `verification`, establishing the target artifact layout for this task.
- 2026-03-16 Europe/London: Confirmed no completed synthetic-frontier A3/B1/C1/C2 artifacts are currently available in the workspace, so the pack will reference the epic sections directly for those control domains.
- 2026-03-16 21:40:16+00:00: Added `workstream_f2_phase_1_listing_pack.json` with conservative launch assumptions, upstream references, and launch-ready entries for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`.
- 2026-03-16 21:40:16+00:00: Added `workstream_f2_validate_phase_1_listing_pack.py` to validate reference existence, leverage bounds, exposure caps, spread floors, and A1-aligned smoothing windows.
- 2026-03-16 21:40:16+00:00: Added `tests/test_sfx_phase_1_listing_pack.py` with direct JSON assertions, in-process validator checks, and CLI validation coverage.
- 2026-03-16 21:40:16+00:00: Executed the three plan-step validations; all passed and were recorded below.

## Changes Made

- Added `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_phase_1_listing_pack.json` with:
  - pack-level launch assumptions for conservative MVP rollout
  - explicit upstream references to the A1 schema artifacts and the governing epic controls
  - per-instrument launch entries for `NGN_VOL`, `KES_VOL`, `GHS_VOL`, and `ZAR_VOL`
  - conservative leverage bands, exposure caps, funding base parameters, spread floors, and launch assumptions
- Added `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/solution/workstreams/workstream_f2_validate_phase_1_listing_pack.py` with:
  - JSON loading for the F2 pack artifact
  - validation of required instruments and required fields
  - conservative posture checks for leverage, spread, and cap settings
  - upstream reference path checks
  - A1-aligned smoothing-window checks
- Added `tests/test_sfx_phase_1_listing_pack.py` with:
  - coverage for expected phase-1 instrument membership
  - direct validator invocation coverage
  - CLI success-path coverage for the standalone validator

## Validation

- Executed:
  - `python -c "import json, pathlib; p = pathlib.Path(r'C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_phase_1_listing_pack.json'); data = json.loads(p.read_text()); expected = {'NGN_VOL','KES_VOL','GHS_VOL','ZAR_VOL'}; assert {item['instrument_id'] for item in data['instruments']} == expected; required = {'instrument_id','launch_enabled','initial_leverage_band','exposure_cap','funding_base_params','spread_floor','status'}; assert all(required.issubset(item) for item in data['instruments']); print('listing_pack_fields_ok')"`
  - `python C:\Users\edebe\eds\ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\solution\workstreams\workstream_f2_validate_phase_1_listing_pack.py`
  - `python -m pytest C:\Users\edebe\eds\tests\test_sfx_phase_1_listing_pack.py -q`
- Result:
  - Pass. Output included `listing_pack_fields_ok`.
  - Pass. Output included `phase_1_pack_ok instruments=4 total_vault_cap=0.55 max_operational_leverage=2.00`.
  - Pass. Output included `3 passed in 0.88s`.
- User verification not required because this task delivers a non-interactive configuration artifact and executable technical validation only.

## Risks/Notes

- The conservative cap and leverage values in this task are derived from the epic's launch posture and the A1 instrument characteristics because the cited A3/B1/C1/C2 artifacts are not yet present in the workspace.
- This task produces a configuration pack and executable validation path only; it does not implement runtime trading, funding, or stress-engine code.
- Downstream tasks can tighten or relax the values once A3/B1/C1/C2 artifacts exist, but any change should continue to respect the aggregate phase-1 cap discipline and per-instrument isolation encoded here.

## Completion Status

Complete as of 2026-03-16 21:40:16+00:00. All checklist items, tests, and required evidence are recorded.
