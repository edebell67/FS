# SUB-TASK A3.2: Implement connection callback handling and bank account record creation

**Parent Task:** A3
**Workstream:** A — Bank Feed And Data Foundation
**Priority:** 2
**Source:** C:\Users\edebe\eds\workstream\100_backlog\20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md
**UI Deliverable:** No
**Status:** [ ] Not Started

---

## Purpose

Convert a successful provider connection result into persisted internal bank account metadata records without exposing secrets.

## Input

Consent initiation contract from the previous sub-task, A1 bank account schema fields, provider callback payload shape, and persistence interfaces.

## Output

A connection callback service that exchanges provider callback data for linked account metadata and creates persisted BankAccount records.

## Action

1. Implement the callback endpoint or service handler that accepts the provider redirect/result payload.
2. Validate state, correlation identifiers, and required callback fields.
3. Exchange the callback authorization artifact for linked account details through the provider adapter.
4. Map returned account metadata into internal BankAccount records using bank_account_id, provider_account_ref, access_scope, connection_status, and last_sync_at.
5. Persist the records and sanitize logs and response payloads so raw tokens and secrets never enter logs or client state.
6. Add tests for successful account creation, duplicate callback handling, and secret redaction behavior.

## Verification

- [ ] A successful provider callback creates one or more persisted BankAccount records with the required metadata fields populated.
- [ ] No raw access tokens, refresh tokens, or provider secrets are written to logs, API responses, or client-visible state.
- [ ] Duplicate or malformed callback payloads fail safely without creating inconsistent account records.

---

## Notes

- Generated via extended decomposition from parent task: `A3`
- This sub-task should be independently implementable.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
