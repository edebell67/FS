const db = require('../config/db');
const actionController = require('./actionController');
const searchController = require('./searchController');
const itemController = require('./itemController');
const { isMonetaryItemType } = require('../services/monetaryIntegrityService');
const {
  evaluateAutoCommitEligibility
} = require('../services/autoCommitGovernanceService');
const {
  buildCaptureParseResult,
  toLegacyIntentShape
} = require('../services/voiceCaptureParserService');
const {
  upsertTransactionClassification,
} = require('../services/inboxClassificationService');
const {
  parseVoiceMicroDecision,
  validateMicroDecisionContext,
} = require('../services/voiceMicroDecisionService');
const {
  confirmSuggestedMatch,
  rejectMatch
} = require('../services/evidenceMatchingService');

function buildMicroDecisionResponse({
  actionStatus,
  confirmationChip,
  appliedActions = [],
  contextBinding = null,
  undoSupported = false,
  extra = {},
}) {
  return {
    action_status: actionStatus,
    confirmation_chip: confirmationChip,
    applied_actions: appliedActions,
    context_binding: contextBinding,
    undoable: undoSupported,
    undo: {
      supported: undoSupported,
      route: undoSupported ? '/api/v1/inbox/undo-last' : null,
      method: undoSupported ? 'POST' : null,
    },
    ...extra,
  };
}

/**
 * Simple Intent Parser and Slot Extractor (NLU Mock)
 * Matches transcripts to core intents and extracts slots using regex.
 */
function parseIntent(transcript, clientDateStr = null) {
  const parseResult = buildCaptureParseResult(transcript, clientDateStr);
  console.log(
    `[VoiceController] Intent matched: ${parseResult.detected_intent} ` +
    `confidence=${parseResult.confidence_score} review=${parseResult.requires_review}`
  );
  return toLegacyIntentShape(parseResult);
}

/**
 * Process incoming voice transcript
 */
const processVoice = async (req, res) => {
  const { transcript, device_id, current_date } = req.body;
  const userId = req.user?.id || '00000000-0000-0000-0000-000000000000';
  const requestNow = current_date ? new Date(current_date) : new Date();
  const effectiveNow = Number.isNaN(requestNow.getTime()) ? new Date() : requestNow;

  if (!transcript) {
    return res.status(400).json({ error: 'Missing transcript in request body' });
  }

  console.log(`[VoiceController] Incoming transcript: "${transcript}" from device: ${device_id} (Client Date: ${current_date})`);

  const captureIntents = {
    'capture_receipt': 'receipt',
    'capture_invoice': 'invoice',
    'capture_payment': 'payment',
    'capture_booking': 'booking',
    'capture_quote': 'quote',
    'create_reminder': 'reminder',
    'create_note': 'note',
    'capture_photo': 'image'
  };

  try {
    const parseState = parseIntent(transcript, current_date);
    const { intent, slots, confidence, parse_result: parseResult } = parseState;

    let confirmationText = `I've understood that as ${intent.replace(/_/g, ' ')}.`;
    let actionStatus = 'execute';

    // Handle Intent Logic
    if (captureIntents[intent]) {
      const type = captureIntents[intent];
      const shouldReview = Boolean(parseResult?.requires_review);
      const baseCompositionPayload = parseResult?.composition_payload || {
        type,
        status: itemController.AUTO_COMMIT_NON_MONETARY_TYPES.has(type) ? 'confirmed' : 'draft',
        amount: slots.amount || 0,
        extracted_text: transcript,
        raw_note: (type === 'note' || type === 'reminder') ? (slots.description || transcript) : transcript,
        client_name: slots.client_name || null,
        transaction_date: slots.date || new Date().toISOString().split('T')[0],
        due_date: type === 'reminder' ? (slots.date || new Date().toISOString().split('T')[0]) : null,
        voice_command_source_text: transcript,
        voice_action_confidence: confidence,
        labels: Array.isArray(slots.labels) ? slots.labels : []
      };
      
      // Attempt to find client by name if provided
      let clientId = null;
      if (slots.client_name) {
        const { rows } = await db.query('SELECT id, name FROM clients WHERE LOWER(name) LIKE $1 AND user_id = $2 LIMIT 1', [`%${slots.client_name}%`, userId]);
        if (rows.length > 0) {
          clientId = rows[0].id;
          slots.client_name = rows[0].name; // Use proper name
        }
      }

      if (shouldReview) {
        const reviewPayload = {
          ...baseCompositionPayload,
          client_id: clientId,
          client_name: slots.client_name || baseCompositionPayload.client_name || null,
          device_id
        };
        confirmationText = `I need you to review this ${type} before commit.`;
        actionStatus = 'review_required';
        return res.status(200).json({
          intent,
          slots,
          confidence,
          transcript,
          confirmation_text: confirmationText,
          action_status: actionStatus,
          parser_result: parseResult,
          review_reason: parseResult?.review_reason || 'low_confidence',
          missing_fields: parseResult?.missing_fields || [],
          composition_payload: reviewPayload
        });
      }

      if (isMonetaryItemType(type)) {
        const composition = await itemController.createItemInternal(
          {
            ...baseCompositionPayload,
            type,
            status: 'draft',
            device_id,
            client_id: clientId,
            client_name: slots.client_name || baseCompositionPayload.client_name || null,
            transaction_date: slots.date || baseCompositionPayload.transaction_date || new Date().toISOString()
          },
          { emitBusinessEvents: false }
        );

        const preview = itemController.buildMonetaryPreviewPayload(composition, {
          counterparty_name: slots.client_name || composition.client_name || null
        });

        const eligibility = await evaluateAutoCommitEligibility(db, {
          user_id: userId,
          entity_type: type,
          amount: slots.amount ?? composition.amount ?? preview.gross_amount ?? 0,
          confidence_score: confidence,
          now: effectiveNow
        });

        if (eligibility.eligible) {
          const committed = await itemController.confirmCompositionInternal(composition.id, {
            user_id: userId,
            actor_id: userId,
            source_type: 'voice',
            commit_mode: 'auto',
            now: effectiveNow,
            confirmation_reference: eligibility.state.confirmation_reference,
            updates: {
              client_id: clientId,
              client_name: slots.client_name || composition.client_name || null,
              transaction_date: slots.date || composition.captured_at || composition.created_at
            }
          });

          confirmationText = `Auto-committed ${type}${slots.amount ? ` £${slots.amount}` : ''}.`;
          actionStatus = 'committed';
          return res.status(200).json({
            intent,
            slots,
            confidence,
            transcript,
            confirmation_text: confirmationText,
            action_status: actionStatus,
            composition_id: composition.id,
            committed_entity_id: committed.id,
            item: committed,
            parser_result: parseResult,
            auto_commit: {
              enabled: true,
              expires_at: eligibility.state.expires_at,
              threshold_applied: eligibility.threshold_applied
            }
          });
        }

        confirmationText = `Preview ready for ${type}${slots.amount ? ` £${slots.amount}` : ''}. Confirm to commit.`;
        actionStatus = 'preview_required';
        return res.status(200).json({
          intent,
          slots,
          confidence,
          transcript,
          confirmation_text: confirmationText,
          action_status: actionStatus,
          composition_id: composition.id,
          preview,
          parser_result: parseResult,
          auto_commit: {
            enabled: eligibility.state.auto_commit_enabled,
            reasons_blocked: eligibility.reasons,
            threshold_applied: eligibility.threshold_applied,
            confidence_threshold: eligibility.confidence_threshold
          }
        });
      } else {
        const client = await db.pool.connect();
        try {
          await client.query('BEGIN');

          const created = await itemController.createItemInternal({
            ...baseCompositionPayload,
            type,
            status: 'confirmed',
            device_id,
            user_id: userId,
            client_id: clientId,
            client_name: slots.client_name || baseCompositionPayload.client_name || null,
            due_date: type === 'reminder' ? (slots.date || baseCompositionPayload.due_date || null) : baseCompositionPayload.due_date,
            transaction_date: slots.date || baseCompositionPayload.transaction_date || new Date().toISOString()
          }, { dbClient: client });

          if (type === 'booking') {
            const bookingDate = slots.date || new Date().toISOString();
            await client.query(
              'INSERT INTO calendar_events (user_id, title, start_at, end_at, client_id, event_type, device_id) VALUES ($1, $2, $3, $4, $5, $6, $7)',
              [userId, transcript, bookingDate, bookingDate, clientId, 'appointment', device_id]
            );
            confirmationText = `Booked ${slots.client_name ? 'with ' + slots.client_name : 'your meeting'} for ${slots.date || 'today'}.`;
          } else if (type === 'note') {
            await client.query(
              'INSERT INTO diary_entries (user_id, content, entry_date, client_id) VALUES ($1, $2, $3, $4)',
              [userId, baseCompositionPayload.raw_note || transcript, slots.date || new Date().toISOString(), clientId]
            );
            confirmationText = `Saved to your diary for ${slots.date || 'today'}.`;
          } else if (type === 'reminder') {
            confirmationText = `Reminder set for ${slots.date || 'today'}.`;
          } else {
            confirmationText = `Logged ${created.type}.`;
          }

          await client.query('COMMIT');
        } catch (err) {
          await client.query('ROLLBACK');
          throw err;
        } finally {
          client.release();
        }
      }
    } else if (intent === 'undo_last_action') {
      await db.query(
        `
        DELETE FROM capture_items
        WHERE id IN (
          SELECT id
          FROM capture_items
          WHERE user_id = $1 AND status = 'draft'
          ORDER BY created_at DESC
          LIMIT 1
        )
        `,
        [userId]
      );
      confirmationText = 'Undone. Last draft composition removed.';
    }

    res.status(200).json({
      intent,
      slots,
      confidence,
      transcript,
      confirmation_text: confirmationText,
      action_status: actionStatus,
      parser_result: parseResult || null
    });
  } catch (err) {
    console.error('[VoiceController] Error:', err);
    res.status(500).json({ error: 'Internal Voice Error' });
  }
};

const processMicroDecision = async (req, res) => {
  const userId = req.user?.id || '00000000-0000-0000-0000-000000000000';
  const {
    transcript = '',
    bank_txn_id = null,
    evidence_id = null,
    context_kind = null,
    context_scope = null,
  } = req.body || {};
  const rawTranscript = String(transcript).trim();
  const text = rawTranscript.toLowerCase();
  const normalizedContext = context_kind ?? context_scope;
  const parsedCommand = parseVoiceMicroDecision(rawTranscript);
  const contextValidation = validateMicroDecisionContext(parsedCommand, normalizedContext);
  const normalizedContextScope = contextValidation.ok
    ? contextValidation.context_kind
    : (normalizedContext === null || normalizedContext === undefined
      ? null
      : String(normalizedContext).toLowerCase().replace(/-/g, '_'));

  if (!text) return res.status(400).json({ error: 'Missing transcript.' });
  if (!contextValidation.ok) return res.status(contextValidation.statusCode).json({ error: contextValidation.error });

  try {
    if (parsedCommand.type === 'category') {
      if (!bank_txn_id) return res.status(400).json({ error: 'bank_txn_id is required for inbox voice commands.' });
      const client = await db.pool.connect();
      try {
        await client.query('BEGIN');
        await upsertTransactionClassification(client, {
          userId,
          bankTxnId: bank_txn_id,
          updates: {
            category_code: parsedCommand.category_code,
            category_name: parsedCommand.category_name,
            source: 'voice',
          },
          auditSource: 'voice',
          readinessDescription: `Voice category micro-decision applied for transaction ${bank_txn_id}`,
        });
        await client.query('COMMIT');
      } catch (err) {
        await client.query('ROLLBACK');
        throw err;
      } finally {
        client.release();
      }
      return res.status(200).json(buildMicroDecisionResponse({
        actionStatus: 'execute',
        confirmationChip: parsedCommand.confirmation_chip,
        appliedActions: [{ type: 'category', label: parsedCommand.category_name }],
        contextBinding: {
          scope: normalizedContextScope,
          target_type: 'bank_transaction',
          target_id: bank_txn_id,
        },
        undoSupported: true,
        extra: {
          bank_txn_id,
          parsed_command: parsedCommand,
        },
      }));
    }

    if (parsedCommand.type === 'business_personal') {
      if (!bank_txn_id) return res.status(400).json({ error: 'bank_txn_id is required for inbox voice commands.' });
      const bp = parsedCommand.business_personal;
      const client = await db.pool.connect();
      try {
        await client.query('BEGIN');
        await upsertTransactionClassification(client, {
          userId,
          bankTxnId: bank_txn_id,
          updates: {
            business_personal: bp,
            is_split: false,
            split_business_pct: null,
            source: 'voice',
          },
          auditSource: 'voice',
          readinessDescription: `Voice ${bp.toLowerCase()} micro-decision applied for transaction ${bank_txn_id}`,
        });
        await client.query('COMMIT');
      } catch (err) {
        await client.query('ROLLBACK');
        throw err;
      } finally {
        client.release();
      }
      return res.status(200).json(buildMicroDecisionResponse({
        actionStatus: 'execute',
        confirmationChip: parsedCommand.confirmation_chip,
        appliedActions: [{ type: 'business_personal', label: bp }],
        contextBinding: {
          scope: normalizedContextScope,
          target_type: 'bank_transaction',
          target_id: bank_txn_id,
        },
        undoSupported: true,
        extra: {
          bank_txn_id,
          parsed_command: parsedCommand,
        },
      }));
    }

    if (parsedCommand.type === 'split') {
      if (!bank_txn_id) return res.status(400).json({ error: 'bank_txn_id is required for inbox voice commands.' });
      const pct = Number(parsedCommand.split_business_pct);
      if (Number.isNaN(pct) || pct < 0 || pct > 100) {
        return res.status(400).json({ error: 'Split percentage must be 0-100.' });
      }
      const client = await db.pool.connect();
      try {
        await client.query('BEGIN');
        await upsertTransactionClassification(client, {
          userId,
          bankTxnId: bank_txn_id,
          updates: {
            business_personal: 'BUSINESS',
            is_split: true,
            split_business_pct: pct,
            source: 'voice',
          },
          auditSource: 'voice',
          readinessDescription: `Voice split micro-decision applied for transaction ${bank_txn_id}`,
        });
        await client.query('COMMIT');
      } catch (err) {
        await client.query('ROLLBACK');
        throw err;
      } finally {
        client.release();
      }
      return res.status(200).json(buildMicroDecisionResponse({
        actionStatus: 'execute',
        confirmationChip: parsedCommand.confirmation_chip,
        appliedActions: [{ type: 'split_business_pct', label: `Split ${pct}%` }],
        contextBinding: {
          scope: normalizedContextScope,
          target_type: 'bank_transaction',
          target_id: bank_txn_id,
        },
        undoSupported: true,
        extra: {
          bank_txn_id,
          parsed_command: parsedCommand,
        },
      }));
    }

    if (parsedCommand.type === 'attach_receipt') {
      if (!evidence_id) return res.status(400).json({ error: 'evidence_id is required for attach receipt commands.' });
      return res.status(200).json(buildMicroDecisionResponse({
        actionStatus: 'clarification_needed',
        confirmationChip: parsedCommand.confirmation_chip,
        appliedActions: [{ type: 'attach_receipt', label: 'Attach receipt' }],
        contextBinding: {
          scope: normalizedContextScope,
          target_type: 'evidence',
          target_id: evidence_id,
        },
        extra: {
          evidence_id,
          parsed_command: parsedCommand,
          instruction: 'Use /api/v1/evidence/upload with file + metadata to attach receipt.'
        }
      }));
    }

    if (parsedCommand.type === 'match_rank') {
      if (!evidence_id) return res.status(400).json({ error: 'evidence_id is required for match commands.' });
      const persisted = await confirmSuggestedMatch({
        userId,
        evidenceId: evidence_id,
        rank: parsedCommand.match_rank,
        method: 'voice',
        database: db
      });
      if (!persisted) return res.status(404).json({ error: 'Requested match suggestion not available.' });
      return res.status(200).json(buildMicroDecisionResponse({
        actionStatus: 'execute',
        confirmationChip: parsedCommand.confirmation_chip,
        appliedActions: [{ type: 'evidence_match', label: `Match ${parsedCommand.match_rank}` }],
        contextBinding: {
          scope: normalizedContextScope,
          target_type: 'evidence',
          target_id: evidence_id,
        },
        extra: {
          evidence_id,
          bank_txn_id: persisted.bank_txn_id,
          parsed_command: parsedCommand,
        },
      }));
    }

    if (parsedCommand.type === 'no_match') {
      if (!evidence_id) return res.status(400).json({ error: 'evidence_id is required for no match.' });
      await rejectMatch({
        userId,
        evidenceId: evidence_id,
        method: 'voice',
        database: db
      });
      return res.status(200).json(buildMicroDecisionResponse({
        actionStatus: 'execute',
        confirmationChip: parsedCommand.confirmation_chip,
        appliedActions: [{ type: 'evidence_match', label: 'No match' }],
        contextBinding: {
          scope: normalizedContextScope,
          target_type: 'evidence',
          target_id: evidence_id,
        },
        extra: {
          evidence_id,
          parsed_command: parsedCommand,
        },
      }));
    }

    return res.status(400).json({ error: 'Unsupported MVP voice micro-decision command.' });
  } catch (err) {
    console.error('[VoiceController] processMicroDecision error:', err);
    return res.status(500).json({ error: 'Failed to process micro-decision.' });
  }
};

module.exports = { parseIntent, processVoice, processMicroDecision };
