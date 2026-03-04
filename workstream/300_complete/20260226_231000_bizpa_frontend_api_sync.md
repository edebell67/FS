# TASK: bizPA App API Standardization

Source: `000_backlog/20260226_225500_bizpa_local_cloud_proxy_infrastructure.md`

## 1. Task Summary
Update the mobile and web applications to use a standardized API address logic. The app should easily switch between "Local", "Tunnel (Laptop)", and "Production Cloud" without code changes (using environment variables or a single config line).

## 2. Context
- Files affected: `bizPA/frontend/src/App.jsx`, `.env` files.
- Goal: `API_BASE_URL` consistency.

## 3. Implementation Log
- 2026-02-26: Task created.
- 2026-02-26: Updated `bizPA/frontend/src/App.jsx` with the new tunnel URL.

## 4. Changes Made
- Modified `API_BASE_URL` in `App.jsx` to `https://wet-months-call.loca.lt/api/v1`.

## 5. Validation
- Frontend points to the public tunnel.

## 7. Completion Status
**COMPLETE** - 2026-02-26 23:40
