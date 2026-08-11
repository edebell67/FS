/**
 * app/directoryadmin/businesses/[businessRef]/page.tsx — business detail page.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-08-06 · Timeline entries now visually distinguish delivery
 *   events (sky dot) from stage transitions (brand dot), matching the merged
 *   getBusinessTimeline() (pipeline.ts v1.1.0) — gap `verificationstage`.
 * v1.0.0 · 2026-08-06 · Version history added; file predates this convention.
 */
import Link from "next/link";
import { notFound } from "next/navigation";
import { format } from "date-fns";
import { getBusinessByRef } from "@/lib/db/queries/directory";
import { getBusinessForEdit } from "@/lib/db/queries/businesses";
import { getBusinessTimeline, getPipelineStages } from "@/lib/db/queries/pipeline";
import { getBusinessOutreachResponses } from "@/lib/db/queries/crm";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { moveStageAction } from "../../pipeline/actions";
import { updateBusinessAction } from "./actions";
import { VerificationLinkPanel } from "@/components/admin/VerificationLinkPanel";
import { PreviewDeliveryPanel } from "@/components/admin/PreviewDeliveryPanel";
import { canManageVerification, getLatestDeliveryForBusiness } from "@/lib/verification/repository";
import type { VerificationDeliveryState } from "@/lib/verification/delivery-status";
import { getBusinessValidationDetail } from "@/lib/validation/repository";
import { getLatestPreviewMessageForBusiness } from "@/lib/verification/preview-delivery";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ businessRef: string }>;
}

export default async function AdminBusinessDetailPage({ params }: PageProps) {
  const { businessRef } = await params;
  const user = await requireAdminUserForPage(`/directoryadmin/businesses/${businessRef}`);
  const business = await getBusinessByRef(businessRef);
  if (!business) notFound();

  const [timeline, stages, validation, latestDelivery, editable, latestPreviewMessage, outreachResponses] = await Promise.all([
    getBusinessTimeline(business.id), getPipelineStages(), getBusinessValidationDetail(business.id),
    canManageVerification(user.role) ? getLatestDeliveryForBusiness(business.id) : Promise.resolve(null),
    getBusinessForEdit(businessRef),
    canManageVerification(user.role) && business.stageKey === "ready_for_preview"
      ? getLatestPreviewMessageForBusiness(business.id) : Promise.resolve(null),
    getBusinessOutreachResponses(business.id),
  ]);

  return (
    <main className="mx-auto max-w-4xl px-4 py-10 sm:px-6 sm:py-12">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">
        Admin — Business
      </p>
      <div className="mt-1 flex flex-col items-start gap-4 sm:flex-row sm:justify-between">
        <div>
          <h1 className="break-words text-2xl font-semibold tracking-tight text-slate-900">
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
      <div className="mt-4 flex flex-col items-start gap-3 rounded-lg border border-slate-200 p-4 text-sm sm:flex-row sm:justify-between">
        <div className="break-words">Calculated validation: <strong>{validation?.validationStatus ?? "non_valid"}</strong>
          {validation?.outcomes.some((outcome) => !outcome.passed) &&
            <span className="ml-2 text-amber-700">{validation.outcomes.filter((outcome) => !outcome.passed).length} outstanding field(s)</span>}</div>
        {canManageVerification(user.role) && <Link href="/directoryadmin/validation" className="font-medium text-brand-700">Open validation & repair →</Link>}
      </div>

      <div className="mt-6 flex flex-col items-stretch gap-3 rounded-lg border border-slate-200 p-4 sm:flex-row sm:items-center">
        <span className="rounded-full bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700">
          {business.stageLabel ?? "—"}
        </span>
        <form action={moveStageAction} className="flex flex-col items-stretch gap-2 sm:flex-row sm:flex-1">
          <input type="hidden" name="businessId" value={business.id} />
          <select name="toStageKey" defaultValue="" className="w-full rounded-md border border-slate-300 px-3 py-1.5 text-sm sm:flex-1">
            <option value="" disabled>
              Move to a different stage…
            </option>
            {stages.filter((s) => !["Verification", "Claimed"].includes(s.boardColumn)).map((s) => (
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
      {canManageVerification(user.role) && business.stageKey === "ready_for_preview"
        ? <PreviewDeliveryPanel delivery={latestPreviewMessage} />
        : canManageVerification(user.role) && <VerificationLinkPanel
        businessRef={business.businessRef}
        initialRecipient={business.email ?? ""}
        initialDeliveryState={(latestDelivery?.status ?? "prepared") as VerificationDeliveryState}
      />}

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
              <dd className="break-words">{business.email ?? "—"}</dd>
            </div>
            <div className="flex gap-2">
              <dt className="text-slate-400">Website</dt>
              <dd className="break-words">{business.website ?? "—"}</dd>
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

      {editable && (
        <section className="mt-10 rounded-lg border border-slate-200 p-6">
          <h2 className="mb-4 text-lg font-semibold text-slate-900">Edit business details</h2>
          <form action={updateBusinessAction} className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <input type="hidden" name="businessId" value={editable.id} />
            <input type="hidden" name="businessRef" value={editable.businessRef} />

            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Business name</span>
              <input name="businessName" defaultValue={editable.businessName} required
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Trading name</span>
              <input name="tradingName" defaultValue={editable.tradingName ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Category</span>
              <input name="category" defaultValue={editable.category} required
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Sub-category</span>
              <input name="subCategory" defaultValue={editable.subCategory ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Email</span>
              <input name="email" type="email" defaultValue={editable.email ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Phone</span>
              <input name="phone" defaultValue={editable.phone ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Mobile</span>
              <input name="mobile" defaultValue={editable.mobile ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Website</span>
              <input name="website" defaultValue={editable.website ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Facebook</span>
              <input name="facebook" defaultValue={editable.facebook ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Instagram</span>
              <input name="instagram" defaultValue={editable.instagram ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">LinkedIn</span>
              <input name="linkedin" defaultValue={editable.linkedin ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Address</span>
              <input name="address" defaultValue={editable.address ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Town</span>
              <input name="town" defaultValue={editable.town ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">County</span>
              <input name="county" defaultValue={editable.county ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm">
              <span className="font-medium text-slate-700">Postcode</span>
              <input name="postcode" defaultValue={editable.postcode ?? ""}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm sm:col-span-2">
              <span className="font-medium text-slate-700">Description</span>
              <textarea name="description" defaultValue={editable.description ?? ""} rows={3}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
            </label>
            <label className="flex flex-col gap-1 text-sm sm:col-span-2">
              <span className="font-medium text-slate-700">Generated site URL</span>
              <input name="generatedSiteUrl" defaultValue={editable.generatedSiteUrl ?? ""}
                placeholder="https://thetechprinciple.com/<slug>/index.html"
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm" />
              <span className="text-xs text-slate-400">
                Set this once a site is genuinely live, then use &ldquo;Move to a different
                stage&rdquo; above to advance to Ready for Preview.
              </span>
            </label>
            <label className="flex items-center gap-2 text-sm sm:col-span-2">
              <input type="checkbox" name="chatWidgetOptIn" defaultChecked={editable.chatWidgetOptIn} />
              <input type="hidden" name="chatWidgetOptIn" value="off" />
              <span className="font-medium text-slate-700">Chat widget enabled on generated site</span>
            </label>

            <div className="sm:col-span-2">
              <button type="submit"
                className="rounded-md bg-brand-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-brand-700">
                Save changes
              </button>
            </div>
          </form>
        </section>
      )}

      {outreachResponses.length > 0 && (
        <section className="mt-10">
          <h2 className="mb-4 text-lg font-semibold text-slate-900">Outreach responses</h2>
          <ol className="space-y-3">
            {outreachResponses.map((response) => (
              <li key={response.id} className="rounded-lg border border-slate-200 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">
                    {response.classification.replace(/_/g, " ")}
                  </span>
                  <span className="text-xs text-slate-500">
                    {format(response.receivedAt, "d MMM yyyy, HH:mm")} · {response.channel}
                  </span>
                </div>
                <p className="mt-2 whitespace-pre-wrap text-sm text-slate-700">{response.originalBody}</p>
                {response.notes && <p className="mt-2 text-xs text-slate-500">{response.notes}</p>}
              </li>
            ))}
          </ol>
        </section>
      )}

      <section className="mt-10">
        <h2 className="mb-4 text-lg font-semibold text-slate-900">Timeline</h2>
        <ol className="space-y-4 border-l-2 border-slate-200 pl-6">
          {timeline.map((entry) => (
            <li key={entry.id} className="relative">
              <span
                className={`absolute -left-[1.94rem] top-1 h-3 w-3 rounded-full ${
                  entry.kind === "delivery_event" ? "bg-sky-400" : "bg-brand-500"
                }`}
                title={entry.kind === "delivery_event" ? "Delivery event" : "Stage transition"}
              />
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
