// Shared types for the CSV/JSON importer. Both formats converge on the same
// RawRow -> validate -> normalize -> dedupe -> assign-ref pipeline (see
// pipeline.ts) so the two entry points (csv.ts, json.ts) are thin adapters,
// not parallel implementations.

/** A single input record before any validation, keyed by source column/field name. */
export type RawRow = Record<string, string | number | null | undefined>;

export type ImportSource = "csv" | "json" | "api";

/** Canonical fields the importer understands, independent of source column naming. */
export interface BusinessInput {
  businessName: string;
  tradingName?: string;
  category: string;
  subCategory?: string;
  email?: string;
  phone?: string;
  mobile?: string;
  website?: string;
  facebook?: string;
  instagram?: string;
  linkedin?: string;
  address?: string;
  town?: string;
  county?: string;
  postcode?: string;
  latitude?: number;
  longitude?: number;
  googleRating?: number;
  reviewCount?: number;
  description?: string;
  notes?: string;
  tags?: string[];
}

export type ErrorCode =
  | "missing_required_field"
  | "invalid_email"
  | "invalid_website"
  | "invalid_phone"
  | "invalid_number"
  | "unknown_column"
  | "duplicate_in_batch"
  | "duplicate_existing";

/**
 * "rejected" — the row was not imported (missing a required field).
 * "duplicate" — the row was not imported (matched another row/business).
 * "warning" — the row WAS imported; this one field was dropped because its
 * value didn't validate. Set by pipeline.ts, not by normalize.ts, since only
 * the pipeline knows the row's ultimate fate.
 */
export type RowIssueKind = "rejected" | "duplicate" | "warning";

export interface RowIssue {
  rowNumber: number;
  column?: string;
  rawValue?: string;
  code: ErrorCode;
  message: string;
  kind?: RowIssueKind;
}

export interface AcceptedRow {
  rowNumber: number;
  input: BusinessInput;
  /** Populated once a ref has been reserved for this row. */
  businessRef?: string;
}

export interface ImportSummary {
  totalRows: number;
  accepted: AcceptedRow[];
  rejected: RowIssue[];
  duplicates: RowIssue[];
  /** Non-blocking: the row was imported, but this field was dropped. */
  warnings: RowIssue[];
  /** Column names present in the source that the importer didn't recognise. */
  unknownColumns: string[];
}

/** Required fields for a row to be importable at all. */
export const REQUIRED_FIELDS: Array<keyof BusinessInput> = ["businessName", "category"];

/**
 * Maps every accepted source column alias to a canonical BusinessInput key.
 * Extend this when a new CSV export uses different header names — it's the
 * single place column-name variance is absorbed.
 */
export const COLUMN_ALIASES: Record<string, keyof BusinessInput> = {
  "business name": "businessName",
  business_name: "businessName",
  name: "businessName",
  "trading name": "tradingName",
  trading_name: "tradingName",
  category: "category",
  "sub category": "subCategory",
  subcategory: "subCategory",
  sub_category: "subCategory",
  email: "email",
  "email address": "email",
  phone: "phone",
  telephone: "phone",
  mobile: "mobile",
  website: "website",
  url: "website",
  facebook: "facebook",
  instagram: "instagram",
  linkedin: "linkedin",
  address: "address",
  town: "town",
  city: "town",
  county: "county",
  postcode: "postcode",
  zip: "postcode",
  "zip code": "postcode",
  latitude: "latitude",
  lat: "latitude",
  longitude: "longitude",
  lng: "longitude",
  long: "longitude",
  "google rating": "googleRating",
  rating: "googleRating",
  "review count": "reviewCount",
  reviews: "reviewCount",
  description: "description",
  notes: "notes",
  tags: "tags",
};
