# EP047 public claim verification gate — 2026-08-10 13:24:55 UTC

- RED: `tests/public-claim-verification-gate.test.ts` failed because the eligibility module did not exist.
- GREEN: two eligibility tests passed: validation, pending, sent, opened, null and claimed stages are blocked; only `verification_completed` is allowed.
- Typecheck: PASS.
- Production build: PASS (existing BusinessMap hook dependency warning).
- Full suite: 165/166 passed. The sole failure is pre-existing/concurrent `claim-approval.test.ts` expecting the old claims link in `SiteHeader.tsx`; the header now delegates admin navigation to `AdminMenuModal`. This change does not edit that header or test.
- Browser state prior to deployment: public 11th Hour listing visibly exposed enabled claim control while `Verification Email Pending`; this is the reproduced defect.
