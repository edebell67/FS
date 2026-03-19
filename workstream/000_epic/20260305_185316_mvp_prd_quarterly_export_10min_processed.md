# MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)

## 0) One-line summary
A mobile app that pulls Open Banking transactions, lets users resolve only “blocking” items via taps or voice, and exports an accountant-friendly **Quarterly Pack** (CSV + PDF). **No submission to HMRC.**

---

## 1) Target user
- UK **cash-light** sole traders (majority of spend/income via bank/card)
- Wants quarterly handoff to accountant / existing MTD-compatible software
- Low tolerance for “doing bookkeeping”

---

## 2) Product promise
**“Quarterly export in 10 minutes.”**
- App reduces work to a short, ordered **exception queue**
- Evidence/receipts are optional (helpful, but not blockers)

---

## 3) MVP goals and success metrics
### Goals
- Fast quarter close (minimal taps)
- High confidence exports (traceable + audit-friendly)
- Voice-driven micro-decisions (not long dictation)

### Metrics (MVP)
- Median time from opening Quarter screen → export generated: **≤ 10 minutes**
- Export completion rate (quarter started → exported): **≥ 70%**
- Average “blocking items” per quarter after 30 days active use: **≤ 15**
- Voice command success rate (intent applied without edit): **≥ 80%**

---

## 4) What’s in scope / out of scope
### In scope (MVP)
- Open Banking read-only connection + transaction ingestion
- Inbox triage with micro-decisions:
  - category assignment (suggest + override)
  - business vs personal tagging
  - split transaction (% business)
  - duplicate handling (dismiss/merge)
- Quarter readiness engine + “Finish now” queue
- Receipt/image capture and evidence store
- Evidence ↔ bank transaction matching **with user confirmation**
- Voice commands for core micro-decisions
- Export Quarterly Pack (3 CSV + 1 PDF)
- Simple merchant rules (“Always categorise X as Y”)

### Out of scope (MVP)
- Filing/submitting to HMRC
- VAT features
- Invoicing / AR / quoting
- Landlords / property income
- Complex tax adjustments (capital allowances etc.)
- Multi-business
- Payroll

---

## 5) Core user journeys
### J1 — First-time setup (5 mins)
1. Install → sign up
2. Connect bank via Open Banking provider
3. Choose: Sole trader (MVP only)
4. App imports last ~90 days bank transactions

### J2 — Ongoing triage (1–2 mins)
1. Open Inbox
2. Resolve only flagged items (tap/voice)
3. Optional: attach receipts (camera/share/email later)

### J3 — Quarter close (headline)
1. Open Quarter screen
2. See: readiness %, “items left”
3. Tap **Finish now**
4. App shows ordered blocking queue
5. Resolve queue via quick actions/voice
6. Tap **Export Quarterly Pack**

### J4 — Evidence attach by voice (user confirms)
1. User captures/shares receipt image
2. App extracts amount/date/merchant (best-effort)
3. App proposes top 3 candidate bank matches
4. User taps to confirm (or “No match / Later”)

---

## 6) Blocking rules (the heart of the 10-minute promise)
A transaction is **RESOLVED** if:
- has `category_code`
- has `business_personal` set (Business or Personal)
- if `is_split = true`, then `split_business_pct` is set
- if flagged as duplicate, it has a resolution (dismiss/merge)

A transaction is **BLOCKING EXPORT** if any:
- missing category
- missing business/personal
- split flagged but % missing
- duplicate flagged but not resolved

**Non-blocking:** evidence/receipt missing or unmatched.

---

## 7) Quarter readiness engine
### Inputs
- all transactions in selected quarter period

### Outputs
- `total_txns_in_period`
- `blocking_txns_count`
- `readiness_pct = round(100 * (1 - blocking_txns_count / total_txns_in_period))`
- ordered `blocking_queue` (uncategorised → personal missing → split missing → duplicates)

### UI requirements (Quarter screen)
- Big: “92% ready — 8 items left”
- CTA: “Finish now” (shows blocking queue only)
- Export enabled only when `blocking_txns_count = 0`

---

## 8) Voice (MVP intent set)
Voice is available on Inbox and Finish Now queue.

### Supported commands
- “Category: {X}”
- “Business” / “Personal”
- “Split {n}%”
- “Attach receipt”
- “Match first / second / third”
- “No match”

### Voice UX rule
After voice action, show a single confirmation chip:
- “Applied: Travel • Business • Split 70%” (tap to undo/edit)

---

## 9) Evidence matching (confirm-first)
### Matching behavior
- Receipt image ingested → extract (amount/date/merchant)
- Suggest top 3 bank candidates using:
  - amount exact match (or tolerance)
  - date proximity window
  - fuzzy merchant match
- Always show confirmation bottom sheet:
  - candidate #1 prominent; #2–#3 smaller
  - “No match / Later”

### Matching UX requirements
- For each candidate show: merchant, date, amount + match-reason chips
- One tap confirms link and removes related evidence task from any queue

---

## 10) Export deliverable — Quarterly Pack
The pack must be accountant-friendly and tool-agnostic.

### File 1: Transactions.csv
Fields:
- txn_id
- date
- merchant
- amount
- direction (in/out)
- category_code
- category_name
- confidence (0–1)
- business_personal (BUSINESS|PERSONAL)
- is_split (true/false)
- split_business_pct (0–100, nullable)
- matched_evidence_ids (comma list)
- bank_account_id
- bank_txn_ref

### File 2: EvidenceIndex.csv (export even if empty)
Fields:
- evidence_id
- type (RECEIPT|INVOICE|OTHER)
- captured_at
- doc_date
- merchant
- amount
- storage_link
- extraction_confidence (0–1)
- matched_bank_txn_id (nullable)
- user_confirmed (true/false)

### File 3: QuarterlySummary.csv
Fields:
- period_start
- period_end
- category_code
- category_name
- total_in
- total_out
- count
- unresolved_count

### File 4: QuarterlyPack.pdf (1–2 pages)
- period + totals
- readiness (should be 100% at export)
- category totals highlights
- audit counts (auto-categorised vs manual overrides)
- evidence coverage (matched vs bank-only)

---

## 11) Category set (MVP)
Keep it small, stable, and expandable. Use codes below.

### Income
- INCOME_SALES — Sales / Fees (main trading income)
- INCOME_OTHER — Other income (refunds, misc)

### Expenses
- EXP_COGS — Cost of goods / stock (optional; hide if irrelevant)
- EXP_SUBCONTRACTORS — Subcontractors / freelancers
- EXP_TRAVEL — Travel (public transport, taxi, claimable fuel)
- EXP_VEHICLE — Vehicle costs (repairs, insurance, parking)
- EXP_MEALS — Meals
- EXP_ACCOM — Accommodation
- EXP_RENT_UTIL — Rent & utilities
- EXP_COMMS — Phone & internet
- EXP_SOFTWARE — Software / subscriptions
- EXP_MARKETING — Marketing / advertising
- EXP_INSURANCE — Business insurance
- EXP_BANK_FEES — Bank/merchant fees (Stripe, PayPal, bank charges)
- EXP_PROFESSIONAL — Accountancy/legal/professional fees
- EXP_OFFICE — Office supplies & small equipment
- EXP_TRAINING — Training / education (business-related)
- EXP_MISC — Misc (discourage; should trend down over time)

### Tags (NOT categories)
- PERSONAL (boolean/tag)
- REVIEW_REQUIRED (boolean/tag; drives blockers)

---

## 12) Data model (MVP)
Entities (minimum):
- User
- BusinessProfile
- BankAccount
- BankTransaction
- TransactionClassification (category_code, business_personal, split pct, confidence, audit)
- Evidence
- EvidenceLink (evidence_id, bank_txn_id, link_confidence, user_confirmed, confirmed_at, method)
- Quarter
- QuarterMetrics (total, blocking, readiness_pct)
- Rule (merchant_pattern → category_code, defaults for personal/split)

Audit fields required on any user edits:
- changed_at, changed_by, previous_value, new_value

---

## 13) Non-functional requirements
- Secure storage of credentials/tokens (provider-managed where possible)
- Encryption in transit + at rest
- Idempotent imports (no duplicates on refresh)
- Inbox load < 2 seconds typical device
- Clear disclaimer: not tax advice; user responsible

---

## 14) Build order (recommended)
1) Open Banking ingestion + Inbox list
2) Classification actions + blocker rules
3) Quarter readiness + Finish Now queue
4) Export (CSV + PDF)
5) Evidence capture + match suggestions + confirm
6) Voice intents + confirmation chip + undo
7) Merchant rules (“always categorise”)

---

## 15) MVP acceptance tests
- A quarter with 200 transactions and 8 blockers shows “8 items left”
- Resolving those 8 enables Export immediately
- Export produces all 4 artifacts with correct totals and traceability
- Evidence attachment always requires user confirmation of match (or “No match”)
- Voice “Category: Travel” applies and is undoable with one tap
