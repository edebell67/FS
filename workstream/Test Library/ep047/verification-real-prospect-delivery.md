# EP047 — real-prospect verification delivery

## Purpose
Verify that an authenticated admin can prepare a verification email only for the selected business's recorded email address, then explicitly confirm a one-time Gmail API send.

## Preconditions
- Production Gmail OAuth, `VERIFICATION_DELIVERY_MODE=gmail-api`, and `VERIFICATION_DELIVERY_APPROVED=true` are configured.
- The business record has a current email address.
- An operations-authorised admin session is active.

## Procedure and pass criteria
1. Open the business detail page. The recipient must be the read-only recorded business email.
2. Prepare the email. The preview must show that recipient, the public listing URL, and a non-sent `Prepared` state.
3. Tick the explicit single-send confirmation. The send button becomes enabled only when transport prerequisites are configured.
4. Send once. The UI must report `Sent` only after Gmail API acceptance and sent-folder readback; record its provider ID/timestamp.
5. Verify the exact attempt in the sender Sent folder, the recipient mailbox (`in:anywhere`), and that the recipient link opens the correct business verification page.

## Safety assertions
- The browser cannot choose an arbitrary recipient.
- Server preparation derives the recipient from the selected business record.
- The send service rechecks the delivery recipient against the current business email.
- No raw capability token is persisted in the delivery audit.
