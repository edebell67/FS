const assert = require('assert');
const path = require('path');

class MockDb {
  constructor() {
    this.calls = [];
    this.matchSuggestions = [
      { bank_txn_id: 'txn-1' },
      { bank_txn_id: 'txn-2' },
      { bank_txn_id: 'txn-3' }
    ];
    this.classifications = new Map();
    this.auditEntries = [];
    this.evidenceLinks = new Map();
  }

  get pool() {
    return {
      connect: async () => ({
        query: this.query.bind(this),
        release() {},
      }),
    };
  }

  async query(text, params = []) {
    const sql = text.replace(/\s+/g, ' ').trim();
    this.calls.push({ sql, params });

    if (sql === 'BEGIN' || sql === 'COMMIT' || sql === 'ROLLBACK') {
      return { rows: [] };
    }

    if (sql.includes('SELECT * FROM transaction_classifications')) {
      const existing = this.classifications.get(params[0]);
      return { rows: existing ? [existing] : [] };
    }

    if (sql.includes('INSERT INTO transaction_classifications')) {
      const next = {
        user_id: params[0],
        bank_txn_id: params[1],
        category_code: params[2],
        category_name: params[3],
        business_personal: params[4],
        is_split: params[5],
        split_business_pct: params[6],
        confidence: params[7],
        source: params[8],
      };
      this.classifications.set(params[1], next);
      return { rows: [next] };
    }

    if (sql.includes('INSERT INTO transaction_audit_log')) {
      this.auditEntries.push({
        bank_txn_id: params[1],
        previous_value: params[4],
        new_value: params[5],
        change_source: params[6],
      });
      return { rows: [] };
    }

    if (sql.includes('SELECT txn_date FROM bank_transactions')) {
      return { rows: [{ txn_date: '2026-03-12' }] };
    }

    if (sql.includes('FROM bank_transactions bt CROSS JOIN ev')) {
      return { rows: this.matchSuggestions };
    }

    if (sql.includes('SELECT GREATEST(0, 1 - LEAST(1, ABS(COALESCE(bt.amount, 0) - COALESCE(ev.amount, 0))')) {
      return {
        rows: [
          {
            amount_score: 0.97,
            date_score: 0.93,
            merchant_score: 0.88
          }
        ]
      };
    }

    if (sql.startsWith('DELETE FROM evidence_links')) {
      this.evidenceLinks.set(params[1], []);
      return { rows: [] };
    }

    if (sql.includes('INSERT INTO evidence_links')) {
      const isNoMatch = sql.includes('VALUES ($1,$2,NULL,0,true');
      const record = {
        evidence_id: params[1],
        bank_txn_id: isNoMatch ? null : params[2],
        user_confirmed: !sql.includes('false'),
        method: params.at(-1)
      };
      this.evidenceLinks.set(params[1], [record]);
      return { rows: [record] };
    }

    return { rows: [] };
  }
}

function loadController(mockDb) {
  const dbModulePath = path.resolve(__dirname, 'src', 'config', 'db.js');
  delete require.cache[dbModulePath];
  require.cache[dbModulePath] = {
    id: dbModulePath,
    filename: dbModulePath,
    loaded: true,
    exports: mockDb
  };

  const controllerPath = path.resolve(__dirname, 'src', 'controllers', 'voiceController.js');
  delete require.cache[controllerPath];
  return require(controllerPath);
}

function createResponse() {
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
    }
  };
}

async function invoke(controller, body) {
  const res = createResponse();
  await controller.processMicroDecision(
    {
      body,
      user: { id: 'user-1' }
    },
    res
  );
  return res;
}

async function main() {
  const mockDb = new MockDb();
  const controller = loadController(mockDb);

  const missingContext = await invoke(controller, {
    transcript: 'Business',
    bank_txn_id: 'txn-123'
  });
  assert.strictEqual(missingContext.statusCode, 400);
  assert.strictEqual(missingContext.body.error, 'context_scope must be inbox or finish_now for transaction micro-decisions.');

  const category = await invoke(controller, {
    transcript: 'Category: Travel',
    bank_txn_id: 'txn-123',
    context_scope: 'inbox'
  });
  assert.strictEqual(category.statusCode, 200);
  assert.strictEqual(category.body.confirmation_chip, 'Applied: Travel');
  assert.strictEqual(category.body.undo.supported, true);
  assert.deepStrictEqual(category.body.context_binding, {
    scope: 'inbox',
    target_type: 'bank_transaction',
    target_id: 'txn-123'
  });
  assert.strictEqual(mockDb.classifications.get('txn-123').category_code, 'TRAVEL');
  assert.strictEqual(mockDb.auditEntries.at(-1).change_source, 'voice');

  const business = await invoke(controller, {
    transcript: 'Business',
    bank_txn_id: 'txn-123',
    context_scope: 'finish_now'
  });
  assert.strictEqual(business.statusCode, 200);
  assert.strictEqual(business.body.confirmation_chip, 'Applied: BUSINESS');
  assert.strictEqual(business.body.context_binding.scope, 'finish_now');
  assert.strictEqual(mockDb.classifications.get('txn-123').category_code, 'TRAVEL');
  assert.strictEqual(mockDb.classifications.get('txn-123').business_personal, 'BUSINESS');
  assert.strictEqual(mockDb.classifications.get('txn-123').is_split, false);

  const split = await invoke(controller, {
    transcript: 'Split 70%',
    bank_txn_id: 'txn-123',
    context_scope: 'inbox'
  });
  assert.strictEqual(split.statusCode, 200);
  assert.strictEqual(split.body.confirmation_chip, 'Applied: Split 70%');
  assert.strictEqual(split.body.undo.supported, true);
  assert.strictEqual(mockDb.classifications.get('txn-123').business_personal, 'BUSINESS');
  assert.strictEqual(mockDb.classifications.get('txn-123').is_split, true);
  assert.strictEqual(mockDb.classifications.get('txn-123').split_business_pct, 70);

  const attachReceipt = await invoke(controller, {
    transcript: 'Attach receipt',
    evidence_id: 'evidence-1',
    context_scope: 'evidence'
  });
  assert.strictEqual(attachReceipt.statusCode, 200);
  assert.strictEqual(attachReceipt.body.action_status, 'clarification_needed');
  assert.strictEqual(attachReceipt.body.confirmation_chip, 'Attach receipt requested');
  assert.strictEqual(attachReceipt.body.undo.supported, false);
  assert.deepStrictEqual(attachReceipt.body.context_binding, {
    scope: 'evidence',
    target_type: 'evidence',
    target_id: 'evidence-1'
  });

  const matchSecond = await invoke(controller, {
    transcript: 'Match second',
    evidence_id: 'evidence-1',
    context_scope: 'evidence'
  });
  assert.strictEqual(matchSecond.statusCode, 200);
  assert.strictEqual(matchSecond.body.confirmation_chip, 'Applied: Match 2');
  assert.deepStrictEqual(matchSecond.body.context_binding, {
    scope: 'evidence',
    target_type: 'evidence',
    target_id: 'evidence-1'
  });
  assert(
    mockDb.calls.some((call) => call.sql.includes('INSERT INTO evidence_links') && call.params[1] === 'evidence-1' && call.params[2] === 'txn-2'),
    'Expected match command to persist selected evidence link'
  );

  const noMatch = await invoke(controller, {
    transcript: 'No match',
    evidence_id: 'evidence-1',
    context_scope: 'evidence'
  });
  assert.strictEqual(noMatch.statusCode, 200);
  assert.strictEqual(noMatch.body.confirmation_chip, 'Applied: No match');

  const invalidSplit = await invoke(controller, {
    transcript: 'Split 140%',
    bank_txn_id: 'txn-123',
    context_scope: 'inbox'
  });
  assert.strictEqual(invalidSplit.statusCode, 400);
  assert.strictEqual(invalidSplit.body.error, 'Split percentage must be 0-100.');

  const unsafeContext = await invoke(controller, {
    transcript: 'Category: Travel',
    bank_txn_id: 'txn-123',
    context_scope: 'evidence'
  });
  assert.strictEqual(unsafeContext.statusCode, 409);
  assert.strictEqual(unsafeContext.body.error, 'Command "category" is not allowed for evidence context.');

  const unsupported = await invoke(controller, {
    transcript: 'Archive this forever',
    context_scope: 'inbox'
  });
  assert.strictEqual(unsupported.statusCode, 400);
  assert.strictEqual(unsupported.body.error, 'Unsupported MVP voice micro-decision command.');

  console.log('voice_micro_decisions_ok');
  console.log('context_guardrails_ok=true');
  console.log('audited_classification_updates_ok=true');
  console.log('attach_receipt_clarification_ok=true');
  console.log('match_selection_ok=true');
  console.log('safe_context_binding_ok=true');
  console.log('validation_errors_ok=true');
}

main().catch((error) => {
  console.error('voice_micro_decisions_failed');
  console.error(error);
  process.exit(1);
});
