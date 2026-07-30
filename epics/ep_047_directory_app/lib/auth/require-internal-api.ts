/**
 * lib/auth/require-internal-api.ts — bearer-key auth for server-to-server
 * endpoints called by infrastructure rather than a logged-in browser.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-29 · Initial version: requireInternalApiKey(), failing closed
 *   when INTERNAL_API_KEY is unset so a missing key can never mean "skip auth".
 */

// Server-to-server auth for endpoints called by infrastructure (a Render
// Cron Job), not a logged-in browser session -- requireAdminUserForApi
// doesn't apply here, there's no user or cookie. Fails closed: an unset
// INTERNAL_API_KEY means nothing can authenticate, not that auth is skipped.

import { NextResponse } from "next/server";

/**
 * Call at the top of every internal (non-admin-browser) Route Handler.
 * Returns null on success, or a NextResponse the caller must return
 * immediately:
 *   const auth = requireInternalApiKey(request);
 *   if (auth) return auth;
 */
export function requireInternalApiKey(request: Request): NextResponse | null {
  const configured = process.env.INTERNAL_API_KEY?.trim();
  if (!configured) {
    return NextResponse.json({ error: "Internal API is not configured." }, { status: 503 });
  }
  const provided = request.headers.get("authorization")?.replace(/^Bearer\s+/i, "").trim();
  if (!provided || provided !== configured) {
    return NextResponse.json({ error: "Not authenticated." }, { status: 401 });
  }
  return null;
}
