const nodeAssert = require('assert');

const {
  canonicalSchemas,
  monetaryEntityTypes,
  nonMonetaryEntityTypes,
  validateEntityPayload,
  validateEventPayload,
  deriveQuarterReference
} = require('./src/services/canonicalSchemaService');
const {
  classifyVatType,
  validateAndClassifyMonetaryPayload
} = require('./src/services/vatQuarterClassificationService');

const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

const requiredMonetaryTypes = [
  'invoice',
  'receipt_expense',
  'payment',
  'quote',
  'monetary_booking'
];

const requiredNonMonetaryTypes = [
  'note',
  'attachment',
  'booking',
  'client',
  'supplier',
  'reminder',
  'snapshot'
];

requiredMonetaryTypes.forEach((entityType) => {
  assert(monetaryEntityTypes.includes(entityType), `Missing monetary entity type: ${entityType}`);
});

requiredNonMonetaryTypes.forEach((entityType) => {
  assert(nonMonetaryEntityTypes.includes(entityType), `Missing non-monetary entity type: ${entityType}`);
});

const validInvoice = {
  unique_id: '11111111-1111-1111-1111-111111111111',
  entity_type: 'invoice',
  transaction_date: '2026-03-11',
  created_at: '2026-03-11T16:30:00Z',
  created_by: 'user:test',
  quarter_reference: deriveQuarterReference('2026-03-11'),
  counterparty_reference: 'client:abc',
  description: 'Invoice for guttering work',
  category: 'income_services',
  net_amount: 500.0,
  vat_amount: 100.0,
  gross_amount: 600.0,
  vat_rate: 20.0,
  vat_type: 'output',
  status: 'committed',
  commit_mode: 'manual',
  source_type: 'voice'
};

const invalidMissingAmount = {
  ...validInvoice
};
delete invalidMissingAmount.net_amount;

const invalidStatus = {
  ...validInvoice,
  status: 'deleted'
};

const validNote = {
  unique_id: '22222222-2222-2222-2222-222222222222',
  entity_type: 'note',
  created_at: '2026-03-11T16:31:00Z',
  created_by: 'user:test',
  description: 'Call supplier tomorrow',
  status: 'committed',
  commit_mode: 'auto',
  source_type: 'manual'
};

const validEvent = {
  unique_id: '33333333-3333-3333-3333-333333333333',
  event_type: 'snapshot_created',
  created_at: '2026-03-11T16:32:00Z',
  created_by: 'user:test',
  source_type: 'system',
  description: 'Snapshot 001 created for Q1-2026',
  linked_entity_id: '44444444-4444-4444-4444-444444444444',
  linked_entity_type: 'snapshot',
  quarter_reference: 'Q1-2026'
};

const validInvoiceResult = validateEntityPayload('invoice', validInvoice);
assert(validInvoiceResult.valid, `Valid invoice payload failed: ${validInvoiceResult.errors.join('; ')}`);

const validReceiptExpense = {
  ...validInvoice,
  entity_type: 'receipt_expense',
  transaction_date: '2026-04-01',
  quarter_reference: deriveQuarterReference('2026-04-01'),
  net_amount: 50.0,
  vat_amount: 10.0,
  gross_amount: 60.0,
  vat_type: 'input',
  status: 'committed'
};
const validReceiptExpenseResult = validateEntityPayload('receipt_expense', validReceiptExpense);
assert(validReceiptExpenseResult.valid, `Valid receipt_expense payload failed: ${validReceiptExpenseResult.errors.join('; ')}`);

const invalidMissingAmountResult = validateEntityPayload('invoice', invalidMissingAmount);
assert(!invalidMissingAmountResult.valid, 'Missing required monetary fields should fail validation');
assert(invalidMissingAmountResult.errors.some((error) => error.includes('net_amount')), 'Missing net_amount should be reported');

const invalidStatusResult = validateEntityPayload('invoice', invalidStatus);
assert(!invalidStatusResult.valid, 'Unsupported invoice state should fail validation');
assert(invalidStatusResult.errors.some((error) => error.includes('Unsupported status')), 'Unsupported status should be reported');

const invalidQuarterInvoiceResult = validateEntityPayload('invoice', {
  ...validInvoice,
  transaction_date: '2026-03-31',
  quarter_reference: 'Q2-2026'
});
assert(!invalidQuarterInvoiceResult.valid, 'Mismatched quarter_reference should fail validation');
assert(
  invalidQuarterInvoiceResult.errors.some((error) => error.includes('does not match transaction_date-derived value')),
  'Quarter mismatch should be reported'
);

const invalidVatInvoiceResult = validateEntityPayload('invoice', {
  ...validInvoice,
  net_amount: 100,
  vat_amount: 10,
  gross_amount: 110,
  vat_rate: 20
});
assert(!invalidVatInvoiceResult.valid, 'Invalid VAT combinations should fail validation');
assert(
  invalidVatInvoiceResult.errors.some((error) => error.includes('Invalid VAT combination')),
  'Invalid VAT combination should be reported'
);

const validNoteResult = validateEntityPayload('note', validNote);
assert(validNoteResult.valid, `Valid note payload failed: ${validNoteResult.errors.join('; ')}`);

const validEventResult = validateEventPayload(validEvent);
assert(validEventResult.valid, `Valid event payload failed: ${validEventResult.errors.join('; ')}`);

nodeAssert.strictEqual(classifyVatType({ entityType: 'invoice' }), 'output', 'Invoice should classify as output VAT');
nodeAssert.strictEqual(classifyVatType({ entityType: 'receipt_expense' }), 'input', 'Receipt expense should classify as input VAT');
nodeAssert.strictEqual(classifyVatType({ entityType: 'invoice', vatType: 'Output' }), 'output', 'Legacy vat_type casing should normalize');

const quarterBoundary = validateAndClassifyMonetaryPayload({
  entityType: 'invoice',
  transactionDate: '2026-06-30',
  amount: 120,
  vat_rate: 20
});
nodeAssert.strictEqual(quarterBoundary.quarter_reference, 'Q2-2026', 'Quarter should derive from transaction date boundary');
nodeAssert.strictEqual(quarterBoundary.net_amount, 100, 'Gross-only payload should derive net amount');
nodeAssert.strictEqual(quarterBoundary.vat_amount, 20, 'Gross-only payload should derive VAT amount');

Object.entries(canonicalSchemas.field_dictionary).forEach(([fieldName, entry]) => {
  assert(entry.export_column, `Field dictionary entry missing export_column: ${fieldName}`);
  assert(entry.snapshot_field, `Field dictionary entry missing snapshot_field: ${fieldName}`);
});

const snapshotDefinition = canonicalSchemas.entity_types.snapshot;
[
  'version_number',
  'included_transaction_ids',
  'totals',
  'vat_totals',
  'readiness_score',
  'integrity_warning_summary',
  'generated_files'
].forEach((field) => {
  assert(snapshotDefinition.required_fields.includes(field), `Snapshot required field missing: ${field}`);
});

console.log('canonical_schema_ok');
console.log(`monetary_types=${requiredMonetaryTypes.join(',')}`);
console.log(`non_monetary_types=${requiredNonMonetaryTypes.join(',')}`);
console.log(`event_types=${canonicalSchemas.event_schema.allowed_event_types.length}`);
console.log('vat_classification_ok');
console.log('quarter_boundary_ok');
