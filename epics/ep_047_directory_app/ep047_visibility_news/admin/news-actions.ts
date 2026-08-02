"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db/client";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { sql } from "drizzle-orm";
import { assessNewsDateEvidence, chooseDuplicateSaveAction } from "./news-evidence";

function value(data: FormData, key: string) {
  return String(data.get(key) ?? "").trim();
}

export async function saveArticle(data: FormData) {
  await requireAdminUserForPage("/directoryadmin/news");
  const slug = value(data, "slug") || value(data, "headline").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const eventIdentity = value(data, "eventIdentity");
  const evidence = assessNewsDateEvidence({
    originalEventDate: value(data, "originalEventDate"),
    sourcePublishedAt: value(data, "sourcePublishedAt"),
    dateProvenanceNote: value(data, "dateProvenanceNote"),
    dateConfidence: value(data, "dateConfidence"),
    dateSelectionRationale: value(data, "dateSelectionRationale"),
    selectedDateKind: value(data, "selectedDateKind"),
  });
  const matching = eventIdentity
    ? await db.execute(sql`SELECT status FROM news_articles WHERE event_identity = ${eventIdentity} AND slug <> ${slug} ORDER BY (status = 'published') DESC LIMIT 1`)
    : null;
  const duplicate = chooseDuplicateSaveAction({ matchingStatus: (matching as any)?.rows?.[0]?.status ?? null });
  const status = !evidence.readyForPublish || duplicate.duplicateState === "review_required" ? "review_required" : "draft";

  const saved = await db.execute(sql`
    INSERT INTO news_articles (
      slug, headline, town, source_name, source_url, verified_update, local_reading, business_voices,
      status, source_published_at, original_event_date, effective_story_date, effective_date_kind,
      date_provenance, event_identity, duplicate_state, duplicate_reason
    ) VALUES (
      ${slug}, ${value(data, "headline")}, ${value(data, "town")}, ${value(data, "sourceName")},
      ${value(data, "sourceUrl")}, ${value(data, "verifiedUpdate")}, ${value(data, "localReading")}, NULL,
      ${status}, ${evidence.sourcePublishedDate ? `${evidence.sourcePublishedDate}T00:00:00.000Z` : null},
      ${evidence.originalEventDate}, ${evidence.effectiveStoryDate}, ${evidence.effectiveDateKind},
      ${JSON.stringify(evidence.dateProvenance)}::jsonb, ${eventIdentity || null}, ${duplicate.duplicateState},
      ${duplicate.reason ?? evidence.reviewReason}
    ) ON CONFLICT (slug) DO UPDATE SET
      headline = excluded.headline, town = excluded.town, source_name = excluded.source_name,
      source_url = excluded.source_url, verified_update = excluded.verified_update, local_reading = excluded.local_reading,
      status = excluded.status, source_published_at = excluded.source_published_at,
      original_event_date = excluded.original_event_date, effective_story_date = excluded.effective_story_date,
      effective_date_kind = excluded.effective_date_kind, date_provenance = excluded.date_provenance,
      event_identity = excluded.event_identity, duplicate_state = excluded.duplicate_state,
      duplicate_reason = excluded.duplicate_reason, updated_at = now()
    WHERE news_articles.status <> 'published'
    RETURNING id
  `);
  if (((saved as any).rows ?? []).length === 0) {
    throw new Error("Published stories cannot be overwritten; create a new draft for duplicate review.");
  }
  revalidatePath("/directoryadmin/news");
}

export async function publishArticle(data: FormData) {
  await requireAdminUserForPage("/directoryadmin/news");
  const id = value(data, "id");
  const published = await db.execute(sql`
    UPDATE news_articles SET status = 'published', published_at = now(), updated_at = now()
    WHERE id = ${id} AND status = 'draft' AND duplicate_state = 'unique'
      AND source_url <> '' AND verified_update <> '' AND local_reading <> ''
      AND source_published_at IS NOT NULL AND effective_story_date IS NOT NULL
      AND effective_date_kind IN ('original_event', 'source_publication')
      AND COALESCE(date_provenance->>'extractionNote', '') <> ''
      AND COALESCE(date_provenance->>'selectionRationale', '') <> ''
      AND COALESCE(date_provenance->>'confidence', '') IN ('high', 'medium', 'low')
      AND (
        (effective_date_kind = 'original_event' AND original_event_date IS NOT NULL AND effective_story_date = original_event_date)
        OR (effective_date_kind = 'source_publication' AND effective_story_date = source_published_at::date)
      )
    RETURNING id
  `);
  if (((published as any).rows ?? []).length === 0) {
    throw new Error("Article is not publishable: complete date evidence and resolve duplicate review first.");
  }
  revalidatePath("/directoryadmin/news");
}
