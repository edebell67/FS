# TASK D2: Build confirm-first evidence matching candidate service

**Workstream:** D — Evidence Matching
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 2
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [ ] Not Started
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

- [ ] The service returns at most three ranked candidates for a given evidence item.
- [ ] Returned candidates include merchant, date, amount, and human-readable match reasons.
- [ ] No automatic link is created without explicit user confirmation.
- [ ] No-match scenarios are supported without generating blockers or errors.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
