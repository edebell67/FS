import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { runAllTownCollection } from "../src/all-town-news-runner.js";

const registry = {
  version: "ep047.all-town-news-sources/v1",
  sources: [{ town: "Manchester", name: "CityCo", canonicalUrl: "https://cityco.com/news/", useMode: "enabled" }],
};
const listing = '<article><a href="/news/latest/">Latest Manchester update</a></article>';
const article = '<html><head><meta property="og:title" content="Latest Manchester update"><meta property="article:published_time" content="2026-08-13T10:00:00Z"></head></html>';

async function fixtureFetch(url) {
  return { url, status: 200, html: url.endsWith('/news/') ? listing : article };
}

test("all-town runner writes a private durable ledger and reports only novel individual records", async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), "ep047-news-runner-"));
  const registryPath = path.join(root, "registry.json");
  const ledgerPath = path.join(root, "ledger.json");
  await writeFile(registryPath, JSON.stringify(registry));
  try {
    const first = await runAllTownCollection({ registryPath, ledgerPath, fetchPage: fixtureFetch, now: "2026-08-13T10:01:00.000Z" });
    assert.equal(first.summary.enabledSources, 1);
    assert.equal(first.summary.healthySources, 1);
    assert.equal(first.summary.newItems, 1);
    assert.equal(first.sources[0].newItems[0].headline, "Latest Manchester update");
    const ledger = JSON.parse(await readFile(ledgerPath, "utf8"));
    assert.equal(ledger.version, "ep047.news-last-seen/v2");
    assert.equal(Object.keys(ledger.sources).length, 1);
    const second = await runAllTownCollection({ registryPath, ledgerPath, fetchPage: fixtureFetch, now: "2026-08-13T10:02:00.000Z" });
    assert.equal(second.summary.newItems, 0);
    assert.equal(second.sources[0].newItems.length, 0);
  } finally { await rm(root, { recursive: true, force: true }); }
});

test("first ledger baseline records current items without falsely reporting historic records as new", async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), "ep047-news-runner-baseline-"));
  const registryPath = path.join(root, "registry.json");
  const ledgerPath = path.join(root, "ledger.json");
  await writeFile(registryPath, JSON.stringify(registry));
  try {
    const result = await runAllTownCollection({ registryPath, ledgerPath, fetchPage: fixtureFetch, now: "2026-08-13T10:01:00.000Z", baseline: true });
    assert.equal(result.summary.newItems, 0);
    assert.equal(result.sources[0].extractedItemCount, 1);
    assert.equal(result.sources[0].newItems.length, 0);
  } finally { await rm(root, { recursive: true, force: true }); }
});
test("all-town runner reports manual-review sources as coverage gaps without requesting them", async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), "ep047-news-runner-gap-"));
  const registryPath = path.join(root, "registry.json");
  const ledgerPath = path.join(root, "ledger.json");
  await writeFile(registryPath, JSON.stringify({ ...registry, sources: [...registry.sources, { town: "Penge", name: "Penge source", canonicalUrl: "https://penge.example/news", useMode: "manual_review" }] }));
  try {
    const result = await runAllTownCollection({ registryPath, ledgerPath, fetchPage: fixtureFetch });
    assert.equal(result.summary.manualReviewCoverageGaps, 1);
    assert.equal(result.manualReviewCoverageGaps[0].town, "Penge");
  } finally { await rm(root, { recursive: true, force: true }); }
});
