# MVP Release Guardrails

## Security

- Open Banking consent scopes are restricted to read-only access (`accounts`, `transactions`, `balance`, `offline_access`).
- Provider base URLs must use HTTPS.
- Redirect URIs must use HTTPS in production; loopback HTTP is allowed only for local review flows.
- Bank access and refresh tokens are encrypted before being written to `bank_connection_tokens`.
- Token values returned from service responses remain redacted and are never emitted back to the client.

## Performance

- The static MVP mobile review surface is served with `no-store` cache headers and a restrictive CSP.
- Release verification checks the aggregate load time for the core inbox-review asset bundle (`/`, `app.js`, `state.js`, `styles.css`, demo JSON) and fails above 2000 ms on the local review machine.

## Legal Disclaimer

- The mobile review flow displays a release disclaimer card stating that the product is not tax advice.
- The same card states that the user remains responsible for reviewing classifications, supporting evidence, and the final export.

## Validation Entry Points

- Backend: `node verify_bank_connection.js`
- Imports: `node verify_transaction_import.js`
- Frontend release guardrails: `node verify_release_ui.js`
- Combined release gate: `node verify_release_readiness.js`
