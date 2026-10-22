# EP047 — Branded verification-email delivery test procedure

## Preconditions
- A verification delivery is only prepared in the admin UI; this procedure does not send email.
- Use a valid business name, canonical listing URL, verification capability URL and expiry.

## Acceptance checks
1. Render verification template.
2. Assert the The Tech Principle header and service tag render.
3. Assert the branded Review and correct details CTA targets the verification capability URL.
4. Assert the plain-text fallback retains the review instruction and URL.
5. Run focused delivery tests, full suite, typecheck and production build.
6. Deploy and verify the hosted revision. Do not report recipient delivery without a separate intentional send and recipient-side evidence.
