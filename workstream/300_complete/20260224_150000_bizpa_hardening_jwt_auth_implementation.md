# Task: bizPA Hardening - JWT Auth & Session Security (20260224_150000)

## Task Summary
Transition the backend from mock header-based authentication to a secure JWT (JSON Web Token) session model.

## Context
- Milestone 1-3 complete (v1.1.7).
- Current auth uses `X-User-ID` header (insecure/prototype).
- Required for production multi-tenant security.

## Sub-tasks
- [ ] Backend: Implement `authController.js` with login logic.
- [ ] Backend: Update `userMiddleware.js` to verify JWT.
- [ ] Backend: Add JWT secret to `.env`.
- [ ] Frontend: Implement basic login state/storage in `App.jsx`.
- [ ] Verification: Confirm endpoints return 401/403 without valid token.

## Implementation Log
- [2026-02-24 15:00] Task initialized.

## Completion Status
TODO
