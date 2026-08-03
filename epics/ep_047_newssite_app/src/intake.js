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
  return {
    version: batch.version,
    batchId: batch.batchId.trim(),
    items: batch.items.map((item) => ({
      itemId: item.itemId.trim(), headline: item.headline.trim(), town: item.town.trim(),
      sourceName: item.sourceName.trim(), sourceUrl: item.sourceUrl.trim(),
      verifiedUpdate: item.verifiedUpdate.trim(), localReading: item.localReading.trim(),
      businessVoices: typeof item.businessVoices === "string" ? item.businessVoices.trim() || undefined : undefined,
      eventIdentity: typeof item.eventIdentity === "string" ? item.eventIdentity.trim() || undefined : undefined,
      originalEventDate: typeof item.originalEventDate === "string" ? item.originalEventDate.trim() || undefined : undefined,
      sourcePublishedAt: item.sourcePublishedAt.trim(), dateProvenanceNote: item.dateProvenanceNote.trim(),
      dateConfidence: item.dateConfidence, dateSelectionRationale: item.dateSelectionRationale.trim(),
      selectedDateKind: item.selectedDateKind, categories: item.categories?.map((value) => value.trim()),
    })),
  };
}

function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.entries(value).sort(([a], [b]) => a.localeCompare(b))
      .map(([key, child]) => `${JSON.stringify(key)}:${canonicalJson(child)}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export function batchHash(batch) {
  return createHash("sha256").update(canonicalJson(batch)).digest("hex");
}
