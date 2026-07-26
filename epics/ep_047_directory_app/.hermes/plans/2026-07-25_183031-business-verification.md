# Business Verification Experience Implementation Plan

> **For Hermes:** Implement task-by-task with tests before each production change.

**Goal:** Add a secure, no-login, pre-filled, mobile-first owner verification flow that can be completed in under one minute and ends by offering a real **Claim Your Business** next step.

**Architecture:** EP047 remains the source of truth. An administrator creates a single-use, expiring opaque verification link for one business; the recipient uses that link without an account or dashboard. The public verification page reads a safe pre-filled projection of the business record, records field-level confirmation/corrections and explicit consent, then creates a claim request for human review. Nothing becomes publicly changed or “claimed” merely because a form was submitted.

**Tech stack:** Next.js App Router, TypeScript, Drizzle ORM, existing Render Postgres, existing EP047 session/role guards, Node crypto, current Tailwind styles.

**Non-goals for this release:** bulk outreach, automatic live-profile publishing, an owner dashboard, or a new paid service. The verification and claim journey must not imply any free or paid website offer. Message sending remains held until explicit approval.

---

## Product contract

### Recipient flow

```text
unique HTTPS link
  → immediately shows the recipient their pre-filled business information (no welcome/interstitial screen)
  → confirm or correct only the presented details
  → confirm relationship to the business + data accuracy consent
  → instant result: submitted/verified status plus the exact next stage
  → visible Claim Your Business action or pending-review state
```

A link is only friction-reducing if the owner reaches their own information immediately. The link must resolve directly to a short, pre-filled verification surface—not a login, generic landing page, search screen, or blank form. Submission must immediately confirm what happened, what has not happened yet, and the next action/state. **The internal Activation pipeline and its stage names are never exposed to the business owner; pipeline integration changes admin controls and audit state only, not the recipient journey.**

### Friction rules

- No login, password, dashboard, account creation, CAPTCHA, or unnecessary fields.
- Only editable public listing fields shown in the first screen: business name/trading name, phone, email, website, address/town/postcode, category, and opening hours where present.
- Keep initial verification to one mobile screen plus an optional “more details” expander.
- Preserve the original imported record, all submitted corrections, and the proof that the recipient possessed the unique link.
- A verification link must never reveal `internalNotes`, source/provenance notes, admin user data, tokens, or another business’s data.

### State model

Add explicit data rather than overloading `businesses.status`:

```text
verification_links: issued → opened → submitted | expired | revoked
verification_submissions: submitted → reviewed → accepted | rejected
claim_requests: pending → approved | declined | withdrawn
```

A successful submission creates a `claim_requests` row with `pending` status. Only an authenticated administrator can approve it and transition the business to `claimed`. This protects against a forwarded or compromised email link while still giving the recipient immediate progress.

---

## Task 1: Define the migration and immutable audit model

**Objective:** Create tables that support secure, revocable verification and reviewable owner claims without modifying imported history.

**Files:**
- Create: `migrations/0003_business_verification.sql`
- Modify: `lib/db/schema.ts`
- Test: `tests/verification-model.test.ts`

**Implementation:**

1. Add `verification_links`:
   - UUID primary key; `business_id` FK; SHA-256 `token_hash` unique; `expires_at`; `opened_at`; `submitted_at`; `revoked_at`; `created_by_user_id`; `created_at`.
   - Store the selected expiry interval (`expires_in_days`) alongside `expires_at` for auditability. Default is **5 days**; an authorized admin can choose a bounded value when issuing/reissuing a link (for example 1–14 days).
   - Index active lookups by `token_hash` and business history by `business_id`.
   - Never store a raw capability token.
2. Add append-only `verification_submissions`:
   - UUID primary key; link FK; business FK; JSONB `submitted_fields`; `relationship_to_business`; `accuracy_confirmed_at`; `privacy_notice_version`; `submitted_at`; optional requester email/phone only when the recipient chooses to provide or correct them.
3. Add `claim_requests`:
   - UUID primary key; business FK; submission FK; `status`; requester name; relationship; contact email; contact phone; reviewer user ID; review time; decision note; timestamps.
4. Add a `verification` stage to `pipeline_stages` only if the current pipeline ordering supports it cleanly; otherwise leave the existing imported stage unchanged and rely on the new review state in this release. Do not fabricate stage ordering.
5. Write a migration test or SQL-schema assertion covering FKs, unique token hash, and allowed state defaults.

**Verification:**

```bash
npm test -- tests/verification-model.test.ts
npm run db:migrate
```

Expected: migration is repeatable and a duplicate token hash is rejected by the database.

---

## Task 2: Build verification-token service and repository

**Objective:** Centralize token issuance, safe lookup, expiry/revocation checks, and submission persistence.

**Files:**
- Create: `lib/verification/tokens.ts`
- Create: `lib/verification/repository.ts`
- Create: `lib/verification/types.ts`
- Test: `tests/verification-tokens.test.ts`

**Implementation:**

1. Generate a raw token with `crypto.randomBytes(32)` and encode as URL-safe base64url.
2. Store only `sha256(rawToken)`.
3. `issueVerificationLink(businessId, actorUserId)` revokes any prior unused active link for that business, stores a replacement, and returns the raw one-time URL value only to the issuing admin response.
4. `getVerificationByRawToken(rawToken)` returns only a safe business view and rejects malformed, unknown, revoked, expired, or submitted tokens with the same neutral invalid-link outcome.
5. Mark `opened_at` once without invalidating the link.
6. Use a single transaction to record a submission, mark the link submitted, write the immutable submission snapshot, create/reuse a pending claim request, and append an owner-sourced `stage_transitions` audit event where an applicable stage exists.

**Tests:**

- valid generated tokens are accepted;
- raw tokens are absent from persisted records/loggable output;
- expired, revoked, malformed, and reused tokens are rejected;
- issuing a new link revokes the previous unused link;
- one submission cannot create duplicate pending claim requests;
- attempted submission leaves original `businesses` source values unchanged.

---

## Task 3: Add a protected admin issuer endpoint and business-page control

**Objective:** Allow an authenticated EP047 administrator to issue one verification URL for a selected record without sending it.

**Files:**
- Create: `app/directoryadmin/api/businesses/[businessRef]/verification-link/route.ts`
- Modify: `app/directoryadmin/businesses/[businessRef]/page.tsx`
- Create: `components/admin/VerificationLinkPanel.tsx`
- Test: `tests/verification-admin-api.test.ts`

**Implementation:**

1. Require the existing admin API guard and enforce an operational role policy before issuing a link. If all current roles have full access, define a small explicit `canIssueVerificationLinks` policy rather than silently broadening public access.
2. Resolve the record by immutable `businessRef`; return 404 for unknown records.
3. Return the generated URL only in the authenticated response. Do not write it to server logs, database notes, page HTML, analytics, or a client-visible history list.
4. Add a simple admin-panel action: **Create verification link**. After creation, display a copy-only link once with its expiry and a separate **Revoke link** action.
5. Do not add a “Send email” button in this release.

**Tests:**

- unauthenticated request is rejected;
- a non-authorized role is rejected once the policy exists;
- valid admin request returns an HTTPS `/verify/<token>` link;
- no raw token appears in the database projection;
- revoke invalidates the link.

---

## Task 4: Implement the public no-login verification page

**Objective:** Deliver the under-one-minute, pre-filled recipient experience.

**Files:**
- Create: `app/verify/[token]/page.tsx`
- Create: `app/verify/[token]/VerificationForm.tsx`
- Create: `app/verify/[token]/actions.ts`
- Modify: `app/globals.css` only for reusable accessible verification styles if existing utilities are insufficient
- Test: `tests/verification-page.test.ts`

**Implementation:**

1. Mark page `force-dynamic`, `robots: { index: false, follow: false }`, and return a generic expired/unavailable page for every invalid token case.
2. Use positive neutral copy:

   ```text
   We have a listing for [Business Name].
   Help us make sure local customers see the right details.
   ```

3. Pre-fill safe fields. Each field must allow the recipient to confirm it unchanged or edit it; do not demand an edit to progress.
4. Collect only two required attestations:
   - “I’m connected with this business” (owner / employee / authorised representative / other);
   - “I confirm the information I submitted is accurate to the best of my knowledge.”
5. Add a compact privacy link and clear text that submission sends changes for review; it does not automatically publish them.
6. Include a client-side completion affordance, but enforce all validation server-side.
7. Never include the raw token in `Referer` links or external assets. Keep the page free of third-party analytics until referral leakage has been assessed.

**Tests:**

- valid link renders prefilled data;
- invalid and expired links are indistinguishable and `noindex`;
- page omits internal/admin data;
- post requires attestation and succeeds with unchanged prefilled values;
- error messages do not disclose whether another token exists.

---

## Task 5: Create the post-verification claim step

**Objective:** Ensure successful verification ends in immediate, honest progress rather than an empty thank-you state.

**Files:**
- Create: `app/verify/[token]/complete/page.tsx` or a server-rendered success state in `app/verify/[token]/page.tsx`
- Create: `app/verify/[token]/claim/actions.ts` if claim details are intentionally separated
- Modify: `lib/verification/repository.ts`
- Test: `tests/verification-claim.test.ts`

**Implementation:**

1. On successful verification, show:

   ```text
   Your details have been received.
   Claim Your Business
   ```

2. The claim step must not create an account. Capture the minimum reviewable ownership information: contact name, relationship, preferred email/phone, and optional short note.
3. The success screen must state exactly what happens next: “A team member will review this claim before changes go live.” Do not promise a turnaround time unless one is operationally supportable.
4. Prevent refresh/back-button duplicate submissions with the already-consumed link and idempotent submission transaction.
5. Keep the claim pending; do not grant editing rights, publish data, or activate a website from this flow.

**Tests:**

- successful verification produces one submission and one pending claim request;
- duplicate POST does not create duplicates;
- an admin can list the pending claim request;
- public profile stays unchanged until explicit approval.

---

## Task 6: Integrate verification operations into the existing Activation pipeline

**Objective:** Extend the live `/directoryadmin/pipeline` board rather than creating a parallel admin workflow.

**Current live baseline observed:**

```text
Discovered → Imported → Validated → Verification → Claimed → … subscriber stages
```

The current board shows 998 records in **Imported**, with a per-card `Move to…` dropdown and `Go` action. **Verification** and **Claimed** already exist as pipeline columns and are currently empty.

**Files:**
- Modify: `app/directoryadmin/pipeline/page.tsx`
- Modify: `app/directoryadmin/pipeline/actions.ts`
- Modify: `lib/db/queries/pipeline.ts`
- Modify: `app/directoryadmin/businesses/[businessRef]/page.tsx`
- Create: `app/directoryadmin/verifications/[claimRequestId]/page.tsx` only as a protected detail/review drill-down
- Test: `tests/verification-review.test.ts`

**Implementation:**

1. Keep the existing pipeline order and use its existing **Verification** and **Claimed** columns as the operational source of truth.
2. Do not let the generic `Move to…` dropdown force a business into `Verification` or `Claimed`. Those states must be entered only by the controlled verification/claim actions below.
3. In **Validated**, add a card action: **Prepare verification delivery**. It opens the existing-record recipient, expiry (default five days), and preview workflow.
4. In **Verification**, show a compact, factual verification sub-status on each card:

   ```text
   Ready to send | Sent | Opened | Submitted | Expired | Revoked | Delivery failed
   ```

   Then offer the appropriate safe action: preview/send, reissue, revoke, or review submission.
5. On submission, retain the card in **Verification** with `Submitted — review required`; do not move it to **Claimed** yet.
6. Only a manual approval from the protected claim detail page moves the card to **Claimed** and writes the stage transition/audit decision in the same transaction.
7. The existing board metrics (`Today`, `Avg time`, `Blocked`) must be recalculated from real verification link/delivery/claim states. For example, expired links and failed deliveries may count as blocked; a sent link must not be counted as completed.
8. The optional protected detail route is reached from a card’s **Review** action; it is not a separate disconnected queue.

**Tests:**

- generic stage move cannot bypass verification/claim controls;
- validated card enters verification only through a created delivery workflow;
- sent/opened/submitted/expired states render on the verification card;
- submitted claim remains in verification until manual approval;
- approval moves card to claimed and creates exactly one audit/stage transition;
- board counts and blocked metrics match real underlying states.

---

## Task 7: Add the public **Claim my listing** entry point

**Objective:** Provide the required V1 public route for an owner or representative who did not receive, cannot find, or has expired their verification link—without letting an arbitrary visitor take control of a listing.

**Files:**
- Create: `app/claim/page.tsx`
- Create: `app/claim/ClaimMyListingForm.tsx`
- Create: `app/claim/actions.ts`
- Create: `app/claim/complete/page.tsx`
- Modify: `app/directory/business/[slug]/page.tsx`
- Create: `lib/verification/claim-intake.ts`
- Test: `tests/public-claim-intake.test.ts`

**Implementation:**

1. Replace the disabled public-profile control with a real **Claim my listing** link to `/claim?business=<businessRef>`.
2. `/claim` supports a direct preselected business (from a profile) and a search/select path (for people arriving independently). Search results reveal only public listing information.
3. Capture the minimum claim-intake data: business selection, claimant name, relationship, a reachable email address or mobile number, and explicit accuracy/privacy acknowledgement.
4. Rate-limit the public route and add server-side abuse controls: one active request per business/contact window, generic success responses, honeypot field, and no disclosure of whether a contact address matches the existing listing.
5. Create a `claim_requests` row in `pending_contact_verification` status. The visitor sees an honest completion screen: “We’ll send a verification link to the contact route you supplied.”
6. The claim does **not** change `businesses.status`, public data, ownership, or access. It becomes actionable only after contact verification and manual admin approval.
7. If an authorized admin later approves the request, transition it through the same review path as a verification-link submission; do not create two competing claim models.

**Tests:**

- public profile routes to the preselected claim page;
- a direct `/claim` search path works without authentication;
- intake creates one pending contact-verification request without changing the listing;
- repeated requests are rate-limited/idempotent;
- the response does not leak whether an email address is already held;
- only a reviewed, contact-verified request can be approved.

---

## Task 8: Add controlled verification delivery capability

**Objective:** Make the flow capable of delivering a verification link directly to a claimant while retaining human control over every external send until the operating policy is approved.

**Files:**
- Create: `lib/verification/delivery.ts`
- Create: `lib/verification/email-template.ts`
- Create: `app/directoryadmin/api/verification-deliveries/[claimRequestId]/route.ts`
- Modify: `app/directoryadmin/verifications/[claimRequestId]/page.tsx`
- Modify: `lib/db/schema.ts` and migration `0003_business_verification.sql` to add immutable delivery-attempt records
- Test: `tests/verification-delivery.test.ts`

**Implementation:**

1. Add `verification_deliveries`: recipient channel/address snapshot, message template version, verification-link ID, created/sent/failed timestamps, provider message ID where available, and actor user ID. Never log the raw link token.
2. Build the rendered email template and a protected admin **Send verification link** action with a mandatory recipient preview and explicit send confirmation. The message is factual and non-salesy: it asks the recipient to verify a listing/claim they initiated; it makes no commercial promise.
3. Support a delivery adapter boundary. Configure no new third-party provider unless separately approved; initial deployment can use **manual copy** plus an admin-visible delivery preview, or an approved existing mail route when it is technically and commercially cleared.
4. Record every attempted send, including provider failure/bounce outcomes if the selected delivery route exposes them. A failed delivery does not claim a business or invalidate the claim request.
5. Add an environment/feature flag such as `VERIFICATION_DELIVERY_ENABLED=false` by default. The function ships tested and ready; turning it on to message real businesses remains an explicit operational approval.
6. Provide an admin reissue action that revokes the old capability URL and sends/exports a new five-day link. The expiry selector is available for authorized admins.

**Clarification of the hold:** external verification delivery means transmitting a link/email/SMS to a real business contact outside a user-controlled test address. The hold is **not** a decision to omit the feature. It prevents an unreviewed outbound campaign or accidental sends while copy, sender identity, recipient selection, privacy notice, delivery route, bounce handling, and suppression rules are not yet signed off. The platform can be built delivery-ready and tested with user-controlled addresses; activation for genuine recipients is a separate one-click operational decision.

**Tests:**

- delivery cannot execute without admin authorization and an explicit confirmation;
- delivery records omit raw tokens;
- feature flag blocks real send but still permits preview/copy tests;
- reissue revokes the old URL;
- provider failure is recorded and keeps the claim safely pending.

---

## Task 9: Privacy, accessibility, and release validation

**Objective:** Prove the flow is secure, usable, and genuinely low-friction before enabling it operationally.

**Files:**
- Create: `docs/business-verification-runbook.md`
- Modify: `.env.example` only if a public `SITE_URL` configuration is not already documented
- Test: `tests/verification-security.test.ts`

**Validation checklist:**

```bash
npm test
npm run typecheck
npm run lint
npm run build
```

Then deploy to Render and verify manually on `https://thetechprinciple.com`:

1. Admin creates, copies, revokes, and reissues a link.
2. Recipient completes the flow on a phone-width viewport without login.
3. Verification takes under 60 seconds with unchanged fields.
4. Expired/revoked/reused URLs disclose no business data.
5. Successful verification creates one pending claim.
6. Admin approval updates only approved fields and marks the business claimed.
7. Logged-out admin routes remain redirected and admin APIs remain unauthorized.
8. Public listing, `/directory`, homepage proxy, and `www → apex` behavior remain intact.

**Release guardrails:**

- No actual verification emails or outreach are sent during implementation or QA.
- Use a user-controlled test record/email only for any end-to-end delivery test, and only after explicit approval.
- Record privacy notice version and consent timestamps before the first real recipient use.
- Create a recovery/reissue procedure before links are issued at scale.

---

## Decisions confirmed by owner

1. **Link lifetime:** default **5 days**; authorized admins must be able to select a bounded alternate expiry at issue/reissue time.
2. **Claim review standard:** manual review of every first claim; no automatic ownership approval.
3. **Initial editable field set:** contact, location, website, and category only.
4. **Public recovery route:** **Claim my listing is required in V1.** It creates a pending contact-verification claim request; it cannot immediately change a listing or grant ownership.
5. **External verification delivery:** the capability is part of V1, with a protected preview/send/reissue workflow and delivery audit trail. Real-recipient sending is enabled only after explicit operational approval; user-controlled test delivery may be used for QA.
