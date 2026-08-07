/**
 * lib/owner-review/repository.ts — Validates and persists one-time capability-scoped owner feedback.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-08-07 · Adds listOwnerReviewSubmissions() and
 *   getOwnerReviewSubmissionDetail() — read-only admin queries. Until now
 *   nothing anywhere read ownerReviewSubmissions/ownerReviewPageResponses
 *   after submitOwnerReview() wrote them; the data existed but no admin could
 *   see it (gap `corrections` on EP047_end_to_end_workflow_gap_register.html).
 *   Deliberately read-only: an apply/reject decision path needs a new column
 *   (e.g. reviewedAt/reviewedByUserId) which is a schema migration, and no
 *   local Postgres was available this session to safely generate and verify
 *   one against — see the task file for that explicit gap.
 * v1.0.0 · 2026-08-05 · Initial durable no-mail owner review repository.
 */
import { and, desc, eq, gt, isNull, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, ownerReviewLinks, ownerReviewPageResponses, ownerReviewSubmissions } from "@/lib/db/schema";
import { generateVerificationToken, hashVerificationToken, isValidRawToken } from "@/lib/verification/tokens";

export type OwnerReviewInput = { decision: "accept" | "change" | "decline"; pages: Array<{ pageKey: string; noActionRequired: boolean; selections: string[]; anythingElse: string; pageOpenDateTime?: string }> };
const valid = (input: OwnerReviewInput) => ["accept", "change", "decline"].includes(input.decision) && input.pages.length <= 30 && input.pages.every(p => /^[a-z0-9_-]{1,80}$/i.test(p.pageKey) && p.anythingElse.length <= 4000 && p.selections.length <= 20 && p.selections.every(s => s.length <= 200));

export async function createOwnerReviewLink({ businessId, actorUserId, expiryDays = 5 }: { businessId: string; actorUserId: string; expiryDays?: number }) {
  if (!Number.isInteger(expiryDays) || expiryDays < 1 || expiryDays > 14) throw new Error("Owner review expiry must be between 1 and 14 days.");
  const token = generateVerificationToken();
  const expiresAt = new Date(Date.now() + expiryDays * 86_400_000);
  await db.insert(ownerReviewLinks).values({ businessId, tokenHash: hashVerificationToken(token), expiresAt, createdByUserId: actorUserId });
  return { token, expiresAt };
}

export async function getOwnerReviewByRawToken(token: string) {
  if (!isValidRawToken(token)) return null;
  const hash = hashVerificationToken(token);
  const [row] = await db.select({ linkId: ownerReviewLinks.id, businessName: businesses.businessName }).from(ownerReviewLinks).innerJoin(businesses, eq(ownerReviewLinks.businessId, businesses.id)).where(and(eq(ownerReviewLinks.tokenHash, hash), isNull(ownerReviewLinks.revokedAt), isNull(ownerReviewLinks.submittedAt), gt(ownerReviewLinks.expiresAt, new Date()))).limit(1);
  if (row) await db.update(ownerReviewLinks).set({ openedAt: new Date() }).where(and(eq(ownerReviewLinks.id, row.linkId), isNull(ownerReviewLinks.openedAt)));
  return row ?? null;
}
export async function submitOwnerReview(token: string, input: OwnerReviewInput) {
  if (!isValidRawToken(token) || !valid(input)) return null;
  const tokenHash = hashVerificationToken(token);
  return db.transaction(async tx => {
    const locked = await tx.execute(sql`SELECT id, business_id FROM owner_review_links WHERE token_hash=${tokenHash} AND revoked_at IS NULL AND submitted_at IS NULL AND expires_at > now() FOR UPDATE`);
    const link = locked.rows[0] as { id: string; business_id: string } | undefined;
    if (!link) return null;
    const now = new Date();
    const [submission] = await tx.insert(ownerReviewSubmissions).values({ linkId: link.id, businessId: link.business_id, decision: input.decision, submittedAt: now }).returning();
    if (!submission) throw new Error("Unable to save owner review.");
    if (input.pages.length) await tx.insert(ownerReviewPageResponses).values(input.pages.map(p => ({ submissionId: submission.id, pageKey: p.pageKey, noActionRequired: p.noActionRequired, selections: p.noActionRequired ? [] : p.selections, anythingElse: p.anythingElse, pageOpenDateTime: p.pageOpenDateTime ? new Date(p.pageOpenDateTime) : null })));
    await tx.update(ownerReviewLinks).set({ submittedAt: now }).where(eq(ownerReviewLinks.id, link.id));
    return { submissionId: submission.id };
  });
}

export type OwnerReviewSubmissionSummary = {
  id: string; businessId: string; businessName: string; businessRef: string;
  decision: string; submittedAt: Date; pageCount: number;
};

// Read-only, most recent first. No apply/reject state exists yet -- see the
// v1.1.0 version-history note above for why that is not built here.
export async function listOwnerReviewSubmissions(): Promise<OwnerReviewSubmissionSummary[]> {
  const rows = await db
    .select({
      id: ownerReviewSubmissions.id,
      businessId: ownerReviewSubmissions.businessId,
      businessName: businesses.businessName,
      businessRef: businesses.businessRef,
      decision: ownerReviewSubmissions.decision,
      submittedAt: ownerReviewSubmissions.submittedAt,
      pageCount: sql<number>`count(${ownerReviewPageResponses.id})::int`,
    })
    .from(ownerReviewSubmissions)
    .innerJoin(businesses, eq(ownerReviewSubmissions.businessId, businesses.id))
    .leftJoin(ownerReviewPageResponses, eq(ownerReviewPageResponses.submissionId, ownerReviewSubmissions.id))
    .groupBy(ownerReviewSubmissions.id, businesses.businessName, businesses.businessRef)
    .orderBy(desc(ownerReviewSubmissions.submittedAt));
  return rows;
}

export type OwnerReviewPageResponseDetail = {
  pageKey: string; noActionRequired: boolean; selections: string[];
  anythingElse: string; pageOpenDateTime: Date | null;
};

export async function getOwnerReviewSubmissionDetail(submissionId: string): Promise<{
  id: string; businessId: string; businessName: string; decision: string;
  submittedAt: Date; pages: OwnerReviewPageResponseDetail[];
} | null> {
  const [submission] = await db
    .select({
      id: ownerReviewSubmissions.id, businessId: ownerReviewSubmissions.businessId,
      businessName: businesses.businessName, decision: ownerReviewSubmissions.decision,
      submittedAt: ownerReviewSubmissions.submittedAt,
    })
    .from(ownerReviewSubmissions)
    .innerJoin(businesses, eq(ownerReviewSubmissions.businessId, businesses.id))
    .where(eq(ownerReviewSubmissions.id, submissionId))
    .limit(1);
  if (!submission) return null;

  const pages = await db
    .select({
      pageKey: ownerReviewPageResponses.pageKey,
      noActionRequired: ownerReviewPageResponses.noActionRequired,
      selections: ownerReviewPageResponses.selections,
      anythingElse: ownerReviewPageResponses.anythingElse,
      pageOpenDateTime: ownerReviewPageResponses.pageOpenDateTime,
    })
    .from(ownerReviewPageResponses)
    .where(eq(ownerReviewPageResponses.submissionId, submissionId));

  return { ...submission, pages: pages as OwnerReviewPageResponseDetail[] };
}
