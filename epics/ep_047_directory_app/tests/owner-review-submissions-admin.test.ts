// tests/owner-review-submissions-admin.test.ts
//
// VERSION HISTORY
// v1.0.0 · 2026-08-07 · Initial version: covers the read-only admin view added
//   for gap `corrections` on EP047_end_to_end_workflow_gap_register.html.
//   Source-text checks (role gate, query wiring) rather than live-DB
//   integration tests -- no local Postgres was available this session. See
//   the task file for that explicit gap.
import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";

const root = new URL("..", import.meta.url);
async function source(path: string) { return readFile(new URL(path, root), "utf8"); }

test("the submissions list page requires operations authority", async () => {
  const page = await source("app/directoryadmin/owner-review-submissions/page.tsx");
  assert.match(page, /canManageVerification\(user\.role\)/);
  assert.match(page, /requireAdminUserForPage/);
});

test("the submission detail page requires operations authority", async () => {
  const page = await source("app/directoryadmin/owner-review-submissions/[submissionId]/page.tsx");
  assert.match(page, /canManageVerification\(user\.role\)/);
  assert.match(page, /requireAdminUserForPage/);
});

test("the list page queries listOwnerReviewSubmissions, not raw table access", async () => {
  const page = await source("app/directoryadmin/owner-review-submissions/page.tsx");
  assert.match(page, /listOwnerReviewSubmissions\(\)/);
});

test("the detail page queries getOwnerReviewSubmissionDetail, not raw table access", async () => {
  const page = await source("app/directoryadmin/owner-review-submissions/[submissionId]/page.tsx");
  assert.match(page, /getOwnerReviewSubmissionDetail\(/);
});

test("the admin nav links to the new submissions view, role-gated the same as Claims", async () => {
  const nav = await source("components/admin/AdminMenuModal.tsx");
  const claimsIdx = nav.indexOf("'Claims'");
  const feedbackIdx = nav.indexOf("'Owner feedback'");
  const gateIdx = nav.lastIndexOf(
    "['super_admin','admin','operations'].includes(role)",
    feedbackIdx,
  );
  assert.ok(claimsIdx > -1 && feedbackIdx > -1, "both menu entries must exist");
  assert.ok(
    gateIdx > -1 && gateIdx < feedbackIdx,
    "Owner feedback must be inside the same role-gated array as Claims, not unguarded",
  );
});

test("no apply/reject mutation exists yet -- the repository additions are read-only", async () => {
  const repo = await source("lib/owner-review/repository.ts");
  assert.match(repo, /export async function listOwnerReviewSubmissions/);
  assert.match(repo, /export async function getOwnerReviewSubmissionDetail/);
  // Deliberately absent for now -- documents the honest state of the gap
  // rather than a defect: an apply/reject action would need a schema
  // migration (e.g. reviewedAt/reviewedByUserId) not safely generated
  // without a local DB to verify it against this session.
  assert.doesNotMatch(repo, /export async function (apply|reject)OwnerReview/);
});
