import { notFound } from "next/navigation";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification, getClaimForReview } from "@/lib/verification/repository";
import { approveClaimAction } from "./actions";
export const dynamic = "force-dynamic";
export default async function ReviewPage({ params }: { params: Promise<{ claimRequestId: string }> }) {
  const { claimRequestId } = await params;
  const user = await requireAdminUserForPage(`/directoryadmin/verifications/${claimRequestId}`);
  if (!canManageVerification(user.role)) return <main className="p-12">Forbidden.</main>;
  const claim = await getClaimForReview(claimRequestId);
  if (!claim) notFound();
  const approve = approveClaimAction.bind(null, claimRequestId);
  return <main className="mx-auto max-w-3xl px-6 py-12"><p className="text-sm font-medium text-brand-600">Admin — Claim review</p>
    <h1 className="mt-1 text-2xl font-semibold">{claim.businessName}</h1>
    <dl className="mt-6 grid gap-2 rounded border p-4 text-sm"><div><dt className="text-slate-500">Status</dt><dd>{claim.status}</dd></div>
      <div><dt className="text-slate-500">Requester</dt><dd>{claim.requesterName} · {claim.relationship}</dd></div>
      <div><dt className="text-slate-500">Contact</dt><dd>{claim.contactEmail || claim.contactPhone || "Not supplied"}</dd></div></dl>
    <h2 className="mt-6 font-semibold">Submitted corrections (not yet published)</h2>
    <pre className="mt-2 overflow-auto rounded bg-slate-50 p-4 text-xs">{JSON.stringify(claim.submittedFields, null, 2)}</pre>
    {claim.status === "pending" && <form action={approve} className="mt-6"><label className="block text-sm">Decision note<textarea name="note" className="mt-1 block w-full rounded border p-2" /></label>
      <button className="mt-3 rounded bg-green-700 px-4 py-2 font-medium text-white">Approve claim manually</button></form>}
  </main>;
}
