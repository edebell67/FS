const crypto = require('crypto');

function cloneValue(value) {
  return JSON.parse(JSON.stringify(value));
}

class MemoryTransactionImportStore {
  constructor() {
    this.bankTransactions = new Map();
    this.transactionsByRef = new Map();
    this.transactionsBySourceHash = new Map();
    this.importRuns = new Map();
    this.importCheckpoints = new Map();
  }

  async startImportRun(importRun) {
    this.importRuns.set(importRun.import_run_id, cloneValue(importRun));
  }

  async completeImportRun(importRunId, summary) {
    const record = this.importRuns.get(importRunId);
    this.importRuns.set(importRunId, {
      ...record,
      ...cloneValue(summary)
    });
  }

  async failImportRun(importRunId, summary) {
    const record = this.importRuns.get(importRunId);
    this.importRuns.set(importRunId, {
      ...record,
      ...cloneValue(summary)
    });
  }

  async getImportCheckpoint(bankAccountId) {
    return cloneValue(this.importCheckpoints.get(bankAccountId) || null);
  }

  async updateImportCheckpoint(bankAccountId, checkpoint) {
    const previous = this.importCheckpoints.get(bankAccountId) || {};
    const lastSuccessfulCursor = checkpoint.last_status === 'completed'
      ? checkpoint.last_successful_cursor
      : previous.last_successful_cursor ?? null;
    const lastSuccessfulImportAt = checkpoint.last_status === 'completed'
      ? checkpoint.last_successful_import_at
      : previous.last_successful_import_at ?? null;
    const merged = {
      ...previous,
      ...cloneValue(checkpoint),
      last_successful_cursor: lastSuccessfulCursor,
      last_successful_import_at: lastSuccessfulImportAt
    };
    this.importCheckpoints.set(bankAccountId, merged);
  }

  async runInTransaction(callback) {
    const snapshot = {
      bankTransactions: cloneValue([...this.bankTransactions.entries()]),
      transactionsByRef: cloneValue([...this.transactionsByRef.entries()]),
      transactionsBySourceHash: cloneValue([...this.transactionsBySourceHash.entries()]),
      importCheckpoints: cloneValue([...this.importCheckpoints.entries()])
    };

    try {
      return await callback(this);
    } catch (error) {
      this.bankTransactions = new Map(snapshot.bankTransactions);
      this.transactionsByRef = new Map(snapshot.transactionsByRef);
      this.transactionsBySourceHash = new Map(snapshot.transactionsBySourceHash);
      this.importCheckpoints = new Map(snapshot.importCheckpoints);
      throw error;
    }
  }

  async upsertBankTransaction(transaction) {
    const refKey = `${transaction.bank_account_id}::${transaction.bank_txn_ref}`;
    const hashKey = `${transaction.bank_account_id}::${transaction.source_hash}`;
    const existingTxnId = this.transactionsByRef.get(refKey) || this.transactionsBySourceHash.get(hashKey);

    if (existingTxnId) {
      return {
        status: 'duplicate',
        record: cloneValue(this.bankTransactions.get(existingTxnId))
      };
    }

    const record = {
      ...cloneValue(transaction),
      txn_id: crypto.randomUUID()
    };
    this.bankTransactions.set(record.txn_id, record);
    this.transactionsByRef.set(refKey, record.txn_id);
    this.transactionsBySourceHash.set(hashKey, record.txn_id);

    return {
      status: 'inserted',
      record: cloneValue(record)
    };
  }

  getTransactionsForAccount(bankAccountId) {
    return [...this.bankTransactions.values()]
      .filter((transaction) => transaction.bank_account_id === bankAccountId)
      .map((transaction) => cloneValue(transaction));
  }

  getImportRun(importRunId) {
    return cloneValue(this.importRuns.get(importRunId));
  }

  countTransactions() {
    return this.bankTransactions.size;
  }
}

module.exports = {
  MemoryTransactionImportStore
};
