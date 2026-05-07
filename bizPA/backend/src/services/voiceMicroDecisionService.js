const INBOX_CONTEXT = 'inbox';
const FINISH_NOW_CONTEXT = 'finish_now';
const EVIDENCE_CONTEXT = 'evidence';

const CONTEXT_ALLOWED_COMMANDS = {
  [INBOX_CONTEXT]: new Set(['category', 'business_personal', 'split']),
  [FINISH_NOW_CONTEXT]: new Set(['category', 'business_personal', 'split']),
  [EVIDENCE_CONTEXT]: new Set(['attach_receipt', 'match_rank', 'no_match']),
};

const TRANSACTION_COMMANDS = new Set(['category', 'business_personal', 'split']);
const EVIDENCE_COMMANDS = new Set(['attach_receipt', 'match_rank', 'no_match']);

const normalizeTranscript = (transcript = '') => String(transcript).trim();

const parseVoiceMicroDecision = (transcript = '') => {
  const raw = normalizeTranscript(transcript);
  const text = raw.toLowerCase();
  if (!raw) {
    return null;
  }

  const categoryMatch = raw.match(/^category\s*:\s*(.+)$/i);
  if (categoryMatch) {
    const categoryName = categoryMatch[1].trim();
    if (!categoryName) {
      return null;
    }
    return {
      type: 'category',
      category_name: categoryName,
      category_code: categoryName.toUpperCase().replace(/[^A-Z0-9]+/g, '_').replace(/^_+|_+$/g, ''),
      confirmation_chip: `Applied: ${categoryName}`,
    };
  }

  if (text === 'business' || text === 'personal') {
    const businessPersonal = text === 'business' ? 'BUSINESS' : 'PERSONAL';
    return {
      type: 'business_personal',
      business_personal: businessPersonal,
      confirmation_chip: `Applied: ${businessPersonal}`,
    };
  }

  const splitMatch = text.match(/^split\s+(\d{1,3})\s*%?$/);
  if (splitMatch) {
    const percentage = Number(splitMatch[1]);
    return {
      type: 'split',
      split_business_pct: percentage,
      business_personal: 'BUSINESS',
      is_split: true,
      confirmation_chip: `Applied: Split ${percentage}%`,
    };
  }

  if (text === 'attach receipt') {
    return {
      type: 'attach_receipt',
      confirmation_chip: 'Attach receipt requested',
    };
  }

  if (text === 'match first' || text === 'match second' || text === 'match third') {
    const rank = text === 'match first' ? 1 : text === 'match second' ? 2 : 3;
    return {
      type: 'match_rank',
      match_rank: rank,
      confirmation_chip: `Applied: Match ${rank}`,
    };
  }

  if (text === 'no match') {
    return {
      type: 'no_match',
      confirmation_chip: 'Applied: No match',
    };
  }

  return null;
};

const validateMicroDecisionContext = (parsedCommand, contextKind) => {
  const normalizedContext = String(contextKind || '').trim().toLowerCase();
  if (!parsedCommand) {
    return {
      ok: false,
      statusCode: 400,
      error: 'Unsupported MVP voice micro-decision command.',
    };
  }
  if (!normalizedContext && TRANSACTION_COMMANDS.has(parsedCommand.type)) {
    return {
      ok: false,
      statusCode: 400,
      error: 'context_scope must be inbox or finish_now for transaction micro-decisions.',
    };
  }
  if (!normalizedContext && EVIDENCE_COMMANDS.has(parsedCommand.type)) {
    return {
      ok: false,
      statusCode: 400,
      error: 'context_scope must be evidence for evidence micro-decisions.',
    };
  }
  const allowedCommands = CONTEXT_ALLOWED_COMMANDS[normalizedContext];
  if (!allowedCommands && TRANSACTION_COMMANDS.has(parsedCommand.type)) {
    return {
      ok: false,
      statusCode: 400,
      error: 'context_scope must be inbox or finish_now for transaction micro-decisions.',
    };
  }
  if (!allowedCommands && EVIDENCE_COMMANDS.has(parsedCommand.type)) {
    return {
      ok: false,
      statusCode: 400,
      error: 'context_scope must be evidence for evidence micro-decisions.',
    };
  }
  if (!allowedCommands.has(parsedCommand.type)) {
    return {
      ok: false,
      statusCode: 409,
      error: `Command "${parsedCommand.type}" is not allowed for ${normalizedContext} context.`,
    };
  }
  return {
    ok: true,
    context_kind: normalizedContext,
  };
};

module.exports = {
  EVIDENCE_CONTEXT,
  FINISH_NOW_CONTEXT,
  INBOX_CONTEXT,
  parseVoiceMicroDecision,
  validateMicroDecisionContext,
};
