// CSV -> { columns, rows } for the pipeline. Uses csv-parse's sync API since
// imports run inside a job (see PLAN.md Phase 2 — the API route hands off to
// a job row, not a request-lifetime parse) rather than a streaming HTTP
// response; sync keeps the error-handling straightforward for now.

import { parse } from "csv-parse/sync";
import type { RawRow } from "./types";

export interface ParsedFile {
  columns: string[];
  rows: RawRow[];
}

export class CsvParseError extends Error {}

export function parseCsv(content: string): ParsedFile {
  let records: Record<string, string>[];
  try {
    records = parse(content, {
      columns: true,
      skip_empty_lines: true,
      trim: true,
      bom: true,
    });
  } catch (err) {
    throw new CsvParseError(err instanceof Error ? err.message : "Failed to parse CSV.");
  }

  const [firstRecord] = records;
  if (!firstRecord) {
    return { columns: [], rows: [] };
  }

  const columns = Object.keys(firstRecord);
  return { columns, rows: records };
}
