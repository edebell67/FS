/**
 * owner-dashboard-handoff-contract.test.js — guards one-password owner-console login.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-12 · Requires a tenant-bound short-lived handoff rather than a second password prompt.
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const root = new URL("../", import.meta.url);
const source = async (path) => readFile(new URL(path, root), "utf8");

test("owner dashboard handoff is tenant-bound, delivered in URL fragment, and consumed without a second password", async () => {
  const [server, widget, owner, ownerHtml] = await Promise.all([
    source("src/server.js"), source("public/widget.js"), source("public/owner.js"), source("public/owner.html")
  ]);
  assert.match(server, /handoffToken: ownerDashboardHandoffToken\(env, client\.id\)/);
  assert.match(server, /ownerDashboardHandoffAuthorized\(token, env, clientId\)/);
  assert.match(widget, /destination\.hash = new URLSearchParams\(\{ handoff: payload\.handoffToken \}\)\.toString\(\)/);
  assert.doesNotMatch(widget, /Enter this site’s owner password again there/);
  assert.match(owner, /new URLSearchParams\(location\.hash\.slice\(1\)\)/);
  assert.match(owner, /const routeTenant = new URLSearchParams\(location\.search\)\.get\('tenant'\) \|\| ''/);
  assert.match(owner, /if \(routeTenant\) \{[\s\S]*\$\('login-tenant-label'\)\.hidden = true/);
  assert.match(owner, /\$\('login-token'\)\.value = ''/);
  assert.match(ownerHtml, /autocomplete="new-password"/);
  assert.match(ownerHtml, /data-lpignore="true"/);
  assert.match(owner, /history\.replaceState\(null, '', `\$\{location\.pathname\}\?tenant=/);
});
