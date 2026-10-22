import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

const source = (path: string) => readFile(new URL(`../${path}`, import.meta.url), "utf8");

test("every production outbound renderer uses the shared black-and-lime email shell", async () => {
  const [verification, preview, claim] = await Promise.all([
    source("lib/verification/email-template.ts"), source("lib/verification/preview-delivery.ts"),
    source("lib/verification/claim-success-delivery.ts"),
  ]);
  for (const module of [verification, preview, claim]) assert.match(module, /renderTheTechPrincipleEmail/);
  assert.doesNotMatch(preview, /background:#00765e/);
  assert.doesNotMatch(claim, /html: `<p>/);
});
