// JSON -> { columns, rows } for the pipeline. Accepts an array of flat
// objects — the brief's "future JSON imports" — using the same RawRow shape
// CSV produces so normalize.ts and pipeline.ts don't need to know the
// source format at all.

import type { ParsedFile } from "./csv";
import type { RawRow } from "./types";

export class JsonParseError extends Error {}

export function parseJson(content: string): ParsedFile {
  let parsed: unknown;
  try {
    parsed = JSON.parse(content);
  } catch (err) {
    throw new JsonParseError(err instanceof Error ? err.message : "Invalid JSON.");
  }

  if (!Array.isArray(parsed)) {
    throw new JsonParseError("Expected a JSON array of business records.");
  }

  const rows: RawRow[] = parsed.map((entry, index) => {
    if (typeof entry !== "object" || entry === null || Array.isArray(entry)) {
      throw new JsonParseError(`Record at index ${index} is not a flat object.`);
    }
    return entry as RawRow;
  });

  const columnSet = new Set<string>();
  for (const row of rows) {
    for (const key of Object.keys(row)) columnSet.add(key);
  }

  return { columns: [...columnSet], rows };
}
