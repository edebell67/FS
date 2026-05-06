const assert = require('assert');
const fs = require('fs');
const path = require('path');

class MockDb {
  constructor() {
    this.evidenceRecords = [];
    this.linkRecords = new Map();
  }

  async query(text, params = []) {
    const sql = text.replace(/\s+/g, ' ').trim();

    if (sql.includes('INSERT INTO evidence (')) {
      const record = {
        id: `evidence-${this.evidenceRecords.length + 1}`,
        user_id: params[0],
        type: params[1],
        doc_date: params[2],
        merchant: params[3],
        amount: params[4],
        storage_link: params[5],
        extraction_confidence: Number(params[6] || 0),
        extraction_payload: params[7],
        captured_at: new Date('2026-03-14T10:00:00Z').toISOString()
      };
      this.evidenceRecords.push(record);
      this.linkRecords.set(record.id, []);
      return { rows: [record] };
    }

    if (sql.includes('FROM bank_transactions bt CROSS JOIN ev')) {
      return {
        rows: [
          {
            bank_txn_id: 'txn-1',
            txn_date: '2026-03-14',
            merchant: 'Tesco',
            amount: 12.5,
            direction: 'out',
            amount_score: 0.99,
            date_score: 0.95,
            merchant_score: 0.9
          }
        ]
      };
    }

    if (sql.includes('FROM evidence e LEFT JOIN evidence_links el ON el.evidence_id = e.id WHERE e.id = $1')) {
      const record = this.evidenceRecords.find((item) => item.id === params[0] && item.user_id === params[1]);
      if (!record) return { rows: [] };
      return {
        rows: [
          {
            ...record,
            links: this.linkRecords.get(record.id) || []
          }
        ]
      };
    }

    if (sql.includes('FROM evidence e LEFT JOIN evidence_links el ON el.evidence_id = e.id WHERE e.user_id = $1')) {
      return {
        rows: this.evidenceRecords
          .filter((item) => item.user_id === params[0])
          .slice(0, params[1])
          .map((item) => ({
            id: item.id,
            type: item.type,
            captured_at: item.captured_at,
            doc_date: item.doc_date,
            merchant: item.merchant,
            amount: item.amount,
            storage_link: item.storage_link,
            extraction_confidence: item.extraction_confidence,
            link_count: 0,
            confirmed_link_count: 0
          }))
      };
    }

    throw new Error(`Unhandled SQL in MockDb: ${sql}`);
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

  const servicePath = path.resolve(__dirname, 'src', 'services', 'evidenceIngestionService.js');
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
  const createdFiles = [];

  try {
    const firstUpload = await service.ingestEvidence({
      userId: 'user-evidence',
      database: mockDb,
      capturedAt: new Date('2026-03-14T09:15:00Z'),
      body: {
        type: 'receipt',
        raw_text: 'Tesco receipt dated 14/03/2026 total GBP 12.50',
        notes: 'Fuel and lunch'
      },
      file: {
        originalname: 'tesco_receipt_2026-03-14_12.50.jpg',
        mimetype: 'image/jpeg',
        buffer: Buffer.from('sample-image-binary'),
        size: 19
      }
    });

    createdFiles.push(firstUpload.evidence.extraction_payload.storage.absolute_path);

    assert.strictEqual(firstUpload.evidence.type, 'RECEIPT');
    assert.strictEqual(firstUpload.evidence.doc_date, '2026-03-14');
    assert.strictEqual(firstUpload.evidence.merchant, 'Tesco');
    assert.strictEqual(firstUpload.evidence.amount, 12.5);
    assert(firstUpload.evidence.storage_link.startsWith('/uploads/evidence/user-evidence/2026/03/14/'));
    assert(fs.existsSync(firstUpload.evidence.extraction_payload.storage.absolute_path));
    assert(firstUpload.evidence.extraction_confidence > 0.7);
    assert.strictEqual(firstUpload.suggestions.length, 1);
    assert.deepStrictEqual(firstUpload.warnings, []);

    const secondUpload = await service.ingestEvidence({
      userId: 'user-evidence',
      database: mockDb,
      capturedAt: new Date('2026-03-14T10:30:00Z'),
      extractor: () => {
        throw new Error('ocr provider unavailable');
      },
      body: {
        type: 'invoice',
        merchant: 'Fallback Services'
      },
      file: {
        originalname: 'fallback_invoice.pdf',
        mimetype: 'application/pdf',
        buffer: Buffer.from('pdf-binary'),
        size: 10
      }
    });

    createdFiles.push(secondUpload.evidence.extraction_payload.storage.absolute_path);

    assert.strictEqual(secondUpload.evidence.type, 'INVOICE');
    assert.strictEqual(secondUpload.evidence.merchant, 'Fallback Services');
    assert.strictEqual(secondUpload.evidence.extraction_confidence, 0);
    assert.strictEqual(secondUpload.evidence.extraction_payload.extraction.extraction_error, 'ocr provider unavailable');
    assert(fs.existsSync(secondUpload.evidence.extraction_payload.storage.absolute_path));
    assert.deepStrictEqual(secondUpload.warnings, []);

    const suggestionFailureDb = new MockDb();
    const originalQuery = suggestionFailureDb.query.bind(suggestionFailureDb);
    suggestionFailureDb.query = async (text, params = []) => {
      const sql = text.replace(/\s+/g, ' ').trim();
      if (sql.includes('FROM bank_transactions bt') && sql.includes('CROSS JOIN ev')) {
        throw new Error('candidate lookup unavailable');
      }
      return originalQuery(text, params);
    };

    const { service: suggestionFailureService } = loadModules(suggestionFailureDb);
    const thirdUpload = await suggestionFailureService.ingestEvidence({
      userId: 'user-evidence',
      database: suggestionFailureDb,
      capturedAt: new Date('2026-03-14T11:45:00Z'),
      body: {
        type: 'receipt',
        raw_text: 'Merchant: Tesco Date: 14/03/2026 Total GBP 12.50'
      },
      file: {
        originalname: 'tesco_receipt_followup.jpg',
        mimetype: 'image/jpeg',
        buffer: Buffer.from('sample-image-binary'),
        size: 19
      }
    });

    createdFiles.push(thirdUpload.evidence.extraction_payload.storage.absolute_path);
    assert.strictEqual(thirdUpload.evidence.merchant, 'Tesco');
    assert.deepStrictEqual(thirdUpload.suggestions, []);
    assert.strictEqual(thirdUpload.warnings.length, 1);

    const listRes = createResponse();
    await controller.listEvidenceRecords(
      { user: { id: 'user-evidence' }, query: { limit: 10 } },
      listRes
    );
    assert.strictEqual(listRes.statusCode, 200);
    assert.strictEqual(listRes.body.length, 2);

    const detailRes = createResponse();
    await controller.getEvidenceRecord(
      { user: { id: 'user-evidence' }, params: { id: firstUpload.evidence.id } },
      detailRes
    );
    assert.strictEqual(detailRes.statusCode, 200);
    assert.strictEqual(detailRes.body.evidence.id, firstUpload.evidence.id);
    assert.strictEqual(detailRes.body.suggestions.length, 1);

    console.log('verify_evidence_pipeline=PASS');
    console.log(JSON.stringify({
      evidence_storage_ok: true,
      metadata_extraction_ok: true,
      retrieval_endpoints_ok: true,
      fallback_ingestion_non_blocking_ok: true,
      suggestion_failure_non_blocking_ok: true,
      stored_records: mockDb.evidenceRecords.length
    }));
  } finally {
    for (const target of createdFiles) {
      if (target && fs.existsSync(target)) {
        fs.unlinkSync(target);
      }
    }
  }
}

main().catch((error) => {
  console.error('verify_evidence_pipeline_failed');
  console.error(error);
  process.exit(1);
});
