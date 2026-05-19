# TASK D2: Build Readiness Drill Down And Resolution Linking

**Workstream:** D — Tax Readiness Engine
**Epic:** bizPA MVP Product Requirements Document
**Priority:** 1
**Source Epic Path:** workstream/epic/bizPA.md
**Suggested Agent:** codex
**UI Deliverable:** No
**Status:** [x] Complete
**Workstream Goal:** Continuously calculate an explainable quarter-readiness score for the active quarter only.

---

## Purpose

Expose the missing-percentage breakdown so users can inspect issues and navigate directly to the relevant fix flow.

## Input

Readiness engine from D1 and entity/inbox routes from C2 to C4.

## Output

Issue breakdown service, actionable issue list, and linking from each issue to the related record or correction flow.

## Fields / Components

- issue_type
- affected_entity_id
- severity
- weight
- resolution_target
- explanation

## Dependencies

- D1
- C3
- C4

## Action

Implement the issue drill-down layer that groups active-quarter readiness problems and links each item to the exact record or workflow needed to resolve it.

## Verification

- [ ] Every readiness issue includes an explanation and a valid navigation target.
- [ ] Drill-down only reports on the active quarter and excludes stored historical snapshots.
- [ ] Resolving a sample issue updates the readiness breakdown on recalculation.

---

## Notes

- Generated from source epic: `workstream/epic/bizPA.md`
- This task is intended for Epic Review allocation before execution.

## Source

- `workstream/epic/bizPA.md`

## Task Summary

Extend the MVP readiness API so it returns an explainable active-quarter issue drill-down, with grouped issue metrics, actionable issue rows, and stable navigation targets for the existing inbox correction flows.

## Context

- Backend readiness logic: `bizPA/backend/src/services/readinessService.js`
- Inbox API/controller surface: `bizPA/backend/src/controllers/inboxController.js`, `bizPA/backend/src/routes/inboxRoutes.js`
- Quarterly event logging and quarter helpers: `bizPA/backend/src/services/businessEventLogService.js`
- Existing quarterly smoke verification: `bizPA/backend/verify_mvp_quarterly_flow.js`

## Plan

- [x] 1. Define active-quarter issue drill-down payload shape in the readiness service and controller, including explanations, severities, weights, and resolution targets.
  - [x] Test: `node -e "const { buildReadinessReport } = require('./src/services/readinessService'); const report = buildReadinessReport({ asOfDate: '2026-03-11', transactions: [{ id: 'txn-1', txn_date: '2026-03-10', merchant: 'Fuel Stop', amount: 42.5, direction: 'out' }, { id: 'txn-2', txn_date: '2025-12-15', merchant: 'Old Expense', amount: 18, direction: 'out' }] }); if (!report.issue_summary || !Array.isArray(report.issue_list) || report.issue_list.length !== 1 || report.issue_list[0].resolution_target?.kind !== 'transaction_classification') { throw new Error('issue drill-down payload missing expected active-quarter issue data'); } console.log('readiness_drilldown_shape=PASS');"`
  - Evidence: 2026-03-11 16:33 Europe/London: Command returned `readiness_drilldown_shape=PASS`, confirming `issue_summary`, active-quarter filtering, and a valid classification navigation target.
- [x] 2. Enforce active-quarter scoping in the readiness endpoint and add non-DB verification coverage for recalculation behavior after resolving a sample issue.
  - [x] Test: `node verify_readiness_drilldown.js`
  - Evidence: 2026-03-11 16:35 Europe/London: Command returned `verify_readiness_drilldown=PASS`, confirming active-quarter filtering, issue explanations/targets, and readiness recalculation after sample issue resolution.
- [x] 3. Update quarterly verification and repository docs/task narrative to reflect the new drill-down contract and captured validation evidence.
  - [x] Test: `node -e "const fs = require('fs'); const verify = fs.readFileSync('./verify_mvp_quarterly_flow.js', 'utf8'); const docs = fs.readFileSync('../docs/api_endpoint_inventory.md', 'utf8'); if (!verify.includes('issue_list') || !verify.includes('quarter_reference') || !docs.includes('/api/v1/inbox/readiness') || !docs.includes('actionable issue list')) { throw new Error('readiness contract updates missing'); } console.log('readiness_contract_docs=PASS');"`
  - Evidence: 2026-03-11 16:38 Europe/London: Command returned `readiness_contract_docs=PASS`, confirming the quarterly smoke script and API inventory were updated for the new drill-down contract.

## Implementation Log

- 2026-03-11 16:20 Europe/London: Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned task brief, then traced the current readiness implementation in the BizPA backend.
- 2026-03-11 16:24 Europe/London: Confirmed `readinessService.js` currently returns only summary counts and blocking transactions, while `getReadiness` accepts arbitrary periods and does not expose drill-down navigation targets.
- 2026-03-11 16:28 Europe/London: Confirmed quarter helper support exists in `businessEventLogService.js`; reviewed the quarterly migration schema and existing `verify_mvp_quarterly_flow.js` harness to align the implementation and tests.
- 2026-03-11 16:33 Europe/London: Implemented issue metadata, active-quarter filtering, issue grouping/list generation, and actionable resolution targets in the readiness service/controller. Added `verify_readiness_drilldown.js` for local regression coverage.
- 2026-03-11 16:36 Europe/London: Updated `verify_mvp_quarterly_flow.js` to assert quarter enforcement and issue drill-down presence, and documented the readiness endpoints in `bizPA/docs/api_endpoint_inventory.md`.
- 2026-03-11 16:39 Europe/London: Ran syntax checks for all modified backend scripts. Attempted the live quarterly smoke script, which failed with `ECONNREFUSED` because no API server was listening on `127.0.0.1:5056` in this session; recorded the environment limitation below.

## Changes Made

- `bizPA/backend/src/services/readinessService.js`
  - Added issue metadata for blocker types, active-quarter derivation, issue summary generation, actionable issue rows, and response fields such as `quarter_reference`, `active_period_enforced`, `issue_summary`, and `issue_list`.
  - Preserved existing summary fields while enriching `blocking_transactions` with explanations and navigation targets.
- `bizPA/backend/src/controllers/inboxController.js`
  - Changed `/api/v1/inbox/readiness` to enforce active-quarter DB scoping from `as_of_date` and to emit readiness recalculation events with the enforced quarter bounds.
- `bizPA/backend/verify_readiness_drilldown.js`
  - Added a local verification script for active-quarter filtering, explanation/target presence, and recalculation after resolving sample issues.
- `bizPA/backend/verify_mvp_quarterly_flow.js`
  - Extended the live quarterly smoke script to assert active-quarter enforcement and issue drill-down contract fields when the API is running.
- `bizPA/docs/api_endpoint_inventory.md`
  - Added the inbox/readiness endpoints and documented that `/api/v1/inbox/readiness` returns actionable issue drill-down data for the enforced active quarter.

## Validation

- 2026-03-11 16:33 Europe/London: `node -e "const { buildReadinessReport } = require('./src/services/readinessService'); const report = buildReadinessReport({ asOfDate: '2026-03-11', transactions: [{ id: 'txn-1', txn_date: '2026-03-10', merchant: 'Fuel Stop', amount: 42.5, direction: 'out' }, { id: 'txn-2', txn_date: '2025-12-15', merchant: 'Old Expense', amount: 18, direction: 'out' }] }); if (!report.issue_summary || !Array.isArray(report.issue_list) || report.issue_list.length !== 1 || report.issue_list[0].resolution_target?.kind !== 'transaction_classification') { throw new Error('issue drill-down payload missing expected active-quarter issue data'); } console.log('readiness_drilldown_shape=PASS');"` -> PASS (`readiness_drilldown_shape=PASS`)
- 2026-03-11 16:35 Europe/London: `node verify_readiness_drilldown.js` -> PASS (`verify_readiness_drilldown=PASS`)
- 2026-03-11 16:38 Europe/London: `node -e "const fs = require('fs'); const verify = fs.readFileSync('./verify_mvp_quarterly_flow.js', 'utf8'); const docs = fs.readFileSync('../docs/api_endpoint_inventory.md', 'utf8'); if (!verify.includes('issue_list') || !verify.includes('quarter_reference') || !docs.includes('/api/v1/inbox/readiness') || !docs.includes('actionable issue list')) { throw new Error('readiness contract updates missing'); } console.log('readiness_contract_docs=PASS');"` -> PASS (`readiness_contract_docs=PASS`)
- 2026-03-11 16:39 Europe/London: `node --check .\\src\\services\\readinessService.js` -> PASS (no syntax errors)
- 2026-03-11 16:39 Europe/London: `node --check .\\src\\controllers\\inboxController.js` -> PASS (no syntax errors)
- 2026-03-11 16:39 Europe/London: `node --check .\\verify_readiness_drilldown.js` -> PASS (no syntax errors)
- 2026-03-11 16:39 Europe/London: `node --check .\\verify_mvp_quarterly_flow.js` -> PASS (no syntax errors)
- 2026-03-11 16:37 Europe/London: `node verify_mvp_quarterly_flow.js` -> FAIL (`verify_mvp_quarterly_flow=FAIL: connect ECONNREFUSED 127.0.0.1:5056`) because the local API server was not running in this session.

## Risks/Notes

- Existing frontend consumers only rely on summary readiness fields today; new drill-down data should be added without breaking the current response shape.
- The current API does not appear to persist quarter metrics snapshots for readiness; this task should avoid introducing historical snapshot coupling unless required for the active-quarter contract.
- Live end-to-end API smoke still depends on a running backend service and database. The contract script was updated, but the live command could not complete in this session because `127.0.0.1:5056` was unavailable.

## Completion Status

Complete as of 2026-03-11 16:39 Europe/London.
