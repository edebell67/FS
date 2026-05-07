import {
  applyInboxVoiceCommandToDraft,
  buildInboxVoiceChip,
  buildInboxVoicePayload,
  parseInboxVoiceCommand,
} from './voiceMicroDecision';

describe('voiceMicroDecision helpers', () => {
  test('parses category commands into inbox-safe payloads', () => {
    expect(parseInboxVoiceCommand('Category: Travel')).toEqual({
      type: 'category',
      category_name: 'Travel',
      category_code: 'TRAVEL',
      confirmation_chip: 'Applied: Travel',
    });
  });

  test('builds inbox request payloads bound to the selected blocker', () => {
    expect(buildInboxVoicePayload({ id: 'txn-9101' }, 'Business')).toEqual({
      transcript: 'Business',
      context_kind: 'inbox',
      context_label: 'finish_now',
      bank_txn_id: 'txn-9101',
    });
  });

  test('applies split commands to the local inbox draft state', () => {
    expect(applyInboxVoiceCommandToDraft({
      category_code: '',
      category_name: '',
      business_personal: '',
      is_split: false,
      split_business_pct: '',
    }, parseInboxVoiceCommand('Split 70%'))).toEqual({
      category_code: '',
      category_name: '',
      business_personal: 'SPLIT',
      is_split: true,
      split_business_pct: '70',
    });
  });

  test('builds a single undoable confirmation chip for inbox feedback', () => {
    expect(buildInboxVoiceChip({
      action_status: 'execute',
      confirmation_chip: 'Applied: Travel',
      undoable: true,
      bank_txn_id: 'txn-9101',
    }, {
      id: 'txn-9101',
      merchant: 'Fuel Stop',
    })).toEqual({
      tone: 'success',
      text: 'Applied: Travel',
      undoable: true,
      bank_txn_id: 'txn-9101',
      merchant: 'Fuel Stop',
    });
  });
});
