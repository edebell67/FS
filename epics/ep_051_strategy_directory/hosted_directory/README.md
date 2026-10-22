# EP051 hosted directory data platform

Version history: 1.1.0 (2026-08-24) — adds intelligence services, persistence, identity boundary and finder operations. 1.0.0 (2026-08-23) — local-first, provider-neutral implementation.

The same application serves the directory screens and `GET /api/dna/strategies` in both environments.

- Local first: set `DATA_BACKEND=sqlserver` plus the read-only `DB_*` values and run `./run_local.ps1`.
- Hosted: set `DATA_BACKEND=postgres`, `DATABASE_URL`, `SYNC_TOKEN`, `INTELLIGENCE_USER_TOKEN` and explicit `ALLOWED_ORIGINS`; apply all seven migrations in numeric order with an administrative migration role able to create the dedicated `NOLOGIN`/`BYPASSRLS` function owner; deploy the OCI image with a non-owner, non-superuser, `NOBYPASSRLS` runtime role. Configure `MAINTENANCE_DATABASE_URL` separately for the 90-day purge using a `NOSUPERUSER`, `NOBYPASSRLS` caller with no private-table or column privileges and only `EXECUTE` on `public.intelligence_purge_expired_history()`; never use either privileged role for requests. The service verifies the caller contract before every purge.
- Publish: export an allowlisted snapshot with `python -m sync.export_snapshot --output snapshot.json`, then send it outbound with `python -m sync.publish_snapshot snapshot.json --url https://... --token ...`.

No raw trades, credentials or local filesystem paths enter the hosted snapshot. Broker integration is intentionally outside this delivery stage.

## Intelligence layer

The intelligence finder is served at `/intelligence.html`. It interprets natural-language requests into a visible `StrategyQuery`, lets the user edit every constraint, applies constraints before ranking, and links qualifying results to evidence and comparison screens. Profile calculations remain server-side.

Private user APIs fail closed unless `INTELLIGENCE_USER_TOKEN` is configured. The trusted-edge contract requires a bearer token and an `X-User-ID` claim supplied by an OIDC-capable hosting identity gateway. The gateway must remove client-supplied identity headers and inject its own verified subject; the browser must never receive the shared edge token. Hosted private objects use PostgreSQL with transaction-local `app.user_id`, explicit owner predicates and forced row-level security. Startup rejects a database role that owns the private tables, is a superuser or has `BYPASSRLS`.

Local public traffic reads a durable, sanitized intelligence snapshot and never triggers a historical full-series scan. Run `python -m sync.warm_local_intelligence` as an operator/scheduled job after source refresh; the default maximum cache age is 24 hours (`LOCAL_INTELLIGENCE_CACHE_MAX_AGE_SECONDS`). If no valid snapshot exists, aggregate-safe profiles are returned and sequence metrics fail closed. The initial catalogue is deterministically capped at 500 strategies by evidence volume. Hosted snapshot promotion invalidates in-process caches immediately.

Machine-readable contracts are published in `contracts/`: the Strategy Intelligence Profile JSON Schema, canonical Strategy Query JSON Schema and OpenAPI document. Market features and regime labels are immutable point-in-time records; stale or incomplete current features return `UNKNOWN` rather than a confident classification. Immediate broker/platform execution integration remains intentionally outside this stage.
