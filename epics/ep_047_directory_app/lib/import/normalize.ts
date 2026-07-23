// Turns one RawRow (arbitrary column names, string/number/null values) into
// either a validated BusinessInput or a list of blocking RowIssues. This is
// where column-alias resolution, required-field checks, and per-field
// validation (email/website/phone/lat/lng) all happen — one row at a time,
// independent of source format, independent of the DB.
//
// Two different outcomes for a bad value, and they're not the same thing:
//   - a missing REQUIRED field (businessName, category) blocks the row —
//     there's nothing useful to import.
//   - a malformed OPTIONAL field (bad email/phone/website/number) does not
//     block the row. The field is dropped and the row is still imported,
//     with a warning recorded so it shows up in the error report. A business
//     with a malformed phone number is still a real business; rejecting the
//     whole row over one messy column punishes every other correct field on
//     it (real import data confirmed this isn't hypothetical — see the 58
//     "01213733439, 01213733196"-style multi-number phone fields in
//     UK_Ltd_email_no_website_VERIFIED_410.csv).

import { COLUMN_ALIASES, REQUIRED_FIELDS, type BusinessInput, type RawRow, type RowIssue } from "./types";
import { isValidEmail, isValidLatitude, isValidLongitude, isValidPhone, isValidWebsite } from "./validators";

function toStringValue(value: RawRow[string]): string | undefined {
  if (value === null || value === undefined) return undefined;
  const str = String(value).trim();
  return str.length > 0 ? str : undefined;
}

function toNumberValue(value: RawRow[string]): number | undefined {
  if (value === null || value === undefined || value === "") return undefined;
  const num = typeof value === "number" ? value : Number(value);
  return Number.isFinite(num) ? num : NaN; // NaN signals "present but invalid", not "absent"
}

export interface NormalizeResult {
  input?: BusinessInput;
  /** Blocking — row was not imported. Only ever missing_required_field. */
  issues: RowIssue[];
  /** Non-blocking — row was imported, this field was dropped. */
  warnings: RowIssue[];
}

/**
 * Resolves the raw column headers/keys against COLUMN_ALIASES once per file
 * (not per row) so unknown-column detection happens exactly once.
 */
export function resolveColumns(rawColumns: string[]): {
  recognized: Map<string, keyof BusinessInput>;
  unknown: string[];
} {
  const recognized = new Map<string, keyof BusinessInput>();
  const unknown: string[] = [];

  for (const column of rawColumns) {
    const key = COLUMN_ALIASES[column.trim().toLowerCase()];
    if (key) {
      recognized.set(column, key);
    } else {
      unknown.push(column);
    }
  }

  return { recognized, unknown };
}

export function normalizeRow(
  rowNumber: number,
  row: RawRow,
  columnMap: Map<string, keyof BusinessInput>
): NormalizeResult {
  const warnings: RowIssue[] = [];
  const draft: Partial<BusinessInput> = {};

  for (const [rawColumn, field] of columnMap.entries()) {
    const rawValue = row[rawColumn];

    switch (field) {
      case "latitude":
      case "longitude":
      case "googleRating":
      case "reviewCount": {
        const num = toNumberValue(rawValue);
        if (num !== undefined) {
          if (Number.isNaN(num)) {
            warnings.push({
              rowNumber,
              column: rawColumn,
              rawValue: String(rawValue),
              code: "invalid_number",
              message: `"${rawColumn}" must be a number.`,
            });
          } else if (field === "latitude" && !isValidLatitude(num)) {
            warnings.push({
              rowNumber,
              column: rawColumn,
              rawValue: String(rawValue),
              code: "invalid_number",
              message: "Latitude must be between -90 and 90.",
            });
          } else if (field === "longitude" && !isValidLongitude(num)) {
            warnings.push({
              rowNumber,
              column: rawColumn,
              rawValue: String(rawValue),
              code: "invalid_number",
              message: "Longitude must be between -180 and 180.",
            });
          } else {
            (draft as Record<string, unknown>)[field] = num;
          }
        }
        break;
      }
      case "tags": {
        const str = toStringValue(rawValue);
        if (str) {
          draft.tags = str
            .split(/[,;|]/)
            .map((t) => t.trim())
            .filter(Boolean);
        }
        break;
      }
      case "email": {
        const str = toStringValue(rawValue);
        if (str) {
          if (!isValidEmail(str)) {
            warnings.push({
              rowNumber,
              column: rawColumn,
              rawValue: str,
              code: "invalid_email",
              message: `"${str}" is not a valid email address.`,
            });
          } else {
            draft.email = str;
          }
        }
        break;
      }
      case "website": {
        const str = toStringValue(rawValue);
        if (str) {
          if (!isValidWebsite(str)) {
            warnings.push({
              rowNumber,
              column: rawColumn,
              rawValue: str,
              code: "invalid_website",
              message: `"${str}" is not a valid website URL.`,
            });
          } else {
            draft.website = str;
          }
        }
        break;
      }
      case "phone":
      case "mobile": {
        const str = toStringValue(rawValue);
        if (str) {
          if (!isValidPhone(str)) {
            warnings.push({
              rowNumber,
              column: rawColumn,
              rawValue: str,
              code: "invalid_phone",
              message: `"${str}" is not a valid phone number.`,
            });
          } else {
            (draft as Record<string, unknown>)[field] = str;
          }
        }
        break;
      }
      default: {
        const str = toStringValue(rawValue);
        if (str) {
          (draft as Record<string, unknown>)[field] = str;
        }
      }
    }
  }

  const issues: RowIssue[] = [];
  for (const required of REQUIRED_FIELDS) {
    if (!draft[required]) {
      issues.push({
        rowNumber,
        column: required,
        code: "missing_required_field",
        message: `"${required}" is required.`,
      });
    }
  }

  if (issues.length > 0) {
    return { issues, warnings };
  }

  return { input: draft as BusinessInput, issues: [], warnings };
}
