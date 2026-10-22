// lib/db/queries/crm.ts — EP043 CRM reporting queries (Lane 2: Batch
// Segmentation & Reporting). Read-only: nothing here writes to businesses,
// stage_transitions, or verification_* tables — those stay owned by the
// existing pipeline/verification code in lib/verification and
// lib/db/queries/pipeline.ts. "Batch" here is verification_batches, reused
// directly as the outreach-batch mechanism (confirmed scope decision, see
// workstream/200_inprogress/ep047-crm/20260810_042109_ep047_997_crm_lane2_batch_reporting.md).
//
// VERSION HISTORY
// v1.0.0 · 2026-08-10 · Initial version: listCrmBatches, getBatchPipelineDistribution,
//   getBatchResponseStats, getBatchBusinesses, getBusinessOutreachResponses.

import { desc, eq, inArray, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import {
  businesses, outreachResponses, pipelineStages, verificationBatchItems,
  verificationBatches, verificationDeliveries,
} from "@/lib/db/schema";

// A response is "positive" for response-rate reporting if the business
// showed active commercial interest, not just any reply (e.g. "wrong
// contact" or "unsubscribe" are responses but not positive ones).
const POSITIVE_CLASSIFICATIONS = ["positive", "interested", "listing_claim_interest", "website_interest"];

export interface CrmBatchSummary {
  id: string;
  status: string;
  totalCount: number;
  readyCount: number;
  createdAt: Date;
  sentCount: number;
  responseCount: number;
}

export async function listCrmBatches(): Promise<CrmBatchSummary[]> {
  const batches = await db.select().from(verificationBatches).orderBy(desc(verificationBatches.createdAt)).limit(100);
  if (batches.length === 0) return [];
  const batchIds = batches.map((b) => b.id);

  const [sentRows, responseRows] = await Promise.all([
    db
      .select({
        batchId: verificationBatchItems.batchId,
        sentCount: sql<number>`count(*) filter (where ${verificationDeliveries.sentAt} is not null)::int`,
      })
      .from(verificationBatchItems)
      .leftJoin(verificationDeliveries, eq(verificationDeliveries.batchItemId, verificationBatchItems.id))
      .where(inArray(verificationBatchItems.batchId, batchIds))
      .groupBy(verificationBatchItems.batchId),
    db
      .select({
        batchId: verificationBatchItems.batchId,
        responseCount: sql<number>`count(${outreachResponses.id})::int`,
      })
      .from(verificationBatchItems)
      .leftJoin(outreachResponses, eq(outreachResponses.batchItemId, verificationBatchItems.id))
      .where(inArray(verificationBatchItems.batchId, batchIds))
      .groupBy(verificationBatchItems.batchId),
  ]);

  const sentByBatch = new Map(sentRows.map((r) => [r.batchId, r.sentCount]));
  const responsesByBatch = new Map(responseRows.map((r) => [r.batchId, r.responseCount]));

  return batches.map((b) => ({
    id: b.id,
    status: b.status,
    totalCount: b.totalCount,
    readyCount: b.readyCount,
    createdAt: b.createdAt,
    sentCount: sentByBatch.get(b.id) ?? 0,
    responseCount: responsesByBatch.get(b.id) ?? 0,
  }));
}

export interface CrmBatchStageCount {
  stageKey: string;
  stageLabel: string;
  sortOrder: number;
  isTerminal: boolean;
  count: number;
}

export async function getBatchPipelineDistribution(batchId: string): Promise<CrmBatchStageCount[]> {
  return db
    .select({
      stageKey: pipelineStages.key,
      stageLabel: pipelineStages.label,
      sortOrder: pipelineStages.sortOrder,
      isTerminal: pipelineStages.isTerminal,
      count: sql<number>`count(distinct ${businesses.id})::int`,
    })
    .from(verificationBatchItems)
    .innerJoin(businesses, eq(verificationBatchItems.businessId, businesses.id))
    .innerJoin(pipelineStages, eq(businesses.currentStageId, pipelineStages.id))
    .where(eq(verificationBatchItems.batchId, batchId))
    .groupBy(pipelineStages.key, pipelineStages.label, pipelineStages.sortOrder, pipelineStages.isTerminal)
    .orderBy(pipelineStages.sortOrder);
}

export interface CrmClassificationCount {
  classification: string;
  count: number;
}

export interface CrmBatchResponseStats {
  sentCount: number;
  responseCount: number;
  responseRate: number | null;
  positiveCount: number;
  positiveRate: number | null;
  byClassification: CrmClassificationCount[];
}

export async function getBatchResponseStats(batchId: string): Promise<CrmBatchResponseStats> {
  const [[sentRow], classificationRows] = await Promise.all([
    db
      .select({
        sentCount: sql<number>`count(*) filter (where ${verificationDeliveries.sentAt} is not null)::int`,
      })
      .from(verificationBatchItems)
      .leftJoin(verificationDeliveries, eq(verificationDeliveries.batchItemId, verificationBatchItems.id))
      .where(eq(verificationBatchItems.batchId, batchId)),
    db
      .select({
        classification: outreachResponses.classification,
        count: sql<number>`count(*)::int`,
      })
      .from(outreachResponses)
      .innerJoin(verificationBatchItems, eq(outreachResponses.batchItemId, verificationBatchItems.id))
      .where(eq(verificationBatchItems.batchId, batchId))
      .groupBy(outreachResponses.classification),
  ]);

  const sentCount = sentRow?.sentCount ?? 0;
  const responseCount = classificationRows.reduce((sum, r) => sum + r.count, 0);
  const positiveCount = classificationRows
    .filter((r) => POSITIVE_CLASSIFICATIONS.includes(r.classification))
    .reduce((sum, r) => sum + r.count, 0);

  return {
    sentCount,
    responseCount,
    responseRate: sentCount > 0 ? (responseCount / sentCount) * 100 : null,
    positiveCount,
    positiveRate: responseCount > 0 ? (positiveCount / responseCount) * 100 : null,
    byClassification: classificationRows,
  };
}

export interface CrmBatchBusinessRow {
  id: string;
  businessRef: string;
  businessName: string;
  category: string;
  town: string | null;
  stageLabel: string | null;
  sentAt: Date | null;
  responded: boolean;
  lastResponseClassification: string | null;
}

export async function getBatchBusinesses(batchId: string): Promise<CrmBatchBusinessRow[]> {
  const [rows, responseRows] = await Promise.all([
    db
      .select({
        id: businesses.id,
        businessRef: businesses.businessRef,
        businessName: businesses.businessName,
        category: businesses.category,
        town: businesses.town,
        stageLabel: pipelineStages.label,
        sentAt: verificationDeliveries.sentAt,
      })
      .from(verificationBatchItems)
      .innerJoin(businesses, eq(verificationBatchItems.businessId, businesses.id))
      .leftJoin(pipelineStages, eq(businesses.currentStageId, pipelineStages.id))
      .leftJoin(verificationDeliveries, eq(verificationDeliveries.batchItemId, verificationBatchItems.id))
      .where(eq(verificationBatchItems.batchId, batchId))
      .orderBy(businesses.businessName),
    db
      .select({
        businessId: outreachResponses.businessId,
        classification: outreachResponses.classification,
        receivedAt: outreachResponses.receivedAt,
      })
      .from(outreachResponses)
      .innerJoin(verificationBatchItems, eq(outreachResponses.batchItemId, verificationBatchItems.id))
      .where(eq(verificationBatchItems.batchId, batchId))
      .orderBy(desc(outreachResponses.receivedAt)),
  ]);

  // First row per business after the DESC order above is the latest response.
  const latestResponseByBusiness = new Map<string, string>();
  for (const r of responseRows) {
    if (!latestResponseByBusiness.has(r.businessId)) latestResponseByBusiness.set(r.businessId, r.classification);
  }

  return rows.map((r) => ({
    ...r,
    responded: latestResponseByBusiness.has(r.id),
    lastResponseClassification: latestResponseByBusiness.get(r.id) ?? null,
  }));
}

export interface CrmBusinessResponseRow {
  id: string;
  classification: string;
  originalBody: string;
  channel: string;
  receivedAt: Date;
  notes: string | null;
}

export async function getBusinessOutreachResponses(businessId: string): Promise<CrmBusinessResponseRow[]> {
  return db
    .select({
      id: outreachResponses.id,
      classification: outreachResponses.classification,
      originalBody: outreachResponses.originalBody,
      channel: outreachResponses.channel,
      receivedAt: outreachResponses.receivedAt,
      notes: outreachResponses.notes,
    })
    .from(outreachResponses)
    .where(eq(outreachResponses.businessId, businessId))
    .orderBy(desc(outreachResponses.receivedAt));
}
