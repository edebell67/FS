"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

type Outcome = { sent: number; failed: number; skipped: number };

export function VerificationBatchSendPanel({ batchId, readyCount, canSend, reason }: {
  batchId: string; readyCount: number; canSend: boolean; reason: string;
}) {
  const router = useRouter();
  const [confirmed, setConfirmed] = useState(false);
  const [sending, setSending] = useState(false);
  const [outcome, setOutcome] = useState<Outcome | null>(null);
  const [error, setError] = useState<string | null>(null);
  const enabled = canSend && readyCount > 0 && confirmed && !sending;

  async function send() {
    if (!enabled) return;
    setSending(true); setError(null); setOutcome(null);
    try {
      const response = await fetch(`/directoryadmin/api/verification-batches/${batchId}/send`, {
        method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ confirmed: true }),
      });
      const result = await response.json() as Outcome & { error?: string };
      if (!response.ok) throw new Error(result.error || "Unable to send verification batch.");
      setOutcome(result); router.refresh();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to send verification batch.");
    } finally { setSending(false); }
  }

  return <section className="mt-5 rounded border border-brand-200 bg-brand-50 p-4 text-sm">
    <h2 className="font-semibold text-[#152022]">Send prepared verification emails</h2>
    <p className="mt-1 text-slate-700">This sends up to {readyCount} individual branded emails through Gmail to the businesses&apos; currently recorded addresses. Each email gets a freshly issued one-time verification link. Sending is intentional and does not prove recipient delivery.</p>
    <label className="mt-3 flex items-start gap-3">
      <input type="checkbox" checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} className="mt-1 h-5 w-5" />
      <span>I confirm that I want to send this batch now.</span>
    </label>
    {!canSend && <p className="mt-2 text-red-700">Cannot send: {reason}</p>}
    <button type="button" disabled={!enabled} onClick={send}
      className="mt-4 min-h-11 rounded bg-[#00765e] px-4 py-2 font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-400">
      {sending ? "Sending…" : `Send ${readyCount} verification email${readyCount === 1 ? "" : "s"}`}
    </button>
    {outcome && <p className="mt-3 font-medium">Batch result — sent: {outcome.sent}; failed: {outcome.failed}; skipped: {outcome.skipped}.</p>}
    {error && <p className="mt-3 text-red-700">{error}</p>}
  </section>;
}
