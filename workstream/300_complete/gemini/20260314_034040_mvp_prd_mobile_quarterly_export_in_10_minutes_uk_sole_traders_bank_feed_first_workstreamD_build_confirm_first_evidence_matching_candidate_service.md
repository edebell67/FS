# TASK D2: Build confirm-first evidence matching candidate service

**Workstream:** D — Evidence Matching
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 2
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [x] Complete
**Workstream Goal:** Allow optional receipt evidence to be captured, extracted, and matched to bank transactions without ever becoming an export blocker.

---

## Purpose

Rank top bank transaction candidates for a piece of evidence using the matching logic described in the epic while preserving user confirmation as the final step.

## Input

A4 bank transactions, D1 extracted evidence metadata, and epic matching criteria.

## Output

Matching service that returns top 3 candidate bank transactions with reason chips and confidence metadata.

## Fields / Components

- candidate_rank
- bank_txn_id
- amount_match
- date_proximity
- merchant_similarity
- link_confidence

## Dependencies

- A4
- D1

## Action

Implement candidate scoring using amount, date proximity, and fuzzy merchant matching, then return the three best matches with explanations suitable for UI presentation.

## Verification

- [x] The service returns at most three ranked candidates for a given evidence item.
  - Test: \
ode solution/backend/src/testing/testEvidenceMatching.js\
  - Evidence: All scenarios passed, max 3 candidates returned.
- [x] Returned candidates include merchant, date, amount, and human-readable match reasons.
  - Test: Inspected JSON output in \	estEvidenceMatching.js\.
  - Evidence: \merchant\, \date\, \mount\, and \easons\ fields present.
- [x] No automatic link is created without explicit user confirmation.
  - Test: Verified \ankCandidates\ only returns data; \confirmMatch\ requires separate call.
  - Evidence: Logic in \evidenceMatchingService.js\ confirms separation.
- [x] No-match scenarios are supported without generating blockers or errors.
  - Test: Scenario 4 in \	estEvidenceMatching.js\.
  - Evidence: Correctly returns empty array for outlier evidence.

---

## Implementation Log
- 2026-03-27 01:13: Created plan \20260327_0113_V20260327_0115_build_confirm_first_evidence_matching_candidate_service.md\.
- 2026-03-27 01:15: Updated \evidenceMatchingService.js\ to include flattened fields and refined scoring logic.
- 2026-03-27 01:15: Updated \	estEvidenceMatching.js\ to verify new fields.
- 2026-03-27 01:16: Ran tests and verified successful output.
- 2026-03-27 01:16: Updated \Constants.py\ version to \V20260327_0115\.

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: \
ode solution/backend/src/testing/testEvidenceMatching.js\ output.
  - Objective-Proved: Technical correctness of matching logic and field adherence.
  - Status: captured

## Completion Status
COMPLETE - 2026-03-27 01:17

---

## Notes

- Generated from source epic: \workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md\
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
