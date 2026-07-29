// Query layer for the businesses list/search admin page. Kept separate from
// the importer's repository (lib/import/repository.ts) since that's write
// path for import specifically — this is general-purpose read access, the
// first piece of what will eventually be the public directory's query layer
// too (Phase 3 reuses this, doesn't reinvent it).

import { and, asc, desc, eq, ilike, or, sql, type SQL } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, pipelineStages } from "@/lib/db/schema";
import { publicScopeWhere } from "./public-scope";

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
    .orderBy(asc(businesses.category));
  return rows.map((r) => r.category);
}

export async function listDistinctTowns(): Promise<string[]> {
  const rows = await db
    .selectDistinct({ town: businesses.town })
    .from(businesses)
    .where(sql`${businesses.town} IS NOT NULL`)
    .orderBy(asc(businesses.town));
  return rows.map((r) => r.town).filter((t): t is string => Boolean(t));
}
