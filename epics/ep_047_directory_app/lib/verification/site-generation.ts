/**
 * lib/verification/site-generation.ts — generation queue, completion recording,
 * and the preview-notification guard for the web-activation pipeline.
 *
 * VERSION HISTORY
 * v1.2.0 · 2026-08-05 · Adds a separate Ready for Preview candidate query for explicitly reissued owner-review invitations, including previously preview-notified businesses.
 * v1.1.0 · 2026-07-29 · Replaces the business_claimed + null-URL queue check with
 *   the explicit awaiting_site_generation stage, renames the completion target to
 *   ready_for_preview, and adds getBusinessesReadyForPreviewNotification() so the
 *   cron job can find businesses still owed their preview email.
 * v1.0.0 · 2026-07-29 · Initial version: queue query and recordSiteGenerated(),
 *   deliberately excluding any attempt to invoke generation itself.
 */

import { and, asc, eq, isNotNull, isNull, notInArray, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, pipelineStages, stageTransitions, previewDeliveryMessages } from "@/lib/db/schema";
import { verifyGeneratedSiteUrl } from "@/lib/verification/site-generation-guards";

/**
 * The actual site-generation step is an agent-invoked skill (ep044_group),
 * not something this application can call as a function -- generating a
 * static site means running a Claude skill against the business's data and
 * images. This module deliberately does NOT attempt to trigger that; it
 * only surfaces the queue and records the outcome once generation has
 * actually happened, the same separation of concerns as a work queue and
 * its worker.
 *
 * Stage flow (see migrations/0016_site_generation_queue_stage.sql):
 *   business_claimed -> awaiting_site_generation -> ready_for_preview
 * awaiting_site_generation is set immediately on claim approval
 * (see claims-approval.ts) and is itself the queue signal -- no separate
 * null-check is needed once a business is in that stage.
 */

async function getStageId(key: string): Promise<number | null> {
  const [stage] = await db.select().from(pipelineStages).where(eq(pipelineStages.key, key)).limit(1);
  return stage?.id ?? null;
}

export type BusinessAwaitingGeneration = {
  id: string; businessRef: string; businessName: string; category: string; town: string | null;
  stageEnteredAt: Date | null;
};

/** Businesses queued for site generation -- the actual work a scheduled agent run should consume. */
export async function getBusinessesAwaitingSiteGeneration(): Promise<BusinessAwaitingGeneration[]> {
  const stageId = await getStageId("awaiting_site_generation");
  if (!stageId) return [];
  return db.select({
    id: businesses.id, businessRef: businesses.businessRef, businessName: businesses.businessName,
    category: businesses.category, town: businesses.town, stageEnteredAt: businesses.stageEnteredAt,
  }).from(businesses).where(eq(businesses.currentStageId, stageId)).orderBy(asc(businesses.stageEnteredAt));
}

/**
 * Records one verified deployment exactly once. This is intentionally not an
 * upsert: callers must use the explicitly named manual-review recovery action
 * if an already-recorded URL must be replaced.
 */
export async function recordSiteGenerated(input: {
  businessId: string; siteUrl: string; actorUserId: string;
}) {
  const verifiedUrl = await verifyGeneratedSiteUrl(input.siteUrl);
  const [awaitingStageId, readyStageId] = await Promise.all([
    getStageId("awaiting_site_generation"),
    getStageId("ready_for_preview"),
  ]);
  if (!awaitingStageId) throw new Error("The Awaiting Site Generation pipeline stage is unavailable.");
  if (!readyStageId) throw new Error("The Ready for Preview pipeline stage is unavailable.");

  return db.transaction(async (tx) => {
    // Locking prevents concurrent completion callers from both observing an
    // eligible row; the conditional update below is a second non-bypassable guard.
    const result = await tx.execute(sql`
      SELECT current_stage_id, generated_site_url
      FROM businesses
      WHERE id = ${input.businessId}
      FOR UPDATE
    `);
    const biz = result.rows[0] as {
      current_stage_id: number | null;
      generated_site_url: string | null;
    } | undefined;
    if (!biz) throw new Error("Business not found.");
    if (biz.current_stage_id !== awaitingStageId) {
      throw new Error("Business is not awaiting site generation; completion cannot be recorded.");
    }
    if (biz.generated_site_url !== null) {
      throw new Error("A generated site URL is already recorded; use recover_generated_site_after_manual_review.");
    }

    const now = new Date();
    const [updated] = await tx.update(businesses).set({
      generatedSiteUrl: verifiedUrl.href, websiteGeneratedAt: now,
      currentStageId: readyStageId, stageEnteredAt: now, lastUpdated: now,
    }).where(and(
      eq(businesses.id, input.businessId),
      eq(businesses.currentStageId, awaitingStageId),
      isNull(businesses.generatedSiteUrl),
    )).returning({ id: businesses.id });
    if (!updated) {
      throw new Error("Business completion changed concurrently; re-read the queue before retrying.");
    }

    await tx.insert(stageTransitions).values({
      businessId: input.businessId, fromStageId: awaitingStageId, toStageId: readyStageId,
      occurredAt: now, source: "automation", actorUserId: input.actorUserId,
      reason: "Verified generated site recorded by generation worker",
    });
  });
}

/**
 * Explicit, audited recovery for an already-recorded preview whose deployment
 * was manually reviewed and must be replaced. Normal completion never calls it.
 */
export async function recoverGeneratedSiteAfterManualReview(input: {
  businessId: string; siteUrl: string; actorUserId: string; recoveryReason: string;
}) {
  if (!input.recoveryReason.trim()) {
    throw new Error("A recoveryReason is required for generated-site replacement.");
  }
  const verifiedUrl = await verifyGeneratedSiteUrl(input.siteUrl);
  const readyStageId = await getStageId("ready_for_preview");
  if (!readyStageId) throw new Error("The Ready for Preview pipeline stage is unavailable.");

  return db.transaction(async (tx) => {
    const result = await tx.execute(sql`
      SELECT current_stage_id, generated_site_url
      FROM businesses
      WHERE id = ${input.businessId}
      FOR UPDATE
    `);
    const biz = result.rows[0] as {
      current_stage_id: number | null;
      generated_site_url: string | null;
    } | undefined;
    if (!biz) throw new Error("Business not found.");
    if (biz.current_stage_id !== readyStageId || biz.generated_site_url === null) {
      throw new Error("Only an already-recorded Ready for Preview site can use manual-review recovery.");
    }

    const now = new Date();
    const [updated] = await tx.update(businesses).set({
      generatedSiteUrl: verifiedUrl.href, websiteGeneratedAt: now, lastUpdated: now,
    }).where(and(
      eq(businesses.id, input.businessId),
      eq(businesses.currentStageId, readyStageId),
      eq(businesses.generatedSiteUrl, biz.generated_site_url),
    )).returning({ id: businesses.id });
    if (!updated) {
      throw new Error("Generated-site recovery changed concurrently; re-read the business before retrying.");
    }

    await tx.insert(stageTransitions).values({
      businessId: input.businessId, fromStageId: readyStageId, toStageId: readyStageId,
      occurredAt: now, source: "admin", actorUserId: input.actorUserId,
      reason: "Generated site replaced after manual review recovery",
      notes: input.recoveryReason.trim(),
    });
  });
}

export type BusinessReadyForPreviewNotification = {
  id: string; businessRef: string; businessName: string; email: string | null; generatedSiteUrl: string | null;
};

/**
 * Businesses at ready_for_preview that have never had a preview_ready
 * message prepared. Absence of a preview_delivery_messages row (any status)
 * is the "not yet notified" guard -- avoids re-notifying every watcher cycle
 * without needing a further pipeline stage just to mean "notification sent".
 */
export async function getBusinessesReadyForPreviewNotification(): Promise<BusinessReadyForPreviewNotification[]> {
  const stageId = await getStageId("ready_for_preview");
  if (!stageId) return [];
  // Only a successfully-sent preview excludes a business. Prepared/failed rows remain
  // visible to admins for a controlled retry after a policy/configuration issue is fixed.
  const alreadyNotified = await db.selectDistinct({ businessId: previewDeliveryMessages.businessId })
    .from(previewDeliveryMessages).where(and(
      eq(previewDeliveryMessages.messageType, "preview_ready"),
      eq(previewDeliveryMessages.status, "sent"),
    ));
  const excludeIds = alreadyNotified.map((row) => row.businessId);
  return db.select({
    id: businesses.id, businessRef: businesses.businessRef, businessName: businesses.businessName,
    email: businesses.email, generatedSiteUrl: businesses.generatedSiteUrl,
  }).from(businesses).where(and(
    eq(businesses.currentStageId, stageId),
    excludeIds.length ? notInArray(businesses.id, excludeIds) : undefined,
  )).orderBy(asc(businesses.stageEnteredAt));
}

/**
 * Candidate list for a deliberate, separately audited review invitation.
 * Unlike initial preview notification, a prior sent preview_ready message does
 * not exclude this list: the operator must explicitly select and confirm it.
 */
export async function getBusinessesReadyForOwnerReviewInvitation(): Promise<BusinessReadyForPreviewNotification[]> {
  const stageId = await getStageId("ready_for_preview");
  if (!stageId) return [];
  return db.select({
    id: businesses.id, businessRef: businesses.businessRef, businessName: businesses.businessName,
    email: businesses.email, generatedSiteUrl: businesses.generatedSiteUrl,
  }).from(businesses).where(and(
    eq(businesses.currentStageId, stageId),
    isNotNull(businesses.email),
    isNotNull(businesses.generatedSiteUrl),
  )).orderBy(asc(businesses.stageEnteredAt));
}
