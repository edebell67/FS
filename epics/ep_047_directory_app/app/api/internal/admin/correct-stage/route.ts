/** Temporary one-off endpoint to correct a business's pipeline stage after the validation regression. */

import { NextResponse } from "next/server";
import { requireInternalApiKey } from "@/lib/auth/require-internal-api";
import { db } from "@/lib/db/client";
import { businesses, pipelineStages, stageTransitions } from "@/lib/db/schema";
import { eq, sql } from "drizzle-orm";

export async function POST(request: Request) {
  const auth = await requireInternalApiKey(request);
  if (auth) return auth;

  let body: { businessRef?: string; targetStageKey?: string; reason?: string; slug?: string } = {};
  try { body = await request.json(); } catch {}
  if ((!body.businessRef && !body.slug) || !body.targetStageKey) {
    return NextResponse.json({ error: "businessRef (or slug) and targetStageKey are required." }, { status: 400 });
  }

  try {
    const whereClause = body.businessRef
      ? eq(businesses.businessRef, body.businessRef)
      : eq(businesses.slug, body.slug!);
    const [business] = await db.select({
      id: businesses.id, currentStageId: businesses.currentStageId, generatedSiteUrl: businesses.generatedSiteUrl,
    }).from(businesses).where(whereClause).limit(1);
    if (!business) return NextResponse.json({ error: "Business not found." }, { status: 404 });

    const [targetStage] = await db.select().from(pipelineStages).where(eq(pipelineStages.key, body.targetStageKey)).limit(1);
    if (!targetStage) return NextResponse.json({ error: `Stage '${body.targetStageKey}' not found.` }, { status: 404 });

    const now = new Date();
    await db.update(businesses).set({
      currentStageId: targetStage.id,
      stageEnteredAt: now,
      lastUpdated: now,
    }).where(eq(businesses.id, business.id));

    await db.insert(stageTransitions).values({
      businessId: business.id,
      fromStageId: business.currentStageId,
      toStageId: targetStage.id,
      occurredAt: now,
      source: "automation",
      reason: body.reason ?? "admin_correction",
    });

    return NextResponse.json({
      corrected: true,
      businessRef: body.businessRef,
      fromStageId: business.currentStageId,
      toStage: body.targetStageKey,
    });
  } catch (error) {
    return NextResponse.json({
      error: error instanceof Error ? error.message : "Unable to correct stage.",
    }, { status: 500 });
  }
}