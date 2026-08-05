import Link from "next/link";
import { formatDistanceToNow } from "date-fns";
import { getDashboardMetrics, getRecentActivity } from "@/lib/db/queries/pipeline";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { getValidationOverview } from "@/lib/validation/repository";
import { ValidationOverviewPanel } from "@/components/admin/ValidationOverviewPanel";

export const dynamic = "force-dynamic";

function Stat({ label, value, tone = "slate" }: { label: string; value: string | number; tone?: "slate" | "red" | "brand" }) {
  const toneClass =
    tone === "red" ? "text-red-600" : tone === "brand" ? "text-brand-600" : "text-slate-900";
  return (
    <div className="rounded-xl border border-slate-200 p-4">
      <p className={`text-2xl font-semibold tabular-nums ${toneClass}`}>{value}</p>
      <p className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-500">{label}</p>
    </div>
  );
}

function formatHours(hours: number | null): string {
  if (hours === null) return "—";
  if (hours < 48) return `${Math.round(hours)}h`;
  return `${Math.round(hours / 24)}d`;
}

export default async function DashboardPage() {
  await requireAdminUserForPage("/directoryadmin/dashboard");
  const [metrics, activity, validationOverview] = await Promise.all([
    getDashboardMetrics(), getRecentActivity(15), getValidationOverview(),
  ]);

  return (
    <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Dashboard</p>
      <div className="mt-1 flex flex-col gap-2 sm:flex-row sm:items-baseline sm:justify-between">
        <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Dashboard</h1>
        <Link href="/directoryadmin/pipeline" className="text-sm font-medium text-brand-600 hover:text-brand-700">
          Pipeline board →
        </Link>
      </div>

      <div className="mt-8 flex flex-wrap gap-3 text-sm font-medium">
        <Link href="/directoryadmin/visibility" className="rounded border px-4 py-2 hover:border-brand-400">Public visibility controls →</Link>
        <Link href="/directoryadmin/news" className="rounded border px-4 py-2 hover:border-brand-400">News drafts & publishing →</Link>
      </div>

      <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Stat label="Businesses" value={metrics.totalBusinesses} />
        <Stat label="Categories" value={metrics.categoryCount} />
        <Stat label="Towns" value={metrics.townCount} />
        <Stat label="Avg. time in pipeline" value={formatHours(metrics.avgPipelineHours)} />
      </div>

      <h2 className="mb-3 mt-10 text-lg font-semibold text-slate-900">Imports</h2>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <Stat label="Today" value={metrics.importsToday} tone="brand" />
        <Stat label="This week" value={metrics.importsThisWeek} tone="brand" />
        <Stat label="This month" value={metrics.importsThisMonth} tone="brand" />
      </div>

      <div className="mt-10">
        <ValidationOverviewPanel overview={validationOverview} heading="Validation outcomes"/>
      </div>

      <h2 className="mb-3 mt-10 text-lg font-semibold text-slate-900">Needs attention</h2>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <Link
          href="/directoryadmin/pipeline"
          className="block rounded-xl border border-slate-200 p-4 hover:border-red-300 hover:bg-red-50/40"
        >
          <p className={`text-2xl font-semibold tabular-nums ${metrics.stalledCount > 0 ? "text-red-600" : "text-slate-900"}`}>
            {metrics.stalledCount}
          </p>
          <p className="mt-1 text-xs font-medium uppercase tracking-wide text-slate-500">
            Stalled activation work (past stage SLA)
          </p>
          <p className="mt-2 text-xs text-slate-500">Completed field validation is not treated as a stalled Imported record.</p>
        </Link>
        <Link
          href="/directoryadmin/import"
          className="block rounded-xl border border-dashed border-slate-300 p-4 text-sm text-slate-600 hover:border-brand-300 hover:bg-brand-50/40"
        >
          Import a new CSV or JSON file →
        </Link>
      </div>

      <h2 className="mb-3 mt-10 text-lg font-semibold text-slate-900">Recent activity</h2>
      <div role="region" aria-label="Recent activity table" tabIndex={0} className="overflow-x-auto rounded-xl border border-slate-200">
        <table className="min-w-max w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Business</th>
              <th className="px-4 py-2 font-medium">Moved to</th>
              <th className="px-4 py-2 font-medium">Source</th>
              <th className="px-4 py-2 font-medium">When</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {activity.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-slate-500">
                  No activity yet.
                </td>
              </tr>
            ) : (
              activity.map((row, index) => (
                <tr key={`${row.businessId}-${index}`}>
                  <td className="whitespace-nowrap px-4 py-2">
                    <Link
                      href={`/directoryadmin/businesses/${row.businessRef}`}
                      className="font-medium text-slate-900 hover:text-brand-600"
                    >
                      {row.businessName}
                    </Link>
                  </td>
                  <td className="whitespace-nowrap px-4 py-2">
                    <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">
                      {row.toStageLabel}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-4 py-2 text-slate-600">{row.source}</td>
                  <td className="whitespace-nowrap px-4 py-2 text-slate-500">
                    {formatDistanceToNow(row.occurredAt, { addSuffix: true })}
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
