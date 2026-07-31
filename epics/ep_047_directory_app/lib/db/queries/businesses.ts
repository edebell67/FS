// Query layer for the businesses list/search admin page. Kept separate from
// the importer's repository (lib/import/repository.ts) since that's write
// path for import specifically — this is general-purpose read access, the
// first piece of what will eventually be the public directory's query layer
// too (Phase 3 reuses this, doesn't reinvent it).

import { and, asc, desc, eq, ilike, or, sql, type SQL } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, pipelineStages, stageTransitions } from "@/lib/db/schema";
import { publicScopeWhere } from "@/ep047_visibility_news/lib/public-scope";

export const PAGE_SIZE = 25;

export interface BusinessListFilters {
  q?: string;
  category?: string;
  town?: string;
  status?: string;
  /** Filters to businesses whose current pipeline stage has this key, e.g. "imported". */
  stageKey?: string;
  /** Filters to businesses whose current stage rolls up into this Kanban board column, e.g. "Validated" (3 stages). */
  boardColumn?: string;
  /** First-letter filter for the A-Z index — matches businessName starting with this letter. */
  startsWith?: string;
  page: number;
  /** "newest" (admin default) or "name" (public listing default). */
  sort?: "newest" | "name";
}

export interface BusinessListRow {
  id: string;
  businessRef: string;
  businessName: string;
  slug: string;
  category: string;
  town: string | null;
  county: string | null;
  phone: string | null;
  email: string | null;
  status: string;
  stageLabel: string | null;
  importDate: Date;
}

export interface BusinessListResult {
  rows: BusinessListRow[];
  total: number;
  page: number;
  pageCount: number;
}

/** Clamps a raw page param to a sane positive integer — never trust query strings directly. */
export function parsePage(raw: string | string[] | undefined): number {
  const value = Array.isArray(raw) ? raw[0] : raw;
  const parsed = value ? Number.parseInt(value, 10) : 1;
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 1;
}

function buildWhere(filters: BusinessListFilters): SQL | undefined {
  const conditions: SQL[] = [];
  conditions.push(publicScopeWhere());

  if (filters.q) {
    const pattern = `%${filters.q}%`;
    conditions.push(
      or(
        ilike(businesses.businessName, pattern),
        ilike(businesses.tradingName, pattern),
        ilike(businesses.category, pattern),
        ilike(businesses.subCategory, pattern),
        ilike(businesses.town, pattern),
        ilike(businesses.county, pattern),
        ilike(businesses.email, pattern),
        ilike(businesses.phone, pattern),
        ilike(businesses.mobile, pattern),
        ilike(businesses.businessRef, pattern),
        ilike(businesses.postcode, pattern)
      )!
    );
  }
  if (filters.category) conditions.push(eq(businesses.category, filters.category));
  if (filters.town) conditions.push(eq(businesses.town, filters.town));
  if (filters.status) conditions.push(eq(businesses.status, filters.status));
  if (filters.startsWith) conditions.push(ilike(businesses.businessName, `${filters.startsWith}%`));
  // Subquery rather than a join, so this filter works whether or not the
  // caller's own query joins pipeline_stages (the count query doesn't).
  if (filters.stageKey) {
    conditions.push(
      sql`${businesses.currentStageId} = (SELECT id FROM pipeline_stages WHERE key = ${filters.stageKey})`
    );
  }
  if (filters.boardColumn) {
    conditions.push(
      sql`${businesses.currentStageId} IN (SELECT id FROM pipeline_stages WHERE board_column = ${filters.boardColumn})`
    );
  }

  return conditions.length > 0 ? and(...conditions) : undefined;
}

export async function listBusinesses(filters: BusinessListFilters): Promise<BusinessListResult> {
  const where = buildWhere(filters);
  const offset = (filters.page - 1) * PAGE_SIZE;
  const orderBy =
    filters.sort === "name"
      ? [asc(businesses.businessName)]
      : [desc(businesses.importDate), asc(businesses.businessName)];

  const [rows, countRows] = await Promise.all([
    db
      .select({
        id: businesses.id,
        businessRef: businesses.businessRef,
        businessName: businesses.businessName,
        slug: businesses.slug,
        category: businesses.category,
        town: businesses.town,
        county: businesses.county,
        phone: businesses.phone,
        email: businesses.email,
        status: businesses.status,
        stageLabel: pipelineStages.label,
        importDate: businesses.importDate,
      })
      .from(businesses)
      .leftJoin(pipelineStages, eq(businesses.currentStageId, pipelineStages.id))
      .where(where)
      .orderBy(...orderBy)
      .limit(PAGE_SIZE)
      .offset(offset),
    db.select({ count: sql<number>`count(*)::int` }).from(businesses).where(where),
  ]);
  const count = countRows[0]?.count ?? 0;

  return {
    rows,
    total: count,
    page: filters.page,
    pageCount: Math.max(1, Math.ceil(count / PAGE_SIZE)),
  };
}

export async function listDistinctCategories(): Promise<string[]> {
  const rows = await db
    .selectDistinct({ category: businesses.category })
    .from(businesses)
    .where(publicScopeWhere())
    .orderBy(asc(businesses.category));
  return rows.map((r) => r.category);
}

export async function listDistinctTowns(): Promise<string[]> {
  const rows = await db
    .selectDistinct({ town: businesses.town })
    .from(businesses)
    .where(and(publicScopeWhere(), sql`${businesses.town} IS NOT NULL`))
    .orderBy(asc(businesses.town));
  return rows.map((r) => r.town).filter((t): t is string => Boolean(t));
}

// --- Admin edit form -------------------------------------------------------
// Deliberately unrestricted by publicScopeWhere() -- an admin editing a
// business needs to see and change it regardless of current public
// visibility, unlike every read above this line which backs public-facing
// pages.

export interface BusinessEditableFields {
  businessName: string;
  tradingName: string | null;
  category: string;
  subCategory: string | null;
  email: string | null;
  phone: string | null;
  mobile: string | null;
  website: string | null;
  facebook: string | null;
  instagram: string | null;
  linkedin: string | null;
  address: string | null;
  town: string | null;
  county: string | null;
  postcode: string | null;
  description: string | null;
  chatWidgetOptIn: boolean;
}

export type BusinessForEdit = BusinessEditableFields & { id: string; businessRef: string; currentStageId: number | null };

export async function getBusinessForEdit(businessRef: string): Promise<BusinessForEdit | null> {
  const [row] = await db
    .select({
      id: businesses.id,
      businessRef: businesses.businessRef,
      currentStageId: businesses.currentStageId,
      businessName: businesses.businessName,
      tradingName: businesses.tradingName,
      category: businesses.category,
      subCategory: businesses.subCategory,
      email: businesses.email,
      phone: businesses.phone,
      mobile: businesses.mobile,
      website: businesses.website,
      facebook: businesses.facebook,
      instagram: businesses.instagram,
      linkedin: businesses.linkedin,
      address: businesses.address,
      town: businesses.town,
      county: businesses.county,
      postcode: businesses.postcode,
      description: businesses.description,
      chatWidgetOptIn: businesses.chatWidgetOptIn,
    })
    .from(businesses)
    .where(eq(businesses.businessRef, businessRef))
    .limit(1);
  return row ?? null;
}

/**
 * Updates any subset of a business's editable fields. Not a stage change --
 * fromStageId/toStageId are both the business's current stage, so the edit
 * shows up in its timeline (reusing stage_transitions rather than a new audit
 * table) without implying any pipeline movement happened.
 */
export async function updateBusinessDetails(
  businessId: string,
  fields: Partial<BusinessEditableFields>,
  actorUserId: string
): Promise<{ ok: true } | { ok: false; error: string }> {
  const [business] = await db.select().from(businesses).where(eq(businesses.id, businessId)).limit(1);
  if (!business) return { ok: false, error: "Business not found." };
  const currentStageId = business.currentStageId;
  if (!currentStageId) return { ok: false, error: "Business has no pipeline stage set." };

  // Only the fields whose value actually differs from what's stored --
  // submitting the whole form every time shouldn't make every field show up
  // in the audit note when only one thing was actually edited.
  const changedFields = (Object.keys(fields) as (keyof BusinessEditableFields)[]).filter(
    (key) => fields[key] !== business[key]
  );
  if (changedFields.length === 0) return { ok: true };

  await db.transaction(async (tx) => {
    const now = new Date();
    await tx.update(businesses).set({ ...fields, lastUpdated: now }).where(eq(businesses.id, businessId));
    await tx.insert(stageTransitions).values({
      businessId,
      fromStageId: currentStageId,
      toStageId: currentStageId,
      occurredAt: now,
      source: "admin",
      reason: "Edited business details",
      notes: `Changed: ${changedFields.join(", ")}`,
      actorUserId,
    });
  });
  return { ok: true };
}
