// The importer's orchestrator: raw rows in, an ImportSummary out. Same code
// path for CSV and JSON — each format's module (csv.ts, json.ts) only has to
// produce { columns, rows: RawRow[] } and hand it here.
//
// Order matters and is deliberate:
//   1. normalize + validate every row (independent of every other row)
//   2. dedupe the rows that passed validation (batch-internal, then DB)
//   3. reserve a business_ref only for rows that survive both — refs are a
//      scarce, gapless-per-category sequence; don't burn one on a row that
//      will be rejected anyway.
//
// A row's field-level warnings (see normalize.ts) are only reported if the
// row actually ends up accepted — a warning on a row that gets rejected for
// a missing required field, or dropped as a duplicate, is moot noise.

import { resolveColumns, normalizeRow } from "./normalize";
import { detectDuplicates, type ExistingLookup } from "./duplicates";
import { generateBusinessRef, type SequenceProvider } from "./business-ref";
import type { AcceptedRow, ImportSummary, RawRow, RowIssue } from "./types";

export interface RunImportOptions {
  columns: string[];
  rows: RawRow[];
  existingLookup: ExistingLookup;
  reserveNext: SequenceProvider;
}

export async function runImport(options: RunImportOptions): Promise<ImportSummary> {
  const { columns, rows, existingLookup, reserveNext } = options;
  const { recognized, unknown } = resolveColumns(columns);

  const rejected: RowIssue[] = [];
  const warningsByRow = new Map<number, RowIssue[]>();
  const survivors: Array<{ rowNumber: number; input: NonNullable<ReturnType<typeof normalizeRow>["input"]> }> = [];

  rows.forEach((row, index) => {
    const rowNumber = index + 1; // 1-indexed, matching what a user sees in a spreadsheet
    const result = normalizeRow(rowNumber, row, recognized);
    if (result.input) {
      survivors.push({ rowNumber, input: result.input });
      if (result.warnings.length > 0) warningsByRow.set(rowNumber, result.warnings);
    } else {
      rejected.push(...result.issues.map((issue) => ({ ...issue, kind: "rejected" as const })));
    }
  });

  const duplicateCheck = await detectDuplicates(survivors, existingLookup);
  const duplicateRowNumbers = new Set([...duplicateCheck.inBatch, ...duplicateCheck.existing]);

  const duplicates: RowIssue[] = [
    ...duplicateCheck.inBatch.map((rowNumber) => ({
      rowNumber,
      code: "duplicate_in_batch" as const,
      message: "Matches another row earlier in this same import.",
      kind: "duplicate" as const,
    })),
    ...duplicateCheck.existing.map((rowNumber) => ({
      rowNumber,
      code: "duplicate_existing" as const,
      message: "Matches a business already in the directory.",
      kind: "duplicate" as const,
    })),
  ];

  const accepted: AcceptedRow[] = [];
  const warnings: RowIssue[] = [];
  for (const survivor of survivors) {
    if (duplicateRowNumbers.has(survivor.rowNumber)) continue;
    const businessRef = await generateBusinessRef(survivor.input.category, reserveNext);
    accepted.push({ rowNumber: survivor.rowNumber, input: survivor.input, businessRef });

    const rowWarnings = warningsByRow.get(survivor.rowNumber);
    if (rowWarnings) {
      warnings.push(...rowWarnings.map((issue) => ({ ...issue, kind: "warning" as const })));
    }
  }

  return {
    totalRows: rows.length,
    accepted,
    rejected,
    duplicates,
    warnings,
    unknownColumns: unknown,
  };
}
