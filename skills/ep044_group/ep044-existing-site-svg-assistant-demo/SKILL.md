---
name: ep044-existing-site-svg-assistant-demo
description: Use when creating a private, owner-reviewable AI-assistant overlay concept for a verified existing business website. Recreate only the site’s visual language with original SVG/CSS, keep the live site intact, and deploy a tenant-scoped demo safely.
version: 1.0.0
author: The Tech Principle
license: Proprietary
metadata:
  hermes:
    tags: [ep044, existing-site, ai-assistant, svg, owner-preview, github-pages, render]
    related_skills: [website-ai-assistant-integration, embedded-assistant-verification]
---

# EP044 Existing-Site SVG Assistant Demo

## Relationship to the master blueprint

This skill is the one deliberate exception to the ep044 family's "build from the blueprint" rule: its job is to **recreate the owner's *existing* site's visual language**, so it does **not** impose the master blueprint's page architecture, font pairing, or type scale — fidelity to the real site comes first.

Consistency still applies to everything this skill originates itself. Any surface it authors — the assistant overlay/launcher/panel, private-preview framing, disclosure banners, and any net-new UI not lifted from the real site — must meet the same premium quality and internal-consistency bar defined in `../ep044_common_site_blueprint/000_site_blueprint.md` Section 6 (a coherent type hierarchy in relative units, deliberate spacing, accessible contrast, no thin/placeholder feel) and Section 9 (accessibility). In short: **mirror the client's site faithfully, but anything you add must look and feel premium and consistent, never bolted-on.**

## Overview

Create a private product experiment that helps a business owner recognise their current website while showing the **AI assistant as an added front door**, not a website-replacement pitch.

The demo should communicate:

```text
Keep the current site
→ add a tenant-scoped assistant overlay
→ approve knowledge and capabilities
→ optionally discuss a refresh only if the owner wants it
```

The finished page is a **clearly labelled private integration concept**. It is not the owner’s official website, does not impersonate their site, and does not perform live bookings, callbacks, payments, emails, CRM actions, or notifications.

## When to Use

Use when all of these are true:

- a current website/domain has been independently verified from an exact directory listing or direct source;
- an initial browser inspection finds no visible assistant launcher and no common assistant-provider script;
- the desired offer is an assistant on the business’s existing site;
- a private preview link is needed for owner review;
- the business identity and public website facts can be sourced without guessing.

Do **not** use when:

- the business has no verified current domain;
- the site is an official client installation rather than a pre-approval preview;
- the goal is a full website rebuild first;
- the required public facts, business identity, or permitted contact route are unclear.

## Non-Negotiable Boundaries

1. **Do not frame the live site.** Check response headers first. If it returns `X-Frame-Options: SAMEORIGIN` or a restrictive `Content-Security-Policy: frame-ancestors`, an iframe overlay will fail. Do not use workarounds.
2. **Do not copy live-site photos, logos, HTML, CSS, screenshots, directory images, reviews, or third-party assets into a public preview.** A private owner-review page can use verified public facts and an original visual concept, but not republished site assets.
3. **Do not clone the site.** Recreate its recognisable visual language: hierarchy, palette family, header rhythm, nav placement, hero composition, and service category cues. Keep it clearly a concept and distinct from the official site.
4. **Do not invent operational information.** Prices, availability, opening hours, coverage beyond sourced wording, appointments, staff, qualifications, reviews, or service detail require owner confirmation.
5. **Do not send the link.** Building, publishing, and drafting are permitted. External email/SMS/WhatsApp/call delivery requires verified recipient identity, suppression check, exact copy review, and explicit send approval.

## Input Evidence Manifest

Create a per-business manifest before building. Quarantine the candidate if any required field is missing.

| Field | Required evidence | Example use |
|---|---|---|
| Business identity | Directory profile + live site match | Demo title and tenant name |
| Existing domain | Current source profile Website field, then browser-load domain | Link to the existing site |
| Visual cues | Browser observation only | Header/navigation/hero rhythm, palette family |
| Public service wording | Exact public-site copy | Bounded assistant knowledge |
| Public contact cue | Existing-site contact route | Recognition anchor only; no unsolicited action |
| Assistant observation | Visible launcher + common provider-script check | `no visible assistant` is an initial observation, not absolute proof |
| Legal/contact status | Corporate identity and recipient route separately checked | Draft/review queue only |

Record the classification precisely:

```text
Existing site reachable: yes/no
Visible assistant: found / not found during initial browser inspection
Public source checked: exact URL
Owner/recipient verified: pending / verified
Outreach status: not_sent
```

A directory filename such as `no_website` is only a hypothesis. Inspect the directory’s current Website field and then load the linked domain.

## Visual Analysis: Extract a Design Language, Not Assets

Use a browser screenshot only as a **visual reference**, never as an asset to republish.

Document these attributes:

1. header background and structure;
2. logo/identity placement without reproducing the logo artwork;
3. navigation location, density, and contrast;
4. accent colour family;
5. hero subject and crop;
6. title placement, type scale, and contrast treatment;
7. recurring geometry (cards, dividers, gradients, shadows, spacing).

Then create a new visual system from those observations.

### Original SVG Hero Rule

Create one original, responsive SVG hero image for the service category. It should echo the **composition** of the observed hero without tracing or duplicating it.

For example, an air-conditioning business may use:

```text
wall-mounted split unit
+ vent/louvre geometry
+ remote-control interaction
+ neutral interior wall
+ original shapes, gradients, shadows, and display graphics
```

The SVG must not contain the original business’s logo, photographs, source SVG fragments, copyrighted product imagery, or copied text. Use an explicit `<title>` and `<desc>` that identify it as an original private-preview illustration.

Store it at:

```text
<preview-folder>/assets/<business-slug>-hero.svg
```

Use it as the hero background through CSS, for example:

```css
.heroVisual {
  position: absolute;
  inset: 0;
  background: url('assets/<business-slug>-hero.svg') center / cover no-repeat;
}
```

## Page Pattern

The first viewport should make the owner recognise the business and the offer within seconds.

Required first-viewport elements:

1. **Persistent disclosure**
   ```text
   PRIVATE AI-ASSISTANT INTEGRATION DEMONSTRATION
   Prepared by The Tech Principle
   Not an official <Business> website or live service
   ```
2. **Business recognition anchors:** exact business name; only verified public phone/email/address/area as appropriate.
3. **Existing-site visual language:** original CSS/SVG implementation based on the evidence manifest.
4. **Assistant overlay:** tenant-scoped widget in demo mode. It may auto-open only when the experiment needs that experience demonstrated.
5. **Current-site link:** open the owner’s existing public domain in a new tab; do not route it through a tracking or fake proxy.
6. **Bounded value statement:** make clear the current site remains and the assistant is added.

Recommended secondary content:

- three tightly bounded service/integration cards;
- a simple “what changes after approval” sequence;
- a safe scrolling ticker/marquee for the integration explanation;
- The Tech Principle identity in the footer.

### Slow Ticker Pattern

For a slow, continuous repeat of an owner-facing explanation, duplicate the sentence once in the track and animate the track by half its width. Use a non-essential `aria-label` for the message, while duplicate copy is `aria-hidden`.

```html
<div class="ticker" aria-label="Integration concept summary">
  <div class="tickerTrack">
    <span>Primary message.</span><b aria-hidden="true">✦</b>
    <span aria-hidden="true">Primary message.</span><b aria-hidden="true">✦</b>
  </div>
</div>
```

```css
.ticker { overflow: hidden; white-space: nowrap; }
.tickerTrack { display: inline-flex; min-width: max-content; animation: ticker 32s linear infinite; }
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }
```

Verify the browser reports `animationName: ticker`, the intended duration, and `playState: running`.

## Tenant Configuration

Every preview gets a unique public key and a unique client ID. Never reuse a tenant key.

Required tenant properties:

```json
{
  "id": "<business>-existing-site-demo",
  "publicKey": "<business>_existing_site_demo",
  "allowedHosts": ["localhost", "127.0.0.1", "edebell67.github.io"],
  "status": "demo",
  "notificationDestinations": [],
  "enabledModules": ["assistant", "faq", "navigation"]
}
```

Knowledge must be limited to public, auditable facts. Include explicit fallback wording such as:

```text
Prices, availability, appointment times and detailed service scope need owner confirmation.
This preview does not make bookings or notify anyone.
```

Do not add callback, lead, booking, payment, email, CRM, notification, or marketplace-transaction modules merely to make a demo look more complete.

### Auto-Open

If the product experiment requires a visible assistant immediately, use only the shared widget’s supported per-embed flag:

```js
widget.dataset.autoOpen = 'true';
```

Do not programmatically click a Shadow-DOM launcher. The production widget must read the flag and call its internal open routine **after** tenant configuration resolves.

## Build and Publish Workflow

### 1. Prepare in clean clones

Use temporary clean clones for source and GitHub Pages. Keep production source and public runtime commits separate.

```text
FS source repository:
  epics/ep_044_web_apps/<business>-existing-site-demo/

Pages repository:
  <business>-existing-site-demo/
```

Public runtime manifest:

```text
index.html
assistant-embed.js
assets/<business>-hero.svg
only other visitor-facing assets strictly needed at runtime
```

Do not publish README files, source evidence, screenshots, crawler outputs, deployment notes, local launch scripts, owner data, or internal planning files.

### 2. Validate before commit

- validate `clients.json` parses;
- confirm tenant key/id uniqueness;
- run the framework test suite;
- scan the preview for predecessor business names and unsafe claims;
- verify `noindex,nofollow` is present;
- verify the hero asset is original SVG and loads locally;
- verify all external links use the real public site URL;
- verify demo mode with empty notification destinations.

### 3. Commit source, then Pages

Source commit must include only:

```text
new tenant record
new source preview folder
related source assets
```

Pages commit must include only the runtime manifest. Push both, then poll the public URL until it returns HTTP 200.

### 4. Deploy and verify Render

A source push does not update the running shared service.

### API-key deployment (preferred at scale)

Store a Render API key only in the active Hermes environment secret file:

```text
/home/edebe/.hermes/.env
RENDER_API_KEY=<secret>
```

Never put it in Git, `SKILL.md`, a project `.env`, a shell command captured in history, a source file, or chat. Restart the Hermes gateway after the secret is added so the gateway/agent process inherits it. Confirm presence only (never print its value):

```bash
test -n "${RENDER_API_KEY:-}" && echo present || echo absent
```

Run the included helper only after a source commit is pushed and the intended deployment has been approved:

```bash
bash skills/ep044_group/ep044-existing-site-svg-assistant-demo/scripts/trigger_render_deploy.sh
```

The helper invokes Render's documented `POST /v1/services/{serviceId}/deploys` endpoint for the existing shared assistant service. It never logs the token.

### Dashboard fallback

If no authenticated API key is available, deploy manually:

```text
shared-website-assistant-api
→ Manual Deploy
→ Deploy latest commit
```

Then verify in this order:

1. `/api/health` returns HTTP 200;
2. `/widget.js` contains any newly introduced widget feature needed by the preview;
3. `/api/public/config?clientKey=<key>&host=edebell67.github.io` returns HTTP 200 with intended business name and `demo` status;
4. the Pages URL returns HTTP 200;
5. fresh browser navigation shows the widget/assistant with the correct tenant identity;
6. if auto-open is enabled, the dialog exists without a launcher click;
7. an unsupported question does not cause invented information;
8. browser console is free of integration errors;
9. no external notification was created.

## Batch Scale Discipline

Do one owner-recognition quality check before batch creation. Then create one evidence manifest per business. A batch row is ready only when all fields below exist:

```text
business identity
current domain
source URL
visual-language notes
public knowledge snippets
unique tenant key
preview slug
live-site assistant observation
recipient/contact status
suppression status
```

Rows with missing evidence are quarantined. Do not generate a generic site by merely replacing the business name.

Use palette variation across verticals while retaining the business-specific visual cues. A repeated template skin creates an obvious mass-generated impression and reduces owner recognition.

## Outreach Gate

The Tech Principle may prepare a review-link draft, but no outreach is sent automatically.

Before any email delivery, require:

```text
exact @thetechprinciple.com sender mailbox
verified corporate identity and intended business recipient
suppression / do-not-contact check
approved final copy and destination
explicit send instruction
```

The initial message must be link-first and factual:

```text
private preview
not official or live
built from public information
review when convenient
follow-up only after a review window
```

Do not promise installation, bookings, callbacks, results, pricing, availability, or marketplace access before owner approval.

## Common Pitfalls

1. **Iframe fails or appears blank.** Check `X-Frame-Options` and CSP first. Build an original integration concept instead of trying to bypass framing controls.
2. **Preview looks like a generic template.** Revisit the visual evidence manifest. Match composition and hierarchy, not only business name and colour.
3. **Copied screenshot/photo used as a hero.** Remove it. Rebuild the subject in original SVG/CSS. The preview can be recognisable without redistributing site assets.
4. **Synthetic click does not open widget.** Use supported `data-auto-open` / `widget.dataset.autoOpen`, and verify the deployed Render widget understands it.
5. **Pages page is live but assistant disabled.** The static page deployed before the tenant reached Render. Deploy Render and verify the real config endpoint.
6. **Directory label says no website.** Treat it as a hypothesis. Recheck the listing Website field and load the live domain.
7. **Preview implies an official business service.** Add and retain the persistent private-demo disclosure; keep all modules demo-safe.
8. **User asks to send link after preview exists.** Stop at a prepared draft until recipient, sender mailbox, suppression check, and explicit send approval are recorded.

## Completion Checklist

- [ ] Current domain was independently verified from a directory source and browser-loaded.
- [ ] Initial visible-assistant observation recorded; no absolute “no AI” claim made.
- [ ] No framing workaround or copied public-site asset was used.
- [ ] Original category-specific SVG hero is present and has `<title>`/`<desc>`.
- [ ] Preview visually reflects the existing site’s hierarchy/palette/composition.
- [ ] Persistent The Tech Principle private-demo disclosure is visible.
- [ ] Tenant ID/key are unique, host-bound, and `demo` status has no notifications.
- [ ] Framework tests pass and tenant config parses.
- [ ] Public Pages runtime contains only intended visitor assets and returns HTTP 200.
- [ ] Render health, widget, tenant config, and browser widget journey are verified.
- [ ] No external outreach was sent; any draft remains pending approval.

## Required shared layout invariant

Apply §6.4 **Mandatory page-edge and footer contract**, §6.1 **Inner-page editorial hierarchy**, and §6.2 **Gallery relevance** from `ep044_common_site_blueprint/000_site_blueprint.md` without exception. The business identity/logo block, header navigation, hero copy, page content, card/form outer edges and footer content must share one responsive left gutter. Use the normal-flow sticky-footer shell for short pages; never independently centre the header or use a fixed footer. The home hero remains the largest display moment; inner-page headings require an explicitly styled, distinct premium serif face at a smaller scale, with a compact mono kicker and restrained sans-serif lede—never browser-default inner-page text. Every gallery must contain real category-relevant visual assets, never empty cards, generic decoration or “images coming later” copy. When owner work is unavailable, use provenance-recorded, clearly labelled illustrative category imagery that does not claim work by the named business. Verify live geometry, type and image loads after cache-busting production CSS.
