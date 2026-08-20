/**
 * tests/assistant-enquiry-delivery-route.test.ts — guards the protected TTP assistant enquiry sender.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-12 · Adds the RED contract for authenticated Gmail handoff so widget confirmation cannot rest on storage alone.
 */

import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

test("assistant enquiry sender uses a route-specific shared key, is fixed to TTP, and requires Gmail sent readback", async () => {
  const route = await readFile("app/api/internal/assistant-enquiries/route.ts", "utf8");
  assert.match(route, /ASSISTANT_ENQUIRY_DELIVERY_KEY/);
  assert.match(route, /timingSafeEqual/);
  assert.match(route, /the-tech-principle-local/);
  assert.match(route, /createGmailApiTransport/);
  assert.match(route, /SENT/);
  assert.match(route, /providerMessageId/);
  assert.doesNotMatch(route, /requireInternalApiKey/);
});
