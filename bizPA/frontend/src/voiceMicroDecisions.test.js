import {
  buildVoiceMicroDecisionRequest,
  findVoiceContextCard,
  reduceVoiceMicroDecisionChip,
} from './voiceMicroDecisions';

const cards = [
  { id: 'txn-1', merchant: 'Fuel Stop' },
  { id: 'txn-2', merchant: 'Builder Depot' },
];

describe('voice micro-decision helpers', () => {
  test('requires explicit finish-now selection before routing voice triage', () => {
    const request = buildVoiceMicroDecisionRequest({
      currentTab: 'inbox',
      transcript: 'Business',
      activeVoiceContextId: '',
      inboxCards: cards,
    });

    expect(request.error).toBe('Select a finish-now item before using voice triage.');
    expect(request.card).toBeNull();
  });

  test('builds a finish-now scoped request for the selected blocker', () => {
    const request = buildVoiceMicroDecisionRequest({
      currentTab: 'quarter',
      transcript: 'Split 70%',
      activeVoiceContextId: 'txn-2',
      inboxCards: cards,
    });

    expect(request.endpoint).toBe('/voice/micro-decision');
    expect(request.card).toEqual(cards[1]);
    expect(request.payload).toEqual({
      transcript: 'Split 70%',
      bank_txn_id: 'txn-2',
      context_scope: 'finish_now',
    });
  });

  test('keeps the selected voice target discoverable', () => {
    expect(findVoiceContextCard(cards, 'txn-1')).toEqual(cards[0]);
    expect(findVoiceContextCard(cards, 'missing')).toBeNull();
  });

  test('combines applied actions for the same target chip and resets for a new target', () => {
    const first = reduceVoiceMicroDecisionChip(null, {
      confirmation_chip: 'Applied: Travel',
      action_status: 'execute',
      applied_actions: [{ label: 'Travel' }],
      undo: { supported: true },
    }, cards[0]);

    const second = reduceVoiceMicroDecisionChip(first, {
      confirmation_chip: 'Applied: BUSINESS',
      action_status: 'execute',
      applied_actions: [{ label: 'BUSINESS' }],
      undo: { supported: true },
    }, cards[0]);

    const third = reduceVoiceMicroDecisionChip(second, {
      confirmation_chip: 'Applied: Split 70%',
      action_status: 'execute',
      applied_actions: [{ label: 'Split 70%' }],
      undo: { supported: true },
    }, cards[1]);

    expect(second.labels).toEqual(['Travel', 'BUSINESS']);
    expect(second.undoSupported).toBe(true);
    expect(third.targetId).toBe('txn-2');
    expect(third.labels).toEqual(['Split 70%']);
  });
});
