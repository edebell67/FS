import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("protected generation-readiness route exposes only the current generation input snapshot", async () => {
  const route = await readFile("app/api/internal/site-generation/readiness/route.ts", "utf8");
  assert.match(route, /requireInternalApiKey/);
  assert.match(route, /getBusinessGenerationReadiness/);
  assert.match(route, /businessRef is required/);
});
