/**
 * lib/auth/require-internal-api.ts — auth for server-to-server endpoints
 * also reachable by an already-logged-in admin/agent session.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-07-31 · Accepts an authenticated admin session (the same
 *   cookie the browser admin console uses) as an alternative to the bearer
 *   key. Reasoning: INTERNAL_API_KEY requires a separate secret to be
 *   provisioned and distributed before these endpoints are usable at all,
 *   but a valid admin login is an equally real credential that already
 *   exists and already works -- an agent driving the admin UI (or replaying
 *   its session cookie) shouldn't need a second, redundant secret just to
 *   call the same app's own API. The bearer-key path still exists and still
 *   fails closed on its own terms, for genuine unattended server-to-server
 *   callers (a Render Cron Job) that have no browser session at all.
 * v1.0.0 · 2026-07-29 · Initial version: requireInternalApiKey(), failing closed
 *   when INTERNAL_API_KEY is unset so a missing key can never mean "skip auth".
 */

// Two legitimate ways to call these endpoints: a bearer key (for
// unattended infrastructure with no session at all, e.g. a Render Cron
// Job), or an authenticated admin session (for an agent/human already
// logged into the admin console). Neither being present is what fails
// closed -- an unset key does NOT mean "skip auth" if there's also no
// valid session.

import { NextResponse } from "next/server";
import { getCurrentUser } from "@/lib/auth/session";

/**
 * Call at the top of every internal (non-admin-browser) Route Handler.
 * Returns null on success, or a NextResponse the caller must return
 * immediately:
 *   const auth = await requireInternalApiKey(request);
 *   if (auth) return auth;
 */
export async function requireInternalApiKey(request: Request): Promise<NextResponse | null> {
  // getCurrentUser() reads Next's request-scoped cookies() -- outside a real
  // request (a unit test, or a genuine server-to-server caller with no
  // cookie jar at all) that throws rather than returning null. Either way
  // the safe fallback is the same: fall through to the bearer-key check.
  try {
    const user = await getCurrentUser();
    if (user) return null;
  } catch {
    // no session available -- fall through to the key check below
  }

  const configured = process.env.INTERNAL_API_KEY?.trim();
  if (!configured) {
    return NextResponse.json(
      { error: "Not authenticated (no admin session and no internal API key configured)." },
      { status: 401 }
    );
  }
  const provided = request.headers.get("authorization")?.replace(/^Bearer\s+/i, "").trim();
  if (!provided || provided !== configured) {
    return NextResponse.json({ error: "Not authenticated." }, { status: 401 });
  }
  return null;
}
