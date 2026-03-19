# SUB-TASK A3.4: Establish connection status and reconnect lifecycle model

**Parent Task:** A3
**Workstream:** A — Bank Feed And Data Foundation
**Priority:** 4
**Source:** C:\Users\edebe\eds\workstream\100_backlog\20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md
**UI Deliverable:** No
**Status:** [ ] Not Started

---

## Purpose

Create a stable internal state machine for active, expired, revoked, and reconnect-required bank connections that downstream imports can rely on.

## Input

Persisted BankAccount records, token lifecycle service, provider error/expiry conditions, and downstream sync readiness requirements.

## Output

A connection status model plus service logic that updates connection_status and last_sync_at based on refresh results, revocations, and reconnect events.

## Action

1. Define the allowed connection states and transition rules for newly connected, active, expired, revoked, reconnect_required, and disconnected cases.
2. Implement status update logic driven by token refresh outcomes, provider authorization failures, and explicit reconnect actions.
3. Add service methods for marking successful sync readiness and updating last_sync_at when imports later run.
4. Implement reconnect handling that preserves account identity while reauthorizing credentials and restoring active status.
5. Add tests covering state transitions, revoked-token behavior, reconnect flow outcomes, and sync-readiness checks.

## Verification

- [ ] Connection status changes deterministically for valid, expired, revoked, and reconnect-required scenarios.
- [ ] Reconnect flows restore a previously broken connection without creating ambiguous duplicate account state.
- [ ] Stored account metadata and status fields are sufficient for later initial and incremental transaction sync orchestration.

---

## Notes

- Generated via extended decomposition from parent task: `A3`
- This sub-task should be independently implementable.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
