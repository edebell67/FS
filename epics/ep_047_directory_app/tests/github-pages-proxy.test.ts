import assert from "node:assert/strict";
import test from "node:test";

import { githubPagesUrl } from "../lib/github-pages-proxy";

test("githubPagesUrl maps the public root to the FS GitHub Pages root", () => {
  assert.equal(githubPagesUrl("/").toString(), "https://edebell67.github.io/FS/");
});

test("githubPagesUrl preserves a public site path and query string", () => {
  assert.equal(
    githubPagesUrl("/blog/?tag=build").toString(),
    "https://edebell67.github.io/FS/blog/?tag=build"
  );
});

test("githubPagesUrl rejects traversal-like paths", () => {
  assert.throws(() => githubPagesUrl("/../../private"), /Invalid public-site path/);
});
