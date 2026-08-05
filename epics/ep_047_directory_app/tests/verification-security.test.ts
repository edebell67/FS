import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("generic pipeline mutation blocks protected lifecycle stages server-side", async () => {
  const [source, policy] = await Promise.all([
    readFile(new URL("../lib/db/queries/pipeline.ts", import.meta.url), "utf8"),
    readFile(new URL("../lib/pipeline/stage-movement-policy.ts", import.meta.url), "utf8"),
  ]);
  assert.match(source, /canMoveBetweenPipelineStages\(fromStage\.key, toStage\.key\)/);
  assert.match(source, /protectedStageMoveError\(\)/);
  assert.match(policy, /controlled workflow/);
});

test("recipient projection omits internal and provenance fields", async () => {
  const source = await readFile(new URL("../lib/verification/repository.ts", import.meta.url), "utf8");
  const lookup = source.slice(source.indexOf("export async function getVerificationByRawToken"), source.indexOf("export async function submitVerification"));
  assert.doesNotMatch(lookup, /internalNotes|notes|importedSource|importBatchId/);
});

test("delivery implementation is explicit, Gmail API-only, allowlisted, and hash-protected", async () => {
  const source = await readFile(new URL("../lib/verification/delivery.ts", import.meta.url), "utf8");
  assert.match(source, /VERIFICATION_DELIVERY_APPROVED/);
  assert.match(source, /INITIAL_ALLOWED_RECIPIENT =\s*\n?\s*process\.env\.VERIFICATION_RECIPIENT_ALLOWLIST/);
  assert.doesNotMatch(source, /INITIAL_ALLOWED_RECIPIENT = "[^"]+@[^"]+"/);
  assert.match(source, /VERIFICATION_FROM = "edward\.bell@thetechprinciple\.com"/);
  assert.match(source, /trackingKeyHash: hashTrackingKey/);
  assert.match(source, /gmail\.googleapis\.com\/gmail\/v1\/users\/me\/messages\/send/);
  assert.match(source, /oauth2\.googleapis\.com\/token/);
  assert.match(source, /sendMessage/);
  assert.doesNotMatch(source, /SMTP_|nodemailer|sendMail/);
  assert.doesNotMatch(source, /rawToken:\s*text|raw_token/);
});

test("verification submission ends on a recipient acknowledgement page", async () => {
  const page = await readFile(new URL("../app/verify/[token]/complete/page.tsx", import.meta.url), "utf8");
  assert.match(page, /Verification received/);
  assert.match(page, /has not changed publicly/i);
  assert.match(page, /manual review/i);
});

test("unavailable verification page offers a safe re-request route", async () => {
  const page = await readFile(new URL("../app/verify/[token]/page.tsx", import.meta.url), "utf8");
  assert.match(page, /href="\/verify\/request"/);
  assert.match(page, /Request a new link/);
});
