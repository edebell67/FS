# EP047 — public claim gate after verification

## Expected behavior
A public claim is available only while the selected business is at the `verification_completed` stage.

## Checks
1. Visit a `verification_email_pending`, `verification_sent`, `verification_opened`, validation, or unset-stage listing as a logged-out visitor.
   - The claim button must be disabled and cannot navigate to `/claim`.
2. Directly open `/claim?business=<ref>` for that listing.
   - The claim form must not render.
3. Submit a forged request for a non-completed listing.
   - The server must not create a claim.
4. Complete the verification capability form and refresh the public listing.
   - The claim button becomes an enabled link only at `verification_completed`.
