// Top-level entry point: file content in, persisted businesses + an
// ImportSummary out. Wires together parse -> pipeline -> repository so API
// routes (and tests) call one function instead of re-deriving this order.

import { parseCsv, CsvParseError } from "./csv";
import { parseJson, JsonParseError } from "./json";
import { runImport } from "./pipeline";
import type { ImportRepository } from "./repository";
import type { ImportSource, ImportSummary } from "./types";

export { CsvParseError, JsonParseError };

export interface ImportFileOptions {
  filename: string;
  content: string;
  source: ImportSource;
  uploadedBy?: string;
  repository: ImportRepository;
}

export interface ImportFileResult {
  batchId: string;
  summary: ImportSummary;
}

export async function importFile(options: ImportFileOptions): Promise<ImportFileResult> {
  const { filename, content, source, uploadedBy, repository } = options;

  const parsed = source === "csv" ? parseCsv(content) : parseJson(content);

  const batchId = await repository.createBatch(filename, source, uploadedBy);

  const summary = await runImport({
    columns: parsed.columns,
    rows: parsed.rows,
    existingLookup: (keys) => repository.existingLookup(keys),
    reserveNext: (categoryCode) => repository.reserveNext(categoryCode),
  });

  await repository.insertAccepted(batchId, source, summary.accepted);

  const allIssues = [...summary.rejected, ...summary.duplicates, ...summary.warnings];
  await repository.recordErrors(batchId, allIssues);

  await repository.completeBatch(batchId, {
    total: summary.totalRows,
    accepted: summary.accepted.length,
    rejected: summary.rejected.length,
    duplicates: summary.duplicates.length,
  });

  return { batchId, summary };
}
