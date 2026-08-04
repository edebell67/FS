"use client";

import { useState } from "react";
import { runWorkflowOperation, type WorkflowOperation } from "@/app/directoryadmin/workflow/actions";

type Counts = { awaitingValidation: number; verificationEligible: number; pendingClaims: number; awaitingGeneration: number; previewEligible: number };

const actionText: Record<WorkflowOperation, string> = {
  validate: "Run field validation",
  "prepare-verification": "Prepare verification batch",
  "approve-claims": "Review and approve claims",
  generate: "Run site generation",
  "send-previews": "Send site preview links",
};

export function WorkflowControlModal({ counts, generationAvailable }: { counts: Counts; generationAvailable: boolean }) {
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState<WorkflowOperation | null>(null);
  const [result, setResult] = useState<string>("");

  async function run(operation: WorkflowOperation, detail: string) {
    if (!window.confirm(`${actionText[operation]}?\n\n${detail}\n\nOnly records still eligible on the server will be processed.`)) return;
    setBusy(operation); setResult("");
    try {
      const response = await runWorkflowOperation(operation, true);
      setResult(response.message);
    } catch (error) {
      setResult(error instanceof Error ? error.message : "Workflow operation failed.");
    } finally { setBusy(null); }
  }

  function openImport() {
    if (window.confirm("Open business import?\n\nYou will choose a CSV or JSON file on the protected importer page.")) window.location.assign("/directoryadmin/import");
  }

  return <>
    <button type="button" onClick={() => setOpen(true)} className="inline-block rounded bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700">Open workflow control</button>
    {open && <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 p-4" role="presentation" onMouseDown={() => !busy && setOpen(false)}>
      <section role="dialog" aria-modal="true" aria-labelledby="workflow-control-title" className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-xl bg-white p-6 shadow-2xl" onMouseDown={(event) => event.stopPropagation()}>
        <div className="flex items-start justify-between gap-4"><div><p className="text-xs font-semibold uppercase tracking-wide text-brand-700">Admin-only control</p><h2 id="workflow-control-title" className="mt-1 text-xl font-semibold">Business lifecycle workflow</h2><p className="mt-2 text-sm text-slate-600">Run in order. Every operation asks for confirmation and re-checks eligibility on the server.</p></div><button type="button" onClick={() => setOpen(false)} disabled={Boolean(busy)} aria-label="Close workflow control" className="rounded px-2 text-xl text-slate-500 hover:bg-slate-100">×</button></div>
        <div className="mt-6 space-y-3">
          <Step number="1" label="Import businesses" detail="Upload a CSV or JSON file; accepted rows begin in Imported." onClick={openImport} />
          <Step number="2" label="Run field validation" detail={`${counts.awaitingValidation.toLocaleString()} awaiting validation`} onClick={() => run("validate", `This starts and processes a bounded validation job for currently eligible records.`)} busy={busy === "validate"} />
          <Step number="3" label="Prepare verification batch" detail={`${counts.verificationEligible.toLocaleString()} validated active businesses eligible`} onClick={() => run("prepare-verification", `This prepares secure verification links for all currently validated active businesses. It does not send email.`)} busy={busy === "prepare-verification"} />
          <Step number="4" label="Send verification emails" detail="Separate capability confirmation required; raw verification capabilities are intentionally not persisted." disabled />
          <Step number="5" label="Review and approve claims" detail={`${counts.pendingClaims.toLocaleString()} claims pending review`} onClick={() => run("approve-claims", `This approves all claims still pending review, uses the protected claim-approval service, and queues approved businesses for generation.`)} busy={busy === "approve-claims"} />
          <Step number="6" label="Run site generation" detail={generationAvailable ? `${counts.awaitingGeneration.toLocaleString()} businesses awaiting generation` : "No configured authenticated generation path — completion is disabled."} onClick={() => run("generate", `This only runs the actual configured generation loop. Completion is recorded only after a generated site URL exists.`)} busy={busy === "generate"} disabled={!generationAvailable} />
          <Step number="7" label="Send site preview links" detail={`${counts.previewEligible.toLocaleString()} Ready for Preview businesses eligible`} onClick={() => run("send-previews", `This sends previews only for records still Ready for Preview, with a generated URL, recipient email, and no prior preview message.`)} busy={busy === "send-previews"} />
        </div>
        {result && <p role="status" className="mt-5 rounded border border-brand-200 bg-brand-50 p-3 text-sm text-slate-800">{result}</p>}
      </section>
    </div>}
  </>;
}

function Step({ number, label, detail, onClick, busy, disabled }: { number: string; label: string; detail: string; onClick?: () => void; busy?: boolean; disabled?: boolean }) {
  return <button type="button" onClick={onClick} disabled={busy || disabled} className="block w-full rounded-lg border border-slate-200 p-4 text-left hover:border-brand-500 hover:bg-brand-50 disabled:cursor-not-allowed disabled:opacity-60"><span className="text-xs font-semibold text-brand-700">STEP {number}</span><strong className="mt-1 block text-slate-900">{busy ? "Working…" : label}</strong><span className="mt-1 block text-sm text-slate-600">{detail}</span></button>;
}
