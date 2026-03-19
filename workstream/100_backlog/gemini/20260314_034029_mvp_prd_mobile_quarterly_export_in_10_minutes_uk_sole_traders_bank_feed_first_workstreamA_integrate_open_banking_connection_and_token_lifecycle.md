# TASK A3: Integrate Open Banking connection and token lifecycle

**Workstream:** A — Bank Feed And Data Foundation
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** gemini
**UI Deliverable:** No
**Status:** [ ] Not Started
**Workstream Goal:** Establish the canonical data contracts, audit fields, and import foundations needed by all downstream MVP flows.

---

## Purpose

Allow the user to connect a read-only bank feed using a provider-managed flow with secure credential and token handling.

## Input

A1 schemas, A2 onboarding flow, and epic in-scope Open Banking requirements.

## Output

Bank connection service, persisted BankAccount records, and secure token management for read-only transaction access.

## Fields / Components

- bank_account_id
- provider_account_ref
- access_scope
- connection_status
- last_sync_at

## Dependencies

- A1
- A2

## Action

Implement provider connection flow, store account metadata, secure refresh/access token handling, and a stable connection status model for later imports.

## Verification

- [ ] A connected account can be created and stored without exposing raw secrets in logs or client state.
- [ ] Token refresh and reconnect paths are handled for expired or revoked connections.
- [ ] Only read-only banking permissions are requested for the MVP flow.
- [ ] Connected account metadata is sufficient to start initial and incremental transaction syncs.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.


---

## Extended Decomposition

This task was decomposed into 4 sub-tasks on 2026-03-14T22:48:54.105920:
- A3.1: Define Open Banking consent contract and provider scope configuration
- A3.2: Implement connection callback handling and bank account record creation
- A3.3: Build secure token storage and refresh lifecycle service
- A3.4: Establish connection status and reconnect lifecycle model


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:27:30
