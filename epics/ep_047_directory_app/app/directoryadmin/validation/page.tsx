import Link from "next/link";
import { notFound } from "next/navigation";
import { requireAdminUserForPage } from "@/lib/auth/require";
import {
  canManageValidation, getLatestValidationJob, getValidationPolicy, listRepairQueue, listValidationRules,
} from "@/lib/validation/repository";
import { RULE_TYPES, VALIDATABLE_FIELDS } from "@/lib/validation/types";
import {
  applyFieldRepairAction, runBusinessValidationAction,
  saveValidationRuleAction, setPartialPolicyAction,
} from "./actions";
import { ValidationJobPanel } from "./ValidationJobPanel";

export const dynamic = "force-dynamic";

export default async function ValidationAdminPage() {
  const user = await requireAdminUserForPage("/directoryadmin/validation");
  if (!canManageValidation(user.role)) notFound();
  const [rules, policy, queue, validationJob] = await Promise.all([
    listValidationRules(), getValidationPolicy(), listRepairQueue(), getLatestValidationJob(),
  ]);
  return <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
    <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Admin — Data quality</p>
    <div className="flex flex-wrap items-end justify-between gap-3">
      <div><h1 className="mt-1 text-2xl font-semibold">Field validation and repair</h1>
        <p className="mt-2 text-slate-600">Rules produce immutable field outcomes and calculated record eligibility.</p></div>
    </div>
    <ValidationJobPanel initialJob={validationJob}/>

    <section className="mt-8 rounded-lg border p-4">
      <h2 className="font-semibold">Protected partial-verification policy</h2>
      <form action={setPartialPolicyAction} className="mt-3 flex flex-col gap-3 text-sm sm:flex-row sm:items-center">
        <label className="flex items-center gap-2"><input type="checkbox" name="allowPartial" defaultChecked={policy.allowPartialVerification}/>
          Permit explicit selection of clearly marked partially validated records</label>
        <button className="rounded border px-3 py-1.5 font-medium">Save policy</button>
      </form>
    </section>

    <section className="mt-8"><h2 className="text-lg font-semibold">Active rules</h2>
      <div role="region" aria-label="Active validation rules" tabIndex={0} className="mt-3 overflow-x-auto"><table className="min-w-max w-full text-left text-sm"><thead><tr className="border-b">
        <th className="p-2">Field</th><th className="p-2">Rule</th><th className="p-2">Mandatory</th>
        <th className="p-2">Blocks verification</th><th className="p-2">Parameters</th>
      </tr></thead><tbody>{rules.map((rule) => <tr key={rule.id} className="border-b">
        <td className="p-2">{rule.label}<div className="font-mono text-xs text-slate-500">{rule.fieldName}</div></td>
        <td className="p-2">{rule.ruleType}</td><td className="p-2">{rule.mandatory ? "Yes" : "No"}</td>
        <td className="p-2">{rule.blocksVerification ? "Yes" : "No"}</td>
        <td className="p-2 font-mono text-xs">{JSON.stringify(rule.parameters)}</td>
      </tr>)}</tbody></table></div>
      <form action={saveValidationRuleAction} className="mt-4 grid gap-3 rounded-lg bg-slate-50 p-4 sm:grid-cols-2 lg:grid-cols-4">
        <label className="text-sm">Field<select name="fieldName" className="mt-1 block w-full rounded border px-2 py-2">
          {VALIDATABLE_FIELDS.map((field) => <option key={field}>{field}</option>)}</select></label>
        <label className="text-sm">Label<input name="label" required className="mt-1 block w-full rounded border px-2 py-2"/></label>
        <label className="text-sm">Rule type<select name="ruleType" className="mt-1 block w-full rounded border px-2 py-2">
          {RULE_TYPES.map((type) => <option key={type}>{type}</option>)}</select></label>
        <label className="text-sm">Regex pattern<input name="pattern" className="mt-1 block w-full rounded border px-2 py-2"/></label>
        <label className="text-sm">Minimum<input name="min" type="number" step="any" className="mt-1 block w-full rounded border px-2 py-2"/></label>
        <label className="text-sm">Maximum<input name="max" type="number" step="any" className="mt-1 block w-full rounded border px-2 py-2"/></label>
        <label className="flex items-center gap-2 text-sm"><input type="checkbox" name="mandatory"/>Mandatory</label>
        <label className="flex items-center gap-2 text-sm"><input type="checkbox" name="blocksVerification"/>Failure blocks verification</label>
        <button className="rounded bg-slate-900 px-4 py-2 text-sm font-medium text-white sm:col-span-2 lg:col-span-4">Add or replace rule</button>
      </form>
    </section>

    <section className="mt-10"><h2 className="text-lg font-semibold">Outstanding field repair queue</h2>
      <div className="mt-3 space-y-3">{queue.map((item) => <article key={item.outcomeId} className="rounded-lg border border-amber-200 p-4">
        <div className="flex flex-wrap justify-between gap-2"><div>
          <Link href={`/directoryadmin/businesses/${item.businessRef}`} className="font-medium text-brand-700">{item.businessName}</Link>
          <p className="text-sm"><strong>{item.fieldName}</strong>: {item.sourceValue || "blank"} · {item.message}</p>
        </div><span className="text-sm">{item.validationStatus}</span></div>
        <form action={applyFieldRepairAction} className="mt-3 grid gap-2 sm:grid-cols-[1fr_1fr_auto]">
          <input type="hidden" name="businessId" value={item.businessId}/><input type="hidden" name="outcomeId" value={item.outcomeId}/>
          <input type="hidden" name="fieldName" value={item.fieldName}/>
          <input name="proposedValue" aria-label={`Replacement ${item.fieldName}`} placeholder="Replacement value" required className="rounded border px-3 py-2 text-sm"/>
          <input name="evidence" aria-label={`Evidence ${item.fieldName}`} placeholder="Evidence/source for correction" required className="rounded border px-3 py-2 text-sm"/>
          <button className="rounded bg-brand-600 px-4 py-2 text-sm font-medium text-white">Apply and revalidate</button>
        </form>
        <form action={runBusinessValidationAction} className="mt-2"><input type="hidden" name="businessId" value={item.businessId}/>
          <button className="text-xs font-medium text-brand-700">Re-run without repair</button></form>
      </article>)}
      {queue.length === 0 && <p className="rounded border p-6 text-center text-slate-500">No outstanding fields in latest validation runs.</p>}</div>
    </section>
  </main>;
}
