import assert from "node:assert/strict";
import test from "node:test";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const read = (relative: string) => readFileSync(join(root, relative), "utf8");

test("public News uses the approved interactive two-pane reader with preserved source separation", () => {
  const componentPath = "app/news/PublicNewsReader.tsx";
  assert.equal(existsSync(join(root, componentPath)), true, "two-pane reader component must exist");
  const page = read("app/news/page.tsx");
  const component = read(componentPath);

  assert.match(page, /status = 'published'/);
  assert.match(page, /publicScopeWhere\(\)/);
  assert.match(component, /By place/);
  assert.match(component, /ticker-track/);
  assert.match(component, /animation:\s*ticker-left/);
  assert.match(component, /@keyframes ticker-left/);
  assert.match(component, /prefers-reduced-motion:\s*reduce/);
  assert.match(component, /Search headlines, places or topics/);
  assert.match(component, /aria-label="View by town, city or postcode"/);
  assert.match(component, /aria-label="View by date"/);
  assert.match(component, /Clear filters/);
  assert.match(component, /Selected article/);
  assert.match(component, /Verified update/);
  assert.match(component, /Local reading/);
  assert.match(component, /Source:/);
  assert.match(component, /target="_blank"/);
});

test("public News reader is mobile-first and keeps interaction targets usable", () => {
  const component = read("app/news/PublicNewsReader.tsx");

  assert.match(component, /px-4[^"`]*sm:px-6/);
  assert.match(component, /grid-cols-1[^"`]*lg:grid-cols-\[minmax\(0,1\.05fr\)_minmax\(0,\.95fr\)\]/);
  assert.match(component, /min-h-11/);
  assert.match(component, /lg:sticky/);
  assert.match(component, /aria-pressed/);
});
