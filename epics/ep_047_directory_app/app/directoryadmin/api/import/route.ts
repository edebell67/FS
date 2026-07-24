import { NextResponse } from "next/server";
import { importFile, CsvParseError, JsonParseError } from "@/lib/import/import-file";
import { DrizzleImportRepository } from "@/lib/import/repository";
import type { ImportSource } from "@/lib/import/types";

export const dynamic = "force-dynamic";

// Accepts a multipart upload: { file: File, source?: "csv" | "json" }.
// Source defaults to inferring from the file extension. Runs the import
// inline for now — Phase 2's "progress bar for large files" note in
// PLAN.md means this moves to the jobs-table worker once imports
// regularly exceed a few thousand rows; for now this is synchronous and
// returns the full summary in the response.
export async function POST(request: Request) {
  let formData: FormData;
  try {
    formData = await request.formData();
  } catch {
    return NextResponse.json({ error: "Expected multipart/form-data with a file field." }, { status: 400 });
  }

  const file = formData.get("file");
  if (!(file instanceof File)) {
    return NextResponse.json({ error: "Missing file." }, { status: 400 });
  }

  const declaredSource = formData.get("source");
  const source: ImportSource =
    declaredSource === "json" || file.name.toLowerCase().endsWith(".json") ? "json" : "csv";

  const content = await file.text();

  try {
    const { batchId, summary } = await importFile({
      filename: file.name,
      content,
      source,
      repository: new DrizzleImportRepository(),
    });

    return NextResponse.json({
      batchId,
      totalRows: summary.totalRows,
      accepted: summary.accepted.length,
      rejected: summary.rejected.length,
      duplicates: summary.duplicates.length,
      warnings: summary.warnings.length,
      unknownColumns: summary.unknownColumns,
      errors: [...summary.rejected, ...summary.duplicates, ...summary.warnings],
    });
  } catch (err) {
    if (err instanceof CsvParseError || err instanceof JsonParseError) {
      return NextResponse.json({ error: err.message }, { status: 422 });
    }
    console.error("Import failed:", err);
    return NextResponse.json({ error: "Import failed. See server logs." }, { status: 500 });
  }
}
