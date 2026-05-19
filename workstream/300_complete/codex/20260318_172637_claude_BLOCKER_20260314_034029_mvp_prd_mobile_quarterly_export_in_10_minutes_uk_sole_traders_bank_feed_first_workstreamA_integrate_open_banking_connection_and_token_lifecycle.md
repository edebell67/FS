Source: `C:\Users\edebe\eds\workstream\300_complete\20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md`
Task Type: standard
Task Attributes:
- `recurring_task: false`
- `looping_task: false`
- `splittable_task: false`
- `workflow_task: false`
Task Summary: Resolve the blocker entry for Open Banking connection lifecycle by validating the prior implementation, aligning it to the canonical BankAccount schema, hardening consent/token/reconnect behavior, and recording completion evidence in the lifecycle file.
Context:
- Epic solution: `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend`
- Services: `src\services\openBankingAdapter.js`, `src\services\bankConnectionService.js`, `src\services\bankAccountService.js`
- Schema/migrations: `src\models\mvp_domain_schemas.json`, `src\models\bank_connection_tokens_migration.sql`
- Verification entrypoint: `verify_bank_connection.js`
Dependency: `A1 schemas` and `A2 onboarding flow` were already completed upstream; this blocker resolution depends on those artifacts only.

Plan:
- [x] 1. Audit the existing blocker resolution artifacts against the canonical MVP schema and determine whether the implementation is present and valid.
  - [x] Test: `Get-Content workstream\300_complete\gemini\20260318_172637_claude_BLOCKER_20260314_034029_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamA_integrate_open_banking_connection_and_token_lifecycle.md` and inspect the referenced backend files for actual presence.
  - [x] Evidence: Confirmed the implementation files existed under `epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend`, but the active `200_inprogress\codex` task file was still a stub and the token migration/service used non-canonical `id` references.
- [x] 2. Harden the Open Banking consent, callback, token storage, and reconnect logic to match the canonical schema and read-only consent rules.
  - [x] Test: Review the patched service and migration files and ensure `bank_account_id` / `last_synced_at` / read-only scope validation are implemented consistently.
  - [x] Evidence: Updated `src\services\openBankingAdapter.js`, `src\services\bankConnectionService.js`, `src\services\bankAccountService.js`, `src\models\bank_connection_tokens_migration.sql`, and `package.json` with schema-aligned persistence, state validation, token redaction, refresh handling, reconnect handling, and a dedicated verification script entry.
- [x] 3. Run technical validation proving connection creation, read-only scope enforcement, refresh handling, reauth fallback, reconnect recovery, and sync timestamp updates.
  - [x] Test: `node validate_mvp_domain_schemas.js`
  - [x] Evidence: Output was `mvp_domain_schema_ok`, `entities=10`, `category_codes=18`, `transaction_fields=14`, `evidence_fields=10`, `summary_fields=8`.
- [x] 4. Run end-to-end bank connection verification and capture proof for the lifecycle record.
  - [x] Test: `node verify_bank_connection.js`
  - [x] Evidence: Output included `VERIFICATION PASSED` plus a redacted final account/token snapshot showing two connected accounts, read-only scopes (`accounts`, `transactions`, `offline_access`), reconnect recovery, and `last_synced_at` updated to `2026-03-21T12:00:00.000Z`.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\openBankingAdapter.js`
  - Objective-Proved: Consent requests now reject over-privileged scopes and only generate read-only authorization payloads.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\bankConnectionService.js`
  - Objective-Proved: Token storage, expiry checks, refresh behavior, redaction, reconnect failure handling, and sync-status updates are implemented against canonical bank-account keys.
  - Status: captured
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\bankAccountService.js`
  - Objective-Proved: Callback handling validates state, persists canonical BankAccount records, avoids raw token leakage, and supports reconnect without duplicating account identity.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\models\bank_connection_tokens_migration.sql`
  - Objective-Proved: Token storage now references `bank_accounts(bank_account_id)` instead of a non-canonical `id` column.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `node validate_mvp_domain_schemas.js`
  - Objective-Proved: The backend solution still satisfies the canonical MVP schema contract after the Open Banking changes.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `node verify_bank_connection.js`
  - Objective-Proved: The Open Banking lifecycle works end-to-end for consent URL generation, callback persistence, refresh, reauth-required fallback, reconnect, and sync timestamp updates.
  - Status: captured

Implementation Log:
- 2026-04-01 16:47: Read `skills/workstream-task-lifecycle/SKILL.md` and the requested blocker file, then traced the referenced original task and prior result artifacts.
- 2026-04-01 16:51: Located the actual implementation in `epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend` and audited it against the canonical `mvp_domain_schemas.json`.
- 2026-04-01 16:57: Identified schema drift in the Open Banking files: token FK referenced `bank_accounts(id)`, refresh failure updated `WHERE id = ...`, and the blocker lifecycle entry had never been updated from its stub state.
- 2026-04-01 17:01: Reworked the Open Banking services to enforce read-only scopes, normalize/redact token records, validate callback state, persist canonical bank-account rows, and support reconnect/sync lifecycle updates.
- 2026-04-01 17:05: Replaced the lightweight verification with an assertion-based end-to-end script covering consent, callback, refresh, reauth-required, reconnect, and sync timestamp transitions.
- 2026-04-01 17:06: Ran schema validation and Open Banking verification successfully, then updated this lifecycle file for completion.
- 2026-04-01 18:01: Re-ran the recorded backend validations from the solution directory, confirmed both still pass unchanged, and prepared the duplicate `200_inprogress` task record to be collapsed into a single `300_complete` lifecycle file.

Changes Made:
- Replaced `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\bankConnectionService.js`.
- Replaced `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\bankAccountService.js`.
- Updated `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\services\openBankingAdapter.js`.
- Updated `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\src\models\bank_connection_tokens_migration.sql`.
- Replaced `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\verify_bank_connection.js`.
- Updated `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend\package.json` to expose `verify:bank-connection`.

Validation:
- 2026-04-01: Ran `node validate_mvp_domain_schemas.js` from `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend`.
  - Result: Passed with `mvp_domain_schema_ok`, `entities=10`, `category_codes=18`, `transaction_fields=14`, `evidence_fields=10`, `summary_fields=8`.
- 2026-04-01: Ran `node verify_bank_connection.js` from `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend`.
  - Result: Passed with `VERIFICATION PASSED`.
  - Result: Output showed a consent URL with `consent_mode=read_only`, two connected bank accounts, redacted tokens, successful reconnect, and `last_synced_at` set.
- 2026-04-01 18:01: Re-ran `node validate_mvp_domain_schemas.js` from `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend`.
  - Result: Passed again with `mvp_domain_schema_ok`, `entities=10`, `category_codes=18`, `transaction_fields=14`, `evidence_fields=10`, `summary_fields=8`.
- 2026-04-01 18:01: Re-ran `node verify_bank_connection.js` from `C:\Users\edebe\eds\epics\ep_004_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first\solution\backend`.
  - Result: Passed again with `VERIFICATION PASSED`.
  - Result: Output again showed `consent_mode=read_only`, encrypted/redacted tokens, two connected accounts, reconnect success, and `last_synced_at=2026-03-21T12:00:00.000Z`.

Risks/Notes:
- Provider API calls remain mocked in `openBankingAdapter.js`; production rollout still requires wiring the real Open Banking provider exchange/refresh/account endpoints.
- `upsertBankAccount` assumes a supporting unique constraint for `(user_id, provider_name, provider_account_id)` in the target database. The service logic is written for that invariant, but the migration establishing the unique index is outside this blocker scope.
- This is a backend-only task, so the completion gate did not require interactive user verification.

Completion Status: COMPLETE - 2026-04-01 18:01
