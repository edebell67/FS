import { and, eq, isNull } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, previewDeliveryMessages } from "@/lib/db/schema";
import { createGmailApiTransport, VERIFICATION_FROM } from "./delivery";

// Same fail-closed discipline already established for verification and
// claim-success delivery: disabled by default, requires an explicit
// approval flag plus a non-empty allowlist before anything can send.
function recipients() {
  return (process.env.PREVIEW_RECIPIENT_ALLOWLIST ?? "")
    .split(",").map((value) => value.trim().toLowerCase()).filter(Boolean);
}
export function previewDeliveryEnabled() {
  return process.env.PREVIEW_DELIVERY_MODE === "gmail-api" &&
    process.env.PREVIEW_DELIVERY_APPROVED === "true" && recipients().length > 0;
}

const NEWS_URL = "https://thetechprinciple.com/news/";

export function previewReadyMessage(businessName: string, siteUrl: string) {
  const subject = `Your website preview is ready — ${businessName}`;
  const text = `Hello,

The website for ${businessName} has been generated and is ready to review.

Preview it here:
${siteUrl}

A website can provide an owner-controlled social profile, stronger visibility to a local audience, and improved lead-generation potential.

Review each page and either request changes or confirm you're happy with it as-is — there's a "no action required" option per page for anything you don't want changed.

You might also be interested in local business news for your area:
${NEWS_URL}`;
  return { subject, text };
}

export function etaMessage(businessName: string, readyForActivationDate: Date) {
  const dateLabel = readyForActivationDate.toISOString().slice(0, 10);
  const subject = `Estimated ready date for your website — ${businessName}`;
  const text = `Hello,

Thanks for reviewing the website preview for ${businessName}. We've gone through your requested changes and expect the site to be ready for activation by ${dateLabel}.

We'll be in touch again once it's ready.`;
  return { subject, text };
}

export function readyForActivationMessage(businessName: string) {
  const subject = `Your website is ready to activate — ${businessName}`;
  const text = `Hello,

The website for ${businessName} has been updated with your requested changes and is ready.

Activating your site is a separate step you control — we'll send you the activation details as their own message.`;
  return { subject, text };
}

export function reminderIntakeMessage(businessName: string) {
  const subject = `A quick reminder — your website preview for ${businessName}`;
  const text = `Hello,

Just checking in — we haven't heard back about the website preview for ${businessName} yet.

Whenever you get a chance, take a look and let us know if anything needs changing, or confirm you're happy with it as-is.`;
  return { subject, text };
}

export function reminderReviewMessage(businessName: string) {
  const subject = `We need a bit more information — ${businessName}`;
  const text = `Hello,

While reviewing your requested changes for ${businessName}, we need a little more information before we can proceed.

Could you reply with the details we asked for when you get a chance?`;
  return { subject, text };
}

export function reminderActivationMessage(businessName: string) {
  const subject = `Your website is still waiting to be activated — ${businessName}`;
  const text = `Hello,

The website for ${businessName} has been ready for a little while now. Whenever you're ready, the activation details from our earlier message are still valid.`;
  return { subject, text };
}

type PreviewMessageType =
  | "preview_ready" | "eta" | "ready_for_activation"
  | "reminder_intake" | "reminder_review" | "reminder_activation";

/** Sends only a message explicitly prepared by an admin action, never a bulk/automatic broadcast. */
export async function sendPreparedPreviewMessage(messageId: string) {
  if (!previewDeliveryEnabled()) return { sent: false, reason: "Preview delivery is not enabled." };
  const allowed = recipients();
  const [row] = await db.select().from(previewDeliveryMessages)
    .where(and(eq(previewDeliveryMessages.id, messageId), eq(previewDeliveryMessages.status, "prepared")));
  if (!row) return { sent: false, reason: "No prepared message with that ID." };
  if (!row.recipientAddress || !allowed.includes(row.recipientAddress.toLowerCase())) {
    return { sent: false, reason: "Recipient is not allowlisted." };
  }
  const transport = createGmailApiTransport(process.env, fetch, allowed);
  try {
    const result = await transport.sendMessage({
      from: VERIFICATION_FROM, to: row.recipientAddress,
      subject: row.subject, text: row.textBody,
      html: `<p>${row.textBody.replace(/\n/g, "<br />")}</p>`,
    });
    await db.update(previewDeliveryMessages).set({ status: "sent", sentAt: new Date(), providerMessageId: result.messageId })
      .where(and(eq(previewDeliveryMessages.id, row.id), isNull(previewDeliveryMessages.sentAt)));
    return { sent: true };
  } catch {
    await db.update(previewDeliveryMessages).set({
      status: "failed", failedAt: new Date(), failureReason: "Gmail API handoff failed.",
    }).where(eq(previewDeliveryMessages.id, row.id));
    return { sent: false, reason: "Gmail API handoff failed." };
  }
}

/** Records a message as prepared; sending is always a distinct, explicit follow-up action. */
export async function preparePreviewMessage(input: {
  businessId: string; messageType: PreviewMessageType;
  recipientAddress: string | null; subject: string; textBody: string; actorUserId: string;
}) {
  const [row] = await db.insert(previewDeliveryMessages).values({
    businessId: input.businessId, messageType: input.messageType,
    recipientAddress: input.recipientAddress?.trim().toLowerCase() || null,
    status: input.recipientAddress ? "prepared" : "failed",
    subject: input.subject, textBody: input.textBody, actorUserId: input.actorUserId,
    failureReason: input.recipientAddress ? null : "No recipient address was available for this business.",
  }).returning({ id: previewDeliveryMessages.id });
  if (!row) throw new Error("Unable to record the prepared preview message.");
  return row.id;
}

export async function getBusinessForPreviewMessage(businessId: string) {
  const [row] = await db.select({
    id: businesses.id, businessName: businesses.businessName, email: businesses.email,
    generatedSiteUrl: businesses.generatedSiteUrl, readyForActivationDate: businesses.readyForActivationDate,
  }).from(businesses).where(eq(businesses.id, businessId));
  return row ?? null;
}
