import assert from "node:assert/strict";
import test from "node:test";

import { githubPagesUrl } from "../lib/github-pages-proxy";

test("githubPagesUrl maps the public root to the epics GitHub Pages root", () => {
  assert.equal(githubPagesUrl("/").toString(), "https://edebell67.github.io/epics/");
});

test("githubPagesUrl preserves a public site path and query string", () => {
  assert.equal(
    githubPagesUrl("/blog/?tag=build").toString(),
    "https://edebell67.github.io/epics/blog/?tag=build"
  );
});

test("githubPagesUrl rejects traversal-like paths", () => {
  assert.throws(() => githubPagesUrl("/../../private"), /Invalid public-site path/);
});

test("githubPagesRedirectLocation keeps GitHub Pages directory redirects on the public path", async () => {
  const { githubPagesRedirectLocation } = await import("../lib/github-pages-proxy");
  assert.equal(
    githubPagesRedirectLocation("https://edebell67.github.io/epics/blog/"),
    "/blog/"
  );
});

test("githubPagesResponseHeaders infers content-type from the request path over a wrong upstream header", async () => {
  const { githubPagesResponseHeaders } = await import("../lib/github-pages-proxy");
  const upstream = new Headers({ "content-type": "text/plain; charset=utf-8" });
  const headers = githubPagesResponseHeaders(upstream, "/dg-maintenance-uk-ltd/index.html");
  assert.equal(headers.get("content-type"), "text/html; charset=utf-8");
});

test("githubPagesResponseHeaders falls back to upstream content-type for an unknown extension", async () => {
  const { githubPagesResponseHeaders } = await import("../lib/github-pages-proxy");
  const upstream = new Headers({ "content-type": "application/octet-stream" });
  const headers = githubPagesResponseHeaders(upstream, "/dg-maintenance-uk-ltd/data.unknownext");
  assert.equal(headers.get("content-type"), "application/octet-stream");
});

test("githubPagesRedirectLocation refuses external redirect locations", async () => {
  const { githubPagesRedirectLocation } = await import("../lib/github-pages-proxy");
  assert.equal(githubPagesRedirectLocation("https://example.com/next"), null);
});
