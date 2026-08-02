import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import {
  contentHash, decideNewsIntakeItem, MAX_NEWS_INTAKE_ATTEMPTS, nextRetryState,
  type NewsIntakeBatch, type NewsIntakeItem,
} from "@/lib/news-intake/importer";

function slugPart(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 120) || "item";
}

function itemSlug(batchKey: string, item: NewsIntakeItem): string {
  return `intake-${slugPart(batchKey)}-${slugPart(item.itemId)}`.slice(0, 240);
}

function retryAt(attempt: number): Date {
  return new Date(Date.now() + Math.min(60, 2 ** Math.max(0, attempt - 1)) * 60_000);
}

type Outcome = "draft" | "review_required" | "retryable" | "failed" | "skipped";

export type NewsIntakeBatchOutcome = {
  batchId: string;
  status: "completed" | "retryable" | "failed" | "already_processed";
  received: number;
  drafted: number;
  reviewRequired: number;
  skipped: number;
  retryable: number;
  failed: number;
};

async function claimBatch(sourceName: string, batch: NewsIntakeBatch) {
  const result = await db.execute(sql`
    INSERT INTO news_intake_batches (batch_key, schema_version, source_filename, content_hash, status, attempt_count, started_at)
    VALUES (${batch.batchId}, ${batch.version}, ${sourceName}, ${contentHash(batch)}, 'processing', 1, now())
    ON CONFLICT (batch_key) DO UPDATE SET
      status = 'processing', attempt_count = news_intake_batches.attempt_count + 1,
      started_at = now(), next_retry_at = NULL, last_error = NULL, updated_at = now()
    WHERE news_intake_batches.content_hash = excluded.content_hash
      AND news_intake_batches.status IN ('pending', 'processing', 'retryable')
      AND (news_intake_batches.next_retry_at IS NULL OR news_intake_batches.next_retry_at <= now())
      AND news_intake_batches.attempt_count < ${MAX_NEWS_INTAKE_ATTEMPTS}
    RETURNING id, attempt_count
  `);
  return (result as unknown as { rows?: Array<{ id: string; attempt_count: number }> }).rows?.[0] ?? null;
}

async function importItem(batchId: string, batch: NewsIntakeBatch, item: NewsIntakeItem, source: string): Promise<Outcome> {
  const batchKey = batch.batchId;
  const itemRow = await db.execute(sql`
    INSERT INTO news_intake_items (batch_id, item_key, content_hash, status, attempt_count, audit)
    VALUES (${batchId}, ${item.itemId}, ${contentHash(item)}, 'processing', 1, ${JSON.stringify({ source })}::jsonb)
    ON CONFLICT (batch_id, item_key) DO UPDATE SET
      status = 'processing', attempt_count = news_intake_items.attempt_count + 1, updated_at = now(), last_error = NULL
    WHERE news_intake_items.content_hash = excluded.content_hash
      AND news_intake_items.status IN ('pending', 'processing', 'retryable')
      AND news_intake_items.attempt_count < ${MAX_NEWS_INTAKE_ATTEMPTS}
    RETURNING id, attempt_count
  `);
  const ledger = (itemRow as unknown as { rows?: Array<{ id: string; attempt_count: number }> }).rows?.[0];
  if (!ledger) return "skipped";

  try {
    const slug = itemSlug(batchKey, item);
    const matching = item.eventIdentity ? await db.execute(sql`
      SELECT status FROM news_articles WHERE event_identity = ${item.eventIdentity} AND slug <> ${slug}
      ORDER BY (status = 'published') DESC LIMIT 1
    `) : null;
    const matchingStatus = (matching as unknown as { rows?: Array<{ status: string }> })?.rows?.[0]?.status ?? null;
    const decision = decideNewsIntakeItem(item, matchingStatus);
    const safeStatus: "draft" | "review_required" = decision.status;
    const evidence = {
      extractionNote: item.dateProvenanceNote,
      confidence: item.dateConfidence,
      selectionRationale: item.dateSelectionRationale,
      intakeVersion: batch.version,
    };
    const articleResult = await db.execute(sql`
      INSERT INTO news_articles (
        slug, headline, town, source_name, source_url, verified_update, local_reading, business_voices,
        status, source_published_at, original_event_date, effective_story_date, effective_date_kind,
        date_provenance, event_identity, duplicate_state, duplicate_reason
      ) VALUES (
        ${slug}, ${item.headline}, ${item.town}, ${item.sourceName}, ${item.sourceUrl}, ${item.verifiedUpdate},
        ${item.localReading}, ${item.businessVoices ?? null}, ${safeStatus}, ${item.sourcePublishedAt}::timestamptz,
        ${item.originalEventDate ?? null}::date,
        ${item.selectedDateKind === 'original_event' ? item.originalEventDate ?? null : item.sourcePublishedAt}::date,
        ${item.selectedDateKind}, ${JSON.stringify(evidence)}::jsonb, ${item.eventIdentity ?? null},
        ${decision.duplicateState}, ${decision.reason}
      ) ON CONFLICT (slug) DO UPDATE SET
        headline = excluded.headline, town = excluded.town, source_name = excluded.source_name, source_url = excluded.source_url,
        verified_update = excluded.verified_update, local_reading = excluded.local_reading, business_voices = excluded.business_voices,
        status = excluded.status, source_published_at = excluded.source_published_at, original_event_date = excluded.original_event_date,
        effective_story_date = excluded.effective_story_date, effective_date_kind = excluded.effective_date_kind,
        date_provenance = excluded.date_provenance, event_identity = excluded.event_identity, duplicate_state = excluded.duplicate_state,
        duplicate_reason = excluded.duplicate_reason, updated_at = now()
      WHERE news_articles.status <> 'published'
      RETURNING id
    `);
    const article = (articleResult as unknown as { rows?: Array<{ id: string }> }).rows?.[0];
    if (!article) throw new Error("Published news article cannot be overwritten by intake.");
    for (const category of item.categories ?? []) await db.execute(sql`
      INSERT INTO news_article_categories (article_id, category_key, category_label)
      VALUES (${article.id}, ${slugPart(category)}, ${category}) ON CONFLICT DO NOTHING
    `);
    await db.execute(sql`
      UPDATE news_intake_items SET status = ${safeStatus}, article_id = ${article.id}, outcome_reason = ${decision.reason},
        audit = ${JSON.stringify({ source, decision })}::jsonb, processed_at = now(), updated_at = now()
      WHERE id = ${ledger.id}
    `);
    return safeStatus;
  } catch (error) {
    const retry = nextRetryState(ledger.attempt_count);
    await db.execute(sql`
      UPDATE news_intake_items SET status = ${retry.status}, last_error = ${error instanceof Error ? error.message : "Import failed"}, updated_at = now()
      WHERE id = ${ledger.id}
    `);
    return retry.status;
  }
}

function summarize(batchId: string, received: number, status: NewsIntakeBatchOutcome["status"], outcomes: Outcome[]): NewsIntakeBatchOutcome {
  return {
    batchId, status, received,
    drafted: outcomes.filter((outcome) => outcome === "draft").length,
    reviewRequired: outcomes.filter((outcome) => outcome === "review_required").length,
    skipped: outcomes.filter((outcome) => outcome === "skipped").length,
    retryable: outcomes.filter((outcome) => outcome === "retryable").length,
    failed: outcomes.filter((outcome) => outcome === "failed").length,
  };
}

export async function importNewsIntakeBatch(batch: NewsIntakeBatch, sourceName: string): Promise<NewsIntakeBatchOutcome> {
  const claim = await claimBatch(sourceName, batch);
  if (!claim) return summarize(batch.batchId, batch.items.length, "already_processed", []);

  try {
    const outcomes = await Promise.all(batch.items.map((item) => importItem(claim.id, batch, item, sourceName)));
    const hasRejections = outcomes.some((outcome) => outcome === "failed" || outcome === "retryable");
    const batchStatus = hasRejections && claim.attempt_count < MAX_NEWS_INTAKE_ATTEMPTS ? "retryable" : hasRejections ? "failed" : "completed";
    await db.execute(sql`
      UPDATE news_intake_batches SET status = ${batchStatus}, next_retry_at = ${batchStatus === "retryable" ? retryAt(nextRetryState(claim.attempt_count).nextAttempt) : null},
        completed_at = ${batchStatus === "completed" || batchStatus === "failed" ? new Date() : null}, updated_at = now()
      WHERE id = ${claim.id}
    `);
    return summarize(batch.batchId, batch.items.length, batchStatus, outcomes);
  } catch (error) {
    const retry = nextRetryState(claim.attempt_count);
    await db.execute(sql`
      UPDATE news_intake_batches SET status = ${retry.status}, next_retry_at = ${retry.status === "retryable" ? retryAt(retry.nextAttempt) : null},
        last_error = ${error instanceof Error ? error.message : "Batch import failed"}, completed_at = ${retry.status === "failed" ? new Date() : null}, updated_at = now()
      WHERE id = ${claim.id}
    `);
    return summarize(batch.batchId, batch.items.length, retry.status, []);
  }
}
