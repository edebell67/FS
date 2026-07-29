// Public-directory-specific queries: homepage aggregates, category/town
// counts, a single business by slug, and its related/nearby businesses.
// Listing pages (category, town, search, A-Z) reuse listBusinesses from
// ./businesses.ts rather than duplicating filter/pagination logic — this
// file only adds what listBusinesses doesn't already do.

import { and, asc, desc, eq, ne, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, pipelineStages } from "@/lib/db/schema";
import { publicScopeWhere } from "./public-scope";

/**
 * Slugs for category/town URL segments. Source data (scraped, see
 * UK_Ltd_email_no_website_VERIFIED_410.csv) has category/town values that
 * are already lowercase words separated by spaces with no punctuation
 * ("appliance repairs", "birmingham") — so hyphen<->space is a safe,
 * reversible scheme for THIS dataset. It is not a general-purpose slugifier:
 * a category containing a literal hyphen would round-trip incorrectly. If
 * that ever happens, add a dedicated slug column instead of reversing this.
 */
export function toSlug(value: string): string {
  return value.trim().toLowerCase().replace(/\s+/g, "-");
}

export function fromSlug(slug: string): string {
  return slug.replace(/-/g, " ");
}

export interface CountedGroup {
  label: string;
  slug: string;
  count: number;
}

export async function getCategoryCounts(): Promise<CountedGroup[]> {
  const rows = await db
    .select({ category: businesses.category, count: sql<number>`count(*)::int` })
    .from(businesses)
    .where(publicScopeWhere())
    .groupBy(businesses.category)
    .orderBy(desc(sql`count(*)`));
  return rows.map((r) => ({ label: r.category, slug: toSlug(r.category), count: r.count }));
}

export async function getTownCounts(): Promise<CountedGroup[]> {
  const rows = await db
    .select({ town: businesses.town, count: sql<number>`count(*)::int` })
    .from(businesses)
    .where(and(publicScopeWhere(), sql`${businesses.town} IS NOT NULL`))
    .groupBy(businesses.town)
    .orderBy(desc(sql`count(*)`));
  return rows
    .filter((r): r is { town: string; count: number } => Boolean(r.town))
    .map((r) => ({ label: r.town, slug: toSlug(r.town), count: r.count }));
}

/** Which first letters of business_name actually have at least one business — drives the A-Z index. */
export async function getAvailableLetters(): Promise<string[]> {
    const rows = await db.execute<{ letter: string }>(
    sql`SELECT DISTINCT upper(left(business_name, 1)) AS letter FROM businesses b WHERE ${publicScopeWhere()} ORDER BY letter`
  );
  const result = rows as unknown as { rows: Array<{ letter: string }> };
  return result.rows.map((r) => r.letter);
}

export async function getNewestBusinesses(limit: number) {
  return db
    .select({
      id: businesses.id,
      slug: businesses.slug,
      businessName: businesses.businessName,
      category: businesses.category,
      town: businesses.town,
      importDate: businesses.importDate,
    })
    .from(businesses)
    .where(publicScopeWhere())
    .orderBy(desc(businesses.importDate))
    .limit(limit);
}

export async function getDirectorySummary() {
  const [totalRows, categories, towns] = await Promise.all([
    db.select({ total: sql<number>`count(*)::int` }).from(businesses),
    getCategoryCounts(),
    getTownCounts(),
  ]);
  return {
    total: totalRows[0]?.total ?? 0,
    categoryCount: categories.length,
    townCount: towns.length,
  };
}

export interface BusinessProfile {
  id: string;
  businessRef: string;
  slug: string;
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
  latitude: number | null;
  longitude: number | null;
  googleRating: number | null;
  reviewCount: number | null;
  description: string | null;
  stageLabel: string | null;
  importDate: Date;
}

export async function getBusinessBySlug(slug: string): Promise<BusinessProfile | null> {
  const [row] = await db
    .select({
      id: businesses.id,
      businessRef: businesses.businessRef,
      slug: businesses.slug,
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
      latitude: businesses.latitude,
      longitude: businesses.longitude,
      googleRating: businesses.googleRating,
      reviewCount: businesses.reviewCount,
      description: businesses.description,
      stageLabel: pipelineStages.label,
      importDate: businesses.importDate,
    })
    .from(businesses)
    .leftJoin(pipelineStages, eq(businesses.currentStageId, pipelineStages.id))
    .where(and(eq(businesses.slug, slug), publicScopeWhere()))
    .limit(1);
  return row ?? null;
}

/** Same shape as getBusinessBySlug, keyed by the permanent business_ref instead — what the admin console uses. */
export async function getBusinessByRef(businessRef: string): Promise<BusinessProfile | null> {
  const [row] = await db
    .select({
      id: businesses.id,
      businessRef: businesses.businessRef,
      slug: businesses.slug,
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
      latitude: businesses.latitude,
      longitude: businesses.longitude,
      googleRating: businesses.googleRating,
      reviewCount: businesses.reviewCount,
      description: businesses.description,
      stageLabel: pipelineStages.label,
      importDate: businesses.importDate,
    })
    .from(businesses)
    .leftJoin(pipelineStages, eq(businesses.currentStageId, pipelineStages.id))
    .where(and(eq(businesses.businessRef, businessRef), publicScopeWhere()))
    .limit(1);
  return row ?? null;
}

export interface RelatedBusiness {
  slug: string;
  businessName: string;
  category: string;
  town: string | null;
}

export async function getRelatedBusinesses(
  category: string,
  excludeId: string,
  limit: number
): Promise<RelatedBusiness[]> {
  return db
    .select({
      slug: businesses.slug,
      businessName: businesses.businessName,
      category: businesses.category,
      town: businesses.town,
    })
    .from(businesses)
    .where(and(eq(businesses.category, category), ne(businesses.id, excludeId), publicScopeWhere()))
    .orderBy(asc(businesses.businessName))
    .limit(limit);
}

export async function getNearbyBusinesses(
  town: string,
  excludeId: string,
  limit: number
): Promise<RelatedBusiness[]> {
  return db
    .select({
      slug: businesses.slug,
      businessName: businesses.businessName,
      category: businesses.category,
      town: businesses.town,
    })
    .from(businesses)
    .where(and(eq(businesses.town, town), ne(businesses.id, excludeId), publicScopeWhere()))
    .orderBy(asc(businesses.businessName))
    .limit(limit);
}
