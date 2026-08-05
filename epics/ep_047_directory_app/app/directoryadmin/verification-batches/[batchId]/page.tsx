import { notFound } from "next/navigation";
import { format } from "date-fns";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { getVerificationBatch } from "@/lib/verification/batches";

export const dynamic = "force-dynamic";

export default async function VerificationBatchPage({ params }: { params: Promise<{ batchId: string }> }) {
  const { batchId } = await params;
  const user = await requireAdminUserForPage(`/directoryadmin/verification-batches/${batchId}`);
  if (!canManageVerification(user.role)) notFound();
  const batch = await getVerificationBatch(batchId);
  if (!batch) notFound();
  const batchReady = batch.readyCount === batch.totalCount && batch.delivery.canSend;
  return <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
    <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Verification audit</p>
    <h1 className="mt-1 text-2xl font-semibold">Batch queue</h1>
    <p className="mt-2 font-mono text-xs text-slate-500">{batch.id}</p>
    <div className="mt-5 rounded border p-4 text-sm">
      <p>Status: <strong>{batch.status}</strong> · individually ready: <strong>{batch.readyCount}/{batch.totalCount}</strong> · batch send readiness: <strong>{batchReady ? "ready" : "not ready"}</strong></p>
      <p className="mt-1 text-slate-600">Outbound delivery: {batch.delivery.reason} Raw secure tokens are intentionally not retained in this audit view.</p>
    </div>
    <div role="region" aria-label="Verification batch items" tabIndex={0} className="mt-5 overflow-x-auto"><table className="min-w-max w-full text-left text-sm"><thead>
      <tr className="border-b"><th className="p-2">Business</th><th className="p-2">Recipient route</th><th className="p-2">Expiry</th><th className="p-2">Status</th><th className="p-2">Individual readiness</th></tr>
    </thead><tbody>{batch.items.map((item) => <tr key={item.id} className="border-b">
      <td className="p-2">{item.businessName}<div className="font-mono text-xs">{item.businessRef}</div></td>
      <td className="p-2">{item.recipientChannel}: {item.recipientAddress || "not configured"}</td>
      <td className="p-2">{format(item.expiresAt, "d MMM yyyy, HH:mm")}</td>
      <td className="p-2">{item.status}</td>
      <td className="p-2">{item.readiness}{item.readinessReason && <div className="text-xs text-red-700">{item.readinessReason}</div>}</td>
    </tr>)}</tbody></table></div>
  </main>;
}
