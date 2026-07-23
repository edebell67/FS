// Shape of the JSON body returned by POST /api/import (see app/api/import/route.ts).
// Kept separate from lib/import/types.ts because that file's RowIssue is the
// server-side pipeline type; this is specifically the wire format the admin
// UI consumes.

import type { RowIssue } from "./types";

export interface ImportApiResponse {
  batchId: string;
  totalRows: number;
  accepted: number;
  rejected: number;
  duplicates: number;
  warnings: number;
  unknownColumns: string[];
  errors: RowIssue[];
}

export interface ImportApiError {
  error: string;
}
