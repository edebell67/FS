// Duplicate detection: exact match on email/phone/website, plus a normalized
// name+postcode match as a fuzzy stand-in until pg_trgm is wired up (PLAN.md
// §1 names pg_trgm as the production approach — this gets the same practical
// result for now without requiring the extension).
//
// Two passes: within the batch itself (so a CSV with the same business
// twice catches it before either row reaches the DB), then against existing
// records via an injected async lookup so this module has no DB dependency.

import type { BusinessInput } from "./types";

export interface DedupeKeys {
  email?: string;
  phone?: string;
  website?: string;
  /** Normalized business name, alnum-only lowercase. Always set (name is required). */
  namePart: string;
  /** Normalized postcode, whitespace stripped lowercase. Empty string if absent. */
  postcodePart: string;
}

export type ExistingLookup = (keys: DedupeKeys) => Promise<boolean> | boolean;

function normalizeEmail(value?: string): string | undefined {
  return value ? value.trim().toLowerCase() : undefined;
}

function normalizePhoneKey(value?: string): string | undefined {
  if (!value) return undefined;
  const digits = value.replace(/\D/g, "");
  return digits.length > 0 ? digits : undefined;
}

function normalizeWebsiteKey(value?: string): string | undefined {
  if (!value) return undefined;
  return value
    .trim()
    .toLowerCase()
    .replace(/^https?:\/\//, "")
    .replace(/^www\./, "")
    .replace(/\/+$/, "");
}

function normalizeNamePart(name: string): string {
  return name.trim().toLowerCase().replace(/[^a-z0-9]/g, "");
}

function normalizePostcodePart(postcode?: string): string {
  return (postcode ?? "").trim().toLowerCase().replace(/\s/g, "");
}

export function dedupeKeysFor(input: BusinessInput): DedupeKeys {
  return {
    email: normalizeEmail(input.email),
    phone: normalizePhoneKey(input.phone),
    website: normalizeWebsiteKey(input.website),
    namePart: normalizeNamePart(input.businessName),
    postcodePart: normalizePostcodePart(input.postcode),
  };
}

function keysCollide(a: DedupeKeys, b: DedupeKeys): boolean {
  if (a.email && b.email && a.email === b.email) return true;
  if (a.phone && b.phone && a.phone === b.phone) return true;
  if (a.website && b.website && a.website === b.website) return true;
  if (a.namePart && a.namePart === b.namePart && a.postcodePart === b.postcodePart) return true;
  return false;
}

export interface RowWithNumber {
  rowNumber: number;
  input: BusinessInput;
}

export interface DuplicateResult {
  /** row numbers found to duplicate an earlier row in the same batch */
  inBatch: number[];
  /** row numbers found to duplicate a record already in the database */
  existing: number[];
}

export async function detectDuplicates(
  rows: RowWithNumber[],
  existingLookup: ExistingLookup
): Promise<DuplicateResult> {
  const inBatch: number[] = [];
  const existing: number[] = [];
  const seenInBatch: DedupeKeys[] = [];

  for (const row of rows) {
    const keys = dedupeKeysFor(row.input);

    const batchDuplicate = seenInBatch.some((seen) => keysCollide(seen, keys));
    if (batchDuplicate) {
      inBatch.push(row.rowNumber);
      continue; // don't also check DB — it's already rejected
    }

    const existsInDb = await existingLookup(keys);
    if (existsInDb) {
      existing.push(row.rowNumber);
      continue;
    }

    seenInBatch.push(keys);
  }

  return { inBatch, existing };
}
