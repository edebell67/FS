# Task: bizPA Milestone 3 - Revenue Engine Implementation (20260224_112000)

## Task Summary
Implement the Revenue Engine plugin (Milestone 3.1) to automate/prompt payment chasing and re-servicing outreach for small traders.

## Context
- Backend core and CRM (Milestone 1 & 2) are complete (v1.1.6).
- Database contains placeholder tables: `outreach_logs`, `trigger_rules`, `message_templates`.
- Goal: Surface actionable outreach prompts in the "Smart Insights" or "Attention" panels.

## Sub-tasks
- [x] Research: Analyze `trigger_rules` and `message_templates` schema.
- [x] Feature: Create `revenueController.js` to manage outreach logic.
- [x] Feature: Implement "Payment Chase" logic (Invoices overdue > X days).
- [x] Feature: Implement "Re-service" logic (Jobs completed > Y months ago).
- [x] Feature: Create `revenueRoutes.js` and bind to `app.js`.
- [x] UI: Add outreach actions to the "Insights" or "Activity" tabs.

## Implementation Log
- [2026-02-24 11:20] Task initialized.
- [2026-02-24 11:25] Seeded `message_templates` and `trigger_rules` with initial UK-toned variants.
- [2026-02-24 11:30] Implemented `revenueController.js` with SQL-driven opportunity identification.
- [2026-02-24 11:32] Bound routes in `app.js`.
- [2026-02-24 11:35] Enhanced `App.jsx` to fetch and display "Priority Outreach" cards in the Insights tab.

## Changes Made
- `bizPA/backend/src/controllers/revenueController.js`: New logic for Payment Chase and Re-service.
- `bizPA/backend/src/routes/revenueRoutes.js`: New endpoints.
- `bizPA/backend/src/app.js`: Route binding.
- `bizPA/frontend/src/App.jsx`: UI display for outreach cards.

## Validation
- Backend code verified for logic correctness.
- UI state management verified.
- **PENDING**: API verification (404) until backend process (PID 29896) is restarted by the user or an automated system.

## Risks/Notes
- **CRITICAL**: Do NOT restart node.exe via taskkill. The new features will remain inactive until the next planned/automated restart of the backend.

## Completion Status
IN_PROGRESS
