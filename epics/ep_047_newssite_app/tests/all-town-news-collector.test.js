import assert from "node:assert/strict";
import test from "node:test";
import { collectSourceItems, selectNovelItems } from "../src/all-town-news-collector.js";

const source = {
  id: "cityco-manchester-news",
  town: "Manchester",
  name: "CityCo Manchester — News & Podcasts",
  canonicalUrl: "https://cityco.com/news/",
  allowedHosts: ["cityco.com"],
};

const listingHtml = `
  <article><a href="/news/newest-story/">Newest story</a></article>
  <article><a href="https://cityco.com/news/older-story/">Older story</a></article>
  <a href="https://other.example/news/not-allowed">Ignore external</a>`;
const pages = {
  "https://cityco.com/news/newest-story/": `<html><head><link rel="canonical" href="https://cityco.com/news/newest-story/"><meta property="og:title" content="Manchester's newest verified update"><meta property="article:published_time" content="2026-08-12T08:26:59+00:00"></head><body><p>Verified source text.</p></body></html>`,
  "https://cityco.com/news/older-story/": `<html><head><meta property="og:title" content="Older update"><meta property="article:published_time" content="2026-07-14T18:20:56+00:00"></head></html>`,
};

const fetchPage = async (url) => {
  if (url === source.canonicalUrl) return { url, status: 200, html: listingHtml };
  if (!pages[url]) throw new Error(`Unexpected candidate URL: ${url}`);
  return { url, status: 200, html: pages[url] };
};

test("collector follows allowed article links and records canonical URL, headline and source date", async () => {
  const result = await collectSourceItems(source, { fetchPage });
  assert.equal(result.status, "healthy");
  assert.equal(result.items.length, 2);
  assert.deepEqual(result.items[0], {
    identity: "https://cityco.com/news/newest-story/",
    canonicalUrl: "https://cityco.com/news/newest-story/",
    headline: "Manchester's newest verified update",
    sourcePublishedAt: "2026-08-12",
    allowedHost: true,
  });
});

test("collector rejects undated article records rather than treating a listing response as coverage", async () => {
  const result = await collectSourceItems(source, { fetchPage: async (url) => ({ url, status: 200, html: url === source.canonicalUrl ? listingHtml : "<html><head><title>No date</title></head></html>" }) });
  assert.equal(result.status, "degraded");
  assert.equal(result.items.length, 0);
  assert.match(result.reason, /dated article/i);
});

test("collector rejects article records whose canonical URL is the listing itself", async () => {
  const result = await collectSourceItems(source, { fetchPage: async (url) => ({ url, status: 200, html: url === source.canonicalUrl ? '<article><a href="/news/category/">Category</a></article>' : '<html><head><link rel="canonical" href="https://cityco.com/news/"><meta property="og:title" content="News listing"><meta property="article:published_time" content="2026-08-12T00:00:00Z"></head></html>' }) });
  assert.equal(result.status, "degraded");
  assert.equal(result.items.length, 0);
});
test("novelty ledger selection only admits identities not already seen for this source", () => {
  const items = [
    { identity: "https://cityco.com/news/newest-story/" },
    { identity: "https://cityco.com/news/older-story/" },
  ];
  const result = selectNovelItems("cityco-manchester-news", items, { sources: { "cityco-manchester-news": ["https://cityco.com/news/older-story/"] } });
  assert.deepEqual(result.newItems.map((item) => item.identity), ["https://cityco.com/news/newest-story/"]);
  assert.equal(result.comparedCount, 1);
});
