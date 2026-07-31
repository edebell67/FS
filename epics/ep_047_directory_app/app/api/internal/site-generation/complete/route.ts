/**
 * app/api/internal/site-generation/complete/route.ts — the single seam the
 * (deferred, model-agnostic) generation module calls once a site genuinely exists.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-29 · Initial version: POST businessId + siteUrl, internal-key
 *   authenticated; both fields required so a caller cannot record a completion
 *   without naming the URL it is asserting is live.
 */

import { NextResponse } from "next/server";
import { requireInternalApiKey } from "@/lib/auth/require-internal-api";
import { recordSiteGenerated } from "@/lib/verification/site-generation";

const SYSTEM_ACTOR_ID = "00000000-0000-0000-0000-000000000000";

/**
 * Called by the Render Cron Job (or any generation-module caller) once a
 * site genuinely exists at siteUrl -- the one seam the black-box generation
 * module needs to know how to call. Never speculative: the caller is
 * asserting the site is real by calling this at all.
 */
export async function POST(request: Request) {
  const auth = await requireInternalApiKey(request);
  if (auth) return auth;

  let body: { businessId?: string; siteUrl?: string } = {};
  try { body = await request.json(); } catch {}
  if (!body.businessId || !body.siteUrl) {
    return NextResponse.json({ error: "businessId and siteUrl are required." }, { status: 400 });
  }
  try {
    await recordSiteGenerated({
      businessId: body.businessId, siteUrl: body.siteUrl, actorUserId: SYSTEM_ACTOR_ID,
    });
    return NextResponse.json({ recorded: true });
  } catch (error) {
    return NextResponse.json({
      error: error instanceof Error ? error.message : "Unable to record site generation.",
    }, { status: 400 });
  }
}
