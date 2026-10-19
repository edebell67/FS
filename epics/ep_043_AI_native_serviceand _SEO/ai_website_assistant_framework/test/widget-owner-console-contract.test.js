/**
 * widget-owner-console-contract.test.js — guards the owner-console handoff.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-12 · Ensures the public widget uses the deployed password
 * gate and opens the separate protected owner dashboard.
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const widgetUrl = new URL("../public/widget.js", import.meta.url);

test("widget owner console uses the deployed dashboard-access gate and opens the dedicated dashboard", async () => {
  const widget = await readFile(widgetUrl, "utf8");
  assert.match(widget, /\/api\/public\/owner-dashboard-access/);
  assert.doesNotMatch(widget, /\/api\/public\/owner\/login/);
  assert.match(widget, /const dashboardWindow = window\.open\("", "_blank"\)/);
  assert.match(widget, /dashboardWindow\.location\.replace\(destination\.toString\(\)\)/);
  assert.match(widget, /handoffToken/);
  assert.doesNotMatch(widget, /Enter this site’s owner password again there/);
});
