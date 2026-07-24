# ep_047 — Implementation Plan

Companion to [PROJECT_PROMPT.md](PROJECT_PROMPT.md). This is the build order, the schema, and
the decisions that have to hold at 500k businesses so nothing gets rewritten later.

Drafted 2026-07-23. No code written yet.

---

## 1. Architecture decisions

These are the choices that are expensive to reverse. Each has a recommendation and the reason.

| Decision | Recommendation | Why |
|---|---|---|
| Framework | **Next.js 14, App Router, TypeScript** | Matches `ep_010`. One deployable serving both the public directory (SSG/ISR, SEO-critical) and the admin console (dynamic, auth-gated). Route handlers cover the API without a second service. |
| Styling | **TailwindCSS 3.4** | Per brief and repo precedent. |
| DB access | **Drizzle ORM + `pg`** | SQL-first — the schema below is written once and Drizzle generates types from it, rather than the schema being a byproduct of an ORM DSL. Migrations are plain checked-in SQL, which matters given the repo already versions SQL under `sql_scripts/`. *Alternative:* Prisma, better DX, but its migration engine and query layer fight raw partitioning and FTS, both of which this design needs. |
| Search | **Postgres FTS (`tsvector` + GIN) + `pg_trgm`** for fuzzy name matching | Keeps search in the DB to ~1M rows. No Elasticsearch until measured need; the schema below leaves a clean seam to add one. |
| Geo / radius | **PostGIS `geography(Point,4326)` + GIST index** | Correct radius maths and cheap `ST_DWithin`. Render Postgres supports the extension. *Alternative:* `cube`+`earthdistance` is lighter but degrades near poles and has a worse index story. |
| Auth | **Auth.js (NextAuth) with credentials + DB sessions** | Roles live in our own tables (six roles now, Business Owner later) so the session only carries a user id. |
| Hosting | **Render:** one Web Service + one Postgres instance, `render.yaml` blueprint | Per brief; matches `ep_043`'s deployment pattern. |
| Background work | **Postgres-backed job table + worker route**, not a queue service | Imports of 100k rows, email sends, and analytics rollups need to survive a request timeout. A `jobs` table with `SELECT … FOR UPDATE SKIP LOCKED` is enough at this scale and adds no infrastructure. |

### The one structural rule

**State is a projection; history is the source of truth.** `businesses.status` is a cached
current-stage pointer. It is only ever written by the same transaction that appends a
`stage_transitions` row. Same for `events` and `audit_log` — append-only, never updated,
never deleted, never aggregated at write time. Every dashboard number is derived. This is what
makes "never lose history" enforceable rather than aspirational.

---

## 2. Data model

Core tables. Full DDL lands in `migrations/0001_init.sql` in Phase 1.

### `businesses` — current-state projection

Holds the 28 fields from the brief. Notable columns:

- `id uuid PRIMARY KEY DEFAULT gen_random_uuid()` — internal join key.
- `business_ref text UNIQUE NOT NULL` — the permanent public identifier, `TP-PLUMB-000001`.
  Immutable, enforced by a trigger that raises on UPDATE.
- `slug text UNIQUE NOT NULL` — SEO URL, derived from name + town, collision-suffixed.
- `current_stage_id int REFERENCES pipeline_stages(id)` — projection, see rule above.
- `stage_entered_at timestamptz` — powers "stalled" and "average time in stage" without a scan.
- `location geography(Point,4326)` — generated from lat/lng.
- `search_doc tsvector` — generated column over name, trading name, town, county, postcode,
  category, description, tags. GIN indexed.
- `import_batch_id uuid REFERENCES import_batches(id)` — makes rollback a single delete.
- `tags text[]`, `notes text`, `internal_notes text`.
- Partial indexes for the admin console's hot filters: missing email, missing phone,
  missing website, stalled.

**Business ref generation:** `category_sequences(category_code text PK, next_val bigint)`,
incremented with `UPDATE … RETURNING` inside the insert transaction. Atomic, gapless per
category, no advisory locks.

### `pipeline_stages` — configurable, not an enum

The 22 default stages are seed rows, not a Postgres enum, because the brief says the pipeline
is configurable. Columns: `key`, `label`, `sort_order`, `board_column` (which of the 8 Kanban
columns it rolls up into), `is_terminal`, `sla_hours` (drives "stalled" and "blocked").

### `stage_transitions` — append-only

`business_id`, `from_stage_id`, `to_stage_id`, `occurred_at`, `actor_user_id`, `source`
(`import` | `admin` | `api` | `automation` | `owner`), `reason`, `notes`. Composite index on
`(business_id, occurred_at)` serves the timeline; `(to_stage_id, occurred_at)` serves the
funnel and velocity charts.

### `events` — raw, permanent, partitioned

`business_id`, `type`, `occurred_at`, `actor_user_id`, `source`, `payload jsonb`,
`ip`, `user_agent`. **Range-partitioned by month on `occurred_at`** from day one — retrofitting
partitioning onto a live 50M-row table is the exact "architectural redesign" the brief forbids.
Analytics read from partitions directly; a nightly rollup into `metrics_daily` backs the charts
without ever mutating raw events.

### `audit_log` — append-only

`entity_type`, `entity_id`, `field`, `old_value`, `new_value`, `changed_at`, `actor_user_id`,
`reason`. Written by a generic trigger on `businesses` (and later on any table we opt in), so
coverage does not depend on application code remembering.

### Supporting tables

`import_batches` (filename, source, uploaded_by, row counts, status, rollback state) ·
`import_row_errors` (batch, row number, column, raw value, error code — this is the error
report) · `users`, `roles`, `user_roles`, `sessions` · `notifications` · `jobs` ·
`metrics_daily` · `categories` / `subcategories`.

---

## 3. Build phases

Each phase is independently deployable and has an explicit completion test. Phases 0–4 are the
production MVP; 5–7 complete the brief.

### Phase 0 — Foundation
Scaffold Next.js 14 + TS + Tailwind. `render.yaml` with web service + Postgres. Health check
route. Drizzle config, migration runner, seed script. CI: typecheck, lint, test.
**Test:** `npm run build` clean; app deploys to Render and `/api/health` returns 200 against a
live Postgres.

### Phase 1 — Data layer
Full schema migration, all indexes, the immutability and audit triggers, monthly partition
helper, seed of 22 pipeline stages and the category tree.
**Test:** migration applies to an empty DB and is idempotent on re-run; a test asserts that
`UPDATE businesses SET business_ref = …` raises; a test asserts an update to any audited column
writes an `audit_log` row.

### Phase 2 — CSV/JSON importer — **done, verified live**
Drag-and-drop upload (`app/admin/import/page.tsx`), real upload-progress bar via XHR, column
validation, per-row validators (email, website, phone, lat/lng), duplicate detection (exact on
email/phone/website + normalized name+postcode — trigram is still a TODO, see PLAN.md §1),
category assignment, ref generation, error report, import summary, rollback by batch. CSV and
JSON both go through the same pipeline (`lib/import/pipeline.ts`).
**Test:** met — verified against a live local Postgres (not the 50k-row/streamed-parse scale
target below): uploaded real CSV and JSON files through the actual browser UI (drag-drop),
got correct accept/reject/duplicate counts and per-row error detail, confirmed the DB rows
(`business_ref`, pipeline stage, stage_transitions) match, rolled back and confirmed cascade
delete. 13 unit tests cover the pipeline logic directly.
**Deferred to a later pass:** streamed parsing for files too large to buffer in memory, the
job-table/progress-polling architecture for imports that outlive a request lifetime, and the
50k-row load test — all three matter once real import files are bigger than a few thousand
rows; nothing about the current design blocks adding them.

### Phase 3 — Public directory — **done for what the data supports, verified live**
Homepage (category/town counts, A–Z index, newest listings, keyword search bar), category
listing (`/category/[slug]`), town listing (`/town/[slug]`), search (`/search` — keyword across
name/category/town/county/email/phone/ref/postcode, category filter, town filter, A–Z letter
filter), business profile (`/business/[slug]` — breadcrumbs, contact details, social links,
related businesses (same category), nearby businesses (same town), disabled "claim" CTA with
honest "coming soon" copy rather than a dead-end button), pagination, sorting (name or newest),
`LocalBusiness` + `BreadcrumbList` JSON-LD, per-page SEO metadata.
**Test:** met, against the live 410-business dataset, not a seeded fixture — homepage counts
(410/30/29) match `psql`; category page (`/category/barbers`) shows the correct 13 businesses,
alphabetical; town page (`/town/birmingham`) shows the correct 80; business profile JSON-LD
extracted from the rendered page via `document.querySelectorAll('script[type="application/
ld+json"]')` and parsed as valid `LocalBusiness`/`BreadcrumbList`; search for a town name
("gloucester") correctly returned 5 cross-category matches once the query was widened to
include category/town/county (originally missed — see Notes below); all 10 routes return 200
on a clean build+restart.
**Deliberately not built (data doesn't support it yet):** photos, map, opening hours, "featured"
businesses, radius search — the source CSV has no lat/lng, images, or hours for any of the 410
rows. Radius/location search needs geocoding first; nothing here blocks adding it once
coordinates exist. Also not built: ISR/ISG caching (everything is `force-dynamic` for now —
fine at 410 rows, revisit before Phase 7's 500k-row target), sitemap.xml, ownership/claim flow
(needs Phase 4 auth first).

### Phase 4 — Admin console — **dashboard + pipeline board done, verified live; auth deferred**
Dashboard (businesses/categories/towns, avg time in pipeline, imports today/week/month, stalled
count, recent activity feed). Kanban pipeline board — all 8 columns (count / movement today /
avg time / blocked), a capped preview of businesses per column with a manual "move to stage"
action, a "View all N →" link into the businesses list filtered by board column. Business
detail page (`/admin/businesses/[businessRef]`) with the full append-only timeline. The
businesses list gained a `stage`/`column` filter so board links resolve to something real.
**Test:** met, live — dashboard's 410/30/29/2h/stalled-0 all reconciled against direct `psql`
queries; moved a real business (Raynes Architecture Ltd) Imported → Validated via the board's
dropdown, confirmed in `psql` that `current_stage_id` updated and exactly one new
`stage_transitions` row was added (the import-time transition untouched); moved it back,
confirmed 3 total transitions and the detail page's timeline rendering all of them correctly;
board-column filter (`/admin/businesses?column=Validated`) correctly returned exactly the 1
business now in that column.
**Deliberately deferred:** Auth.js + the six roles (everything here is unauthenticated — same
gap as the rest of the site so far), true drag-and-drop (the board uses a select+button "move
to stage" instead — functionally equivalent, no DnD library needed), multi-select bulk update,
and the events/audit_log tables (Phase 5). The 1s-at-100k-businesses load target is untested —
current data is 410 rows.

### Deployment target restructure — done, verified live
Real requirement, not in the original brief: this app needs to live at
`thetechprinciple.com/directory` (public) and `thetechprinciple.com/directoryadmin` (admin),
alongside the existing unrelated ep_046 site at `thetechprinciple.com/`. Next.js only supports
one `basePath` per app, which can't give two route groups two independent prefixes — so every
route folder was physically moved: `app/*` → `app/directory/*`, `app/admin/*` →
`app/directoryadmin/*`, `app/api/import*` → `app/directoryadmin/api/import*` (admin-only, so
nested with it), `app/api/health` stayed at the root (Render's own health check hits this app
directly, not through the `thetechprinciple.com` proxy). Every internal link, form action,
fetch/XHR target, canonical URL, and JSON-LD field was updated to match. `/` now redirects to
`/directory`. See the epic README's "URL structure" section for the full path table.
**Test:** met, live — all routes return 200, the old flat paths correctly 404, a real
import+rollback round-tripped through `/directoryadmin/api/import`, and a business profile's
`LocalBusiness`/`BreadcrumbList` JSON-LD and `<link rel=canonical>` all resolved to the new
`/directory/business/...` URL. Re-verified against the live dataset (832 businesses at the time
of this change, up from 410 — a second real import had happened between sessions).

### Phase 5 — Events, audit and analytics
Event emission across every action in the brief's list, nightly rollup job, the 12 analytics
charts, conversion funnel, pipeline velocity, geographic distribution.
**Test:** each listed event type is emitted by its trigger action and is queryable raw; chart
totals match raw-event counts for the same window.

### Phase 6 — Operations layer
All 11 dashboard widgets, notification centre with the full notification list and severity
levels, verification queue, claims queue, publishing queue.
**Test:** each widget links to a working filtered view; each notification type fires from its
source condition.

### Phase 7 — Hardening
Load test at 500k businesses. Query plan review on every hot path. Rate limiting. Backups and a
rehearsed restore. Error tracking. Runbook.
**Test:** search, board and dashboard all hold their p95 targets at 500k rows.

### Deliberately deferred

Website Generator, AI Assistant, CRM, email/SMS campaigns, payments, subscriptions, customer
portal, knowledge base, analytics AI, recommendations, lead scoring, marketing automation. The
schema accommodates them — `events`, `jobs` and the stage table are the seams — but none are in
this build.

---

## 4. Repository layout

```
epics/ep_047_directory_app/
  app/
    (public)/                 directory — homepage, categories, towns, search, profile
    admin/                    console — dashboard, pipeline, businesses, imports, analytics
    api/                      route handlers
  lib/
    db/                       drizzle schema, client, queries
    import/                   parsers, validators, duplicate detection
    pipeline/                 stage transitions, guards
    events/                   emitters
    auth/
  migrations/                 checked-in SQL
  scripts/                    seed, partition maintenance, load-test fixtures
  tests/
  render.yaml
```

---

## 5. Open questions

Answers change the build; none block starting Phase 0.

1. **Category taxonomy** — is there a fixed category/sub-category list, or is it derived from the
   first CSV? Affects the `TP-PLUMB` ref code allocation.
2. **Sample CSV** — a real file would let Phase 2's validators be written against actual data
   rather than assumed columns.
3. **Geography** — UK-only (postcode validation, county lists) or international?
4. **Volume at launch** — the row count of the first real import sets the Phase 7 load target.
5. **Verification email** — which provider, and is open/click tracking expected from day one?
   The pipeline has four verification stages that need a sender behind them.
