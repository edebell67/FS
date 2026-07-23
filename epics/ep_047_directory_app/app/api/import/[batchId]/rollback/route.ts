import { NextResponse } from "next/server";
import { DrizzleImportRepository } from "@/lib/import/repository";

export const dynamic = "force-dynamic";

// Rolls back a single import batch: deletes every business it created
// (and, via FK cascade, their stage_transitions) and marks the batch
// rolled_back. This is the brief's "Rollback" requirement for the CSV
// importer — scoped to one batch by design, so rolling back a bad upload
// never touches businesses from any other import.
export async function POST(
  _request: Request,
  { params }: { params: Promise<{ batchId: string }> }
) {
  const { batchId } = await params;
  const repository = new DrizzleImportRepository();
  try {
    const deletedCount = await repository.rollbackBatch(batchId);
    return NextResponse.json({ batchId, deletedCount });
  } catch (err) {
    console.error("Rollback failed:", err);
    return NextResponse.json({ error: "Rollback failed. See server logs." }, { status: 500 });
  }
}
