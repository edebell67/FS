const db = require('../config/db');
const { DEFAULT_USER_ID, getTopSuggestions } = require('./evidenceIngestionService');

const normalizeMethod = (value = 'manual') => {
  const normalized = String(value || 'manual').trim().toLowerCase();
  return ['suggested', 'manual', 'voice'].includes(normalized) ? normalized : 'manual';
};

async function calculateLinkConfidence({ userId, evidenceId, bankTxnId, database = db }) {
  const score = await database.query(
    `
    SELECT
      GREATEST(0, 1 - LEAST(1, ABS(COALESCE(bt.amount, 0) - COALESCE(ev.amount, 0)) / NULLIF(GREATEST(ABS(COALESCE(ev.amount, 1)), 1), 0))) AS amount_score,
      GREATEST(0, 1 - LEAST(1, ABS(bt.txn_date - COALESCE(ev.doc_date, bt.txn_date)) / 14.0)) AS date_score,
      similarity(COALESCE(bt.merchant, ''), COALESCE(ev.merchant, '')) AS merchant_score
    FROM bank_transactions bt
    JOIN evidence ev ON ev.id = $2 AND ev.user_id = $1
    WHERE bt.id = $3 AND bt.user_id = $1
    `,
    [userId, evidenceId, bankTxnId]
  );

  if (!score.rows.length) {
    return null;
  }

  const row = score.rows[0];
  return Math.max(
    0,
    Math.min(
      1,
      (0.45 * Number(row.amount_score || 0)) +
      (0.35 * Number(row.date_score || 0)) +
      (0.2 * Number(row.merchant_score || 0))
    )
  );
}

async function clearEvidenceLinks({ userId, evidenceId, database = db }) {
  await database.query(
    `
    DELETE FROM evidence_links
    WHERE user_id = $1 AND evidence_id = $2
    `,
    [userId, evidenceId]
  );
}

async function confirmMatch({
  userId = DEFAULT_USER_ID,
  evidenceId,
  bankTxnId,
  method = 'manual',
  database = db
} = {}) {
  if (!evidenceId || !bankTxnId) {
    throw new Error('evidenceId and bankTxnId are required to confirm a match.');
  }

  const confidence = await calculateLinkConfidence({
    userId,
    evidenceId,
    bankTxnId,
    database
  });

  if (confidence === null) {
    return null;
  }

  await clearEvidenceLinks({ userId, evidenceId, database });
  const result = await database.query(
    `
    INSERT INTO evidence_links (user_id, evidence_id, bank_txn_id, link_confidence, user_confirmed, confirmed_at, method)
    VALUES ($1,$2,$3,$4,true,CURRENT_TIMESTAMP,$5)
    RETURNING *
    `,
    [userId, evidenceId, bankTxnId, confidence, normalizeMethod(method)]
  );

  return result.rows[0];
}

async function rejectMatch({
  userId = DEFAULT_USER_ID,
  evidenceId,
  method = 'manual',
  database = db
} = {}) {
  if (!evidenceId) {
    throw new Error('evidenceId is required to persist a no-match decision.');
  }

  await clearEvidenceLinks({ userId, evidenceId, database });
  const result = await database.query(
    `
    INSERT INTO evidence_links (user_id, evidence_id, bank_txn_id, link_confidence, user_confirmed, confirmed_at, method)
    VALUES ($1,$2,NULL,0,true,CURRENT_TIMESTAMP,$3)
    RETURNING *
    `,
    [userId, evidenceId, normalizeMethod(method)]
  );

  return result.rows[0];
}

async function deferMatch({
  userId = DEFAULT_USER_ID,
  evidenceId,
  bankTxnId = null,
  method = 'manual',
  database = db
} = {}) {
  if (!evidenceId) {
    throw new Error('evidenceId is required to defer a match.');
  }

  let confidence = null;
  if (bankTxnId) {
    confidence = await calculateLinkConfidence({
      userId,
      evidenceId,
      bankTxnId,
      database
    });
    if (confidence === null) {
      return null;
    }
  }

  await clearEvidenceLinks({ userId, evidenceId, database });
  const result = await database.query(
    `
    INSERT INTO evidence_links (user_id, evidence_id, bank_txn_id, link_confidence, user_confirmed, confirmed_at, method)
    VALUES ($1,$2,$3,$4,false,NULL,$5)
    RETURNING *
    `,
    [userId, evidenceId, bankTxnId, confidence, normalizeMethod(method)]
  );

  return result.rows[0];
}

async function getPendingEvidence({
  userId = DEFAULT_USER_ID,
  limit = 50,
  database = db
} = {}) {
  const safeLimit = Math.max(1, Math.min(200, Number(limit) || 50));
  const result = await database.query(
    `
    SELECT
      e.id AS evidence_id,
      e.type,
      e.captured_at,
      e.doc_date,
      e.merchant,
      e.amount,
      e.storage_link,
      COALESCE(e.extraction_confidence, 0) AS extraction_confidence,
      decision.bank_txn_id AS pending_bank_txn_id,
      COALESCE(decision.user_confirmed, false) AS user_confirmed,
      decision.method,
      CASE
        WHEN decision.user_confirmed = TRUE AND decision.bank_txn_id IS NOT NULL THEN 'confirmed_match'
        WHEN decision.user_confirmed = TRUE AND decision.bank_txn_id IS NULL THEN 'confirmed_no_match'
        WHEN decision.bank_txn_id IS NOT NULL THEN 'deferred_match'
        ELSE 'pending_review'
      END AS match_state
    FROM evidence e
    LEFT JOIN LATERAL (
      SELECT el.bank_txn_id, el.user_confirmed, el.method, el.confirmed_at, el.created_at
      FROM evidence_links el
      WHERE el.user_id = $1 AND el.evidence_id = e.id
      ORDER BY
        CASE WHEN el.user_confirmed THEN 0 ELSE 1 END,
        el.confirmed_at DESC NULLS LAST,
        el.created_at DESC
      LIMIT 1
    ) AS decision ON TRUE
    WHERE e.user_id = $1
      AND COALESCE(decision.user_confirmed, false) = false
    ORDER BY e.captured_at ASC
    LIMIT $2
    `,
    [userId, safeLimit]
  );

  return result.rows;
}

async function confirmSuggestedMatch({
  userId = DEFAULT_USER_ID,
  evidenceId,
  rank = 1,
  method = 'voice',
  database = db
} = {}) {
  const suggestions = await getTopSuggestions(userId, evidenceId, 3, database);
  const chosen = suggestions[Number(rank) - 1];
  if (!chosen?.bank_txn_id) {
    return null;
  }

  const persisted = await confirmMatch({
    userId,
    evidenceId,
    bankTxnId: chosen.bank_txn_id,
    method,
    database
  });

  return persisted ? { persisted, bank_txn_id: chosen.bank_txn_id } : null;
}

module.exports = {
  calculateLinkConfidence,
  clearEvidenceLinks,
  confirmMatch,
  confirmSuggestedMatch,
  deferMatch,
  getPendingEvidence,
  rejectMatch
};
