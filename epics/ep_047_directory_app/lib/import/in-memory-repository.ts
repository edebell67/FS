// Test double for ImportRepository. Lets pipeline.ts and the API route logic
// be exercised end-to-end (batch create -> insert -> rollback) without a
// live Postgres connection. Mirrors the Drizzle implementation's behaviour
// closely enough that tests written against this catch real regressions.

import { randomUUID } from "node:crypto";
import type { DedupeKeys } from "./duplicates";
import type { ImportRepository } from "./repository";
import type { AcceptedRow, ImportSource, RowIssue } from "./types";
import { createInMemorySequenceProvider, type SequenceProvider } from "./business-ref";

export interface StoredBusiness {
  id: string;
  businessRef: string;
  batchId: string;
  input: AcceptedRow["input"];
}

export class InMemoryImportRepository implements ImportRepository {
  readonly businessesByBatch = new Map<string, StoredBusiness[]>();
  readonly errorsByBatch = new Map<string, RowIssue[]>();
  readonly batchStatus = new Map<string, string>();
  private readonly existing: DedupeKeys[];
  private readonly sequenceProvider: SequenceProvider = createInMemorySequenceProvider();

  constructor(preExisting: DedupeKeys[] = []) {
    this.existing = preExisting;
  }

  async createBatch(): Promise<string> {
    const id = randomUUID();
    this.businessesByBatch.set(id, []);
    this.errorsByBatch.set(id, []);
    this.batchStatus.set(id, "processing");
    return id;
  }

  async existingLookup(keys: DedupeKeys): Promise<boolean> {
    return this.existing.some(
      (candidate) =>
        (Boolean(keys.email) && candidate.email === keys.email) ||
        (Boolean(keys.phone) && candidate.phone === keys.phone) ||
        (Boolean(keys.website) && candidate.website === keys.website) ||
        (Boolean(keys.namePart) &&
          candidate.namePart === keys.namePart &&
          (candidate.postcodePart ?? "") === keys.postcodePart)
    );
  }

  async reserveNext(categoryCode: string): Promise<number> {
    return this.sequenceProvider(categoryCode);
  }

  async insertAccepted(batchId: string, _source: ImportSource, rows: AcceptedRow[]): Promise<void> {
    const bucket = this.businessesByBatch.get(batchId) ?? [];
    for (const row of rows) {
      if (!row.businessRef) continue;
      bucket.push({ id: randomUUID(), businessRef: row.businessRef, batchId, input: row.input });
    }
    this.businessesByBatch.set(batchId, bucket);
  }

  async recordErrors(batchId: string, issues: RowIssue[]): Promise<void> {
    const bucket = this.errorsByBatch.get(batchId) ?? [];
    bucket.push(...issues);
    this.errorsByBatch.set(batchId, bucket);
  }

  async completeBatch(batchId: string): Promise<void> {
    this.batchStatus.set(batchId, "completed");
  }

  async rollbackBatch(batchId: string): Promise<number> {
    const count = this.businessesByBatch.get(batchId)?.length ?? 0;
    this.businessesByBatch.set(batchId, []);
    this.batchStatus.set(batchId, "rolled_back");
    return count;
  }
}
