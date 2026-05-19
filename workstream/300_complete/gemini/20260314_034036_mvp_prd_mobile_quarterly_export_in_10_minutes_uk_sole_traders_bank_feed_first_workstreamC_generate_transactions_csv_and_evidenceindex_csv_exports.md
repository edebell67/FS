# TASK C2: Generate Transactions.csv and EvidenceIndex.csv exports

**Workstream:** C — Quarter Close And Export
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Convert classified transaction data into a quarter-close workflow and accountant-friendly export pack with immediate export enablement once blockers reach zero.

---

## Purpose

Produce the detailed accountant-facing CSV exports that carry quarter transaction traceability and evidence linkage.

## Input

A1 export contracts, B1 classifications, C1 quarter metrics, and D3 confirmed evidence links when available.

## Output

Transactions.csv and EvidenceIndex.csv generation service that emits valid files for the selected quarter, including empty EvidenceIndex.csv when needed.

## Fields / Components

- txn_id
- date
- merchant
- amount
- direction
- category_code
- category_name
- confidence
- business_personal
- is_split
- split_business_pct
- matched_evidence_ids
- bank_account_id
- bank_txn_ref
- evidence_id
- type
- captured_at
- doc_date
- storage_link
- extraction_confidence
- matched_bank_txn_id
- user_confirmed

## Dependencies

- C1

## Action

Build CSV serializers, field mapping, null-handling, ordering, and export packaging for transaction and evidence index outputs.

## Verification

- [ ] Transactions.csv contains every field required by the epic in a stable, documented order.
- [ ] EvidenceIndex.csv is exported even when no evidence exists for the period.
- [ ] Matched evidence identifiers and confirmed bank transaction links are preserved accurately.
- [ ] CSV totals and record counts reconcile with quarter transaction selection.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
