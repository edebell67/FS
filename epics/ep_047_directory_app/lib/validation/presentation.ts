import type { ValidationJobProgress } from "./repository";

export const VALIDATION_TIME_ZONE = "Europe/London";

export function formatValidationTimestamp(value: Date | null): string {
  if (!value) return "—";
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "long",
    timeZone: VALIDATION_TIME_ZONE,
  }).format(value) + ` (${VALIDATION_TIME_ZONE})`;
}

export function formatValidationDuration(job: Pick<ValidationJobProgress, "startedAt" | "completedAt">): string {
  if (!job.startedAt) return "—";
  const end = job.completedAt ?? new Date();
  const seconds = Math.max(0, Math.round((end.getTime() - job.startedAt.getTime()) / 1000));
  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;
  if (minutes < 60) return remainder ? `${minutes}m ${remainder}s` : `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  const minuteRemainder = minutes % 60;
  return minuteRemainder ? `${hours}h ${minuteRemainder}m` : `${hours}h`;
}

export function formatValidationStatus(status: string): string {
  return status.replaceAll("_", " ");
}
