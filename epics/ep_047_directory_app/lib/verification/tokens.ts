import { createHash, randomBytes } from "node:crypto";

export const DEFAULT_EXPIRY_DAYS = 5;
export const MIN_EXPIRY_DAYS = 1;
export const MAX_EXPIRY_DAYS = 14;

export function generateVerificationToken(): string {
  return randomBytes(32).toString("base64url");
}

export function hashVerificationToken(token: string): string {
  return createHash("sha256").update(token).digest("hex");
}

export function isValidRawToken(token: string): boolean {
  return /^[A-Za-z0-9_-]{43}$/.test(token);
}

export function normalizeExpiryDays(value: unknown): number {
  const days = Number(value ?? DEFAULT_EXPIRY_DAYS);
  if (!Number.isInteger(days) || days < MIN_EXPIRY_DAYS || days > MAX_EXPIRY_DAYS) {
    throw new Error(`Expiry must be between ${MIN_EXPIRY_DAYS} and ${MAX_EXPIRY_DAYS} days.`);
  }
  return days;
}
