# EP047 real-prospect verification delivery policy — 2026-08-10 12:50:03 UTC

## Change
Replaced the temporary `VERIFICATION_RECIPIENT_ALLOWLIST` gate with the selected business's current recorded email address. The recipient is read-only in the admin panel; preparation derives it server-side and sending rechecks it before Gmail handoff. Explicit administrator confirmation, Gmail OAuth, fixed sender, expiry/token checks, sent-folder readback, and delivery audit remain mandatory.

## Results
- Focused verification regression: **PASS** — 18/18 tests.
- Typecheck: **PASS**.
- Production build: **PASS** (one pre-existing BusinessMap hook-dependency warning).
- Full `npm test`: **BLOCKED by unrelated pre-existing/concurrent UI test failure**: `tests/claim-approval.test.ts` expects `/directoryadmin/claims` in `components/layout/SiteHeader.tsx`; SiteHeader had already been changed to use `AdminMenuModal`. This change does not modify either file.
- Render configuration: **PASS** — removed `VERIFICATION_RECIPIENT_ALLOWLIST`; verified absent afterwards.

## Deferred end-to-end recipient test
No external email was sent during this release. It requires the authenticated admin's explicit single-send confirmation from the live business page, then Sent-folder, recipient-mailbox, and link-use verification.
