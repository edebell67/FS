import { and, desc, eq, inArray, isNull, sql } from "drizzle-orm";
import { createHash, randomBytes } from "node:crypto";
import { db } from "@/lib/db/client";
import {
  businesses, fieldValidationOutcomes, pipelineStages, stageTransitions, validationPolicy,
  verificationBatchItems, verificationBatches, verificationDeliveries, verificationDeliveryEvents, verificationLinks,
} from "@/lib/db/schema";
import { VERIFICATION_TEMPLATE_VERSION } from "./email-template";
import { getDeliveryPolicy, sendPreparedDelivery } from "./delivery";
import { generateVerificationToken, hashVerificationToken, normalizeExpiryDays } from "./tokens";
import { verificationCapabilityUrl } from "./urls";

const MAX_BATCH_SIZE = 250;

export function normalizeBusinessIds(input: unknown): string[] {
  if (!Array.isArray(input)) throw new Error("businessIds must be an array.");
  const ids = [...new Set(input.filter((id): id is string =>
    typeof id === "string" && /^[0-9a-f]{8}-[0-9a-f-]{27,}$/i.test(id)))];
  if (ids.length === 0) throw new Error("Select at least one eligible business.");
  if (ids.length > MAX_BATCH_SIZE) throw new Error(`A batch may contain at most ${MAX_BATCH_SIZE} businesses.`);
  if (ids.length !== input.length) throw new Error("The selection contains invalid or duplicate businesses.");
  return ids;
}

export async function getEligibleVerificationBusinesses() {
  return db.select({
    id: businesses.id, businessRef: businesses.businessRef, businessName: businesses.businessName,
    email: businesses.email, town: businesses.town, validationStatus: businesses.validationStatus,
  }).from(businesses)
    .where(and(
      inArray(businesses.validationStatus, ["validated", "partially_validated"]),
      eq(businesses.status, "active"),
      sql`NOT EXISTS (
        SELECT 1 FROM verification_deliveries sent_delivery
        INNER JOIN verification_links sent_link ON sent_link.id = sent_delivery.verification_link_id
        WHERE sent_link.business_id = ${businesses.id}
          AND sent_delivery.sent_at IS NOT NULL
      )`,
    ))
    .orderBy(businesses.businessName);
}

export async function prepareVerificationBatch(
  rawIds: unknown, actorUserId: string, rawExpiry: unknown, requestPartial = false,
) {
  const businessIds = normalizeBusinessIds(rawIds);
  const expiresInDays = normalizeExpiryDays(rawExpiry);
  const expiresAt = new Date(Date.now() + expiresInDays * 86_400_000);
  const policy = getDeliveryPolicy();

  return db.transaction(async (tx) => {
    const locked = await tx.execute(sql`
      SELECT b.id, b.business_ref, b.business_name, b.email, b.current_stage_id,
             b.validation_status, b.last_validation_run_id
      FROM businesses b
      WHERE b.id IN (${sql.join(businessIds.map((id) => sql`${id}::uuid`), sql`, `)})
        AND b.status = 'active'
        AND b.validation_status IN ('validated', 'partially_validated')
      ORDER BY b.id FOR UPDATE OF b`);
    if (locked.rows.length !== businessIds.length) {
      throw new Error("Every selected business must still be active and validation-eligible.");
    }

    const rows = locked.rows as Array<{
      id: string; business_ref: string; business_name: string; email: string | null;
      current_stage_id: number | null; validation_status: string; last_validation_run_id: string | null;
    }>;
    const [storedPolicy] = await tx.select().from(validationPolicy).where(eq(validationPolicy.id, 1)).limit(1);
    const partialRows = rows.filter((row) => row.validation_status === "partially_validated");
    if (partialRows.length && (!storedPolicy?.allowPartialVerification || !requestPartial)) {
      throw new Error("Partially validated businesses require the protected partial-verification policy and explicit batch confirmation.");
    }
    const readyCount = rows.filter((row) => Boolean(row.email?.trim())).length;
    const batchStatus = readyCount === rows.length ? "ready" : readyCount === 0 ? "prepared" : "partially_ready";
    const [batch] = await tx.insert(verificationBatches).values({
      status: batchStatus, expiresInDays, totalCount: rows.length, readyCount, createdByUserId: actorUserId,
    }).returning();
    if (!batch) throw new Error("Unable to create verification batch.");

    const [pendingStage] = await tx.select().from(pipelineStages)
      .where(eq(pipelineStages.key, "verification_email_pending")).limit(1);
    if (!pendingStage) throw new Error("Verification pending pipeline stage is not configured.");

    const prepared = [];
    for (const row of rows) {
      const rawToken = generateVerificationToken();
      const outstanding = row.last_validation_run_id ? await tx.select({
        fieldName: fieldValidationOutcomes.fieldName,
      }).from(fieldValidationOutcomes).where(and(
        eq(fieldValidationOutcomes.runId, row.last_validation_run_id),
        eq(fieldValidationOutcomes.passed, false),
      )) : [];
      const outstandingFields = [...new Set(outstanding.map((item) => item.fieldName))];
      await tx.update(verificationLinks).set({ revokedAt: new Date() }).where(and(
        eq(verificationLinks.businessId, row.id),
        sql`${verificationLinks.revokedAt} IS NULL`,
        sql`${verificationLinks.submittedAt} IS NULL`,
        sql`${verificationLinks.expiresAt} > now()`,
      ));
      const [link] = await tx.insert(verificationLinks).values({
        businessId: row.id, tokenHash: hashVerificationToken(rawToken), expiresAt,
        expiresInDays, createdByUserId: actorUserId, validationStatusAtIssue: row.validation_status,
        validationRunId: row.last_validation_run_id, outstandingFields,
      }).returning();
      if (!link) throw new Error("Unable to create a verification link.");
      const recipient = row.email?.trim() || null;
      const readiness = recipient ? "ready" : "not_ready";
      const [item] = await tx.insert(verificationBatchItems).values({
        batchId: batch.id, businessId: row.id, verificationLinkId: link.id,
        recipientAddress: recipient, readiness,
        readinessReason: recipient ? null : "Business has no email recipient.",
      }).returning();
      if (!item) throw new Error("Unable to create batch item.");
      if (recipient) {
        await tx.insert(verificationDeliveries).values({
          verificationLinkId: link.id, batchItemId: item.id, channel: "email",
          recipientAddress: recipient, templateVersion: VERIFICATION_TEMPLATE_VERSION,
          actorUserId, status: "prepared", deliveryMode: policy.mode,
          trackingKeyHash: createHash("sha256").update(randomBytes(32)).digest("hex"),
        });
      }
      await tx.update(businesses).set({
        currentStageId: pendingStage.id, stageEnteredAt: new Date(), lastUpdated: new Date(),
      }).where(eq(businesses.id, row.id));
      await tx.insert(stageTransitions).values({
        businessId: row.id, fromStageId: row.current_stage_id, toStageId: pendingStage.id,
        source: "admin", actorUserId, reason: `Verification prepared in batch ${batch.id}`,
      });
      prepared.push({
        itemId: item.id, businessRef: row.business_ref, businessName: row.business_name,
        recipientChannel: "email", recipientAddress: recipient, readiness,
        readinessReason: item.readinessReason, status: item.status, expiresAt: expiresAt.toISOString(),
        url: verificationCapabilityUrl(rawToken),
      });
    }
    return { batchId: batch.id, status: batch.status, readyCount, totalCount: rows.length,
      delivery: policy, items: prepared };
  });
}

export async function getVerificationBatch(batchId: string) {
  const [batch] = await db.select().from(verificationBatches)
    .where(eq(verificationBatches.id, batchId)).limit(1);
  if (!batch) return null;
  const items = await db.select({
    id: verificationBatchItems.id, businessRef: businesses.businessRef,
    businessName: businesses.businessName, recipientChannel: verificationBatchItems.recipientChannel,
    recipientAddress: verificationBatchItems.recipientAddress, status: verificationBatchItems.status,
    readiness: verificationBatchItems.readiness, readinessReason: verificationBatchItems.readinessReason,
    expiresAt: verificationLinks.expiresAt, createdAt: verificationBatchItems.createdAt,
  }).from(verificationBatchItems)
    .innerJoin(businesses, eq(verificationBatchItems.businessId, businesses.id))
    .innerJoin(verificationLinks, eq(verificationBatchItems.verificationLinkId, verificationLinks.id))
    .where(eq(verificationBatchItems.batchId, batchId))
    .orderBy(businesses.businessName);
  return { ...batch, items, delivery: getDeliveryPolicy() };
}

export async function listVerificationBatches() {
  return db.select().from(verificationBatches).orderBy(desc(verificationBatches.createdAt)).limit(50);
}


type BatchSendCandidate = {
  itemId: string;
  businessId: string;
  businessName: string;
  businessSlug: string;
  businessEmail: string | null;
  oldLinkId: string;
  validationStatus: string;
  validationRunId: string | null;
  outstandingFields: string[];
  expiresInDays: number;
};

/**
 * Reissues capabilities only inside the explicit confirmed send operation.
 * The raw token and tracking key remain in memory only long enough for Gmail
 * handoff; hashes alone persist, so a previously prepared batch cannot leak a
 * usable capability from storage.
 */
async function reissueBatchDelivery(candidate: BatchSendCandidate, batchId: string, actorUserId: string) {
  const recipient = candidate.businessEmail?.trim().toLowerCase() || null;
  if (!recipient) return { skipped: true as const, reason: "Business has no current email recipient." };
  const policy = getDeliveryPolicy(recipient);
  if (!policy.canSend) return { skipped: true as const, reason: policy.reason };
  const rawToken = generateVerificationToken();
  const trackingKey = randomBytes(32).toString("base64url");
  const expiresAt = new Date(Date.now() + candidate.expiresInDays * 86_400_000);
  const prepared = await db.transaction(async (tx) => {
    const [lockedItem] = await tx.execute(sql`
      SELECT i.id, b.email
      FROM verification_batch_items i
      INNER JOIN businesses b ON b.id = i.business_id
      WHERE i.id = ${candidate.itemId}::uuid AND i.batch_id = ${batchId}::uuid
      FOR UPDATE OF i, b
    `).then((result) => result.rows as Array<{ id: string; email: string | null }>);
    if (!lockedItem || lockedItem.email?.trim().toLowerCase() !== recipient) {
      throw new Error("Prepared delivery recipient no longer matches the business email.");
    }
    await tx.update(verificationLinks).set({ revokedAt: new Date() }).where(and(
      eq(verificationLinks.id, candidate.oldLinkId), isNull(verificationLinks.submittedAt), isNull(verificationLinks.revokedAt),
    ));
    const revoked = await tx.update(verificationDeliveries).set({ status: "revoked", revokedAt: new Date() })
      .where(and(eq(verificationDeliveries.verificationLinkId, candidate.oldLinkId), eq(verificationDeliveries.status, "prepared")))
      .returning({ id: verificationDeliveries.id });
    for (const delivery of revoked) await tx.insert(verificationDeliveryEvents).values({
      deliveryId: delivery.id, eventType: "revoked", actorUserId, metadata: { reason: "Reissued by explicit batch send." },
    });
    const [link] = await tx.insert(verificationLinks).values({
      businessId: candidate.businessId, tokenHash: hashVerificationToken(rawToken), expiresAt,
      expiresInDays: candidate.expiresInDays, createdByUserId: actorUserId,
      validationStatusAtIssue: candidate.validationStatus, validationRunId: candidate.validationRunId,
      outstandingFields: candidate.outstandingFields,
    }).returning({ id: verificationLinks.id });
    if (!link) throw new Error("Unable to reissue a verification capability.");
    await tx.update(verificationBatchItems).set({ verificationLinkId: link.id, recipientAddress: recipient, readiness: "ready", readinessReason: null })
      .where(eq(verificationBatchItems.id, candidate.itemId));
    const [delivery] = await tx.insert(verificationDeliveries).values({
      verificationLinkId: link.id, batchItemId: candidate.itemId, channel: "email", recipientAddress: recipient,
      templateVersion: VERIFICATION_TEMPLATE_VERSION, actorUserId, status: "prepared", deliveryMode: policy.mode,
      trackingKeyHash: createHash("sha256").update(trackingKey).digest("hex"),
    }).returning({ id: verificationDeliveries.id });
    if (!delivery) throw new Error("Unable to prepare batch delivery.");
    await tx.insert(verificationDeliveryEvents).values({
      deliveryId: delivery.id, eventType: "prepared", actorUserId,
      metadata: { channel: "email", batchId, templateVersion: VERIFICATION_TEMPLATE_VERSION },
    });
    return { deliveryId: delivery.id, rawToken, trackingKey };
  });
  return { skipped: false as const, ...prepared };
}

export async function sendPreparedVerificationBatch(input: { batchId: string; actorUserId: string }) {
  const rows = await db.select({
    itemId: verificationBatchItems.id, businessId: businesses.id, businessName: businesses.businessName,
    businessSlug: businesses.slug, businessEmail: businesses.email, oldLinkId: verificationLinks.id,
    validationStatus: verificationLinks.validationStatusAtIssue, validationRunId: verificationLinks.validationRunId,
    outstandingFields: verificationLinks.outstandingFields, expiresInDays: verificationLinks.expiresInDays,
  }).from(verificationBatchItems)
    .innerJoin(verificationBatches, eq(verificationBatchItems.batchId, verificationBatches.id))
    .innerJoin(businesses, eq(verificationBatchItems.businessId, businesses.id))
    .innerJoin(verificationLinks, eq(verificationBatchItems.verificationLinkId, verificationLinks.id))
    .where(and(eq(verificationBatchItems.batchId, input.batchId), eq(verificationBatches.createdByUserId, input.actorUserId), eq(verificationBatchItems.status, "prepared")));
  if (!rows.length) throw new Error("No prepared verification emails are available in this batch.");
  const outcome = { sent: 0, failed: 0, skipped: 0, results: [] as Array<{ itemId: string; businessName: string; outcome: "sent" | "failed" | "skipped"; reason?: string }> };
  for (const row of rows) {
    const candidate: BatchSendCandidate = {
      ...row,
      validationStatus: row.validationStatus ?? "validated",
      outstandingFields: Array.isArray(row.outstandingFields) ? row.outstandingFields.map(String) : [],
    };
    try {
      const prepared = await reissueBatchDelivery(candidate, input.batchId, input.actorUserId);
      if (prepared.skipped) {
        outcome.skipped += 1; outcome.results.push({ itemId: row.itemId, businessName: row.businessName, outcome: "skipped", reason: prepared.reason });
        continue;
      }
      await sendPreparedDelivery({ ...prepared, actorUserId: input.actorUserId });
      await db.update(verificationBatchItems).set({ status: "sent" }).where(eq(verificationBatchItems.id, row.itemId));
      outcome.sent += 1; outcome.results.push({ itemId: row.itemId, businessName: row.businessName, outcome: "sent" });
    } catch (error) {
      const reason = error instanceof Error ? error.message : "Gmail API handoff failed.";
      outcome.failed += 1; outcome.results.push({ itemId: row.itemId, businessName: row.businessName, outcome: "failed", reason });
    }
  }
  const status = outcome.failed ? (outcome.sent ? "partially_sent" : "failed") : outcome.skipped ? "partially_sent" : "sent";
  await db.update(verificationBatches).set({ status }).where(eq(verificationBatches.id, input.batchId));
  return outcome;
}
