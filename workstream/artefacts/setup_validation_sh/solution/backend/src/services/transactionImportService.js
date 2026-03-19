const crypto = require('crypto');
const { normalizeBatch } = require('./openBankingAdapter');

const DEFAULT_BACKFILL_DAYS = 90;

function toIsoTimestamp(value = new Date()) {
  const date = value instanceof Date ? value : new Date(value);
  return date.toISOString();
}

function computeBackfillStartDate(now = new Date(), windowDays = DEFAULT_BACKFILL_DAYS) {
  const date = now instanceof Date ? new Date(now.getTime()) : new Date(now);
  date.setUTCHours(0, 0, 0, 0);
  date.setUTCDate(date.getUTCDate() - windowDays);
  return date.toISOString().slice(0, 10);
}

function summarizeSkipped(skipped) {
  return skipped.reduce((accumulator, item) => {
    const key = item.reason || 'unknown';
    accumulator[key] = (accumulator[key] || 0) + 1;
    return accumulator;
  }, {});
}

function createImportRunRecord({
  bankAccount,
  importTriggeredBy,
  requestedWindowDays,
  fetchStartedAt,
  fromDate,
  cursorUsed
}) {
  return {
    import_run_id: crypto.randomUUID(),
    bank_account_id: bankAccount.bank_account_id,
    user_id: bankAccount.user_id,
    provider_name: bankAccount.provider_name,
    import_triggered_by: importTriggeredBy,
    requested_window_days: requestedWindowDays,
    fetch_started_at: fetchStartedAt,
    from_date: fromDate,
    cursor_used: cursorUsed,
    status: 'started'
  };
}

async function importNormalizedTransactions({
  store,
  bankAccount,
  rawTransactions,
  now = new Date(),
  importTriggeredBy = 'manual_refresh',
  requestedWindowDays = DEFAULT_BACKFILL_DAYS,
  fromDate = null,
  nextCursor = null,
  failAfterTransactionCount = null
}) {
  const importedAt = toIsoTimestamp(now);
  const { validTransactions, skipped } = normalizeBatch(rawTransactions, bankAccount);
  const importRun = createImportRunRecord({
    bankAccount,
    importTriggeredBy,
    requestedWindowDays,
    fetchStartedAt: importedAt,
    fromDate,
    cursorUsed: nextCursor
  });
  await store.startImportRun(importRun);

  try {
    const transactionSummary = await store.runInTransaction(async (transactionalStore) => {
      let inserted = 0;
      let deduped = 0;
      let processed = 0;
      let latestTransactionDate = null;

      for (const transaction of validTransactions) {
        processed += 1;
        if (failAfterTransactionCount !== null && processed > failAfterTransactionCount) {
          throw new Error(`Simulated import failure after ${failAfterTransactionCount} transaction(s)`);
        }

        const result = await transactionalStore.upsertBankTransaction({
          ...transaction,
          imported_at: importedAt
        });

        if (result.status === 'inserted') {
          inserted += 1;
        } else {
          deduped += 1;
        }

        if (!latestTransactionDate || result.record.date > latestTransactionDate) {
          latestTransactionDate = result.record.date;
        }
      }

      return {
        inserted,
        deduped,
        processed,
        latestTransactionDate
      };
    });

    const summary = {
      status: 'completed',
      import_run_id: importRun.import_run_id,
      bank_account_id: bankAccount.bank_account_id,
      requested_window_days: requestedWindowDays,
      from_date: fromDate,
      next_cursor: nextCursor,
      received: Array.isArray(rawTransactions) ? rawTransactions.length : 0,
      normalized: validTransactions.length,
      skipped_invalid: skipped.length,
      skipped_reasons: summarizeSkipped(skipped),
      inserted: transactionSummary.inserted,
      duplicate_suppressed: transactionSummary.deduped,
      imported_at: importedAt,
      latest_transaction_date: transactionSummary.latestTransactionDate
    };

    await store.completeImportRun(importRun.import_run_id, summary);
    await store.updateImportCheckpoint(bankAccount.bank_account_id, {
      bank_account_id: bankAccount.bank_account_id,
      last_attempt_at: importedAt,
      last_successful_import_at: importedAt,
      last_status: 'completed',
      last_error: null,
      last_requested_window_days: requestedWindowDays,
      last_backfill_start_date: fromDate,
      last_successful_cursor: nextCursor,
      last_received_count: summary.received,
      last_inserted_count: summary.inserted,
      last_duplicate_suppressed_count: summary.duplicate_suppressed,
      last_skipped_invalid_count: summary.skipped_invalid,
      latest_transaction_date: summary.latest_transaction_date
    });

    return summary;
  } catch (error) {
    const failureSummary = {
      status: 'failed',
      import_run_id: importRun.import_run_id,
      bank_account_id: bankAccount.bank_account_id,
      requested_window_days: requestedWindowDays,
      from_date: fromDate,
      next_cursor: nextCursor,
      received: Array.isArray(rawTransactions) ? rawTransactions.length : 0,
      normalized: validTransactions.length,
      skipped_invalid: skipped.length,
      skipped_reasons: summarizeSkipped(skipped),
      error_message: error.message,
      failed_at: importedAt
    };

    await store.failImportRun(importRun.import_run_id, failureSummary);
    await store.updateImportCheckpoint(bankAccount.bank_account_id, {
      bank_account_id: bankAccount.bank_account_id,
      last_attempt_at: importedAt,
      last_status: 'failed',
      last_error: error.message,
      last_requested_window_days: requestedWindowDays,
      last_backfill_start_date: fromDate,
      last_successful_cursor: null
    });

    error.importSummary = failureSummary;
    throw error;
  }
}

async function refreshBankAccount({
  store,
  providerClient,
  bankAccount,
  now = new Date(),
  requestedWindowDays = DEFAULT_BACKFILL_DAYS,
  importTriggeredBy = 'refresh'
}) {
  const checkpoint = await store.getImportCheckpoint(bankAccount.bank_account_id);
  const fromDate = checkpoint?.last_successful_import_at
    ? null
    : computeBackfillStartDate(now, requestedWindowDays);
  const cursor = checkpoint?.last_successful_cursor || null;
  const payload = await providerClient.fetchTransactions({
    bankAccount,
    fromDate,
    cursor,
    requestedWindowDays
  });

  return importNormalizedTransactions({
    store,
    bankAccount,
    rawTransactions: payload.transactions || [],
    now,
    importTriggeredBy,
    requestedWindowDays,
    fromDate,
    nextCursor: payload.nextCursor ?? cursor
  });
}

module.exports = {
  DEFAULT_BACKFILL_DAYS,
  computeBackfillStartDate,
  importNormalizedTransactions,
  refreshBankAccount
};
