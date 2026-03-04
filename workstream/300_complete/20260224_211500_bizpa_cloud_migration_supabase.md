# TASK: Migrate bizPA to Cloud Architecture (Supabase & Render)

## 1. Objective
Transition the backend and database from the local laptop to cloud-hosted infrastructure to ensure the mobile APK is globally accessible without a local VPN/Firewall tunnel.

## 2. Infrastructure Target
- **Database**: Supabase (PostgreSQL).
- **Backend API**: Render or Railway (Node.js).
- **Storage**: Supabase Storage (for receipts/images).

## 3. Migration Plan
- [x] **Phase 1: Database Migration**
  - [x] Export local `bizpa` schema and data. (Generated `bizpa_full_migration.sql`)
  - [x] Apply schema to Supabase instance.
  - [x] Update `backend/.env` with `SUPABASE_DATABASE_URL` and keys.
- [x] **Phase 2: Code Decoupling**
  - [x] Abstract local file system paths in `itemController.js` to use cloud storage (Supabase).
  - [x] Update `db.js` to handle connection pooling for high-latency cloud connections.
- [>] **Phase 3: Deployment**
  - [x] Prepare `.gitignore` files to exclude sensitive data (`.env`, keystores).
  - [ ] Pushed backend code to GitHub (Build failing on Render).
- [x] **Phase 4: Frontend Re-pointing**
  - [x] Update `App.jsx` `API_BASE_URL` to point to the Render URL (reverted to local due to deployment failure).

## 4. Log
- 2026-02-24: Strategic pivot to cloud requested by user.
- 2026-02-26: Render deployment found to be a "dead end" due to environment/root dir issues.
- 2026-02-26: TASK CLOSED/PIVOTED. New strategy: Docker-based Local-to-Cloud Proxy Implementation.

## 5. Completion Status
**PIVOTED** - 2026-02-26 22:50
Moved to new task stream for Docker-based approach.
