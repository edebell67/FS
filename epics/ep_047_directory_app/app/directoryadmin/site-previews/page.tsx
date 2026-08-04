import Link from "next/link";
import { notFound } from "next/navigation";
import { requireAdminUserForPage } from "@/lib/auth/require";
import { canManageVerification } from "@/lib/verification/repository";
import { getBusinessesReadyForPreviewNotification } from "@/lib/verification/site-generation";
import { sendSelectedPreviewLinksAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function SitePreviewsPage({ searchParams }: { searchParams: Promise<{ error?: string; sent?: string; skipped?: string }> }) {
  const user = await requireAdminUserForPage("/directoryadmin/site-previews");
  if (!canManageVerification(user.role)) notFound();
  const [eligible, params] = await Promise.all([getBusinessesReadyForPreviewNotification(), searchParams]);
  return <main className="mx-auto max-w-6xl px-4 py-8"><Link href="/directoryadmin/pipeline" className="text-sm text-brand-700 hover:underline">← Pipeline</Link><h1 className="mt-4 text-2xl font-semibold">Send site preview links</h1><p className="mt-2 text-sm text-slate-600">Only Ready for Preview records with a saved live URL, recipient email, and no prior preview delivery appear here.</p>
    {params.error === "selection" && <p role="alert" className="mt-4 rounded border border-amber-300 bg-amber-50 p-3">Select at least one business.</p>}
    {params.error === "confirm" && <p role="alert" className="mt-4 rounded border border-amber-300 bg-amber-50 p-3">Confirm the selected preview links before sending.</p>}
    {params.sent && <p role="status" className="mt-4 rounded border border-green-300 bg-green-50 p-3">Sent: {params.sent}. Skipped: {params.skipped ?? "0"}. Check delivery status before treating recipients as informed.</p>}
    <form action={sendSelectedPreviewLinksAction} className="mt-6"><div className="overflow-x-auto rounded-xl border border-slate-200"><table className="w-full text-left text-sm"><thead className="bg-slate-50"><tr><th className="p-3">Select</th><th className="p-3">Business</th><th className="p-3">Recipient</th><th className="p-3">Live preview</th></tr></thead><tbody>{eligible.map(b=><tr key={b.id} className="border-t"><td className="p-3"><input type="checkbox" name="businessId" value={b.id} aria-label={`Select ${b.businessName}`} /></td><td className="p-3"><strong>{b.businessName}</strong><span className="block font-mono text-xs text-slate-500">{b.businessRef}</span></td><td className="p-3">{b.email}</td><td className="p-3"><a className="text-brand-700 underline" href={b.generatedSiteUrl!} target="_blank">Open preview</a></td></tr>)}{!eligible.length&&<tr><td colSpan={4} className="p-8 text-center text-slate-500">No eligible Ready for Preview businesses.</td></tr>}</tbody></table></div>{eligible.length>0&&<section className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-5"><label className="flex gap-2 text-sm"><input type="checkbox" name="confirmed" />I reviewed the selected recipients and preview URLs. Send the selected site preview links.</label><button className="mt-4 rounded bg-brand-700 px-4 py-2 font-medium text-white">Send site preview links</button></section>}</form></main>;
}
