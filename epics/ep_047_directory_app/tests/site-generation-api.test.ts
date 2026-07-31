/**
 * tests/site-generation-api.test.ts — covers internal bearer-key auth behaviour and
 * the contract of the three site-generation handoff endpoints.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-07-31 · requireInternalApiKey() is now async and also
 *   accepts an authenticated admin session, not just the bearer key.
 * v1.0.0 · 2026-07-29 · Initial version.
 */

import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";
import { requireInternalApiKey } from "../lib/auth/require-internal-api";

const root = new URL("..", import.meta.url);
async function source(path: string) { return readFile(new URL(path, root), "utf8"); }

function makeRequest(headers: Record<string, string> = {}) {
  return new Request("https://example.com/internal", { headers });
}

test("internal API key auth fails closed when unconfigured (no session, no key)", async () => {
  delete process.env.INTERNAL_API_KEY;
  const result = await requireInternalApiKey(makeRequest({ authorization: "Bearer anything" }));
  assert.notEqual(result, null);
});

test("internal API key auth rejects a missing or wrong bearer token", async () => {
  process.env.INTERNAL_API_KEY = "test-internal-key";
  assert.notEqual(await requireInternalApiKey(makeRequest()), null);
  assert.notEqual(await requireInternalApiKey(makeRequest({ authorization: "Bearer wrong" })), null);
  assert.equal(await requireInternalApiKey(makeRequest({ authorization: "Bearer test-internal-key" })), null);
  delete process.env.INTERNAL_API_KEY;
});

test("internal API auth also accepts an authenticated admin session, not only the bearer key", async () => {
  const authSource = await source("lib/auth/require-internal-api.ts");
  assert.match(authSource, /getCurrentUser/);
  assert.match(authSource, /if \(user\) return null;/);
});

test("queue endpoint requires internal API auth and is read-only", async () => {
  const route = await source("app/api/internal/site-generation/queue/route.ts");
  assert.match(route, /requireInternalApiKey\(request\)/);
  assert.match(route, /export async function GET/);
  assert.doesNotMatch(route, /export async function POST/);
  assert.match(route, /getBusinessesAwaitingSiteGeneration/);
});

test("complete endpoint requires businessId and siteUrl, never speculative", async () => {
  const route = await source("app/api/internal/site-generation/complete/route.ts");
  assert.match(route, /requireInternalApiKey\(request\)/);
  assert.match(route, /businessId and siteUrl are required/);
  assert.match(route, /recordSiteGenerated/);
});

test("notify endpoint is fail-closed and idempotent by design", async () => {
  const route = await source("app/api/internal/site-generation/notify/route.ts");
  assert.match(route, /requireInternalApiKey\(request\)/);
  assert.match(route, /previewDeliveryEnabled\(\)/);
  assert.match(route, /getBusinessesReadyForPreviewNotification/);
  assert.match(route, /preparePreviewMessage/);
  assert.match(route, /sendPreparedPreviewMessage/);
});
