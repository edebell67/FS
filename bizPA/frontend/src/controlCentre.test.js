import {
  buildAutoCommitVisibility,
  buildControlCentreSummary,
  buildQueueBacklogSummary,
} from './controlCentre';
import { buildDefaultPolicyRecords } from './governance';

describe('control centre helpers', () => {
  test('buildQueueBacklogSummary counts severity buckets', () => {
    const summary = buildQueueBacklogSummary([
      { blocker_reason: 'missing_category', severity: 'high' },
      { blocker_reason: 'unresolved_duplicate', severity: 'medium' },
      { blocker_reason: 'missing_business_personal', severity: 'high' },
    ]);

    expect(summary.total).toBe(3);
    expect(summary.high).toBe(2);
    expect(summary.medium).toBe(1);
    expect(summary.low).toBe(0);
    expect(summary.headline).toContain('3 blockers');
  });

  test('buildAutoCommitVisibility returns governed mode copy when enabled', () => {
    const policyRecords = buildDefaultPolicyRecords({
      tenantId: 'tenant-bizpa-demo',
      actor: { id: '1', name: 'Alice', role: 'owner' },
      now: '2026-03-11T16:30:00.000Z',
    });

    const visibility = buildAutoCommitVisibility(policyRecords);

    expect(visibility.enabled).toBe(true);
    expect(visibility.headerBadge).toBe('Auto-commit ON');
    expect(visibility.bannerDetail).toContain('GBP 500');
    expect(visibility.bannerDetail).toContain('GBP 150');
  });

  test('buildControlCentreSummary aggregates queue and session health', () => {
    const policyRecords = buildDefaultPolicyRecords({
      tenantId: 'tenant-bizpa-demo',
      actor: { id: '1', name: 'Alice', role: 'owner' },
      now: '2026-03-11T16:30:00.000Z',
    });

    const summary = buildControlCentreSummary({
      policyRecords,
      syncTelemetry: {
        health: 'warning',
        backlogCount: 5,
        failedCount: 1,
      },
      sessions: [{ sessionId: '1' }, { sessionId: '2' }],
      inboxItems: [{ severity: 'high' }, { severity: 'low' }],
      governanceAudit: [{ id: 'a1' }, { id: 'a2' }, { id: 'a3' }],
    });

    expect(summary.autoCommit.enabled).toBe(true);
    expect(summary.queue.total).toBe(2);
    expect(summary.health.syncStatus).toBe('warning');
    expect(summary.health.activeSessions).toBe(2);
    expect(summary.health.recentAuditEvents).toBe(3);
  });
});
