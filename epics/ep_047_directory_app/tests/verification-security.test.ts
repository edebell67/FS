import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("generic pipeline mutation blocks Verification and Claimed server-side", async () => {
  const source = await readFile(new URL("../lib/db/queries/pipeline.ts", import.meta.url), "utf8");
  assert.match(source, /toStage\.boardColumn === "Verification"/);
  assert.match(source, /toStage\.boardColumn === "Claimed"/);
  assert.match(source, /controlled workflow/);
});

test("recipient projection omits internal and provenance fields", async () => {
  const source = await readFile(new URL("../lib/verification/repository.ts", import.meta.url), "utf8");
  const lookup = source.slice(source.indexOf("export async function getVerificationByRawToken"), source.indexOf("export async function submitVerification"));
  assert.doesNotMatch(lookup, /internalNotes|notes|importedSource|importBatchId/);
});

test("delivery implementation is preview-only and contains no network send", async () => {
  const source = await readFile(new URL("../lib/verification/delivery.ts", import.meta.url), "utf8");
  assert.match(source, /deliveryEnabled: false/);
  assert.equal(source.includes("fetch("), false);
  assert.doesNotMatch(source, /sendMail|providerMessageId/);
});
