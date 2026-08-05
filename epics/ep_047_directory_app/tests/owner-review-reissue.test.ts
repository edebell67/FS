/**
 * tests/owner-review-reissue.test.ts — Contract checks for controlled repeat owner-review invitations.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-05 · Defines the admin-only, separate review-invitation reissue contract.
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const root = new URL("../", import.meta.url);
const read = (path: string) => readFile(new URL(path, root), "utf8");

test("admin can explicitly reissue a fresh owner-review invitation for already preview-notified Ready for Preview businesses", async () => {
  const [action, page, candidates, delivery, migration] = await Promise.all([
    read("app/directoryadmin/site-previews/actions.ts"),
    read("app/directoryadmin/site-previews/page.tsx"),
    read("lib/verification/site-generation.ts"),
    read("lib/verification/preview-delivery.ts"),
    read("migrations/0022_owner_review_reissue_delivery.sql"),
  ]);

  assert.match(action, /export async function sendOwnerReviewInvitationAction/);
  assert.match(action, /getBusinessesReadyForOwnerReviewInvitation/);
  assert.match(action, /createOwnerReviewLink/);
  assert.match(action, /\/review\//);
  assert.match(action, /messageType:\s*"owner_review_invitation"/);
  assert.match(action, /confirmed/);
  assert.match(page, /Send owner-review invitation/);
  assert.match(page, /sendOwnerReviewInvitationAction/);
  assert.match(candidates, /export async function getBusinessesReadyForOwnerReviewInvitation/);
  assert.doesNotMatch(candidates.match(/export async function getBusinessesReadyForOwnerReviewInvitation[\s\S]*?(?=\n}\n|$)/)?.[0] ?? "", /alreadyNotified|notInArray/);
  assert.match(delivery, /owner_review_invitation/);
  assert.match(migration, /owner_review_invitation/);
});
