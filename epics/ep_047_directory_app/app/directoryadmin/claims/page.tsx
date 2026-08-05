import Link from "next/link";
import { notFound } from "next/navigation";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { listPendingClaims } from "@/lib/verification/claims-approval";
import { approveSelectedClaimsAction, sendPreparedClaimSuccessMessagesAction } from "./actions";

export const dynamic = "force-dynamic";
export default async function ClaimsPage({ searchParams }: { searchParams: Promise<{ approved?: string; messages?: string; error?: string }> }) {
  const user = await requireAdminUserForPage("/directoryadmin/claims");
  if (!canManageVerification(user.role)) notFound();
  const [claims, params] = await Promise.all([listPendingClaims(), searchParams]);
  return <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-12"><p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Ownership</p>
    <div className="mt-1 flex flex-wrap items-end justify-between gap-3"><div><h1 className="break-words text-2xl font-semibold">Claims needing review</h1><p className="mt-2 text-slate-600">Claims submitted by businesses remain Claims pending until an authorised reviewer approves them.</p></div>
      <span className="rounded-full bg-amber-100 px-3 py-1 text-sm font-semibold text-amber-900">{claims.length} Claims pending</span></div>
    {params.error === "select" && <p role="alert" className="mt-5 rounded border border-amber-300 bg-amber-50 p-3 text-sm text-amber-950">Select at least one pending claim before approving.</p>}
    {params.error === "confirm" && <p role="alert" className="mt-5 rounded border border-amber-300 bg-amber-50 p-3 text-sm text-amber-950">Confirm that you reviewed the selected claims before approving.</p>}
    {params.approved && <p role="status" className="mt-5 rounded border border-green-300 bg-green-50 p-3 text-sm text-green-900">Selected claims were approved. Their listings are now Claimed; owner messages are recorded separately as prepared or not ready.</p>}
    {params.messages && <p role="status" className="mt-3 rounded border border-blue-300 bg-blue-50 p-3 text-sm text-blue-900">Prepared claim-success messages were handed to the configured delivery policy. Check message status before calling them delivered.</p>}
    <form action={sendPreparedClaimSuccessMessagesAction} className="mt-4"><button className="rounded border border-blue-600 px-3 py-2 text-sm font-medium text-blue-800 hover:bg-blue-50">Send prepared claim-success messages</button></form>
    <form action={approveSelectedClaimsAction} className="mt-8"><div role="region" aria-label="Pending claims table" tabIndex={0} className="overflow-x-auto rounded-xl border border-slate-200"><table className="min-w-max w-full text-left text-sm"><thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500"><tr>
      <th className="px-4 py-3"><input aria-label="Select all pending claims" type="checkbox" data-select-all /></th><th className="px-4 py-3">Business</th><th className="px-4 py-3">Claimant</th><th className="px-4 py-3">Contact route</th><th className="px-4 py-3">Submitted</th></tr></thead><tbody className="divide-y divide-slate-100">
      {claims.map((claim) => <tr key={claim.id}><td className="px-4 py-3"><input name="claimId" value={claim.id} type="checkbox" data-claim /></td><td className="px-4 py-3"><Link className="font-medium text-brand-700 hover:underline" href={`/directoryadmin/verifications/${claim.id}`}>{claim.businessName}</Link><span className="block font-mono text-xs text-slate-400">{claim.businessRef}</span></td><td className="px-4 py-3">{claim.requesterName}<span className="block text-xs text-slate-500">{claim.relationship}</span></td><td className="px-4 py-3">{claim.contactEmail || claim.contactPhone || <span className="text-amber-700">No email supplied</span>}</td><td className="whitespace-nowrap px-4 py-3 text-slate-500">{claim.createdAt.toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" })}</td></tr>)}
      {claims.length === 0 && <tr><td colSpan={5} className="px-4 py-12 text-center text-slate-500">No claims are pending review.</td></tr>}</tbody></table></div>
      {claims.length > 0 && <section className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-5"><h2 className="font-semibold">Approve selected claims</h2><p className="mt-1 text-sm text-slate-700">This changes each selected business to <strong>Claimed</strong> and records its reviewer, decision note, and pipeline transition. A claimed-listing owner message is prepared for every claim with an email; prepared does not mean sent.</p><label className="mt-4 block text-sm font-medium">Decision note<textarea name="note" className="mt-1 block w-full rounded border border-amber-300 bg-white p-2" /></label><label className="mt-4 flex gap-2 text-sm"><input required type="checkbox" name="confirmed"/><span>I reviewed the selected claims and confirm they should become Claimed.</span></label><button className="mt-4 rounded bg-green-700 px-4 py-2 font-medium text-white">Approve selected claims</button></section>}
    </form><script dangerouslySetInnerHTML={{ __html: `document.querySelector('[data-select-all]')?.addEventListener('change',(e)=>document.querySelectorAll('[data-claim]').forEach((x)=>x.checked=e.target.checked));` }} /></main>;
}
