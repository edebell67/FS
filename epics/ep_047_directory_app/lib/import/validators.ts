// Field-level validators. Deliberately conservative — reject obvious garbage,
// don't try to be the last word on RFC 5322 or E.164. Each function returns
// a boolean rather than throwing; the pipeline decides what a failure means.

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function isValidEmail(value: string): boolean {
  return EMAIL_RE.test(value.trim());
}

export function isValidWebsite(value: string): boolean {
  const trimmed = value.trim();
  const candidate = /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;
  try {
    const url = new URL(candidate);
    return /\./.test(url.hostname) && url.hostname.length > 3;
  } catch {
    return false;
  }
}

/**
 * Accepts UK-style and loosely international phone numbers: optional leading
 * +, digits, spaces, hyphens, parentheses, 7-15 digits total. Open question
 * in PLAN.md §5 (UK-only vs international) will tighten this once answered.
 */
export function isValidPhone(value: string): boolean {
  const trimmed = value.trim();
  if (!/^[+\d][\d\s().-]*$/.test(trimmed)) return false;
  const digits = trimmed.replace(/\D/g, "");
  return digits.length >= 7 && digits.length <= 15;
}

export function normalizePhone(value: string): string {
  return value.trim().replace(/[^\d+]/g, "");
}

export function isValidLatitude(value: number): boolean {
  return Number.isFinite(value) && value >= -90 && value <= 90;
}

export function isValidLongitude(value: number): boolean {
  return Number.isFinite(value) && value >= -180 && value <= 180;
}
