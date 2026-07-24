# ep_047 Project Status — Business Activation Directory Platform

**Written:** 2026-07-24
**Status:** Built, tested, verified live locally. Committed and pushed to GitHub. **Not yet
deployed anywhere public.**
**Branch:** `ep047-directory-app` on `github.com/edebell67/FS`, PR
[#1](https://github.com/edebell67/FS/pull/1) open against `master`, not yet merged.
**Audience:** any AI model or engineer picking this up next — assume zero prior context. This
document exists so the next session doesn't have to re-derive any of this from git log or by
re-reading the whole build conversation.

---

## 1. One-paragraph summary

Starting from a project brief (`PROJECT_PROMPT.md`), this built a Next.js/TypeScript/Tailwind
app on Postgres/Drizzle: a CSV/JSON business importer with real-time validation, duplicate
detection, and rollback; a public business directory (homepage, category/town listings,
keyword search, business profile pages with schema.org JSON-LD); and an admin console
(dashboard, an 8-column Kanban pipeline board with a working stage-move action, business
detail/timeline pages). Every phase was verified against a **live** local Postgres database and
a **live** browser, not just unit tests — including two real bugs that were only found because
real (messy) data was used instead of synthetic test fixtures. The app was then restructured so
its public and admin routes can later be mounted at `thetechprinciple.com/directory` and
`thetechprinciple.com/directoryadmin` respectively, without touching the existing live site at
`thetechprinciple.com/`. Everything is committed and pushed to GitHub. **Nothing is deployed to
the public internet yet** — that's the next task (see §7).

---

## 2. Where things are, precisely

| What | Where |
|---|---|
| App code | `epics/ep_047_directory_app/` in `github.com/edebell67/FS` |
| Branch | `ep047-directory-app` (2 commits ahead of the point it branched from `master`) |
| PR | `https://github.com/edebell67/FS/pull/1` — open, not merged, mergeable |
| Local dev DB | Postgres 17, `localhost:5432`, database `ep047_directory` (credentials: see `api_server_pg/.env` in the repo root — shared local Postgres instance used by other apps in this workspace too, this app has its own separate database within it) |
| Local dev server | `epics/ep_047_directory_app/start_app.bat` — installs deps, checks Postgres, starts `npm run dev` on port 8140 |
| Local data as of last check | 832 real businesses (imported from `UK_Ltd_email_no_website_VERIFIED_410.csv` at the repo root, plus a second real import of a larger file during the session), 31 categories, 39 towns |
| Full build/decision history | `epics/ep_047_directory_app/PLAN.md` (architecture decisions + phase-by-phase completion tests) and `README.md` (what's built, what's verified, gotchas found) |
| Deployment task | `workstream/100_backlog/general/20260724_072234_ep047_997_render_production_deployment.md` |

---

## 3. What was built, in order

### Phase 0 — Foundation
Next.js 15 + TypeScript + Tailwind + Drizzle ORM scaffold, matching this workspace's existing
conventions (`epics/ep_010_.../package.json` for the stack choice, `epics/ep_043_.../render.yaml`
for the deploy-blueprint pattern). `/api/health` route, migration runner, seed script. Verified
against a real Postgres connection (`{"status":"ok","db":"connected"}`), not just that it built.

### The data model
`businesses`, `pipeline_stages` (22 stages seeded, each mapped to one of 8 Kanban board columns),
`stage_transitions` (append-only — this is the audit trail), `import_batches`,
`import_row_errors`, `category_sequences` (backs the gapless-per-category `business_ref`
sequence, e.g. `TP-PLUMB-000001`). The core design rule, stated explicitly in `PLAN.md` §1:
**state is a projection, history is the source of truth** — `businesses.currentStageId` is only
ever written in the same transaction as the `stage_transitions` row that justifies it
(`lib/db/queries/pipeline.ts`'s `moveBusinessToStage` is the one function that does this). The
`business_ref` column is immutable, enforced by a Postgres trigger — tested directly by trying
to `UPDATE` it in `psql` and confirming it raises.

### CSV/JSON importer
Drag-and-drop upload UI (`ProgressBar` shows real upload percentage via
`XMLHttpRequest.upload.onprogress`, not a fake timer), column-alias resolution (so
`"business name"`, `"Business Name"`, `"name"` all map to the same field), per-field validators,
duplicate detection (exact email/phone/website match, plus normalized name+postcode match for
businesses with no contact info at all), rollback by batch. Backed by 16 unit tests run against
an in-memory repository (no DB needed for the test suite itself).

**Two real bugs found via real data, both fixed:**
1. A malformed *optional* field (e.g. two phone numbers crammed into one CSV cell) was rejecting
   the entire business, not just that field. Fixed: only a missing *required* field (name,
   category) blocks a row now; a bad optional field is dropped with a `warning`, and the
   business still imports.
2. Duplicate detection against the database only checked email/phone/website — a business with
   none of the three (common in the real dataset) could never be caught as a re-import of an
   existing record, only as a duplicate within the same file. Fixed by adding a normalized
   name+postcode SQL comparison to the existing-record check, mirroring the in-batch JS logic.
   Confirmed live: re-uploading a sample that included a no-contact-info business went from
   incorrectly re-inserting it to correctly flagging it as a duplicate.

### Public directory
Homepage (live counts, category/town browse, A-Z index, newest listings, search bar), category
and town listing pages, search (keyword — now correctly spans name/category/town/county, not
just name — see the "search bug" note below), business profile pages with breadcrumbs,
`LocalBusiness` + `BreadcrumbList` JSON-LD (verified by parsing the actual `<script
type="application/ld+json">` tags out of the rendered page), a deliberately-**disabled** "Claim
this business" button with honest "coming soon" copy rather than a CTA that looks live but does
nothing.

**One more real bug found via real data:** the search box's placeholder promised "name,
category, or town" but the underlying query only actually matched name/email/phone/ref/postcode
— searching a town name returned zero results. Fixed by widening the `ilike` match; this is the
same `listBusinesses` function used by every listing page and the admin businesses list, so the
fix applied everywhere at once.

Deliberately not built (the data doesn't support it): photos, map, opening hours, "featured"
listings, radius/location search — the source CSV has no images, hours, or lat/lng for any
business.

### Admin console
Dashboard (live totals, imports today/week/month, stalled-past-SLA count, recent-activity feed),
an 8-column Kanban pipeline board (count / movement-today / avg-time-in-stage / blocked per
column, a "move to stage" dropdown+button per business card instead of drag-and-drop — a select
accomplishes the same functional outcome without a DnD library dependency), business detail
pages with the full append-only timeline, a businesses list with search/filter (by category,
town, pipeline stage, or Kanban board column) and pagination.

**Verified with a real stage move, not a mocked one:** moved a real business through
Imported → Validated → back to Imported using the actual UI, and confirmed via direct `psql`
queries at each step that exactly one new `stage_transitions` row was written per move (the
prior history was never overwritten), the board's column counts updated correctly, and the
detail page's timeline rendered all 3 transitions in order.

**One CSS bug found and fixed:** the Kanban board initially rendered as a single stacked column
instead of 8 side-by-side ones. Cause: Tailwind's `grid-cols-1` utility isn't cleared just
because a breakpoint variant (`sm:grid-flow-col`) is also present — the
`grid-template-columns: repeat(1, ...)` persisted at every screen size. Fixed by explicitly
clearing it (`md:grid-cols-none`) before the auto-flow columns take over. Only caught by testing
at desktop viewport width — the default narrow preview viewport happened to hide the bug (mobile
stacking looks identical to the broken desktop layout).

### URL restructure (most recent work)
The user's actual deployment target is `thetechprinciple.com/directory` (public) and
`thetechprinciple.com/directoryadmin` (admin), alongside the existing unrelated site at
`thetechprinciple.com/` (built in a different epic, `epics/ep_046_thetechprinciple` — **never
touched by any of this work**). Next.js only supports one `basePath` per app instance, which
can't give two route groups two different prefixes — so every route folder was physically moved
instead: `app/*` → `app/directory/*`, `app/admin/*` → `app/directoryadmin/*`, the admin-only
import API → `app/directoryadmin/api/import*`. `/api/health` deliberately stayed unprefixed,
since Render's own health check hits the app's own domain directly, not through whatever
reverse-proxy eventually sits in front of `thetechprinciple.com`. `/` now redirects to
`/directory`. Every internal link, form action, fetch/XHR target, canonical URL, and JSON-LD
field was updated to match and re-verified live — including a real import + rollback
round-tripped through the new `/directoryadmin/api/import` path.

---

## 4. Verification standard used throughout

Every phase in this build was checked against the **live** local Postgres database and the
**live** browser — never just "the code looks right" or "the tests pass." Concretely, this
meant: direct `psql` queries to confirm what the UI showed matched what was actually in the
database; JSON-LD extracted from the rendered DOM and parsed, not just assumed correct from
reading the code; a `curl` smoke test of every route after every significant change, including
after clean production-build-and-restart cycles; real stage moves through the pipeline
confirmed via the database, not just "the button didn't error." `npm test` (16/16), `npm run
typecheck`, and `npm run lint` are all clean as of the last commit, and `npm run build` produces
the exact 14-route output documented in the deployment task file.

---

## 5. What's explicitly NOT built (don't be surprised by this)

- **Authentication/roles.** The entire admin console is reachable by anyone with the URL — no
  login exists. This is the single most important thing to flag before this goes anywhere public.
- **`events` and `audit_log` tables**, the 12 analytics charts, notifications, verification
  email sending — all Phase 5/6 in `PLAN.md`, not started.
- **True drag-and-drop** on the pipeline board (a select dropdown is used instead — functionally
  equivalent).
- **Bulk/multi-select actions.**
- **Photos, map, opening hours, radius search** on the public directory — no source data
  supports them yet.
- **The actual `thetechprinciple.com` domain connection.** The app is *structured* to support it
  (see the URL restructure above) but nothing has been deployed anywhere, and no reverse-proxy/
  DNS work has been done. This depends on an open question — how is `thetechprinciple.com`
  currently hosted? — that hadn't been answered as of this document being written.

---

## 6. Two things to tell the user, unprompted, the next time you talk to them

1. **The admin console has no authentication.** If this gets deployed and especially if it gets
   linked from `thetechprinciple.com`, anyone who finds `/directoryadmin/*` can import data, roll
   back imports, and move businesses through the pipeline. Worth deciding whether that's
   acceptable short-term or whether auth needs to come first.
2. **`thetechprinciple.com` routing is still an open question.** The user was asked how that
   domain is currently hosted (Render? Vercel? something else?) so the eventual reverse-proxy/
   rewrite rules for `/directory*` and `/directoryadmin*` could be planned — that question
   hadn't been answered as of this document. Ask again before attempting the domain connection.

---

## 7. Next step

See `workstream/100_backlog/general/20260724_072234_ep047_997_render_production_deployment.md`
for the fully detailed, ready-to-execute task: deploying this app to Render (its own URL, not
yet the `thetechprinciple.com` domain — that's a further follow-up once the routing question
above is answered).
