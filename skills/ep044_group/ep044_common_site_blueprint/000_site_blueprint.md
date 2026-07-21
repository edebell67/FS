# Common Local Business Demo Website Blueprint

**Version:** 1.0  
**Role:** Master orchestration specification  
**Applies to:** All local-service and trade-category demo websites

## 1. Purpose

This blueprint defines the shared architecture, content, conversion behaviour, and quality standards for reusable local business demo websites. Category-specific skills inherit this specification and provide only the industry-specific details: services, terminology, imagery, qualification questions, FAQs, pricing guidance, case studies, and calls to action.

The primary objective is to turn visitors into qualified enquiries and paying clients while making each demo feel authentic to its category.

## 2. Common architecture

Every generated site should use this structure, adapting labels and content where appropriate:

```text
Home
├── Services
│   ├── Individual service pages
│   ├── Service FAQs
│   └── Service-specific calls to action
├── Gallery / Our Work
├── Before & After / Transformations
├── Reviews / Testimonials
├── About / Meet the Team
├── Pricing Guide
├── Areas Covered
│   └── Individual town or area pages
├── Knowledge Centre / Blog
│   └── Helpful customer articles
├── FAQ
├── Contact
├── Request a Quote / Book a Consultation
├── Privacy Policy
├── Terms and Conditions
└── Cookie Policy, where required
```

The header must provide clear navigation, a prominent primary CTA, and direct contact options. The footer must repeat essential navigation, service links, contact details, social links where available, legal links, and the business copyright notice.

## 3. Required pages and page standards

### Home

The homepage must communicate the business, service area, and value proposition immediately. Include:

- Clear category-specific headline and supporting statement
- Primary CTA such as **Get a Free Quote** or **Book a Consultation**
- Secondary CTA such as **View Our Work** or **Call Now**
- Trust signals near the hero
- Featured services
- Selected gallery or transformation projects
- Why choose us section
- Review preview
- Process overview
- Areas covered preview
- FAQ preview
- Contact or quote CTA
- AI assistant entry point

### Services

Provide an easy-to-scan overview of all services. Each service card should link to a dedicated service page where practical.

### Individual service pages

Each service page should explain the customer problem, the service solution, benefits, inclusions, process, expected timescale, relevant imagery, FAQs, trust signals, and a clear enquiry CTA. Link to related services, gallery items, useful articles, and the quote page.

### Gallery / Our Work

Show completed work using high-quality, relevant imagery. Support category-appropriate filtering where useful, such as service, style, colour, property type, size, or budget. Include captions only when they add useful project context; never use placeholder or misleading project claims.

### Before & After / Transformations

Where the category supports it, show the original condition and completed result. Include a concise project summary, work completed, location or area (with permission), and timescale. Use an accessible comparison slider or a clear side-by-side layout.

### Reviews / Testimonials

Present genuine written, video, or platform reviews when available. Show the source, date, rating, and customer context where appropriate. Never invent reviews, ratings, accreditations, guarantees, or project outcomes.

### About / Meet the Team

Explain the business story, experience, working approach, team, qualifications, insurance, accreditations, guarantees, and local connection. Use real photography when supplied.

### Pricing Guide

Provide indicative ranges or explain why a fixed price requires a survey. Cover what is included, the main cost factors, possible extras, timescales, payment stages, and finance only when genuinely offered. Always distinguish estimates from quotations.

### Areas Covered

List the primary service area and nearby towns or postcodes. Generate individual area pages only when each page can contain useful, locally relevant information and a genuine service connection; avoid thin doorway pages.

### Knowledge Centre / Blog

Create helpful articles that answer real customer questions. Each article must have a useful title, clear structure, appropriate imagery, internal links to services, and a relevant CTA. Prioritise cost, planning, maintenance, comparison, and preparation topics.

### FAQ

Answer common questions about pricing, scope, preparation, access, duration, disruption, guarantees, payment, service areas, cancellations, and booking. FAQs must reflect the actual business offer.

### Contact and Request a Quote

Offer simple contact routes: phone, email, enquiry form, and messaging channels such as WhatsApp only when supplied. The quote form should collect, as appropriate:

- Name
- Phone and email
- Postcode or service location
- Required service
- Approximate scope or room/property details
- Budget or preferred investment range
- Preferred start date or timing
- Additional notes
- Optional image upload

State what happens after submission and provide a privacy notice link.

## 4. AI assistant requirements

The AI assistant is a guided consultation and lead-qualification feature, not merely a generic chatbot. It must:

- Welcome visitors using category-specific language
- Identify the service or problem
- Ask only the minimum useful qualification questions
- Recommend relevant services, gallery items, articles, or FAQs
- Explain the process, likely timescale, and indicative pricing carefully
- Collect consent before storing or forwarding personal information
- Capture name, contact details, postcode, requirements, budget, timing, and notes when appropriate
- Offer a callback, quote request, consultation, or booking action
- Produce a structured summary for the business
- Escalate to a human for urgent, complex, sensitive, or uncertain requests
- Clearly identify itself as an AI assistant
- Never promise availability, prices, qualifications, outcomes, or guarantees unless provided by the business

The assistant should be available throughout the site, preserve context as the visitor moves between pages, and provide a visible fallback to phone, email, or the quote form. Conversation data must follow the site's privacy and retention rules.

## 5. Conversion requirements

Every page must support a clear next step:

- Visible primary CTA above the fold
- Relevant CTA after major content sections
- Trust signal close to important CTAs
- Mobile-friendly sticky call, quote, or message action where suitable
- Short forms with clear field labels and validation
- Confirmation state after submission
- Fast access to gallery, reviews, pricing, and FAQs
- Prominent phone number on mobile and desktop
- Relevant internal links rather than dead-end pages

Use a consistent conversion hierarchy: inspire, establish trust, explain the service, remove objections, then request the enquiry. Track meaningful events such as CTA clicks, form starts, form submissions, phone clicks, message clicks, gallery engagement, and completed AI handoffs when analytics is available and consent is handled correctly.

### 5.1 Visitor analytics (required, anonymous)

Every visitor-facing page should log **anonymous** visitor behaviour so the business gets insight into how people use the site — unique visits and their timing, pages viewed, and buttons clicked — **without identifying any visitor**. Use the shared tracker from the assistant service; add, alongside `assistant-embed.js`, one tag per page:

```html
<script src="<assistant-service>/analytics-embed.js" data-client="CLIENT_PUBLIC_KEY" data-api-base="<assistant-service>" async></script>
```

The tracker auto-captures page views, scroll depth, dwell time, phone/email/WhatsApp taps, form start/submit, gallery opens, and assistant open/handoff, and shares an **ephemeral, tab-scoped visit id** with the AI assistant so behaviour and chat join within a single visit (surfaced in the admin "Visitor insights" view). To make CTA clicks meaningful, tag primary buttons with a stable identifier, e.g. `data-ev="cta:quote"`, `data-ev="cta:call"`, `data-ev="cta:book"`.

- **Anonymous and PII-free by contract**: there is **no persistent visitor identifier** (the visit id is session-scoped and gone when the browser closes), so a person is never tracked across visits or days. Only event type, page path (never query strings), referrer host, device class, scroll %, and dwell time leave the page. Never add event attributes carrying names, emails, phone numbers, or free-typed input. It honours Do Not Track and a per-visit opt-out.
- **Per-site on/off switch**: logging is controlled per client via `analyticsEnabled` (admin toggle), enforced server-side — off means nothing is stored. Even anonymous logging should sit behind the site's consent handling (Section 4 / privacy pages).

## 6. Visual system: typography, imagery, and look-and-feel

This section is normative. A category demo is not "done" until it satisfies it. Its purpose is to guarantee that every generated site — regardless of category or which agent built it — reads as one consistent, professional family, with depth rather than a thin skeleton. Category skills inherit this section and only choose category-appropriate content (image subjects, accent palette), never a different type scale, font pairing, or image density.

### 6.1 Typography — one shared, relative scale

All sizes are defined in **relative units** (`rem` for fixed roles, `clamp()` for fluid headings) so that every element is sized in proportion to the others and the whole page stays harmonious across screen sizes. Do not use `px` for type. Do not invent per-site font sizes; use the roles below.

**Font pairing (fixed across the whole family — load from Google Fonts):**

| Role | Family | Usage |
|---|---|---|
| Display / headings | `Cormorant Garamond`, serif | All `h1`–`h3`, brand name, decorative marks. Weight 600 (700 for brand). `line-height: 1.1`, `letter-spacing: -0.01em`. |
| Body / UI | `Outfit`, sans-serif | Paragraphs, lists, nav, buttons, forms. Body `line-height: 1.6`. |
| Mono / meta | `JetBrains Mono`, monospace | Eyebrows, prices, gallery captions, trust pills, tech/legal notes. Uppercase, wide `letter-spacing`. |

**Modular type scale (the family standard — reuse these exact values):**

| Token / role | Size | Notes |
|---|---|---|
| Hero `h1` | `clamp(2.5rem, 4.8vw, 3.9rem)` | Fluid; one per page. |
| Section `h2` | `clamp(2rem, 3.6vw, 2.9rem)` | Every major section header. |
| CTA-box `h2` | `clamp(2.2rem, 4vw, 3.2rem)` | Dark conversion blocks. |
| Sub-heading `h3` | `1.2rem`–`1.5rem` | Cards, service rows, split copy. |
| Lede / intro `p` | `1.05rem`–`1.12rem`, `max-width: 44–46ch` | Hero and section intros. |
| Body `p` | `1rem` | Default; muted colour token. |
| Nav / feature-list / small UI | `0.88rem`, weight 500 | |
| Button | `0.92rem` (large `1rem`), weight 600 | |
| Eyebrow (mono) | `0.72rem`, uppercase, `letter-spacing: 0.16em` | Section kickers. |
| Trust pill / sample note (mono) | `0.68rem` | |
| Caption label (mono) | `0.64rem`, uppercase, `letter-spacing: 0.1em` | Gallery category tags. |
| Footer / legal meta | `0.75rem`–`0.8rem` | |

Every heading uses the serif; every eyebrow/price/caption uses the mono; everything else uses the sans. Because all sizes derive from this one scale, headings, body, and meta always complement each other on a page. If a category genuinely needs a role not listed, size it relative to its nearest neighbour on this scale — never as a standalone `px` value.

**Inner-page editorial hierarchy (mandatory):** The home hero remains the largest display moment. Every visitor-facing inner-page hero must preserve that premium hierarchy rather than falling back to browser-default text: use a distinct premium serif display face (for example `Cormorant Garamond`) for the inner-page `h1`, at `clamp(2.15rem, 4.1vw, 3.6rem)` or smaller than the home hero; pair it with a compact uppercase mono kicker and a restrained sans-serif lede. The inner heading, kicker and lede must be explicitly styled in the shared stylesheet—never rely on unscoped `h1`/`p` defaults. This treatment must apply consistently to services, gallery, process, guides, FAQ, quote/contact, reviews, pricing, areas, about and legal routes.

### 6.2 Image system — depth through real photography

Thin, image-poor screens are not acceptable. **Images are the sales pitch** — the work and the premises are what convert a visitor. Every build must be visually rich, with real, verified photography across the categories below, not one token hero.

**Required imagery per page (minimum):**

| Location | Images | Category of image |
|---|---|---|
| Hero | 1 | Premises, hero subject, or signature work for the category |
| Two split / feature sections | 1 each | The two primary service disciplines, alternating image side |
| Homepage gallery preview strip | 4 | A representative mix of the category's work |
| Dedicated gallery page (`gallery.html`) | 9–10 | Editorial masonry, captioned by sub-category |
| Before & After (where the category supports it) | 2+ pairs | Original condition + completed result |
| About / team (when real photos supplied) | 1+ | Real people/premises only; never stock portraits as "the team" |

Category skills specify the **subjects** for these slots (e.g. a gardener's gallery = lawns, borders, patios, planting schemes, seasonal transformations); the counts and placements above are fixed by this blueprint.

**Gallery relevance is mandatory:** a gallery must contain real visual assets that unmistakably relate to the underlying business category, services and visitor intent. A nail site needs nails/manicures/studio process; a bathroom site needs bathrooms/fittings; a garage site needs vehicles/workshop work; a gardener site needs gardens/planting—not empty category cards, generic decorative imagery or a textual promise that images will arrive later. When verified owner work is unavailable for a private concept, use curated, verified stock images that genuinely match the category and mark the whole set clearly as `ILLUSTRATIVE <CATEGORY> DIRECTION — NOT VERIFIED WORK BY <BUSINESS>`. Keep asset provenance, use captions that do not imply the named business performed the work, and replace illustrative assets with owner-approved imagery before official launch.

**Image sourcing and verification workflow (mandatory for every image):**

1. Find real photos via `WebSearch`/`WebFetch` against a stock source's search pages for the category's themes — never guess an image ID from memory.
2. Skip paid-tier results (e.g. `plus.unsplash.com`).
3. Verify each candidate loads before it goes in HTML: it must return HTTP `200` (e.g. `curl -s -o /dev/null -w "%{http_code}" "<image-url>"`).
4. Check for accidental reuse across sibling sites in the family (`grep -r "<image-id>" epics/ep_044_web_apps`) so no two category demos share the same photo.
5. Vary composition within a gallery (wide/detail, premises/in-action) so the set feels curated, not repetitive.
6. Every `<img>` needs a descriptive filename/alt text (see §9 Accessibility) and lazy-loading below the fold (see §10 Performance).

Verification gate: serving the finished site, **every `<img>` on every page must load successfully** (`complete: true`), and section image counts must match the table above.

### 6.3 Look-and-feel consistency tokens

Define all of these once in `:root` custom properties and reference them everywhere — never hard-code a second copy of a value:

- **Colour**: one accent palette per site, applied only through `:root` tokens (`--ink`, `--accent`, `--surface`, `--text-main`, `--text-muted`, `--border`, etc.). Before choosing a palette, read `epics/ep_044_web_apps/PALETTE_REGISTRY.md`, propose 2–4 candidates genuinely distinct from every existing row, apply the chosen one via `:root` only, grep the finished file for stray/placeholder hex values outside `:root`, then append the new site's row to the registry in the same turn so parallel builds never collide.
- **Spacing**: a consistent rhythm (section padding, card gaps, element margins) driven by a small set of spacing tokens rather than ad-hoc values.
- **Radius & pills**: buttons and pills use a consistent full-round radius (`border-radius: 100px`); cards a consistent smaller radius.
- **Motion**: one shared easing token (`--ease`) and transition duration (~0.2–0.25s); a single self-contained IntersectionObserver reveal script for on-scroll reveals; respect `prefers-reduced-motion` (see §9).
- **Buttons**: consistent padding (`~0.95rem 1.9rem`, large `~1.15rem 2.3rem`), a primary (accent fill) and secondary (bordered) variant, used the same way on every site.

The test of consistency: place any two sites from this family side by side and they should feel like the same design system with different content and colour — same type rhythm, same spacing, same component shapes.

### 6.4 Mandatory page-edge and footer contract

This is a non-negotiable shared layout invariant for every EP044 visitor-facing page, including short legal, pricing, contact and quote pages.

1. Define one responsive page gutter token such as `--site-gutter: clamp(1.5rem, 3.5vw, 2.75rem)` and one content-width token such as `--site-max: 80rem` in `:root`.
2. The **business identity/logo block**, header navigation container, hero copy, cards/grid outer edge, ordinary page copy, form-card outer edge and footer content must begin from the same computed left page gutter. Do not centre the header/brand independently while the page content is left-aligned.
3. Use one shared container rule for those page regions. Do not repair individual pages with arbitrary `margin-left`, magic pixel offsets or differing section paddings.
4. When the page body is a flex column, an auto-margined header can shrink to its intrinsic content width and centre itself. Prevent this by giving the header an explicit full responsive container width, e.g. `width: min(100%, var(--site-max))`, while retaining shared horizontal padding.
5. Cards may keep internal padding for readable controls; the card's **outer edge** must still align with the shared page gutter.
6. The footer is part of normal document flow. Use a sticky-footer shell, not `position: fixed`: `body { min-height: 100dvh; display: flex; flex-direction: column; }`, `main { flex: 1 0 auto; }`, `footer { margin-top: auto; }`. On short pages this places the footer at the viewport bottom; on long pages it follows content without overlap.
7. Cache-bust a stylesheet URL whenever a production-wide CSS repair is published, then verify the live computed geometry rather than relying only on source inspection.
8. QA desktop and narrow/mobile widths: no horizontal overflow, consistent gutter geometry for header/hero/cards/forms/footer, and no blank area below a short-page footer.

## 7. Trust signals

Use verifiable evidence wherever available:

- Genuine reviews and rating sources
- Years in business
- Relevant qualifications and memberships
- Insurance details
- Guarantees and warranties
- Completed project count, only if substantiated
- Clear response expectations
- Real team and project photography
- Supplier or brand relationships, only when accurate
- Local service area and contact details

Trust signals must be specific, consistent, and easy to verify. Do not use fabricated badges, stock customer portraits presented as real people, or unsupported claims such as “best” or “number one.”

## 8. SEO requirements

Every indexable page must include:

- Unique, descriptive title tag
- Unique meta description with a useful reason to click
- One clear H1 and logical heading hierarchy
- Search-intent-aligned copy written for people
- Canonical URL
- Open Graph and social sharing metadata
- Descriptive image filenames and alt text
- Internal links to related services and conversion pages
- XML sitemap and sensible robots directives
- Structured data appropriate to the page and supported by visible content
- Consistent business name, address, phone, and service area information
- Fast, crawlable, mobile-first rendering

Use local intent naturally in page titles, copy, and area references. Avoid keyword stuffing, duplicate service pages, automatically generated thin location pages, hidden text, and unsupported schema claims.

## 9. Accessibility requirements

Build to WCAG-aligned best practices:

- Semantic HTML and logical document structure
- Full keyboard navigation
- Visible focus indicators
- Sufficient colour contrast
- Meaningful link and button labels
- Proper form labels, instructions, errors, and success messages
- Alt text for informative images and empty alt text for decorative images
- Captions or transcripts for meaningful video content
- No information conveyed by colour alone
- Respect for reduced-motion preferences
- Touch targets large enough for mobile use
- Accessible modal, lightbox, slider, menu, and AI assistant behaviour

Accessibility applies equally to generated content, imagery, interactive components, and validation states.

## 10. Performance and technical quality

The site must be responsive and suitable for modern mobile devices. Optimise images, use appropriate formats and dimensions, lazy-load below-the-fold media, minimise unnecessary scripts, and avoid layout shift. Aim for strong Core Web Vitals, fast first render, stable typography, and usable performance on slower connections.

Use robust loading, empty, error, and success states. Ensure forms, navigation, filters, gallery lightboxes, sliders, and the AI assistant work without console errors. Keep components reusable and content-driven so a new category can be generated without duplicating the shared system.

## 11. Reusable module list

Category sites should inherit these common modules:

1. Site shell, header, navigation, mobile menu, and footer
2. Homepage hero and CTA system
3. Trust strip and credentials section
4. Services index and service detail template
5. Gallery, filters, lightbox, and related work
6. Before-and-after comparison
7. Reviews and testimonials
8. About and team
9. Process or customer journey timeline
10. Pricing guide
11. Areas covered and local landing template
12. FAQ and FAQ schema support
13. Knowledge Centre and article template
14. Contact and quote-request forms
15. AI consultation assistant and lead summary
16. CTA, callback, and booking components
17. Consent, privacy, and legal-link components
18. SEO metadata and structured-data utilities
19. Accessibility primitives and validation states
20. Responsive image, performance, analytics, and error-handling utilities
21. Shared visual system: `:root` design tokens, the font pairing, the relative modular type scale, spacing/radius/motion tokens, and the reveal script (Section 6)
22. Visitor analytics event logging: the shared first-party, PII-free tracker (`analytics-embed.js`) plus `data-ev` CTA tagging (Section 5.1)

## 12. Category inheritance contract

Each category-specific skill must provide:

- Business identity and tone
- Primary and secondary services
- Service-specific page content
- Target customers and common problems
- Category terminology and qualification questions
- Category image **subjects** for each slot in the Section 6 image matrix (hero, the two split sections, gallery, before-and-after) plus category search queries
- Relevant gallery and before-and-after content
- Genuine business facts and trust signals
- Pricing model or estimate guidance
- Service areas
- Category FAQs and article topics
- Appropriate CTAs and booking actions
- A category-appropriate accent palette direction (chosen against `PALETTE_REGISTRY.md`)
- Safety, regulatory, or escalation considerations

The category skill supplies content and palette choices only; it inherits the Section 6 visual system (font pairing, relative type scale, image matrix, look-and-feel tokens) unchanged. It may extend the common blueprint but must not redefine the shared type scale or font pairing, and must not remove essential navigation, trust, accessibility, SEO, privacy, or conversion requirements without an explicit product decision.

## 13. Generation workflow

Use this sequence whenever generating a category demo site:

1. Load this common blueprint and all required shared modules.
2. Load the category-specific skill and validate its inheritance contract.
3. Gather the available business facts, service area, contact details, imagery, reviews, and brand direction.
4. Mark unknown facts as placeholders or omit them; never invent claims.
5. Build the content model for services, projects, reviews, FAQs, areas, articles, and CTAs.
6. Generate the site shell and common page templates.
7. Insert category-specific content, imagery, terminology, and AI qualification flow.
8. Add metadata, internal links, structured data, consent handling, and legal links.
9. Check conversion paths from homepage, service pages, gallery, articles, AI assistant, and mobile CTAs to a contact action.
10. Test responsive layouts, keyboard access, form states, error handling, image behaviour, and performance.
11. Review claims, links, contact details, accessibility, SEO, and visual consistency.
12. Deliver the demo with a concise content-gap list identifying information the business should replace or confirm.

## 14. Definition of done

A category demo is ready when:

- The common architecture is present and navigable
- Every required conversion path works
- Category-specific pages and content are meaningful rather than generic
- **The Section 6 visual system is applied**: the font pairing and shared relative type scale are used (no `px` type, no per-site font sizes), and the page reads as part of the family
- **The Section 6 image matrix is satisfied**: every required image slot is filled with real, verified photography, every `<img>` loads, and no screen is thin or image-poor
- The AI assistant can qualify and hand off a lead
- Trust claims are evidence-based or clearly marked as placeholders
- SEO metadata and internal linking are complete
- Forms include privacy handling and usable feedback states
- The experience works on mobile, keyboard, and common screen sizes
- Images are relevant, optimised, and accessible
- No page is a dead end
- The site has been checked for performance, accessibility, broken links, and misleading content
