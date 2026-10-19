/**
 * owner-dashboard-ui-contract.test.js — protects the mobile-first TTP owner shell.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-12 · Captures hidden-state, TTP black-lime, touch-target, and mobile-nav requirements.
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const cssUrl = new URL("../public/owner.css", import.meta.url);

test("owner dashboard hides prior login state and uses TTP black-lime mobile-first shell", async () => {
  const css = await readFile(cssUrl, "utf8");
  assert.match(css, /\[hidden\],\.screen\[hidden\]\{display:none!important\}/);
  assert.match(css, /--ink:#0a0c0e/);
  assert.match(css, /--lime:#c8f250/);
  assert.match(css, /\.dash-nav\{display:grid;grid-template-columns:repeat\(5,minmax\(0,1fr\)\)/);
  assert.match(css, /\.dash-nav button\{min-height:44px/);
  assert.match(css, /\.primary\{min-height:44px/);
  assert.match(css, /@media\(min-width:680px\)/);
});
