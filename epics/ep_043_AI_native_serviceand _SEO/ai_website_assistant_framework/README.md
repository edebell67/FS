# AI Website Assistant Framework

A reusable, multi-tenant website assistant that is configured once per client and embedded with one script tag. The same service and widget support many client profiles; client data and modules are resolved per request.

## Visual and interaction direction

- **Visual thesis:** warm editorial hospitality for the visitor widget, paired with a quiet, precise operations workspace for administrators.
- **Content plan:** the demo host establishes the client, the widget answers and routes, contextual module actions collect intent, and the admin workspace configures and audits the platform.
- **Interaction thesis:** a composed widget entrance, conversational message reveals, and a focused admin inspector that updates without page navigation.

## Start

Requires Node.js 20 or later. No package installation is required.

```powershell
Copy-Item .env.example .env
npm start
```

Then open:

- Demo client site: `http://127.0.0.1:4310/`
- Administration: `http://127.0.0.1:4310/admin`
- Health check: `http://127.0.0.1:4310/api/health`

For a one-click review, run `open_demo.bat`. The default local admin token is `change-me-before-live-use`; set a strong `ADMIN_TOKEN` before any shared or live deployment.

## Embed on any website

```html
<script
  src="https://assistant.example.com/widget.js"
  data-client="CLIENT_PUBLIC_KEY"
  data-api-base="https://assistant.example.com"
  defer
></script>
```

The public key identifies a client profile; it is not a secret. Production host allow-lists prevent a key being reused on an unapproved website.

## Architecture

```text
Client website → isolated widget → public API → client resolver
                                              ├─ configuration + module registry
                                              ├─ approved knowledge retrieval
                                              ├─ deterministic grounded response
                                              ├─ optional OpenAI Responses adapter
                                              └─ conversations / leads / callbacks

Administrator → bearer-protected API → client and operational record store
```

The included JSON repositories make the MVP immediately runnable. `ClientStore` is isolated behind a small interface so a managed SQL/document database can replace it without changing the widget or API contract. Writes use an atomic temporary-file rename and are serialized in process.

## Engagement modes

Each client profile chooses how the assistant introduces itself, set in the admin editor's "Assistant engagement" section:

- **On-demand** (default) — the visitor opens the widget themselves; behavior is unchanged from before this feature.
- **Proactive** — the widget opens itself shortly after the page loads (delay configurable, default 2500ms) and offers help, on every page visit. If the visitor responds negatively — clicking "No thanks" or typing a decline such as "no thanks" / "not interested" — the assistant collapses back to the launcher icon and behaves like on-demand mode for the rest of that browser session (tracked client-side via `sessionStorage`), rather than re-prompting on subsequent page loads.

The mode and delay are served in the public config projection (`engagementMode`, `proactiveDelayMs`) and enforced entirely in `widget.js`; no per-page integration code is required.

## Assistant quick actions (blueprint functions)

The assistant's quick-action buttons expose the canonical visitor functions defined by the common site blueprint (`skills/ep044_group/ep044_common_site_blueprint`, sections 2 and 4): Services, Our Work (Gallery), Before & After, Reviews, About Us, Pricing Guide, Areas Covered, Knowledge Centre, FAQ, Contact, Request a Quote, Book, and Request a Callback. The vocabulary and ordering live in `src/blueprint.js` and follow the blueprint's conversion hierarchy.

Buttons are resolved per client, server-side, and only appear when the function actually leads somewhere — so there are no dead ends (blueprint sections 5 and 13):

1. If the client has a page tagged with that blueprint function (`"blueprint": "gallery"` on a page, with the `navigation` module enabled), the button **navigates** straight to that real page.
2. Otherwise, if the function maps to an enabled module (FAQ, Contact, Request a Quote → `leadCapture`, Book → `booking`, Request a Callback → `callback`), the button **prompts** the assistant, which answers or offers that module.
3. Otherwise, if the function is answerable from approved knowledge (Services, About Us, Pricing, Areas) **and the retriever actually matches** knowledge for it, the button prompts the assistant.
4. Otherwise the button is hidden.

An unrecognised `blueprint` tag on a page is dropped during normalisation, so a typo can never surface a button that navigates nowhere.

Platform demonstration workflows (Demo booking / payment / email / CRM) are **not** blueprint visitor functions; in demo-mode clients they are resolved separately (`demoActions`) and rendered under a distinct "Platform demonstration" divider so a genuine visitor is not confused. The resolved lists are exposed in the public config as `assistantActions` and `demoActions`.

Not yet in this feature (planned as a follow-up): the blueprint section 4 assistant *behaviours* — consent before storing personal data, a structured lead summary for the business, escalate-to-human, and explicit AI self-identification.

## AI behavior

Without `OPENAI_API_KEY`, the assistant uses the approved knowledge retriever and deterministic response composer. This is intentional: demo mode remains fully reviewable and never invents business facts.

With `OPENAI_API_KEY`, the central service calls the OpenAI Responses API. The model receives only the resolved client's approved knowledge, contact data, enabled-module context, and bounded conversation history. Set `OPENAI_MODEL` to control the deployment model. The API key remains server-side.

## Visitor analytics

Every embedded site can log **anonymous** visitor behaviour through the same service, giving each client insight into how people use their site — without a third-party analytics tool and without identifying any visitor.

```html
<script src="https://assistant.example.com/analytics-embed.js" data-client="CLIENT_PUBLIC_KEY" data-api-base="https://assistant.example.com" async></script>
```

- **Anonymous, PII-free by contract**: there is **no persistent visitor identifier** — only an ephemeral, tab-scoped `sessionId` (sessionStorage, ~30 min, gone when the browser closes), so a person is never tracked across visits or days. It sends only event type, page path (never query strings), referrer host, device class, scroll %, and dwell time. Honours Do Not Track and a per-visit opt-out (`window.aiwAnalytics.optOut()`).
- **Per-site on/off switch**: controlled per client via `analyticsEnabled` (admin toggle, exposed in the public config), enforced at the endpoint — when off, events are accepted-and-dropped and nothing is stored.
- **Auto-captured events**: page view, scroll depth, dwell/exit, CTA clicks (`data-ev="cta:quote"` attributes), phone/email/WhatsApp taps, outbound clicks, form start/submit, gallery opens, and assistant open/handoff.
- **Joined to chat within a visit**: the tracker shares its ephemeral `sessionId` with `widget.js` (same `aiw-session` key), so page behaviour and the assistant conversation join into one visit — without any durable identity.
- **Ingestion**: batched via `navigator.sendBeacon` to `POST /api/public/events` — tenant-resolved and host-allow-listed like every other public route, event types whitelisted server-side, stored in a larger ring buffer (`events`, cap 20k) than the lead/conversation records.
- **Reporting**: the admin **Visitor insights** view aggregates per client — unique visits, page views, engaged-visit rate, enquiries, phone/email/CTA taps, assistant opens/handoffs, average dwell and scroll, top pages, and an event breakdown. Raw events are also browsable under Activity → Visitor events. A **From / To / Page** filter narrows every stat to an exact window (e.g. "page views of `/services` between 10am and 12pm").

## Site owner console

The visitor-insights aggregates above are also reachable **directly by the site owner**, without giving them access to the shared admin panel (which spans every tenant). A small ⚙ icon in the widget's own header — visible only once the widget is open — unlocks a compact, in-widget version of Visitor insights (same stats, same From/To/Page filter) after the owner enters a per-client console password.

- **Inherently single-tenant**: the widget only ever knows its own `clientKey`, so the console can never show another client's data — no separate per-site authorization model had to be built to guarantee that.
- **Opt-in per client**: set (or clear) a client's console password in the admin editor's "Site owner console" section. No password set = the console login always answers 403, so nothing changes for clients who don't want it.
- **Session-scoped, rate-limited**: a correct password issues a 2-hour bearer token (in-memory only, not persisted); 5 wrong attempts locks that client out for 5 minutes. Passwords are compared with a timing-safe check and are never included in the public config projection the browser can read.
- **Same anonymity contract as Visitor analytics**: the console only ever receives pre-aggregated numbers (`GET /api/public/owner/insights`) — no raw session ids or individual event rows reach the browser.

For production traffic, point the `events` sink at a managed store rather than the JSON ring buffer (same caveat as the rest of persistence, below).

## Master-prompt coverage

| Component | Implementation |
|---|---|
| AI assistant | `/api/public/chat`, session history, approved-context responses, optional model adapter |
| FAQ | Knowledge retrieval and FAQ quick action |
| Navigation | Client page map and navigation actions |
| Appointment booking | Provider-agnostic booking config and booking action |
| Callback requests | Widget form, validated API, demo/live notification behavior |
| Lead capture | Widget form, validated API, secure server-side storage |
| Contact assistance | Client-specific contact details and method actions |
| Business knowledge | Editable client knowledge records; no code change required |
| Demo mode | Visible notice, simulated notifications, safe feature demonstrations |
| Live mode | Configuration switch activates live booking/notification behavior without rebuild |
| Client configuration | Branding, hosts, contact, booking, knowledge, modules and destinations |
| Administration | Create, duplicate, edit, switch status, and inspect conversations/leads/callbacks |

## Security baseline

- Tenant resolution occurs on every public request; the browser never selects arbitrary internal IDs.
- Public responses expose only a safe configuration projection.
- Admin endpoints require bearer authentication and use constant-time token comparison.
- Inputs are size-limited, normalized, and HTML is never injected into the widget.
- Demo submissions are marked simulated and never trigger external notifications.
- Live webhook notifications are opt-in through `NOTIFICATION_WEBHOOK_URL`.
- Secrets belong in environment variables, never in `clients.json` or widget attributes.

Before production use, place the service behind TLS and a reverse proxy, move persistence to a managed database, add administrator identity/roles, configure rate limiting and retention, and complete a privacy/security review for the jurisdictions served.

## Test

```powershell
npm test
npm run check
```

The suite starts an isolated service with temporary data and validates tenant resolution, safe configuration, knowledge grounding, module gating, demo/live submission behavior, admin authorization, persistence, and static delivery.
