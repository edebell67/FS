# EP047 — Batch verification email sending

## Preconditions
- Logged-in user has verification management authority.
- Render has approved Gmail API credentials and a configured `VERIFICATION_SENDER_ADDRESS`.
- Batch contains at least one prepared business with a current recorded email address.

## Procedure
1. Open the batch audit page.
2. Confirm recipient count and delivery policy.
3. Tick **I confirm that I want to send this batch now**.
4. Select **Send N verification emails** once.
5. Verify the returned sent/failed/skipped counts and refresh the item table.

## Pass criteria
- No send occurs before checkbox confirmation.
- Each sent recipient equals the business's current recorded email.
- Each send uses a newly issued one-time capability; raw capabilities are not persisted.
- Result counts are truthful; provider acceptance is not described as recipient delivery.
