"use client";

import type { RowIssue } from "@/lib/import/types";

export interface ErrorReportTableProps {
  errors: RowIssue[];
}

function badgeClass(kind: RowIssue["kind"]): string {
  switch (kind) {
    case "duplicate":
      return "bg-amber-50 text-amber-700";
    case "warning":
      return "bg-blue-50 text-blue-700";
    case "rejected":
    default:
      return "bg-red-50 text-red-700";
  }
}

function outcomeLabel(kind: RowIssue["kind"]): string {
  return kind === "warning" ? "Imported" : "Not imported";
}

function outcomeClass(kind: RowIssue["kind"]): string {
  return kind === "warning" ? "text-green-700" : "text-slate-500";
}

const CODE_LABELS: Record<string, string> = {
  missing_required_field: "Missing required field",
  invalid_email: "Invalid email",
  invalid_website: "Invalid website",
  invalid_phone: "Invalid phone",
  invalid_number: "Invalid number",
  unknown_column: "Unknown column",
  duplicate_in_batch: "Duplicate in this file",
  duplicate_existing: "Duplicate of existing business",
};

export function ErrorReportTable({ errors }: ErrorReportTableProps) {
  if (errors.length === 0) {
    return (
      <p className="rounded-lg bg-green-50 px-4 py-3 text-sm text-green-700">
        Every row was accepted — nothing to report.
      </p>
    );
  }

  const sorted = [...errors].sort((a, b) => a.rowNumber - b.rowNumber);

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-4 py-2 font-medium">Row</th>
            <th className="px-4 py-2 font-medium">Outcome</th>
            <th className="px-4 py-2 font-medium">Column</th>
            <th className="px-4 py-2 font-medium">Value</th>
            <th className="px-4 py-2 font-medium">Issue</th>
            <th className="px-4 py-2 font-medium">Message</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {sorted.map((issue, index) => (
            <tr key={`${issue.rowNumber}-${issue.column ?? "row"}-${index}`}>
              <td className="whitespace-nowrap px-4 py-2 tabular-nums">{issue.rowNumber}</td>
              <td className={`whitespace-nowrap px-4 py-2 text-xs font-medium ${outcomeClass(issue.kind)}`}>
                {outcomeLabel(issue.kind)}
              </td>
              <td className="whitespace-nowrap px-4 py-2 text-slate-600">{issue.column ?? "—"}</td>
              <td className="max-w-[16rem] truncate px-4 py-2 text-slate-500">
                {issue.rawValue ?? "—"}
              </td>
              <td className="whitespace-nowrap px-4 py-2">
                <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${badgeClass(issue.kind)}`}>
                  {CODE_LABELS[issue.code] ?? issue.code}
                </span>
              </td>
              <td className="px-4 py-2 text-slate-600">{issue.message}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
