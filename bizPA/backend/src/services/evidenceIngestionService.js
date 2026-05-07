const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const db = require('../config/db');

const DEFAULT_USER_ID = '00000000-0000-0000-0000-000000000000';
const STORAGE_ROOT = path.resolve(__dirname, '../../uploads/evidence');
const MERCHANT_STOPWORDS = new Set([
  'receipt',
  'invoice',
  'evidence',
  'scan',
  'photo',
  'image',
  'document',
  'copy',
  'attachment',
  'page',
  'paid',
  'payment',
  'statement',
  'bank',
  'feed',
  'file',
  'upload',
  'dated',
  'date',
  'total',
  'gbp',
  'and'
]);

function sanitizePathSegment(value) {
  return String(value || 'unknown')
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, '_')
    .replace(/^_+|_+$/g, '') || 'unknown';
}

function sanitizeFilename(value) {
  const parsed = path.parse(String(value || 'evidence'));
  const base = parsed.name
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 80) || 'evidence';
  const ext = (parsed.ext || '').replace(/[^a-z0-9.]/gi, '').slice(0, 10);
  return `${base}${ext || ''}`;
}

function normalizeEvidenceType(value) {
  const normalized = String(value || 'RECEIPT').trim().toUpperCase();
  if (['RECEIPT', 'INVOICE', 'OTHER'].includes(normalized)) {
    return normalized;
  }
  return 'OTHER';
}

function parseAmountCandidate(rawValue) {
  if (rawValue === null || rawValue === undefined || rawValue === '') return null;
  const normalized = String(rawValue).replace(/[, ]+/g, '').replace(/[^\d.-]/g, '');
  if (!normalized || normalized === '-' || normalized === '.' || normalized === '-.') return null;
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? Number(parsed.toFixed(2)) : null;
}

function normalizeDateCandidate(rawValue) {
  if (!rawValue) return null;
  if (rawValue instanceof Date && !Number.isNaN(rawValue.valueOf())) {
    return rawValue.toISOString().slice(0, 10);
  }

  const value = String(rawValue).trim();
  if (!value) return null;

  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return value;

  const gbMatch = value.match(/\b(\d{1,2})[\/.-](\d{1,2})[\/.-](\d{2,4})\b/);
  if (gbMatch) {
    const day = Number(gbMatch[1]);
    const month = Number(gbMatch[2]);
    const year = Number(gbMatch[3].length === 2 ? `20${gbMatch[3]}` : gbMatch[3]);
    if (day >= 1 && day <= 31 && month >= 1 && month <= 12) {
      return `${year.toString().padStart(4, '0')}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    }
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.valueOf())) return null;
  return parsed.toISOString().slice(0, 10);
}

function pickMerchantFromTokens(rawValue) {
  const rawTokens = String(rawValue || '')
    .split(/[^a-z0-9]+/i)
    .map((token) => token.trim())
    .filter(Boolean);

  const tokens = [];
  for (const token of rawTokens) {
    const lower = token.toLowerCase();
    if (/^\d+$/.test(token)) {
      if (tokens.length) break;
      continue;
    }
    if (MERCHANT_STOPWORDS.has(lower)) {
      if (tokens.length) break;
      continue;
    }
    tokens.push(token);
    if (tokens.length >= 3) break;
  }

  if (!tokens.length) return null;
  return tokens
    .map((token) => token.charAt(0).toUpperCase() + token.slice(1).toLowerCase())
    .join(' ');
}

function buildExtractionText(body = {}, file = {}) {
  const parts = [
    body.raw_text,
    body.extracted_text,
    body.notes,
    body.note,
    body.transcript,
    body.description,
    body.merchant,
    file.originalname ? path.parse(file.originalname).name.replace(/[_-]+/g, ' ') : null
  ];

  return parts
    .filter((part) => part !== null && part !== undefined && part !== '')
    .map((part) => String(part))
    .join(' | ');
}

function extractMerchantFromText(text) {
  if (!text) return null;

  const labeledMatch = text.match(/\b(?:merchant|seller|vendor|shop|store)[:= -]+([a-z0-9 &.'-]{2,80})/i);
  if (labeledMatch) {
    return labeledMatch[1].trim().replace(/\s+/g, ' ');
  }

  const fromMatch = text.match(/\b(?:from|at)\s+([A-Za-z][A-Za-z0-9&.' -]{1,60})/);
  if (fromMatch) {
    return fromMatch[1].trim().replace(/\s+/g, ' ');
  }

  return pickMerchantFromTokens(text);
}

function extractMerchant({ body = {}, file = {} } = {}) {
  const filenameCandidate = file.originalname ? pickMerchantFromTokens(path.parse(file.originalname).name) : null;
  if (filenameCandidate) {
    return filenameCandidate;
  }

  const candidateSources = [
    body.raw_text,
    body.extracted_text,
    body.description,
    body.note,
    body.notes,
    body.transcript
  ];

  for (const source of candidateSources) {
    const candidate = extractMerchantFromText(source);
    if (candidate) return candidate;
  }
  return null;
}

function extractAmountFromText(text) {
  if (!text) return null;
  const currencyMatch = text.match(/(?:£|\bGBP\b)\s*([0-9]+(?:[.,][0-9]{2})?)/i);
  if (currencyMatch) return parseAmountCandidate(currencyMatch[1]);

  const genericMatch = text.match(/\btotal\b[:= -]*([0-9]+(?:[.,][0-9]{2})?)/i) || text.match(/\b([0-9]+(?:[.,][0-9]{2}))\b/);
  return genericMatch ? parseAmountCandidate(genericMatch[1]) : null;
}

function extractDateFromText(text) {
  if (!text) return null;
  const isoMatch = text.match(/\b\d{4}-\d{2}-\d{2}\b/);
  if (isoMatch) return normalizeDateCandidate(isoMatch[0]);

  const gbMatch = text.match(/\b\d{1,2}[\/.-]\d{1,2}[\/.-]\d{2,4}\b/);
  return gbMatch ? normalizeDateCandidate(gbMatch[0]) : null;
}

function roundConfidence(value) {
  return Number(Math.max(0, Math.min(1, value)).toFixed(3));
}

function extractMetadata({ body = {}, file = {} } = {}) {
  const text = buildExtractionText(body, file);
  const fileStats = {
    original_name: file.originalname || null,
    mime_type: file.mimetype || null,
    size_bytes: Number(file.size || file.buffer?.length || 0) || 0
  };

  const explicitAmount = parseAmountCandidate(body.amount);
  const explicitDate = normalizeDateCandidate(body.doc_date);
  const explicitMerchant = body.merchant ? String(body.merchant).trim() : null;

  const inferredAmount = explicitAmount ?? extractAmountFromText(text);
  const inferredDate = explicitDate ?? extractDateFromText(text);
  const inferredMerchant = explicitMerchant || extractMerchant({ body, file });

  const fieldConfidence = {
    amount: explicitAmount !== null ? 0.99 : inferredAmount !== null ? 0.76 : 0,
    doc_date: explicitDate ? 0.99 : inferredDate ? 0.72 : 0,
    merchant: explicitMerchant ? 0.99 : inferredMerchant ? 0.68 : 0
  };

  const populatedScores = Object.values(fieldConfidence).filter((score) => score > 0);
  const extractionConfidence = populatedScores.length
    ? roundConfidence(populatedScores.reduce((sum, score) => sum + score, 0) / populatedScores.length)
    : 0;

  return {
    amount: inferredAmount,
    doc_date: inferredDate,
    merchant: inferredMerchant,
    extraction_confidence: extractionConfidence,
    extraction_payload: {
      source_fields: Object.keys(body || {}),
      extraction_text: text || null,
      file: fileStats,
      field_confidence: fieldConfidence,
      missing_fields: Object.entries({
        amount: inferredAmount,
        doc_date: inferredDate,
        merchant: inferredMerchant
      })
        .filter(([, value]) => value === null || value === undefined || value === '')
        .map(([key]) => key)
    }
  };
}

function ensureDirectory(targetDir) {
  fs.mkdirSync(targetDir, { recursive: true });
}

function persistEvidenceFile({ userId, file, capturedAt = new Date() }) {
  if (!file?.buffer?.length) {
    throw new Error('Missing in-memory evidence file buffer.');
  }

  const year = String(capturedAt.getUTCFullYear());
  const month = String(capturedAt.getUTCMonth() + 1).padStart(2, '0');
  const day = String(capturedAt.getUTCDate()).padStart(2, '0');
  const targetDir = path.join(STORAGE_ROOT, sanitizePathSegment(userId), year, month, day);
  ensureDirectory(targetDir);

  const uniquePrefix = `${capturedAt.toISOString().replace(/[:.]/g, '').replace('T', '_').replace('Z', '')}_${crypto.randomUUID().slice(0, 8)}`;
  const filename = `${uniquePrefix}_${sanitizeFilename(file.originalname)}`;
  const absolutePath = path.join(targetDir, filename);
  fs.writeFileSync(absolutePath, file.buffer);

  const relativePath = path.relative(path.resolve(__dirname, '../../uploads'), absolutePath).replace(/\\/g, '/');

  return {
    absolute_path: absolutePath,
    storage_link: `/uploads/${relativePath}`
  };
}

async function getTopSuggestions(userId, evidenceId, limit = 3, database = db) {
  const query = `
    WITH ev AS (
      SELECT id, doc_date, merchant, amount
      FROM evidence
      WHERE id = $1 AND user_id = $2
    )
    SELECT
      bt.id AS bank_txn_id,
      bt.txn_date,
      bt.merchant,
      bt.amount,
      bt.direction,
      GREATEST(0, 1 - LEAST(1, ABS(COALESCE(bt.amount, 0) - COALESCE(ev.amount, 0)) / NULLIF(GREATEST(ABS(COALESCE(ev.amount, 1)), 1), 0))) AS amount_score,
      GREATEST(0, 1 - LEAST(1, ABS(bt.txn_date - COALESCE(ev.doc_date, bt.txn_date)) / 14.0)) AS date_score,
      similarity(COALESCE(bt.merchant, ''), COALESCE(ev.merchant, '')) AS merchant_score
    FROM bank_transactions bt
    CROSS JOIN ev
    WHERE bt.user_id = $2
    ORDER BY (0.45 * GREATEST(0, 1 - LEAST(1, ABS(COALESCE(bt.amount, 0) - COALESCE(ev.amount, 0)) / NULLIF(GREATEST(ABS(COALESCE(ev.amount, 1)), 1), 0)))
             +0.35 * GREATEST(0, 1 - LEAST(1, ABS(bt.txn_date - COALESCE(ev.doc_date, bt.txn_date)) / 14.0))
             +0.20 * similarity(COALESCE(bt.merchant, ''), COALESCE(ev.merchant, ''))) DESC
    LIMIT $3
  `;
  const result = await database.query(query, [evidenceId, userId, limit]);
  return result.rows;
}

async function ingestEvidence({
  userId = DEFAULT_USER_ID,
  file,
  body = {},
  database = db,
  extractor = extractMetadata,
  capturedAt = new Date()
} = {}) {
  if (!file?.buffer?.length) {
    throw new Error('Missing evidence file upload.');
  }

  const storage = persistEvidenceFile({ userId, file, capturedAt });

  let extracted;
  try {
    extracted = extractor({ body, file });
  } catch (error) {
    extracted = {
      amount: parseAmountCandidate(body.amount),
      doc_date: normalizeDateCandidate(body.doc_date),
      merchant: body.merchant ? String(body.merchant).trim() : null,
      extraction_confidence: 0,
      extraction_payload: {
        extraction_error: error.message,
        source_fields: Object.keys(body || {}),
        file: {
          original_name: file.originalname || null,
          mime_type: file.mimetype || null,
          size_bytes: Number(file.size || file.buffer?.length || 0) || 0
        }
      }
    };
  }

  const mergedPayload = {
    ...(body || {}),
    storage: {
      storage_link: storage.storage_link,
      absolute_path: storage.absolute_path
    },
    extraction: extracted.extraction_payload
  };

  const created = await database.query(
    `
    INSERT INTO evidence (
      user_id,
      type,
      doc_date,
      merchant,
      amount,
      storage_link,
      extraction_confidence,
      extraction_payload
    )
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
    RETURNING *
    `,
    [
      userId,
      normalizeEvidenceType(body.type),
      extracted.doc_date,
      extracted.merchant,
      extracted.amount,
      storage.storage_link,
      extracted.extraction_confidence,
      mergedPayload
    ]
  );

  const evidence = created.rows[0];
  let suggestions = [];
  const warnings = [];
  try {
    suggestions = await getTopSuggestions(userId, evidence.id, 3, database);
  } catch (error) {
    warnings.push('Evidence captured, but matching suggestions could not be loaded.');
  }
  return {
    evidence,
    suggestions,
    warnings
  };
}

async function getEvidenceById({ evidenceId, userId = DEFAULT_USER_ID, database = db } = {}) {
  const result = await database.query(
    `
    SELECT
      e.*,
      COALESCE(
        JSON_AGG(
          JSON_BUILD_OBJECT(
            'id', el.id,
            'bank_txn_id', el.bank_txn_id,
            'link_confidence', el.link_confidence,
            'user_confirmed', el.user_confirmed,
            'confirmed_at', el.confirmed_at,
            'method', el.method
          )
          ORDER BY el.created_at ASC
        ) FILTER (WHERE el.id IS NOT NULL),
        '[]'::json
      ) AS links
    FROM evidence e
    LEFT JOIN evidence_links el ON el.evidence_id = e.id
    WHERE e.id = $1 AND e.user_id = $2
    GROUP BY e.id
    `,
    [evidenceId, userId]
  );
  return result.rows[0] || null;
}

async function listEvidence({ userId = DEFAULT_USER_ID, limit = 50, database = db } = {}) {
  const safeLimit = Math.max(1, Math.min(200, Number(limit) || 50));
  const result = await database.query(
    `
    SELECT
      e.id,
      e.type,
      e.captured_at,
      e.doc_date,
      e.merchant,
      e.amount,
      e.storage_link,
      COALESCE(e.extraction_confidence, 0) AS extraction_confidence,
      COUNT(el.id)::int AS link_count,
      COUNT(*) FILTER (WHERE el.user_confirmed = TRUE)::int AS confirmed_link_count
    FROM evidence e
    LEFT JOIN evidence_links el ON el.evidence_id = e.id
    WHERE e.user_id = $1
    GROUP BY e.id
    ORDER BY e.captured_at DESC
    LIMIT $2
    `,
    [userId, safeLimit]
  );
  return result.rows;
}

module.exports = {
  DEFAULT_USER_ID,
  STORAGE_ROOT,
  extractMetadata,
  getEvidenceById,
  getTopSuggestions,
  ingestEvidence,
  listEvidence,
  normalizeDateCandidate,
  parseAmountCandidate,
  persistEvidenceFile
};
