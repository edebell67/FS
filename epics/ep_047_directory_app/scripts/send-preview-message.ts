/**
 * scripts/send-preview-message.ts — controlled-test CLI to prepare and send any
 * one preview-delivery message type, until the admin UI for this exists.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-29 · Initial version: takes businessRef + recipient + optional
 *   messageType; refuses to run unless preview delivery is explicitly enabled.
 */

// One-off / controlled-test CLI for the preview-delivery message types, until
// the admin UI for this exists. Prepares then immediately sends a message,
// printing the result. Requires PREVIEW_DELIVERY_MODE=gmail-api,
// PREVIEW_DELIVERY_APPROVED=true, and a non-empty PREVIEW_RECIPIENT_ALLOWLIST
// containing the target recipient -- fails closed otherwise, same as every
// other delivery path in this app.
//
// Usage:
//   npx tsx scripts/send-preview-message.ts <businessRef> <recipientEmail> [messageType]
//   messageType defaults to preview_ready.

import { config } from "dotenv";
config({ path: ".env.local" });
config();

import { eq } from "drizzle-orm";
import { db } from "../lib/db/client";
import { businesses } from "../lib/db/schema";
import {
  preparePreviewMessage, sendPreparedPreviewMessage, previewDeliveryEnabled,
  previewReadyMessage, etaMessage, readyForActivationMessage,
  reminderIntakeMessage, reminderReviewMessage, reminderActivationMessage,
} from "../lib/verification/preview-delivery";

async function main() {
  const [businessRef, recipient, messageType = "preview_ready"] = process.argv.slice(2);
  if (!businessRef || !recipient) {
    console.error("Usage: npx tsx scripts/send-preview-message.ts <businessRef> <recipientEmail> [messageType]");
    process.exit(1);
  }
  if (!previewDeliveryEnabled()) {
    console.error("Preview delivery is not enabled (PREVIEW_DELIVERY_MODE/APPROVED/ALLOWLIST). Refusing to proceed.");
    process.exit(1);
  }

  const [biz] = await db.select().from(businesses).where(eq(businesses.businessRef, businessRef));
  if (!biz) { console.error(`Business ${businessRef} not found.`); process.exit(1); }
  console.log(`Business: ${biz.businessName} (${biz.id})`);

  const siteUrl = biz.generatedSiteUrl ?? "https://thetechprinciple.com/preview/example";
  const messages: Record<string, { subject: string; text: string }> = {
    preview_ready: previewReadyMessage(biz.businessName, siteUrl),
    eta: etaMessage(biz.businessName, biz.readyForActivationDate ?? new Date(Date.now() + 7 * 86400000)),
    ready_for_activation: readyForActivationMessage(biz.businessName),
    reminder_intake: reminderIntakeMessage(biz.businessName),
    reminder_review: reminderReviewMessage(biz.businessName),
    reminder_activation: reminderActivationMessage(biz.businessName),
  };
  const message = messages[messageType];
  if (!message) { console.error(`Unknown messageType "${messageType}". Valid: ${Object.keys(messages).join(", ")}`); process.exit(1); }

  const messageId = await preparePreviewMessage({
    businessId: biz.id, messageType: messageType as never,
    recipientAddress: recipient, subject: message.subject, textBody: message.text,
    actorUserId: undefined as unknown as string,
  });
  console.log(`Prepared message ${messageId}. Subject: "${message.subject}"`);

  const result = await sendPreparedPreviewMessage(messageId);
  console.log("Send result:", result);
  process.exit(result.sent ? 0 : 1);
}

main().catch((err) => { console.error("FATAL:", err); process.exit(1); });
