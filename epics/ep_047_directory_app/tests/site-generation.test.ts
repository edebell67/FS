/**
 * tests/site-generation.test.ts — covers claim-approval queueing, the queue stage
 * being explicit rather than inferred, and the notification guard.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-29 · Initial version.
 */

import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";
import {
  assertApprovedCustomerProxyUrl,
  DEFAULT_CUSTOMER_PROXY_HOSTNAMES,
  verifyGeneratedSiteUrl,
} from "../lib/verification/site-generation-guards";

const root = new URL("..", import.meta.url);
async function source(path: string) { return readFile(new URL(path, root), "utf8"); }

test("claim approval immediately queues the business for automated site generation", async () => {
  const repository = await source("lib/verification/claims-approval.ts");
  assert.match(repository, /awaiting_site_generation/);
  assert.match(repository, /Claim approved; queued for automated site generation/);
  assert.match(repository, /source: "automation"/);
  // Claimed remains a real, audited transition -- not skipped or overwritten silently.
  assert.match(repository, /reason: "Claim approved from Claims pending queue"/);
});

test("site generation queue is a distinct pipeline stage, not a business_claimed + null check", async () => {
  const module = await source("lib/verification/site-generation.ts");
  assert.match(module, /getStageId\("awaiting_site_generation"\)/);
  assert.doesNotMatch(module, /eq\(pipelineStages\.key, "business_claimed"\)/);
});

test("recording generation advances to ready_for_preview, never speculatively", async () => {
  const module = await source("lib/verification/site-generation.ts");
  assert.match(module, /getStageId\("ready_for_preview"\)/);
  assert.match(module, /export async function recordSiteGenerated/);
  assert.match(module, /generatedSiteUrl: verifiedUrl\.href, websiteGeneratedAt: now/);
  assert.match(module, /verifyGeneratedSiteUrl\(input\.siteUrl\)/);
});

test("generated-site completion accepts only HTTPS URLs on approved customer proxy hostnames", () => {
  assert.deepEqual(DEFAULT_CUSTOMER_PROXY_HOSTNAMES, ["thetechprinciple.com"]);
  assert.equal(
    assertApprovedCustomerProxyUrl("https://thetechprinciple.com/test02-prospect-ltd/").href,
    "https://thetechprinciple.com/test02-prospect-ltd/",
  );
  assert.throws(
    () => assertApprovedCustomerProxyUrl("http://thetechprinciple.com/test02-prospect-ltd/"),
    /HTTPS/,
  );
  assert.throws(
    () => assertApprovedCustomerProxyUrl("https://example.com/test02-prospect-ltd/"),
    /approved customer proxy hostname/,
  );
});

test("live verification requires the approved public URL itself to return success", async () => {
  const verified = await verifyGeneratedSiteUrl(
    "https://thetechprinciple.com/test02-prospect-ltd/",
    (async () => new Response("ok", { status: 200 })) as typeof fetch,
  );
  assert.equal(verified.href, "https://thetechprinciple.com/test02-prospect-ltd/");
  await assert.rejects(
    verifyGeneratedSiteUrl(
      "https://thetechprinciple.com/test02-prospect-ltd/",
      (async () => new Response("not found", { status: 404 })) as typeof fetch,
    ),
    /did not verify live \(HTTP 404\)/,
  );
});

test("completion service locks and conditionally advances only awaiting businesses without an existing generated URL", async () => {
  const module = await source("lib/verification/site-generation.ts");
  assert.match(module, /FOR UPDATE/);
  assert.match(module, /biz\.current_stage_id !== awaitingStageId/);
  assert.match(module, /generatedSiteUrl/);
  assert.match(module, /eq\(businesses\.currentStageId, awaitingStageId\)/);
  assert.match(module, /recoverGeneratedSiteAfterManualReview/);
});

test("preview-ready notification guard is absence of a prior message, not a further pipeline stage", async () => {
  const module = await source("lib/verification/site-generation.ts");
  assert.match(module, /getBusinessesReadyForPreviewNotification/);
  assert.match(module, /messageType, "preview_ready"/);
  assert.match(module, /notInArray\(businesses\.id, excludeIds\)/);
});

test("stage rename migration is additive/rename only, no stage removed", async () => {
  const migration = await source("migrations/0016_site_generation_queue_stage.sql");
  assert.match(migration, /INSERT INTO pipeline_stages/);
  assert.match(migration, /awaiting_site_generation/);
  assert.match(migration, /UPDATE pipeline_stages/);
  assert.match(migration, /key = 'ready_for_preview'/);
  assert.doesNotMatch(migration, /DELETE FROM pipeline_stages/i);
  assert.doesNotMatch(migration, /DROP /i);
});
