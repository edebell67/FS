# Hosted Identity and Access Decision

Decision: use an OIDC-capable hosting identity edge as the authentication provider boundary; keep the directory API provider-neutral.

The edge authenticates the user, owns login, MFA, session expiry, revocation and recovery, strips all inbound identity headers, and forwards only a verified user identifier plus a server-held bearer credential to the private intelligence API. The API rejects missing/invalid edge credentials and derives ownership exclusively from the verified identifier. Browsers never receive the shared edge credential. Direct access to private routes is blocked by the hosting network boundary.

Local development leaves private intelligence unloaded unless the same trusted boundary is explicitly configured. Public directory, comparison, finder and regime evidence remain anonymous and contain no private-user objects.

Hosted persistence uses PostgreSQL forced row-level security, transaction-scoped owner identity and explicit owner predicates. The runtime role is non-owner, `NOSUPERUSER` and `NOBYPASSRLS`. Cross-owner retention is isolated behind a no-argument security-definer function owned by a dedicated `NOLOGIN` role; the maintenance caller has no private-table or column privileges.

Required hosting controls:

1. OIDC Authorization Code + PKCE, secure/HTTP-only/same-site session cookies and short session lifetime.
2. Immediate provider-side session revocation on account disable or credential reset.
3. Edge header stripping and network denial of direct private-API access.
4. Server-held credentials supplied through the hosting secret store and rotated without code changes.
5. Audit logging for failed identity checks, export, deletion, consent and retention actions without logging tokens or private payloads.

The local shared-edge token is an integration credential, not a user login mechanism. Production launch is prohibited unless the deployment evidence confirms the controls above.
