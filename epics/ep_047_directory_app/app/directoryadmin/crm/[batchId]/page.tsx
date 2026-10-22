/**
 * app/directoryadmin/crm/[batchId]/page.tsx — EP043 CRM: batch detail.
 * Pipeline distribution (report 2.2), response % (report 2.3), and a
 * business list linking into the drill-down (report 2.4, on the business
 * detail page's "Outreach responses" section).
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-10 · Initial version.
 */
import Link from "next/link";
import { notFound } from "next/navigation";
import { format } from "date-fns";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import {
  getBatchBusinesses, getBatchPipelineDistribution, getBatchResponseStats,
} from "@/lib/db/queries/crm";
import { getVerificationBatch } from "@/lib/verification/batches";

export const dynamic = "force-dynamic";

function StageBar({ label, count, max, isTerminal }: { label: string; count: number; max: number; isTerminal: boolean }) {
  const width = max > 0 ? Math.max((count / max) * 100, count > 0 ? 3 : 0) : 0;
  return (
    <div className="flex items-center gap-3 text-sm">
      <span className="w-48 shrink-0 truncate text-slate-600">{label}</span>
      <div className="h-4 flex-1 overflow-hidden rounded bg-slate-100">
        <div
          className={`h-full rounded ${isTerminal ? "bg-slate-400" : "bg-brand-500"}`}
          style={{ width: `${width}%` }}
        />
      </div>
      <span className="w-10 shrink-0 text-right tabular-nums text-slate-900">{count}</span>
    </div>
  );
}

function fmtPct(value: number | null): string {
  return value === null ? "—" : `${Math.round(value)}%`;
}

export default async function CrmBatchDetailPage({ params }: { params: Promise<{ batchId: string }> }) {
  const { batchId } = await params;
  const user = await requireAdminUserForPage(`/directoryadmin/crm/${batchId}`);
  if (!canManageVerification(user.role)) notFound();

  const batch = await getVerificationBatch(batchId);
  if (!batch) notFound();

  const [distribution, responseStats, batchBusinesses] = await Promise.all([
    getBatchPipelineDistribution(batchId),
    getBatchResponseStats(batchId),
    getBatchBusinesses(batchId),
  ]);

  const maxStageCount = Math.max(1, ...distribution.map((s) => s.count));

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — CRM</p>
      <div className="mt-1 flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
        <h1 className="text-2xl font-semibold">Batch report</h1>
        <Link href="/directoryadmin/crm" className="text-sm font-medium text-brand-600 hover:text-brand-700">← All batches</Link>
      </div>
      <p className="mt-2 font-mono text-xs text-slate-500">{batch.id}</p>

      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div className="rounded-xl border border-slate-200 p-4">
          <p className="text-2xl font-semibold tabular-nums text-slate-900">{responseStats.sentCount}</p>
          <p className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-500">Sent</p>
        </div>
        <div className="rounded-xl border border-slate-200 p-4">
          <p className="text-2xl font-semibold tabular-nums text-slate-900">{responseStats.responseCount}</p>
          <p className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-500">Responses ({fmtPct(responseStats.responseRate)})</p>
        </div>
        <div className="rounded-xl border border-slate-200 p-4">
          <p className="text-2xl font-semibold tabular-nums text-brand-600">{responseStats.positiveCount}</p>
          <p className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-500">Positive ({fmtPct(responseStats.positiveRate)})</p>
        </div>
        <div className="rounded-xl border border-slate-200 p-4">
          <p className="text-2xl font-semibold tabular-nums text-slate-900">{batch.totalCount}</p>
          <p className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-500">Businesses in batch</p>
        </div>
      </div>

      <h2 className="mb-3 mt-10 text-lg font-semibold text-slate-900">Pipeline status distribution</h2>
      {distribution.length === 0 ? (
        <p className="text-sm text-slate-500">No businesses with a pipeline stage in this batch yet.</p>
      ) : (
        <div className="space-y-2 rounded-xl border border-slate-200 p-4">
          {distribution.map((stage) => (
            <StageBar key={stage.stageKey} label={stage.stageLabel} count={stage.count} max={maxStageCount} isTerminal={stage.isTerminal} />
          ))}
        </div>
      )}

      <h2 className="mb-3 mt-10 text-lg font-semibold text-slate-900">Response classification breakdown</h2>
      {responseStats.byClassification.length === 0 ? (
        <p className="text-sm text-slate-500">No responses recorded yet.</p>
      ) : (
        <div className="flex flex-wrap gap-2">
          {responseStats.byClassification.map((c) => (
            <span key={c.classification} className="rounded-full border border-slate-200 px-3 py-1 text-xs font-medium text-slate-700">
              {c.classification.replace(/_/g, " ")}: <span className="tabular-nums">{c.count}</span>
            </span>
          ))}
        </div>
      )}

      <h2 className="mb-3 mt-10 text-lg font-semibold text-slate-900">Businesses in this batch</h2>
      <div role="region" aria-label="Batch businesses" tabIndex={0} className="overflow-x-auto rounded-xl border border-slate-200">
        <table className="min-w-max w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Business</th>
              <th className="px-4 py-2 font-medium">Stage</th>
              <th className="px-4 py-2 font-medium">Sent</th>
              <th className="px-4 py-2 font-medium">Responded</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {batchBusinesses.map((b) => (
              <tr key={b.id} className="hover:bg-slate-50">
                <td className="whitespace-nowrap px-4 py-2">
                  <Link href={`/directoryadmin/businesses/${b.businessRef}`} className="font-medium text-slate-900 hover:text-brand-600">
                    {b.businessName}
                  </Link>
                  <div className="text-xs text-slate-500">{b.category}{b.town ? ` · ${b.town}` : ""}</div>
                </td>
                <td className="whitespace-nowrap px-4 py-2">
                  <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">{b.stageLabel ?? "—"}</span>
                </td>
                <td className="whitespace-nowrap px-4 py-2 text-slate-600">{b.sentAt ? format(b.sentAt, "d MMM yyyy") : "—"}</td>
                <td className="whitespace-nowrap px-4 py-2">
                  {b.responded ? (
                    <span className="rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">
                      {b.lastResponseClassification?.replace(/_/g, " ")}
                    </span>
                  ) : (
                    <span className="text-slate-400">no response</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
