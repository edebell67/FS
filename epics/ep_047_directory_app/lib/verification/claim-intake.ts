import { createHash } from "node:crypto";
import { and, eq, gt } from "drizzle-orm";
import { db } from "@/lib/db/client";
import { businesses, claimRequests, pipelineStages } from "@/lib/db/schema";
import { canRequestPublicClaim } from "./claim-eligibility";

const WINDOW_MS = 24 * 60 * 60 * 1000;
export async function createPublicClaimIntake(input: {
  businessRef: string; requesterName: string; relationship: string;
  email?: string; phone?: string; acknowledged: boolean; website?: string;
}) {
  if (input.website || !input.acknowledged || !input.requesterName.trim() ||
      (!input.email?.trim() && !input.phone?.trim())) return { accepted: false };
  const [business] = await db.select({
    id: businesses.id,
    currentStageId: businesses.currentStageId,
    stageKey: pipelineStages.key,
  }).from(businesses)
    .leftJoin(pipelineStages, eq(businesses.currentStageId, pipelineStages.id))
    .where(eq(businesses.businessRef, input.businessRef)).limit(1);
  if (!business || !canRequestPublicClaim(business.stageKey)) return { accepted: true };
  const contact = (input.email || input.phone || "").trim().toLowerCase();
  const fingerprint = createHash("sha256").update(`${business.id}:${contact}`).digest("hex");
  const [recent] = await db.select({ id: claimRequests.id }).from(claimRequests).where(and(
    eq(claimRequests.businessId, business.id), eq(claimRequests.contactFingerprint, fingerprint),
    gt(claimRequests.createdAt, new Date(Date.now() - WINDOW_MS)),
  )).limit(1);
  if (!recent) {
    await db.insert(claimRequests).values({
      businessId: business.id, status: "pending",
    requesterName: input.requesterName.trim(), relationship: input.relationship,
    contactEmail: input.email?.trim() || null, contactPhone: input.phone?.trim() || null,
    contactFingerprint: fingerprint,
    });
    await db.update(businesses).set({ status: "claims_pending", lastUpdated: new Date() }).where(eq(businesses.id, business.id));
  }
  return { accepted: true };
}
