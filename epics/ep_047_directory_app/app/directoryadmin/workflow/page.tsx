import Link from "next/link";
import { requireAdminUserForPage } from "@/lib/auth/require";

const steps = [
  ["1", "Import businesses", "/directoryadmin/import", "Choose a source file and import records."],
  ["2", "Run field validation", "/directoryadmin/validation", "Processes only records awaiting validation."],
  ["3", "Select verification batch", "/directoryadmin/verification-batches", "Uses validated businesses only."],
  ["4", "Review claims", "/directoryadmin/claims", "Uses pending claims only."],
  ["5", "Generate sites", "/directoryadmin/pipeline", "Uses businesses awaiting site generation only."],
  ["6", "Send site preview links", "/directoryadmin/site-previews", "Uses eligible Ready for Preview businesses only."],
] as const;

export const dynamic = "force-dynamic";
export default async function WorkflowPage() {
  await requireAdminUserForPage("/directoryadmin/workflow");
  return <main className="mx-auto max-w-xl px-4 sm:px-6 py-8 sm:py-10"><Link href="/directoryadmin/pipeline" className="text-sm text-brand-700 hover:underline">← Pipeline</Link><h1 className="mt-4 text-2xl font-semibold">Workflow control</h1><p className="mt-2 text-sm text-slate-600">Run the business journey in order. Each control opens its protected action screen and only operates on eligible records.</p><div className="mt-6 space-y-3">{steps.map(([number,title,href,description])=><Link key={href} href={href} className="block rounded-xl border border-slate-200 bg-white p-4 shadow-sm hover:border-brand-500 hover:bg-brand-50"><span className="text-xs font-semibold text-brand-700">STEP {number}</span><strong className="mt-1 block">{title}</strong><span className="mt-1 block text-sm text-slate-600">{description}</span></Link>)}</div></main>;
}
