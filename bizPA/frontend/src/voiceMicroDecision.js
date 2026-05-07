const sanitizeCategoryCode = (value) => String(value || '')
  .trim()
  .toUpperCase()
  .replace(/[^A-Z0-9]+/g, '_')
  .replace(/^_+|_+$/g, '');

export const parseInboxVoiceCommand = (transcript = '') => {
  const raw = String(transcript || '').trim();
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
      category_code: sanitizeCategoryCode(categoryName),
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
      business_personal: 'SPLIT',
      is_split: true,
      split_business_pct: percentage,
      confirmation_chip: `Applied: Split ${percentage}%`,
    };
  }

  return null;
};

export const buildInboxVoicePayload = (card, transcript) => ({
  transcript,
  context_kind: 'inbox',
  context_label: 'finish_now',
  bank_txn_id: card?.id || null,
});

export const applyInboxVoiceCommandToDraft = (draft, parsedCommand) => {
  if (!parsedCommand) {
    return draft;
  }
  if (parsedCommand.type === 'category') {
    return {
      ...draft,
      category_code: parsedCommand.category_code,
      category_name: parsedCommand.category_name,
    };
  }
  if (parsedCommand.type === 'business_personal') {
    return {
      ...draft,
      business_personal: parsedCommand.business_personal,
      is_split: false,
      split_business_pct: '',
    };
  }
  if (parsedCommand.type === 'split') {
    return {
      ...draft,
      business_personal: 'SPLIT',
      is_split: true,
      split_business_pct: String(parsedCommand.split_business_pct),
    };
  }
  return draft;
};

export const buildInboxVoiceChip = (response, card) => ({
  tone: response?.action_status === 'clarification_needed' ? 'info' : 'success',
  text: response?.confirmation_chip || response?.confirmation_text || 'Voice action applied.',
  undoable: Boolean(response?.undoable),
  bank_txn_id: response?.bank_txn_id || card?.id || '',
  merchant: card?.merchant || 'Selected blocker',
});
