import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("verification panel does not call a verification email a site preview", async () => {
  const panel = await readFile(new URL("../components/admin/VerificationLinkPanel.tsx", import.meta.url), "utf8");
  assert.match(panel, /Prepare verification email/);
  assert.doesNotMatch(panel, />Prepare preview</);
});
