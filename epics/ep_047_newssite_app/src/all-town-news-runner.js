import { createHash } from "node:crypto";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import path from "node:path";
import { collectSourceItems } from "./all-town-news-collector.js";

function sourceId(source) {
  return createHash("sha256").update(new URL(source.canonicalUrl).toString()).digest("hex").slice(0, 24);
}

function normalizedSource(source) {
  const canonicalUrl = new URL(source.canonicalUrl).toString();
  return { ...source, id: source.id || sourceId(source), canonicalUrl, allowedHosts: source.allowedHosts || [new URL(canonicalUrl).hostname.toLowerCase()] };
}

async function loadJson(file, fallback) {
  try { return JSON.parse(await readFile(file, "utf8")); } catch (error) {
    if (error?.code === "ENOENT") return fallback;
    throw error;
  }
}

function emptyLedger(registryVersion, now) {
  return { version: "ep047.news-last-seen/v2", registryVersion, updatedAt: now, sources: {} };
}

function seenFor(ledger, id) {
  return new Set(Object.keys(ledger.sources?.[id]?.seen || {}));
}

function recordSeen(ledger, source, items, now) {
  const prior = ledger.sources[source.id] || { canonicalUrl: source.canonicalUrl, seen: {} };
  const seen = { ...prior.seen };
  for (const item of items) {
    const existing = seen[item.identity];
    seen[item.identity] = { firstSeenAt: existing?.firstSeenAt || now, lastSeenAt: now, sourcePublishedAt: item.sourcePublishedAt };
  }
  ledger.sources[source.id] = { canonicalUrl: source.canonicalUrl, seen };
}

async function writeJsonAtomically(file, value) {
  await mkdir(path.dirname(file), { recursive: true });
  const temp = `${file}.${process.pid}.tmp`;
  await writeFile(temp, `${JSON.stringify(value, null, 2)}\n`, "utf8");
  await rename(temp, file);
}

/** Private-only all-town collection. It never writes an intake batch or contacts a receiver. */
export async function runAllTownCollection({ registryPath, ledgerPath, fetchPage, now = new Date().toISOString(), maxCandidates = 24, writeLedger = true, baseline = false }) {
  const registry = await loadJson(registryPath);
  if (!registry || registry.version !== "ep047.all-town-news-sources/v1" || !Array.isArray(registry.sources)) throw new Error("Invalid all-town source registry.");
  const ledger = await loadJson(ledgerPath, emptyLedger(registry.version, now));
  if (ledger.version !== "ep047.news-last-seen/v2") throw new Error("Invalid durable news last-seen ledger.");
  const enabled = registry.sources.filter((source) => source.useMode === "enabled").map(normalizedSource);
  const manualReviewCoverageGaps = registry.sources.filter((source) => source.useMode === "manual_review").map((source) => ({ town: source.town, name: source.name, canonicalUrl: source.canonicalUrl, reason: "Manual review source is excluded from unattended retrieval." }));
  const sources = [];
  for (const source of enabled) {
    const collected = await collectSourceItems(source, { fetchPage, maxCandidates });
    const seen = seenFor(ledger, source.id);
    const newItems = baseline ? [] : (collected.items || []).filter((item) => !seen.has(item.identity));
    if (collected.status === "healthy") recordSeen(ledger, source, collected.items, now);
    sources.push({ sourceId: source.id, town: source.town, name: source.name, canonicalUrl: source.canonicalUrl, status: collected.status, candidateCount: collected.candidateCount || 0, extractedItemCount: collected.items?.length || 0, newItems, reason: collected.reason || null });
  }
  ledger.updatedAt = now;
  ledger.registryVersion = registry.version;
  if (writeLedger) await writeJsonAtomically(ledgerPath, ledger);
  const summary = { enabledSources: enabled.length, healthySources: sources.filter((source) => source.status === "healthy").length, degradedSources: sources.filter((source) => source.status === "degraded").length, blockedSources: sources.filter((source) => source.status === "blocked").length, newItems: sources.reduce((total, source) => total + source.newItems.length, 0), manualReviewCoverageGaps: manualReviewCoverageGaps.length, deliveryAttempted: false, intakeBatchCreated: false, publicContentCreated: false };
  return { version: "ep047.all-town-news-collection/v1", collectedAt: now, registryVersion: registry.version, summary, sources, manualReviewCoverageGaps };
}
