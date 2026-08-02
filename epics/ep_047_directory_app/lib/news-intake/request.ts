import { timingSafeEqual } from "node:crypto";
import { contentHash, parseNewsIntakeBatch, type NewsIntakeBatch } from "@/lib/news-intake/importer";

export type NewsIntakeDeliveryValidation =
  | { ok: true; batch: NewsIntakeBatch }
  | { ok: false; status: 400 | 401; error: string };

function matchesSecret(provided: string | undefined, configured: string | undefined): boolean {
  if (!configured || !provided) return false;
  const actual = Buffer.from(provided);
  const expected = Buffer.from(configured);
  return actual.length === expected.length && timingSafeEqual(actual, expected);
}

export function validateNewsIntakeDelivery({
  raw,
  authorization,
  batchHash,
  configuredApiKey,
}: {
  raw: string;
  authorization: string | null;
  batchHash: string | null;
  configuredApiKey: string | undefined;
}): NewsIntakeDeliveryValidation {
  const providedKey = authorization?.replace(/^Bearer\s+/i, "").trim();
  if (!matchesSecret(providedKey, configuredApiKey?.trim())) {
    return { ok: false, status: 401, error: "Not authenticated." };
  }

  let batch: NewsIntakeBatch;
  try {
    batch = parseNewsIntakeBatch(raw);
  } catch {
    return { ok: false, status: 400, error: "Invalid news intake batch." };
  }
  if (!batchHash || !matchesSecret(batchHash.trim(), contentHash(batch))) {
    return { ok: false, status: 400, error: "Invalid news batch hash." };
  }
  return { ok: true, batch };
}
