// Generates the permanent business_ref, e.g. TP-PLUMB-000001.
//
// Format: {PREFIX}-{CATEGORY_CODE}-{6-digit sequence, gapless per category}.
// The sequence is reserved through an injected provider so callers can back
// it with a real `category_sequences` row (UPDATE ... RETURNING inside the
// insert transaction — see PLAN.md §2) in production, or an in-memory map in
// tests.

const REF_PREFIX = "TP"; // TheTechPrinciple — matches the brief's example.

/** Turns a free-text category into a stable ~5-char uppercase code. */
export function deriveCategoryCode(category: string): string {
  const cleaned = category
    .trim()
    .toUpperCase()
    .replace(/[^A-Z0-9]/g, "");
  if (cleaned.length === 0) return "GEN"; // "general" fallback for blank/symbolic categories
  return cleaned.slice(0, 5);
}

export type SequenceProvider = (categoryCode: string) => Promise<number> | number;

export async function generateBusinessRef(
  category: string,
  reserveNext: SequenceProvider
): Promise<string> {
  const categoryCode = deriveCategoryCode(category);
  const sequence = await reserveNext(categoryCode);
  const padded = String(sequence).padStart(6, "0");
  return `${REF_PREFIX}-${categoryCode}-${padded}`;
}

/** In-memory sequence provider — for tests and for scripts that don't touch the DB. */
export function createInMemorySequenceProvider(): SequenceProvider {
  const counters = new Map<string, number>();
  return (categoryCode: string) => {
    const next = (counters.get(categoryCode) ?? 0) + 1;
    counters.set(categoryCode, next);
    return next;
  };
}
