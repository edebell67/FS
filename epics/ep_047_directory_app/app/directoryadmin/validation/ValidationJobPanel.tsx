"use client";

import { useRef, useState } from "react";
import type { ValidationJobProgress } from "@/lib/validation/repository";
import {
  processValidationJobChunkAction,
  startValidationJobAction,
} from "./actions";

function isActive(job: ValidationJobProgress | null) {
  return job?.status === "pending" || job?.status === "running";
}

export function ValidationJobPanel({ initialJob }: { initialJob: ValidationJobProgress | null }) {
  const [job, setJob] = useState(initialJob);
  const [working, setWorking] = useState(false);
  const [message, setMessage] = useState("");
  const continuing = useRef(false);

  async function continueUntilFinished(jobId: string) {
    if (continuing.current) return;
    continuing.current = true;
    setWorking(true);
    setMessage("");
    try {
      let current: ValidationJobProgress;
      do {
        current = await processValidationJobChunkAction(jobId);
        setJob(current);
        if (current.busy) {
          setMessage("Another request is processing this run. You can safely try again shortly.");
          break;
        }
        // Yield between bounded server actions so the browser paints progress
        // and no single request owns the whole run.
        if (isActive(current)) await new Promise((resolve) => setTimeout(resolve, 150));
      } while (isActive(current));
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "The run paused unexpectedly. It is safe to continue.");
    } finally {
      continuing.current = false;
      setWorking(false);
    }
  }

  async function start() {
    if (working) return;
    setWorking(true);
    setMessage("");
    try {
      const created = await startValidationJobAction();
      setJob(created);
      setWorking(false);
      await continueUntilFinished(created.id);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to start validation.");
      setWorking(false);
    }
  }

  const percent = job?.totalCount
    ? Math.min(100, Math.round((job.processedCount / job.totalCount) * 100))
    : job ? 100 : 0;

  return <section className="mt-6 rounded-lg border border-brand-200 bg-brand-50 p-4">
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h2 className="font-semibold">Active-business validation run</h2>
        {job ? <p className="mt-1 text-sm text-slate-700">
          {job.processedCount.toLocaleString()} / {job.totalCount.toLocaleString()} processed
          {" · "}{job.status.replaceAll("_", " ")}
          {" · "}{job.errorCount.toLocaleString()} errors
        </p> : <p className="mt-1 text-sm text-slate-700">No validation run has been started.</p>}
      </div>
      {!isActive(job) ? <button type="button" onClick={start} disabled={working}
        className="rounded bg-brand-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50">
        {working ? "Starting…" : "Validate all active businesses"}
      </button> : <button type="button" onClick={() => job && continueUntilFinished(job.id)} disabled={working}
        className="rounded bg-brand-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50">
        {working ? "Processing…" : "Continue / resume"}
      </button>}
    </div>
    {job && <div className="mt-3 h-2 overflow-hidden rounded bg-white" role="progressbar"
      aria-label="Business validation progress" aria-valuemin={0} aria-valuemax={job.totalCount}
      aria-valuenow={job.processedCount}>
      <div className="h-full bg-brand-600 transition-[width]" style={{ width: `${percent}%` }}/>
    </div>}
    {message && <p className="mt-3 text-sm text-amber-800">{message}</p>}
    {job?.errors.length ? <details className="mt-3 text-sm">
      <summary className="cursor-pointer font-medium">Recent errors ({job.errorCount})</summary>
      <ul className="mt-2 space-y-1">{job.errors.map((error) =>
        <li key={error.businessId} className="break-words font-mono text-xs">
          {error.businessId}: {error.message}
        </li>)}</ul>
    </details> : null}
  </section>;
}
