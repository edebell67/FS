import assert from "node:assert/strict";
import test from "node:test";

import { readFile } from "node:fs/promises";
import { contentHash, decideNewsIntakeItem, nextRetryState, parseNewsIntakeBatch, resolveNewsIntakeDirectory } from "../lib/news-intake/importer";

test("accepts only the versioned private news intake batch contract", () => {
  const batch = parseNewsIntakeBatch(JSON.stringify({
    version: "ep047.news-intake/v1",
    batchId: "daily-20260802",
    items: [{
      itemId: "council-roadworks-1",
      headline: "Roadworks update",
      town: "Birmingham",
      sourceName: "Birmingham Council",
      sourceUrl: "https://www.birmingham.gov.uk/news/roadworks",
      verifiedUpdate: "The council has published the diversion route.",
      localReading: "Local shops should plan for altered deliveries.",
      sourcePublishedAt: "2026-08-02",
      dateProvenanceNote: "Publication date from council notice.",
      dateConfidence: "high",
      dateSelectionRationale: "No earlier event date was evidenced.",
      selectedDateKind: "source_publication",
    }],
  }));

  assert.equal(batch.batchId, "daily-20260802");
  assert.equal(batch.items[0]?.headline, "Roadworks update");
  assert.throws(() => parseNewsIntakeBatch(JSON.stringify({ ...batch, version: "v2" })), /version/i);
  assert.throws(() => parseNewsIntakeBatch(JSON.stringify({ ...batch, items: [{ ...batch.items[0], status: "published" }] })), /status/i);
});

test("safe intake policy permits only draft or review_required, never published", () => {
  const item = parseNewsIntakeBatch(JSON.stringify({
    version: "ep047.news-intake/v1", batchId: "policy-test", items: [{
      itemId: "1", headline: "Update", town: "Bristol", sourceName: "Council", sourceUrl: "https://example.test/news",
      verifiedUpdate: "Verified", localReading: "Reading", sourcePublishedAt: "2026-08-02",
      dateProvenanceNote: "Publisher metadata", dateConfidence: "high", dateSelectionRationale: "No event date",
      selectedDateKind: "source_publication", eventIdentity: "roadworks-1",
    }],
  })).items[0]!;

  assert.deepEqual(decideNewsIntakeItem(item, null), { status: "draft", duplicateState: "unique", reason: null });
  assert.deepEqual(decideNewsIntakeItem(item, "published"), {
    status: "review_required", duplicateState: "review_required", reason: "matches_published_event",
  });
  assert.deepEqual(decideNewsIntakeItem({ ...item, sourcePublishedAt: "2026-02-31" }, null), {
    status: "review_required", duplicateState: "unique", reason: "missing_date_evidence",
  });
});

test("hashes canonical item content, restricts scanning to deployed intake, and bounds retries", () => {
  assert.equal(contentHash({ b: "two", a: "one" }), contentHash({ a: "one", b: "two" }));
  assert.equal(resolveNewsIntakeDirectory("/srv/app"), "/srv/app/private/news-intake");
  assert.deepEqual(nextRetryState(1), { status: "retryable", nextAttempt: 2 });
  assert.deepEqual(nextRetryState(3), { status: "failed", nextAttempt: 3 });
});

test("automatic importer and API receiver share the durable ledger service and cannot create published articles", async () => {
  const [script, service, migration] = await Promise.all([
    readFile(new URL("../scripts/import-news-batches.ts", import.meta.url), "utf8"),
    readFile(new URL("../lib/news-intake/service.ts", import.meta.url), "utf8"),
    readFile(new URL("../migrations/0019_news_intake_batch_ledger.sql", import.meta.url), "utf8"),
  ]);
  assert.match(script, /resolveNewsIntakeDirectory/);
  assert.match(script, /importNewsIntakeBatch/);
  assert.match(service, /news_intake_batches/);
  assert.match(service, /news_intake_items/);
  assert.match(service, /safeStatus: "draft" \| "review_required"/);
  assert.doesNotMatch(service, /VALUES[\s\S]{0,400}'published'/);
  assert.match(migration, /CREATE TABLE IF NOT EXISTS news_intake_batches/i);
  assert.match(migration, /CREATE TABLE IF NOT EXISTS news_intake_items/i);
  assert.match(migration, /UNIQUE \(batch_id, item_key\)/i);
  assert.match(migration, /attempt_count integer NOT NULL DEFAULT 0 CHECK \(attempt_count BETWEEN 0 AND 3\)/i);
});
