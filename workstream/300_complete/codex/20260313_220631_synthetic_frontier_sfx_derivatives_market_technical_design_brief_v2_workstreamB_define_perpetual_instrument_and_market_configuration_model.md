## Source
- Epic: `workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md`
- Original generated task stub: `workstream/400_failed/claude/20260313_220631_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_define_perpetual_instrument_and_market_configuration_model.md`

## Task Summary
Define the perpetual instrument and market configuration model for the Synthetic Frontier sFX derivatives MVP, including a schema, operator listing template, and explicit field ownership for trading, risk, and transparency consumers.

## Context
- Epic output folder: `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2`
- Target workstream output path: `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B`
- Upstream design references: epic sections 2, 3, 8, and 9

## Dependency
Dependency: A1 and A3 from the same epic. No A1/A3 artifacts are present yet under `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/A`, so this task uses the source epic as the active dependency baseline and records the assumption explicitly in Risks/Notes.

## Plan
- [x] 1. Re-activate the failed task as a valid lifecycle work item and align it to the required template.
  - [x] Test: `Test-Path 'workstream\200_inprogress\codex\20260313_220631_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_define_perpetual_instrument_and_market_configuration_model.md'` returns `True`.
  - Evidence: Task file moved into `workstream/200_inprogress/codex/` and rewritten to the lifecycle format.
- [x] 2. Author the perpetual market configuration deliverables under the epic output folder.
  - [x] Test: `Test-Path 'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md'` and `Test-Path 'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_market_listing_template.json'` and `Test-Path 'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_market_configuration_schema.json'` each return `True`.
  - Evidence: Deliverables created in `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/`.
- [x] 3. Validate the deliverables, capture evidence, and close the task.
  - [x] Test: `python -c "import json, pathlib; base = pathlib.Path(r'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B'); json.load(open(base / 'b1_perpetual_market_listing_template.json')); json.load(open(base / 'b1_perpetual_market_configuration_schema.json')); print('json_ok')"` prints `json_ok`, and a content check confirms the schema/model covers stablecoin margining, isolated exposure, index references, and required consumer fields.
  - Evidence: Validation commands recorded in the Validation section with passing results.

## Evidence
Objective-Delivery-Coverage: 100%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b1_perpetual_instrument_market_configuration_model.md`, `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b1_perpetual_market_listing_template.json`, `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b1_perpetual_market_configuration_schema.json`
  - Objective-Proved: The workspace contains the required B1 design artifacts implementing the perpetual instrument and market configuration model.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -c "import json, pathlib; base = pathlib.Path(r'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B'); json.load(open(base / 'b1_perpetual_market_listing_template.json')); json.load(open(base / 'b1_perpetual_market_configuration_schema.json')); print('json_ok')"`
  - Objective-Proved: The JSON template and JSON schema are syntactically valid and load successfully.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `rg -n "quote_collateral|isolated_margin|index_reference|transparency_fields|position_size_cap|vault_id" ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b1_perpetual_instrument_market_configuration_model.md`
  - Objective-Proved: The written model explicitly covers stablecoin margining, isolation, index references, listing controls, and downstream consumer field requirements.
  - Status: captured

## Implementation Log
- 2026-03-16 21:35:35 +00:00: Read `skills/workstream-task-lifecycle/SKILL.md`, located the requested B1 task, and found the provided path was stale because the task lived in `workstream/400_failed/claude/`.
- 2026-03-16 21:35:35 +00:00: Confirmed the epic output tree existed but `workstreams/B` and `verification/` were still empty.
- 2026-03-16 21:35:35 +00:00: Moved the failed B1 stub into `workstream/200_inprogress/codex/` and rewrote it to the required lifecycle template.
- 2026-03-16 21:35:35 +00:00: Authored the B1 market configuration specification, a launch-oriented listing template, and a machine-readable JSON schema in the epic output folder.
- 2026-03-16 21:35:35 +00:00: Ran JSON validation and field coverage checks, then prepared the task for completion archival.
- 2026-03-16 21:42:42 +00:00: Recorded passing validation output and closed the lifecycle item for archival into `workstream/300_complete/codex/`.

## Changes Made
- Created `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b1_perpetual_instrument_market_configuration_model.md`
  - Defined the canonical per-market configuration model.
  - Added required fields for trading engine, risk engine, funding, and transparency consumers.
  - Added operator rules, lifecycle statuses, and a worked phase-1 listing strategy.
- Created `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b1_perpetual_market_listing_template.json`
  - Added a concrete template containing four phase-1 instruments: `SFX_NGN_PERP`, `SFX_KES_PERP`, `SFX_GHS_PERP`, and `SFX_ZAR_PERP`.
  - Included stablecoin collateral, isolated margin, index references, leverage bands, position caps, vault scoping, and publication fields.
- Created `ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b1_perpetual_market_configuration_schema.json`
  - Added a draft-07 JSON schema for machine validation of listing packs.
  - Enforced required fields, enums, and nested structure for pricing, risk, funding, transparency, and governance controls.

## Validation
- `Test-Path 'workstream\200_inprogress\codex\20260313_220631_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_define_perpetual_instrument_and_market_configuration_model.md'`
  - Result: `True`
- `Test-Path 'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_instrument_market_configuration_model.md'`
  - Result: `True`
- `Test-Path 'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_market_listing_template.json'`
  - Result: `True`
- `Test-Path 'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2\workstreams\B\b1_perpetual_market_configuration_schema.json'`
  - Result: `True`
- `python -c "import json, pathlib; base = pathlib.Path(r'ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B'); json.load(open(base / 'b1_perpetual_market_listing_template.json')); json.load(open(base / 'b1_perpetual_market_configuration_schema.json')); print('json_ok')"`
  - Result: `json_ok`
- `rg -n "quote_collateral|isolated_margin|index_reference|transparency_fields|position_size_cap|vault_id" ep_003_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2/workstreams/B/b1_perpetual_instrument_market_configuration_model.md`
  - Result: Matching lines confirm coverage of margining, isolation, references, caps, vault linkage, and transparency fields.

## Risks/Notes
- Upstream A1 and A3 design artifacts are not yet present in the epic output folder. The B1 model therefore fixes interface shapes and assumptions from the epic, but index field names and smoothing metadata may need a follow-up alignment pass once A1/A3 are authored.
- `Auto-Acceptance` remains `false` because the dependency gap means a manual review should confirm the provisional index-reference structure still matches future A1/A3 outputs.
- No runtime code changes were required for this task; the deliverable is a design/package artifact set under the epic output folder.

## Completion Status
Complete and validated on 2026-03-16 21:42:42 +00:00. Archived to `workstream/300_complete/codex/20260313_220631_synthetic_frontier_sfx_derivatives_market_technical_design_brief_v2_workstreamB_define_perpetual_instrument_and_market_configuration_model.md`.
