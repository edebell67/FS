# EP047 — Branded verification-email delivery

## Request
Verification emails must use the established The Tech Principle branded HTML system; basic HTML paragraphs and a plain-text admin preview are not sufficient.

## Scope
- Apply the shared brand shell to verification emails.
- Include an accessible branded **Review and correct details** CTA.
- Preserve the existing plain-text fallback, recipient/sender enforcement, explicit send confirmation, tracking pixel, and truthful delivery states.
- Do not send a real email as part of this implementation.

## Progress
- 2026-08-10 14:03:11 UTC — Task created in a clean release workspace at remote commit `179f51b`. Existing unrelated map and header work is excluded.
- 2026-08-10 14:03:11 UTC — RED: the branded-template test failed because verification HTML had no The Tech Principle shell or CTA.
- 2026-08-10 14:03:11 UTC — GREEN: added the shared brand shell to verification delivery, with a branded review CTA, preserved plain-text fallback and tracking pixel.
- 2026-08-10 14:03:11 UTC — Validation: focused tests 12/12 passed; full suite 167/167 passed; typecheck passed; production build passed (existing BusinessMap dependency warning only).
