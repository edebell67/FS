// Persistence seam for the importer. pipeline.ts and normalize.ts never
// touch the DB directly — everything that reads or writes Postgres goes
// through this interface, so the pipeline can be unit-tested with the
// in-memory implementation and only the adapter below needs a live database.

import { and, eq, or, sql } from "drizzle-orm";
import { db } from "@/lib/db/client";
import {
  businesses,
  categorySequences,
  importBatches,
  importRowErrors,
  pipelineStages,
  stageTransitions,
} from "@/lib/db/schema";
import type { DedupeKeys } from "./duplicates";
import type { AcceptedRow, ImportSource, RowIssue } from "./types";
import { slugify } from "./slug";

export interface ImportRepository {
  createBatch(filename: string, source: ImportSource, uploadedBy?: string): Promise<string>;
  existingLookup(keys: DedupeKeys): Promise<boolean>;
  reserveNext(categoryCode: string): Promise<number>;
  insertAccepted(batchId: string, source: ImportSource, rows: AcceptedRow[]): Promise<void>;
  recordErrors(batchId: string, issues: RowIssue[]): Promise<void>;
  completeBatch(
    batchId: string,
    counts: { total: number; accepted: number; rejected: number; duplicates: number }
  ): Promise<void>;
  rollbackBatch(batchId: string): Promise<number>;
}

const IMPORTED_STAGE_KEY = "imported";

/**
 * Drizzle-backed implementation, wired to the live Postgres client. Requires
 * the Phase 1 migration (pipeline_stages seeded with "imported") to have run.
 */
export class DrizzleImportRepository implements ImportRepository {
  async createBatch(filename: string, source: ImportSource, uploadedBy?: string): Promise<string> {
    const [row] = await db
      .insert(importBatches)
      .values({ filename, source, uploadedBy, status: "processing" })
      .returning({ id: importBatches.id });
    if (!row) throw new Error("Failed to create import batch.");
    return row.id;
  }

  async existingLookup(keys: DedupeKeys): Promise<boolean> {
    const conditions = [];
    if (keys.email) conditions.push(eq(businesses.email, keys.email));
    if (keys.phone) conditions.push(eq(businesses.phone, keys.phone));
    if (keys.website) conditions.push(eq(businesses.website, keys.website));

    // Mirrors duplicates.ts's normalizeNamePart/normalizePostcodePart exactly —
    // must, since this is comparing against DB rows the JS-side in-batch check
    // never sees. Without this, any business with no email/phone/website
    // (common — see UK_Ltd_email_no_website_VERIFIED_410.csv, most rows have
    // none of the three) could never be caught as a duplicate of an existing
    // record, only within the same file.
    if (keys.namePart) {
      conditions.push(
        and(
          sql`lower(regexp_replace(${businesses.businessName}, '[^a-zA-Z0-9]', '', 'g')) = ${keys.namePart}`,
          sql`lower(regexp_replace(coalesce(${businesses.postcode}, ''), '\\s', '', 'g')) = ${keys.postcodePart}`
        )
      );
    }

    if (conditions.length === 0) return false;

    const [match] = await db
      .select({ id: businesses.id })
      .from(businesses)
      .where(or(...conditions))
      .limit(1);
    return Boolean(match);
  }

  async reserveNext(categoryCode: string): Promise<number> {
    const result = await db.execute(sql`
      INSERT INTO ${categorySequences} (category_code, next_val)
      VALUES (${categoryCode}, 1)
      ON CONFLICT (category_code)
      DO UPDATE SET next_val = ${categorySequences.nextVal} + 1
      RETURNING next_val
    `);
    const rows = (result as unknown as { rows: Array<{ next_val: number }> }).rows;
    const first = rows[0];
    if (!first) throw new Error(`Failed to reserve a sequence value for category "${categoryCode}".`);
    return Number(first.next_val);
  }

  async insertAccepted(batchId: string, source: ImportSource, rows: AcceptedRow[]): Promise<void> {
    if (rows.length === 0) return;

    const [importedStage] = await db
      .select({ id: pipelineStages.id })
      .from(pipelineStages)
      .where(eq(pipelineStages.key, IMPORTED_STAGE_KEY))
      .limit(1);
    if (!importedStage) {
      throw new Error(
        `Pipeline stage "${IMPORTED_STAGE_KEY}" is not seeded. Run the Phase 1 seed script first.`
      );
    }

    await db.transaction(async (tx) => {
      for (const row of rows) {
        if (!row.businessRef) continue;
        const now = new Date();
        const [inserted] = await tx
          .insert(businesses)
          .values({
            businessRef: row.businessRef,
            slug: slugify(`${row.input.businessName}-${row.input.town ?? ""}-${row.businessRef}`),
            businessName: row.input.businessName,
            tradingName: row.input.tradingName,
            category: row.input.category,
            subCategory: row.input.subCategory,
            email: row.input.email,
            phone: row.input.phone,
            mobile: row.input.mobile,
            website: row.input.website,
            facebook: row.input.facebook,
            instagram: row.input.instagram,
            linkedin: row.input.linkedin,
            address: row.input.address,
            town: row.input.town,
            county: row.input.county,
            postcode: row.input.postcode,
            latitude: row.input.latitude,
            longitude: row.input.longitude,
            googleRating: row.input.googleRating,
            reviewCount: row.input.reviewCount,
            description: row.input.description,
            notes: row.input.notes,
            tags: row.input.tags,
            importedSource: source,
            importBatchId: batchId,
            importDate: now,
            lastUpdated: now,
            currentStageId: importedStage.id,
            stageEnteredAt: now,
          })
          .returning({ id: businesses.id });
        if (!inserted) throw new Error(`Failed to insert business for row ${row.rowNumber}.`);

        await tx.insert(stageTransitions).values({
          businessId: inserted.id,
          fromStageId: null,
          toStageId: importedStage.id,
          occurredAt: now,
          source: "import",
          notes: `Imported in batch ${batchId}`,
        });
      }
    });
  }

  async recordErrors(batchId: string, issues: RowIssue[]): Promise<void> {
    if (issues.length === 0) return;
    await db.insert(importRowErrors).values(
      issues.map((issue) => ({
        batchId,
        rowNumber: issue.rowNumber,
        column: issue.column,
        rawValue: issue.rawValue,
        errorCode: issue.code,
        message: issue.message,
      }))
    );
  }

  async completeBatch(
    batchId: string,
    counts: { total: number; accepted: number; rejected: number; duplicates: number }
  ): Promise<void> {
    await db
      .update(importBatches)
      .set({
        status: "completed",
        totalRows: counts.total,
        acceptedRows: counts.accepted,
        rejectedRows: counts.rejected,
        duplicateRows: counts.duplicates,
        completedAt: new Date(),
      })
      .where(eq(importBatches.id, batchId));
  }

  async rollbackBatch(batchId: string): Promise<number> {
    // Businesses first (stage_transitions cascade via FK -> businesses is
    // not ON DELETE CASCADE by design, since a business could theoretically
    // outlive its import batch's error rows; delete explicitly instead).
    const deletedBusinesses = await db
      .delete(businesses)
      .where(eq(businesses.importBatchId, batchId))
      .returning({ id: businesses.id });

    await db
      .update(importBatches)
      .set({ status: "rolled_back" })
      .where(eq(importBatches.id, batchId));

    return deletedBusinesses.length;
  }
}
