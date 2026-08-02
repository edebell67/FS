import { createHash } from "node:crypto";

export const VERSION = "ep047.news-intake/v1";
const REQUIRED = ["itemId", "headline", "town", "sourceName", "sourceUrl", "verifiedUpdate", "localReading", "sourcePublishedAt", "dateProvenanceNote", "dateConfidence", "dateSelectionRationale", "selectedDateKind"];

export function parseBatch(raw) {
  const batch = JSON.parse(raw);
  if (!batch || typeof batch !== "object" || batch.version !== VERSION || typeof batch.batchId !== "string" || !Array.isArray(batch.items) || !batch.items.length) throw new Error("Invalid EP047 private News intake batch.");
  const ids = new Set();
  for (const item of batch.items) {
    if (!item || typeof item !== "object" || "status" in item || "publishedAt" in item || "published_at" in item) throw new Error("Publication fields are forbidden in intake.");
    for (const field of REQUIRED) if (typeof item[field] !== "string" || !item[field].trim()) throw new Error(`Missing ${field}.`);
    if (ids.has(item.itemId)) throw new Error(`Duplicate itemId ${item.itemId}.`);
    ids.add(item.itemId);
    if (!["high", "medium", "low"].includes(item.dateConfidence)) throw new Error("Invalid dateConfidence.");
    if (!["original_event", "source_publication"].includes(item.selectedDateKind)) throw new Error("Invalid selectedDateKind.");
  }
  return batch;
}

export function batchHash(batch) {
  return createHash("sha256").update(JSON.stringify(batch)).digest("hex");
}
