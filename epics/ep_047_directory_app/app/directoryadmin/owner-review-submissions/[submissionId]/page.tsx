/**
 * app/directoryadmin/owner-review-submissions/[submissionId]/page.tsx —
 * read-only detail view of one owner review submission's per-page responses.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-08-07 · Initial version, alongside the list page — gap
 *   `corrections`. Read-only; see the list page's version history for why.
 */
import { notFound } from "next/navigation";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { getOwnerReviewSubmissionDetail } from "@/lib/owner-review/repository";

export const dynamic = "force-dynamic";

export default async function OwnerReviewSubmissionDetailPage({
  params,
}: {
  params: Promise<{ submissionId: string }>;
}) {
  const user = await requireAdminUserForPage("/directoryadmin/owner-review-submissions");
  if (!canManageVerification(user.role)) notFound();

  const { submissionId } = await params;
  const submission = await getOwnerReviewSubmissionDetail(submissionId);
  if (!submission) notFound();

  return (
    <main className="mx-auto max-w-4xl px-4 py-10 sm:px-6 sm:py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Owner feedback</p>
      <h1 className="mt-1 text-2xl font-semibold">{submission.businessName}</h1>
      <p className="mt-2 text-slate-600">
        Decision: <strong>{submission.decision}</strong> · submitted{" "}
        {submission.submittedAt.toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" })}
      </p>
      <p className="mt-1 text-sm text-amber-800">
        Read-only. No apply/reject action exists yet — act on this by hand for now.
      </p>

      <div className="mt-8 space-y-4">
        {submission.pages.map((page) => (
          <section key={page.pageKey} className="rounded-xl border border-slate-200 p-4">
            <h2 className="font-semibold text-slate-900">{page.pageKey}</h2>
            {page.noActionRequired ? (
              <p className="mt-2 text-sm text-slate-500">No action required for this page.</p>
            ) : (
              <>
                {page.selections.length > 0 && (
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                    {page.selections.map((selection, i) => (
                      <li key={i}>{selection}</li>
                    ))}
                  </ul>
                )}
                {page.anythingElse && (
                  <p className="mt-2 rounded bg-slate-50 p-2 text-sm text-slate-700">
                    &ldquo;{page.anythingElse}&rdquo;
                  </p>
                )}
              </>
            )}
            {page.pageOpenDateTime && (
              <p className="mt-2 text-xs text-slate-400">
                Opened {page.pageOpenDateTime.toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" })}
              </p>
            )}
          </section>
        ))}
        {submission.pages.length === 0 && (
          <p className="text-slate-500">No per-page responses were recorded for this submission.</p>
        )}
      </div>
    </main>
  );
}
