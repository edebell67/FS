const assert = require('assert');

const {
  buildCaptureParseResult
} = require('./src/services/voiceCaptureParserService');

function expectCompositionContract(parseResult) {
  assert(parseResult.composition_payload, 'Expected composition payload to exist');
  assert.strictEqual(parseResult.composition_payload.type, parseResult.entity_type);
  assert.strictEqual(parseResult.composition_payload.voice_command_source_text, parseResult.utterance);
  assert.strictEqual(parseResult.composition_payload.voice_action_confidence, parseResult.confidence_score);
}

function main() {
  const referenceDate = '2026-03-11T12:00:00.000Z';
  const samples = [
    {
      name: 'invoice',
      utterance: 'Raise an invoice for Sarah for £500 due Friday',
      expectedIntent: 'capture_invoice',
      expectedType: 'invoice',
      expectedCounterparty: 'sarah',
      expectedAmount: 500
    },
    {
      name: 'receipt',
      utterance: 'Record a receipt for £42 petrol today',
      expectedIntent: 'capture_receipt',
      expectedType: 'receipt',
      expectedAmount: 42
    },
    {
      name: 'quote',
      utterance: 'Create a quote for Acme Builders for 900 pounds next Monday',
      expectedIntent: 'capture_quote',
      expectedType: 'quote',
      expectedCounterparty: 'acme builders',
      expectedAmount: 900
    },
    {
      name: 'payment',
      utterance: 'Record payment 240 pounds from John by bank transfer',
      expectedIntent: 'capture_payment',
      expectedType: 'payment',
      expectedCounterparty: 'john',
      expectedAmount: 240
    },
    {
      name: 'booking',
      utterance: 'Book a meeting with Acme Plumbing tomorrow',
      expectedIntent: 'capture_booking',
      expectedType: 'booking',
      expectedCounterparty: 'acme plumbing'
    },
    {
      name: 'reminder',
      utterance: 'Remind me tomorrow to call Acme Plumbing',
      expectedIntent: 'create_reminder',
      expectedType: 'reminder',
      expectedCounterparty: 'acme plumbing'
    },
    {
      name: 'note',
      utterance: 'Note customer wants the bathroom tiles in matte black',
      expectedIntent: 'create_note',
      expectedType: 'note'
    }
  ];

  for (const sample of samples) {
    const result = buildCaptureParseResult(sample.utterance, referenceDate);
    assert.strictEqual(result.detected_intent, sample.expectedIntent, `${sample.name} intent mismatch`);
    assert.strictEqual(result.entity_type, sample.expectedType, `${sample.name} entity mismatch`);
    if (sample.expectedCounterparty) {
      assert.strictEqual(result.counterparty_name, sample.expectedCounterparty, `${sample.name} counterparty mismatch`);
    }
    if (sample.expectedAmount !== undefined) {
      assert.strictEqual(result.amount, sample.expectedAmount, `${sample.name} amount mismatch`);
    }
    expectCompositionContract(result);
  }

  const lowConfidence = buildCaptureParseResult('Invoice for Sarah', referenceDate);
  assert.strictEqual(lowConfidence.detected_intent, 'capture_invoice');
  assert.strictEqual(lowConfidence.requires_review, true);
  assert(lowConfidence.missing_fields.includes('amount'), 'Low confidence parse should flag missing amount');
  assert.strictEqual(lowConfidence.review_reason, 'missing_fields:amount');

  const lowConfidenceNote = buildCaptureParseResult('Remember this', referenceDate);
  assert.strictEqual(lowConfidenceNote.detected_intent, 'create_note');
  assert.strictEqual(lowConfidenceNote.requires_review, true);

  const thisWeekQuery = buildCaptureParseResult('Show invoices for Acme this week', referenceDate);
  assert.strictEqual(thisWeekQuery.detected_intent, 'view_invoices');
  assert.strictEqual(thisWeekQuery.counterparty_name, 'acme');
  assert(thisWeekQuery.time_period, 'Expected this week query to include time period');
  assert.strictEqual(thisWeekQuery.time_period.key, 'this_week');
  assert.strictEqual(thisWeekQuery.time_period.start_iso, '2026-03-09');
  assert.strictEqual(thisWeekQuery.time_period.end_iso, '2026-03-15');

  const lastWeekQuery = buildCaptureParseResult('Show expenses for Brookside last week', referenceDate);
  assert.strictEqual(lastWeekQuery.detected_intent, 'view_expenses');
  assert.strictEqual(lastWeekQuery.counterparty_name, 'brookside');
  assert(lastWeekQuery.time_period, 'Expected last week query to include time period');
  assert.strictEqual(lastWeekQuery.time_period.key, 'last_week');
  assert.strictEqual(lastWeekQuery.time_period.start_iso, '2026-03-02');
  assert.strictEqual(lastWeekQuery.time_period.end_iso, '2026-03-08');

  const exactDateQuery = buildCaptureParseResult('Show invoices for Acme on 2026-03-11', referenceDate);
  assert.strictEqual(exactDateQuery.detected_intent, 'view_invoices');
  assert.strictEqual(exactDateQuery.counterparty_name, 'acme');
  assert(exactDateQuery.date_hint, 'Expected exact-date query to include date hint');
  assert.strictEqual(exactDateQuery.date_hint.iso, '2026-03-11');

  console.log('voice_capture_parser_ok');
  console.log('entity_mapping_ok=true');
  console.log('low_confidence_review_ok=true');
  console.log('composition_contract_ok=true');
  console.log('query_period_filters_ok=true');
  console.log('query_exact_date_filters_ok=true');
}

main();
