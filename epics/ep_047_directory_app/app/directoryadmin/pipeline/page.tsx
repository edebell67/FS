import Link from "next/link";
import { formatDistanceToNow } from "date-fns";
import { getBoardColumns } from "@/lib/db/queries/pipeline";
import { moveStageAction } from "./actions";

export const dynamic = "force-dynamic";

function formatHours(hours: number | null): string {
  if (hours === null) return "—";
  if (hours < 1) return "<1h";
  if (hours < 48) return `${Math.round(hours)}h`;
  return `${Math.round(hours / 24)}d`;
}

export default async function PipelinePage() {
  const columns = await getBoardColumns();

  return (
    <main className="mx-auto max-w-[1400px] px-6 py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Pipeline</p>
      <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">
        Activation pipeline
      </h1>
      <p className="mt-2 text-slate-600">
        Every business, wherever it is between discovery and subscriber. Move a business between
        stages with the dropdown on its card.
      </p>

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
                    <form action={moveStageAction} className="mt-2 flex gap-1.5">
                      <input type="hidden" name="businessId" value={business.id} />
                      <select
                        name="toStageKey"
                        defaultValue=""
                        className="flex-1 rounded border border-slate-300 px-1.5 py-1 text-xs"
                      >
                        <option value="" disabled>
                          Move to…
                        </option>
                        {columns.flatMap((c) =>
                          c.stages.map((s) => (
                            <option key={s.key} value={s.key}>
                              {s.label}
                            </option>
                          ))
                        )}
                      </select>
                      <button
                        type="submit"
                        className="rounded bg-brand-600 px-2 py-1 text-xs font-medium text-white hover:bg-brand-700"
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
