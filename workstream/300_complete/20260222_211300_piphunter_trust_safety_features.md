# Task: Trust & Safety - Critical Trust Features

## Task Summary
Implement trust validation logic and UI components: negative P&L block, minimum formulation, leadership gap, silent bucket, trust badge, transparency dashboard, audit log, and rules explainer.

## Context
- Source: spec Section 8 (Critical Trust Features)
- File: `app/services/trust.tsx` — shared validation + UI components
- Consumed by: battle.tsx, signalpro.tsx, and any promotion-related screen

## Implementation Log
- 2026-02-23 02:02: Moved to 200_inprogress
- 2026-02-23 02:03: Created `app/services/trust.tsx` with full trust module
- 2026-02-23 02:03: Implemented `validatePromotion()` — 4 checks (2 hard, 1 soft, 1 info)
- 2026-02-23 02:04: Built `TrustBadge` — green shield with VERIFIED label (full + compact)
- 2026-02-23 02:04: Built `NegativePnlBlock` — red bar shown when P&L < 0
- 2026-02-23 02:05: Built `TransparencyDashboard` — shows all checks with pass/fail + severity
- 2026-02-23 02:05: Built `AuditLog` — chronological decision log with color-coded actions
- 2026-02-23 02:06: Built `TrustRulesExplainer` — user-facing explanation of all 4 trust rules

## Changes Made
- `app/services/trust.tsx` — NEW FILE (280+ lines):
  - `TRUST_CONFIG` — configurable thresholds
  - `validatePromotion()` — returns {eligible, reason, checks[]} with 4 validation checks
  - `TrustBadge` — shield checkmark badge (compact or full)
  - `NegativePnlBlock` — red alert bar for negative P&L
  - `TransparencyDashboard` — visual checklist of all trust criteria
  - `AuditLog` — timestamped decision log (PROMOTED/BLOCKED/DEMOTED/SILENT)
  - `TrustRulesExplainer` — 4-rule explainer card with icons

## Validation
- `validatePromotion()` correctly blocks on negative P&L and insufficient trades
- Hard checks (P&L, formulation) prevent promotion regardless of other criteria
- Soft check (leadership gap) warns but is still required for full eligibility

## Risks/Notes
- Audit log storage is frontend-only (would need backend persistence)
- Trust metrics reporting not yet wired to analytics
- TRUST_CONFIG values are hardcoded — could be moved to API config

## Completion Status
Complete — 2026-02-23 02:07 UTC

## Sub-tasks
- [x] Implement negative P&L block (hard block, no override) — validatePromotion() check 1
- [x] Add visual indicator when leader is negative — NegativePnlBlock component
- [x] Enforce formulation requirement (min trades before eligible) — check 2, MIN_TRADES 5
- [x] Implement leadership gap validation — check 3, MIN_GAP 3%
- [x] Create "Silent Bucket" state for no qualified leader — NO_LEADER state in signalpro
- [x] Add trust badge/indicator for promoted signals — TrustBadge component
- [x] Implement transparency dashboard (why promoted/not promoted) — TransparencyDashboard
- [x] Create audit log for all promotion decisions — AuditLog component
- [x] Add user-facing explanation of trust rules — TrustRulesExplainer
- [ ] Implement trust metrics reporting — Requires analytics backend
