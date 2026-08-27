# EP051 Render deployment package

Version 1.0.0 (2026-08-27).

Companion to `deploy/render.yaml`. This covers the gap between the existing
provider-neutral deploy docs (`OPERATIONS.md`, `environment_matrix.md`,
`docker-compose.yml`) and Render specifically. Written for you to click
through in the Render dashboard/CLI yourself — nothing here is executed
automatically.

## What ships

- `ep051-directory` web service, built from `hosted_directory/Dockerfile`
  (already exists, provider-neutral).
- `ep051-db` managed Postgres.
- No Redis: the `cache` service in `docker-compose.yml` is unused by the
  running app code (`grep -ri redis hosted_directory/app` returns nothing) —
  don't provision it, it's dead config in the compose file only.

## Steps

1. **Blueprint deploy.** In Render: New → Blueprint → this repo → root
   directory `epics/ep_051_strategy_directory` → point it at
   `deploy/render.yaml`. This provisions the DB and web service but the web
   service will fail health checks until migrations are applied (step 2).

2. **Apply migrations, in order, once, before first traffic.**
   Connect with `psql` using the Render DB's external connection string
   (Dashboard → ep051-db → Connect), then run
   `hosted_directory/migrations/001` through `007` in numeric order:
   ```bash
   for f in hosted_directory/migrations/0*.sql; do psql "$DATABASE_URL" -f "$f"; done
   ```
   Migration `007` creates a dedicated `ep051_retention_owner` role
   (`NOLOGIN`, `BYPASSRLS`, no memberships) that owns
   `intelligence_purge_expired_history()`. This requires the connecting
   role to have `CREATEROLE`. Render's default database user on the
   Starter plan has this by default; confirm with
   `SELECT rolcreaterole FROM pg_roles WHERE rolname = current_user;`
   before running migration 007 — if it's `f`, you'll need to ask Render
   support to grant it or run that one migration as a superuser-equivalent
   connection.

3. **Create the maintenance role** used for the 90-day retention purge.
   Per `hosted_directory/README.md`, this must be `NOSUPERUSER`,
   `NOBYPASSRLS`, with no private-table/column privileges and only
   `EXECUTE` on `intelligence_purge_expired_history()`:
   ```sql
   CREATE ROLE ep051_maintenance LOGIN PASSWORD '<generate one>';
   GRANT EXECUTE ON FUNCTION public.intelligence_purge_expired_history() TO ep051_maintenance;
   ```
   Build a `MAINTENANCE_DATABASE_URL` from that role's credentials and set
   it in the Render service's environment (it's marked `sync: false` in
   `render.yaml` on purpose — never generate this one automatically).

4. **Runtime role for the app itself.** The `DATABASE_URL` Render injects
   via `fromDatabase` uses Render's default app user. Confirm it is not a
   superuser and does not own the private intelligence tables (it shouldn't,
   since migrations create/own those objects as whichever role ran step 2 —
   keep that distinct from the app's runtime `DATABASE_URL` role if you want
   the same non-owner/`NOBYPASSRLS` separation the README calls for. For a
   first deploy with private intelligence routes left disabled (see step 6)
   this separation is lower-stakes, but tighten it before turning
   `INTELLIGENCE_USER_TOKEN` on.

5. **Verify.** Once the service is up: `GET /healthz`, `GET /readyz`, then
   confirm the public screens (`/`, `/search.html`, `/strategy.html`,
   `/compare.html`, `/regimes.html`) load with `EP051_SNAPSHOT` still
   `not-published` — expect an empty/placeholder directory until you publish
   a snapshot (step 7).

6. **Private intelligence stays off by default.** Do not set
   `INTELLIGENCE_USER_TOKEN` until an OIDC identity edge is actually
   deployed in front of this service — see
   `hosted_directory/evidence/identity_access_decision.md`. Render doesn't
   provide this natively; you'd need something like Cloudflare Access,
   Auth0, or a custom OIDC-terminating proxy in front. Without it, the app
   correctly leaves private routes unloaded and only serves public,
   anonymous directory/finder/compare/regime screens — that's the intended
   fail-closed behavior, not a bug.

## The 10-minute cache sync, for a hosted target

The local app (port 8012 / `run_local.ps1`) reads `runtime/*.json` files
refreshed by `python -m sync.warm_local_intelligence`, run locally on a
schedule. That mechanism is local-only and does not apply to the hosted
deployment — Postgres is the hosted store, refreshed differently:

1. On your machine (where the SQL Server trade data lives), export:
   `python -m sync.export_snapshot --output snapshot.json`
2. Publish it outbound to the hosted service:
   `python -m sync.publish_snapshot snapshot.json --url https://ep051-directory.onrender.com --token <SYNC_TOKEN>`

To replicate the "every 10 minutes" cadence you have locally, wrap steps 1–2
in a script and register it as a Windows Scheduled Task (`schtasks`) running
every 10 minutes — analogous to whatever currently refreshes
`runtime/directory_summary_cache.json` locally. `publish_snapshot.py` is
already idempotent (retries with backoff, `Idempotency-Key` header), so
overlapping runs are safe.

## Deliberately not covered here

Backup/restore, incident/rollback, and the public-launch go/no-go gate are
already specified in `deploy/backup_restore.md`, `deploy/rollback.md`, and
`workstreams/WF-704/go_no_go.md` — nothing in this package changes that
project's own gating; it only gets a private/internal Render instance
running so those evidence-gathering steps have somewhere to run against.
