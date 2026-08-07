/**
 * app/directoryadmin/owner-review-submissions/page.tsx — read-only list of
 * owner review submissions.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-07 · Initial version: closes part of gap `corrections` on
 *   EP047_end_to_end_workflow_gap_register.html — submitted owner feedback was
 *   previously written to the database and never read anywhere. Deliberately
 *   read-only for now; no apply/reject action exists yet (would need a schema
 *   migration this session could not safely generate without a local DB to
 *   verify it against).
 */
import Link from "next/link";
import { notFound } from "next/navigation";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { listOwnerReviewSubmissions } from "@/lib/owner-review/repository";

export const dynamic = "force-dynamic";

export default async function OwnerReviewSubmissionsPage() {
  const user = await requireAdminUserForPage("/directoryadmin/owner-review-submissions");
  if (!canManageVerification(user.role)) notFound();

  const submissions = await listOwnerReviewSubmissions();

  return (
    <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Owner feedback</p>
      <div className="mt-1 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="break-words text-2xl font-semibold">Owner review submissions</h1>
          <p className="mt-2 text-slate-600">
            Read-only for now. No apply/reject action exists yet — corrections still have to be
            actioned by hand until that decision path is built.
          </p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-700">
          {submissions.length} submission{submissions.length === 1 ? "" : "s"}
        </span>
      </div>

      <div role="region" aria-label="Owner review submissions table" tabIndex={0} className="mt-8 overflow-x-auto rounded-xl border border-slate-200">
        <table className="min-w-max w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3">Business</th>
              <th className="px-4 py-3">Decision</th>
              <th className="px-4 py-3">Pages responded</th>
              <th className="px-4 py-3">Submitted</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {submissions.map((s) => (
              <tr key={s.id}>
                <td className="px-4 py-3">
                  <Link className="font-medium text-brand-700 hover:underline" href={`/directoryadmin/owner-review-submissions/${s.id}`}>
                    {s.businessName}
                  </Link>
                  <span className="block font-mono text-xs text-slate-400">{s.businessRef}</span>
                </td>
                <td className="px-4 py-3">
                  <span
                    className={
                      s.decision === "accept"
                        ? "rounded-full bg-green-100 px-2 py-1 text-xs font-semibold text-green-900"
                        : s.decision === "decline"
                          ? "rounded-full bg-red-100 px-2 py-1 text-xs font-semibold text-red-900"
                          : "rounded-full bg-amber-100 px-2 py-1 text-xs font-semibold text-amber-900"
                    }
                  >
                    {s.decision}
                  </span>
                </td>
                <td className="px-4 py-3">{s.pageCount}</td>
                <td className="whitespace-nowrap px-4 py-3 text-slate-500">
                  {s.submittedAt.toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" })}
                </td>
              </tr>
            ))}
            {submissions.length === 0 && (
              <tr>
                <td colSpan={4} className="px-4 py-12 text-center text-slate-500">
                  No owner review submissions yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
}
