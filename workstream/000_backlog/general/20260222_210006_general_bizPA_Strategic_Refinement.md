# bizPA Strategic Refinement Document

**Generated:** 2026-02-22

------------------------------------------------------------------------

# 1. Gap Closure Plan

## Structural Data Gaps

To ensure accountant-ready exports without becoming bookkeeping
software, each financial record must include:

-   Unique ID
-   Date
-   Type (Invoice / Receipt / Payment / Quote)
-   Counterparty (Client/Supplier)
-   Net Amount
-   VAT Amount
-   Gross Amount
-   VAT Rate
-   VAT Type (Input / Output)
-   Category (high-level only)
-   Status (Paid / Unpaid / Draft / Converted)
-   Quarter reference

## VAT Readiness

-   Quarterly aggregation engine (Box 1, 4, 6, 7 compatible structure)
-   VAT confidence flag (user-confirmed vs auto-detected)
-   VAT threshold alert logic (\~£90k turnover warning)

## Invoice / Quote Flow Completion

-   Auto invoice numbering
-   Quote → Invoice conversion link
-   Payment status tracking
-   Due date tracking
-   Overdue logic + notification triggers

## Receipt Intelligence

-   Auto category suggestion via AI
-   VAT auto-detection
-   Reclaimable toggle
-   Supplier learning (auto-fill repeat suppliers)

------------------------------------------------------------------------

# 2. Homepage Revisit -- Navigation & Delivery

## Current Strength

-   Clean dashboard
-   Clear financial buckets
-   Voice capture prominent

## Improvements Required

### A. Introduce "Action Panel" (Top Section)

Replace passive summary with: - Overdue invoices - Quotes awaiting
response - VAT quarter countdown - Revenue opportunity alerts

### B. Replace Static Totals with Insight Blocks

Instead of only totals, show: - This week vs last week revenue delta -
VAT payable estimate - Clients inactive \> 60 days

### C. Navigation Structure

Recommended bottom navigation (mobile-first):

1.  Capture (Voice-first primary action)
2.  Activity (All records timeline)
3.  Clients
4.  Insights
5.  Tax

Dashboard becomes insight hub, not just totals screen.

------------------------------------------------------------------------

# 3. Core Connection Architecture (Base Layer)

## Accounting Export Connectors

-   Xero (CSV compatible)
-   QuickBooks (CSV compatible)
-   Generic accountant export (structured CSV + PDF summary)

## Payment Connectors

-   Stripe (invoice payment links)
-   GoCardless (recurring payments)

## Calendar Connector

-   Google Calendar (booking sync)

## Tax Connector

-   VAT summary export for MTD software
-   Accountant referral integration

## Communication Connector

-   Email automation
-   SMS reminder integration
-   WhatsApp Business API (future)

------------------------------------------------------------------------

# 4. Workflow Testing Framework

## Voice Capture Workflow Test

1.  Speak: "Invoice John 500 plus VAT for guttering."
2.  System parses:
    -   Type: Invoice
    -   Client: John
    -   Net: 500
    -   VAT: 100
    -   Gross: 600
3.  Confirmation summary shown
4.  Invoice generated + emailed
5.  Status tracked

## Receipt Workflow Test

1.  Speak: "Fuel 60 pounds including VAT."
2.  Auto-categorised: Fuel
3.  VAT calculated
4.  Quarter updated
5.  VAT summary updated

## Quote Conversion Workflow

1.  Create quote
2.  Reminder after 5 days
3.  Convert to invoice
4.  Track payment
5.  Reflect in revenue dashboard

## VAT Quarter Workflow

1.  Quarter countdown active
2.  VAT running summary visible
3.  "Export for Accountant" generates full structured pack

------------------------------------------------------------------------

# 5. Additional Critical Items

## A. Data Model Discipline

-   Flat transactional structure
-   No double-entry system
-   Strict schema validation

## B. Confidence Indicators

-   AI classification confidence score
-   Highlight records needing review

## C. Notification Governance

-   Smart notification frequency controls
-   Prioritised alerts (Critical / Informational)

## D. Client Intelligence Layer

-   Lifetime value calculation
-   Last contact tracking
-   Revenue frequency detection
-   Recurring service pattern detection

## E. Daily Habit Engine

-   End-of-day summary notification
-   Weekly performance recap
-   "You earned X more than last week" insight

## F. Psychological Stickiness

-   Revenue milestone badges
-   VAT readiness indicator
-   Clean accountant feedback loop

------------------------------------------------------------------------

# 6. Strategic Guardrails

Do NOT: - Build full bookkeeping system - Add chart of accounts
complexity - Attempt full MTD submission initially - Overload UI with
accounting jargon

Focus on: - Frictionless capture - Structured data - Intelligent
prompting - Export readiness - Habit formation

------------------------------------------------------------------------

# 7. Immediate Priority Roadmap (Execution Order)

1.  Harden structured transaction schema
2.  Complete VAT quarter engine
3.  Improve invoice/quote state machine
4.  Introduce Action Panel on homepage
5.  Build clean accountant export
6.  Add smart notification triggers
7.  Begin first connector integration

------------------------------------------------------------------------

# Conclusion

bizPA should become:

A frictionless business memory layer that: - Structures data in
real-time - Reduces tax anxiety - Surfaces revenue opportunities -
Connects cleanly to accountants - Builds daily usage habits

Not bookkeeping.

Not bloated accounting software.

A business intelligence co-pilot for sole traders.
