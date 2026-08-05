import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("protected completion supports an audited regenerated URL only from awaiting generation with an existing URL", async () => {
  const service = await readFile("lib/verification/site-generation.ts", "utf8");
  const route = await readFile("app/api/internal/site-generation/complete/route.ts", "utf8");
  assert.match(service, /replaceGeneratedSiteAfterRegeneration/);
  assert.match(service, /awaitingStageId/);
  assert.match(service, /isNotNull\(businesses\.generatedSiteUrl\)/);
  assert.match(route, /replace_after_regeneration/);
  assert.match(route, /regenerationReason is required/);
});
