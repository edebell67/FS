const express = require('express');
const multer = require('multer');
const evidenceController = require('../controllers/evidenceController');

const router = express.Router();
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 15 * 1024 * 1024
  }
});

// GET /api/v1/evidence
router.get('/', evidenceController.listEvidenceRecords);

// GET /api/v1/evidence/pending
router.get('/pending', evidenceController.listPendingEvidenceRecords);

// POST /api/v1/evidence/upload
router.post('/upload', upload.single('file'), evidenceController.uploadEvidence);

// GET /api/v1/evidence/:id/suggestions
router.get('/:id/suggestions', evidenceController.getEvidenceSuggestions);

// POST /api/v1/evidence/:id/confirm-match
router.post('/:id/confirm-match', evidenceController.confirmEvidenceMatch);

// POST /api/v1/evidence/:id/defer-match
router.post('/:id/defer-match', evidenceController.deferEvidenceMatch);

// GET /api/v1/evidence/:id
router.get('/:id', evidenceController.getEvidenceRecord);

module.exports = router;
