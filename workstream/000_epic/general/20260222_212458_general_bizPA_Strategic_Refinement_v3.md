# bizPA Strategic Refinement Document (v3 -- Energetic UI Included)

**Generated:** 2026-02-22

------------------------------------------------------------------------

# 1. Gap Closure Plan

## Structured Transaction Requirements

Each financial record must include:

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

-   Quarterly aggregation engine (Box 1, 4, 6, 7 compatible)
-   VAT confidence flag
-   VAT threshold alert (\~£90k turnover)
-   Quarter countdown indicator

## Invoice / Quote State Machine

-   Auto invoice numbering
-   Quote → Invoice conversion
-   Due date tracking
-   Overdue logic + notification trigger
-   Payment status state model

------------------------------------------------------------------------

# 2. Energetic Homepage Redesign (Command Centre Model)

## Objective

Transform homepage from static menu → dynamic business cockpit.

## Section 1: Live Momentum Bar (Top)

Display:

🔥 THIS WEEK\
£X,XXX\
↑ / ↓ % vs last week

Sub-row: - Expenses this week - VAT estimated - Unpaid invoice count

Rules: - Always show delta vs previous period - Colour code: Green
(growth), Amber (flat), Red (decline) - Never show static zero-state
without context

------------------------------------------------------------------------

## Section 2: Attention Panel (Critical)

Label: ⚠ Attention Required

Examples: - 1 invoice overdue (£110) - 2 quotes expiring in 3 days - VAT
quarter ends in 19 days

Rules: - Red badge indicator when urgent items exist - Sorted by
urgency - Tapping opens filtered activity view

This is the primary daily engagement trigger.

------------------------------------------------------------------------

## Section 3: Performance Grid (Compact)

Replace large tiles with status-driven compact cards:

Invoices - X unpaid - £ outstanding

Receipts - X logged this week

Bookings - X upcoming (next date shown)

Clients - X active - X inactive \> 60 days

Cards must show micro-data, not just icons.

------------------------------------------------------------------------

## Section 4: Smart Insight Feed

Dynamic AI-driven cards:

-   Revenue down 12% vs last week
-   Fuel spend higher than average
-   Client due for follow-up
-   Milestone reached (£10k month)

Rules: - Maximum 3 visible at once - Ranked by impact - Dismissible but
tracked

------------------------------------------------------------------------

## Section 5: Capture Engine (Primary Action)

Large central button:

🎙 Log Something

Behaviour: - Opens voice capture panel - Structured preview before
save - Confidence indicator if AI auto-classifies

This is the behavioural anchor of the app.

------------------------------------------------------------------------

# 3. Navigation Restructure (Mobile-First)

Bottom Navigation:

1.  Home
2.  Activity
3.  Clients
4.  Insights
5.  Tax

Remove oversized category tiles from homepage.

------------------------------------------------------------------------

# 4. Cloud Sync Architecture

## Objectives

-   Local-first capture
-   Near real-time cloud sync
-   Multi-device readiness
-   SaaS scalability

## Requirements

-   Delta sync model
-   Offline queue
-   Conflict resolution strategy
-   Encrypted transport
-   Per-user cloud isolation

## Future Enablement

-   Accountant read-only access
-   Aggregated anonymised analytics
-   Subscription gating
-   Connector marketplace

------------------------------------------------------------------------

# 5. Connection Architecture (Base Integrations)

## Accounting

-   Xero-compatible CSV
-   QuickBooks-compatible CSV
-   Generic structured export

## Payments

-   Stripe
-   GoCardless

## Calendar

-   Google Calendar sync

## Communication

-   Email automation
-   SMS reminders
-   WhatsApp Business (future)

------------------------------------------------------------------------

# 6. Workflow Testing Framework

## Voice Capture

Test structured parsing including VAT handling.

## Invoice Lifecycle

Draft → Sent → Overdue → Paid → Reflected in metrics.

## VAT Quarter Flow

Countdown → Aggregation → Export pack generation.

## Cloud Sync

Create locally → Sync → Modify on web → Sync back → No data loss.

------------------------------------------------------------------------

# 7. Notification Governance

-   Critical (Overdue, VAT deadline)
-   Important (Quote follow-up)
-   Informational (Performance delta)

Limit frequency to avoid fatigue. Prioritise actionable notifications.

------------------------------------------------------------------------

# 8. Strategic Guardrails

Do NOT: - Build double-entry bookkeeping - Add chart of accounts -
Attempt direct MTD filing initially - Overcomplicate UI

Focus on: - Structured capture - Intelligent prompting - Revenue
awareness - VAT readiness - Habit formation

------------------------------------------------------------------------

# 9. Immediate Execution Order

1.  Harden structured transaction schema
2.  Implement VAT quarter engine
3.  Build energetic homepage redesign
4.  Implement cloud sync layer
5.  Improve invoice/quote lifecycle
6.  Add intelligent notification triggers
7.  Build accountant-ready export

------------------------------------------------------------------------

# Conclusion

bizPA becomes:

A frictionless, energetic business command centre that: - Captures via
voice - Structures data correctly - Syncs securely to cloud - Surfaces
obligations & opportunities - Reduces tax anxiety - Builds daily
engagement habits

Not bookkeeping.

A business intelligence co-pilot for sole traders.
