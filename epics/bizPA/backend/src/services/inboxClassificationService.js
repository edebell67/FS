const {
  deriveQuarterFromDate,
  recordReadinessRecalculated,
} = require('./businessEventLogService');

async function recordReadinessForTransaction(executor, userId, bankTxnId, txnDate, summary, description) {
  await recordReadinessRecalculated(executor, {
    user_id: userId,
    actor_id: userId,
    source_type: summary?.source || 'manual',
    quarter_reference: deriveQuarterFromDate(txnDate),
    entity_id: bankTxnId,
    entity_type: 'bank_transaction',
    description,
    metadata: summary,
  });
}

async function upsertTransactionClassification(executor, {
  userId,
  bankTxnId,
  changedBy = userId,
  updates = {},
  auditSource = 'ui',
  readinessDescription = null,
}) {
  const existing = await executor.query(
    'SELECT * FROM transaction_classifications WHERE bank_txn_id = $1 AND user_id = $2',
    [bankTxnId, userId]
  );
  const previous = existing.rows[0] || null;

  const next = {
    category_code: updates.category_code !== undefined ? updates.category_code : previous?.category_code || null,
    category_name: updates.category_name !== undefined ? updates.category_name : previous?.category_name || null,
    business_personal: updates.business_personal !== undefined ? updates.business_personal : previous?.business_personal || null,
    is_split: updates.is_split !== undefined ? Boolean(updates.is_split) : Boolean(previous?.is_split),
    split_business_pct: null,
    confidence: updates.confidence !== undefined ? updates.confidence : previous?.confidence ?? null,
    source: updates.source !== undefined ? updates.source : previous?.source || 'manual',
  };

  if (next.is_split) {
    if (updates.split_business_pct !== undefined) {
      next.split_business_pct = updates.split_business_pct;
    } else {
      next.split_business_pct = previous?.split_business_pct ?? null;
    }
  }

  const upsert = await executor.query(
    `
    INSERT INTO transaction_classifications
    (user_id, bank_txn_id, category_code, category_name, business_personal, is_split, split_business_pct, confidence, source)
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
    ON CONFLICT (bank_txn_id)
    DO UPDATE SET
      category_code = EXCLUDED.category_code,
      category_name = EXCLUDED.category_name,
      business_personal = EXCLUDED.business_personal,
      is_split = EXCLUDED.is_split,
      split_business_pct = EXCLUDED.split_business_pct,
      confidence = EXCLUDED.confidence,
      source = EXCLUDED.source,
      updated_at = CURRENT_TIMESTAMP
    RETURNING *
    `,
    [
      userId,
      bankTxnId,
      next.category_code,
      next.category_name,
      next.business_personal,
      next.is_split,
      next.split_business_pct,
      next.confidence,
      next.source,
    ]
  );

  await executor.query(
    `
    INSERT INTO transaction_audit_log (user_id, bank_txn_id, changed_by, field_name, previous_value, new_value, change_source)
    VALUES ($1,$2,$3,$4,$5,$6,$7)
    `,
    [userId, bankTxnId, changedBy, 'classification', previous, upsert.rows[0], auditSource]
  );

  const bankTxn = await executor.query(
    'SELECT txn_date FROM bank_transactions WHERE id = $1 AND user_id = $2',
    [bankTxnId, userId]
  );

  await recordReadinessForTransaction(
    executor,
    userId,
    bankTxnId,
    bankTxn.rows[0]?.txn_date,
    {
      category_code: upsert.rows[0].category_code,
      business_personal: upsert.rows[0].business_personal,
      is_split: upsert.rows[0].is_split,
      split_business_pct: upsert.rows[0].split_business_pct,
      source: upsert.rows[0].source,
    },
    readinessDescription || `Inbox classification updated for transaction ${bankTxnId}`
  );

  return upsert.rows[0];
}

module.exports = {
  upsertTransactionClassification,
};
