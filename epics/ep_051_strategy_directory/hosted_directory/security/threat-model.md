# EP051 DNA Strategy Directory — Repository-Scoped Threat Model

## Overview

This deployable package serves a public strategy directory, strategy evidence screens, comparison and portfolio tools, and an intelligence layer over locally sourced or hosted DNA trading evidence. FastAPI in `app/main.py` exposes public read APIs, authenticated private user-object APIs, a protected snapshot-ingestion endpoint, deterministic natural-language interpretation, comparative scoring, and market-regime decision support. `web/` is a same-origin HTML/CSS/JavaScript client. `app/repository.py` reads local SQL Server or promoted PostgreSQL snapshots; `migrations/` defines hosted storage.

The system supports research and allocation investigation. It does not place trades, and broker integration is outside the current scope. Financial evidence integrity, methodology provenance, tenant isolation, and avoiding misleading recommendations are higher-value security properties than confidentiality of already-public aggregate statistics.

Assets that matter are source and hosted database credentials, snapshot and trusted-edge tokens, private watchlists/searches/collections/preferences/history, canonical strategy evidence and methodology versions, market-feature timestamps, release state, audit records, and the integrity/availability of public results.

## Threat Model, Trust Boundaries, and Assumptions

1. **Public browser → FastAPI.** Search text, query parameters, strategy IDs, JSON bodies, request IDs, and all headers are attacker-controlled. The browser is not trusted to calculate metrics, assert identity, or supply privileged tokens. CORS is not an authorization control.
2. **Trusted identity edge → private APIs.** The hosting gateway authenticates a user, keeps the shared edge credential outside browser JavaScript, and supplies both the bearer credential and `X-User-ID`. `trusted_user` in `app/main.py` fails closed if the edge secret or identity is missing. The deployment must strip client-supplied identity headers before adding trusted claims.
3. **Local SQL Server → application.** SQL Server data and credentials are operator-controlled. Queries use fixed SQL plus positional parameters; the account is assumed read-only. Strategy descriptions and product names remain untrusted display data and require output encoding.
4. **Snapshot publisher → hosted ingestion.** `/internal/snapshots` accepts only a configured bearer token, matching idempotency key, bounded item count, verified digest, schema contract, and non-stale watermark. A publisher compromise can corrupt public intelligence even without server compromise.
5. **Application → hosted PostgreSQL.** `DATABASE_URL` is secret. PostgreSQL stores canonical snapshots, intelligence time series, market/regime data, and private objects. Migration `002_intelligence_layer_schema.sql` enables row-level security; each private transaction must set `app.user_id` locally and use a role that cannot bypass RLS.
6. **Market feed → regime services.** Feature values, timestamps, source versions, gaps, and licences are operator-controlled external inputs. `app/intelligence/market.py` makes point-in-time snapshots immutable, and regime services fail closed on missing/stale evidence. Future-dated or revised data must never enter historical evaluations.
7. **Developer/build → container/runtime.** Dockerfile, dependencies, migrations, and methodology registries are developer-controlled. The runtime is non-root. Secrets must enter only through environment configuration and must not be copied into images, logs, screenshots, snapshots, or client bundles.

Core invariants:

- `DNA_…_B` and `DNA_…_S` normalize to one canonical strategy; direction is evidence, not a separate product.
- Outcomes derive from signed `net_return`; `close_type='target reached'` never determines win/loss, and costs/commission are not applied twice.
- Public/browser code never calculates canonical intelligence metrics or changes score weights.
- Hard discovery constraints are validated and applied before ranking. Unsupported units, missing regime evidence, stale features, and insufficient samples fail closed.
- Every private read/write is scoped to the authenticated owner at both API and repository/database layers.
- Snapshot promotion is atomic, idempotent, digest-verified, bounded, and rollback-capable.
- Historical regime joins use only features/labels known at or before the evaluated timestamp.
- Recommendation text is fact-bound decision support, includes uncertainty/counter-evidence, and cannot place trades.

## Attack Surface, Mitigations, and Attacker Stories

### Public APIs and browser rendering

An attacker can submit oversized, malformed, contradictory, or injection-shaped language/query inputs; enumerate strategy IDs; force expensive profile rebuilds; manipulate URLs; or attempt stored/reflected XSS through source-controlled names and product labels. Pydantic bounds, allowlisted sort/search fields, fixed SQL parameters, canonical query plans, HTML escaping in `web/intelligence.html` and `web/compare.html`, response security headers, bounded result counts, and a short server cache reduce this surface. Remaining production controls must include gateway body/rate limits, request timeouts, CSP, centralized error redaction, and load-shedding for cold rebuilds.

Natural-language text is never executable SQL or Python and cannot alter the query schema. Prompt-injection stories become material only if a probabilistic model is later introduced; any such model must output the same validated schema and have no tools, secrets, retrieval credentials, or direct repository access.

### Private user intelligence

An attacker may spoof `X-User-ID`, reuse/replay the trusted-edge token, perform cross-tenant object access, retain history after consent revocation, or infer preferences through exports/errors. The API checks a constant-time bearer value and non-empty bounded identity; service methods scope every object by owner; export/delete/consent tests exist; PostgreSQL RLS provides defense in depth. Deployment must prevent direct public access that bypasses the identity gateway, rotate the edge secret, use TLS, set transaction-local RLS identity, enforce retention jobs, audit access without sensitive payloads, and test direct repository access.

CSRF is lower risk while private authorization uses gateway-injected headers rather than ambient browser cookies. If cookies are introduced, SameSite/secure/httpOnly attributes and CSRF defenses become mandatory.

### Snapshot, evidence, and methodology integrity

A compromised publisher or stolen sync token could promote manipulated aggregates, downgrade a watermark, overload storage, or fabricate evidence quality. Digest/idempotency/watermark/item-count checks and atomic promotion mitigate accidental corruption. Production needs source-to-snapshot reconciliation, short-lived publisher credentials, network restriction, separation of publisher and application roles, append-only audit evidence, signed release records, and tested rollback/restore.

Source data is not assumed safe for display. Metric provenance must retain source watermark and methodology version. Capital-dependent percentage measures must remain unavailable without an explicit capital base; money and fractional units cannot be compared.

### Regime and recommendation integrity

Feed poisoning, stale data, look-ahead leakage, small-sample overconfidence, classifier drift, and explanation hallucination could create misleading recommendations. Immutable as-of features, stale/missing `UNKNOWN` responses, no-lookahead joins, minimum-sample gates, bounded scores, counter-evidence, versioned methodologies, and walk-forward leakage tests mitigate these. A recommendation must never be represented as personalized financial advice or trigger execution.

### Operations and supply chain

Dependency compromise, verbose tracebacks, secret-bearing environment/log output, missing backups, cache staleness, and denial of service are relevant. The container runs as UID 65532 and uses pinned runtime requirements. Production must add dependency/image scanning, SBOM/provenance, structured redacted logs, metrics/traces, database backups and restore drills, cache invalidation monitoring, canary rollout, and automated rollback.

Out of scope are attacks requiring local administrator control over the SQL Server host, container host, developer workstation, or cloud account; such actors already control credentials and runtime. Broker/order compromise is out of scope because the package has no broker connection or execution path.

## Severity Calibration (Critical, High, Medium, Low)

- **Critical:** unauthenticated remote code execution; public extraction of database/edge/snapshot credentials enabling full data compromise; or a remote path from public input to broker/order execution if execution is later added.
- **High:** cross-tenant read/write/delete of private intelligence; bypass of snapshot authorization enabling fabricated current evidence; SQL injection into source/hosted databases; stored XSS that steals privileged operator context; silent look-ahead or unit-confusion that systematically emits materially false high-confidence recommendations.
- **Medium:** denial of service through repeated cold profile builds; consent revocation that leaves history beyond the declared SLO; stale regime data presented as current; reflected XSS with constrained impact; missing auditability or rollback for an otherwise authorized promotion.
- **Low:** disclosure of public aggregate data earlier than intended, minor error-detail leakage without secrets, non-sensitive UI integrity issues, or missing hardening headers where no exploitable chain is demonstrated.

Repository: C:/Users/edebe/eds::epics/ep_051_strategy_directory/hosted_directory
Version: snapshot-79bd958debf7a966d49ee3888bcb00148662510d054b089e3e695f6ff5c7fc47
