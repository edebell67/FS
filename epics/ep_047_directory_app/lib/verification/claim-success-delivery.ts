import { and, eq, inArray, isNull } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { claimSuccessMessages } from "@/lib/db/schema";
import { createGmailApiTransport } from "./delivery";
import { escapeEmailHtml, renderTheTechPrincipleEmail } from "@/lib/email/brand";

function recipients() { return (process.env.CLAIM_SUCCESS_RECIPIENT_ALLOWLIST ?? "").split(",").map((x) => x.trim().toLowerCase()).filter(Boolean); }
export function claimSuccessDeliveryEnabled() {
  return process.env.CLAIM_SUCCESS_DELIVERY_MODE === "gmail-api" &&
    process.env.CLAIM_SUCCESS_DELIVERY_APPROVED === "true" && recipients().length > 0;
}

/** Sends only messages explicitly created by the just-authorised approval action. */
export async function sendPreparedClaimSuccessMessages(messageIds: string[]) {
  if (!messageIds.length || !claimSuccessDeliveryEnabled()) return { sent: 0, prepared: messageIds.length };
  const allowed = recipients();
  const rows = await db.select().from(claimSuccessMessages).where(and(
    inArray(claimSuccessMessages.id, messageIds), eq(claimSuccessMessages.status, "prepared"),
  ));
  const transport = createGmailApiTransport(process.env, fetch, allowed);
  let sent = 0;
  for (const row of rows) {
    if (!row.recipientAddress || !allowed.includes(row.recipientAddress.toLowerCase())) continue;
    try {
      const result = await transport.sendMessage({ from: "edward.bell@thetechprinciple.com", to: row.recipientAddress,
        subject: row.subject, text: row.textBody, html: renderTheTechPrincipleEmail({
          eyebrow: "Listing claim confirmed", heading: row.subject,
          bodyHtml: row.textBody.split("\n\n").map((paragraph) => `<p style="margin:0 0 14px">${escapeEmailHtml(paragraph).replace(/\n/g, "<br>")}</p>`).join(""),
          footerDetail: `thetechprinciple.com · Reply to this email for support or to update your contact preferences.<br><br>This is a service message about your business listing.<br><br>${escapeEmailHtml(process.env.VERIFICATION_SENDER_ADDRESS?.trim() || "[Registered business address — to be added]")}`,
        }) });
      await db.update(claimSuccessMessages).set({ status: "sent", sentAt: new Date(), providerMessageId: result.messageId })
        .where(and(eq(claimSuccessMessages.id, row.id), isNull(claimSuccessMessages.sentAt)));
      sent++;
    } catch {
      await db.update(claimSuccessMessages).set({ status: "failed", failedAt: new Date(), failureReason: "Gmail API handoff failed." }).where(eq(claimSuccessMessages.id, row.id));
    }
  }
  return { sent, prepared: rows.length - sent };
}

export async function sendAllPreparedClaimSuccessMessages() {
  const rows = await db.select({ id: claimSuccessMessages.id }).from(claimSuccessMessages)
    .where(eq(claimSuccessMessages.status, "prepared")).limit(100);
  return sendPreparedClaimSuccessMessages(rows.map((row) => row.id));
}
