---
name: ep044_app_barber_hair_demo_template
description: Build a generic, reusable sales-demo website template for a barbershop / hair salon business covering both classic barbering (fades, beard trims, hot towel shaves) and hair styling (cut, colour, blow-dry) when no real evidence (address/phone/name) is available yet — a clearly-marked sample identity, real verified barbershop/salon photography, and a config-free single-file structure ready to be adapted per real client later. Use when asked for a barber/hairdresser demo or template with placeholder or missing business details. Reference implementation: epics/ep_044_web_apps/hartleys-barber-hair-template. Shared colour registry across all ep044_*-family builds: epics/ep_044_web_apps/PALETTE_REGISTRY.md — check it before picking a palette so multiple agents building sites in this family never collide. Every build wires the shared AI assistant (epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework) on by default via a self-contained assistant-embed.js with a single ASSISTANT_ENABLED flag as the switch-off. Sibling skill ep044_app_beauty_tanning_demo_template covers the real-evidenced-business pattern for hair/beauty/tanning; this skill is for the no-evidence-yet, reusable-template case for barbering and hair styling.
---

# Web App: Barber & Hair Studio Demo Template

Build a generic, reusable demo site for the barbering/hair-styling niche when there is **no real business identified yet** — same family as `ep044_fix_finish_demo_template`/`ep044_app_tiling_demo_template`, not the real-evidenced-business pattern.

## Inherit the master blueprint (non-negotiable)

Build on the master blueprint `../ep044_common_site_blueprint/000_site_blueprint.md` — load it first and treat it as authoritative for the **common page architecture** (blueprint Section 2/3) and the **premium visual system** (blueprint Section 6: the fixed `Cormorant Garamond` + `Outfit` + `JetBrains Mono` pairing, the single shared **relative** modular type scale, the per-page **image matrix**, and the `:root` look-and-feel tokens), alongside trust, conversion, SEO, accessibility and performance. The category-specific detail in this skill **extends** the blueprint and must never drop below its Section 14 definition of done — no thin, image-poor screens. Where this skill already names fonts, image counts, or sourcing steps, they match the blueprint's shared system; keep them aligned rather than divergent.

## Which skill applies — decision rule

- **All evidence fields blank/placeholder** (`????`, empty, "TBC") → this skill. Build with a clearly-fictional but realistic sample identity, place output under `epics/ep_044_web_apps/<template-name>/`.
- **Real evidence exists** (a real address, phone, niche confirmed via a citation) → use `ep044_app_beauty_tanning_demo_template`'s pattern instead and place output under `epics/ep_006_website_rebuilds/redesigns/<business-slug>/`.
- If a real barbershop/hair salon is identified *later*, adapt this reference build's structure/copy with the real facts rather than starting from scratch.

## Deciding barbershop vs. hair salon vs. both

Real leads in this niche split into distinct sub-categories — `barbers` and `hairdressers` (and `mobile hairdressers`, a service-area variant, see note below). The reference build (`hartleys-barber-hair-template`) deliberately covers **both** under one identity — a unisex studio offering classic barbering (fades, beard work, hot towel shaves) alongside hair styling (cut, colour, blow-dry) — because that's a common, credible real-world business shape and it lets one template serve two lead categories at once. If a real client is clearly one or the other only (a traditional barbershop with no styling chairs, or a salon with no barbering), trim the section catalog to match rather than forcing both split sections.

**Mobile hairdressers** are a distinct enough business model (no fixed shop, "we come to you") that this fixed-premises template shouldn't be stretched to cover them — that needs its own service-area-first copy (no walk-in trust pills, a coverage-area map/list instead of a shop address) if built.

## Sample identity convention

Invent a plausible-but-clearly-fictional business identity (name, address, phone, email). Mark this explicitly with a footer disclosure line: `Business name, address, phone and prices are sample placeholders for this reusable template — replace with real details per client.` No fabricated stats/ratings/years-established claims — use honest generic differentiators (`Walk-ins welcome`, `Evening appointments`, `Local to <area>`).

## File structure

```
epics/ep_044_web_apps/<template-name>/
├── index.html            Single file, all sections, hard-coded sample content
├── gallery.html           Dedicated editorial masonry gallery page
├── styles.css             :root tokens + every component style
├── reveal.js              Self-contained copy of the standard IntersectionObserver reveal script
└── assistant-embed.js     AI assistant loader with an ASSISTANT_ENABLED switch-off flag — see below
```

No config.js — same reasoning as every sibling in this template family.

## Design system

- **Fonts**: `Cormorant Garamond` (serif headings) + `Outfit` (sans body/UI) + `JetBrains Mono` (eyebrows, prices) — same pairing as every sibling in this family of skills.
- **Palette**: the reference build uses burgundy (`--ink: #241a1e`, `--accent: #8a2f3d`) — a classic barbershop-red without repeating the softer dusty-rose already used by the nail bar template. Read `epics/ep_044_web_apps/PALETTE_REGISTRY.md` before picking a palette for a new build, propose 2–4 candidates genuinely distinct from every row, apply the chosen one only via `:root` custom properties, grep the finished file for old/placeholder hex values to catch hardcoded duplicates outside `:root`, then append the new site's row to the registry in the same turn.
- **"Lots of images" matters here too** — the studio itself and the work are the sales pitch. Real, verified photography throughout: hero, both split sections, a 4-image homepage gallery preview, and a full 9–10 image editorial masonry gallery page.

## Section catalog

1. **Navbar** — brand + tagline, anchor links (Services / Barbering / Hair Styling), `Gallery` page link, `Book Now` nav-button.
2. **Hero** — eyebrow (sample location), italic-accented `<h1>`, one-sentence lede covering both barbering and styling, dual CTA (call + view services), honest trust pills (`Walk-ins welcome`, `Evening appointments`, `Local to <area>`), real hero photo (a barber chair or studio interior reads best).
3. **Services menu** — priced list spanning both disciplines: classic haircut, skin fade & tidy-up, beard trim & hot towel shave, cut & blow-dry, colour & highlights, kids' cut.
4. **Two split sections** — "Barbering" (fades, beard work, hot towel shaves) vs. "Hair Styling" (cut, colour, blow-dry, special occasion). Each with eyebrow/h2/paragraph/4-item feature list/real photo, alternating image side via `.split-item.reverse`.
5. **Gallery preview strip** — 4 images on the homepage linking to the full gallery, mixing studio-interior and in-session shots.
6. **Why row** (dark section) — walk-ins welcome, qualified stylists, evening appointments are the strongest niche-appropriate trust points.
7. **Contact CTA** — dark box, call + email buttons.
8. **Footer** — brand/address, contact column, tech badge, sample-data disclosure line.
9. **`gallery.html`** — CSS `column-count` masonry, 9–10 photos captioned by category (`Studio` / `Barbering` / `Styling`), exhibition-style captions (italic title + small mono category label).

## Image sourcing workflow

Same discipline as every sibling in this family:
1. `WebSearch`/`WebFetch` Unsplash search pages for barbershop/hair-salon themes — good queries: `barbershop`, `hair-salon-interior`. Never guess a `photo-<id>` from memory.
2. Skip `plus.unsplash.com` results (paid tier).
3. `curl -s -o /dev/null -w "%{http_code}" "https://images.unsplash.com/photo-<id>?auto=format&fit=crop&q=80&w=1000"` must return `200` for every candidate before it goes in HTML.
4. Check for accidental reuse across sibling sites (`grep -r "photo-<id>" epics/ep_044_web_apps`).
5. Vary composition — mix studio-interior shots (chairs, mirrors, signage) with in-session action shots (cutting, shaving) so barbering and styling both feel represented, not just one or the other.

## Verification

Serve locally (`python -m http.server <port>` from `ep_044_web_apps/`) and check via `javascript_tool`:
- Every `<img>` on both `index.html` and `gallery.html` has `complete: true`/loads successfully.
- `tel:`/`mailto:` links are consistent with the sample identity everywhere they appear.
- Section counts match intent (`service-item`, `split-item`, `why-card`, `gallery-strip-item`, `art-gallery-item`).

## AI assistant integration — default on, one-flag off

Every site built under this skill ships with the shared AI assistant wired in **by default** (see `hartleys-barber-hair-template/assistant-embed.js` for the reference implementation).

1. Create a self-contained `assistant-embed.js` — dynamically injects `widget.js` from the shared Render-hosted service, guarded by a single `const ASSISTANT_ENABLED = true;` flag at the top. That flag **is** the switch-off mechanism: flipping it to `false` disables the assistant for a client who doesn't want it, with no HTML edits needed.
2. Add `<script src="assistant-embed.js"></script>` to every visitor-facing page (`index.html`, `gallery.html`), right after `reveal.js`.
3. Register the site as a tenant in `epics/ep_043_AI_native_serviceand _SEO/ai_website_assistant_framework` via its admin API — never by hand-editing `data/clients.json`. Check `curl http://127.0.0.1:4310/api/health` first (another agent may already have it running); otherwise `npm start` from the framework folder. `POST /api/admin/clients` with `Authorization: Bearer <ADMIN_TOKEN from .env>` and a body built from the site's own content: identity/theme/contact matching the site, `pages` (real nav anchors), `knowledge` (location/contact/services/pricing derived from the site copy, never invented), `demoWorkflows.booking` (priced services + slots), `status: "demo"`, `deployments` with `status: "local"` until actually hosted.
4. Verify before calling the build done: `curl "http://127.0.0.1:4310/api/public/config?clientKey=<publicKey>&host=localhost"` resolves the tenant, and one `POST /api/public/chat` request returns an answer genuinely grounded in the new site's knowledge.

## Where output goes + task tracking

Generic template (no real business yet) → `epics/ep_044_web_apps/<template-name>/`, lowercase-hyphenated, descriptive of the sample identity or niche (e.g. `hartleys-barber-hair-template`). If a real barbershop/hair salon is identified later, that becomes a new build under `epics/ep_006_website_rebuilds/redesigns/<business-slug>/` per `ep044_app_beauty_tanning_demo_template` instead. Per this repo's `CLAUDE.md`, create a workstream task file in `workstream/300_complete/claude/` once built and verified.

## Required shared layout invariant

Apply §6.4 **Mandatory page-edge and footer contract**, §6.1 **Inner-page editorial hierarchy**, and §6.2 **Gallery relevance** from `ep044_common_site_blueprint/000_site_blueprint.md` without exception. The business identity/logo block, header navigation, hero copy, page content, card/form outer edges and footer content must share one responsive left gutter. Use the normal-flow sticky-footer shell for short pages; never independently centre the header or use a fixed footer. The home hero remains the largest display moment; inner-page headings require an explicitly styled, distinct premium serif face at a smaller scale, with a compact mono kicker and restrained sans-serif lede—never browser-default inner-page text. Every gallery must contain real category-relevant visual assets, never empty cards, generic decoration or “images coming later” copy. When owner work is unavailable, use provenance-recorded, clearly labelled illustrative category imagery that does not claim work by the named business. Verify live geometry, type and image loads after cache-busting production CSS.
