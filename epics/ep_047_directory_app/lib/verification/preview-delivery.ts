/**
 * lib/verification/preview-delivery.ts — the six web-activation message templates
 * plus fail-closed prepare/send for preview-ready, ETA, ready-for-activation and
 * the three reminder nudges.
 *
 * VERSION HISTORY
 * v1.2.0 · 2026-08-06 · Extracts preview/review URLs from text body to render both CTAs as branded buttons.
 * v1.1.0 · 2026-08-05 · Adds a separately audited, explicitly authorized owner-review invitation message type.
 * v1.0.0 · 2026-07-29 · Initial version: six message builders, previewDeliveryEnabled()
 *   gating (mode + explicit approval + non-empty allowlist, mirroring the existing
 *   verification and claim-success paths), and preparePreviewMessage() /
 *   sendPreparedPreviewMessage() kept as deliberately separate actions so preparing
 *   a message never implies it was sent.
 */

import { and, desc, eq, isNull } from "drizzle-orm";
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

/** Renders the branded The Tech Principle email template around any text body. */
function renderBrandedEmail(subject: string, textBody: string): string {
  const escapedSubject = subject.replace(/[&<>\"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" })[c]!);
  const escapedBody = textBody
      .replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" })[c]!)
      .replace(/\n/g, "<br>");
    // Extract URLs from the fixed text body format written by previewReadyMessage()
    const lines = textBody.split("\n");
    let siteUrl = "", reviewUrl = "";
    for (let i = 0; i < lines.length; i++) {
      const t = lines[i]!.trim();
      if (t === "Preview it here:" && i + 1 < lines.length) siteUrl = lines[i + 1]!.trim();
      if (t.startsWith("Submit your review securely here:") && i + 1 < lines.length) reviewUrl = lines[i + 1]!.trim();
    }
    const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" })[c]!);
    const reviewBtn = reviewUrl
      ? `<a class="cta" href="${esc(reviewUrl)}" style="background:#00765e;color:white!important;text-decoration:none;padding:13px 19px;border-radius:3px;font-weight:bold;margin:10px 0 18px;display:inline-block">Review your website</a>`
      : "";
    const siteBtn = siteUrl
      ? `<a class="cta" href="${esc(siteUrl)}" style="background:#152b2a;color:white!important;text-decoration:none;padding:13px 19px;border-radius:3px;font-weight:bold;margin:10px 0 18px;display:inline-block">View website preview</a>`
      : "";
    const ctaRow = [reviewBtn, siteBtn].filter(Boolean).join("&nbsp;&nbsp;");
  return `<!doctype html>\n<html lang="en">\n<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n<style>body{margin:0;background:#e7ecea;font:15px Arial,sans-serif;color:#152022}.wrap{max-width:620px;margin:auto;padding:38px 18px}.inbox{background:#fff;box-shadow:0 6px 26px #17332a22}.top{background:#152b2a;padding:30px;color:white}.brand{font:700 22px Georgia,serif}.tag{margin-top:5px;color:#b8d9ce;font-size:11px;letter-spacing:.12em;text-transform:uppercase}.body{padding:34px 34px 20px;line-height:1.6}.eyebrow{color:#00765e;font-size:11px;font-weight:bold;letter-spacing:.12em;text-transform:uppercase}.cta-row{margin:10px 0 18px}.foot{border-top:1px solid #dce3df;padding:22px 34px 30px;color:#63716b;font-size:12px;line-height:1.5}</style></head>\n<body><div class="wrap"><div class="inbox"><div class="top"><div class="brand">The Tech Principle</div><div class="tag">Local business directory &amp; website support</div></div>\n<div class="body"><div class="eyebrow">Website preview</div><h2 style="font-size:1.4rem;color:#152022;margin:10px 0 16px">${escapedSubject}</h2>\n<p style="margin:0 0 14px">Hello,</p>\n<p style="margin:0 0 14px">${escapedBody}</p>\n${ctaRow ? `<div class="cta-row">${ctaRow}</div>` : ""}</div>\n<div class="foot"><strong>The Tech Principle</strong><br>thetechprinciple.com · Reply to this email for support or to update your contact preferences.<br><br>This is a service message about your business listing or website. We do not treat a prepared message as sent, or sent as delivered, without delivery evidence.</div></div></div></body></html>`;
}

export function previewReadyMessage(businessName: string, siteUrl: string, reviewUrl?: string) {
  const subject = `Your website preview is ready — ${businessName}`;
  const reviewSection = reviewUrl ? `\n\nSubmit your review securely here:\n${reviewUrl}` : "";
  const text = `Hello,\n\nThe website for ${businessName} has been generated and is ready to review.\n\nPreview it here:\n${siteUrl}\n\nA website can provide an owner-controlled social profile, stronger visibility to a local audience, and improved lead-generation potential.\n\nReview each page and either request changes or confirm you're happy with it as-is — there's a "no action required" option per page for anything you don't want changed.${reviewSection}\n\nYou might also be interested in local business news for your area:\n${NEWS_URL}`;
  return { subject, text };
}

export function etaMessage(businessName: string, readyForActivationDate: Date) {
  const dateLabel = readyForActivationDate.toISOString().slice(0, 10);
  const subject = `Estimated ready date for your website — ${businessName}`;
  const text = `Hello,\n\nThanks for reviewing the website preview for ${businessName}. We've gone through your requested changes and expect the site to be ready for activation by ${dateLabel}.\n\nWe'll be in touch again once it's ready.`;
  return { subject, text };
}

export function readyForActivationMessage(businessName: string) {
  const subject = `Your website is ready to activate — ${businessName}`;
  const text = `Hello,\n\nThe website for ${businessName} has been updated with your requested changes and is ready.\n\nActivating your site is a separate step you control — we'll send you the activation details as their own message.`;
  return { subject, text };
}

export function reminderIntakeMessage(businessName: string) {
  const subject = `A quick reminder — your website preview for ${businessName}`;
  const text = `Hello,\n\nJust checking in — we haven't heard back about the website preview for ${businessName} yet.\n\nWhenever you get a chance, take a look and let us know if anything needs changing, or confirm you're happy with it as-is.`;
  return { subject, text };
}

export function reminderReviewMessage(businessName: string) {
  const subject = `We need a bit more information — ${businessName}`;
  const text = `Hello,\n\nWhile reviewing your requested changes for ${businessName}, we need a little more information before we can proceed.\n\nCould you reply with the details we asked for when you get a chance?`;
  return { subject, text };
}

export function reminderActivationMessage(businessName: string) {
  const subject = `Your website is still waiting to be activated — ${businessName}`;
  const text = `Hello,\n\nThe website for ${businessName} has been ready for a little while now. Whenever you're ready, the activation details from our earlier message are still valid.`;
  return { subject, text };
}

type PreviewMessageType =
  | "preview_ready" | "owner_review_invitation" | "eta" | "ready_for_activation"
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
      html: renderBrandedEmail(row.subject, row.textBody),
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

/** Returns the most recent preview delivery message for display on the business detail page. */
export async function getLatestPreviewMessageForBusiness(businessId: string) {
  const [row] = await db.select({
    id: previewDeliveryMessages.id,
    messageType: previewDeliveryMessages.messageType,
    status: previewDeliveryMessages.status,
    recipientAddress: previewDeliveryMessages.recipientAddress,
    subject: previewDeliveryMessages.subject,
    textBody: previewDeliveryMessages.textBody,
    sentAt: previewDeliveryMessages.sentAt,
    failureReason: previewDeliveryMessages.failureReason,
    createdAt: previewDeliveryMessages.createdAt,
  }).from(previewDeliveryMessages)
    .where(eq(previewDeliveryMessages.businessId, businessId))
    .orderBy(desc(previewDeliveryMessages.createdAt)).limit(1);
  return row ?? null;
}