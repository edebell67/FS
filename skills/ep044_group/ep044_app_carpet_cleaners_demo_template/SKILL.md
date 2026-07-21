---
name: ep044_app_carpet_cleaners_demo_template
description: Build a premium, reusable sales-demo website for a carpet cleaners business (a clearly-marked sample identity, real verified photography, and a config-free single-file structure ready to adapt per real client). Inherits the master site blueprint at ep044_common_site_blueprint/000_site_blueprint.md, which owns the common page architecture and the normative visual system (font pairing, one shared relative type scale, the per-page image matrix, and the look-and-feel consistency tokens) — this skill supplies only the carpet cleaners-specific content. No thin/light output: the blueprint's Section 6 (Visual system) and Section 14 (Definition of done) set the premium bar every build must meet. Shared colour registry across all ep044_* builds: epics/ep_044_web_apps/PALETTE_REGISTRY.md — check it before choosing a palette so parallel builds never collide. Every build wires the shared AI assistant (epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework) on by default via a self-contained assistant-embed.js with a single ASSISTANT_ENABLED switch-off flag. Use for a carpet cleaners demo/template when real business details are not yet confirmed.
---

# Web App: Carpet Cleaners Demo Template

Build a **premium**, reusable demo site for the carpet cleaners niche — visible results, safe methods, and convenient bookings. Same family and standard as every other `ep044_app_*` template.

## 1. Inherit the master blueprint (non-negotiable)

This skill **must** be built on the master blueprint: `../ep044_common_site_blueprint/000_site_blueprint.md`. Load it first and treat it as authoritative. It owns, so this skill never re-invents them:

- **Common page architecture** (blueprint Section 2/3): Home, Services + individual service pages, Gallery/Our Work, Before & After, Reviews, About, Pricing Guide, Areas Covered, Knowledge Centre, FAQ, Contact, Request a Quote, and legal pages.
- **The premium visual system** (blueprint Section 6): the fixed font pairing (`Cormorant Garamond` + `Outfit` + `JetBrains Mono`), the single shared **relative** modular type scale (every size in `rem`/`clamp`, sized in proportion so headings, body and meta complement each other), the **image matrix** (required images per page), and the **look-and-feel tokens** (colour via `:root`, spacing, radius, motion).
- **Trust, Conversion, SEO, Accessibility, Performance** (blueprint Sections 5, 7–10).

This skill adds only the carpet cleaners-specific content below. **A thin, image-poor screen is not acceptable** — the blueprint's definition of done applies.

## 2. Which skill applies — decision rule

- **All evidence fields blank/placeholder** (no confirmed name/address/phone) → this skill. Build a clearly-fictional but realistic sample identity and place output under `epics/ep_044_web_apps/<template-name>/`. Add the footer disclosure: `Business name, address, phone and prices are sample placeholders for this reusable template — replace with real details per client.`
- **Real evidence exists** (a real address/phone/niche confirmed via citation) → adapt this structure with the real facts and place output under `epics/ep_006_website_rebuilds/redesigns/<business-slug>/`. Never fabricate stats, ratings, reviews, accreditations, or years established.

## 3. Design system — defer to the blueprint, choose the palette here

Fonts, type scale, spacing, radius, and motion come **verbatim from blueprint Section 6** — do not redefine them. Apply them via `:root` custom properties in a single `styles.css`.

- **Palette**: fresh, clean tones (crisp blue / aqua / bright neutral). Read `epics/ep_044_web_apps/PALETTE_REGISTRY.md` first, propose 2–4 candidates genuinely distinct from every existing row, apply the chosen one via `:root` only, grep the finished file for stray hex values outside `:root`, then append this site's row to the registry in the same turn.

## 4. Category content model — Carpet Cleaners

- **Services**: carpet cleaning, upholstery, rugs, stairs, pet odour treatment, stain treatment, end-of-tenancy, and commercial cleaning.
- **Qualification data** (feeds the quote form and AI qualification): fabric or carpet type, rooms, approximate area, stains, pets, parking, and preferred date.
- **Trust signals**: equipment, drying times, product safety, insurance, child/pet considerations, and commercial credentials. Use only honest, non-fabricated differentiators.
- **FAQs**: drying, moving furniture, stain guarantees, preparation, and re-soiling.

## 5. Imagery — map the blueprint image matrix to carpet cleaners

Follow the blueprint's per-page image matrix and its mandatory sourcing/verification workflow (real photos only, verified HTTP 200 before use, no reuse across sibling sites, every `<img>` must load). Carpet Cleaners-specific subjects for each slot:

- **Hero (1)**: a freshly cleaned carpet or a professional cleaning machine mid-work.
- **Two split/feature sections (1 each)**: **Carpets & rugs** (deep cleaning, stairs, stain and pet-odour treatment) and **Upholstery & commercial** (sofas, upholstery, end-of-tenancy, commercial contracts), alternating image side.
- **Homepage gallery preview strip (4)** and **dedicated `gallery.html` (9–10, editorial masonry, captioned by sub-category)**: stain-removal and room transformations, honest side-by-side results (never overstated).
- **Before & After (where shown)**: honest original-vs-completed pairs.
- **Search queries** for sourcing: `clean-carpet`, `carpet-cleaning-machine`, `upholstery-cleaning`, `spotless-living-room`. Vary composition (wide/detail, premises/in-action).

## 6. Conversion

Category CTAs: **Get an Instant Estimate**, **Book a Cleaning**, and **Send Photos of the Stain**. Keep the blueprint's conversion hierarchy (inspire → trust → explain → remove objections → request the enquiry) and a prominent phone number on mobile and desktop.

## 7. AI assistant integration — default on, one-flag off

Every build ships with the shared AI assistant wired in **by default** (blueprint Section 4). Create a self-contained `assistant-embed.js` that injects the widget from the shared Render-hosted service, guarded by a single `const ASSISTANT_ENABLED = true;` flag (flip to `false` to disable, no HTML edits). Add `<script src="assistant-embed.js"></script>` after `reveal.js` on every visitor-facing page. Register the site as a tenant via the framework admin API (`POST /api/admin/clients`, never by hand-editing `data/clients.json`); seed `knowledge` (location/services/pricing derived from the site copy, never invented) and `pages` (real nav anchors, tagged with blueprint keys so the assistant's shortcut buttons resolve). Verify: `GET /api/public/config` resolves the tenant and one `POST /api/public/chat` returns a grounded answer.

## 8. Output location, verification, and task tracking

- **Output**: `epics/ep_044_web_apps/<template-name>/` — `index.html`, `gallery.html`, `styles.css` (`:root` tokens + all component styles), `reveal.js`, `assistant-embed.js`. No `config.js`.
- **Verify before done** (blueprint Section 14): serve locally and confirm every `<img>` on every page loads (`complete: true`); type scale, spacing and components match the blueprint; section image counts match the matrix; `tel:`/`mailto:` are consistent with the sample identity; no console errors; responsive, keyboard-accessible, reduced-motion respected.
- **Task tracking**: per this repo's `CLAUDE.md`, create a workstream task file in `workstream/300_complete/claude/` once built and verified.

## Required shared layout invariant

Apply §6.4 **Mandatory page-edge and footer contract**, §6.1 **Inner-page editorial hierarchy**, and §6.2 **Gallery relevance** from `ep044_common_site_blueprint/000_site_blueprint.md` without exception. The business identity/logo block, header navigation, hero copy, page content, card/form outer edges and footer content must share one responsive left gutter. Use the normal-flow sticky-footer shell for short pages; never independently centre the header or use a fixed footer. The home hero remains the largest display moment; inner-page headings require an explicitly styled, distinct premium serif face at a smaller scale, with a compact mono kicker and restrained sans-serif lede—never browser-default inner-page text. Every gallery must contain real category-relevant visual assets, never empty cards, generic decoration or “images coming later” copy. When owner work is unavailable, use provenance-recorded, clearly labelled illustrative category imagery that does not claim work by the named business. Verify live geometry, type and image loads after cache-busting production CSS.
