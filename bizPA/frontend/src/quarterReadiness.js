const SEVERITY_ORDER = {
  high: 0,
  medium: 1,
  low: 2,
};

const normalizeNumber = (value, fallback = 0) => {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
};

const sortIssues = (issues = []) => [...issues].sort((left, right) => {
  const severityDelta = (SEVERITY_ORDER[left.severity] ?? 99) - (SEVERITY_ORDER[right.severity] ?? 99);
  if (severityDelta !== 0) {
    return severityDelta;
  }

  const leftDate = String(left.txn_date || '');
  const rightDate = String(right.txn_date || '');
  if (leftDate !== rightDate) {
    return leftDate.localeCompare(rightDate);
  }

  return String(left.affected_entity_id || '').localeCompare(String(right.affected_entity_id || ''));
});

const buildIssueSummary = (issues = []) => {
  const groups = new Map();

  issues.forEach((issue) => {
    const key = issue.issue_type || issue.resolution_target?.label || 'unknown_issue';
    const existing = groups.get(key);
    if (existing) {
      existing.count += 1;
      existing.total_weight += normalizeNumber(issue.weight, 0);
      return;
    }

    groups.set(key, {
      issue_type: key,
      label: issue.summary_label || issue.label || issue.resolution_target?.label || key.replace(/_/g, ' '),
      severity: issue.severity || 'low',
      count: 1,
      weight: normalizeNumber(issue.weight, 0),
      total_weight: normalizeNumber(issue.weight, 0),
      explanation: issue.explanation || '',
    });
  });

  return [...groups.values()].sort((left, right) => {
    const severityDelta = (SEVERITY_ORDER[left.severity] ?? 99) - (SEVERITY_ORDER[right.severity] ?? 99);
    if (severityDelta !== 0) {
      return severityDelta;
    }
    return right.count - left.count;
  });
};

const buildBlockersByReason = (issueSummary = []) => issueSummary.map((entry) => ({
  reason: entry.issue_type,
  label: entry.label,
  count: entry.count,
}));

const buildExplanationLines = ({ readinessPct, report = {}, activeIssues = [], issueSummary = [] }) => {
  const totalTransactions = normalizeNumber(report.total_txns_in_period, 0);
  const blockerCount = activeIssues.length;
  const quarterStart = report.period_start || 'current quarter start';
  const quarterEnd = report.period_end || 'current quarter end';
  const reasonSummary = issueSummary.length
    ? issueSummary.map((entry) => `${entry.label} (${entry.count})`).join('; ')
    : 'No blocking reasons remain.';

  return [
    `Readiness is ${readinessPct}% for ${quarterStart} to ${quarterEnd}.`,
    blockerCount > 0
      ? `${blockerCount} of ${totalTransactions} transactions are still blocking export.`
      : 'No blocking transactions remain. Export is ready now.',
    `Blocking reasons: ${reasonSummary}`,
  ];
};

export const deriveResolvedIssueIdsFromSearchParams = (searchParams, fallbackIssues = []) => {
  const resolvedValue = searchParams?.get('resolvedDemoIssues');
  if (!resolvedValue) {
    return [];
  }

  if (resolvedValue === 'all') {
    return fallbackIssues
      .map((issue) => issue?.affected_entity_id)
      .filter(Boolean);
  }

  return resolvedValue
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);
};

export const buildQuarterUiState = ({ report = null, fallbackIssues = [], resolvedIssueIds = [] }) => {
  if (!report) {
    return {
      report: null,
      activeIssues: [],
      headline: '0% ready - 0 items left',
      itemsLeft: 0,
      exportEnabled: false,
    };
  }

  const issueSource = Array.isArray(report.issue_list) && report.issue_list.length > 0
    ? report.issue_list
    : fallbackIssues;
  const allIssues = sortIssues(Array.isArray(issueSource) ? issueSource : []);
  const resolvedSet = new Set(resolvedIssueIds);
  const activeIssues = allIssues.filter((issue) => !resolvedSet.has(issue.affected_entity_id));
  const originalPenalty = allIssues.reduce((sum, issue) => sum + normalizeNumber(issue.weight, 0), 0);
  const activePenalty = activeIssues.reduce((sum, issue) => sum + normalizeNumber(issue.weight, 0), 0);
  const baseReadiness = normalizeNumber(report.readiness_pct, 0);
  const readinessLoss = Math.max(0, 100 - baseReadiness);
  const readinessPct = activeIssues.length === 0
    ? 100
    : originalPenalty > 0
      ? Math.max(0, Math.min(100, Math.round(100 - ((activePenalty / originalPenalty) * readinessLoss))))
      : baseReadiness;
  const issueSummary = buildIssueSummary(activeIssues);
  const blockersByReason = buildBlockersByReason(issueSummary);
  const itemsLeft = activeIssues.length;
  const exportEnabled = itemsLeft === 0;
  const headline = `${readinessPct}% ready - ${itemsLeft} item${itemsLeft === 1 ? '' : 's'} left`;

  return {
    report: {
      ...report,
      readiness_pct: readinessPct,
      blocking_txns_count: itemsLeft,
      can_export: exportEnabled,
      issue_list: activeIssues,
      issue_count: itemsLeft,
      issue_summary: issueSummary,
      blockers_by_reason: blockersByReason,
      explanation_lines: buildExplanationLines({
        readinessPct,
        report,
        activeIssues,
        issueSummary,
      }),
    },
    activeIssues,
    headline,
    itemsLeft,
    exportEnabled,
  };
};
