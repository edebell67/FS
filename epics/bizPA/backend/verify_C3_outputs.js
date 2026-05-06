const assert = require('assert');
const fs = require('fs');
const path = require('path');

const {
  buildQuarterlyPackArtifacts,
  buildQuarterlyPackReport
} = require('./src/services/quarterlyExportService');

const fixturePath = path.join(__dirname, 'regression_fixtures', 'readiness_export_fixture.json');

const loadFixture = () => JSON.parse(fs.readFileSync(fixturePath, 'utf8'));

const main = () => {
  const fixture = loadFixture();
  const exportFixture = fixture.export;

  const exportArtifacts = buildQuarterlyPackArtifacts({
    periodStart: exportFixture.period_start,
    periodEnd: exportFixture.period_end,
    transactions: exportFixture.transactions,
    evidenceRows: exportFixture.evidence_rows,
    summaryRows: exportFixture.summary_rows,
    previousSnapshotRows: fixture.snapshot_diff.previous_snapshot_transactions,
    nextSnapshotRows: fixture.snapshot_diff.next_snapshot_transactions
  });

  const quarterlyPackReport = buildQuarterlyPackReport({
    periodStart: exportFixture.period_start,
    periodEnd: exportFixture.period_end,
    transactions: exportFixture.transactions,
    evidenceRows: exportFixture.evidence_rows,
    summaryRows: exportFixture.summary_rows,
    readinessPct: 100
  });

  assert.strictEqual(
    exportArtifacts.manifest.pack_checksum,
    exportFixture.expected_export_checksum,
    'Quarterly export checksum drift detected.'
  );

  const summaryLines = exportArtifacts.summaryCsv.trim().split('\n');
  assert.strictEqual(summaryLines[0], 'period_start,period_end,category_code,category_name,total_in,total_out,count,unresolved_count');
  assert(summaryLines.includes('2026-01-01,2026-03-31,materials,"Materials",0,140.5,1,0'));
  assert(summaryLines.includes('2026-01-01,2026-03-31,sales,"Sales",520,0,1,0'));

  const pdfText = quarterlyPackReport.pdf.toString('utf8');
  assert(pdfText.startsWith('%PDF-1.4'), 'QuarterlyPack.pdf is missing a PDF header.');
  assert(pdfText.includes('Quarterly Pack Summary'), 'QuarterlyPack.pdf is missing the title.');
  assert(pdfText.includes('Period: 2026-01-01 to 2026-03-31'), 'QuarterlyPack.pdf is missing the period line.');
  assert(pdfText.includes('Total inflows: GBP 520.00'), 'QuarterlyPack.pdf is missing total inflows.');
  assert(pdfText.includes('Total outflows: GBP 140.50'), 'QuarterlyPack.pdf is missing total outflows.');
  assert(pdfText.includes('Matched evidence: 1'), 'QuarterlyPack.pdf is missing matched evidence count.');
  assert(pdfText.includes('Evidence coverage: 50%'), 'QuarterlyPack.pdf is missing evidence coverage.');
  assert(quarterlyPackReport.pdf.length > 500, 'QuarterlyPack.pdf is unexpectedly small.');

  console.log('verify_C3_outputs=PASS');
  console.log(JSON.stringify({
    summary_rows: exportFixture.summary_rows.length,
    export_checksum: exportArtifacts.manifest.pack_checksum,
    pdf_bytes: quarterlyPackReport.pdf.length,
    category_highlights: quarterlyPackReport.stats.category_highlights
  }));
};

try {
  main();
} catch (error) {
  console.error('verify_C3_outputs=FAIL');
  console.error(error.message);
  process.exit(1);
}
