const { createHash } = require('crypto');

const csvEscape = (value) => `"${String(value ?? '').replace(/"/g, '""')}"`;

const asDateOnly = (value) => {
  if (!value) return '';
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  return String(value).slice(0, 10);
};

const asIsoDateTime = (value) => {
  if (!value) return '';
  return new Date(value).toISOString();
};

const sha256 = (value) => createHash('sha256')
  .update(Buffer.isBuffer(value) ? value : Buffer.from(String(value), 'utf8'))
  .digest('hex');

const stableStringify = (value) => {
  if (Array.isArray(value)) {
    return `[${value.map((entry) => stableStringify(entry)).join(',')}]`;
  }
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
};

const buildTransactionsCsv = (rows = []) => {
  const header = [
    'txn_id', 'date', 'merchant', 'amount', 'direction', 'category_code', 'category_name', 'confidence',
    'business_personal', 'is_split', 'split_business_pct', 'matched_evidence_ids', 'bank_account_id', 'bank_txn_ref'
  ];
  const body = rows.map((row) => ([
    row.txn_id,
    asDateOnly(row.date),
    csvEscape(row.merchant),
    row.amount,
    row.direction,
    row.category_code || '',
    csvEscape(row.category_name),
    Number(row.confidence || 0).toFixed(3),
    row.business_personal || '',
    row.is_split === true,
    row.split_business_pct ?? '',
    csvEscape(row.matched_evidence_ids || ''),
    row.bank_account_id,
    row.bank_txn_ref
  ].join(',')));
  return [header.join(',')].concat(body).join('\n');
};

const buildEvidenceCsv = (rows = []) => {
  const header = ['evidence_id', 'type', 'captured_at', 'doc_date', 'merchant', 'amount', 'storage_link', 'extraction_confidence', 'matched_bank_txn_id', 'user_confirmed'];
  const body = rows.map((row) => ([
    row.evidence_id,
    row.type,
    asIsoDateTime(row.captured_at),
    row.doc_date || '',
    csvEscape(row.merchant),
    row.amount ?? '',
    csvEscape(row.storage_link),
    Number(row.extraction_confidence || 0).toFixed(3),
    row.matched_bank_txn_id || '',
    row.user_confirmed === true
  ].join(',')));
  return [header.join(',')].concat(body).join('\n');
};

const buildSummaryCsv = (rows = []) => {
  const header = ['period_start', 'period_end', 'category_code', 'category_name', 'total_in', 'total_out', 'count', 'unresolved_count'];
  const body = rows.map((row) => ([
    asDateOnly(row.period_start),
    asDateOnly(row.period_end),
    row.category_code || '',
    csvEscape(row.category_name),
    row.total_in || 0,
    row.total_out || 0,
    row.count || 0,
    row.unresolved_count || 0
  ].join(',')));
  return [header.join(',')].concat(body).join('\n');
};

const formatMoney = (value) => Number(value || 0).toFixed(2);

const buildSimplePdf = (lines) => {
  const safe = lines.map((line) => String(line).replace(/[()\\]/g, ''));
  const text = safe.map((line, index) => `BT 40 ${760 - index * 16} Td (${line}) Tj`).join('\n');
  const stream = `BT /F1 12 Tf\n${text}\nET`;
  const objects = [];
  objects.push('1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj');
  objects.push('2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj');
  objects.push('3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj');
  objects.push(`4 0 obj << /Length ${stream.length} >> stream\n${stream}\nendstream endobj`);
  objects.push('5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj');

  let body = '%PDF-1.4\n';
  const offsets = [0];
  for (const obj of objects) {
    offsets.push(body.length);
    body += `${obj}\n`;
  }
  const xrefStart = body.length;
  body += `xref\n0 ${objects.length + 1}\n0000000000 65535 f \n`;
  for (let index = 1; index <= objects.length; index += 1) {
    body += `${String(offsets[index]).padStart(10, '0')} 00000 n \n`;
  }
  body += `trailer << /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xrefStart}\n%%EOF`;
  return Buffer.from(body, 'utf8');
};

const buildQuarterlyPackReport = ({
  periodStart,
  periodEnd,
  transactions = [],
  evidenceRows = [],
  summaryRows = [],
  readinessPct = 100
}) => {
  const totals = transactions.reduce((acc, row) => {
    const amount = Number(row.amount || 0);
    if (row.direction === 'in') {
      acc.total_in += amount;
    } else {
      acc.total_out += amount;
    }
    if (Number(row.confidence || 0) > 0) {
      acc.auto_categorised += 1;
    } else {
      acc.manual_overrides += 1;
    }
    return acc;
  }, {
    total_in: 0,
    total_out: 0,
    auto_categorised: 0,
    manual_overrides: 0
  });

  const matchedEvidence = evidenceRows.filter((row) => row.user_confirmed && row.matched_bank_txn_id).length;
  const evidenceCoveragePct = transactions.length === 0
    ? 100
    : Math.round((matchedEvidence / transactions.length) * 100);

  const categoryHighlights = summaryRows
    .slice()
    .sort((left, right) => {
      const leftMagnitude = Math.abs(Number(left.total_in || 0)) + Math.abs(Number(left.total_out || 0));
      const rightMagnitude = Math.abs(Number(right.total_in || 0)) + Math.abs(Number(right.total_out || 0));
      return rightMagnitude - leftMagnitude;
    })
    .slice(0, 4)
    .map((row) => {
      const unresolved = Number(row.unresolved_count || 0);
      return `${row.category_name || row.category_code || 'Uncategorised'}: in ${formatMoney(row.total_in)} out ${formatMoney(row.total_out)} txns ${row.count || 0} unresolved ${unresolved}`;
    });

  const lines = [
    'Quarterly Pack Summary',
    `Period: ${periodStart} to ${periodEnd}`,
    `Readiness: ${readinessPct}%`,
    `Transactions: ${transactions.length}`,
    `Total inflows: GBP ${formatMoney(totals.total_in)}`,
    `Total outflows: GBP ${formatMoney(totals.total_out)}`,
    `Auto-categorised: ${totals.auto_categorised}`,
    `Manual overrides: ${totals.manual_overrides}`,
    `Matched evidence: ${matchedEvidence}`,
    `Evidence coverage: ${evidenceCoveragePct}%`,
    `Bank-only transactions: ${Math.max(0, transactions.length - matchedEvidence)}`,
    'Category highlights:'
  ].concat(
    categoryHighlights.length > 0
      ? categoryHighlights
      : ['No category totals available.']
  );

  return {
    pdf: buildSimplePdf(lines),
    stats: {
      readiness_pct: readinessPct,
      transaction_count: transactions.length,
      total_in: Number(totals.total_in.toFixed(2)),
      total_out: Number(totals.total_out.toFixed(2)),
      auto_categorised: totals.auto_categorised,
      manual_overrides: totals.manual_overrides,
      matched_evidence: matchedEvidence,
      evidence_coverage_pct: evidenceCoveragePct,
      category_highlights: categoryHighlights
    },
    lines
  };
};

const comparableSnapshotRow = (row = {}) => ({
  txn_id: row.txn_id,
  date: asDateOnly(row.date),
  merchant: row.merchant || null,
  amount: row.amount ?? null,
  direction: row.direction || null,
  category_code: row.category_code || null,
  business_personal: row.business_personal || null,
  is_split: row.is_split === true,
  split_business_pct: row.split_business_pct ?? null
});

const buildSnapshotDiff = (previousRows = [], nextRows = []) => {
  const previous = new Map(previousRows.map((row) => [String(row.txn_id), comparableSnapshotRow(row)]));
  const next = new Map(nextRows.map((row) => [String(row.txn_id), comparableSnapshotRow(row)]));

  const added = [];
  const removed = [];
  const changed = [];
  let unchangedCount = 0;

  for (const [txnId, currentRow] of next.entries()) {
    if (!previous.has(txnId)) {
      added.push(txnId);
      continue;
    }

    const previousRow = previous.get(txnId);
    const changedFields = Object.keys(currentRow).filter((field) => stableStringify(previousRow[field]) !== stableStringify(currentRow[field]));
    if (changedFields.length > 0) {
      changed.push({ txn_id: txnId, changed_fields: changedFields.sort() });
    } else {
      unchangedCount += 1;
    }
  }

  for (const txnId of previous.keys()) {
    if (!next.has(txnId)) {
      removed.push(txnId);
    }
  }

  return {
    added: added.sort(),
    removed: removed.sort(),
    changed: changed.sort((left, right) => left.txn_id.localeCompare(right.txn_id)),
    unchanged_count: unchangedCount
  };
};

const buildQuarterlyPackArtifacts = ({
  periodStart,
  periodEnd,
  transactions = [],
  evidenceRows = [],
  summaryRows = [],
  previousSnapshotRows = [],
  nextSnapshotRows = transactions
}) => {
  const transactionsCsv = buildTransactionsCsv(transactions);
  const evidenceCsv = buildEvidenceCsv(evidenceRows);
  const summaryCsv = buildSummaryCsv(summaryRows);
  const snapshotDiff = buildSnapshotDiff(previousSnapshotRows, nextSnapshotRows);
  const manifest = {
    period_start: periodStart,
    period_end: periodEnd,
    file_checksums: {
      Transactions_csv: sha256(transactionsCsv),
      EvidenceIndex_csv: sha256(evidenceCsv),
      QuarterlySummary_csv: sha256(summaryCsv)
    },
    counts: {
      transactions: transactions.length,
      evidence: evidenceRows.length,
      summary_rows: summaryRows.length
    },
    snapshot_diff: snapshotDiff
  };
  manifest.pack_checksum = sha256(stableStringify(manifest.file_checksums) + stableStringify(manifest.counts) + stableStringify(snapshotDiff));

  return {
    transactionsCsv,
    evidenceCsv,
    summaryCsv,
    manifest,
    manifestJson: `${JSON.stringify(manifest, null, 2)}\n`
  };
};

module.exports = {
  buildEvidenceCsv,
  buildQuarterlyPackReport,
  buildQuarterlyPackArtifacts,
  buildSnapshotDiff,
  buildSimplePdf,
  buildSummaryCsv,
  buildTransactionsCsv,
  csvEscape,
  sha256,
  stableStringify
};
