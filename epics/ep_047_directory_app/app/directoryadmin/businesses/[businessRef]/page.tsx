import Link from "next/link";
import { notFound } from "next/navigation";
import { format } from "date-fns";
import { getBusinessByRef } from "@/lib/db/queries/directory";
import { getBusinessTimeline, getPipelineStages } from "@/lib/db/queries/pipeline";
import { moveStageAction } from "../../pipeline/actions";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ businessRef: string }>;
}

export default async function AdminBusinessDetailPage({ params }: PageProps) {
  const { businessRef } = await params;
  const business = await getBusinessByRef(businessRef);
  if (!business) notFound();

  const [timeline, stages] = await Promise.all([getBusinessTimeline(business.id), getPipelineStages()]);

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">
        Admin — Business
      </p>
      <div className="mt-1 flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">
            {business.businessName}
          </h1>
          <p className="mt-1 text-sm capitalize text-slate-500">
            {business.category}
            {business.town ? ` · ${business.town}` : ""} ·{" "}
            <span className="font-mono text-xs">{business.businessRef}</span>
          </p>
        </div>
        <Link
          href={`/directory/business/${business.slug}`}
          className="whitespace-nowrap text-sm font-medium text-brand-600 hover:text-brand-700"
        >
          View public page →
        </Link>
      </div>

      <div className="mt-6 flex items-center gap-3 rounded-lg border border-slate-200 p-4">
        <span className="rounded-full bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700">
          {business.stageLabel ?? "—"}
        </span>
        <form action={moveStageAction} className="flex flex-1 gap-2">
          <input type="hidden" name="businessId" value={business.id} />
          <select name="toStageKey" defaultValue="" className="flex-1 rounded-md border border-slate-300 px-3 py-1.5 text-sm">
            <option value="" disabled>
              Move to a different stage…
            </option>
            {stages.map((s) => (
              <option key={s.key} value={s.key}>
                {s.label}
              </option>
            ))}
          </select>
          <button
            type="submit"
            className="rounded-md bg-brand-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-brand-700"
          >
            Move
          </button>
        </form>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
        <div className="rounded-lg border border-slate-200 p-4">
          <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Contact</h2>
          <dl className="space-y-1">
            <div className="flex gap-2">
              <dt className="text-slate-400">Phone</dt>
              <dd>{business.phone ?? "—"}</dd>
            </div>
            <div className="flex gap-2">
              <dt className="text-slate-400">Mobile</dt>
              <dd>{business.mobile ?? "—"}</dd>
            </div>
            <div className="flex gap-2">
              <dt className="text-slate-400">Email</dt>
              <dd>{business.email ?? "—"}</dd>
            </div>
            <div className="flex gap-2">
              <dt className="text-slate-400">Website</dt>
              <dd>{business.website ?? "—"}</dd>
            </div>
          </dl>
        </div>
        <div className="rounded-lg border border-slate-200 p-4">
          <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">Address</h2>
          <p>
            {[business.address, business.town, business.county, business.postcode]
              .filter(Boolean)
              .join(", ") || "—"}
          </p>
          <p className="mt-2 text-slate-400">
            Imported {format(business.importDate, "d MMM yyyy, HH:mm")}
          </p>
        </div>
      </div>

      <section className="mt-10">
        <h2 className="mb-4 text-lg font-semibold text-slate-900">Timeline</h2>
        <ol className="space-y-4 border-l-2 border-slate-200 pl-6">
          {timeline.map((entry) => (
            <li key={entry.id} className="relative">
              <span className="absolute -left-[1.94rem] top-1 h-3 w-3 rounded-full bg-brand-500" />
              <p className="font-medium text-slate-900">
                {entry.fromStageLabel ? `${entry.fromStageLabel} → ${entry.toStageLabel}` : entry.toStageLabel}
              </p>
              <p className="text-xs text-slate-500">
                {format(entry.occurredAt, "d MMM yyyy, HH:mm")} · source: {entry.source}
                {entry.reason ? ` · ${entry.reason}` : ""}
              </p>
              {entry.notes && <p className="mt-1 text-sm text-slate-600">{entry.notes}</p>}
            </li>
          ))}
        </ol>
      </section>
    </main>
  );
}
