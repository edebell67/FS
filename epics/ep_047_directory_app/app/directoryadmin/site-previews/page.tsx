/**
 * app/directoryadmin/site-previews/page.tsx — Authorized admin controls for preview and owner-review email delivery.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-08-05 · Adds the explicit owner-review invitation reissue panel for Ready for Preview businesses, including previously notified records.
 * v1.0.0 · 2026-08-05 · Version history added; file predates this convention.
 */
import Link from "next/link";
import { notFound } from "next/navigation";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { getBusinessesReadyForOwnerReviewInvitation, getBusinessesReadyForPreviewNotification } from "@/lib/verification/site-generation";
import { sendOwnerReviewInvitationAction, sendSelectedPreviewLinksAction } from "./actions";

export const dynamic = "force-dynamic";

type Candidate = { id: string; businessRef: string; businessName: string; email: string | null; generatedSiteUrl: string | null };

function CandidateTable({ businesses }: { businesses: Candidate[] }) {
  return <div className="overflow-x-auto rounded-xl border border-slate-200"><table className="w-full text-left text-sm"><thead className="bg-slate-50"><tr><th className="p-3">Select</th><th className="p-3">Business</th><th className="p-3">Recipient</th><th className="p-3">Live preview</th></tr></thead><tbody>{businesses.map((business) => <tr key={business.id} className="border-t"><td className="p-3"><input type="checkbox" name="businessId" value={business.id} aria-label={`Select ${business.businessName}`} /></td><td className="p-3"><strong>{business.businessName}</strong><span className="block font-mono text-xs text-slate-500">{business.businessRef}</span></td><td className="p-3">{business.email}</td><td className="p-3"><a className="text-brand-700 underline" href={business.generatedSiteUrl!} target="_blank">Open preview</a></td></tr>)}</tbody></table></div>;
}

export default async function SitePreviewsPage({ searchParams }: { searchParams: Promise<{ error?: string; sent?: string; skipped?: string; reviewError?: string; reviewSent?: string; reviewSkipped?: string }> }) {
  const user = await requireAdminUserForPage("/directoryadmin/site-previews");
  if (!canManageVerification(user.role)) notFound();
  const [initialCandidates, reviewCandidates, params] = await Promise.all([
    getBusinessesReadyForPreviewNotification(),
    getBusinessesReadyForOwnerReviewInvitation(),
    searchParams,
  ]);

  return <main className="mx-auto max-w-6xl px-4 py-8">
    <Link href="/directoryadmin/pipeline" className="text-sm text-brand-700 hover:underline">← Pipeline</Link>
    <h1 className="mt-4 text-2xl font-semibold">Send site preview links</h1>
    <p className="mt-2 text-sm text-slate-600">Initial preview delivery lists Ready for Preview records with a saved live URL, recipient email, and no successful preview-ready delivery.</p>
    {params.error === "selection" && <p role="alert" className="mt-4 rounded border border-amber-300 bg-amber-50 p-3">Select at least one business.</p>}
    {params.error === "confirm" && <p role="alert" className="mt-4 rounded border border-amber-300 bg-amber-50 p-3">Confirm the selected preview links before sending.</p>}
    {params.sent && <p role="status" className="mt-4 rounded border border-green-300 bg-green-50 p-3">Sent: {params.sent}. Skipped: {params.skipped ?? "0"}. Check delivery status before treating recipients as informed.</p>}
    <form action={sendSelectedPreviewLinksAction} className="mt-6">
      {initialCandidates.length ? <CandidateTable businesses={initialCandidates} /> : <p className="rounded-xl border border-slate-200 p-8 text-center text-slate-500">No initial preview deliveries are eligible.</p>}
      {initialCandidates.length > 0 && <section className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-5"><label className="flex gap-2 text-sm"><input type="checkbox" name="confirmed" />I reviewed the selected recipients and preview URLs. Send the selected site preview links.</label><button className="mt-4 rounded bg-brand-700 px-4 py-2 font-medium text-white">Send site preview links</button></section>}
    </form>

    <section className="mt-12 border-t pt-8">
      <h2 className="text-xl font-semibold">Send owner-review invitation</h2>
      <p className="mt-2 text-sm text-slate-600">This is a separate, deliberate email that mints a fresh one-time review link. It includes Ready for Preview businesses that were already sent a preview-ready email and does not move their pipeline state.</p>
      {params.reviewError === "selection" && <p role="alert" className="mt-4 rounded border border-amber-300 bg-amber-50 p-3">Select at least one recipient for an owner-review invitation.</p>}
      {params.reviewError === "confirm" && <p role="alert" className="mt-4 rounded border border-amber-300 bg-amber-50 p-3">Explicitly confirm the selected owner-review invitations before sending.</p>}
      {params.reviewSent && <p role="status" className="mt-4 rounded border border-green-300 bg-green-50 p-3">Owner-review invitations sent: {params.reviewSent}. Skipped: {params.reviewSkipped ?? "0"}.</p>}
      <form action={sendOwnerReviewInvitationAction} className="mt-6">
        {reviewCandidates.length ? <CandidateTable businesses={reviewCandidates} /> : <p className="rounded-xl border border-slate-200 p-8 text-center text-slate-500">No Ready for Preview businesses with a recipient and live URL are available.</p>}
        {reviewCandidates.length > 0 && <section className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-5"><label className="flex gap-2 text-sm"><input type="checkbox" name="confirmed" />I reviewed the selected recipients and live preview URLs. Send a separate owner-review invitation with a new one-time link.</label><button className="mt-4 rounded bg-brand-700 px-4 py-2 font-medium text-white">Send owner-review invitation</button></section>}
      </form>
    </section>
  </main>;
}
