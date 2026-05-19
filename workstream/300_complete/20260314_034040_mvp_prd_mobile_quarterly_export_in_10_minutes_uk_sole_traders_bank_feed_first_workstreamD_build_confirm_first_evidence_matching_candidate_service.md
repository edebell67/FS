# TASK D2: Build confirm-first evidence matching candidate service

**Workstream:** D � Evidence Matching
**Epic:** MVP PRD � Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
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

## Dependency
Dependency: A4, D1

## Plan
- [x] 1. Define candidate ranking logic (Amount, Date, Merchant)
  - Test: Create mock evidence and transactions and verify ranking
  - Evidence: testEvidenceMatching.js output
- [x] 2. Implement Evidence Matching Service
  - Test: verify implementation handles amount tolerance, date window, and fuzzy merchant match
  - Evidence: src/services/evidenceMatchingService.js
- [x] 3. Verify rank candidates returns top 3 with reasons
  - Test: Run node testEvidenceMatching.js
  - Evidence: Scenario 1-5 passing in test output

## Evidence
- Objective-Delivery-Coverage: 100%
- Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: node src/testing/testEvidenceMatching.js
  - Objective-Proved: Service correctly ranks candidates and ignores non-matching directions/amounts.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: src/services/evidenceMatchingService.js
  - Objective-Proved: core logic implemented.
  - Status: captured

## Implementation Log
- 2026-03-22 18:30: Created `evidenceMatchingService.js` with Levenshtein-based fuzzy merchant matching and weighted scoring.
- 2026-03-22 18:35: Created `testEvidenceMatching.js` with 5 scenarios.
- 2026-03-22 18:45: Discovered Scenario 5 failing due to date-only matches meeting 0.2 threshold.
- 2026-03-22 18:50: Increased link_confidence threshold to 0.3 to ensure better quality candidates. Verified all scenarios pass.

## Changes Made
- Added `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\evidenceMatchingService.js`
- Added `C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\testing\testEvidenceMatching.js`

## Validation
Ran `node C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\testing\testEvidenceMatching.js`
All 5 scenarios passed:
1. Perfect Match (1.0 confidence)
2. Fuzzy Merchant Match
3. Close Match (Amount and Date only)
4. No Match (Outliers)
5. Direction Check (Ignore Income)

## Risks/Notes
- Weighted scoring: Amount (0.5), Merchant (0.3), Date (0.2).
- Threshold set to 0.3 to filter out weak "date-only" matches.

## Completion Status
Final state: Complete
Timestamp: 2026-03-22 19:00
