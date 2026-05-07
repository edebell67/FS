const db = require('../config/db');
const {
  DEFAULT_USER_ID,
  getEvidenceById,
  getTopSuggestions,
  ingestEvidence,
  listEvidence
} = require('../services/evidenceIngestionService');
const {
  confirmMatch,
  deferMatch,
  getPendingEvidence,
  rejectMatch
} = require('../services/evidenceMatchingService');

const uploadEvidence = async (req, res) => {
  const userId = req.user?.id || DEFAULT_USER_ID;
  if (!req.file?.buffer?.length) {
    return res.status(400).json({ error: 'Missing evidence file upload.' });
  }

  try {
    const { evidence, suggestions, warnings = [] } = await ingestEvidence({
      userId,
      file: req.file,
      body: req.body,
      database: db
    });
    return res.status(201).json({ evidence, suggestions, warnings });
  } catch (err) {
    console.error('[EvidenceController] uploadEvidence failed:', err);
    return res.status(500).json({ error: 'Failed to store evidence.' });
  }
};

const listEvidenceRecords = async (req, res) => {
  const userId = req.user?.id || DEFAULT_USER_ID;
  const { limit = 50 } = req.query || {};
  try {
    const rows = await listEvidence({ userId, limit, database: db });
    return res.status(200).json(rows);
  } catch (err) {
    console.error('[EvidenceController] listEvidence failed:', err);
    return res.status(500).json({ error: 'Failed to load evidence records.' });
  }
};

const getEvidenceRecord = async (req, res) => {
  const userId = req.user?.id || DEFAULT_USER_ID;
  const evidenceId = req.params.id;
  try {
    const evidence = await getEvidenceById({ evidenceId, userId, database: db });
    if (!evidence) {
      return res.status(404).json({ error: 'Evidence not found.' });
    }
    const suggestions = await getTopSuggestions(userId, evidenceId, 3, db);
    return res.status(200).json({ evidence, suggestions });
  } catch (err) {
    console.error('[EvidenceController] getEvidenceRecord failed:', err);
    return res.status(500).json({ error: 'Failed to load evidence record.' });
  }
};

const getEvidenceSuggestions = async (req, res) => {
  const userId = req.user?.id || DEFAULT_USER_ID;
  const evidenceId = req.params.id;
  try {
    const suggestions = await getTopSuggestions(userId, evidenceId, 3, db);
    return res.status(200).json(suggestions);
  } catch (err) {
    console.error('[EvidenceController] getEvidenceSuggestions failed:', err);
    return res.status(500).json({ error: 'Failed to load suggestions.' });
  }
};

const listPendingEvidenceRecords = async (req, res) => {
  const userId = req.user?.id || DEFAULT_USER_ID;
  const { limit = 50 } = req.query || {};

  try {
    const rows = await getPendingEvidence({ userId, limit, database: db });
    return res.status(200).json(rows);
  } catch (err) {
    console.error('[EvidenceController] listPendingEvidenceRecords failed:', err);
    return res.status(500).json({ error: 'Failed to load pending evidence records.' });
  }
};

const confirmEvidenceMatch = async (req, res) => {
  const userId = req.user?.id || DEFAULT_USER_ID;
  const evidenceId = req.params.id;
  const { bank_txn_id = null, method = 'manual', no_match = false } = req.body || {};

  try {
    if (no_match || !bank_txn_id) {
      await rejectMatch({ userId, evidenceId, method, database: db });
      return res.status(200).json({ status: 'confirmed_no_match' });
    }

    const persisted = await confirmMatch({
      userId,
      evidenceId,
      bankTxnId: bank_txn_id,
      method,
      database: db
    });
    if (!persisted) return res.status(404).json({ error: 'Evidence or bank transaction not found.' });
    return res.status(200).json({
      status: 'confirmed_match',
      bank_txn_id,
      link_confidence: Number(persisted.link_confidence)
    });
  } catch (err) {
    console.error('[EvidenceController] confirmEvidenceMatch failed:', err);
    return res.status(500).json({ error: 'Failed to confirm evidence match.' });
  }
};

const deferEvidenceMatch = async (req, res) => {
  const userId = req.user?.id || DEFAULT_USER_ID;
  const evidenceId = req.params.id;
  const { bank_txn_id = null, method = 'manual' } = req.body || {};

  try {
    const persisted = await deferMatch({
      userId,
      evidenceId,
      bankTxnId: bank_txn_id,
      method,
      database: db
    });
    if (!persisted) return res.status(404).json({ error: 'Evidence or bank transaction not found.' });
    return res.status(200).json({
      status: 'deferred_match',
      bank_txn_id: persisted.bank_txn_id,
      user_confirmed: persisted.user_confirmed
    });
  } catch (err) {
    console.error('[EvidenceController] deferEvidenceMatch failed:', err);
    return res.status(500).json({ error: 'Failed to defer evidence match.' });
  }
};

module.exports = {
  deferEvidenceMatch,
  getEvidenceRecord,
  listPendingEvidenceRecords,
  uploadEvidence,
  listEvidenceRecords,
  getEvidenceSuggestions,
  confirmEvidenceMatch
};
