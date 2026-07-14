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

## AI behavior

Without `OPENAI_API_KEY`, the assistant uses the approved knowledge retriever and deterministic response composer. This is intentional: demo mode remains fully reviewable and never invents business facts.

With `OPENAI_API_KEY`, the central service calls the OpenAI Responses API. The model receives only the resolved client's approved knowledge, contact data, enabled-module context, and bounded conversation history. Set `OPENAI_MODEL` to control the deployment model. The API key remains server-side.

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
