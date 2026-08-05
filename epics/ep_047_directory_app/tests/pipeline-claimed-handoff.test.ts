import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("pipeline explains the audited Claimed-to-generation handoff", async () => {
  const page = await readFile(new URL("../app/directoryadmin/pipeline/page.tsx", import.meta.url), "utf8");
  assert.match(page, /awaiting_site_generation/);
  assert.match(page, /Claim approval is recorded before a business queues here for generation/);
});
