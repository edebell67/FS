const assert = require('assert');
const path = require('path');

const {
  buildEvidenceCsv
} = require('./src/services/quarterlyExportService');

class MockDb {
  constructor() {
    this.evidenceRecords = new Map([
      ['evidence-1', this.createEvidence('evidence-1', '2026-03-14T09:00:00Z', 'Tesco', 12.5)],
      ['evidence-2', this.createEvidence('evidence-2', '2026-03-14T09:30:00Z', 'Cafe Nero', 8.2)],
      ['evidence-3', this.createEvidence('evidence-3', '2026-03-14T10:00:00Z', 'Trainline', 34.9)],
      ['evidence-4', this.createEvidence('evidence-4', '2026-03-14T10:30:00Z', 'Stationery Shop', 18.0)]
    ]);
    this.linkRecords = new Map();
    this.scoreRows = new Map([
      ['evidence-1::txn-1', { amount_score: 0.99, date_score: 0.95, merchant_score: 0.9 }],
      ['evidence-3::txn-3', { amount_score: 0.92, date_score: 0.85, merchant_score: 0.75 }],
      ['evidence-4::txn-4', { amount_score: 0.88, date_score: 0.8, merchant_score: 0.65 }]
    ]);
  }

  createEvidence(id, capturedAt, merchant, amount) {
    return {
      id,
      type: 'RECEIPT',
      captured_at: capturedAt,
      doc_date: '2026-03-14',
      merchant,
      amount,
      storage_link: `/uploads/evidence/${id}.jpg`,
      extraction_confidence: 0.84
    };
  }

  orderedLinks(evidenceId) {
    const links = this.linkRecords.get(evidenceId) || [];
    return links.slice().sort((left, right) => {
      const leftPriority = left.user_confirmed ? 0 : 1;
      const rightPriority = right.user_confirmed ? 0 : 1;
      if (leftPriority !== rightPriority) return leftPriority - rightPriority;
      const leftStamp = left.confirmed_at || left.created_at;
      const rightStamp = right.confirmed_at || right.created_at;
      return String(rightStamp).localeCompare(String(leftStamp));
    });
  }

  async query(text, params = []) {
    const sql = text.replace(/\s+/g, ' ').trim();

    if (sql.includes('SELECT GREATEST(0, 1 - LEAST(1, ABS(COALESCE(bt.amount, 0) - COALESCE(ev.amount, 0))')) {
      const key = `${params[1]}::${params[2]}`;
      const row = this.scoreRows.get(key);
      return { rows: row ? [row] : [] };
    }

    if (sql.startsWith('DELETE FROM evidence_links')) {
      this.linkRecords.set(params[1], []);
      return { rows: [] };
    }

    if (sql.startsWith('INSERT INTO evidence_links')) {
      const isRejectInsert = sql.includes('VALUES ($1,$2,NULL,0,true');
      const isConfirmedInsert = sql.includes('VALUES ($1,$2,$3,$4,true');
      const isDeferredInsert = sql.includes('VALUES ($1,$2,$3,$4,false');
      const record = {
        id: `link-${params[1]}-${(this.linkRecords.get(params[1]) || []).length + 1}`,
        user_id: params[0],
        evidence_id: params[1],
        bank_txn_id: isRejectInsert ? null : (params[2] ?? null),
        link_confidence: isRejectInsert ? 0 : (params[3] ?? 0),
        user_confirmed: isRejectInsert || isConfirmedInsert,
        confirmed_at: isRejectInsert || isConfirmedInsert ? '2026-03-14T12:00:00.000Z' : null,
        method: params.at(-1),
        created_at: '2026-03-14T12:00:00.000Z'
      };
      assert(isRejectInsert || isConfirmedInsert || isDeferredInsert, `Unexpected insert shape: ${sql}`);
      this.linkRecords.set(params[1], [record]);
      return { rows: [record] };
    }

    if (sql.includes('FROM evidence e LEFT JOIN LATERAL')) {
      const rows = [];
      for (const evidence of this.evidenceRecords.values()) {
        const decision = this.orderedLinks(evidence.id)[0] || null;
        const userConfirmed = decision?.user_confirmed === true;
        if (userConfirmed) {
          continue;
        }
        rows.push({
          evidence_id: evidence.id,
          type: evidence.type,
          captured_at: evidence.captured_at,
          doc_date: evidence.doc_date,
          merchant: evidence.merchant,
          amount: evidence.amount,
          storage_link: evidence.storage_link,
          extraction_confidence: evidence.extraction_confidence,
          pending_bank_txn_id: decision?.bank_txn_id || null,
          user_confirmed: userConfirmed,
          method: decision?.method || null,
          match_state: decision?.bank_txn_id ? 'deferred_match' : 'pending_review'
        });
      }
      return { rows: rows.slice(0, params[1]) };
    }

    throw new Error(`Unhandled SQL in MockDb: ${sql}`);
  }

  exportRows() {
    return Array.from(this.evidenceRecords.values()).map((evidence) => {
      const decision = this.orderedLinks(evidence.id)[0] || null;
      return {
        evidence_id: evidence.id,
        type: evidence.type,
        captured_at: evidence.captured_at,
        doc_date: evidence.doc_date,
        merchant: evidence.merchant,
        amount: evidence.amount,
        storage_link: evidence.storage_link,
        extraction_confidence: evidence.extraction_confidence,
        matched_bank_txn_id: decision?.bank_txn_id || '',
        user_confirmed: decision?.user_confirmed === true
      };
    });
  }
}

function loadModules(mockDb) {
  const dbModulePath = path.resolve(__dirname, 'src', 'config', 'db.js');
  delete require.cache[dbModulePath];
  require.cache[dbModulePath] = {
    id: dbModulePath,
    filename: dbModulePath,
    loaded: true,
    exports: mockDb
  };

  const servicePath = path.resolve(__dirname, 'src', 'services', 'evidenceMatchingService.js');
  const controllerPath = path.resolve(__dirname, 'src', 'controllers', 'evidenceController.js');
  delete require.cache[servicePath];
  delete require.cache[controllerPath];

  return {
    service: require(servicePath),
    controller: require(controllerPath)
  };
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

async function main() {
  const mockDb = new MockDb();
  const { service, controller } = loadModules(mockDb);

  const confirmed = await service.confirmMatch({
    userId: 'user-1',
    evidenceId: 'evidence-1',
    bankTxnId: 'txn-1',
    method: 'manual',
    database: mockDb
  });
  assert(confirmed);
  assert.strictEqual(confirmed.bank_txn_id, 'txn-1');
  assert.strictEqual(confirmed.user_confirmed, true);

  const rejected = await service.rejectMatch({
    userId: 'user-1',
    evidenceId: 'evidence-2',
    method: 'manual',
    database: mockDb
  });
  assert(rejected);
  assert.strictEqual(rejected.bank_txn_id, null);
  assert.strictEqual(rejected.user_confirmed, true);

  const deferred = await service.deferMatch({
    userId: 'user-1',
    evidenceId: 'evidence-3',
    bankTxnId: 'txn-3',
    method: 'manual',
    database: mockDb
  });
  assert(deferred);
  assert.strictEqual(deferred.bank_txn_id, 'txn-3');
  assert.strictEqual(deferred.user_confirmed, false);

  const deferRes = createResponse();
  await controller.deferEvidenceMatch(
    {
      user: { id: 'user-1' },
      params: { id: 'evidence-4' },
      body: { bank_txn_id: 'txn-4', method: 'manual' }
    },
    deferRes
  );
  assert.strictEqual(deferRes.statusCode, 200);
  assert.strictEqual(deferRes.body.status, 'deferred_match');

  const pendingRes = createResponse();
  await controller.listPendingEvidenceRecords(
    {
      user: { id: 'user-1' },
      query: { limit: 10 }
    },
    pendingRes
  );
  assert.strictEqual(pendingRes.statusCode, 200);
  assert.deepStrictEqual(
    pendingRes.body.map((row) => row.evidence_id),
    ['evidence-3', 'evidence-4']
  );
  assert.strictEqual(pendingRes.body[0].match_state, 'deferred_match');
  assert.strictEqual(pendingRes.body[1].pending_bank_txn_id, 'txn-4');

  const csv = buildEvidenceCsv(mockDb.exportRows());
  assert(csv.includes('evidence-1,RECEIPT,2026-03-14T09:00:00.000Z,2026-03-14,"Tesco",12.5,"/uploads/evidence/evidence-1.jpg",0.840,txn-1,true'));
  assert(csv.includes('evidence-2,RECEIPT,2026-03-14T09:30:00.000Z,2026-03-14,"Cafe Nero",8.2,"/uploads/evidence/evidence-2.jpg",0.840,,true'));
  assert(csv.includes('evidence-3,RECEIPT,2026-03-14T10:00:00.000Z,2026-03-14,"Trainline",34.9,"/uploads/evidence/evidence-3.jpg",0.840,txn-3,false'));
  assert(csv.includes('evidence-4,RECEIPT,2026-03-14T10:30:00.000Z,2026-03-14,"Stationery Shop",18,"/uploads/evidence/evidence-4.jpg",0.840,txn-4,false'));

  console.log('verify_evidence_confirmation=PASS');
  console.log(JSON.stringify({
    confirmed_match_state: confirmed.bank_txn_id,
    no_match_state: rejected.bank_txn_id,
    deferred_pending_ids: pendingRes.body.map((row) => row.evidence_id),
    csv_rows: csv.trim().split('\n').length - 1
  }));
}

main().catch((error) => {
  console.error('verify_evidence_confirmation=FAIL');
  console.error(error);
  process.exit(1);
});
