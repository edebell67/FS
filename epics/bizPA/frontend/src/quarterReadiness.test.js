import {
  buildQuarterUiState,
  deriveResolvedIssueIdsFromSearchParams,
} from './quarterReadiness';

const reportFixture = {
  quarter_reference: 'Q1-2026',
  period_start: '2026-01-01',
  period_end: '2026-03-31',
  total_txns_in_period: 18,
  readiness_pct: 78,
  can_export: false,
  issue_list: [
    {
      issue_type: 'missing_category',
      affected_entity_id: 'txn-9101',
      severity: 'high',
      weight: 35,
      explanation: 'Category missing for Fuel Stop.',
      txn_date: '2026-02-04',
      merchant: 'Fuel Stop',
      amount: 64.18,
      direction: 'out',
      resolution_target: {
        label: 'Classify transaction',
        workflow: '/inbox/finish-now',
      },
    },
    {
      issue_type: 'missing_business_personal',
      affected_entity_id: 'txn-9103',
      severity: 'high',
      weight: 30,
      explanation: 'Business/personal decision missing.',
      txn_date: '2026-02-15',
      merchant: 'Mobile Contract',
      amount: 42.5,
      direction: 'out',
      resolution_target: {
        label: 'Set business or personal',
        workflow: '/inbox/finish-now',
      },
    },
    {
      issue_type: 'unresolved_duplicate',
      affected_entity_id: 'txn-9104',
      severity: 'medium',
      weight: 15,
      explanation: 'Duplicate not resolved.',
      txn_date: '2026-03-02',
      merchant: 'Client Payment',
      amount: 820,
      direction: 'in',
      resolution_target: {
        label: 'Resolve duplicate',
        workflow: '/inbox/finish-now',
      },
    },
  ],
};

describe('quarter readiness helpers', () => {
  test('keeps blockers ordered and updates headline while blockers remain', () => {
    const state = buildQuarterUiState({ report: reportFixture, resolvedIssueIds: ['txn-9104'] });

    expect(state.itemsLeft).toBe(2);
    expect(state.exportEnabled).toBe(false);
    expect(state.report.readiness_pct).toBeGreaterThan(78);
    expect(state.headline).toContain('items left');
    expect(state.activeIssues.map((issue) => issue.affected_entity_id)).toEqual(['txn-9101', 'txn-9103']);
    expect(state.report.explanation_lines[0]).toContain('Readiness is');
  });

  test('unlocks export immediately when every blocker is resolved', () => {
    const state = buildQuarterUiState({
      report: reportFixture,
      resolvedIssueIds: ['txn-9101', 'txn-9103', 'txn-9104'],
    });

    expect(state.itemsLeft).toBe(0);
    expect(state.exportEnabled).toBe(true);
    expect(state.report.readiness_pct).toBe(100);
    expect(state.report.can_export).toBe(true);
    expect(state.report.issue_summary).toEqual([]);
  });

  test('supports demo query params that resolve all blockers', () => {
    const params = new URLSearchParams('resolvedDemoIssues=all');
    const resolvedIds = deriveResolvedIssueIdsFromSearchParams(params, reportFixture.issue_list);

    expect(resolvedIds).toEqual(['txn-9101', 'txn-9103', 'txn-9104']);
  });
});
