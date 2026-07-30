/**
 * lib/verification/claims-approval.ts — pending-claim listing and the atomic
 * bulk-approval transaction.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-07-29 · Queues each approved business for automated site
 *   generation in the same transaction, so awaiting_site_generation becomes its
 *   current stage immediately; the Claimed transition is still written as its own
 *   audited row rather than skipped.
 * v1.0.0 · 2026-07-29 · Version history added; file predates this convention.
 */

import { and, asc, eq, inArray, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, claimRequests, claimSuccessMessages, pipelineStages, stageTransitions } from "@/lib/db/schema";

const PENDING_STATUSES = ["pending", "pending_contact_verification"];

export type PendingClaim = {
  id: string; businessRef: string; businessName: string; town: string | null;
  requesterName: string; relationship: string; contactEmail: string | null;
  contactPhone: string | null; createdAt: Date;
};

export async function listPendingClaims(): Promise<PendingClaim[]> {
  return db.select({
    id: claimRequests.id, businessRef: businesses.businessRef, businessName: businesses.businessName,
    town: businesses.town, requesterName: claimRequests.requesterName, relationship: claimRequests.relationship,
    contactEmail: claimRequests.contactEmail, contactPhone: claimRequests.contactPhone, createdAt: claimRequests.createdAt,
  }).from(claimRequests).innerJoin(businesses, eq(claimRequests.businessId, businesses.id))
    .where(inArray(claimRequests.status, PENDING_STATUSES)).orderBy(asc(claimRequests.createdAt));
}

export async function getPendingClaimCount(): Promise<number> {
  const [row] = await db.select({ count: sql<number>`count(*)::int` }).from(claimRequests)
    .where(inArray(claimRequests.status, PENDING_STATUSES));
  return row?.count ?? 0;
}

export function claimSuccessMessage(businessName: string) {
  const subject = `You have successfully claimed ${businessName}`;
  const text = `You have successfully claimed this business listing for ${businessName}.

Your website can now be previewed. A website can provide an owner-controlled social profile, stronger visibility to a local audience, and improved lead-generation potential.

You can reply with suggested changes or provide approved assets for incorporation, including your company logo, branding, colours, photography, and copy. No public website changes are made without your review and approval.`;
  return { subject, text };
}

export type ApprovalResult = { approved: number; skipped: number; messagesPrepared: number; messagesNotReady: number; messageIds: string[] };

/**
 * Revalidates every selection in the same transaction that records the
 * decision. Each claim gets its own transition and message snapshot; a stale
 * or already-decided ID is skipped rather than changing another record.
 */
export async function approveSelectedClaims(input: { claimIds: string[]; actorUserId: string; note?: string }): Promise<ApprovalResult> {
  const ids = [...new Set(input.claimIds)].filter((id) => /^[0-9a-f-]{36}$/i.test(id));
  if (!ids.length) throw new Error("Select at least one pending claim.");
  return db.transaction(async (tx) => {
    const [claimedStage] = await tx.select().from(pipelineStages)
      .where(eq(pipelineStages.key, "business_claimed")).limit(1);
    if (!claimedStage) throw new Error("The Claimed pipeline stage is unavailable.");
    const [queueStage] = await tx.select().from(pipelineStages)
      .where(eq(pipelineStages.key, "awaiting_site_generation")).limit(1);
    if (!queueStage) throw new Error("The Awaiting Site Generation pipeline stage is unavailable.");
    const claims = await tx.select({
      id: claimRequests.id, businessId: claimRequests.businessId, status: claimRequests.status,
      contactEmail: claimRequests.contactEmail, businessName: businesses.businessName,
      currentStageId: businesses.currentStageId,
    }).from(claimRequests).innerJoin(businesses, eq(claimRequests.businessId, businesses.id))
      .where(and(inArray(claimRequests.id, ids), inArray(claimRequests.status, PENDING_STATUSES)));
    const now = new Date();
    let prepared = 0;
    let notReady = 0;
    const messageIds: string[] = [];
    for (const claim of claims) {
      const message = claimSuccessMessage(claim.businessName);
      const recipient = claim.contactEmail?.trim().toLowerCase() || null;
      await tx.update(claimRequests).set({ status: "approved", reviewerUserId: input.actorUserId,
        reviewedAt: now, decisionNote: input.note?.trim() || null, updatedAt: now }).where(eq(claimRequests.id, claim.id));
      await tx.update(businesses).set({ status: "claimed", currentStageId: claimedStage.id,
        stageEnteredAt: now, lastUpdated: now }).where(eq(businesses.id, claim.businessId));
      await tx.insert(stageTransitions).values({ businessId: claim.businessId, fromStageId: claim.currentStageId,
        toStageId: claimedStage.id, occurredAt: now, source: "admin", actorUserId: input.actorUserId,
        reason: "Claim approved from Claims pending queue", notes: input.note?.trim() || null });
      // Immediately queues the business for automated site generation --
      // Claimed remains a real, audited transition, not a lingering visible
      // state; the business's actual current stage becomes the queue signal.
      await tx.update(businesses).set({ currentStageId: queueStage.id, stageEnteredAt: now, lastUpdated: now })
        .where(eq(businesses.id, claim.businessId));
      await tx.insert(stageTransitions).values({ businessId: claim.businessId, fromStageId: claimedStage.id,
        toStageId: queueStage.id, occurredAt: now, source: "automation", actorUserId: input.actorUserId,
        reason: "Claim approved; queued for automated site generation" });
      const [messageRecord] = await tx.insert(claimSuccessMessages).values({ claimRequestId: claim.id, businessId: claim.businessId,
        recipientAddress: recipient, status: recipient ? "prepared" : "not_ready", subject: message.subject,
        textBody: message.text, actorUserId: input.actorUserId,
        failureReason: recipient ? null : "No owner email was supplied with this claim request." }).returning({ id: claimSuccessMessages.id });
      if (messageRecord) messageIds.push(messageRecord.id);
      if (recipient) prepared += 1; else notReady += 1;
    }
    return { approved: claims.length, skipped: ids.length - claims.length, messagesPrepared: prepared, messagesNotReady: notReady, messageIds };
  });
}
