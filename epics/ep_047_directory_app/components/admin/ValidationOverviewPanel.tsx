import Link from "next/link";
import type { ValidationOverview } from "@/lib/validation/repository";
import {
  formatValidationDuration,
  formatValidationStatus,
  formatValidationTimestamp,
} from "@/lib/validation/presentation";

function Count({ label, value }: { label: string; value: number }) {
  return <div className="rounded-lg border border-slate-200 bg-white p-3">
    <dd className="text-xl font-semibold tabular-nums text-slate-900">{value.toLocaleString()}</dd>
    <dt className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-500">{label}</dt>
  </div>;
}

export function ValidationOverviewPanel({
  overview,
  heading = "Field validation",
}: {
  overview: ValidationOverview;
  heading?: string;
}) {
  const { counts, latestJob } = overview;
  return <section className="rounded-xl border border-slate-200 bg-slate-50/50 p-4">
    <div className="flex flex-wrap items-baseline justify-between gap-2">
      <div>
        <h2 className="text-lg font-semibold text-slate-900">{heading}</h2>
        <p className="mt-1 text-sm text-slate-600">Current outcome for active businesses, independent of historic pipeline stage.</p>
      </div>
      <Link href="/directoryadmin/validation" className="text-sm font-medium text-brand-700 hover:text-brand-800">
        Open validation &amp; repair →
      </Link>
    </div>

    <dl className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
      <Count label="Validated" value={counts.validated}/>
      <Count label="Partially validated" value={counts.partiallyValidated}/>
      <Count label="Non-valid" value={counts.nonValid}/>
      <Count label="Awaiting validation" value={counts.awaitingValidation}/>
    </dl>

    <div className="mt-4 rounded-lg border border-slate-200 bg-white p-3">
      <h3 className="text-sm font-semibold text-slate-900">Latest validation run</h3>
      {latestJob ? <>
        <dl className="mt-2 grid gap-x-6 gap-y-2 text-sm sm:grid-cols-2 lg:grid-cols-4">
          <div><dt className="text-slate-500">Status</dt><dd className="font-medium capitalize">{formatValidationStatus(latestJob.status)}</dd></div>
          <div><dt className="text-slate-500">Processed</dt><dd className="font-medium tabular-nums">{latestJob.processedCount.toLocaleString()} / {latestJob.totalCount.toLocaleString()}</dd></div>
          <div><dt className="text-slate-500">Errors</dt><dd className={`font-medium tabular-nums ${latestJob.errorCount ? "text-red-600" : ""}`}>{latestJob.errorCount.toLocaleString()}</dd></div>
          <div><dt className="text-slate-500">Duration</dt><dd className="font-medium tabular-nums">{formatValidationDuration(latestJob)}</dd></div>
          <div className="sm:col-span-2"><dt className="text-slate-500">Started</dt><dd className="font-medium tabular-nums">{formatValidationTimestamp(latestJob.startedAt)}</dd></div>
          <div className="sm:col-span-2"><dt className="text-slate-500">Completed</dt><dd className="font-medium tabular-nums">{formatValidationTimestamp(latestJob.completedAt)}</dd></div>
        </dl>
        {latestJob.errors.length > 0 && <details className="mt-3 text-sm">
          <summary className="cursor-pointer font-medium text-red-700">Recent errors ({latestJob.errorCount.toLocaleString()})</summary>
          <ul className="mt-2 space-y-1 text-xs text-slate-700">
            {latestJob.errors.map((error) => <li key={error.businessId} className="break-words">
              <span className="font-mono">{error.businessId}</span>: {error.message}
            </li>)}
          </ul>
        </details>}
      </> : <p className="mt-2 text-sm text-slate-500">No validation run has been started.</p>}
    </div>
  </section>;
}
