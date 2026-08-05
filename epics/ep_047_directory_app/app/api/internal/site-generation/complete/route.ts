/**
 * The protected completion seam for generated customer-proxy sites.
 * Normal recording is one-shot; replacement requires the explicit, audited
 * recover_generated_site_after_manual_review action.
 */

import { NextResponse } from "next/server";
import { requireInternalApiKey } from "@/lib/auth/require-internal-api";
import {
  recordSiteGenerated,
  recoverGeneratedSiteAfterManualReview,
  replaceGeneratedSiteAfterRegeneration,
} from "@/lib/verification/site-generation";

const SYSTEM_ACTOR_ID = "00000000-0000-0000-0000-000000000000";
const RECOVERY_ACTION = "recover_generated_site_after_manual_review";

type CompletionRequest = {
  businessId?: string;
  siteUrl?: string;
  action?: string;
  recoveryReason?: string;
  regenerationReason?: string;
};

export async function POST(request: Request) {
  const auth = await requireInternalApiKey(request);
  if (auth) return auth;

  let body: CompletionRequest = {};
  try { body = await request.json(); } catch {}
  if (!body.businessId || !body.siteUrl) {
    return NextResponse.json({ error: "businessId and siteUrl are required." }, { status: 400 });
  }

  try {
    if (body.action === undefined || body.action === "record") {
      await recordSiteGenerated({
        businessId: body.businessId, siteUrl: body.siteUrl, actorUserId: SYSTEM_ACTOR_ID,
      });
      return NextResponse.json({ recorded: true });
    }

    if (body.action === RECOVERY_ACTION) {
      if (!body.recoveryReason?.trim()) {
        return NextResponse.json({ error: "recoveryReason is required for generated-site recovery." }, { status: 400 });
      }
      await recoverGeneratedSiteAfterManualReview({
        businessId: body.businessId,
        siteUrl: body.siteUrl,
        actorUserId: SYSTEM_ACTOR_ID,
        recoveryReason: body.recoveryReason,
      });
      return NextResponse.json({ recovered: true, action: RECOVERY_ACTION });
    }

    if (body.action === "replace_after_regeneration") {
      if (!body.regenerationReason?.trim()) {
        return NextResponse.json({ error: "regenerationReason is required for verified regeneration completion." }, { status: 400 });
      }
      await replaceGeneratedSiteAfterRegeneration({
        businessId: body.businessId, siteUrl: body.siteUrl, actorUserId: SYSTEM_ACTOR_ID,
        regenerationReason: body.regenerationReason,
      });
      return NextResponse.json({ regenerated: true, action: "replace_after_regeneration" });
    }

    return NextResponse.json({ error: "Unsupported site-generation completion action." }, { status: 400 });
  } catch (error) {
    return NextResponse.json({
      error: error instanceof Error ? error.message : "Unable to record site generation.",
    }, { status: 400 });
  }
}
