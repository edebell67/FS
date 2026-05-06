const VOICE_MICRO_DECISION_TABS = new Set(['inbox', 'quarter']);

function findVoiceContextCard(inboxCards = [], activeVoiceContextId = '') {
  if (!activeVoiceContextId) {
    return null;
  }
  return inboxCards.find((card) => String(card.id) === String(activeVoiceContextId)) || null;
}

function buildVoiceMicroDecisionRequest({
  currentTab,
  transcript,
  activeVoiceContextId,
  inboxCards = [],
}) {
  if (!VOICE_MICRO_DECISION_TABS.has(currentTab)) {
    return null;
  }

  const card = findVoiceContextCard(inboxCards, activeVoiceContextId);
  if (!card) {
    return {
      error: 'Select a finish-now item before using voice triage.',
      card: null,
    };
  }

  return {
    endpoint: '/voice/micro-decision',
    card,
    payload: {
      transcript,
      bank_txn_id: card.id,
      context_scope: currentTab === 'quarter' ? 'finish_now' : 'inbox',
    },
  };
}

function reduceVoiceMicroDecisionChip(previousChip, response = {}, card = null) {
  if (!card) {
    return previousChip;
  }

  const nextLabels = Array.isArray(response.applied_actions)
    ? response.applied_actions.map((action) => action?.label).filter(Boolean)
    : [];
  const previousLabels = previousChip?.targetId === card.id && Array.isArray(previousChip.labels)
    ? previousChip.labels
    : [];
  const labels = Array.from(new Set([...previousLabels, ...nextLabels]));

  return {
    targetId: card.id,
    targetLabel: card.merchant || 'Selected blocker',
    confirmationChip: response.confirmation_chip || '',
    labels,
    actionStatus: response.action_status || 'execute',
    undoSupported: Boolean(response.undo?.supported),
  };
}

export {
  buildVoiceMicroDecisionRequest,
  findVoiceContextCard,
  reduceVoiceMicroDecisionChip,
};
