"use client";

import { CheckCircle2, AlertTriangle, Copy, FileWarning, Info } from "lucide-react";
import type { ImportApiResponse } from "@/lib/import/client-types";

export interface ImportSummaryCardProps {
  summary: ImportApiResponse;
  filename: string;
}

type Tone = "green" | "red" | "amber" | "slate" | "blue";

const TONE_CLASSES: Record<Tone, string> = {
  green: "text-green-600 bg-green-50",
  red: "text-red-600 bg-red-50",
  amber: "text-amber-600 bg-amber-50",
  slate: "text-slate-600 bg-slate-50",
  blue: "text-blue-600 bg-blue-50",
};

function StatTile({
  icon: Icon,
  label,
  value,
  tone,
}: {
  icon: typeof CheckCircle2;
  label: string;
  value: number;
  tone: Tone;
}) {

  return (
    <div className={`flex flex-col items-start gap-1 rounded-lg p-4 ${TONE_CLASSES[tone]}`}>
      <Icon className="h-5 w-5" aria-hidden="true" />
      <span className="text-2xl font-semibold tabular-nums">{value}</span>
      <span className="text-xs font-medium uppercase tracking-wide">{label}</span>
    </div>
  );
}

export function ImportSummaryCard({ summary, filename }: ImportSummaryCardProps) {
  return (
    <div className="rounded-xl border border-slate-200 p-5">
      <h2 className="mb-1 text-lg font-semibold text-slate-900">Import summary</h2>
      <p className="mb-4 text-sm text-slate-500">
        <span className="font-medium">{filename}</span> — batch{" "}
        <code className="rounded bg-slate-100 px-1 py-0.5 text-xs">{summary.batchId}</code>
      </p>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
        <StatTile icon={FileWarning} label="Total rows" value={summary.totalRows} tone="slate" />
        <StatTile icon={CheckCircle2} label="Accepted" value={summary.accepted} tone="green" />
        <StatTile icon={AlertTriangle} label="Rejected" value={summary.rejected} tone="red" />
        <StatTile icon={Copy} label="Duplicates" value={summary.duplicates} tone="amber" />
        <StatTile icon={Info} label="Warnings" value={summary.warnings} tone="blue" />
      </div>

      {summary.warnings > 0 && (
        <p className="mt-3 text-sm text-blue-700">
          {summary.warnings} field{summary.warnings === 1 ? "" : "s"} dropped for having an
          invalid value — those businesses were still imported, just without that field. See
          the error report below.
        </p>
      )}

      {summary.unknownColumns.length > 0 && (
        <p className="mt-2 text-sm text-amber-700">
          Unrecognized columns (ignored): {summary.unknownColumns.join(", ")}
        </p>
      )}
    </div>
  );
}
