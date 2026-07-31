/**
 * app/api/internal/site-generation/queue/route.ts — read-only queue endpoint the
 * Render Cron Job calls to find businesses awaiting site generation.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-29 · Initial version: GET only, internal-key authenticated.
 */

import { NextResponse } from "next/server";
import { requireInternalApiKey } from "@/lib/auth/require-internal-api";
import { getBusinessesAwaitingSiteGeneration } from "@/lib/verification/site-generation";

/** Called by the Render Cron Job to fetch the current generation queue. Read-only. */
export async function GET(request: Request) {
  const auth = await requireInternalApiKey(request);
  if (auth) return auth;
  const businesses = await getBusinessesAwaitingSiteGeneration();
  return NextResponse.json({ businesses });
}
