/**
 * app/directoryadmin/crm/page.tsx — EP043 CRM: batch list (node report 2.1).
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-10 · Initial version. Read-only view over verification_batches,
 *   reused as the outreach-batch mechanism — no batch creation/management here,
 *   that stays on /directoryadmin/verification-batches.
 */
import Link from "next/link";
import { format } from "date-fns";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { listCrmBatches } from "@/lib/db/queries/crm";
import { notFound } from "next/navigation";

export const dynamic = "force-dynamic";

function pct(n: number, d: number): string {
  return d > 0 ? `${Math.round((n / d) * 100)}%` : "—";
}

export default async function CrmBatchesPage() {
  const user = await requireAdminUserForPage("/directoryadmin/crm");
  if (!canManageVerification(user.role)) notFound();
  const batches = await listCrmBatches();

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — CRM</p>
      <h1 className="mt-1 text-2xl font-semibold">Batch reporting</h1>
      <p className="mt-2 text-slate-600">
        Read-only reporting on outreach batches — pipeline status, response rate and opportunities.
        Batches themselves are created and sent from{" "}
        <Link href="/directoryadmin/verification-batches" className="font-medium text-brand-600 hover:text-brand-700">
          Batch verification
        </Link>.
      </p>

      <div role="region" aria-label="CRM batches" tabIndex={0} className="mt-8 overflow-x-auto rounded-xl border border-slate-200">
        <table className="min-w-max w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Batch</th>
              <th className="px-4 py-2 font-medium">Created</th>
              <th className="px-4 py-2 font-medium">Businesses</th>
              <th className="px-4 py-2 font-medium">Sent</th>
              <th className="px-4 py-2 font-medium">Responses</th>
              <th className="px-4 py-2 font-medium">Response rate</th>
              <th className="px-4 py-2 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {batches.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-4 py-8 text-center text-slate-500">No batches yet.</td>
              </tr>
            ) : (
              batches.map((batch) => (
                <tr key={batch.id} className="hover:bg-slate-50">
                  <td className="whitespace-nowrap px-4 py-2">
                    <Link href={`/directoryadmin/crm/${batch.id}`} className="font-mono text-xs font-medium text-brand-600 hover:text-brand-700">
                      {batch.id.slice(0, 8)}…
                    </Link>
                  </td>
                  <td className="whitespace-nowrap px-4 py-2 text-slate-600">{format(batch.createdAt, "d MMM yyyy, HH:mm")}</td>
                  <td className="whitespace-nowrap px-4 py-2 tabular-nums">{batch.totalCount}</td>
                  <td className="whitespace-nowrap px-4 py-2 tabular-nums">{batch.sentCount}</td>
                  <td className="whitespace-nowrap px-4 py-2 tabular-nums">{batch.responseCount}</td>
                  <td className="whitespace-nowrap px-4 py-2 tabular-nums">{pct(batch.responseCount, batch.sentCount)}</td>
                  <td className="whitespace-nowrap px-4 py-2">
                    <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">{batch.status}</span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
}
