# SUB-TASK A3.1: Define Open Banking consent contract and provider scope configuration

**Parent Task:** A3
**Workstream:** A — Bank Feed And Data Foundation
**Priority:** 1
**Source:** C:\Users\edebe\eds\workstream\100_backlog\20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md
**UI Deliverable:** No
**Status:** [ ] Not Started

---

## Purpose

Establish the provider-specific request contract for initiating a read-only bank connection with only the MVP permissions required.

## Input

A1 schemas, A2 onboarding flow entry points, in-scope provider requirements, and MVP read-only permission rules.

## Output

A consent configuration module and initiation contract that produces provider-ready connection requests limited to read-only scopes.

## Action

1. Map the MVP-required banking capabilities to explicit provider scopes and permissions.
2. Define the internal consent request payload and validation rules used by the onboarding flow.
3. Implement the provider initiation adapter that translates internal consent requests into provider-specific authorization parameters.
4. Ensure the adapter excludes write/payment scopes and any non-MVP permissions.
5. Add tests for allowed scopes, rejected invalid scope combinations, and generated provider request payloads.

## Verification

- [ ] Consent initiation requests include only read-only banking permissions required for transaction access.
- [ ] Invalid or over-privileged scope combinations are rejected before calling the provider.
- [ ] Generated provider authorization parameters are stable and sufficient for the onboarding flow to launch the connection process.

---

## Notes

- Generated via extended decomposition from parent task: `A3`
- This sub-task should be independently implementable.


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:30
