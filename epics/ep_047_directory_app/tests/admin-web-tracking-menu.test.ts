import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("..", import.meta.url);

async function source(path: string) {
  return readFile(new URL(path, root), "utf8");
}

test("admin menu links Web Tracking to the existing tenant-scoped assistant owner dashboard", async () => {
  const nav = await source("components/admin/AdminMenuModal.tsx");
  const claimsIdx = nav.indexOf("'Claims'");
  const trackingIdx = nav.indexOf("'Web Tracking'");
  const gateIdx = nav.lastIndexOf("['super_admin','admin','operations'].includes(role)", trackingIdx);

  assert.ok(trackingIdx > -1, "Web Tracking must be present in the admin menu");
  assert.ok(gateIdx > -1 && gateIdx < trackingIdx && claimsIdx < trackingIdx, "Web Tracking must use the operational role gate");
  assert.match(nav, /https:\/\/shared-website-assistant-api\.onrender\.com\/owner\?tenant=the-tech-principle-local/);
  assert.doesNotMatch(nav, /token=|password=/i);
});
