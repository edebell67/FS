# Source
- User request: generate a complete checklist with tests to fully deliver the pivot to `workstream/000_backlog/mvp_prd_quarterly_export_10min.md`.

# Task Summary
Create an implementation delivery checklist with explicit tests covering all MVP PRD requirements for inbox-driven categorization and quarterly export flow.

# Context
- Existing system: `C:\Users\edebe\eds\bizPA`
- Target PRD: `C:\Users\edebe\eds\workstream\000_backlog\mvp_prd_quarterly_export_10min.md`

# Plan
- [x] 1. Extract deliverables from the PRD into workstreams.
  - [x] Test: Ensure checklist spans scope/in-scope features, data model, NFRs, and acceptance tests.
  - [x] Evidence: Checklist sections include ingestion, inbox triage, blockers/readiness, evidence matching, voice, export, security, performance, QA.
- [x] 2. Produce full checklist with explicit test for each item.
  - [x] Test: Every checklist line has a clear verification command/manual test with pass criteria.
  - [x] Evidence: Generated checklist uses step + test format for each line item.

# Implementation Log
- 2026-03-05 19:16:57 Created task file.
- 2026-03-05 19:17:10 Produced complete delivery checklist and tests for PRD pivot.

# Changes Made
- Added delivery checklist in this lifecycle file.

## Delivery Checklist (Pivot to Quarterly Export MVP)

### A) Product Scope & Guardrails
- [ ] 1. Add explicit product mode flag: `MVP_QUARTERLY_EXPORT_MODE` to disable out-of-scope modules (VAT filing, invoicing workflows beyond export prep, landlord/payroll features).
  - [ ] Test: Start app with mode ON; UI and routes for out-of-scope capabilities are hidden/disabled; pass if no blocked route can be invoked.
- [ ] 2. Add legal disclaimer: "Not tax advice; user responsible; no HMRC submission" on onboarding + export confirmation.
  - [ ] Test: Manual UI check on onboarding and export screens; pass if disclaimer text is visible in both locations.

### B) Data Model & Migrations
- [ ] 3. Create `bank_accounts` entity with provider metadata and connection status.
  - [ ] Test: Run migration + insert/select smoke test; pass if one account record can be created and retrieved.
- [ ] 4. Create `bank_transactions` entity with idempotency key (`bank_txn_ref` + `bank_account_id`) and required fields.
  - [ ] Test: Import same feed twice; pass if duplicate rows are not created.
- [ ] 5. Create `transaction_classifications` with fields: category_code, business_personal, is_split, split_business_pct, confidence.
  - [ ] Test: Update classification for a transaction; pass if latest values persist and load via API.
- [ ] 6. Create `transaction_audit_log` (changed_at/by, previous_value, new_value).
  - [ ] Test: Apply two edits to one transaction; pass if two audit rows exist with old/new payloads.
- [ ] 7. Create `evidence` and `evidence_links` tables with user_confirmed flag + confidence.
  - [ ] Test: Link evidence to txn then unset; pass if link lifecycle is recorded and queryable.
- [ ] 8. Create `quarters` and `quarter_metrics` materialization model.
  - [ ] Test: Seed quarter and run metrics recompute; pass if total/blocking/readiness are populated.
- [ ] 9. Create `rules` table for merchant auto-categorization defaults.
  - [ ] Test: Add rule "Always categorize X as Y"; pass if next import auto-suggests Y.

### C) Ingestion & Inbox Pipeline
- [ ] 10. Build Open Banking connector abstraction (provider-agnostic, read-only).
  - [ ] Test: Mock provider pull endpoint; pass if adapter returns normalized transaction payload.
- [ ] 11. Implement ingestion job with cursor/since token and retry/idempotency.
  - [ ] Test: Simulate timeout + retry; pass if final state has no duplicates and checkpoint advances once.
- [ ] 12. Build normalization mapper into canonical `bank_transactions` schema.
  - [ ] Test: Feed mixed merchant/amount/date formats; pass if canonical records validate schema.
- [ ] 13. Build inbox API returning only unresolved/triage-relevant transactions with sort order.
  - [ ] Test: Call inbox endpoint with seeded resolved/unresolved data; pass if only unresolved items are returned in expected order.

### D) Categorization & Triage Actions
- [ ] 14. Implement category taxonomy (codes from PRD) as server-enforced enum/config.
  - [ ] Test: Attempt invalid category code write; pass if API rejects with validation error.
- [ ] 15. Implement business/personal action toggle.
  - [ ] Test: Toggle both states on a txn; pass if persisted and reflected in blocking evaluation.
- [ ] 16. Implement split action (requires 0-100 business %).
  - [ ] Test: Submit split without percent; pass if validation blocks and item remains blocking.
- [ ] 17. Implement duplicate resolution actions (dismiss/merge reference).
  - [ ] Test: Mark duplicate unresolved then resolve; pass if blocker count decreases by one.
- [ ] 18. Implement one-tap undo for last triage action.
  - [ ] Test: Apply action then undo; pass if state and audit trail show exact rollback.

### E) Blocking Engine & Quarter Readiness
- [ ] 19. Implement blocker predicate exactly per PRD rules.
  - [ ] Test: Unit-test matrix across all rule combinations; pass if expected blocking state matches 100% of cases.
- [ ] 20. Implement readiness metrics: total, blocking, readiness_pct formula.
  - [ ] Test: Seed known dataset (e.g., 200 total, 8 blocking); pass if API returns 96% readiness and 8 left.
- [ ] 21. Implement ordered Finish Now queue: uncategorized -> personal missing -> split missing -> duplicates.
  - [ ] Test: Seed one of each blocker type; pass if queue order matches specification.
- [ ] 22. Gate export action on `blocking_txns_count == 0`.
  - [ ] Test: Try export with one blocker; pass if API returns blocked status with reason.

### F) Evidence Capture & Matching
- [ ] 23. Implement evidence upload/capture endpoint and storage metadata.
  - [ ] Test: Upload image/PDF; pass if evidence row + storage reference created.
- [ ] 24. Implement extraction pipeline (amount/date/merchant best-effort).
  - [ ] Test: Run extractor on sample receipt set; pass if fields are extracted for >= agreed threshold sample.
- [ ] 25. Implement candidate matching engine (amount/date window/fuzzy merchant) and top-3 ranking.
  - [ ] Test: Seed deterministic fixtures; pass if expected top candidate appears rank #1.
- [ ] 26. Implement mandatory user-confirmation sheet (Match 1/2/3 or No match/Later).
  - [ ] Test: Attempt auto-link without user action; pass if system prevents confirmed link until user selection.
- [ ] 27. Mark evidence as non-blocking in export readiness logic.
  - [ ] Test: Unmatched evidence present + zero tx blockers; pass if export remains enabled.

### G) Voice Micro-Decisions
- [ ] 28. Implement supported intent set only: Category, Business/Personal, Split n%, Attach receipt, Match first/second/third, No match.
  - [ ] Test: Intent contract tests for each utterance pattern; pass if expected action payload emitted.
- [ ] 29. Bind voice commands to current inbox/queue context item safely.
  - [ ] Test: Speak command with no selected context; pass if app asks for selection and applies nothing.
- [ ] 30. Add post-action confirmation chip with combined applied actions.
  - [ ] Test: Execute 3 voice actions; pass if chip shows all and can be tapped to edit/undo.
- [ ] 31. Track voice success metric (intent applied without manual correction).
  - [ ] Test: Analytics event replay test; pass if dashboard computes success rate from events.

### H) Quarter Export Pack
- [ ] 32. Implement `Transactions.csv` exact column contract.
  - [ ] Test: Schema assertion test against generated CSV header/order/types; pass if exact match.
- [ ] 33. Implement `EvidenceIndex.csv` export even when empty.
  - [ ] Test: Export quarter with no evidence; pass if file exists with headers only.
- [ ] 34. Implement `QuarterlySummary.csv` aggregated by category.
  - [ ] Test: Seed known totals; pass if per-category totals/counts/unresolved match expected values.
- [ ] 35. Implement `QuarterlyPack.pdf` (1–2 pages with readiness/totals/audit/evidence coverage).
  - [ ] Test: Render PDF and parse text snapshot; pass if required sections are present.
- [ ] 36. Implement pack bundling + download endpoint (zip with 4 artifacts).
  - [ ] Test: Download and inspect archive; pass if exactly 4 files with non-zero size (except empty EvidenceIndex allowed data-empty).

### I) UX Flows
- [ ] 37. Build Quarter screen with readiness headline and items-left counter.
  - [ ] Test: UI e2e check with seeded quarter; pass if text reflects backend metrics.
- [ ] 38. Build Finish Now queue screen with quick actions and voice entry.
  - [ ] Test: Resolve all queue items manually/voice; pass if queue reaches zero and exits cleanly.
- [ ] 39. Build Inbox screen optimized for 1–2 minute triage loops.
  - [ ] Test: Usability run (10 items); pass if median resolve time per item meets target baseline.
- [ ] 40. Add merchant rule creation affordance from corrected categorization action.
  - [ ] Test: Choose "always categorize" after manual override; pass if future matching applies rule.

### J) Security, Compliance, and Reliability
- [ ] 41. Harden token/credential storage and rotate secrets into env/vault only.
  - [ ] Test: Secret scan + config audit; pass if no secrets present in repo-tracked files.
- [ ] 42. Enforce encryption in transit and at rest policy for stored files/DB connection.
  - [ ] Test: Runtime config check; pass if TLS enabled and storage encryption policy documented/applied.
- [ ] 43. Add idempotent ingestion guardrails and operational alerts.
  - [ ] Test: Replay identical webhook/import batch; pass if transaction counts remain stable and alerting remains green.
- [ ] 44. Add resilience for offline/temporary network loss in inbox actions.
  - [ ] Test: Disable network mid-triage and recover; pass if queued actions sync without data loss.

### K) Performance & Telemetry
- [ ] 45. Instrument quarter-close funnel timing (open quarter -> export generated).
  - [ ] Test: Synthetic run emits start/end events; pass if median duration metric is queryable.
- [ ] 46. Measure and optimize inbox load to <2s typical device.
  - [ ] Test: Performance test on representative dataset; pass if p50 <2s and p95 within agreed bound.
- [ ] 47. Instrument export completion rate and blocker count trend KPI.
  - [ ] Test: KPI dashboard query test; pass if metrics populate from event + DB sources.

### L) QA, UAT, and Acceptance
- [ ] 48. Create unit tests for blocker engine, readiness formula, matching ranker, and CSV builders.
  - [ ] Test: CI unit suite; pass if all target modules covered and green.
- [ ] 49. Create integration tests for ingestion->inbox->finish now->export happy path.
  - [ ] Test: End-to-end test run with seeded quarter; pass if export enabled only at zero blockers.
- [ ] 50. Execute PRD acceptance tests exactly as specified.
  - [ ] Test: Manual + automated acceptance report; pass if all five acceptance criteria are green.
- [ ] 51. Run pilot with 3-5 realistic trader datasets and capture defects.
  - [ ] Test: Pilot sign-off checklist; pass if P0/P1 issues resolved or explicitly waived.

### M) Release Readiness
- [ ] 52. Produce migration and rollback runbook for production rollout.
  - [ ] Test: Dry-run migration/rollback in staging; pass if both complete without data integrity loss.
- [ ] 53. Finalize API contract docs and accountant handoff guide for quarterly pack.
  - [ ] Test: Doc review with engineering + accounting stakeholder; pass if approved.
- [ ] 54. Gate release on KPI smoke baseline (10-min close path, voice success, export correctness).
  - [ ] Test: Pre-release go/no-go checklist; pass if all gates meet thresholds.

# Validation
- Command: `Get-Content C:\Users\edebe\eds\workstream\000_backlog\mvp_prd_quarterly_export_10min.md`
- Result: requirements consumed and checklist produced.

# Risks/Notes
- Full delivery depends on resolving doc-code drift (existing bizPA modules vs narrowed MVP scope).
- Existing endpoints/features outside MVP should be feature-flagged, not necessarily deleted, during pivot.

# Completion Status
- Complete (2026-03-05 19:17:10).
