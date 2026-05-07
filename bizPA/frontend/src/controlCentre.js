import { getPolicyValue } from './governance';

export const DEFAULT_SYNC_TELEMETRY = {
  lastSuccessfulSyncAt: '2026-03-11T16:24:00.000Z',
  mode: 'Local-first delta sync',
  health: 'healthy',
  backlogCount: 3,
  failedCount: 0,
  avgLatencyMs: 420,
  workerState: 'Draining backlog within policy guardrails.',
};

export const DEFAULT_ACTIVE_SESSIONS = [
  {
    sessionId: 'sess-owner-01',
    actorName: 'Alice (Owner)',
    role: 'owner',
    surface: 'Control Centre',
    state: 'Policy review',
    lastSeenAt: '2026-03-11T16:27:00.000Z',
  },
  {
    sessionId: 'sess-admin-02',
    actorName: 'Cara (Admin)',
    role: 'admin',
    surface: 'Capture',
    state: 'Inbox triage',
    lastSeenAt: '2026-03-11T16:26:00.000Z',
  },
  {
    sessionId: 'sess-staff-03',
    actorName: 'Bob (Staff)',
    role: 'staff',
    surface: 'Capture',
    state: 'Receipt draft open',
    lastSeenAt: '2026-03-11T16:25:00.000Z',
  },
];

export const buildQueueBacklogSummary = (items = []) => {
  const summary = items.reduce((accumulator, item) => {
    const severity = item?.severity || (item?.blocker_reason === 'missing_category' ? 'high' : 'medium');
    if (severity === 'high') {
      accumulator.high += 1;
    } else if (severity === 'medium') {
      accumulator.medium += 1;
    } else {
      accumulator.low += 1;
    }
    return accumulator;
  }, { total: items.length, high: 0, medium: 0, low: 0 });

  return {
    ...summary,
    headline: summary.total === 0
      ? 'Queue clear'
      : `${summary.total} blockers need governed review`,
  };
};

export const buildAutoCommitVisibility = (policyRecords = []) => {
  const enabled = !!getPolicyValue(policyRecords, 'auto_commit_enabled', false);
  const dailyCapGbp = Number(getPolicyValue(policyRecords, 'auto_commit_daily_cap_gbp', 0));
  const singleTxnCapGbp = Number(getPolicyValue(policyRecords, 'auto_commit_single_txn_cap_gbp', 0));

  if (enabled) {
    return {
      enabled: true,
      headerBadge: 'Auto-commit ON',
      headerTone: 'warning',
      bannerTone: 'warning',
      bannerTitle: 'Governed auto-commit is active',
      bannerDetail: `Eligible captures can commit without an extra confirmation prompt up to GBP ${dailyCapGbp.toFixed(0)} per day and GBP ${singleTxnCapGbp.toFixed(0)} per item.`,
      captureTitle: 'Capture is in governed auto-commit mode',
      captureDetail: 'Low-risk eligible capture can commit immediately. High-risk or over-cap actions still force manual confirmation.',
      modeBadge: 'Governed mode active',
    };
  }

  return {
    enabled: false,
    headerBadge: 'Manual mode',
    headerTone: 'safe',
    bannerTone: 'safe',
    bannerTitle: 'Manual confirmation mode is active',
    bannerDetail: 'All captures require an explicit review or confirmation step before commit.',
    captureTitle: 'Capture requires explicit confirmation',
    captureDetail: 'Nothing will auto-commit while governed mode is disabled.',
    modeBadge: 'Manual review mode',
  };
};

export const buildControlCentreSummary = ({
  policyRecords = [],
  syncTelemetry = DEFAULT_SYNC_TELEMETRY,
  sessions = DEFAULT_ACTIVE_SESSIONS,
  inboxItems = [],
  governanceAudit = [],
}) => {
  const autoCommit = buildAutoCommitVisibility(policyRecords);
  const queue = buildQueueBacklogSummary(inboxItems);

  return {
    autoCommit,
    queue,
    health: {
      syncStatus: syncTelemetry.health,
      backlogCount: Number(syncTelemetry.backlogCount || 0),
      failedCount: Number(syncTelemetry.failedCount || 0),
      activeSessions: sessions.length,
      recentAuditEvents: governanceAudit.length,
    },
  };
};
