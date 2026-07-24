"use client";

import { useCallback, useState } from "react";
import Link from "next/link";
import { RefreshCw } from "lucide-react";
import { Dropzone } from "@/components/import/Dropzone";
import { ProgressBar } from "@/components/import/ProgressBar";
import { ImportSummaryCard } from "@/components/import/ImportSummaryCard";
import { ErrorReportTable } from "@/components/import/ErrorReportTable";
import { RollbackControl } from "@/components/import/RollbackControl";
import type { ImportApiError, ImportApiResponse } from "@/lib/import/client-types";

type Phase =
  | { status: "idle" }
  | { status: "uploading"; filename: string; percent: number }
  | { status: "processing"; filename: string }
  | { status: "done"; filename: string; summary: ImportApiResponse }
  | { status: "error"; filename: string; message: string };

/**
 * Uses XMLHttpRequest (not fetch) specifically to get real upload-progress
 * events for the drag-and-drop progress bar the brief asks for. Once the
 * upload itself hits 100%, the request is still open while the server runs
 * the import synchronously (see app/api/import/route.ts) — that gap is
 * surfaced as the indeterminate "processing" phase below, since there's no
 * server-push progress channel until imports move to the jobs-table worker
 * (PLAN.md Phase 2 note).
 */
function uploadFile(
  file: File,
  onProgress: (percent: number) => void
): Promise<ImportApiResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append("file", file);

    xhr.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable) {
        onProgress((event.loaded / event.total) * 100);
      }
    });

    xhr.addEventListener("load", () => {
      let body: unknown;
      try {
        body = JSON.parse(xhr.responseText);
      } catch {
        reject(new Error("Server returned an invalid response."));
        return;
      }

      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(body as ImportApiResponse);
      } else {
        reject(new Error((body as ImportApiError).error ?? `Import failed (${xhr.status}).`));
      }
    });

    xhr.addEventListener("error", () => reject(new Error("Network error during upload.")));

    xhr.open("POST", "/directoryadmin/api/import");
    xhr.send(formData);
  });
}

export default function ImportPageClient() {
  const [phase, setPhase] = useState<Phase>({ status: "idle" });

  const handleFileSelected = useCallback(async (file: File) => {
    setPhase({ status: "uploading", filename: file.name, percent: 0 });

    try {
      const summary = await uploadFile(file, (percent) => {
        setPhase((prev) =>
          prev.status === "uploading" ? { ...prev, percent } : prev
        );
        if (percent >= 100) {
          setPhase({ status: "processing", filename: file.name });
        }
      });
      setPhase({ status: "done", filename: file.name, summary });
    } catch (err) {
      setPhase({
        status: "error",
        filename: file.name,
        message: err instanceof Error ? err.message : "Import failed.",
      });
    }
  }, []);

  const isBusy = phase.status === "uploading" || phase.status === "processing";

  return (
    <main className="mx-auto max-w-3xl px-6 py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">
        Admin — Import
      </p>
      <div className="mt-1 flex items-baseline justify-between">
        <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Import businesses</h1>
        <Link href="/directoryadmin/businesses" className="text-sm font-medium text-brand-600 hover:text-brand-700">
          Browse businesses →
        </Link>
      </div>
      <p className="mt-2 text-slate-600">
        Upload a CSV or JSON file. Every row is validated, checked for duplicates, and — if it
        passes — assigned a permanent business ID and dropped onto the{" "}
        <span className="font-medium">Imported</span> pipeline stage.
      </p>

      <div className="mt-8 space-y-6">
        <Dropzone onFileSelected={handleFileSelected} disabled={isBusy} />

        {phase.status === "uploading" && (
          <ProgressBar percent={phase.percent} label={`Uploading ${phase.filename}…`} />
        )}

        {phase.status === "processing" && (
          <ProgressBar label={`Validating and importing ${phase.filename}…`} />
        )}

        {phase.status === "error" && (
          <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
            Failed to import <span className="font-medium">{phase.filename}</span>:{" "}
            {phase.message}
          </div>
        )}

        {phase.status === "done" && (
          <>
            <ImportSummaryCard summary={phase.summary} filename={phase.filename} />
            <div>
              <h2 className="mb-2 text-lg font-semibold text-slate-900">Error report</h2>
              <ErrorReportTable errors={phase.summary.errors} />
            </div>
            <div className="flex items-center justify-between border-t border-slate-200 pt-4">
              <RollbackControl batchId={phase.summary.batchId} acceptedCount={phase.summary.accepted} />
              <button
                onClick={() => setPhase({ status: "idle" })}
                className="inline-flex items-center gap-1.5 text-sm font-medium text-brand-600 hover:text-brand-700"
              >
                <RefreshCw className="h-4 w-4" aria-hidden="true" />
                Import another file
              </button>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
