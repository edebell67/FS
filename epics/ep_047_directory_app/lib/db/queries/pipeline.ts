// Query + mutation layer for the admin pipeline board and dashboard. This is
// the "operational control centre" half of the brief — everything here
// reads or writes stage_transitions/businesses.currentStageId together,
// never one without the other (see PLAN.md §1's "state is a projection"
// rule).

import { and, asc, desc, eq, gte, sql } from "drizzle-orm";
import { alias } from "drizzle-orm/pg-core";
import { db } from "@/lib/db/client";
import { businesses, pipelineStages, stageTransitions } from "@/lib/db/schema";

export interface PipelineStage {
  id: number;
  key: string;
  label: string;
  sortOrder: number;
  boardColumn: string;
  isTerminal: boolean;
  slaHours: number | null;
}

export async function getPipelineStages(): Promise<PipelineStage[]> {
  return db.select().from(pipelineStages).orderBy(asc(pipelineStages.sortOrder));
}

export interface BoardCardBusiness {
  id: string;
  businessRef: string;
  businessName: string;
  category: string;
  town: string | null;
  stageEnteredAt: Date | null;
}

export interface BoardColumn {
  name: string;
  stages: PipelineStage[];
  count: number;
  movementToday: number;
  /** Average hours businesses currently in this column have been sitting there. Null if empty. */
  avgHoursInStage: number | null;
  blockedCount: number;
  /** Capped preview list — the board shows a sample, not every row (see admin businesses list for the full view). */
  businesses: BoardCardBusiness[];
}

const BOARD_ORDER = [
  "Discovered",
  "Imported",
  "Validated",
  "Verification",
  "Claimed",
  "Website",
  "Published",
  "Subscriber",
];

const CARD_PREVIEW_LIMIT = 8;

export async function getBoardColumns(): Promise<BoardColumn[]> {
  const stages = await getPipelineStages();
  const stagesByColumn = new Map<string, PipelineStage[]>();
  for (const stage of stages) {
    const list = stagesByColumn.get(stage.boardColumn) ?? [];
    list.push(stage);
    stagesByColumn.set(stage.boardColumn, list);
  }

  const columns: BoardColumn[] = [];

  for (const name of BOARD_ORDER) {
    const stagesInColumn = stagesByColumn.get(name) ?? [];
    const stageIds = stagesInColumn.map((s) => s.id);
    if (stageIds.length === 0) {
      columns.push({ name, stages: [], count: 0, movementToday: 0, avgHoursInStage: null, blockedCount: 0, businesses: [] });
      continue;
    }

    const stageIdList = sql.join(stageIds.map((id) => sql`${id}`), sql`, `);

    const [countRows, movementRows, avgRows, previewRows] = await Promise.all([
      db.select({ count: sql<number>`count(*)::int` }).from(businesses).where(sql`current_stage_id IN (${stageIdList})`),
      db
        .select({ movementToday: sql<number>`count(*)::int` })
        .from(stageTransitions)
        .where(and(sql`to_stage_id IN (${stageIdList})`, gte(stageTransitions.occurredAt, sql`current_date`))),
      db
        .select({ avgHours: sql<number | null>`avg(extract(epoch from (now() - stage_entered_at)) / 3600)` })
        .from(businesses)
        .where(sql`current_stage_id IN (${stageIdList})`),
      db
        .select({
          id: businesses.id,
          businessRef: businesses.businessRef,
          businessName: businesses.businessName,
          category: businesses.category,
          town: businesses.town,
          stageEnteredAt: businesses.stageEnteredAt,
        })
        .from(businesses)
        .where(sql`current_stage_id IN (${stageIdList})`)
        .orderBy(desc(businesses.stageEnteredAt))
        .limit(CARD_PREVIEW_LIMIT),
    ]);
    const count = countRows[0]?.count ?? 0;
    const movementToday = movementRows[0]?.movementToday ?? 0;
    const avgHours = avgRows[0]?.avgHours ?? null;

    // "Blocked" = sitting past this stage's SLA. Stages with no sla_hours (most of them,
    // currently) never count as blocked — that's a config gap, not a business one.
    const slaHours = stagesInColumn.find((s) => s.slaHours !== null)?.slaHours;
    const blockedCount =
      slaHours != null
        ? previewRows.filter((b) => {
            if (!b.stageEnteredAt) return false;
            const hours = (Date.now() - b.stageEnteredAt.getTime()) / 3_600_000;
            return hours > slaHours;
          }).length
        : 0;

    columns.push({
      name,
      stages: stagesInColumn,
      count,
      movementToday,
      avgHoursInStage: avgHours,
      blockedCount,
      businesses: previewRows,
    });
  }

  return columns;
}

export interface DashboardMetrics {
  totalBusinesses: number;
  categoryCount: number;
  townCount: number;
  importsToday: number;
  importsThisWeek: number;
  importsThisMonth: number;
  stalledCount: number;
  avgPipelineHours: number | null;
}

export async function getDashboardMetrics(): Promise<DashboardMetrics> {
  const [totalRows, categoryRows, townRows, todayRows, weekRows, monthRows, avgRows, stalledRows] =
    await Promise.all([
      db.select({ total: sql<number>`count(*)::int` }).from(businesses),
      db.select({ categoryCount: sql<number>`count(distinct category)::int` }).from(businesses),
      db.select({ townCount: sql<number>`count(distinct town)::int` }).from(businesses).where(sql`town IS NOT NULL`),
      db.select({ today: sql<number>`count(*)::int` }).from(businesses).where(sql`import_date >= current_date`),
      db
        .select({ week: sql<number>`count(*)::int` })
        .from(businesses)
        .where(sql`import_date >= current_date - interval '7 days'`),
      db
        .select({ month: sql<number>`count(*)::int` })
        .from(businesses)
        .where(sql`import_date >= current_date - interval '30 days'`),
      db
        .select({ avgHours: sql<number | null>`avg(extract(epoch from (now() - import_date)) / 3600)` })
        .from(businesses),
      // "Stalled" = sitting in a non-terminal stage past that stage's configured SLA.
      db
        .select({ stalled: sql<number>`count(*)::int` })
        .from(businesses)
        .innerJoin(pipelineStages, eq(businesses.currentStageId, pipelineStages.id))
        .where(
          and(
            eq(pipelineStages.isTerminal, false),
            sql`${pipelineStages.slaHours} IS NOT NULL`,
            sql`${businesses.stageEnteredAt} < now() - (${pipelineStages.slaHours} || ' hours')::interval`
          )
        ),
    ]);

  const total = totalRows[0]?.total ?? 0;
  const categoryCount = categoryRows[0]?.categoryCount ?? 0;
  const townCount = townRows[0]?.townCount ?? 0;
  const today = todayRows[0]?.today ?? 0;
  const week = weekRows[0]?.week ?? 0;
  const month = monthRows[0]?.month ?? 0;
  const avgHours = avgRows[0]?.avgHours ?? null;
  const stalled = stalledRows[0]?.stalled ?? 0;

  return {
    totalBusinesses: total,
    categoryCount,
    townCount,
    importsToday: today,
    importsThisWeek: week,
    importsThisMonth: month,
    stalledCount: stalled,
    avgPipelineHours: avgHours,
  };
}

export interface RecentActivityRow {
  businessId: string;
  businessRef: string;
  businessName: string;
  toStageLabel: string;
  occurredAt: Date;
  source: string;
}

export async function getRecentActivity(limit: number): Promise<RecentActivityRow[]> {
  return db
    .select({
      businessId: businesses.id,
      businessRef: businesses.businessRef,
      businessName: businesses.businessName,
      toStageLabel: pipelineStages.label,
      occurredAt: stageTransitions.occurredAt,
      source: stageTransitions.source,
    })
    .from(stageTransitions)
    .innerJoin(businesses, eq(stageTransitions.businessId, businesses.id))
    .innerJoin(pipelineStages, eq(stageTransitions.toStageId, pipelineStages.id))
    .orderBy(desc(stageTransitions.occurredAt))
    .limit(limit);
}

export interface TimelineEntry {
  id: number;
  fromStageLabel: string | null;
  toStageLabel: string;
  occurredAt: Date;
  source: string;
  reason: string | null;
  notes: string | null;
}

export async function getBusinessTimeline(businessId: string): Promise<TimelineEntry[]> {
  // Two joins to the same table need two aliases.
  const fromStages = alias(pipelineStages, "from_stages");
  const toStages = alias(pipelineStages, "to_stages");

  const rows = await db
    .select({
      id: stageTransitions.id,
      fromStageLabel: fromStages.label,
      toStageLabel: toStages.label,
      occurredAt: stageTransitions.occurredAt,
      source: stageTransitions.source,
      reason: stageTransitions.reason,
      notes: stageTransitions.notes,
    })
    .from(stageTransitions)
    .leftJoin(fromStages, eq(stageTransitions.fromStageId, fromStages.id))
    .innerJoin(toStages, eq(stageTransitions.toStageId, toStages.id))
    .where(eq(stageTransitions.businessId, businessId))
    .orderBy(asc(stageTransitions.occurredAt));

  return rows.map((r) => ({ ...r, toStageLabel: r.toStageLabel! }));
}

export interface MoveStageResult {
  ok: boolean;
  error?: string;
}

/**
 * The one place a business's stage ever changes. Writes the transition and
 * the businesses.currentStageId/stageEnteredAt projection in the same
 * transaction — this is the rule from PLAN.md §1, not optional.
 */
export async function moveBusinessToStage(
  businessId: string,
  toStageKey: string,
  source: "admin" | "automation" = "admin",
  reason?: string
): Promise<MoveStageResult> {
  const [toStage] = await db.select().from(pipelineStages).where(eq(pipelineStages.key, toStageKey)).limit(1);
  if (!toStage) return { ok: false, error: `Unknown stage "${toStageKey}".` };

  const [business] = await db.select().from(businesses).where(eq(businesses.id, businessId)).limit(1);
  if (!business) return { ok: false, error: "Business not found." };

  await db.transaction(async (tx) => {
    const now = new Date();
    await tx
      .update(businesses)
      .set({ currentStageId: toStage.id, stageEnteredAt: now, lastUpdated: now })
      .where(eq(businesses.id, businessId));

    await tx.insert(stageTransitions).values({
      businessId,
      fromStageId: business.currentStageId,
      toStageId: toStage.id,
      occurredAt: now,
      source,
      reason,
    });
  });

  return { ok: true };
}
