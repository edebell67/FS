import Link from "next/link";
import { formatDistanceToNow } from "date-fns";
import { getBoardColumns } from "@/lib/db/queries/pipeline";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { moveStageAction } from "./actions";
import { getValidationOverview } from "@/lib/validation/repository";
import { ValidationOverviewPanel } from "@/components/admin/ValidationOverviewPanel";
import { getPendingClaimCount } from "@/lib/verification/claims-approval";
import { getEligibleVerificationBusinesses } from "@/lib/verification/batches";
import { getBusinessesAwaitingSiteGeneration, getBusinessesReadyForPreviewNotification } from "@/lib/verification/site-generation";
import { isGenerationConfigured } from "@/lib/generation/config";
import { WorkflowControlModal } from "@/components/admin/WorkflowControlModal";

export const dynamic = "force-dynamic";

function formatHours(hours: number | null): string {
  if (hours === null) return "—";
  if (hours < 1) return "<1h";
  if (hours < 48) return `${Math.round(hours)}h`;
  return `${Math.round(hours / 24)}d`;
}

export default async function PipelinePage() {
  await requireAdminUserForPage("/directoryadmin/pipeline");
  const [columns, validationOverview, pendingClaims, verificationBusinesses, generationQueue, previewBusinesses] = await Promise.all([
    getBoardColumns(), getValidationOverview(), getPendingClaimCount(), getEligibleVerificationBusinesses(),
    getBusinessesAwaitingSiteGeneration(), getBusinessesReadyForPreviewNotification(),
  ]);
  const generationAvailable = isGenerationConfigured() && Boolean(process.env.INTERNAL_API_KEY?.trim()) && Boolean(process.env.PUBLIC_APP_ORIGIN?.trim());
  const workflowCounts = {
    awaitingValidation: validationOverview.counts.awaitingValidation,
    verificationEligible: verificationBusinesses.filter((business) => business.validationStatus === "validated").length,
    pendingClaims,
    awaitingGeneration: generationQueue.length,
    previewEligible: previewBusinesses.length,
  };
  return (
    <main className="mx-auto max-w-[1400px] px-4 py-10 sm:px-6 sm:py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Pipeline</p>
      <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">
        Activation pipeline
      </h1>
      <p className="mt-2 text-slate-600">
        Every business, wherever it is between discovery and subscriber. Move a business between
        stages with the dropdown on its card.
      </p>
      <div className="mt-4 flex flex-wrap gap-3">
        <WorkflowControlModal counts={workflowCounts} generationAvailable={generationAvailable} />
        <Link href="/directoryadmin/validation"
          className="inline-block rounded bg-brand-600 px-4 py-2 text-sm font-medium text-white">
          {validationOverview.counts.awaitingValidation > 0
            ? `Run field validation for ${validationOverview.counts.awaitingValidation.toLocaleString()} awaiting ${validationOverview.counts.awaitingValidation === 1 ? "business" : "businesses"}`
            : "Open field validation"}
        </Link>
        <Link href="/directoryadmin/verification-batches"
          className="inline-block rounded border border-brand-600 px-4 py-2 text-sm font-medium text-brand-700 hover:bg-brand-50">
          Select validated businesses for batch verification
        </Link>
        <Link href="/directoryadmin/site-previews"
          className="inline-block rounded border border-brand-600 px-4 py-2 text-sm font-medium text-brand-700 hover:bg-brand-50">
          Send site preview links
        </Link>
        <Link href="/directoryadmin/claims"
          className="inline-block rounded border border-amber-500 px-4 py-2 text-sm font-medium text-amber-800 hover:bg-amber-50">
          {pendingClaims ? `Review ${pendingClaims} claims pending` : "Open claims review"}
        </Link>
      </div>

      <div className="mt-8">
        <ValidationOverviewPanel overview={validationOverview} heading="Field-validation status"/>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-4 overflow-x-auto pb-4 md:grid-cols-none md:grid-flow-col md:auto-cols-[280px]">
        {columns.map((column) => (
          <div key={column.name} className="flex min-w-[260px] flex-col rounded-xl border border-slate-200 bg-slate-50/50">
            <div className="border-b border-slate-200 p-4">
              <div className="flex items-center justify-between">
                <h2 className="font-semibold text-slate-900">{column.name}</h2>
                <span className="rounded-full bg-slate-200 px-2 py-0.5 text-xs font-semibold text-slate-700">
                  {column.count}
                </span>
              </div>
              {column.stages.some((stage) => stage.key === "awaiting_site_generation") && (
                <p className="mt-2 rounded bg-brand-50 px-2 py-1 text-xs text-brand-900">
                  Claim approval is recorded before a business queues here for generation.
                </p>
              )}
              <dl className="mt-2 grid grid-cols-3 gap-2 text-xs text-slate-500">
                <div>
                  <dt className="uppercase tracking-wide">Today</dt>
                  <dd className="font-medium text-slate-700">{column.movementToday}</dd>
                </div>
                <div>
                  <dt className="uppercase tracking-wide">Avg time</dt>
                  <dd className="font-medium text-slate-700">{formatHours(column.avgHoursInStage)}</dd>
                </div>
                <div>
                  <dt className="uppercase tracking-wide">Blocked</dt>
                  <dd className={column.blockedCount > 0 ? "font-medium text-red-600" : "font-medium text-slate-700"}>
                    {column.blockedCount}
                  </dd>
                </div>
              </dl>
            </div>

            <div className="flex-1 space-y-2 p-3">
              {column.businesses.length === 0 ? (
                <p className="px-2 py-4 text-center text-xs text-slate-400">Nothing here.</p>
              ) : (
                column.businesses.map((business) => (
                  <div key={business.id} className="rounded-lg border border-slate-200 bg-white p-3 text-sm shadow-sm">
                    <Link
                      href={`/directoryadmin/businesses/${business.businessRef}`}
                      className="font-medium text-slate-900 hover:text-brand-600"
                    >
                      {business.businessName}
                    </Link>
                    <p className="mt-0.5 capitalize text-slate-500">
                      {business.category}
                      {business.town ? ` · ${business.town}` : ""}
                    </p>
                    {business.stageEnteredAt && (
                      <p className="mt-0.5 text-xs text-slate-400">
                        Entered {formatDistanceToNow(business.stageEnteredAt, { addSuffix: true })}
                      </p>
                    )}
                    <form action={moveStageAction} className="mt-2 flex flex-col gap-1.5 sm:flex-row">
                      <input type="hidden" name="businessId" value={business.id} />
                      <select
                        name="toStageKey"
                        defaultValue=""
                        className="w-full rounded border border-slate-300 px-1.5 py-1 text-xs sm:flex-1"
                      >
                        <option value="" disabled>
                          Move to…
                        </option>
                        {columns.flatMap((c) =>
                          c.stages.filter((s) => !["Verification", "Claimed"].includes(s.boardColumn)).map((s) => (
                            <option key={s.key} value={s.key}>
                              {s.label}
                            </option>
                          ))
                        )}
                      </select>
                      <button
                        type="submit"
                        className="rounded bg-brand-600 px-2 py-1 text-xs font-medium text-white hover:bg-brand-700 sm:w-auto"
                      >
                        Go
                      </button>
                    </form>
                  </div>
                ))
              )}
            </div>

            {column.count > column.businesses.length && (
              <Link
                href={`/directoryadmin/businesses?column=${encodeURIComponent(column.name)}`}
                className="border-t border-slate-200 p-3 text-center text-xs font-medium text-brand-600 hover:bg-brand-50"
              >
                View all {column.count} →
              </Link>
            )}
          </div>
        ))}
      </div>
    </main>
  );
}
