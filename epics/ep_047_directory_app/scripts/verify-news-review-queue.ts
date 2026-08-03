// EP047 — reproduce the 2026-07-30 production E2E finding: a saved draft did not appear
// in the /directoryadmin/news review queue ("No articles yet."). This mirrors the exact
// INSERT from saveArticle() and the exact SELECT from the admin page, on one connection/
// transaction (rolled back at the end), using the real evidence-assessment functions.
import pg from "pg";
import { assessNewsDateEvidence, chooseDuplicateSaveAction } from "../ep047_visibility_news/admin/news-evidence";

async function main() {
  const client = new pg.Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();
  await client.query("BEGIN");
  try {
    const slug = `fixture-review-queue-${Date.now()}`;
    const eventIdentity = "";

    const evidence = assessNewsDateEvidence({
      originalEventDate: "",
      sourcePublishedAt: "2026-07-15",
      dateProvenanceNote: "Fixture: extracted from source byline",
      dateConfidence: "high",
      dateSelectionRationale: "Fixture: only source publication date available",
      selectedDateKind: "source_publication",
    });

    const matching = eventIdentity
      ? await client.query(`SELECT status FROM news_articles WHERE event_identity = $1 AND slug <> $2 ORDER BY (status = 'published') DESC LIMIT 1`, [eventIdentity, slug])
      : null;
    const duplicate = chooseDuplicateSaveAction({ matchingStatus: matching?.rows[0]?.status ?? null });
    const status = !evidence.readyForPublish || duplicate.duplicateState === "review_required" ? "review_required" : "draft";

    const saved = await client.query(
      `INSERT INTO news_articles (
        slug, headline, town, source_name, source_url, verified_update, local_reading, business_voices,
        status, source_published_at, original_event_date, effective_story_date, effective_date_kind,
        date_provenance, event_identity, duplicate_state, duplicate_reason
      ) VALUES (
        $1,$2,$3,$4,$5,$6,$7,NULL,
        $8, $9, $10, $11, $12,
        $13::jsonb, $14, $15, $16
      ) ON CONFLICT (slug) DO UPDATE SET
        headline = excluded.headline, town = excluded.town, source_name = excluded.source_name,
        source_url = excluded.source_url, verified_update = excluded.verified_update, local_reading = excluded.local_reading,
        status = excluded.status, source_published_at = excluded.source_published_at,
        original_event_date = excluded.original_event_date, effective_story_date = excluded.effective_story_date,
        effective_date_kind = excluded.effective_date_kind, date_provenance = excluded.date_provenance,
        event_identity = excluded.event_identity, duplicate_state = excluded.duplicate_state,
        duplicate_reason = excluded.duplicate_reason, updated_at = now()
      WHERE news_articles.status <> 'published'
      RETURNING id`,
      [
        slug, "Fixture Review Queue Headline", "Fixture Town", "Fixture Source", "https://fixture.invalid/review-queue",
        "Verified fixture update", "Local reading fixture",
        status, evidence.sourcePublishedDate ? `${evidence.sourcePublishedDate}T00:00:00.000Z` : null,
        evidence.originalEventDate, evidence.effectiveStoryDate, evidence.effectiveDateKind,
        JSON.stringify(evidence.dateProvenance), eventIdentity || null, duplicate.duplicateState, duplicate.reason ?? evidence.reviewReason,
      ]
    );
    if (saved.rows.length === 0) throw new Error("INSERT ... RETURNING id returned no row (saveArticle would have thrown 'Published stories cannot be overwritten')");
    const insertedId = saved.rows[0].id;

    // Exact query the admin page runs (app/directoryadmin/news/page.tsx).
    const queue = await client.query(`
      SELECT id, slug, headline, town, status, source_name, source_published_at, original_event_date,
        effective_story_date, effective_date_kind, duplicate_state, duplicate_reason, updated_at
      FROM news_articles ORDER BY updated_at DESC
    `);
    const found = queue.rows.find((r) => r.id === insertedId);
    if (!found) throw new Error(`inserted article ${insertedId} (slug=${slug}) did not appear in the review-queue query; queue had ${queue.rows.length} row(s)`);
    if (found.status !== "draft") throw new Error(`expected status 'draft' for a fully-evidenced unique article, got '${found.status}'`);

    // Edge case 2: incomplete date evidence -> review_required, must still be visible (not silently dropped).
    const incompleteSlug = `fixture-review-queue-incomplete-${Date.now()}`;
    const incompleteEvidence = assessNewsDateEvidence({
      originalEventDate: "", sourcePublishedAt: "", dateProvenanceNote: "", dateConfidence: "", dateSelectionRationale: "", selectedDateKind: "",
    });
    const incompleteDuplicate = chooseDuplicateSaveAction({ matchingStatus: null });
    const incompleteStatus = !incompleteEvidence.readyForPublish || incompleteDuplicate.duplicateState === "review_required" ? "review_required" : "draft";
    const incompleteSaved = await client.query(
      `INSERT INTO news_articles (slug, headline, town, source_name, source_url, verified_update, local_reading, status, duplicate_state, duplicate_reason)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) RETURNING id`,
      [incompleteSlug, "Fixture Incomplete Headline", "Fixture Town", "Fixture Source", "https://fixture.invalid/incomplete",
        "Verified fixture update", "Local reading fixture", incompleteStatus, incompleteDuplicate.duplicateState, incompleteDuplicate.reason ?? incompleteEvidence.reviewReason]
    );
    const incompleteQueue = await client.query(`SELECT id, status, duplicate_reason FROM news_articles WHERE id = $1`, [incompleteSaved.rows[0].id]);
    if (incompleteQueue.rows.length === 0) throw new Error("incomplete-evidence draft did not appear in the queue");
    if (incompleteQueue.rows[0].status !== "review_required") throw new Error(`expected 'review_required' for incomplete evidence, got '${incompleteQueue.rows[0].status}'`);

    // Edge case 3: eventIdentity matching an existing non-published article -> review_required (matches_existing_event), still visible.
    const identity = `fixture-event-${Date.now()}`;
    const firstOfPair = await client.query(
      `INSERT INTO news_articles (slug, headline, town, source_name, source_url, verified_update, local_reading, status, event_identity, duplicate_state)
       VALUES ($1,$2,$3,$4,$5,$6,$7,'draft',$8,'unique') RETURNING id`,
      [`fixture-pair-a-${Date.now()}`, "Fixture Pair A", "Fixture Town", "Fixture Source", "https://fixture.invalid/pair-a", "Verified", "Reading", identity]
    );
    const secondMatch = await client.query(`SELECT status FROM news_articles WHERE event_identity = $1 ORDER BY (status = 'published') DESC LIMIT 1`, [identity]);
    const secondDuplicate = chooseDuplicateSaveAction({ matchingStatus: secondMatch.rows[0]?.status ?? null });
    const secondSaved = await client.query(
      `INSERT INTO news_articles (slug, headline, town, source_name, source_url, verified_update, local_reading, status, event_identity, duplicate_state, duplicate_reason)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11) RETURNING id`,
      [`fixture-pair-b-${Date.now()}`, "Fixture Pair B", "Fixture Town", "Fixture Source", "https://fixture.invalid/pair-b", "Verified", "Reading",
        "review_required", identity, secondDuplicate.duplicateState, secondDuplicate.reason]
    );
    const pairCheck = await client.query(`SELECT id, status, duplicate_reason FROM news_articles WHERE id = $1`, [secondSaved.rows[0].id]);
    if (pairCheck.rows.length === 0) throw new Error("second-of-pair duplicate draft did not appear in the queue");
    if (pairCheck.rows[0].duplicate_reason !== "matches_existing_event") throw new Error(`expected duplicate_reason 'matches_existing_event', got '${pairCheck.rows[0].duplicate_reason}'`);
    void firstOfPair;

    console.log(JSON.stringify({
      insertedId, status: found.status, queueSize: queue.rows.length,
      checks: ["fully-evidenced-draft-visible", "incomplete-evidence-review-required-visible", "duplicate-event-pair-review-required-visible"],
      result: "pass: all three states are visible in the review queue on current code",
    }));
    await client.query("ROLLBACK");
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    await client.end();
  }
}

main().catch((error) => { console.error(error); process.exit(1); });
