"use client";

import { useState } from "react";
import { Trash2, Loader2 } from "lucide-react";

export interface RollbackControlProps {
  batchId: string;
  acceptedCount: number;
}

type State = "idle" | "confirming" | "rolling-back" | "done" | "error";

export function RollbackControl({ batchId, acceptedCount }: RollbackControlProps) {
  const [state, setState] = useState<State>("idle");
  const [deletedCount, setDeletedCount] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (acceptedCount === 0) return null;

  if (state === "done") {
    return (
      <p className="text-sm text-slate-600">
        Rolled back — {deletedCount} business{deletedCount === 1 ? "" : "es"} removed.
      </p>
    );
  }

  async function performRollback() {
    setState("rolling-back");
    setErrorMessage(null);
    try {
      const res = await fetch(`/api/import/${batchId}/rollback`, { method: "POST" });
      if (!res.ok) throw new Error(`Rollback failed (${res.status})`);
      const data = (await res.json()) as { deletedCount: number };
      setDeletedCount(data.deletedCount);
      setState("done");
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : "Rollback failed.");
      setState("error");
    }
  }

  return (
    <div className="flex items-center gap-3">
      {state === "confirming" ? (
        <>
          <span className="text-sm text-slate-600">
            Delete all {acceptedCount} imported business{acceptedCount === 1 ? "" : "es"} from
            this batch?
          </span>
          <button
            onClick={performRollback}
            className="rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700"
          >
            Confirm rollback
          </button>
          <button
            onClick={() => setState("idle")}
            className="rounded-md px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-100"
          >
            Cancel
          </button>
        </>
      ) : (
        <button
          onClick={() => setState("confirming")}
          disabled={state === "rolling-back"}
          className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
        >
          {state === "rolling-back" ? (
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          ) : (
            <Trash2 className="h-4 w-4" aria-hidden="true" />
          )}
          Roll back this import
        </button>
      )}
      {state === "error" && errorMessage && (
        <span className="text-sm text-red-600">{errorMessage}</span>
      )}
    </div>
  );
}
