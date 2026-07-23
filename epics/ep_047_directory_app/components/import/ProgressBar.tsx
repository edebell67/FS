"use client";

import { Loader2 } from "lucide-react";

export interface ProgressBarProps {
  /** 0-100. Omit (or pass undefined) for the indeterminate "processing" state. */
  percent?: number;
  label: string;
}

export function ProgressBar({ percent, label }: ProgressBarProps) {
  const determinate = typeof percent === "number";

  return (
    <div className="w-full">
      <div className="mb-1.5 flex items-center gap-2 text-sm text-slate-600">
        {!determinate && <Loader2 className="h-4 w-4 animate-spin text-brand-500" aria-hidden="true" />}
        <span>{label}</span>
        {determinate && <span className="ml-auto tabular-nums">{Math.round(percent)}%</span>}
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
        {determinate ? (
          <div
            className="h-full rounded-full bg-brand-500 transition-[width] duration-200"
            style={{ width: `${Math.min(100, Math.max(0, percent))}%` }}
            role="progressbar"
            aria-valuenow={Math.round(percent)}
            aria-valuemin={0}
            aria-valuemax={100}
          />
        ) : (
          <div className="h-full w-full animate-pulse rounded-full bg-brand-400" />
        )}
      </div>
    </div>
  );
}
