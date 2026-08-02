import { createHash } from "node:crypto";
import path from "node:path";

export const NEWS_INTAKE_VERSION = "ep047.news-intake/v1" as const;

export type NewsIntakeItem = {
  itemId: string;
  headline: string;
  town: string;
  sourceName: string;
  sourceUrl: string;
  verifiedUpdate: string;
  localReading: string;
  businessVoices?: string;
  eventIdentity?: string;
  originalEventDate?: string;
  sourcePublishedAt: string;
  dateProvenanceNote: string;
  dateConfidence: "high" | "medium" | "low";
  dateSelectionRationale: string;
  selectedDateKind: "original_event" | "source_publication";
  categories?: string[];
};

export type NewsIntakeBatch = {
  version: typeof NEWS_INTAKE_VERSION;
  batchId: string;
  items: NewsIntakeItem[];
};

export const MAX_NEWS_INTAKE_ATTEMPTS = 3;

function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.entries(value as Record<string, unknown>).sort(([a], [b]) => a.localeCompare(b))
      .map(([key, child]) => `${JSON.stringify(key)}:${canonicalJson(child)}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export function contentHash(value: unknown): string {
  return createHash("sha256").update(canonicalJson(value)).digest("hex");
}

export function resolveNewsIntakeDirectory(applicationRoot = process.cwd()): string {
  return path.resolve(applicationRoot, "private", "news-intake");
}

export function nextRetryState(attempts: number): { status: "retryable" | "failed"; nextAttempt: number } {
  const safeAttempts = Math.max(1, Math.floor(attempts));
  return safeAttempts >= MAX_NEWS_INTAKE_ATTEMPTS
    ? { status: "failed", nextAttempt: MAX_NEWS_INTAKE_ATTEMPTS }
    : { status: "retryable", nextAttempt: safeAttempts + 1 };
}

const REQUIRED_TEXT_FIELDS = [
  "itemId", "headline", "town", "sourceName", "sourceUrl", "verifiedUpdate", "localReading",
  "sourcePublishedAt", "dateProvenanceNote", "dateConfidence", "dateSelectionRationale", "selectedDateKind",
] as const;

function object(value: unknown, message: string): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(message);
  return value as Record<string, unknown>;
}

function text(value: unknown, field: string): string {
  if (typeof value !== "string" || !value.trim()) throw new Error(`News intake ${field} must be a non-empty string.`);
  return value.trim();
}

export type NewsIntakeDecision = {
  status: "draft" | "review_required";
  duplicateState: "unique" | "review_required";
  reason: string | null;
};

function validIsoDate(value: string | undefined): boolean {
  if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T00:00:00.000Z`);
  return !Number.isNaN(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
}

export function decideNewsIntakeItem(item: NewsIntakeItem, matchingStatus: string | null): NewsIntakeDecision {
  const hasDateEvidence = validIsoDate(item.sourcePublishedAt)
    && (item.selectedDateKind === "source_publication" || validIsoDate(item.originalEventDate));
  if (!hasDateEvidence) return { status: "review_required", duplicateState: "unique", reason: "missing_date_evidence" };
  if (matchingStatus === "published") {
    return { status: "review_required", duplicateState: "review_required", reason: "matches_published_event" };
  }
  if (matchingStatus) return { status: "review_required", duplicateState: "review_required", reason: "matches_existing_event" };
  return { status: "draft", duplicateState: "unique", reason: null };
}

export function parseNewsIntakeBatch(raw: string): NewsIntakeBatch {
  let parsed: unknown;
  try { parsed = JSON.parse(raw); } catch { throw new Error("News intake batch is not valid JSON."); }
  const batch = object(parsed, "News intake batch must be an object.");
  if (batch.version !== NEWS_INTAKE_VERSION) throw new Error(`Unsupported news intake version: ${String(batch.version)}.`);
  const batchId = text(batch.batchId, "batchId");
  if (!Array.isArray(batch.items) || batch.items.length === 0 || batch.items.length > 100) {
    throw new Error("News intake items must contain 1 to 100 items.");
  }
  const itemIds = new Set<string>();
  const items = batch.items.map((candidate, index) => {
    const item = object(candidate, `News intake item ${index + 1} must be an object.`);
    if ("status" in item || "publishedAt" in item || "published_at" in item) {
      throw new Error("News intake item status and publication fields are forbidden.");
    }
    for (const field of REQUIRED_TEXT_FIELDS) text(item[field], field);
    const itemId = text(item.itemId, "itemId");
    if (itemIds.has(itemId)) throw new Error(`News intake batch contains duplicate itemId ${itemId}.`);
    itemIds.add(itemId);
    if (item.dateConfidence !== "high" && item.dateConfidence !== "medium" && item.dateConfidence !== "low") {
      throw new Error("News intake dateConfidence is invalid.");
    }
    if (item.selectedDateKind !== "original_event" && item.selectedDateKind !== "source_publication") {
      throw new Error("News intake selectedDateKind is invalid.");
    }
    if (item.categories !== undefined && (!Array.isArray(item.categories) || item.categories.some((value) => typeof value !== "string" || !value.trim()))) {
      throw new Error("News intake categories must be non-empty strings.");
    }
    const dateConfidence = item.dateConfidence as NewsIntakeItem["dateConfidence"];
    const selectedDateKind = item.selectedDateKind as NewsIntakeItem["selectedDateKind"];
    return {
      itemId, headline: text(item.headline, "headline"), town: text(item.town, "town"),
      sourceName: text(item.sourceName, "sourceName"), sourceUrl: text(item.sourceUrl, "sourceUrl"),
      verifiedUpdate: text(item.verifiedUpdate, "verifiedUpdate"), localReading: text(item.localReading, "localReading"),
      businessVoices: typeof item.businessVoices === "string" ? item.businessVoices.trim() || undefined : undefined,
      eventIdentity: typeof item.eventIdentity === "string" ? item.eventIdentity.trim() || undefined : undefined,
      originalEventDate: typeof item.originalEventDate === "string" ? item.originalEventDate.trim() || undefined : undefined,
      sourcePublishedAt: text(item.sourcePublishedAt, "sourcePublishedAt"),
      dateProvenanceNote: text(item.dateProvenanceNote, "dateProvenanceNote"),
      dateConfidence, dateSelectionRationale: text(item.dateSelectionRationale, "dateSelectionRationale"),
      selectedDateKind,
      categories: item.categories?.map((value) => String(value).trim()),
    };
  });
  return { version: NEWS_INTAKE_VERSION, batchId, items };
}
