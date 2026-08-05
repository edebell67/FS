/**
 * lib/owner-review/repository.ts — Validates and persists one-time capability-scoped owner feedback.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-05 · Initial durable no-mail owner review repository.
 */
import { and, eq, gt, isNull, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, ownerReviewLinks, ownerReviewPageResponses, ownerReviewSubmissions } from "@/lib/db/schema";
import { hashVerificationToken, isValidRawToken } from "@/lib/verification/tokens";

export type OwnerReviewInput = { decision: "accept" | "change" | "decline"; pages: Array<{ pageKey: string; noActionRequired: boolean; selections: string[]; anythingElse: string; pageOpenDateTime?: string }> };
const valid = (input: OwnerReviewInput) => ["accept", "change", "decline"].includes(input.decision) && input.pages.length <= 30 && input.pages.every(p => /^[a-z0-9_-]{1,80}$/i.test(p.pageKey) && p.anythingElse.length <= 4000 && p.selections.length <= 20 && p.selections.every(s => s.length <= 200));

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
