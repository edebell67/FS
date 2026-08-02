import assert from "node:assert/strict";
import test from "node:test";

import { contentHash, parseNewsIntakeBatch } from "../lib/news-intake/importer";
import { validateNewsIntakeDelivery } from "../lib/news-intake/request";

const batch = {
  version: "ep047.news-intake/v1",
  batchId: "receiver-20260802",
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
};

const raw = JSON.stringify(batch);

test("receiver delivery validation fails closed without a configured service key", () => {
  const result = validateNewsIntakeDelivery({
    raw,
    authorization: "Bearer sender-secret",
    batchHash: contentHash(parseNewsIntakeBatch(raw)),
    configuredApiKey: undefined,
  });

  assert.deepEqual(result, { ok: false, status: 401, error: "Not authenticated." });
});

test("receiver delivery validation requires an exact bearer key and canonical batch hash", () => {
  const unauthorized = validateNewsIntakeDelivery({
    raw,
    authorization: "Bearer wrong-secret",
    batchHash: contentHash(parseNewsIntakeBatch(raw)),
    configuredApiKey: "sender-secret",
  });
  assert.deepEqual(unauthorized, { ok: false, status: 401, error: "Not authenticated." });

  const tampered = validateNewsIntakeDelivery({
    raw,
    authorization: "Bearer sender-secret",
    batchHash: "0".repeat(64),
    configuredApiKey: "sender-secret",
  });
  assert.deepEqual(tampered, { ok: false, status: 400, error: "Invalid news batch hash." });
});

test("receiver delivery validation returns parsed batch only after authenticated integrity verification", () => {
  const result = validateNewsIntakeDelivery({
    raw,
    authorization: "Bearer sender-secret",
    batchHash: contentHash(parseNewsIntakeBatch(raw)),
    configuredApiKey: "sender-secret",
  });

  assert.equal(result.ok, true);
  if (result.ok) assert.equal(result.batch.batchId, batch.batchId);
});

test("POST receiver fails closed when NEWS_IMPORT_API_KEY is absent", async () => {
  const prior = process.env.NEWS_IMPORT_API_KEY;
  delete process.env.NEWS_IMPORT_API_KEY;
  try {
    const { POST } = await import("../app/api/internal/news-intake/route");
    const response = await POST(new Request("https://directory.test/api/internal/news-intake", {
      method: "POST",
      headers: { authorization: "Bearer sender-secret", "x-news-batch-hash": contentHash(parseNewsIntakeBatch(raw)) },
      body: raw,
    }));
    assert.equal(response.status, 401);
    assert.deepEqual(await response.json(), { error: "Not authenticated." });
  } finally {
    if (prior === undefined) delete process.env.NEWS_IMPORT_API_KEY;
    else process.env.NEWS_IMPORT_API_KEY = prior;
  }
});
