import Link from "next/link";
import { format } from "date-fns";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { getEligibleVerificationBusinesses, listVerificationBatches } from "@/lib/verification/batches";
import { VerificationBatchBuilder } from "@/components/admin/VerificationBatchBuilder";
import { notFound } from "next/navigation";
import { getValidationPolicy } from "@/lib/validation/repository";

export const dynamic = "force-dynamic";

export default async function VerificationBatchesPage() {
  const user = await requireAdminUserForPage("/directoryadmin/verification-batches");
  if (!canManageVerification(user.role)) notFound();
  const [businesses, batches, policy] = await Promise.all([
    getEligibleVerificationBusinesses(), listVerificationBatches(), getValidationPolicy(),
  ]);
  return <main className="mx-auto max-w-6xl px-6 py-12">
    <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Verification</p>
    <h1 className="mt-1 text-2xl font-semibold">Batch verification</h1>
    <p className="mt-2 text-slate-600">Eligibility is calculated from field validation, independently of the pipeline board. Non-valid records are never selectable. Preparation creates one secure active link per business and never sends a message.</p>
    <div className="mt-8"><VerificationBatchBuilder businesses={businesses} allowPartial={policy.allowPartialVerification}/></div>
    <section className="mt-12"><h2 className="text-lg font-semibold">Recent durable queues</h2>
      <div className="mt-3 space-y-2">{batches.map((batch) =>
        <Link key={batch.id} href={`/directoryadmin/verification-batches/${batch.id}`}
          className="flex justify-between rounded border p-3 text-sm hover:bg-slate-50">
          <span className="font-mono">{batch.id}</span>
          <span>{batch.readyCount}/{batch.totalCount} individually ready · {batch.status} · {format(batch.createdAt, "d MMM yyyy, HH:mm")}</span>
        </Link>)}</div>
    </section>
  </main>;
}
