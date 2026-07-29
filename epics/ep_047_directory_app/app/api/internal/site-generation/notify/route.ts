import { NextResponse } from "next/server";
import { requireInternalApiKey } from "@/lib/auth/require-internal-api";
import { getBusinessesReadyForPreviewNotification } from "@/lib/verification/site-generation";
import {
  previewReadyMessage, preparePreviewMessage, sendPreparedPreviewMessage, previewDeliveryEnabled,
} from "@/lib/verification/preview-delivery";

const SYSTEM_ACTOR_ID = "00000000-0000-0000-0000-000000000000";

/**
 * Called by the Render Cron Job after each generation run (and safe to call
 * anytime -- idempotent). Sends the preview-ready notification for every
 * business at ready_for_preview that hasn't already been notified. Absence
 * of a prior preview_ready message is the entire guard; no further pipeline
 * stage is needed just to mean "already notified".
 */
export async function POST(request: Request) {
  const auth = requireInternalApiKey(request);
  if (auth) return auth;

  if (!previewDeliveryEnabled()) {
    return NextResponse.json({ notified: 0, reason: "Preview delivery is not enabled." });
  }

  const pending = await getBusinessesReadyForPreviewNotification();
  const results: Array<{ businessRef: string; sent: boolean; reason?: string }> = [];

  for (const business of pending) {
    if (!business.email || !business.generatedSiteUrl) {
      results.push({ businessRef: business.businessRef, sent: false, reason: "Missing recipient email or generated site URL." });
      continue;
    }
    const message = previewReadyMessage(business.businessName, business.generatedSiteUrl);
    const messageId = await preparePreviewMessage({
      businessId: business.id, messageType: "preview_ready",
      recipientAddress: business.email, subject: message.subject, textBody: message.text,
      actorUserId: SYSTEM_ACTOR_ID,
    });
    const result = await sendPreparedPreviewMessage(messageId);
    results.push({ businessRef: business.businessRef, sent: result.sent, reason: "reason" in result ? result.reason : undefined });
  }

  return NextResponse.json({ notified: results.filter((r) => r.sent).length, results });
}
