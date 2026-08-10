# EP047 — Explicit batch verification-email send

## Request
Allow an authorised directory administrator to send the selected/prepared verification emails in a batch, with an explicit confirmation and truthful sent/failed/skipped results.

## Required safety boundaries
- No automatic send on preparation.
- Role protected and server-side confirmed.
- Send only to each selected business’s current recorded email address.
- Preserve no-raw-capability-at-rest design: batch send must mint/reissue current one-time links during the confirmed operation, not persist tokens.
- Gmail API-only, fixed sender, sender-address configuration, audit, and per-recipient idempotency.
- No send is triggered by implementation/testing/deploy.

## Progress
- 2026-08-10 14:57 UTC — Task created. Root cause confirmed: existing batch preparation persists only hashes, so a later batch send cannot reconstruct secure capability URLs; no batch-send endpoint/control exists.
- 2026-08-10 14:57 UTC — RED: batch-send contract test failed because the protected route did not exist.
- 2026-08-10 14:57 UTC — GREEN: implemented protected confirmed batch send, per-recipient link reissue and Gmail handoff, durable per-recipient audit/outcomes, and the admin send panel.
- 2026-08-10 14:57 UTC — Focused security/delivery tests 12/12 passed; full suite 168/168 passed; typecheck passed; production build passed (existing BusinessMap dependency warning only); diff check passed.
- 2026-08-10 15:27 UTC — Deployed commit `ff795bc` to Render deployment `dep-d9suq9m7bikc73aac40g`, which reached `live`. Health endpoint reports database connected. Render confirms `VERIFICATION_SENDER_ADDRESS` is configured. Unauthenticated browser access correctly redirected to admin sign-in; no email was sent during deployment verification.
