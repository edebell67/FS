import { and, desc, eq, gt, isNull, ne, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import {
  businesses, claimRequests, pipelineStages, stageTransitions,
  fieldValidationOutcomes, verificationLinks, verificationSubmissions,
  verificationDeliveries, verificationDeliveryEvents,
} from "@/lib/db/schema";
import {
  generateVerificationToken, hashVerificationToken, isValidRawToken, normalizeExpiryDays,
} from "./tokens";
import type { VerificationInput } from "./types";

export const PRIVACY_NOTICE_VERSION = "2026-07-25";
export const CONTROLLED_STAGE_KEYS = new Set([
  "verification_email_pending", "verification_sent", "verification_opened",
  "verification_completed", "business_claimed",
]);

export function canManageVerification(role: string): boolean {
  return ["super_admin", "admin", "operations"].includes(role);
}

export async function issueVerificationLink(businessId: string, actorUserId: string, expiry: unknown = 5) {
  const expiresInDays = normalizeExpiryDays(expiry);
  const rawToken = generateVerificationToken();
  const tokenHash = hashVerificationToken(rawToken);
  const expiresAt = new Date(Date.now() + expiresInDays * 86_400_000);

  const link = await db.transaction(async (tx) => {
    const [business] = await tx.select().from(businesses).where(eq(businesses.id, businessId)).limit(1);
    if (!business) throw new Error("Business not found.");
    const outstanding = business.lastValidationRunId ? await tx.select({
      fieldName: fieldValidationOutcomes.fieldName,
    }).from(fieldValidationOutcomes).where(and(
      eq(fieldValidationOutcomes.runId, business.lastValidationRunId),
      eq(fieldValidationOutcomes.passed, false),
    )) : [];
    await tx.update(verificationLinks).set({ revokedAt: new Date() }).where(and(
      eq(verificationLinks.businessId, businessId), isNull(verificationLinks.revokedAt),
      isNull(verificationLinks.submittedAt), gt(verificationLinks.expiresAt, new Date()),
    ));
    const [created] = await tx.insert(verificationLinks).values({
      businessId, tokenHash, expiresAt, expiresInDays, createdByUserId: actorUserId,
      validationStatusAtIssue: business.validationStatus, validationRunId: business.lastValidationRunId,
      outstandingFields: [...new Set(outstanding.map((item) => item.fieldName))],
    }).returning();
    if (!created) throw new Error("Unable to create verification link.");
    const [stage] = await tx.select().from(pipelineStages)
      .where(eq(pipelineStages.key, "verification_email_pending")).limit(1);
    if (stage && business.currentStageId !== stage.id) {
      const now = new Date();
      await tx.update(businesses).set({ currentStageId: stage.id, stageEnteredAt: now, lastUpdated: now })
        .where(eq(businesses.id, businessId));
      await tx.insert(stageTransitions).values({
        businessId, fromStageId: business.currentStageId, toStageId: stage.id, source: "admin",
        actorUserId, reason: "Verification delivery prepared",
      });
    }
    return created;
  });
  return { rawToken, id: link.id, expiresAt: link.expiresAt, expiresInDays };
}

export async function getVerificationByRawToken(rawToken: string, markOpened = true) {
  if (!isValidRawToken(rawToken)) return null;
  const tokenHash = hashVerificationToken(rawToken);
  const [row] = await db.select({
    linkId: verificationLinks.id, businessId: businesses.id, expiresAt: verificationLinks.expiresAt,
    businessName: businesses.businessName, tradingName: businesses.tradingName,
    phone: businesses.phone, email: businesses.email, website: businesses.website,
    address: businesses.address, town: businesses.town, postcode: businesses.postcode,
    category: businesses.category, validationStatusAtIssue: verificationLinks.validationStatusAtIssue,
    outstandingFields: verificationLinks.outstandingFields,
  }).from(verificationLinks).innerJoin(businesses, eq(verificationLinks.businessId, businesses.id))
    .where(and(eq(verificationLinks.tokenHash, tokenHash), isNull(verificationLinks.revokedAt),
      isNull(verificationLinks.submittedAt), gt(verificationLinks.expiresAt, new Date()))).limit(1);
  if (!row) return null;
  if (markOpened) {
    await db.update(verificationLinks).set({ openedAt: new Date() })
      .where(and(eq(verificationLinks.id, row.linkId), isNull(verificationLinks.openedAt)));
  }
  return row;
}

export async function submitVerification(rawToken: string, input: VerificationInput) {
  if (!isValidRawToken(rawToken) || !input.accuracyConfirmed || !input.requesterName.trim()) return null;
  const allowed = ["owner", "employee", "authorised_representative", "other"];
  if (!allowed.includes(input.relationship)) return null;
  const tokenHash = hashVerificationToken(rawToken);
  return db.transaction(async (tx) => {
    const locked = await tx.execute(sql`
      SELECT id, business_id FROM verification_links
      WHERE token_hash=${tokenHash} AND revoked_at IS NULL AND submitted_at IS NULL AND expires_at > now()
      FOR UPDATE`);
    const link = locked.rows[0] as { id: string; business_id: string } | undefined;
    if (!link) return null;
    const now = new Date();
    const [submission] = await tx.insert(verificationSubmissions).values({
      linkId: link.id, businessId: link.business_id, submittedFields: input.fields,
      relationshipToBusiness: input.relationship, accuracyConfirmedAt: now,
      privacyNoticeVersion: PRIVACY_NOTICE_VERSION, requesterEmail: input.contactEmail || null,
      requesterPhone: input.contactPhone || null, submittedAt: now,
    }).returning();
    if (!submission) throw new Error("Unable to save verification submission.");
    await tx.update(verificationLinks).set({ submittedAt: now }).where(eq(verificationLinks.id, link.id));
    const deliveries = await tx.update(verificationDeliveries).set({
      status: "completed", completedAt: now,
    }).where(and(
      eq(verificationDeliveries.verificationLinkId, link.id),
      ne(verificationDeliveries.status, "revoked"),
    )).returning({ id: verificationDeliveries.id });
    if (deliveries.length) await tx.insert(verificationDeliveryEvents).values(
      deliveries.map((delivery) => ({
        deliveryId: delivery.id, eventType: "completed" as const,
        metadata: { source: "verification_submission" },
      })),
    );
    const [claim] = await tx.insert(claimRequests).values({
      businessId: link.business_id, submissionId: submission.id, status: "pending",
      requesterName: input.requesterName.trim(), relationship: input.relationship,
      contactEmail: input.contactEmail || null, contactPhone: input.contactPhone || null,
    }).returning();
    if (!claim) throw new Error("Unable to create claim request.");
    const [stage] = await tx.select().from(pipelineStages)
      .where(eq(pipelineStages.key, "verification_completed")).limit(1);
    const [business] = await tx.select().from(businesses).where(eq(businesses.id, link.business_id)).limit(1);
    if (stage && business && business.currentStageId !== stage.id) {
      await tx.update(businesses).set({ currentStageId: stage.id, stageEnteredAt: now, lastUpdated: now })
        .where(eq(businesses.id, link.business_id));
      await tx.insert(stageTransitions).values({
        businessId: link.business_id, fromStageId: business.currentStageId, toStageId: stage.id,
        occurredAt: now, source: "owner", reason: "Verification submitted; manual review required",
      });
    }
    return { submissionId: submission.id, claimRequestId: claim.id };
  });
}

export async function getLatestVerificationForBusiness(businessId: string) {
  const [row] = await db.select().from(verificationLinks)
    .where(eq(verificationLinks.businessId, businessId)).orderBy(desc(verificationLinks.createdAt)).limit(1);
  return row ?? null;
}

export async function revokeVerificationLink(linkId: string) {
  return db.transaction(async (tx) => {
    const now = new Date();
    const rows = await tx.update(verificationLinks).set({ revokedAt: now })
      .where(and(eq(verificationLinks.id, linkId), isNull(verificationLinks.submittedAt)))
      .returning({ id: verificationLinks.id });
    if (!rows.length) return false;
    const deliveries = await tx.update(verificationDeliveries).set({
      status: "revoked", revokedAt: now,
    }).where(and(
      eq(verificationDeliveries.verificationLinkId, linkId),
      ne(verificationDeliveries.status, "completed"),
      ne(verificationDeliveries.status, "revoked"),
    ))
      .returning({ id: verificationDeliveries.id });
    if (deliveries.length) await tx.insert(verificationDeliveryEvents).values(
      deliveries.map((delivery) => ({
        deliveryId: delivery.id, eventType: "revoked" as const, metadata: {},
      })),
    );
    return true;
  });
}

export async function getLatestDeliveryForBusiness(businessId: string) {
  const [row] = await db.select({
    id: verificationDeliveries.id, status: verificationDeliveries.status,
    recipientAddress: verificationDeliveries.recipientAddress,
    createdAt: verificationDeliveries.createdAt, sentAt: verificationDeliveries.sentAt,
    openedAt: verificationDeliveries.openedAt, clickedAt: verificationDeliveries.clickedAt,
    completedAt: verificationDeliveries.completedAt, failedAt: verificationDeliveries.failedAt,
    revokedAt: verificationDeliveries.revokedAt, failureReason: verificationDeliveries.failureReason,
  }).from(verificationDeliveries)
    .innerJoin(verificationLinks, eq(verificationDeliveries.verificationLinkId, verificationLinks.id))
    .where(eq(verificationLinks.businessId, businessId))
    .orderBy(desc(verificationDeliveries.createdAt)).limit(1);
  return row ?? null;
}

export async function approveClaim(claimRequestId: string, actorUserId: string, note?: string) {
  return db.transaction(async (tx) => {
    const rows = await tx.execute(sql`SELECT * FROM claim_requests WHERE id=${claimRequestId} FOR UPDATE`);
    const claim = rows.rows[0] as { id: string; business_id: string; status: string; submission_id: string | null } | undefined;
    if (!claim || claim.status !== "pending" || !claim.submission_id) return false;
    const [claimedStage] = await tx.select().from(pipelineStages).where(eq(pipelineStages.key, "business_claimed")).limit(1);
    const [business] = await tx.select().from(businesses).where(eq(businesses.id, claim.business_id)).limit(1);
    if (!claimedStage || !business) return false;
    const now = new Date();
    await tx.update(claimRequests).set({ status: "approved", reviewerUserId: actorUserId,
      reviewedAt: now, decisionNote: note || null, updatedAt: now }).where(eq(claimRequests.id, claim.id));
    await tx.update(businesses).set({ status: "claimed", currentStageId: claimedStage.id,
      stageEnteredAt: now, lastUpdated: now }).where(eq(businesses.id, claim.business_id));
    await tx.insert(stageTransitions).values({ businessId: claim.business_id,
      fromStageId: business.currentStageId, toStageId: claimedStage.id, occurredAt: now,
      source: "admin", actorUserId, reason: "Owner claim manually approved", notes: note });
    return true;
  });
}

export async function getClaimForReview(id: string) {
  const [row] = await db.select({
    id: claimRequests.id, status: claimRequests.status, requesterName: claimRequests.requesterName,
    relationship: claimRequests.relationship, contactEmail: claimRequests.contactEmail,
    contactPhone: claimRequests.contactPhone, decisionNote: claimRequests.decisionNote,
    businessId: businesses.id, businessRef: businesses.businessRef, businessName: businesses.businessName,
    submittedFields: verificationSubmissions.submittedFields,
  }).from(claimRequests).innerJoin(businesses, eq(claimRequests.businessId, businesses.id))
    .leftJoin(verificationSubmissions, eq(claimRequests.submissionId, verificationSubmissions.id))
    .where(eq(claimRequests.id, id)).limit(1);
  return row ?? null;
}
