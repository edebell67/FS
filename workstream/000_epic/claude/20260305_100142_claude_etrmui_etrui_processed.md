Priority: 2

Here’s the UI for the UK Power training simulator (Endur-like, but clean and teachable). Think: left nav + blotter-centric workflow + drilldowns.

Global layout

Top bar

Environment badge: TRAINING

As-of date selector (drives MTM/positions views)

Book selector (optional global filter)

User + role badge (FO/MO/BO/MD/Admin)

Left nav (modules)

Trading

Risk & Valuation

Settlements

Market Data (MD Admin only)

Admin (Admin only)

Main area

Most screens are: Filters panel (top) + Grid (middle) + Details drawer (right)

Trading UI
1) Deal Blotter (home screen)

This is the heart of the app.

Filters (top)

Date range, Status, Book, Trader, Counterparty, Buy/Sell, Profile (Base/Peak/Off-peak)

Grid columns

Deal ID | Ver | Status | Book | Trader | Counterparty | Buy/Sell | Profile | Start | End | Qty (MWh/h) | Price Type | Price/Spread | Last Changed

Row click → right drawer

Deal summary + lifecycle timeline

Actions (role-based): Amend, Request Cancel, Submit, Validate, Confirm

Links: Versions, Positions impact, Valuation, Settlement schedule

2) Deal Entry / Edit (wizard style)

Two-column form, minimal friction.

Header

Deal Type: Fixed / Index

Buy/Sell, Counterparty, Book, Trader

Delivery

Start date, End date (UK)

Profile: Base / Peak / Off-peak

Qty: MWh per hour

Location: GB_BASE

Pricing

Fixed: £/MWh

Index: Curve selector + Spread £/MWh

Ops

Payment terms, Notes, Contract ref

Buttons

Save Draft

Submit for Validation

Create Amendment (if editing an existing confirmed/validated deal, creates a new version)

3) Deal Versions (audit view)

Endur people expect this.

Version list (v1, v2, v3…)

Each version shows:

who/when + change reason

a “diff” panel (Qty/Price/Dates/Profile changes)

“Open version” read-only view

4) Confirmations

Simple, but teaches controls.

Grid: Deal | Counterparty | Sent | Received | Status | Notes

Drawer: send method + timestamps + attach metadata

MO controls: mark disputed / received

Risk & Valuation UI
5) Positions Viewer (Daily)

Filters

Delivery date range, Book, Location, Profile, Counterparty

Grid

Delivery Date | Book | Location | Profile | Buy MWh | Sell MWh | Net MWh

Drilldowns

Click a day → breakdown by deal (with deal links)

Badges

Base / Peak / Off-peak is always visible (critical)

6) Valuation (MTM)

Inputs

As-of date, Book(s), Curve version selector (latest published by default)

Outputs

Summary cards: Total MTM, MTM by Book, MTM by Profile

Grid: Deal | Profile | Qty (derived daily/monthly) | Fixed/Index | Curve | MTM | Drivers

Drivers view (drawer)

Shows the simple calculation components (teachability > sophistication)

7) Limits Dashboard

Top

Limits table: limit type (Volume/MTM), threshold, period, book

Breaches table

Breach ID | Limit | Book | As-of | Actual | Threshold | Status | Owner

Actions

Acknowledge, Resolve, Add comment (MO only)

Settlements UI
8) Settlement Run (Monthly)

Select Month (e.g., Mar 2026)

Grid: eligible deals (Confirmed only)

Button: Generate settlement

Output grid:

Deal | Period | Due date | Status (Generated/Locked)

9) Invoice Preview

Select counterparty + month

Invoice header preview (counterparty, period, terms)

Lines (deal-level is enough):

Deal | Profile | Volume MWh | Price rule | Amount

Button: Issue invoice (freezes)

10) GL Export (Stub)

Grid: issued invoices

Drawer shows JSON payload preview

Button: Mark Sent

Market Data UI (MD Admin only)
11) Curve Manager (Versioned publishing)

Curve list: UKP_BASE_FWD / UKP_PEAK_FWD

Curve versions grid:

Version | Status (Draft/Published) | As-of | Created by | Created at

Points editor:

Delivery Month | Price

Publish button (locks version)

Admin UI (Admin only)

Parties, Books, Users/Roles, Locations, Calendar

Maker/checker toggles per role

Two probing questions (to stop this becoming a toy)

Do you want the UI to look like a “classic grid-heavy trading system” (Endur vibe), or more modern app-like (less dense, more guided)?

For training, should confirmation happen automatically on MO approval, or do you want trainees to perform an explicit “Send/Receive confirmation” step?

1

Classic grid-heavy trading system it is (Endur vibe). Here’s the UI spec in that style — screens, layout, grids, drawers, and actions.

Global shell

Top bar (sticky)

Left: TRAINING badge + environment dropdown

Center: As-Of Date picker (drives Positions/MTM)

Right: User | Role (FO/MO/BO/MD/Admin) | Book filter | Search (Deal ID / Counterparty)

Left nav (collapsed icons + labels)

Trading

Deal Blotter

Deal Entry

Confirmations

Risk

Positions (Daily)

Valuation (MTM)

Limits

Settlements

Settlement Run

Invoice Workbench

GL Export

Market Data (MD Admin only)

Curves

Admin (Admin only)

Parties / Books / Users / Calendar

Interaction pattern (everywhere)

Filters row at top

Big grid (sortable, column chooser, saved views)

Right-side Details Drawer (tabs)

Bottom status bar: row count, last refresh, export CSV

Trading
Deal Blotter (home)

Filters (single row + advanced collapse)

Trade date range | Status | Book | Trader | Counterparty | Buy/Sell | Profile | Deal Type

Grid columns (default view)

Deal ID | Ver | Status | Trade Date | Book | Trader | Counterparty | B/S | Profile | Start | End | Qty (MWh/h) | Price Type | Price/Spread | Location | Last Changed

Row click → Details Drawer tabs

Summary (read-only key fields)

Lifecycle (Draft → Submitted → Validated → Confirmed; plus Cancel Requested/Cancelled)

Versions (v1/v2 diff list)

Positions Impact (daily breakdown)

Valuation (latest MTM)

Settlement (if generated)

Toolbar actions (role-based)

FO: New Deal, Copy Deal, Amend, Request Cancel, Submit

MO: Validate, Confirm, Approvecancel, Run MTM (for selected)

Export: CSV, Excel

Deal Entry (classic form, no wizard)

Two-column dense form with section headers:

Parties/Book

Delivery

Profile

Pricing

Ops
Buttons: Save Draft | Submit | Reset

Confirmations

Grid

Deal ID | Counterparty | Method | Sent At | Received At | Status | Owner
Drawer

Timeline + status change actions (MO)

Risk
Positions (Daily)

Filters

Delivery date range | Book | Location | Profile | Counterparty

Grid

Delivery Date | Book | Location | Profile | Buy MWh | Sell MWh | Net MWh | #Deals
Double-click row → drilldown grid of contributing deals.

Valuation (MTM)

Filters

As-Of Date | Book | Curve Version (Published only) | Profile

Grid

Deal ID | Book | Profile | Volume (MWh) | Fixed/Index | Curve | Forward Price | Fixed Price | Spread | MTM (£) | Last Run
Drawer “Drivers” shows the simplified calc components.

Limits

Split view:

Upper grid: Limits

Lower grid: Breaches
Actions: Acknowledge, Resolve (MO)

Settlements
Settlement Run

Filters

Month | Book | Counterparty | Status (Eligible/Generated/Locked)

Eligible deals grid

Deal ID | Counterparty | Profile | Period | Est Volume | Pricing | Eligible Y/N
Button: Generate Settlement (BO)

Invoice Workbench

Filters

Counterparty | Month | Status (Draft/Issued)

Invoices grid

Invoice ID | Counterparty | Period | Amount | Status | Issued At
Drawer tabs:

Lines (deal-level)

Summary

Audit
Actions: Preview, Issue, Generate Credit Note (optional later)

GL Export

Grid

Export ID | Invoice ID | Period | Amount | Status
Drawer shows JSON payload preview.

Market Data (MD Admin only)
Curves

Curve list left; versions grid right; points grid below.

Versions: Draft/Published; Publish button locks.

Points: Delivery Month → Price
Audit panel: who changed what.

Critical “Endur vibe” details (don’t skip)

Saved grid views per user/role (e.g., “My Book – Open Trades”)

Column chooser + quick filter row under headers

Right drawer with tabs everywhere

Version number visible in blotter (people look for it immediately)

- `Completion Status`: Awaiting user verification

## Generated Tasks
| Task | File |
|------|------|
| 20260305_100147_claude_etrmui_task_01_from_20260305_100142_claude_etrmui_etrui | `workstream/200_inprogress/claude/20260305_100147_claude_etrmui_task_01_from_20260305_100142_claude_etrmui_etrui.md` |
| 20260305_100147_claude_etrmui_task_02_from_20260305_100142_claude_etrmui_etrui | `workstream/100_backlog/claude/20260305_100147_claude_etrmui_task_02_from_20260305_100142_claude_etrmui_etrui.md` |

