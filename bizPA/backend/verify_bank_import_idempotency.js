const assert = require('assert');

const db = require('./src/config/db');
const { ingestBankFeed } = require('./src/controllers/inboxController');

function createResponseRecorder() {
  return {
    statusCode: 200,
    body: null,
    status(code) {
      this.statusCode = code;
      return this;
    },
    json(payload) {
      this.body = payload;
      return this;
    },
  };
}

const originalConnect = db.pool.connect;

async function main() {
  const insertedRefs = new Set();

  const client = {
    async query(text, params) {
      const sql = text.replace(/\s+/g, ' ').trim();

      if (sql === 'BEGIN' || sql === 'COMMIT' || sql === 'ROLLBACK') {
        return { rows: [] };
      }

      if (sql.includes('INSERT INTO bank_accounts')) {
        return { rows: [{ id: 'bank-account-1' }] };
      }

      if (sql.includes('INSERT INTO bank_transactions')) {
        const bankTxnRef = params[2];
        if (insertedRefs.has(bankTxnRef)) {
          return { rows: [] };
        }
        insertedRefs.add(bankTxnRef);
        return { rows: [{ id: `txn-${insertedRefs.size}` }] };
      }

      if (sql.startsWith('UPDATE bank_accounts SET last_synced_at')) {
        return { rows: [] };
      }

      throw new Error(`Unsupported SQL in idempotency verifier: ${sql}`);
    },
    release() {},
  };

  db.pool.connect = async () => client;

  const request = {
    user: { id: 'user-1' },
    body: {
      provider_name: 'mock_bank',
      provider_account_id: 'acct-123',
      account_name: 'Primary account',
      transactions: [
        {
          transaction_id: 'ob-txn-1',
          booking_date: '2026-03-31',
          amount: 120.45,
          credit_debit_indicator: 'debit',
          description: 'Fuel stop',
        },
        {
          transaction_id: 'ob-txn-1',
          booking_date: '2026-03-31',
          amount: 120.45,
          credit_debit_indicator: 'debit',
          description: 'Fuel stop duplicate replay',
        },
      ],
    },
  };

  const firstResponse = createResponseRecorder();
  await ingestBankFeed(request, firstResponse);
  assert.strictEqual(firstResponse.statusCode, 200);
  assert.strictEqual(firstResponse.body.inserted, 1);
  assert.strictEqual(firstResponse.body.deduped, 1);

  const secondResponse = createResponseRecorder();
  await ingestBankFeed(request, secondResponse);
  assert.strictEqual(secondResponse.statusCode, 200);
  assert.strictEqual(secondResponse.body.inserted, 0);
  assert.strictEqual(secondResponse.body.deduped, 2);

  db.pool.connect = originalConnect;

  console.log('verify_bank_import_idempotency=PASS');
  console.log(JSON.stringify({
    first_run: firstResponse.body,
    second_run: secondResponse.body,
  }));
}

main().catch((error) => {
  db.pool.connect = originalConnect;
  console.error('verify_bank_import_idempotency=FAIL');
  console.error(error);
  process.exit(1);
});
