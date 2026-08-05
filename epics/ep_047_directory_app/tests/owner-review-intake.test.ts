/**
 * tests/owner-review-intake.test.ts — Focused contract checks for protected durable owner review intake.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-05 · Initial RED tests for capability protection, structured feedback, and no-mail transport.
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const root = new URL("../", import.meta.url);
const read = (path: string) => readFile(new URL(path, root), "utf8");

test("owner review schema keeps only capability hashes and page snapshots", async () => {
  const [schema, migration] = await Promise.all([read("lib/db/schema.ts"), read("migrations/0021_owner_review_intake.sql")]);
  assert.match(schema, /export const ownerReviewLinks/);
  assert.match(schema, /export const ownerReviewSubmissions/);
  assert.match(schema, /export const ownerReviewPageResponses/);
  assert.match(migration, /token_hash text NOT NULL UNIQUE/i);
  assert.match(migration, /page_open_date_time/i);
  assert.doesNotMatch(migration, /raw_token/i);
});

test("owner review endpoint is capability protected and does not send email", async () => {
  const [route, repository] = await Promise.all([
    read("app/review/[token]/actions.ts"), read("lib/owner-review/repository.ts"),
  ]);
  assert.match(route, /submitOwnerReview/);
  assert.match(repository, /FOR UPDATE/);
  assert.match(repository, /hashVerificationToken/);
  assert.doesNotMatch(repository, /sendMail|sendEmail|mailto:|verificationDeliver/);
});

test("owner review UI preserves per-page no-action and time-open structured model", async () => {
  const page = await read("app/review/[token]/page.tsx");
  assert.match(page, /No action required for this page/);
  assert.match(page, /pageOpenDateTime/);
  assert.match(page, /anythingElse/);
  assert.match(page, /accept.*change.*decline/s);
});
