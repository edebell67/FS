import { createHash } from "node:crypto";

function plain(value = "") {
  return value.replace(/<[^>]*>/g, " ").replace(/&(?:amp|#38);/gi, "&").replace(/&(?:#39|apos);/gi, "'").replace(/&quot;/gi, '"').replace(/\s+/g, " ").trim();
}

function attribute(tag, name) {
  const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const doubleQuoted = tag.match(new RegExp(`${escaped}\\s*=\\s*"([^"]*)"`, "i"));
  if (doubleQuoted) return doubleQuoted[1];
  const singleQuoted = tag.match(new RegExp(`${escaped}\\s*=\\s*'([^']*)'`, "i"));
  return singleQuoted?.[1] || "";
}

function meta(html, property) {
  const tags = html.match(/<meta\b[^>]*>/gi) || [];
  for (const tag of tags) {
    const key = attribute(tag, "property") || attribute(tag, "name");
    if (key.toLowerCase() === property.toLowerCase()) return plain(attribute(tag, "content"));
  }
  return "";
}

function normalizeUrl(value, fallback) {
  const url = new URL(value, fallback);
  url.hash = "";
  return url.toString();
}

function canonicalUrl(html, fallback) {
  const tags = html.match(/<link\b[^>]*>/gi) || [];
  const canonical = tags.find((tag) => /\brel=["']canonical["']/i.test(tag));
  const href = canonical ? attribute(canonical, "href") : "";
  return normalizeUrl(href || fallback, fallback);
}

function dateOnly(value) {
  const match = String(value || "").match(/^(20\d{2})-(\d{2})-(\d{2})/);
  if (!match) return "";
  const [, year, month, day] = match;
  const parsed = new Date(`${year}-${month}-${day}T00:00:00.000Z`);
  return parsed.getUTCFullYear() === Number(year) && parsed.getUTCMonth() + 1 === Number(month) && parsed.getUTCDate() === Number(day) ? `${year}-${month}-${day}` : "";
}

function allowed(source, url) {
  const host = new URL(url).hostname.toLowerCase();
  return (source.allowedHosts || []).some((entry) => host === String(entry).toLowerCase());
}

function listingLinks(html, listingUrl, source) {
  const links = new Map();
  const articleBlocks = html.match(/<article\b[\s\S]*?<\/article>/gi) || [];
  for (const block of articleBlocks) {
    const match = block.match(/<a\b[^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/i);
    if (!match) continue;
    const headline = plain(match[2]);
    if (!headline || headline.length < 8) continue;
    let url;
    try { url = normalizeUrl(match[1], listingUrl); } catch { continue; }
    if (!allowed(source, url) || url === listingUrl || /^(mailto:|tel:|javascript:)/i.test(url)) continue;
    links.set(url, headline);
  }
  return [...links].map(([url, headline]) => ({ url, listingHeadline: headline }));
}

async function nativeFetchPage(url) {
  const response = await fetch(url, { headers: { "user-agent": "TTPNewsCollection/1.0 (+https://thetechprinciple.com/)" }, redirect: "follow", signal: AbortSignal.timeout(30_000) });
  return { url: response.url, status: response.status, html: await response.text() };
}

/** Extract allowed, individually dated article records from one approved listing endpoint. */
export async function collectSourceItems(source, { fetchPage = nativeFetchPage, maxCandidates = 24 } = {}) {
  let listing;
  try { listing = await fetchPage(source.canonicalUrl); } catch (error) { return { status: "blocked", items: [], reason: error instanceof Error ? error.message : "Listing request failed." }; }
  if (listing.status < 200 || listing.status >= 300) return { status: "blocked", items: [], reason: `Listing returned HTTP ${listing.status}.` };
  if (!allowed(source, listing.url)) return { status: "degraded", items: [], reason: "Listing redirected outside its allowed host." };
  const candidates = listingLinks(listing.html, listing.url, source).slice(0, maxCandidates);
  const items = [];
  for (const candidate of candidates) {
    let page;
    try { page = await fetchPage(candidate.url); } catch { continue; }
    if (page.status < 200 || page.status >= 300 || !allowed(source, page.url)) continue;
    let canonical;
    try { canonical = canonicalUrl(page.html, page.url); } catch { continue; }
    if (!allowed(source, canonical) || canonical === listing.url) continue;
    const headline = meta(page.html, "og:title") || plain((page.html.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/i) || [])[1]) || candidate.listingHeadline;
    const sourcePublishedAt = dateOnly(meta(page.html, "article:published_time")) || dateOnly(meta(page.html, "date")) || dateOnly((page.html.match(/<time\b[^>]*datetime=["']([^"']+)/i) || [])[1]);
    if (!headline || !sourcePublishedAt) continue;
    items.push({ identity: canonical, canonicalUrl: canonical, headline, sourcePublishedAt, allowedHost: true });
  }
  if (!items.length) return { status: "degraded", items: [], candidateCount: candidates.length, reason: "No individually dated article records could be established from the approved listing." };
  return { status: "healthy", items, candidateCount: candidates.length };
}

/** Select only identities absent from the durable per-source local ledger. */
export function selectNovelItems(sourceId, items, ledger) {
  const seen = new Set(ledger?.sources?.[sourceId] || []);
  return { comparedCount: seen.size, newItems: items.filter((item) => !seen.has(item.identity)) };
}

export function updateLedger(ledger, sourceId, items, collectedAt = new Date().toISOString()) {
  const current = new Set(ledger?.sources?.[sourceId] || []);
  for (const item of items) current.add(item.identity);
  return { version: "ep047.news-last-seen/v1", updatedAt: collectedAt, sources: { ...(ledger?.sources || {}), [sourceId]: [...current].sort() } };
}

export function itemId(sourceId, identity) {
  return `${sourceId}:${createHash("sha256").update(identity).digest("hex").slice(0, 20)}`;
}
