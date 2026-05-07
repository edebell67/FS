import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import {
  ArchiveRestore,
  ArrowRight,
  Bell,
  Briefcase,
  Calendar,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Clock,
  Download,
  Flame,
  FileText,
  History,
  LayoutGrid,
  Lock,
  LockOpen,
  Mic,
  Moon,
  Plus,
  RefreshCcw,
  Receipt,
  ShieldAlert,
  StickyNote,
  Sun,
  TriangleAlert,
  Wallet,
} from 'lucide-react';
import { SpeechRecognition } from '@capacitor-community/speech-recognition';
import { Preferences } from '@capacitor/preferences';
import {
  PERMISSIONS,
  ROLE_LABELS,
  applyPolicyUpdate,
  buildDefaultPolicyRecords,
  getPermissionsForRole,
  getPolicyValue,
  hasPermission,
  runGovernedAction,
} from './governance';
import {
  buildAutoCommitVisibility,
  buildControlCentreSummary,
  DEFAULT_ACTIVE_SESSIONS,
  DEFAULT_SYNC_TELEMETRY,
} from './controlCentre';
import {
  buildQuarterUiState,
  deriveResolvedIssueIdsFromSearchParams,
} from './quarterReadiness';
import {
  buildVoiceMicroDecisionRequest,
  findVoiceContextCard,
  reduceVoiceMicroDecisionChip,
} from './voiceMicroDecisions';
import {
  applyInboxVoiceCommandToDraft,
  buildInboxVoiceChip,
  parseInboxVoiceCommand,
} from './voiceMicroDecision';
import OnboardingGate from './OnboardingGate';
import {
  createAppUserFromSession,
  mergeUserIntoList,
  normalizeOnboardingSession,
} from './onboarding';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5056/api/v1';
const MVP_QUARTERLY_EXPORT_MODE = process.env.REACT_APP_MVP_QUARTERLY_EXPORT_MODE !== 'false';
const LEGAL_DISCLAIMER = 'No HMRC submission. Not tax advice. You remain responsible for filings.';
axios.defaults.withCredentials = true;
const MONETARY_TYPES = ['invoice', 'receipt', 'payment', 'quote'];
const TENANT_ID = 'tenant-bizpa-demo';
const INBOX_FILTERS = [
  { key: 'all', label: 'All blockers' },
  { key: 'missing_category', label: 'Category' },
  { key: 'missing_business_personal', label: 'Business / personal' },
  { key: 'missing_split_pct', label: 'Split' },
  { key: 'unresolved_duplicate', label: 'Duplicate' },
];
const INBOX_REASON_LABELS = {
  missing_category: 'Category missing',
  missing_business_personal: 'Business or personal pending',
  missing_split_pct: 'Split percentage missing',
  unresolved_duplicate: 'Duplicate unresolved',
};
const INBOX_MERCHANT_SUGGESTIONS = [
  { pattern: /fuel|shell|esso|bp/i, category_code: 'MOTOR', category_name: 'Motor expenses' },
  { pattern: /builder|depot|screwfix|toolstation/i, category_code: 'MATERIALS', category_name: 'Materials' },
  { pattern: /mobile|vodafone|o2|ee/i, category_code: 'TELECOMS', category_name: 'Mobile and telecoms' },
  { pattern: /uber|trainline|tfl/i, category_code: 'TRAVEL', category_name: 'Travel' },
  { pattern: /client payment|stripe|gocardless/i, category_code: 'INCOME', category_name: 'Sales income' },
];

const USERS = [
  {
    id: '11111111-1111-1111-1111-111111111111',
    name: 'Alice (Owner)',
    email: 'alice@bizpa.local',
    role: 'owner',
    tenant_id: TENANT_ID,
  },
  {
    id: '22222222-2222-2222-2222-222222222222',
    name: 'Cara (Admin)',
    email: 'cara@bizpa.local',
    role: 'admin',
    tenant_id: TENANT_ID,
  },
  {
    id: '33333333-3333-3333-3333-333333333333',
    name: 'Bob (Staff)',
    email: 'bob@bizpa.local',
    role: 'staff',
    tenant_id: TENANT_ID,
  },
  {
    id: '44444444-4444-4444-4444-444444444444',
    name: 'Dana (Accountant)',
    email: 'dana@bizpa.local',
    role: 'accountant_readonly',
    tenant_id: TENANT_ID,
  },
];

const DEFAULT_MANUAL_FORM = {
  type: 'invoice',
  counterparty: '',
  grossAmount: '',
  netAmount: '',
  vatAmount: '',
  vatRate: '20',
  category: '',
  relevantDate: '',
  note: '',
};

const READINESS_DEMO_REPORT = {
  as_of_date: '2026-03-11',
  quarter_reference: 'Q1-2026',
  period_start: '2026-01-01',
  period_end: '2026-03-31',
  active_period_enforced: true,
  requested_period_start: '2025-10-01',
  requested_period_end: '2025-12-31',
  total_txns_in_period: 18,
  blocking_txns_count: 4,
  readiness_pct: 78,
  can_export: false,
  blockers_by_reason: [
    { reason: 'missing_category', label: 'Category missing', count: 2 },
    { reason: 'missing_business_personal', label: 'Business or personal flag missing', count: 1 },
    { reason: 'unresolved_duplicate', label: 'Duplicate unresolved', count: 1 },
  ],
  issue_summary: [
    {
      issue_type: 'missing_category',
      label: 'Category missing',
      severity: 'high',
      weight: 35,
      count: 2,
      percentage_of_issues: 50,
      percentage_of_period_transactions: 11,
      total_weight: 70,
      explanation: 'This transaction has no tax category yet, so it cannot be included safely in the quarter calculation.',
    },
    {
      issue_type: 'missing_business_personal',
      label: 'Business or personal flag missing',
      severity: 'high',
      weight: 30,
      count: 1,
      percentage_of_issues: 25,
      percentage_of_period_transactions: 6,
      total_weight: 30,
      explanation: 'This transaction still needs a business or personal decision before readiness can be finalized.',
    },
    {
      issue_type: 'unresolved_duplicate',
      label: 'Duplicate unresolved',
      severity: 'medium',
      weight: 15,
      count: 1,
      percentage_of_issues: 25,
      percentage_of_period_transactions: 6,
      total_weight: 15,
      explanation: 'This transaction is flagged as a duplicate but has not been dismissed or merged yet.',
    },
  ],
  issue_list: [
    {
      issue_type: 'missing_category',
      affected_entity_id: 'txn-9101',
      affected_entity_type: 'bank_transaction',
      severity: 'high',
      weight: 35,
      explanation: 'This transaction has no tax category yet, so it cannot be included safely in the quarter calculation. Merchant: Fuel Stop.',
      txn_date: '2026-02-04',
      merchant: 'Fuel Stop',
      amount: 64.18,
      direction: 'out',
      resolution_target: {
        kind: 'transaction_classification',
        route: '/api/v1/inbox/txn-9101/classification',
        method: 'PATCH',
        label: 'Classify transaction',
        entity_id: 'txn-9101',
        workflow: '/inbox/finish-now',
      },
    },
    {
      issue_type: 'missing_category',
      affected_entity_id: 'txn-9102',
      affected_entity_type: 'bank_transaction',
      severity: 'high',
      weight: 35,
      explanation: 'This transaction has no tax category yet, so it cannot be included safely in the quarter calculation. Merchant: Builder Depot.',
      txn_date: '2026-02-11',
      merchant: 'Builder Depot',
      amount: 148.0,
      direction: 'out',
      resolution_target: {
        kind: 'transaction_classification',
        route: '/api/v1/inbox/txn-9102/classification',
        method: 'PATCH',
        label: 'Classify transaction',
        entity_id: 'txn-9102',
        workflow: '/inbox/finish-now',
      },
    },
    {
      issue_type: 'missing_business_personal',
      affected_entity_id: 'txn-9103',
      affected_entity_type: 'bank_transaction',
      severity: 'high',
      weight: 30,
      explanation: 'This transaction still needs a business or personal decision before readiness can be finalized. Merchant: Mobile Contract.',
      txn_date: '2026-02-15',
      merchant: 'Mobile Contract',
      amount: 42.5,
      direction: 'out',
      resolution_target: {
        kind: 'transaction_classification',
        route: '/api/v1/inbox/txn-9103/classification',
        method: 'PATCH',
        label: 'Set business or personal',
        entity_id: 'txn-9103',
        workflow: '/inbox/finish-now',
      },
    },
    {
      issue_type: 'unresolved_duplicate',
      affected_entity_id: 'txn-9104',
      affected_entity_type: 'bank_transaction',
      severity: 'medium',
      weight: 15,
      explanation: 'This transaction is flagged as a duplicate but has not been dismissed or merged yet. Merchant: Client Payment.',
      txn_date: '2026-03-02',
      merchant: 'Client Payment',
      amount: 820.0,
      direction: 'in',
      resolution_target: {
        kind: 'duplicate_resolution',
        route: '/api/v1/inbox/txn-9104/duplicate-resolution',
        method: 'POST',
        label: 'Resolve duplicate',
        entity_id: 'txn-9104',
        workflow: '/inbox/finish-now',
      },
    },
  ],
  explanation_lines: [
    'Readiness is 78% for 2026-01-01 to 2026-03-31.',
    '4 of 18 transactions are still blocking export.',
    'Blocking reasons: Category missing (2); Business or personal flag missing (1); Duplicate unresolved (1).',
  ],
};

const READINESS_HISTORY_DEMO = [
  {
    quarter_reference: 'Q4-2025',
    readiness_pct: 100,
    status: 'Closed snapshot',
    detail: 'Historical snapshot archived after quarter close. Reference only; not editable from this screen.',
  },
  {
    quarter_reference: 'Q3-2025',
    readiness_pct: 96,
    status: 'Archived snapshot',
    detail: 'Older quarter retained for comparison and audit trail. Excluded from the active-quarter score.',
  },
];

const SNAPSHOT_DEMO_HISTORY = [
  {
    snapshot_id: 'snap-q1-2026-v002',
    event_id: 'evt-snap-q1-2026-v002',
    quarter_reference: 'Q1-2026',
    version_number: 2,
    created_at: '2026-03-09T10:24:00.000Z',
    description: 'Snapshot 002 generated before quarter sign-off',
    readiness_pct: 100,
    status: 'Current baseline',
    integrity_warnings: [
      {
        level: 'warning',
        title: 'Manual reopen required for late documents',
        detail: 'Quarter is currently open, but the previous close created an audit obligation for any further edits.'
      }
    ],
    snapshot_summary: {
      transaction_count: 18,
      totals: {
        net_amount: 18240,
        vat_amount: 3648,
        gross_amount: 21888
      },
      vat_totals: {
        total_vat: 3648,
        by_rate: { '20': 3648 },
        by_type: { output: 4012, input: -364 }
      }
    },
    diff_summary: {
      added_transactions: [],
      voided_transactions: [],
      adjustments: [],
      revenue_impact: 0,
      vat_impact: 0,
      changed_since_snapshot: false
    }
  },
  {
    snapshot_id: 'snap-q1-2026-v001',
    event_id: 'evt-snap-q1-2026-v001',
    quarter_reference: 'Q1-2026',
    version_number: 1,
    created_at: '2026-03-01T08:10:00.000Z',
    description: 'Snapshot 001 generated after first review pass',
    readiness_pct: 96,
    status: 'Archived',
    integrity_warnings: [
      {
        level: 'warning',
        title: 'One unresolved duplicate at snapshot time',
        detail: 'Snapshot 001 was preserved with a duplicate-warning note for comparison during audit.'
      }
    ],
    snapshot_summary: {
      transaction_count: 17,
      totals: {
        net_amount: 16980,
        vat_amount: 3396,
        gross_amount: 20376
      },
      vat_totals: {
        total_vat: 3396,
        by_rate: { '20': 3396 },
        by_type: { output: 3732, input: -336 }
      }
    },
    diff_summary: {
      added_transactions: [
        {
          txn_id: 'inv-204',
          entity_type: 'invoice',
          merchant: 'Brookside Renovations',
          date: '2026-03-08',
          gross_amount: 1512,
          revenue_impact: 1512,
          vat_impact: 252
        }
      ],
      voided_transactions: [
        {
          txn_id: 'rec-118',
          entity_type: 'receipt',
          merchant: 'Fuel Stop',
          date: '2026-03-05',
          gross_amount: 61.2,
          revenue_impact: 61.2,
          vat_impact: 10.2
        }
      ],
      adjustments: [
        {
          txn_id: 'inv-190',
          changed_fields: ['gross_amount', 'vat_amount'],
          revenue_impact: 336,
          vat_impact: 56,
          current_transaction: {
            merchant: 'Acme Interiors',
            gross_amount: 960,
            date: '2026-02-24'
          }
        }
      ],
      revenue_impact: 1786.8,
      vat_impact: 297.8,
      changed_since_snapshot: true
    }
  }
];

const styles = `
  :root { --primary: #0d5c63; --primary-strong: #083d42; --success: #2d8f5b; --danger: #cc444b; --warning: #f4b860; --bg-app: #f4f1ea; --bg-card: #fffdf8; --text-main: #182224; --text-muted: #5f6b6d; --border: #d9d2c3; --nav-bg: rgba(255,253,248,0.96); --chip-bg: #eef3f1; --shadow: 0 18px 42px rgba(24,34,36,0.08); }
  [data-theme='dark'] { --primary: #63c3b1; --primary-strong: #92e0d2; --success: #63c3b1; --danger: #ff7c82; --warning: #f4b860; --bg-app: #0d1415; --bg-card: #162022; --text-main: #f1f5f4; --text-muted: #95a4a4; --border: #243335; --nav-bg: rgba(22,32,34,0.96); --chip-bg: #1b282a; --shadow: 0 20px 48px rgba(0,0,0,0.34); }
  body { background: radial-gradient(circle at top, rgba(13,92,99,0.14), transparent 34%), var(--bg-app); color: var(--text-main); margin: 0; font-family: Georgia, 'Times New Roman', serif; }
  .shell { max-width: 1080px; margin: 0 auto; }
  .momentum-bar { background: linear-gradient(135deg, var(--primary) 0%, var(--primary-strong) 100%); border-radius: 24px; padding: 24px; color: white; margin-bottom: 20px; box-shadow: var(--shadow); }
  .attention-item, .compact-card, .insight-card, .capture-panel, .preview-panel, .empty-panel { background: var(--bg-card); border-radius: 18px; border: 1px solid var(--border); box-shadow: var(--shadow); }
  .attention-item { display: flex; align-items: center; padding: 14px; margin-bottom: 10px; }
  .compact-card { padding: 16px; cursor: pointer; height: 100%; }
  .insight-card { padding: 14px; margin-bottom: 10px; border-left: 4px solid var(--primary); position: relative; }
  .capture-panel, .preview-panel, .empty-panel { padding: 20px; }
  .capture-btn-container { position: fixed; bottom: 88px; right: 16px; z-index: 2147483647; display: flex; flex-direction: column; align-items: end; pointer-events: none; }
  .capture-btn-container .log-something-btn { pointer-events: auto; }
  .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; min-height: 64px; background: var(--nav-bg); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid var(--border); backdrop-filter: blur(12px); z-index: 1000; }
  .nav-item { display: flex; flex-direction: column; align-items: center; font-size: 0.68rem; color: var(--text-muted); cursor: pointer; padding: 6px 4px; }
  .nav-item.active { color: var(--primary); font-weight: 700; }
  .log-something-btn, .primary-action, .secondary-action, .danger-action { border-radius: 999px; border: none; display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-weight: 700; }
  .log-something-btn, .primary-action { background: var(--primary); color: white; box-shadow: var(--shadow); }
  .log-something-btn { padding: 12px 20px; min-height: 48px; }
  .primary-action, .secondary-action, .danger-action { padding: 12px 18px; min-height: 44px; }
  .secondary-action { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
  .danger-action { background: rgba(204,68,75,0.12); color: var(--danger); border: 1px solid rgba(204,68,75,0.28); }
  .grouped-section { margin-bottom: 20px; }
  .grouped-section-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
  .grouped-section-header h5 { margin: 0; }
  .group-toggle-actions { display: flex; gap: 8px; flex-wrap: wrap; }
  .group-toggle-btn { border: 1px solid var(--border); background: transparent; color: var(--text-muted); border-radius: 999px; padding: 8px 12px; font-weight: 700; font-size: 0.78rem; }
  .date-group-shell { border: 1px solid var(--border); border-radius: 18px; background: var(--bg-card); box-shadow: var(--shadow); overflow: hidden; margin-bottom: 10px; }
  .date-group-header { width: 100%; background: transparent; padding: 12px 14px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border: none; }
  .date-group-header-meta { display: flex; align-items: center; gap: 8px; }
  .date-group-count { border-radius: 999px; padding: 4px 9px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }
  .date-group-body { padding: 0 12px 12px; }
  .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
  .voice-context-banner { display: grid; gap: 10px; padding: 14px 16px; margin-bottom: 16px; border-radius: 18px; background: var(--bg-card); border: 1px solid var(--border); box-shadow: var(--shadow); }
  .voice-context-row, .voice-chip-actions, .voice-chip-labels { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .voice-context-pill, .voice-action-pill { border-radius: 999px; padding: 6px 10px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.74rem; font-weight: 700; }
  .voice-context-pill.active { background: rgba(13,92,99,0.12); color: var(--primary-strong); border-color: rgba(13,92,99,0.24); }
  .voice-micro-chip { display: grid; gap: 10px; padding: 14px 16px; border-radius: 18px; background: rgba(13,92,99,0.08); border: 1px solid rgba(13,92,99,0.18); }
  .voice-micro-chip strong { display: block; }
  .inbox-action-card.voice-target { border-color: rgba(13,92,99,0.36); box-shadow: 0 0 0 2px rgba(13,92,99,0.12), var(--shadow); }
  .spinner { animation: rotate 2s linear infinite; }
  .capture-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr); gap: 18px; align-items: start; }
  .command-centre { display: grid; gap: 18px; }
  .command-shell { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(300px, 0.75fr); gap: 18px; align-items: stretch; }
  .command-hero { background: linear-gradient(150deg, #14353a 0%, #0d5c63 55%, #8bcbb5 140%); border-radius: 28px; padding: 26px; color: white; box-shadow: var(--shadow); position: relative; overflow: hidden; }
  .command-hero::after { content: ''; position: absolute; inset: auto -60px -90px auto; width: 220px; height: 220px; border-radius: 50%; background: rgba(255,255,255,0.12); }
  .command-kicker { display: inline-flex; align-items: center; gap: 8px; border-radius: 999px; padding: 7px 12px; background: rgba(255,255,255,0.16); font-size: 0.74rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
  .command-hero h3 { margin: 14px 0 8px; font-size: 2rem; line-height: 1.1; max-width: 12ch; }
  .command-hero p { margin: 0; max-width: 48ch; color: rgba(255,255,255,0.84); }
  .hero-metrics { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 18px; }
  .hero-metric { padding: 14px; border-radius: 18px; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.12); backdrop-filter: blur(10px); }
  .hero-metric strong { display: block; font-size: 1.2rem; margin-top: 4px; }
  .hero-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; position: relative; z-index: 1; }
  .hero-action-main, .hero-action-secondary { border: none; border-radius: 999px; padding: 12px 18px; font-weight: 700; display: inline-flex; align-items: center; gap: 8px; }
  .hero-action-main { background: #f7f3e8; color: #173135; }
  .hero-action-secondary { background: transparent; color: white; border: 1px solid rgba(255,255,255,0.26); }
  .command-rail, .performance-grid, .insight-feed { display: grid; gap: 14px; }
  .command-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 24px; box-shadow: var(--shadow); padding: 18px; }
  .command-card h5, .command-card h6, .command-card p { margin-top: 0; }
  .rail-stack { display: grid; gap: 12px; }
  .mini-stat-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
  .mini-stat { border-radius: 18px; padding: 14px; background: var(--chip-bg); border: 1px solid var(--border); }
  .mini-stat strong { display: block; font-size: 1.15rem; margin-top: 4px; }
  .attention-list { display: grid; gap: 10px; }
  .attention-row { display: grid; grid-template-columns: auto 1fr auto; gap: 10px; align-items: start; border-radius: 18px; border: 1px solid var(--border); background: var(--chip-bg); padding: 12px; }
  .attention-row strong, .feed-row strong { display: block; margin-bottom: 2px; }
  .attention-row small, .feed-row small { color: var(--text-muted); }
  .attention-icon { width: 34px; height: 34px; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; }
  .attention-icon.urgent { background: rgba(204,68,75,0.16); color: var(--danger); }
  .attention-icon.watch { background: rgba(244,184,96,0.2); color: #9b6610; }
  .attention-icon.good { background: rgba(45,143,91,0.16); color: var(--success); }
  .attention-action { border: none; background: transparent; color: var(--primary); font-weight: 700; }
  .performance-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .performance-card { border-radius: 22px; padding: 18px; background: var(--bg-card); border: 1px solid var(--border); box-shadow: var(--shadow); min-height: 154px; display: flex; flex-direction: column; justify-content: space-between; }
  .performance-card strong { font-size: 1.7rem; line-height: 1; display: block; margin: 8px 0 4px; }
  .performance-foot { display: flex; justify-content: space-between; gap: 12px; color: var(--text-muted); font-size: 0.85rem; }
  .progress-shell { margin-top: 10px; height: 10px; border-radius: 999px; background: rgba(13,92,99,0.12); overflow: hidden; }
  .progress-bar { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #0d5c63, #7bcbb2); }
  .feed-row { display: grid; grid-template-columns: auto 1fr auto; gap: 10px; align-items: start; border-radius: 18px; border: 1px solid var(--border); background: var(--bg-card); padding: 12px; }
  .feed-tag { border-radius: 999px; padding: 6px 10px; background: var(--chip-bg); border: 1px solid var(--border); color: var(--text-muted); font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }
  .capture-type-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin: 16px 0; }
  .capture-type-btn { border-radius: 16px; border: 1px solid var(--border); background: var(--chip-bg); color: var(--text-main); padding: 12px; font-weight: 700; text-transform: capitalize; }
  .capture-type-btn.active { background: var(--primary); border-color: var(--primary); color: white; }
  .capture-field-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
  .field-shell { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
  .field-shell label, .preview-field label { font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); }
  .field-shell input, .field-shell textarea, .preview-field input, .preview-field textarea, .preview-field select { width: 100%; border-radius: 14px; border: 1px solid var(--border); background: transparent; color: var(--text-main); padding: 12px 14px; font-size: 0.96rem; }
  .field-shell textarea, .preview-field textarea { min-height: 120px; resize: vertical; }
  .capture-inline-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
  .meta-chip { background: var(--chip-bg); border: 1px solid var(--border); border-radius: 999px; color: var(--text-muted); padding: 6px 10px; font-size: 0.78rem; }
  .preview-header { display: flex; justify-content: space-between; gap: 16px; align-items: start; margin-bottom: 16px; }
  .preview-header h5, .capture-panel h4, .empty-panel h5 { margin: 0; }
  .preview-badge { border-radius: 999px; padding: 6px 10px; font-size: 0.76rem; font-weight: 700; text-transform: uppercase; background: var(--chip-bg); color: var(--text-muted); border: 1px solid var(--border); }
  .preview-badge.high { background: rgba(45,143,91,0.14); color: var(--success); border-color: rgba(45,143,91,0.28); }
  .preview-badge.medium { background: rgba(244,184,96,0.18); color: #9b6610; border-color: rgba(244,184,96,0.28); }
  .preview-badge.low { background: rgba(204,68,75,0.14); color: var(--danger); border-color: rgba(204,68,75,0.28); }
  .preview-field-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
  .preview-field { display: flex; flex-direction: column; gap: 6px; }
  .preview-value { min-height: 48px; border-radius: 14px; border: 1px solid var(--border); background: var(--chip-bg); color: var(--text-main); padding: 12px 14px; }
  .preview-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
  .preview-note { margin-top: 12px; color: var(--text-muted); font-size: 0.88rem; }
  .panel-warning { border-radius: 14px; border: 1px solid rgba(244,184,96,0.32); background: rgba(244,184,96,0.12); color: #8a5c12; padding: 12px 14px; margin-bottom: 14px; }
  .panel-error { border-radius: 14px; border: 1px solid rgba(204,68,75,0.32); background: rgba(204,68,75,0.12); color: var(--danger); padding: 12px 14px; margin-bottom: 14px; }
  .small-muted { color: var(--text-muted); font-size: 0.9rem; }
  .status-pill { display: inline-flex; align-items: center; gap: 8px; background: rgba(13,92,99,0.1); color: var(--primary); border: 1px solid rgba(13,92,99,0.2); border-radius: 999px; padding: 6px 12px; font-size: 0.78rem; font-weight: 700; }
  .readiness-layout { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(320px, 0.75fr); gap: 18px; align-items: start; }
  .readiness-hero { background: linear-gradient(145deg, #173135 0%, #0d5c63 55%, #9ed8bf 140%); border-radius: 28px; color: white; padding: 26px; box-shadow: var(--shadow); position: relative; overflow: hidden; }
  .readiness-hero::after { content: ''; position: absolute; right: -50px; top: -35px; width: 180px; height: 180px; border-radius: 50%; background: rgba(255,255,255,0.1); }
  .readiness-hero h3 { margin: 14px 0 10px; font-size: 2.2rem; line-height: 1; }
  .readiness-hero p { margin: 0; max-width: 54ch; color: rgba(255,255,255,0.82); }
  .readiness-kicker { display: inline-flex; align-items: center; gap: 8px; border-radius: 999px; background: rgba(255,255,255,0.14); padding: 7px 12px; font-size: 0.74rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
  .readiness-stat-grid, .severity-grid, .history-grid { display: grid; gap: 12px; }
  .readiness-stat-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 18px; }
  .readiness-stat { border-radius: 18px; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.14); padding: 14px; backdrop-filter: blur(10px); }
  .readiness-stat strong { display: block; font-size: 1.3rem; margin-top: 4px; }
  .readiness-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; position: relative; z-index: 1; }
  .readiness-secondary { background: transparent; border: 1px solid rgba(255,255,255,0.28); color: white; }
  .readiness-panel { background: var(--bg-card); border: 1px solid var(--border); border-radius: 24px; padding: 20px; box-shadow: var(--shadow); }
  .readiness-panel h5, .readiness-panel h6, .readiness-panel p { margin-top: 0; }
  .readiness-side-stack { display: grid; gap: 14px; }
  .finish-now-list { display: grid; gap: 12px; }
  .finish-now-card { display: grid; grid-template-columns: 52px minmax(0, 1fr) auto; gap: 14px; align-items: center; border-radius: 18px; border: 1px solid var(--border); background: var(--chip-bg); padding: 16px; }
  .finish-now-order { width: 40px; height: 40px; border-radius: 14px; background: rgba(13,92,99,0.12); display: flex; align-items: center; justify-content: center; font-weight: 700; color: var(--primary-strong); }
  .finish-now-body { display: grid; gap: 10px; min-width: 0; }
  .finish-now-actions { display: flex; align-items: center; }
  .status-pill-success { color: var(--success); border-color: rgba(45,143,91,0.26); background: rgba(45,143,91,0.1); }
  .severity-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .severity-card, .history-card, .issue-row, .timeline-row { border-radius: 18px; border: 1px solid var(--border); background: var(--chip-bg); }
  .severity-card { padding: 14px; }
  .severity-card strong { display: block; font-size: 1.2rem; margin-top: 4px; }
  .severity-pill, .timeline-pill, .issue-pill { display: inline-flex; align-items: center; border-radius: 999px; padding: 5px 10px; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }
  .severity-pill.high, .issue-pill.high { background: rgba(204,68,75,0.14); color: var(--danger); border: 1px solid rgba(204,68,75,0.24); }
  .severity-pill.medium, .issue-pill.medium { background: rgba(244,184,96,0.18); color: #9b6610; border: 1px solid rgba(244,184,96,0.3); }
  .severity-pill.low, .issue-pill.low { background: rgba(45,143,91,0.14); color: var(--success); border: 1px solid rgba(45,143,91,0.24); }
  .timeline-pill.live { background: rgba(13,92,99,0.12); color: var(--primary); border: 1px solid rgba(13,92,99,0.22); }
  .timeline-pill.archived { background: rgba(24,34,36,0.08); color: var(--text-muted); border: 1px solid rgba(24,34,36,0.14); }
  .issue-list { display: grid; gap: 12px; }
  .issue-row { padding: 16px; display: grid; gap: 12px; }
  .issue-head, .issue-meta, .history-card { display: flex; justify-content: space-between; gap: 12px; align-items: start; }
  .issue-meta { flex-wrap: wrap; }
  .issue-links { display: flex; flex-wrap: wrap; gap: 8px; }
  .issue-link { border: 1px solid var(--border); background: transparent; color: var(--primary); border-radius: 999px; padding: 8px 12px; font-weight: 700; }
  .history-grid { grid-template-columns: 1fr; }
  .history-card { padding: 14px; }
  .history-score { font-size: 1.5rem; line-height: 1; font-weight: 700; }
  .readiness-explainer { display: grid; gap: 8px; margin-top: 12px; }
  .readiness-note { border-radius: 16px; padding: 12px 14px; border: 1px solid var(--border); background: var(--chip-bg); color: var(--text-muted); }
  .governance-action-grid { display: grid; gap: 10px; }
  .policy-record-list, .audit-event-list { display: grid; gap: 10px; }
  .policy-record, .audit-event { border-radius: 16px; padding: 12px 14px; border: 1px solid var(--border); background: var(--chip-bg); }
  .policy-record strong, .audit-event strong { display: block; margin-bottom: 4px; }
  .mode-badge { display: inline-flex; align-items: center; gap: 8px; border-radius: 999px; padding: 8px 12px; font-size: 0.78rem; font-weight: 700; border: 1px solid transparent; }
  .mode-badge.warning { background: rgba(244,184,96,0.18); color: #9b6610; border-color: rgba(244,184,96,0.3); }
  .mode-badge.safe { background: rgba(45,143,91,0.14); color: var(--success); border-color: rgba(45,143,91,0.24); }
  .auto-commit-banner { display: flex; justify-content: space-between; gap: 14px; align-items: start; border-radius: 22px; padding: 16px 18px; margin-bottom: 16px; border: 1px solid var(--border); background: var(--bg-card); box-shadow: var(--shadow); }
  .auto-commit-banner.warning { border-color: rgba(244,184,96,0.34); background: linear-gradient(145deg, rgba(244,184,96,0.16), rgba(255,255,255,0.72)); }
  .auto-commit-banner.safe { border-color: rgba(45,143,91,0.26); background: linear-gradient(145deg, rgba(45,143,91,0.12), rgba(255,255,255,0.72)); }
  .auto-commit-banner strong { display: block; margin-bottom: 4px; }
  .control-centre-layout { display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(320px, 0.7fr); gap: 18px; align-items: start; }
  .control-centre-stack { display: grid; gap: 14px; }
  .control-hero { background: linear-gradient(145deg, #1f2937 0%, #0d5c63 58%, #9ed8bf 140%); color: white; border-radius: 28px; padding: 24px; box-shadow: var(--shadow); position: relative; overflow: hidden; }
  .control-hero::after { content: ''; position: absolute; right: -42px; top: -30px; width: 160px; height: 160px; border-radius: 50%; background: rgba(255,255,255,0.1); }
  .control-hero p { color: rgba(255,255,255,0.84); max-width: 58ch; }
  .control-hero-grid, .health-stat-grid, .control-grid-two { display: grid; gap: 12px; }
  .control-hero-grid, .health-stat-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .control-grid-two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .control-stat, .health-stat, .session-card, .toggle-card { border-radius: 18px; border: 1px solid var(--border); background: var(--chip-bg); padding: 14px; }
  .control-hero .control-stat { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.16); }
  .control-stat strong, .health-stat strong { display: block; font-size: 1.3rem; margin-top: 4px; }
  .control-list { display: grid; gap: 10px; }
  .control-row { display: flex; justify-content: space-between; gap: 12px; align-items: start; border-radius: 16px; border: 1px solid var(--border); background: var(--chip-bg); padding: 12px 14px; }
  .session-card strong, .toggle-card strong, .control-row strong { display: block; margin-bottom: 4px; }
  .inbox-mobile-shell { display: grid; gap: 16px; }
  .inbox-mobile-hero { background: linear-gradient(145deg, #12292d 0%, #0d5c63 58%, #9fdac3 145%); color: white; border-radius: 28px; padding: 24px; box-shadow: var(--shadow); position: relative; overflow: hidden; }
  .inbox-mobile-hero::after { content: ''; position: absolute; right: -55px; top: -35px; width: 170px; height: 170px; border-radius: 50%; background: rgba(255,255,255,0.12); }
  .inbox-mobile-hero h4 { margin: 12px 0 8px; font-size: 2rem; line-height: 1; }
  .inbox-mobile-hero p { margin: 0; max-width: 48ch; color: rgba(255,255,255,0.84); }
  .inbox-kicker { display: inline-flex; align-items: center; gap: 8px; border-radius: 999px; background: rgba(255,255,255,0.14); padding: 7px 12px; font-size: 0.74rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
  .inbox-mobile-stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 18px; }
  .inbox-mobile-stat { border-radius: 18px; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.16); padding: 14px; }
  .inbox-mobile-stat strong { display: block; font-size: 1.25rem; margin-top: 4px; }
  .inbox-filter-row { display: flex; flex-wrap: wrap; gap: 10px; }
  .inbox-filter-chip { border-radius: 999px; border: 1px solid var(--border); background: var(--chip-bg); color: var(--text-main); padding: 10px 14px; font-weight: 700; display: inline-flex; align-items: center; gap: 8px; }
  .inbox-filter-chip.active { background: var(--primary); color: white; border-color: var(--primary); }
  .inbox-filter-chip small { opacity: 0.84; font-size: 0.74rem; }
  .inbox-card-list { display: grid; gap: 14px; }
  .inbox-action-card { border-radius: 24px; border: 1px solid var(--border); background: var(--bg-card); box-shadow: var(--shadow); padding: 18px; display: grid; gap: 14px; }
  .inbox-card-top { display: flex; justify-content: space-between; gap: 12px; align-items: start; }
  .inbox-card-top strong { display: block; font-size: 1.08rem; margin-bottom: 4px; }
  .inbox-card-subline { color: var(--text-muted); font-size: 0.88rem; }
  .inbox-chip-row { display: flex; flex-wrap: wrap; gap: 8px; }
  .inbox-issue-chip, .inbox-suggestion-chip { display: inline-flex; align-items: center; gap: 6px; border-radius: 999px; padding: 7px 10px; font-size: 0.74rem; font-weight: 700; border: 1px solid var(--border); background: var(--chip-bg); color: var(--text-muted); }
  .inbox-issue-chip.high { border-color: rgba(204,68,75,0.24); background: rgba(204,68,75,0.12); color: var(--danger); }
  .inbox-issue-chip.medium { border-color: rgba(244,184,96,0.28); background: rgba(244,184,96,0.14); color: #9b6610; }
  .inbox-suggestion-chip { color: var(--primary); }
  .inbox-explainer { color: var(--text-main); margin: 0; }
  .inbox-action-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
  .inbox-field { display: flex; flex-direction: column; gap: 6px; }
  .inbox-field label { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); }
  .inbox-field input, .inbox-field select { width: 100%; border-radius: 14px; border: 1px solid var(--border); background: transparent; color: var(--text-main); padding: 12px 14px; font-size: 0.96rem; }
  .inbox-toggle-row, .inbox-duplicate-row, .inbox-footer-row { display: flex; flex-wrap: wrap; gap: 10px; }
  .inbox-toggle { flex: 1; min-width: 92px; border-radius: 16px; border: 1px solid var(--border); background: var(--chip-bg); color: var(--text-main); padding: 12px 14px; font-weight: 700; }
  .inbox-toggle.active { background: var(--primary); color: white; border-color: var(--primary); }
  .inbox-footer-row { justify-content: space-between; align-items: center; }
  .inbox-footer-actions { display: flex; flex-wrap: wrap; gap: 10px; }
  .inbox-inline-status { font-size: 0.84rem; color: var(--text-muted); }
  .inbox-empty { border-radius: 24px; border: 1px dashed var(--border); background: rgba(45,143,91,0.08); padding: 22px; color: var(--text-main); }
  .inbox-message.success { border-color: rgba(45,143,91,0.28); background: rgba(45,143,91,0.12); color: var(--success); }
  .inbox-message.error { border-color: rgba(204,68,75,0.32); background: rgba(204,68,75,0.12); color: var(--danger); }
  .capture-mode-panel { border-radius: 22px; border: 1px solid var(--border); background: linear-gradient(145deg, rgba(13,92,99,0.08), rgba(158,216,191,0.08)); padding: 18px; margin-bottom: 16px; box-shadow: var(--shadow); }
  .capture-mode-panel.warning { border-color: rgba(244,184,96,0.3); background: linear-gradient(145deg, rgba(244,184,96,0.16), rgba(255,255,255,0.88)); }
  .capture-mode-panel.safe { border-color: rgba(45,143,91,0.24); background: linear-gradient(145deg, rgba(45,143,91,0.12), rgba(255,255,255,0.88)); }
  .snapshot-toolbar, .snapshot-card-head, .quarter-state-row, .snapshot-meta-row, .diff-impact-grid, .diff-columns, .snapshot-download-row { display: flex; gap: 10px; }
  .snapshot-toolbar, .snapshot-card-head, .quarter-state-row, .snapshot-meta-row, .snapshot-download-row { align-items: center; justify-content: space-between; flex-wrap: wrap; }
  .snapshot-version-list, .warning-list, .diff-list, .lifecycle-form { display: grid; gap: 12px; }
  .snapshot-version-card, .warning-card, .diff-card { border-radius: 18px; border: 1px solid var(--border); background: var(--chip-bg); padding: 14px; }
  .snapshot-version-card.selected { border-color: var(--primary); box-shadow: inset 0 0 0 1px rgba(13,92,99,0.18); }
  .snapshot-version-button, .download-link-button { width: 100%; border: none; background: transparent; color: inherit; text-align: left; padding: 0; }
  .snapshot-label-row, .warning-head { display: flex; justify-content: space-between; gap: 10px; align-items: start; }
  .snapshot-version-code { font-size: 1.05rem; font-weight: 700; }
  .snapshot-subline { color: var(--text-muted); font-size: 0.85rem; }
  .warning-card.warning { border-color: rgba(244,184,96,0.34); background: rgba(244,184,96,0.12); }
  .warning-card.info { border-color: rgba(13,92,99,0.24); background: rgba(13,92,99,0.08); }
  .warning-card.error { border-color: rgba(204,68,75,0.32); background: rgba(204,68,75,0.12); }
  .warning-title { font-weight: 700; }
  .diff-impact-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .diff-impact-stat { border-radius: 16px; border: 1px solid var(--border); background: var(--bg-card); padding: 12px; }
  .diff-impact-stat strong { display: block; font-size: 1.2rem; margin-top: 4px; }
  .diff-columns { align-items: stretch; }
  .diff-columns > div { flex: 1; min-width: 0; }
  .diff-card h6 { margin-bottom: 10px; }
  .diff-row { border-top: 1px solid var(--border); padding-top: 10px; margin-top: 10px; }
  .diff-row:first-child { border-top: none; padding-top: 0; margin-top: 0; }
  .lifecycle-form textarea, .lifecycle-form input { width: 100%; border-radius: 14px; border: 1px solid var(--border); background: transparent; color: var(--text-main); padding: 12px 14px; font-size: 0.96rem; }
  .lifecycle-form textarea { min-height: 92px; resize: vertical; }
  .quarter-state-badge { display: inline-flex; align-items: center; gap: 8px; border-radius: 999px; padding: 6px 12px; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; }
  .quarter-state-badge.open { background: rgba(45,143,91,0.14); color: var(--success); border: 1px solid rgba(45,143,91,0.24); }
  .quarter-state-badge.closed { background: rgba(204,68,75,0.14); color: var(--danger); border: 1px solid rgba(204,68,75,0.24); }
  .quarter-state-badge.pending { background: rgba(244,184,96,0.18); color: #9b6610; border: 1px solid rgba(244,184,96,0.3); }
  .header-controls { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .header-select { min-width: 210px; border-radius: 999px; border: 1px solid var(--border); background: var(--bg-card); color: var(--text-main); padding: 10px 14px; }
  @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
  @media (max-width: 860px) {
    .capture-grid, .preview-field-grid, .capture-field-grid, .command-shell, .performance-grid, .hero-metrics, .readiness-layout, .readiness-stat-grid, .severity-grid, .diff-impact-grid, .control-centre-layout, .control-hero-grid, .health-stat-grid, .control-grid-two, .inbox-mobile-stats, .inbox-action-grid, .finish-now-card { grid-template-columns: 1fr; }
    .diff-columns { display: grid; }
    .finish-now-actions { justify-content: stretch; }
  }
  @media (max-width: 640px) {
    .capture-btn-container { right: 12px; bottom: 84px; }
    .log-something-btn { padding: 10px 16px; min-height: 44px; }
    .capture-type-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .mini-stat-grid { grid-template-columns: 1fr; }
    .inbox-mobile-hero { padding: 20px; }
    .inbox-mobile-hero h4 { font-size: 1.7rem; }
    .inbox-action-card { padding: 16px; }
  }
`;

const isMonetaryType = (type) => MONETARY_TYPES.includes(type);
const getTodayForInput = () => new Date().toISOString().slice(0, 10);

const buildManualPayload = (form) => {
  const note = form.note.trim();
  const grossAmount = form.grossAmount === '' ? null : Number(form.grossAmount);
  const netAmount = form.netAmount === '' ? null : Number(form.netAmount);
  const vatAmount = form.vatAmount === '' ? null : Number(form.vatAmount);
  const vatRate = form.vatRate === '' ? null : Number(form.vatRate);

  return {
    type: form.type,
    device_id: 'web-manual-entry',
    client_name: form.counterparty.trim() || null,
    amount: grossAmount,
    gross_amount: grossAmount,
    net_amount: netAmount,
    vat_amount: vatAmount,
    vat_rate: vatRate,
    raw_note: note || `${form.type} entry`,
    extracted_text: note || `${form.type} entry`,
    transaction_date: form.relevantDate || undefined,
    due_date: form.type === 'invoice' ? form.relevantDate || undefined : undefined,
    labels: form.category.trim() ? [form.category.trim()] : [],
  };
};

const buildPreviewForm = (preview, note = '') => ({
  entityType: preview?.entity_type || 'invoice',
  counterparty: preview?.counterparty || '',
  grossAmount: preview?.gross_amount ?? '',
  netAmount: preview?.net_amount ?? '',
  vatAmount: preview?.vat_amount ?? '',
  vatRate: preview?.vat_rate ?? '',
  category: preview?.category || '',
  relevantDate: preview?.relevant_date ? String(preview.relevant_date).slice(0, 10) : getTodayForInput(),
  note,
});

const ACTIVITY_TIME_PERIOD_OPTIONS = [
  { value: '', label: 'All dates' },
  { value: 'today', label: 'Today' },
  { value: 'this_week', label: 'This week' },
  { value: 'last_week', label: 'Last week' },
];

const CLOSED_JOB_STATUSES = new Set(['completed', 'closed', 'won', 'lost', 'cancelled', 'canceled']);

const getActivityItemDate = (item) => {
  const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
  if (!dateValue) {
    return null;
  }

  const parsedDate = new Date(dateValue);
  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
};

const formatGroupDateLabel = (date) => date.toLocaleDateString('en-GB', {
  weekday: 'short',
  day: '2-digit',
  month: 'short',
  year: 'numeric',
});

const buildGroupedDateCollections = (entries, getDate, sortDirection = 'desc') => {
  const datedEntries = entries.map((entry) => {
    const date = getDate(entry);
    if (!date) {
      return {
        entry,
        date: null,
        sortValue: sortDirection === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY,
        dateKey: 'no-date',
        dateLabel: 'No date',
      };
    }

    return {
      entry,
      date,
      sortValue: date.getTime(),
      dateKey: date.toISOString().slice(0, 10),
      dateLabel: formatGroupDateLabel(date),
    };
  });

  datedEntries.sort((left, right) => (
    sortDirection === 'asc'
      ? left.sortValue - right.sortValue
      : right.sortValue - left.sortValue
  ));

  const groups = [];
  const groupMap = new Map();

  datedEntries.forEach(({ entry, dateKey, dateLabel }) => {
    if (!groupMap.has(dateKey)) {
      const nextGroup = { dateKey, dateLabel, items: [] };
      groupMap.set(dateKey, nextGroup);
      groups.push(nextGroup);
    }
    groupMap.get(dateKey).items.push(entry);
  });

  return groups;
};

const isOpenJob = (job) => !CLOSED_JOB_STATUSES.has(String(job?.status || '').toLowerCase());

const getJobDate = (job) => {
  const dateValue = job?.next_due_date || job?.updated_at || job?.created_at || null;
  if (!dateValue) {
    return null;
  }

  const parsedDate = new Date(dateValue);
  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
};

const matchesActivityClientFilter = (item, clientFilter) => {
  const normalizedFilter = String(clientFilter || '').trim().toLowerCase();
  if (!normalizedFilter) {
    return true;
  }

  const clientFields = [
    item?.client_name,
    item?.counterparty_name,
    item?.counterparty,
    item?.extracted_text,
    item?.raw_note,
  ];

  return clientFields.some((value) => String(value || '').toLowerCase().includes(normalizedFilter));
};

const getDayBounds = (referenceDate) => {
  const start = new Date(referenceDate);
  start.setHours(0, 0, 0, 0);
  const end = new Date(referenceDate);
  end.setHours(23, 59, 59, 999);
  return { start, end };
};

const getWeekBounds = (referenceDate, offsetWeeks = 0) => {
  const start = new Date(referenceDate);
  const day = start.getDay();
  const diff = day === 0 ? -6 : 1 - day;
  start.setDate(start.getDate() + diff + (offsetWeeks * 7));
  start.setHours(0, 0, 0, 0);

  const end = new Date(start);
  end.setDate(end.getDate() + 6);
  end.setHours(23, 59, 59, 999);
  return { start, end };
};

const getActivityPeriodBounds = (periodKey, referenceDate = new Date()) => {
  switch (periodKey) {
    case 'today':
      return getDayBounds(referenceDate);
    case 'this_week':
      return getWeekBounds(referenceDate, 0);
    case 'last_week':
      return getWeekBounds(referenceDate, -1);
    default:
      return null;
  }
};

const matchesActivityTimePeriod = (item, periodKey) => {
  if (!periodKey) {
    return true;
  }

  const itemDate = getActivityItemDate(item);
  const periodBounds = getActivityPeriodBounds(periodKey);
  if (!itemDate || !periodBounds) {
    return false;
  }

  return itemDate >= periodBounds.start && itemDate <= periodBounds.end;
};

const resolveVoiceTimePeriod = (slots = {}) => {
  if (slots.time_period) {
    return slots.time_period;
  }

  if (slots.time_period_hint?.key) {
    return slots.time_period_hint.key;
  }

  if (slots.date_hint?.raw === 'today') {
    return 'today';
  }

  return null;
};

const resolveVoiceDateFilter = (slots = {}) => {
  if (slots.time_period || slots.time_period_hint?.key) {
    return null;
  }

  if (slots.date) {
    return String(slots.date).slice(0, 10);
  }

  if (slots.date_hint?.iso) {
    return String(slots.date_hint.iso).slice(0, 10);
  }

  return null;
};

const currencyValue = (value) => {
  if (value === null || value === undefined || value === '') {
    return 'Pending';
  }
  const numeric = Number(value);
  return Number.isFinite(numeric) ? `GBP ${numeric.toFixed(2)}` : String(value);
};

const formatCurrency = (value, digits = 0) => {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    return digits === 0 ? 'GBP 0' : `GBP ${Number(0).toFixed(digits)}`;
  }
  return `GBP ${numeric.toFixed(digits)}`;
};

const formatPercentDelta = (value) => {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) {
    return 'Flat vs last week';
  }
  if (numeric === 0) {
    return 'Flat vs last week';
  }
  return `${numeric > 0 ? '+' : ''}${numeric.toFixed(0)}% vs last week`;
};

const formatQuarterLabel = (quarterReference, periodStart, periodEnd) => {
  if (quarterReference) {
    return `${quarterReference} active quarter`;
  }
  return `${periodStart || 'Current period'} to ${periodEnd || 'Active period'}`;
};

const formatIssueAmount = (amount, direction) => {
  if (!Number.isFinite(Number(amount))) {
    return 'Amount pending';
  }
  return `${direction === 'in' ? 'Inflow' : 'Outflow'} ${formatCurrency(amount, 2)}`;
};

const sanitizeCategoryCode = (value) => String(value || '')
  .trim()
  .toUpperCase()
  .replace(/[^A-Z0-9]+/g, '_')
  .replace(/^_+|_+$/g, '');

const buildSuggestedCategory = (merchant, existingSuggestion = null) => {
  if (existingSuggestion?.category_code || existingSuggestion?.category_name) {
    return {
      category_code: existingSuggestion.category_code || sanitizeCategoryCode(existingSuggestion.category_name),
      category_name: existingSuggestion.category_name || existingSuggestion.category_code,
    };
  }

  const matchedRule = INBOX_MERCHANT_SUGGESTIONS.find((rule) => rule.pattern.test(String(merchant || '')));
  if (!matchedRule) {
    return { category_code: '', category_name: '' };
  }

  return {
    category_code: matchedRule.category_code,
    category_name: matchedRule.category_name,
  };
};

const buildInboxDraft = (item) => ({
  category_code: item.category_code || item.suggested_category?.category_code || '',
  category_name: item.category_name || item.suggested_category?.category_name || '',
  business_personal: item.business_personal || '',
  is_split: Boolean(item.is_split),
  split_business_pct: item.split_business_pct === null || item.split_business_pct === undefined ? '' : String(item.split_business_pct),
  duplicate_action: item.duplicate_resolution || 'dismiss',
  duplicate_of_txn_id: item.duplicate_of_txn_id || '',
});

const buildInboxCards = (queueRows = [], readinessReport = null) => {
  const cards = new Map();
  const readinessIssues = Array.isArray(readinessReport?.issue_list) ? readinessReport.issue_list : [];

  const ensureCard = (seed) => {
    const id = String(seed.affected_entity_id || seed.id || seed.entity_id || '');
    if (!id) {
      return null;
    }
    if (!cards.has(id)) {
      const suggestedCategory = buildSuggestedCategory(
        seed.merchant,
        seed.suggested_category ? {
          category_code: seed.suggested_category.category_code || seed.suggested_category,
          category_name: seed.suggested_category.category_name || seed.suggested_category_name || null,
        } : null
      );
      cards.set(id, {
        id,
        merchant: seed.merchant || 'Unknown merchant',
        txn_date: seed.txn_date || seed.date || null,
        amount: seed.amount ?? null,
        direction: seed.direction || 'out',
        blocker_reason: seed.blocker_reason || seed.issue_type || 'missing_category',
        severity: seed.severity || 'medium',
        weight: Number(seed.weight || 0),
        explanation: seed.explanation || '',
        issue_types: [],
        issue_labels: [],
        issues: [],
        resolution_target: seed.resolution_target || null,
        category_code: seed.category_code || '',
        category_name: seed.category_name || '',
        business_personal: seed.business_personal || '',
        is_split: Boolean(seed.is_split),
        split_business_pct: seed.split_business_pct ?? null,
        duplicate_resolution: seed.duplicate_resolution || null,
        duplicate_of_txn_id: seed.duplicate_of_txn_id || null,
        suggested_category: suggestedCategory,
      });
    }

    const existing = cards.get(id);
    existing.weight = Math.max(existing.weight, Number(seed.weight || 0));
    if ((seed.severity || 'low') === 'high' || (existing.severity !== 'high' && seed.severity === 'medium')) {
      existing.severity = seed.severity || existing.severity;
    }
    if (!existing.txn_date && seed.txn_date) {
      existing.txn_date = seed.txn_date;
    }
    if (!existing.amount && Number.isFinite(Number(seed.amount))) {
      existing.amount = seed.amount;
    }
    if (!existing.explanation && seed.explanation) {
      existing.explanation = seed.explanation;
    }
    if (!existing.resolution_target && seed.resolution_target) {
      existing.resolution_target = seed.resolution_target;
    }
    if (!existing.business_personal && seed.business_personal) {
      existing.business_personal = seed.business_personal;
    }
    if (!existing.category_code && seed.category_code) {
      existing.category_code = seed.category_code;
    }
    if (!existing.category_name && seed.category_name) {
      existing.category_name = seed.category_name;
    }
    if (!existing.split_business_pct && seed.split_business_pct !== null && seed.split_business_pct !== undefined) {
      existing.split_business_pct = seed.split_business_pct;
    }
    if (seed.is_split) {
      existing.is_split = true;
    }
    if (seed.duplicate_resolution) {
      existing.duplicate_resolution = seed.duplicate_resolution;
    }
    return existing;
  };

  queueRows.forEach((row) => {
    const card = ensureCard(row);
    if (!card) {
      return;
    }
    const issueType = row.blocker_reason || row.issue_type;
    if (issueType && !card.issue_types.includes(issueType)) {
      card.issue_types.push(issueType);
      card.issue_labels.push(issueType.replace(/_/g, ' '));
      card.issues.push({
        issue_type: issueType,
        label: issueType.replace(/_/g, ' '),
        severity: row.severity || card.severity,
        explanation: row.explanation || '',
        resolution_target: row.resolution_target || null,
      });
    }
  });

  readinessIssues.forEach((issue) => {
    const card = ensureCard(issue);
    if (!card) {
      return;
    }
    const issueType = issue.issue_type;
    if (!card.issue_types.includes(issueType)) {
      card.issue_types.push(issueType);
      card.issue_labels.push(issue.label || issueType.replace(/_/g, ' '));
      card.issues.push({
        issue_type: issueType,
        label: issue.label || issueType.replace(/_/g, ' '),
        severity: issue.severity || card.severity,
        explanation: issue.explanation || '',
        resolution_target: issue.resolution_target || null,
      });
    }
    if (issue.resolution_target) {
      card.resolution_target = issue.resolution_target;
    }
    if (card.blocker_reason === 'missing_category' && issue.issue_type !== 'missing_category') {
      card.blocker_reason = issue.issue_type;
    }
    if (!card.explanation && issue.explanation) {
      card.explanation = issue.explanation;
    }
  });

  return Array.from(cards.values())
    .map((card) => ({
      ...card,
      issue_types: card.issue_types.length ? card.issue_types : [card.blocker_reason],
      issue_labels: card.issue_labels.length ? card.issue_labels : [card.blocker_reason.replace(/_/g, ' ')],
      supports_category: card.issue_types.includes('missing_category'),
      supports_business_personal: card.issue_types.includes('missing_business_personal'),
      supports_split: card.issue_types.includes('missing_split_pct'),
      supports_duplicate: card.issue_types.includes('unresolved_duplicate'),
    }))
    .sort((left, right) => {
      if (right.weight !== left.weight) {
        return right.weight - left.weight;
      }
      return String(right.txn_date || '').localeCompare(String(left.txn_date || ''));
    });
};

const formatPolicyDisplayValue = (policyKey, policyValue) => {
  if (policyKey.includes('_cap_gbp') || policyKey.includes('_threshold_gbp')) {
    return formatCurrency(policyValue, 2);
  }
  if (typeof policyValue === 'boolean') {
    return policyValue ? 'Enabled' : 'Disabled';
  }
  return String(policyValue);
};

const buildSeverityBreakdown = (issueSummary = []) => {
  const totals = issueSummary.reduce((accumulator, issue) => {
    const severity = issue.severity || 'low';
    if (!accumulator[severity]) {
      accumulator[severity] = { severity, count: 0, weight: 0 };
    }
    accumulator[severity].count += Number(issue.count || 0);
    accumulator[severity].weight += Number(issue.total_weight || 0);
    return accumulator;
  }, {});

  return ['high', 'medium', 'low']
    .map((severity) => totals[severity] || { severity, count: 0, weight: 0 })
    .filter((entry) => entry.count > 0 || entry.severity === 'high');
};

const buildHistoricalSnapshots = (report) => {
  if (report?.quarter_reference === 'Q1-2026') {
    return READINESS_HISTORY_DEMO;
  }
  return READINESS_HISTORY_DEMO;
};

const normalizeEventMetadata = (value) => {
  if (!value) {
    return {};
  }
  if (typeof value === 'string') {
    try {
      return JSON.parse(value);
    } catch (error) {
      return {};
    }
  }
  return typeof value === 'object' ? value : {};
};

const toDisplayTimestamp = (value) => {
  if (!value) {
    return 'Pending';
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }
  return date.toLocaleString('en-GB', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatSnapshotVersion = (value) => `Snapshot ${String(Number(value) || 0).padStart(3, '0')}`;

const buildIntegrityWarnings = ({ snapshotStatus, lifecycle, selectedSnapshot }) => {
  const warnings = [];
  const selectedWarnings = Array.isArray(selectedSnapshot?.integrity_warnings) ? selectedSnapshot.integrity_warnings : [];
  warnings.push(...selectedWarnings);

  if (snapshotStatus?.no_change_reason) {
    warnings.push({
      level: 'info',
      title: 'Redundant version creation blocked',
      detail: snapshotStatus.no_change_reason
    });
  }

  if (lifecycle?.quarter_state === 'closed') {
    warnings.push({
      level: 'warning',
      title: 'Quarter is closed',
      detail: `New monetary changes and snapshot versions are blocked until ${lifecycle.quarter_label || 'this quarter'} is reopened.`
    });
  }

  return warnings;
};

const buildSnapshotWorkspaceFromApi = (snapshotStatus, history = [], readinessReport = null) => {
  if (!snapshotStatus && !history.length) {
    return null;
  }

  const lifecycle = snapshotStatus?.quarter_lifecycle || null;
  const snapshots = history
    .filter((event) => event.event_type === 'snapshot_created')
    .map((event) => {
      const metadata = normalizeEventMetadata(event.metadata);
      const snapshotSummary = metadata.snapshot_summary || {
        transaction_count: Array.isArray(metadata.transactions) ? metadata.transactions.length : 0,
        totals: metadata.totals || {},
        vat_totals: metadata.vat_totals || {}
      };
      return {
        snapshot_id: event.entity_id,
        event_id: event.event_id,
        quarter_reference: event.quarter_reference || snapshotStatus?.quarter_reference || readinessReport?.quarter_reference || null,
        version_number: Number(metadata.version_number || 1),
        created_at: event.timestamp,
        description: event.description,
        readiness_pct: Number(metadata.readiness_pct ?? readinessReport?.readiness_pct ?? 0),
        status: snapshotStatus?.latest_snapshot?.snapshot_id === event.entity_id ? 'Current baseline' : 'Archived',
        integrity_warnings: metadata.integrity_warnings || metadata.integrity_warning_summary || [],
        snapshot_summary: snapshotSummary,
        diff_summary: metadata.diff_summary || {
          added_transactions: [],
          voided_transactions: [],
          adjustments: [],
          revenue_impact: 0,
          vat_impact: 0,
          changed_since_snapshot: false
        }
      };
    })
    .sort((left, right) => Number(right.version_number) - Number(left.version_number));

  const selectedSnapshot = snapshots[0] || null;

  return {
    quarter_reference: snapshotStatus?.quarter_reference || readinessReport?.quarter_reference || lifecycle?.quarter_label || null,
    snapshot_status: snapshotStatus,
    quarter_lifecycle: lifecycle,
    snapshots,
    integrity_warnings: buildIntegrityWarnings({
      snapshotStatus,
      lifecycle,
      selectedSnapshot
    }),
    activity_events: history.filter((event) => ['quarter_closed', 'quarter_reopened', 'snapshot_created'].includes(event.event_type))
  };
};

const buildDemoSnapshotWorkspace = () => {
  const snapshotStatus = {
    quarter_reference: READINESS_DEMO_REPORT.quarter_reference,
    latest_snapshot: {
      snapshot_id: SNAPSHOT_DEMO_HISTORY[0].snapshot_id,
      version_number: SNAPSHOT_DEMO_HISTORY[0].version_number,
      created_at: SNAPSHOT_DEMO_HISTORY[0].created_at,
      description: SNAPSHOT_DEMO_HISTORY[0].description
    },
    baseline_exists: true,
    changed_since_snapshot: false,
    can_create_snapshot_version: false,
    next_version_number: 3,
    no_change_reason: 'No changes since Snapshot 002 for Q1-2026.',
    diff: SNAPSHOT_DEMO_HISTORY[0].diff_summary,
    live_transactions: []
  };

  return {
    quarter_reference: READINESS_DEMO_REPORT.quarter_reference,
    snapshot_status: snapshotStatus,
    quarter_lifecycle: {
      id: 'quarter-q1-2026',
      quarter_label: 'Q1-2026',
      quarter_state: 'open',
      status: 'open',
      closed_at: '2026-03-09T09:55:00.000Z',
      reopened_at: '2026-03-10T08:40:00.000Z',
      reopen_reason: 'Late supplier invoice received after final bank sync.',
      confirmation_reference: 'mgr-approval-42',
      governance_metadata: {
        close_reason: 'Quarter review completed',
        reopen_reason: 'Late supplier invoice received after final bank sync.'
      },
      period_start: '2026-01-01',
      period_end: '2026-03-31'
    },
    snapshots: SNAPSHOT_DEMO_HISTORY,
    integrity_warnings: buildIntegrityWarnings({
      snapshotStatus,
      lifecycle: {
        quarter_state: 'open',
        quarter_label: 'Q1-2026'
      },
      selectedSnapshot: SNAPSHOT_DEMO_HISTORY[0]
    }),
    activity_events: [
      {
        event_id: 'evt-q1-reopen',
        event_type: 'quarter_reopened',
        description: 'Q1-2026 reopened',
        timestamp: '2026-03-10T08:40:00.000Z',
        metadata: {
          reopen_reason: 'Late supplier invoice received after final bank sync.',
          confirmation_reference: 'mgr-approval-42'
        }
      },
      {
        event_id: 'evt-snap-q1-2026-v002',
        event_type: 'snapshot_created',
        description: 'Snapshot 002 generated before quarter sign-off',
        timestamp: '2026-03-09T10:24:00.000Z',
        metadata: {
          version_number: 2
        }
      },
      {
        event_id: 'evt-q1-close',
        event_type: 'quarter_closed',
        description: 'Q1-2026 manually closed',
        timestamp: '2026-03-09T09:55:00.000Z',
        metadata: {
          reason: 'Quarter review completed'
        }
      }
    ]
  };
};

function App() {
  const searchParams = typeof window !== 'undefined' ? new URLSearchParams(window.location.search) : null;
  const captureDemoEnabled = typeof window !== 'undefined'
    && searchParams?.get('captureDemo') === '1';
  const commandCentreDemoEnabled = typeof window !== 'undefined'
    && searchParams?.get('commandCentreDemo') === '1';
  const readinessDemoEnabled = typeof window !== 'undefined'
    && searchParams?.get('readinessDemo') === '1';
  const snapshotDemoEnabled = typeof window !== 'undefined'
    && searchParams?.get('snapshotDemo') === '1';
  const inboxDemoEnabled = typeof window !== 'undefined'
    && searchParams?.get('inboxDemo') === '1';
  const voiceDemoCommand = searchParams?.get('voiceDemoCommand') || '';
  const voiceDemoTarget = searchParams?.get('voiceDemoTarget') || '';
  const requestedTab = searchParams?.get('tab');
  const [items, setItems] = useState([]);
  const [upcomingItems, setUpcomingItems] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [vatSummary, setVatSummary] = useState(null);
  const [momentum, setMomentum] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [connectionError, setConnectionError] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [currentTab, setCurrentTab] = useState(requestedTab || (commandCentreDemoEnabled ? 'control' : 'home'));
  const [activityTypeFilter, setActivityTypeFilter] = useState(null);
  const [activityClientFilter, setActivityClientFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [activityDateFilter, setActivityDateFilter] = useState('');
  const [timePeriodFilter, setTimePeriodFilter] = useState(null);
  const [clients, setClients] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [diaryEntries, setDiaryEntries] = useState([]);
  const [theme, setTheme] = useState('light');
  const [appUsers, setAppUsers] = useState(USERS);
  const [currentUser, setCurrentUser] = useState(USERS[0]);
  const [onboardingSession, setOnboardingSession] = useState(null);
  const [authBootstrapped, setAuthBootstrapped] = useState(false);
  const [onboardingBusy, setOnboardingBusy] = useState(false);
  const [onboardingError, setOnboardingError] = useState('');
  const [policyRecords, setPolicyRecords] = useState(() => buildDefaultPolicyRecords({
    tenantId: TENANT_ID,
    actor: USERS[0],
    now: '2026-03-11T16:30:00.000Z',
  }));
  const [governanceAudit, setGovernanceAudit] = useState([]);
  const [syncTelemetry] = useState(DEFAULT_SYNC_TELEMETRY);
  const [activeSessions] = useState(DEFAULT_ACTIVE_SESSIONS);
  const [voiceStatus, setVoiceStatus] = useState('idle');
  const [expandedDateGroups, setExpandedDateGroups] = useState({});
  const [inboxItems, setInboxItems] = useState([]);
  const [quarterReadiness, setQuarterReadiness] = useState(null);
  const [resolvedQuarterIssueIds, setResolvedQuarterIssueIds] = useState(() => deriveResolvedIssueIdsFromSearchParams(
    searchParams,
    READINESS_DEMO_REPORT.issue_list,
  ));
  const [snapshotWorkspace, setSnapshotWorkspace] = useState(null);
  const [selectedSnapshotId, setSelectedSnapshotId] = useState(null);
  const [quarterActionMessage, setQuarterActionMessage] = useState('');
  const [quarterActionError, setQuarterActionError] = useState('');
  const [quarterActionBusy, setQuarterActionBusy] = useState(false);
  const [closeReason, setCloseReason] = useState('Quarter review completed');
  const [reopenReason, setReopenReason] = useState('Late supplier invoice received after final bank sync.');
  const [reopenConfirmation, setReopenConfirmation] = useState('mgr-approval-42');
  const [manualForm, setManualForm] = useState({ ...DEFAULT_MANUAL_FORM, relevantDate: getTodayForInput() });
  const [manualSaving, setManualSaving] = useState(false);
  const [previewDraft, setPreviewDraft] = useState(null);
  const [previewForm, setPreviewForm] = useState(null);
  const [previewMode, setPreviewMode] = useState('review');
  const [previewBusy, setPreviewBusy] = useState(false);
  const [previewError, setPreviewError] = useState('');
  const [inboxFilter, setInboxFilter] = useState('all');
  const [inboxDrafts, setInboxDrafts] = useState({});
  const [inboxBusyId, setInboxBusyId] = useState('');
  const [inboxMessage, setInboxMessage] = useState(null);
  const [activeVoiceContextId, setActiveVoiceContextId] = useState(voiceDemoTarget);
  const [voiceMicroDecisionChip, setVoiceMicroDecisionChip] = useState(null);
  const [inboxLoadMs, setInboxLoadMs] = useState(null);
  const finalTranscriptRef = useRef('');
  const webRecognitionRef = useRef(null);
  const voiceDemoSeedRef = useRef('');
  const quarterStart = '2026-01-01';
  const quarterEnd = '2026-03-31';

  useEffect(() => {
    const load = async () => {
      const { value: savedTheme } = await Preferences.get({ key: 'theme' });
      if (savedTheme) {
        setTheme(savedTheme);
      }
      if (readinessDemoEnabled || snapshotDemoEnabled || inboxDemoEnabled) {
        setQuarterReadiness(READINESS_DEMO_REPORT);
        setInboxItems(READINESS_DEMO_REPORT.issue_list);
        setInboxLoadMs(120);
        setSnapshotWorkspace(buildDemoSnapshotWorkspace());
        setCurrentTab(requestedTab || (inboxDemoEnabled ? 'inbox' : 'quarter'));
        setLoading(false);
        setAuthBootstrapped(true);
        setConnectionError(null);
        setVatSummary(null);
        return;
      }
      let restoredUser = null;
      try {
        const response = await axios.get(`${API_BASE_URL}/auth/me`, {
          headers: { 'bypass-tunnel-reminder': 'true' },
        });
        const parsedSession = normalizeOnboardingSession({
          user: response.data,
          onboarding: response.data?.onboarding || null,
        });
        const sessionUser = createAppUserFromSession(parsedSession, TENANT_ID);
        if (sessionUser?.id) {
          restoredUser = sessionUser;
          setOnboardingSession(parsedSession);
          setAppUsers((previous) => mergeUserIntoList(previous, sessionUser));
          setCurrentUser(sessionUser);
          await Preferences.set({ key: 'userId', value: sessionUser.id });
        }
      } catch (_) {
        setOnboardingSession(null);
      }

      if (!restoredUser) {
        const { value: savedUserId } = await Preferences.get({ key: 'userId' });
        if (savedUserId) {
          const matchedUser = USERS.find((user) => user.id === savedUserId);
          if (matchedUser) {
            setCurrentUser(matchedUser);
          }
        }
      }
      setAuthBootstrapped(true);
      if (MVP_QUARTERLY_EXPORT_MODE && !restoredUser) {
        setLoading(false);
        setConnectionError(null);
        return;
      }
      fetchAllData(restoredUser || currentUser);
    };
    load();
  }, [inboxDemoEnabled, readinessDemoEnabled, requestedTab, snapshotDemoEnabled]);

  useEffect(() => {
    document.body.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    if (!captureDemoEnabled) {
      return;
    }
    setCurrentTab('add');
    setPreviewDraft({
      compositionId: 'demo-preview',
      rawNote: 'Voice capture: invoice for Brookside Renovations, GBP 480 labour, standard VAT.',
      preview: {
        confidence_indicator: 'medium',
      },
    });
    setPreviewForm({
      entityType: 'invoice',
      counterparty: 'Brookside Renovations',
      grossAmount: '480.00',
      netAmount: '400.00',
      vatAmount: '80.00',
      vatRate: '20',
      category: 'labour',
      relevantDate: '2026-03-11',
      note: 'Voice capture: invoice for Brookside Renovations, GBP 480 labour, standard VAT.',
    });
  }, [captureDemoEnabled]);

  useEffect(() => {
    if (commandCentreDemoEnabled && !captureDemoEnabled) {
      setCurrentTab(requestedTab || 'control');
    }
  }, [captureDemoEnabled, commandCentreDemoEnabled, requestedTab]);

  useEffect(() => {
    if (readinessDemoEnabled || snapshotDemoEnabled || inboxDemoEnabled) {
      setCurrentTab(requestedTab || (inboxDemoEnabled ? 'inbox' : 'quarter'));
    }
  }, [inboxDemoEnabled, readinessDemoEnabled, requestedTab, snapshotDemoEnabled]);

  useEffect(() => {
    if (!snapshotWorkspace?.snapshots?.length) {
      setSelectedSnapshotId(null);
      return;
    }
    const matchedSnapshot = snapshotWorkspace.snapshots.find((snapshot) => snapshot.snapshot_id === selectedSnapshotId);
    if (!matchedSnapshot) {
      setSelectedSnapshotId(snapshotWorkspace.snapshots[0].snapshot_id);
    }
  }, [selectedSnapshotId, snapshotWorkspace]);

  const loadQuarterWorkspace = async (readinessReport = null) => {
    if (snapshotDemoEnabled || readinessDemoEnabled || inboxDemoEnabled) {
      return buildDemoSnapshotWorkspace();
    }

    const quarterReference = readinessReport?.quarter_reference || 'Q1-2026';
    const [snapshotStatusResponse, historyResponse] = await Promise.all([
      axios.get(`${API_BASE_URL}/business-events/quarters/${quarterReference}/snapshot-status`).catch(() => ({ data: null })),
      axios.get(`${API_BASE_URL}/business-events`, {
        params: {
          quarter_reference: quarterReference,
          limit: 25
        }
      }).catch(() => ({ data: [] }))
    ]);

    return buildSnapshotWorkspaceFromApi(
      snapshotStatusResponse.data,
      Array.isArray(historyResponse.data) ? historyResponse.data : [],
      readinessReport
    );
  };

  const fetchAllData = async (activeUser = currentUser) => {
    try {
      axios.defaults.headers.common['X-User-ID'] = activeUser.id;
      const inboxLoadStartedAt = typeof performance !== 'undefined' && typeof performance.now === 'function'
        ? performance.now()
        : Date.now();
      const endpoints = [
        'items',
        'upcoming',
        'stats/summary',
        'upcoming/notifications',
        'stats/momentum',
        'insights',
        'clients',
        'jobs',
        'calendar',
        'diary',
        'inbox/finish-now',
        `inbox/readiness?period_start=${quarterStart}&period_end=${quarterEnd}`,
      ];
      const responses = await Promise.all(
        endpoints.map((endpoint) => axios.get(`${API_BASE_URL}/${endpoint}`).catch(() => ({ data: [] }))),
      );
      const inboxLoadFinishedAt = typeof performance !== 'undefined' && typeof performance.now === 'function'
        ? performance.now()
        : Date.now();
      setItems(Array.isArray(responses[0].data) ? responses[0].data : []);
      setUpcomingItems(Array.isArray(responses[1].data) ? responses[1].data : []);
      setNotifications(Array.isArray(responses[3].data) ? responses[3].data : []);
      setMomentum(responses[4].data || null);
      setInsights(Array.isArray(responses[5].data) ? responses[5].data : []);
      setClients(Array.isArray(responses[6].data) ? responses[6].data : []);
      setJobs(Array.isArray(responses[7].data) ? responses[7].data : []);
      setCalendarEvents(Array.isArray(responses[8].data) ? responses[8].data : []);
      setDiaryEntries(Array.isArray(responses[9].data) ? responses[9].data : []);
      setInboxItems(Array.isArray(responses[10].data) ? responses[10].data : []);
      setQuarterReadiness(responses[11].data || null);
      setInboxLoadMs(Math.round(inboxLoadFinishedAt - inboxLoadStartedAt));
      const nextWorkspace = await loadQuarterWorkspace(responses[11].data || null);
      setSnapshotWorkspace(nextWorkspace);

      if (!MVP_QUARTERLY_EXPORT_MODE) {
        const taxResponse = await axios.get(`${API_BASE_URL}/tax/vat-summary`).catch(() => ({ data: null }));
        setVatSummary(taxResponse.data);
      } else {
        setVatSummary(null);
      }
      setConnectionError(null);
    } catch (error) {
      setConnectionError('Disconnected');
    } finally {
      setLoading(false);
    }
  };

  const quarterUiState = buildQuarterUiState({
    report: quarterReadiness || READINESS_DEMO_REPORT,
    fallbackIssues: inboxItems,
    resolvedIssueIds: resolvedQuarterIssueIds,
  });
  const activeQuarterReport = quarterUiState.report || READINESS_DEMO_REPORT;
  const activeFinishNowQueue = quarterUiState.activeIssues;

  const resolveQuarterIssue = (issueId) => {
    if (!issueId || (!readinessDemoEnabled && !snapshotDemoEnabled)) {
      return;
    }

    setResolvedQuarterIssueIds((previous) => (
      previous.includes(issueId) ? previous : [...previous, issueId]
    ));
    setQuarterActionMessage(`Blocker ${issueId} cleared in demo mode. Export state updated immediately.`);
    setQuarterActionError('');
  };

  const toggleTheme = async () => {
    const nextTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(nextTheme);
    await Preferences.set({ key: 'theme', value: nextTheme });
  };

  const dismissInsight = (id) => setInsights((previous) => previous.filter((insight) => insight.id !== id));
  const inboxCards = buildInboxCards(activeFinishNowQueue, activeQuarterReport);
  const activeVoiceCard = findVoiceContextCard(inboxCards, activeVoiceContextId);
  const filteredInboxCards = inboxCards.filter((card) => inboxFilter === 'all' || card.issue_types.includes(inboxFilter));
  const highSeverityCount = inboxCards.filter((card) => card.severity === 'high').length;
  const readyToExportCount = Math.max(0, (activeQuarterReport?.total_txns_in_period || READINESS_DEMO_REPORT.total_txns_in_period) - inboxCards.length);

  const applyVoiceMicroDecisionLocally = (card, parsedCommand, responseLike = {}) => {
    if (!card || !parsedCommand) {
      return;
    }

    const nextDraft = applyInboxVoiceCommandToDraft(inboxDrafts[card.id] || buildInboxDraft(card), parsedCommand);
    setInboxDrafts((previous) => ({
      ...previous,
      [card.id]: nextDraft,
    }));

    if (parsedCommand.type === 'category') {
      syncInboxCardLocally(card.id, {
        category_code: nextDraft.category_code,
        category_name: nextDraft.category_name,
      });
    } else if (parsedCommand.type === 'business_personal') {
      syncInboxCardLocally(card.id, {
        business_personal: nextDraft.business_personal,
        is_split: false,
        split_business_pct: null,
      });
    } else if (parsedCommand.type === 'split') {
      syncInboxCardLocally(card.id, {
        business_personal: 'BUSINESS',
        is_split: true,
        split_business_pct: Number(parsedCommand.split_business_pct),
      });
    }

    setVoiceMicroDecisionChip((previous) => reduceVoiceMicroDecisionChip(previous, {
      ...responseLike,
      action_status: responseLike.action_status || 'execute',
      confirmation_chip: responseLike.confirmation_chip || parsedCommand.confirmation_chip,
      applied_actions: responseLike.applied_actions || [{ label: parsedCommand.confirmation_chip.replace(/^Applied:\s*/, '') }],
      undo: responseLike.undo || { supported: true },
    }, card));
  };

  useEffect(() => {
    if (!activeVoiceContextId) {
      return;
    }
    if (!findVoiceContextCard(inboxCards, activeVoiceContextId)) {
      setActiveVoiceContextId('');
    }
  }, [activeVoiceContextId, inboxCards]);

  useEffect(() => {
    if (!inboxDemoEnabled || !voiceDemoCommand || !activeVoiceCard) {
      return;
    }
    const seedKey = `${activeVoiceCard.id}:${voiceDemoCommand}`;
    if (voiceDemoSeedRef.current === seedKey) {
      return;
    }
    const parsedCommand = parseInboxVoiceCommand(voiceDemoCommand);
    if (!parsedCommand) {
      return;
    }
    voiceDemoSeedRef.current = seedKey;
    applyVoiceMicroDecisionLocally(activeVoiceCard, parsedCommand, {
      action_status: 'execute',
      confirmation_chip: parsedCommand.confirmation_chip,
      applied_actions: [{ label: parsedCommand.confirmation_chip.replace(/^Applied:\s*/, '') }],
      undo: { supported: true },
    });
  }, [activeVoiceCard, inboxDemoEnabled, voiceDemoCommand]);

  const currentRoleLabel = ROLE_LABELS[currentUser.role] || currentUser.role;
  const currentPermissions = getPermissionsForRole(currentUser.role);
  const canManageGovernance = hasPermission(currentUser, PERMISSIONS.GOVERNANCE_MANAGE);
  const canReadAudit = hasPermission(currentUser, PERMISSIONS.GOVERNANCE_AUDIT_READ);
  const autoCommitVisibility = buildAutoCommitVisibility(policyRecords);
  const onboardingRequired = MVP_QUARTERLY_EXPORT_MODE && authBootstrapped && !onboardingSession;
  const controlCentreSummary = buildControlCentreSummary({
    policyRecords,
    syncTelemetry,
    sessions: activeSessions,
    inboxItems: activeFinishNowQueue,
    governanceAudit,
  });

  const appendAuditEvent = (event) => {
    if (!event) {
      return;
    }
    setGovernanceAudit((previous) => [event, ...previous].slice(0, 12));
  };

  const switchUser = async (userId) => {
    const matchedUser = appUsers.find((user) => user.id === userId);
    if (!matchedUser) {
      return;
    }
    setCurrentUser(matchedUser);
    await Preferences.set({ key: 'userId', value: userId });
  };

  const completeOnboarding = async (payload) => {
    setOnboardingBusy(true);
    setOnboardingError('');
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/signup`, payload, {
        headers: {
          'Content-Type': 'application/json',
          'bypass-tunnel-reminder': 'true',
        },
      });
      const session = normalizeOnboardingSession(response.data);
      const appUser = createAppUserFromSession(session, TENANT_ID);
      await Preferences.set({ key: 'userId', value: appUser.id });
      setOnboardingSession(session);
      setAppUsers((previous) => mergeUserIntoList(previous, appUser));
      setCurrentUser(appUser);
      setCurrentTab('home');
      setLoading(false);
      setConnectionError(null);
      await fetchAllData(appUser);
    } catch (error) {
      const message = error?.response?.data?.error || 'Unable to create your account right now.';
      setOnboardingError(message);
    } finally {
      setOnboardingBusy(false);
    }
  };

  const applyTenantPolicyChange = ({ policyKey, policyValue, reason }) => {
    const outcome = applyPolicyUpdate({
      records: policyRecords,
      tenantId: currentUser.tenant_id,
      actor: currentUser,
      policyKey,
      policyValue,
      reason,
      onAudit: appendAuditEvent,
    });

    if (!outcome.allowed) {
      alert(outcome.reason);
      return false;
    }

    setPolicyRecords(outcome.records);
    return true;
  };

  const setManualField = (field, value) => {
    setManualForm((previous) => ({ ...previous, [field]: value }));
  };

  const resetManualCapture = (nextType = manualForm.type) => {
    setManualForm({ ...DEFAULT_MANUAL_FORM, type: nextType, relevantDate: getTodayForInput() });
    setPreviewDraft(null);
    setPreviewForm(null);
    setPreviewMode('review');
    setPreviewError('');
  };

  const setPreviewField = (field, value) => {
    setPreviewForm((previous) => ({ ...previous, [field]: value }));
  };

  const setInboxDraftField = (itemId, field, value) => {
    setInboxDrafts((previous) => {
      const baseCard = inboxCards.find((card) => card.id === itemId);
      const currentDraft = previous[itemId] || (baseCard ? buildInboxDraft(baseCard) : buildInboxDraft({}));
      const nextDraft = { ...currentDraft, [field]: value };
      if (field === 'business_personal' && value !== 'SPLIT') {
        nextDraft.is_split = false;
        nextDraft.split_business_pct = '';
      }
      return { ...previous, [itemId]: nextDraft };
    });
  };

  const clearInboxMessage = () => setInboxMessage(null);

  const syncInboxCardLocally = (itemId, updates = {}) => {
    setInboxItems((previous) => previous
      .map((item) => {
        const currentId = String(item.affected_entity_id || item.id || '');
        if (currentId !== String(itemId)) {
          return item;
        }
        return { ...item, ...updates };
      })
      .filter((item) => {
        const currentId = String(item.affected_entity_id || item.id || '');
        if (currentId !== String(itemId)) {
          return true;
        }
        const nextIssueType = item.issue_type || item.blocker_reason;
        if (nextIssueType === 'missing_category') {
          return !updates.category_code;
        }
        if (nextIssueType === 'missing_business_personal') {
          return !updates.business_personal;
        }
        if (nextIssueType === 'missing_split_pct') {
          return !(updates.is_split === true && (updates.split_business_pct === null || updates.split_business_pct === undefined || updates.split_business_pct === ''));
        }
        if (nextIssueType === 'unresolved_duplicate') {
          return !updates.duplicate_resolution;
        }
        return true;
      }));

    setQuarterReadiness((previous) => {
      if (!previous) {
        return previous;
      }
      const nextIssueList = (previous.issue_list || []).filter((issue) => {
        if (String(issue.affected_entity_id) !== String(itemId)) {
          return true;
        }
        if (issue.issue_type === 'missing_category') {
          return !updates.category_code;
        }
        if (issue.issue_type === 'missing_business_personal') {
          return !updates.business_personal;
        }
        if (issue.issue_type === 'missing_split_pct') {
          return !(updates.is_split === true && (updates.split_business_pct === null || updates.split_business_pct === undefined || updates.split_business_pct === ''));
        }
        if (issue.issue_type === 'unresolved_duplicate') {
          return !updates.duplicate_resolution;
        }
        return true;
      });
      return {
        ...previous,
        issue_list: nextIssueList,
        blocking_txns_count: new Set(nextIssueList.map((issue) => issue.affected_entity_id)).size,
      };
    });
  };

  const applySuggestedInboxCategory = (card) => {
    const suggestion = card.suggested_category || {};
    if (!suggestion.category_code && !suggestion.category_name) {
      setInboxMessage({ type: 'error', text: `No suggested category is available for ${card.merchant}.` });
      return;
    }
    setInboxDrafts((previous) => ({
      ...previous,
      [card.id]: {
        ...(previous[card.id] || buildInboxDraft(card)),
        category_code: suggestion.category_code || '',
        category_name: suggestion.category_name || '',
      },
    }));
    setInboxMessage({ type: 'success', text: `Suggested category applied for ${card.merchant}.` });
  };

  const undoLastInboxAction = async () => {
    clearInboxMessage();
    try {
      setInboxBusyId('undo-last');
      setVoiceMicroDecisionChip(null);
      if (inboxDemoEnabled || readinessDemoEnabled || snapshotDemoEnabled) {
        setInboxItems(READINESS_DEMO_REPORT.issue_list);
        setQuarterReadiness(READINESS_DEMO_REPORT);
        setInboxDrafts({});
        setVoiceMicroDecisionChip(null);
        setInboxMessage({ type: 'success', text: 'Demo queue reset to the original blocker set.' });
        return;
      }
      await axios.post(`${API_BASE_URL}/inbox/undo-last`);
      await fetchAllData();
      setVoiceMicroDecisionChip(null);
      setInboxMessage({ type: 'success', text: 'Last triage action undone.' });
    } catch (error) {
      setInboxMessage({ type: 'error', text: error?.response?.data?.error || 'Unable to undo the last triage action.' });
    } finally {
      setInboxBusyId('');
    }
  };

  const submitInboxAction = async (card) => {
    clearInboxMessage();
    const draft = inboxDrafts[card.id] || buildInboxDraft(card);
    const shouldClassify = card.supports_category || card.supports_business_personal || card.supports_split;
    const shouldResolveDuplicate = card.supports_duplicate;
    const isSplit = draft.business_personal === 'SPLIT' || draft.is_split;
    const splitPctValue = draft.split_business_pct === '' ? null : Number(draft.split_business_pct);
    if (card.supports_category && !draft.category_code.trim()) {
      setInboxMessage({ type: 'error', text: `Add a category for ${card.merchant} before saving.` });
      return;
    }
    if (card.supports_business_personal && !draft.business_personal) {
      setInboxMessage({ type: 'error', text: `Choose business or personal for ${card.merchant}.` });
      return;
    }
    if ((card.supports_split || isSplit) && !Number.isFinite(splitPctValue)) {
      setInboxMessage({ type: 'error', text: `Enter a split percentage for ${card.merchant}.` });
      return;
    }
    if ((card.supports_split || isSplit) && (splitPctValue < 0 || splitPctValue > 100)) {
      setInboxMessage({ type: 'error', text: 'Split percentage must be between 0 and 100.' });
      return;
    }
    if (card.supports_duplicate && draft.duplicate_action === 'merge' && !draft.duplicate_of_txn_id.trim()) {
      setInboxMessage({ type: 'error', text: `Enter the target transaction id to merge ${card.merchant}.` });
      return;
    }

    try {
      setInboxBusyId(card.id);
      if (shouldClassify) {
        const classificationPayload = {
          category_code: draft.category_code.trim() || null,
          category_name: draft.category_name.trim() || null,
          business_personal: draft.business_personal === 'SPLIT' ? 'BUSINESS' : (draft.business_personal || null),
          is_split: Boolean(isSplit),
          split_business_pct: isSplit ? splitPctValue : null,
          source: inboxDemoEnabled || readinessDemoEnabled || snapshotDemoEnabled ? 'demo' : 'manual',
        };
        if (!(inboxDemoEnabled || readinessDemoEnabled || snapshotDemoEnabled)) {
          await axios.patch(`${API_BASE_URL}/inbox/${card.id}/classification`, classificationPayload);
        }
        syncInboxCardLocally(card.id, classificationPayload);
      }

      if (shouldResolveDuplicate) {
        const duplicatePayload = {
          action: draft.duplicate_action,
          duplicate_of_txn_id: draft.duplicate_action === 'merge' ? draft.duplicate_of_txn_id.trim() : null,
        };
        if (!(inboxDemoEnabled || readinessDemoEnabled || snapshotDemoEnabled)) {
          await axios.post(`${API_BASE_URL}/inbox/${card.id}/duplicate-resolution`, duplicatePayload);
        }
        syncInboxCardLocally(card.id, { duplicate_resolution: duplicatePayload.action });
      }

      if (!(inboxDemoEnabled || readinessDemoEnabled || snapshotDemoEnabled)) {
        await fetchAllData();
      }

      setInboxDrafts((previous) => {
        const next = { ...previous };
        delete next[card.id];
        return next;
      });
      setInboxMessage({ type: 'success', text: `${card.merchant} cleared from the finish-now queue.` });
    } catch (error) {
      setInboxMessage({ type: 'error', text: error?.response?.data?.error || `Unable to update ${card.merchant}.` });
    } finally {
      setInboxBusyId('');
    }
  };

  const toggleListening = async () => {
    if (connectionError) {
      alert('Cannot start voice capture while backend is disconnected.');
      return;
    }

    try {
      let available = false;
      try {
        const capability = await SpeechRecognition.available();
        available = !!capability?.available;
      } catch (_) {
        available = false;
      }

      if (!available) {
        const SpeechRecognitionBrowser = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognitionBrowser) {
          alert('Voice recognition is not available in this browser.');
          return;
        }
        if (!webRecognitionRef.current) {
          const recognition = new SpeechRecognitionBrowser();
          recognition.lang = 'en-GB';
          recognition.interimResults = false;
          recognition.continuous = false;
          recognition.onresult = (event) => {
            const spokenText = event?.results?.[0]?.[0]?.transcript || '';
            finalTranscriptRef.current = spokenText;
            setTranscript(spokenText);
            if (spokenText.trim()) {
              handleVoiceProcess(spokenText);
            }
          };
          recognition.onend = () => {
            setIsListening(false);
            setVoiceStatus((previous) => (previous === 'processing' ? previous : 'idle'));
          };
          recognition.onerror = () => {
            setIsListening(false);
            setVoiceStatus('idle');
          };
          webRecognitionRef.current = recognition;
        }

        if (isListening) {
          setIsListening(false);
          setVoiceStatus('processing');
          webRecognitionRef.current.stop();
          if (!finalTranscriptRef.current.trim()) {
            setVoiceStatus('idle');
          }
        } else {
          setTranscript('');
          finalTranscriptRef.current = '';
          setIsListening(true);
          setVoiceStatus('listening');
          webRecognitionRef.current.start();
        }
        return;
      }

      if (isListening) {
        setIsListening(false);
        setVoiceStatus('processing');
        SpeechRecognition.stop().catch(() => {});
        const finalText = finalTranscriptRef.current.trim();
        if (finalText) {
          handleVoiceProcess(finalText);
        } else {
          setVoiceStatus('idle');
        }
      } else {
        const permissions = await SpeechRecognition.checkPermissions();
        if (permissions.speechRecognition !== 'granted') {
          await SpeechRecognition.requestPermissions();
        }
        setTranscript('');
        finalTranscriptRef.current = '';
        setIsListening(true);
        setVoiceStatus('listening');
        const result = await SpeechRecognition.start({ language: 'en-GB', popup: true });
        if (result?.matches?.length > 0) {
          handleVoiceProcess(result.matches[0]);
        } else {
          setIsListening(false);
          setVoiceStatus('idle');
        }
      }
    } catch (error) {
      setIsListening(false);
      setVoiceStatus('idle');
    }
  };

  const handleVoiceProcess = async (text) => {
    const cleanText = text.replace(/┬ú/g, 'GBP ');
    try {
      setVoiceStatus('processing');
      const microDecisionRequest = buildVoiceMicroDecisionRequest({
        currentTab,
        transcript: cleanText,
        activeVoiceContextId,
        inboxCards,
      });

      if (microDecisionRequest?.error) {
        setInboxMessage({ type: 'error', text: microDecisionRequest.error });
        setCurrentTab('inbox');
        return;
      }

      let response;
      if (microDecisionRequest) {
        if (inboxDemoEnabled || readinessDemoEnabled || snapshotDemoEnabled) {
          const parsedCommand = parseInboxVoiceCommand(cleanText);
          if (!parsedCommand) {
            throw new Error('Only Category, Business, Personal, and Split {n}% are available in the local voice triage demo.');
          }
          applyVoiceMicroDecisionLocally(microDecisionRequest.card, parsedCommand, {
            action_status: 'execute',
            confirmation_chip: parsedCommand.confirmation_chip,
            applied_actions: [{ label: parsedCommand.confirmation_chip.replace(/^Applied:\s*/, '') }],
            undo: { supported: true },
          });
          response = { data: buildInboxVoiceChip({
            action_status: 'execute',
            confirmation_chip: parsedCommand.confirmation_chip,
            undoable: true,
            bank_txn_id: microDecisionRequest.card.id,
          }, microDecisionRequest.card) };
          response.data.confirmation_chip = parsedCommand.confirmation_chip;
        } else {
          response = await axios.post(`${API_BASE_URL}${microDecisionRequest.endpoint}`, microDecisionRequest.payload);
        }
      } else {
        response = await axios.post(`${API_BASE_URL}/voice/process`, {
          transcript: cleanText,
          device_id: 'mobile-v139',
          current_date: new Date().toISOString(),
        });
      }
      const spokenConfirmation = response.data.confirmation_chip || response.data.confirmation_text;
      if (spokenConfirmation && window.SpeechSynthesisUtterance) {
        try {
          const utterance = new window.SpeechSynthesisUtterance(spokenConfirmation);
          window.speechSynthesis.speak(utterance);
        } catch (_) {
        }
      }
      if (microDecisionRequest) {
        if (!(inboxDemoEnabled || readinessDemoEnabled || snapshotDemoEnabled)) {
          setVoiceMicroDecisionChip((previous) => reduceVoiceMicroDecisionChip(previous, response.data, microDecisionRequest.card));
        }
        setInboxMessage({
          type: 'success',
          text: response.data.confirmation_chip || 'Voice triage action applied.',
        });
      } else {
        executeVoiceAction(response.data);
      }
      if (!(microDecisionRequest && (inboxDemoEnabled || readinessDemoEnabled || snapshotDemoEnabled))) {
        await fetchAllData();
      }
    } catch (error) {
      const message = error?.response?.data?.error || error?.message || 'AI Error';
      if (currentTab === 'inbox' || currentTab === 'quarter') {
        setInboxMessage({ type: 'error', text: message });
      } else {
        alert(message);
      }
    } finally {
      setVoiceStatus('idle');
      setIsListening(false);
    }
  };

  const openActivityView = ({ type = null, search = '', client = '', date = '', timePeriod = null } = {}) => {
    setCurrentTab('activity');
    setActivityTypeFilter(type);
    setSearchQuery(search);
    setActivityClientFilter(client);
    setActivityDateFilter(date);
    setTimePeriodFilter(timePeriod);
  };

  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
    setCurrentTab('quotes');
    setActivityTypeFilter(null);
    setSearchQuery(search);
    setActivityClientFilter(client);
    setActivityDateFilter(date);
    setTimePeriodFilter(timePeriod);
  };

  const executeVoiceAction = (data) => {
    const { intent, slots = {} } = data || {};
    const nextTimePeriod = resolveVoiceTimePeriod(slots);
    const nextDate = resolveVoiceDateFilter(slots);
    const nextClient = slots.client_name || '';
    switch (intent) {
      case 'go_home':
        setCurrentTab('home');
        break;
      case 'view_expenses':
        openActivityView({
          type: 'receipt',
          client: nextClient,
          date: nextDate,
          timePeriod: nextTimePeriod,
        });
        break;
      case 'view_invoices':
        openActivityView({
          type: 'invoice',
          client: nextClient,
          date: nextDate,
          timePeriod: nextTimePeriod,
        });
        break;
      case 'view_quotes':
        openQuotesView({
          client: nextClient,
          date: nextDate,
          timePeriod: nextTimePeriod,
        });
        break;
      case 'view_vat':
        setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
        break;
      case 'view_bookings':
        setCurrentTab('calendar');
        break;
      default:
        break;
    }
  };

  const getDateGroupStateKey = (sectionKey, dateKey) => `${sectionKey}:${dateKey}`;

  const isDateGroupExpanded = (sectionKey, dateKey) => Boolean(
    expandedDateGroups[getDateGroupStateKey(sectionKey, dateKey)]
  );

  const toggleDateGroup = (sectionKey, dateKey) => {
    const stateKey = getDateGroupStateKey(sectionKey, dateKey);
    setExpandedDateGroups((previous) => ({
      ...previous,
      [stateKey]: !previous[stateKey],
    }));
  };

  const setDateGroupsExpandedState = (sectionKey, groups, expanded) => {
    setExpandedDateGroups((previous) => {
      const nextState = { ...previous };
      groups.forEach((group) => {
        nextState[getDateGroupStateKey(sectionKey, group.dateKey)] = expanded;
      });
      return nextState;
    });
  };

  const renderDateGroupedSection = ({
    title,
    sectionKey,
    groups,
    emptyTitle,
    emptyDescription,
    renderItem,
  }) => {
    if (groups.length === 0) {
      return (
        <section className="grouped-section">
          <div className="grouped-section-header">
            <h5>{title}</h5>
          </div>
          <div className="empty-panel">
            <h5>{emptyTitle}</h5>
            <p className="small-muted mb-0">{emptyDescription}</p>
          </div>
        </section>
      );
    }

    return (
      <section className="grouped-section">
        <div className="grouped-section-header">
          <h5>{title}</h5>
          <div className="group-toggle-actions">
            <button
              type="button"
              className="group-toggle-btn"
              onClick={() => setDateGroupsExpandedState(sectionKey, groups, true)}
            >
              Expand All
            </button>
            <button
              type="button"
              className="group-toggle-btn"
              onClick={() => setDateGroupsExpandedState(sectionKey, groups, false)}
            >
              Collapse All
            </button>
          </div>
        </div>
        {groups.map((group) => {
          const expanded = isDateGroupExpanded(sectionKey, group.dateKey);
          return (
            <div key={`${sectionKey}-${group.dateKey}`} className="date-group-shell">
              <button
                type="button"
                className="date-group-header"
                onClick={() => toggleDateGroup(sectionKey, group.dateKey)}
              >
                <span className="date-group-header-meta">
                  <span>{group.dateLabel}</span>
                  <span className="date-group-count">
                    {group.items.length} item{group.items.length === 1 ? '' : 's'}
                  </span>
                </span>
                {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
              </button>
              {expanded && (
                <div className="date-group-body">
                  {group.items.map((item) => renderItem(item))}
                </div>
              )}
            </div>
          );
        })}
      </section>
    );
  };

  const submitManualEntry = async () => {
    if (manualSaving) {
      return;
    }
    if (!manualForm.note.trim() && !manualForm.counterparty.trim()) {
      setPreviewError('Add a short description or counterparty before saving.');
      return;
    }
    if (isMonetaryType(manualForm.type) && !manualForm.grossAmount) {
      setPreviewError('Gross amount is required for monetary preview.');
      return;
    }

    try {
      setManualSaving(true);
      setPreviewError('');
      const payload = buildManualPayload(manualForm);
      const response = await axios.post(`${API_BASE_URL}/items`, payload);

      if (response.data?.action_status === 'preview_required') {
        setPreviewDraft({
          compositionId: response.data.composition_id,
          preview: response.data.preview,
          rawNote: manualForm.note.trim(),
        });
        setPreviewForm(buildPreviewForm(response.data.preview, manualForm.note.trim()));
        setPreviewMode('review');
        return;
      }

      resetManualCapture(manualForm.type);
      await fetchAllData();
      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
      alert(`${manualForm.type} saved.`);
    } catch (error) {
      setPreviewError(error.response?.data?.error || 'Failed to save item.');
    } finally {
      setManualSaving(false);
    }
  };

  const confirmPreviewDraft = async () => {
    if (!previewDraft?.compositionId || !previewForm || previewBusy) {
      return;
    }

    try {
      setPreviewBusy(true);
      setPreviewError('');
      const updatePayload = {
        source_type: 'manual',
        client_name: previewForm.counterparty.trim() || null,
        gross_amount: previewForm.grossAmount === '' ? null : Number(previewForm.grossAmount),
        amount: previewForm.grossAmount === '' ? null : Number(previewForm.grossAmount),
        net_amount: previewForm.netAmount === '' ? null : Number(previewForm.netAmount),
        vat_amount: previewForm.vatAmount === '' ? null : Number(previewForm.vatAmount),
        vat_rate: previewForm.vatRate === '' ? null : Number(previewForm.vatRate),
        transaction_date: previewForm.relevantDate || null,
        due_date: previewForm.entityType === 'invoice' ? previewForm.relevantDate || null : null,
        extracted_text: previewForm.note.trim() || `${previewForm.entityType} entry`,
        raw_note: previewForm.note.trim() || `${previewForm.entityType} entry`,
        labels: previewForm.category.trim() ? [previewForm.category.trim()] : [],
      };
      await axios.post(`${API_BASE_URL}/items/${previewDraft.compositionId}/confirm`, updatePayload);
      const nextType = previewForm.entityType || manualForm.type;
      resetManualCapture(nextType);
      await fetchAllData();
      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
      alert(`${nextType} confirmed.`);
    } catch (error) {
      setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
    } finally {
      setPreviewBusy(false);
    }
  };

  const cancelPreviewDraft = async () => {
    if (!previewDraft?.compositionId || previewBusy) {
      return;
    }

    try {
      setPreviewBusy(true);
      setPreviewError('');
      await axios.delete(`${API_BASE_URL}/items/${previewDraft.compositionId}`);
      resetManualCapture(manualForm.type);
      await fetchAllData();
    } catch (error) {
      setPreviewError(error.response?.data?.error || 'Failed to cancel draft.');
    } finally {
      setPreviewBusy(false);
    }
  };

  const renderDashboard = () => {
    const demoMomentum = commandCentreDemoEnabled
      ? {
        thisWeek: { incoming: 4820, outgoing: 1360 },
        deltas: { incoming: 18 },
      }
      : null;
    const demoReadiness = commandCentreDemoEnabled
      ? { readiness_pct: 82, blocking_txns_count: 3, can_export: false }
      : null;
    const liveIncoming = momentum?.thisWeek?.incoming ?? demoMomentum?.thisWeek?.incoming ?? 0;
    const liveOutgoing = momentum?.thisWeek?.outgoing ?? demoMomentum?.thisWeek?.outgoing ?? 0;
    const deltaIncoming = momentum?.deltas?.incoming ?? demoMomentum?.deltas?.incoming ?? 0;
    const unpaidInvoices = items.filter((item) => item.type === 'invoice' && item.payment_status !== 'paid');
    const invoiceCount = items.filter((item) => item.type === 'invoice').length;
    const receiptCount = items.filter((item) => item.type === 'receipt').length;
    const quarterPct = activeQuarterReport?.readiness_pct ?? demoReadiness?.readiness_pct ?? 0;
    const blockerCount = activeFinishNowQueue.length || activeQuarterReport?.blocking_txns_count || demoReadiness?.blocking_txns_count || 0;
    const openAttentionCount = notifications.length + upcomingItems.length + blockerCount;
    const liveVatPayable = vatSummary?.vat_boxes?.payable;

    const attentionItems = [
      ...(blockerCount > 0
        ? [{
          id: 'finish-now-blockers',
          title: `${blockerCount} item${blockerCount === 1 ? '' : 's'} blocking quarter close`,
          detail: 'Resolve coding, split, and duplicate blockers from the Finish Now queue.',
          tone: 'urgent',
          actionLabel: 'Open queue',
          action: () => setCurrentTab('inbox'),
        }]
        : []),
      ...(unpaidInvoices.length > 0
        ? [{
          id: 'unpaid-invoices',
          title: `${unpaidInvoices.length} unpaid invoice${unpaidInvoices.length === 1 ? '' : 's'} need chasing`,
          detail: 'Review invoice activity and move follow-up work forward today.',
          tone: 'watch',
          actionLabel: 'View invoices',
          action: () => openActivityView({ type: 'invoice' }),
        }]
        : []),
      ...notifications.slice(0, 2).map((notification, index) => ({
        id: notification.id || `notification-${index}`,
        title: notification.title || 'Business notification',
        detail: notification.message || notification.description || 'A new business alert needs review.',
        tone: index === 0 ? 'urgent' : 'watch',
        actionLabel: 'Review',
        action: () => setCurrentTab('inbox'),
      })),
      ...upcomingItems.slice(0, 2).map((item, index) => ({
        id: item.id || `upcoming-${index}`,
        title: item.title || item.name || 'Upcoming commitment',
        detail: item.description || item.raw_note || 'An upcoming commitment is due soon.',
        tone: 'watch',
        actionLabel: 'Open schedule',
        action: () => setCurrentTab('calendar'),
      })),
    ];

    if (attentionItems.length === 0) {
      attentionItems.push({
        id: 'all-clear',
        title: 'No critical blockers right now',
        detail: 'Use the command centre to capture fresh activity or review quarter readiness before the next run.',
        tone: 'good',
        actionLabel: 'Start capture',
        action: () => setCurrentTab('add'),
      });
    }

    const feedItems = [
      ...(insights.length > 0
        ? insights.slice(0, 4).map((insight, index) => ({
          id: insight.id || `insight-${index}`,
          tag: 'Insight',
          title: insight.title || 'Business insight',
          detail: insight.text || insight.description || 'No detail supplied.',
          dismissible: !!insight.id,
        }))
        : []),
      ...(insights.length === 0
        ? [{
          id: 'fallback-insight-revenue',
          tag: 'Signal',
          title: deltaIncoming >= 0 ? 'Revenue momentum is holding' : 'Revenue momentum slipped',
          detail: `${formatPercentDelta(deltaIncoming)}. Pair fresh capture with invoice review to keep the week on pace.`,
        }, {
          id: 'fallback-insight-quarter',
          tag: 'Quarter',
          title: `${quarterPct}% of the quarter pack is ready`,
          detail: blockerCount > 0
            ? `Clear ${blockerCount} blocker${blockerCount === 1 ? '' : 's'} to unlock a cleaner export run.`
            : 'No finish-now blockers are currently stopping the quarterly pack.',
        }]
        : []),
    ];

    const performanceCards = [
      {
        id: 'weekly-revenue',
        eyebrow: 'Weekly Revenue',
        value: formatCurrency(liveIncoming),
        note: formatPercentDelta(deltaIncoming),
        footLeft: `${invoiceCount} invoices captured`,
        footRight: 'Momentum',
        onClick: () => openActivityView({ type: 'invoice' }),
      },
      {
        id: 'expense-summary',
        eyebrow: 'Expense Summary',
        value: formatCurrency(liveOutgoing),
        note: `${receiptCount} receipt${receiptCount === 1 ? '' : 's'} logged this cycle`,
        footLeft: 'Outgoing',
        footRight: 'Receipts',
        onClick: () => openActivityView({ type: 'receipt' }),
      },
      {
        id: 'vat-summary',
        eyebrow: MVP_QUARTERLY_EXPORT_MODE ? 'Quarter Readiness' : 'VAT Summary',
        value: MVP_QUARTERLY_EXPORT_MODE ? `${quarterPct}% ready` : formatCurrency(liveVatPayable, 2),
        note: MVP_QUARTERLY_EXPORT_MODE
          ? `${blockerCount} blocker${blockerCount === 1 ? '' : 's'} left before export`
          : 'Estimated VAT payable from the current ledger snapshot',
        footLeft: MVP_QUARTERLY_EXPORT_MODE ? 'Quarter pack' : 'HMRC prep',
        footRight: MVP_QUARTERLY_EXPORT_MODE ? 'Export mode' : 'Tax',
        onClick: () => setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'quarter' : 'tax'),
      },
      {
        id: 'attention-count',
        eyebrow: 'Needs Attention',
        value: `${openAttentionCount}`,
        note: attentionItems[0]?.title || 'No issues logged',
        footLeft: `${calendarEvents.length} booking${calendarEvents.length === 1 ? '' : 's'} scheduled`,
        footRight: `${clients.length} client${clients.length === 1 ? '' : 's'}`,
        onClick: () => setCurrentTab('calendar'),
      },
    ];

    return (
      <div className="command-centre">
        <div className="command-shell">
          <section className="command-hero">
            <div className="command-kicker">
              <Flame size={14} />
              Homepage Command Centre
            </div>
            <h3>What needs attention today is now in one place.</h3>
            <p>
              Weekly revenue, blockers, quarter readiness, and fresh insights are surfaced here first so the next action is obvious.
            </p>
            <div className="hero-metrics">
              <div className="hero-metric">
                <small>Weekly revenue</small>
                <strong>{formatCurrency(liveIncoming)}</strong>
              </div>
              <div className="hero-metric">
                <small>Period delta</small>
                <strong>{formatPercentDelta(deltaIncoming)}</strong>
              </div>
              <div className="hero-metric">
                <small>Today&apos;s blockers</small>
                <strong>{blockerCount}</strong>
              </div>
            </div>
            <div className="hero-actions">
              <button className="hero-action-main" onClick={() => setCurrentTab('add')}>
                <Plus size={18} />
                Central capture action
              </button>
              <button className="hero-action-secondary" onClick={() => setCurrentTab('quarter')}>
                Quarter status
                <ArrowRight size={16} />
              </button>
            </div>
          </section>

          <aside className="command-rail">
            <div className="command-card">
              <h5 style={{ marginBottom: 12 }}>Today&apos;s Operating Snapshot</h5>
              <div className="mini-stat-grid">
                <div className="mini-stat">
                  <small>Expense summary</small>
                  <strong>{formatCurrency(liveOutgoing)}</strong>
                </div>
                <div className="mini-stat">
                  <small>VAT / readiness</small>
                  <strong>{MVP_QUARTERLY_EXPORT_MODE ? `${quarterPct}%` : formatCurrency(liveVatPayable, 2)}</strong>
                </div>
                <div className="mini-stat">
                  <small>Notifications</small>
                  <strong>{notifications.length + upcomingItems.length}</strong>
                </div>
                <div className="mini-stat">
                  <small>Capture queue</small>
                  <strong>{items.length}</strong>
                </div>
              </div>
            </div>

            <div className="command-card">
              <h5 style={{ marginBottom: 8 }}>Capture First</h5>
              <p className="small-muted" style={{ marginBottom: 12 }}>
                The homepage is designed to push directly into capture when the business context is clear.
              </p>
              <button className="primary-action" onClick={() => setCurrentTab('add')}>
                <Wallet size={16} />
                Open capture workspace
              </button>
            </div>
          </aside>
        </div>

        <section className="command-card">
          <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-2">
            <div>
              <h5 style={{ marginBottom: 4 }}>Attention Required</h5>
              <small className="small-muted">The homepage should answer this question first.</small>
            </div>
            <div className="status-pill">{openAttentionCount} live items</div>
          </div>
          <div className="attention-list">
            {attentionItems.map((item) => (
              <div key={item.id} className="attention-row">
                <div className={`attention-icon ${item.tone}`}>
                  {item.tone === 'urgent' ? <TriangleAlert size={18} /> : item.tone === 'good' ? <CheckCircle2 size={18} /> : <Bell size={18} />}
                </div>
                <div>
                  <strong>{item.title}</strong>
                  <small>{item.detail}</small>
                </div>
                <button className="attention-action" onClick={item.action}>{item.actionLabel}</button>
              </div>
            ))}
          </div>
        </section>

        <section>
          <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-2">
            <div>
              <h5 style={{ marginBottom: 4 }}>Performance Grid</h5>
              <small className="small-muted">Compact metrics for momentum, cash, readiness, and workload.</small>
            </div>
          </div>
          <div className="performance-grid">
            {performanceCards.map((card) => (
              <button
                key={card.id}
                type="button"
                className="performance-card text-start"
                onClick={card.onClick}
                style={{ cursor: 'pointer' }}
              >
                <div>
                  <small>{card.eyebrow}</small>
                  <strong>{card.value}</strong>
                  <div className="small-muted">{card.note}</div>
                  {card.id === 'vat-summary' && MVP_QUARTERLY_EXPORT_MODE ? (
                    <div className="progress-shell">
                      <div className="progress-bar" style={{ width: `${Math.max(0, Math.min(100, quarterPct))}%` }} />
                    </div>
                  ) : null}
                </div>
                <div className="performance-foot">
                  <span>{card.footLeft}</span>
                  <span>{card.footRight}</span>
                </div>
              </button>
            ))}
          </div>
        </section>

        <section className="command-card">
          <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-2">
            <div>
              <h5 style={{ marginBottom: 4 }}>Smart Insight Feed</h5>
              <small className="small-muted">Fast reads that help the operator decide the next move.</small>
            </div>
          </div>
          <div className="insight-feed">
            {feedItems.map((feedItem) => (
              <div key={feedItem.id} className="feed-row">
                <div className="attention-icon good">
                  <Flame size={18} />
                </div>
                <div>
                  <div className="feed-tag">{feedItem.tag}</div>
                  <strong style={{ marginTop: 8 }}>{feedItem.title}</strong>
                  <small>{feedItem.detail}</small>
                </div>
                {feedItem.dismissible ? (
                  <button className="attention-action" onClick={() => dismissInsight(feedItem.id)}>Dismiss</button>
                ) : (
                  <button className="attention-action" onClick={() => setCurrentTab('quarter')}>Open</button>
                )}
              </div>
            ))}
          </div>
        </section>
      </div>
    );
  };

  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
    const searchedItems = searchQuery.trim()
      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
      : sourceItems;
    const clientFilteredItems = activityClientFilter.trim()
      ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
      : searchedItems;
    const typeFilteredItems = typeFilter
      ? clientFilteredItems.filter((item) => item.type === typeFilter)
      : clientFilteredItems;
    const exactDateFilteredItems = activityDateFilter
      ? typeFilteredItems.filter((item) => {
        const itemDate = getActivityItemDate(item);
        return itemDate && itemDate.toISOString().slice(0, 10) === activityDateFilter;
      })
      : typeFilteredItems;
    const filteredItems = timePeriodFilter
      ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
      : exactDateFilteredItems;
    return filteredItems;
  };

  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
    const groups = buildGroupedDateCollections(filteredItems, getActivityItemDate, 'desc');

    return (
      <div>
        <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
          <h4>{title}</h4>
          <div className="d-flex flex-wrap gap-2">
            <select
              className="form-select"
              style={{ maxWidth: 180 }}
              value={timePeriodFilter || ''}
              onChange={(event) => {
                const nextValue = event.target.value || null;
                setTimePeriodFilter(nextValue);
                if (nextValue) {
                  setActivityDateFilter('');
                }
              }}
            >
              {ACTIVITY_TIME_PERIOD_OPTIONS.map((option) => (
                <option key={option.value || 'all'} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <input
              className="form-control"
              style={{ maxWidth: 180 }}
              type="date"
              value={activityDateFilter}
              onChange={(event) => {
                const nextValue = event.target.value;
                setActivityDateFilter(nextValue);
                if (nextValue) {
                  setTimePeriodFilter(null);
                }
              }}
            />
            <input
              className="form-control"
              style={{ maxWidth: 220 }}
              placeholder="Filter client"
              value={activityClientFilter}
              onChange={(event) => setActivityClientFilter(event.target.value)}
            />
            <input
              className="form-control"
              style={{ maxWidth: 280 }}
              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
            />
          </div>
        </div>
        {renderDateGroupedSection({
          title,
          sectionKey: `activity-${typeFilter || 'all'}`,
          groups,
          emptyTitle,
          emptyDescription: emptyMessage,
          renderItem: (item) => (
            <div key={item.id} className="attention-item">
              <div>
                <b style={{ textTransform: 'capitalize' }}>{item.type}</b>
                <br />
                <small>{item.extracted_text || item.raw_note || item.type}</small>
                <br />
                <small className="small-muted">
                  {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                </small>
              </div>
            </div>
          ),
        })}
      </div>
    );
  };

  const renderActivity = () => {
    const timelineItems = items.filter((item) => item.type !== 'quote');

    return renderActivityList({
      title: activityTypeFilter || 'Activity',
      sourceItems: timelineItems,
      typeFilter: activityTypeFilter,
      emptyTitle: 'No matching activity',
      emptyMessage: 'Try clearing the client search or switching the date range filter.',
    });
  };

  const renderQuotes = () => {
    const quoteItems = items.filter((item) => item.type === 'quote');
    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);

    return (
      <div>
        <section className="momentum-bar">
          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
            <div>
              <div className="command-kicker">
                <FileText size={14} />
                Dedicated quotes view
              </div>
              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
              <div style={{ opacity: 0.84 }}>
                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
              </div>
            </div>
            <div>
              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
              <small>{currencyValue(quoteValue)} total quoted</small>
            </div>
          </div>
        </section>
        {renderActivityList({
          title: 'Quote activity',
          sourceItems: quoteItems,
          typeFilter: null,
          emptyTitle: 'No matching quotes',
          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
        })}
      </div>
    );
  };

  const renderCalendar = () => {
    const bookingGroups = buildGroupedDateCollections(
      calendarEvents,
      (event) => {
        const parsedDate = new Date(event.start_at);
        return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
      },
      'asc',
    );
    const openJobGroups = buildGroupedDateCollections(jobs.filter(isOpenJob), getJobDate, 'asc');

    return (
      <div>
        <h4>Schedule</h4>
        {renderDateGroupedSection({
          title: 'Bookings',
          sectionKey: 'schedule-bookings',
          groups: bookingGroups,
          emptyTitle: 'No bookings scheduled',
          emptyDescription: 'New bookings will appear here under their scheduled dates.',
          renderItem: (event) => (
            <div key={event.id} className="attention-item">
              <div>
                <b>{event.title || 'Booking'}</b>
                <br />
                <small>{event.client_name || event.event_type || 'No client assigned'}</small>
                <br />
                <small className="small-muted">{toDisplayTimestamp(event.start_at)}</small>
              </div>
            </div>
          ),
        })}
        {renderDateGroupedSection({
          title: 'Open Jobs',
          sectionKey: 'schedule-open-jobs',
          groups: openJobGroups,
          emptyTitle: 'No open jobs',
          emptyDescription: 'Open jobs with a next due date will appear here.',
          renderItem: (job) => (
            <div key={job.id} className="attention-item">
              <div>
                <b>{job.client_name || 'Unassigned client'}</b>
                <br />
                <small>{job.service_category || 'General work'} | {job.status || 'open'}</small>
                <br />
                <small className="small-muted">
                  {job.value_estimate ? currencyValue(job.value_estimate) : 'Value pending'}
                  {' | '}
                  {job.next_due_date ? toDisplayTimestamp(job.next_due_date) : 'No next due date'}
                </small>
              </div>
            </div>
          ),
        })}
      </div>
    );
  };

  const renderClients = () => (
    <div>
      <h4>Clients</h4>
      {clients.map((client) => (
        <div key={client.id} className="attention-item">
          {client.name}
        </div>
      ))}
    </div>
  );

  const renderDiary = () => (
    <div>
      <h4>Diary</h4>
      {diaryEntries.map((entry) => (
        <div key={entry.id} className="insight-card">
          <b>{entry.entry_date}</b>
          <br />
          {entry.content}
        </div>
      ))}
    </div>
  );

  const renderTax = () => (
    <div>
      <h4>Tax</h4>
      <div className="momentum-bar">VAT PAYABLE: GBP {vatSummary?.vat_boxes?.payable}</div>
    </div>
  );

  const renderInbox = () => {
    return (
    <div className="inbox-mobile-shell">
      <section className="inbox-mobile-hero">
        <div className="d-flex justify-content-between align-items-center flex-wrap gap-2">
          <div className="inbox-kicker">
            <Bell size={14} />
            Mobile-first exception queue
          </div>
          <div className="status-pill">{filteredInboxCards.length} visible</div>
        </div>
        <h4>Finish now</h4>
        <p>
          Clear the blockers that stop the quarterly export: category, business or personal, split treatment, and duplicate resolution.
        </p>
        <div className="inbox-mobile-stats">
          <div className="inbox-mobile-stat">
            <small>Queue</small>
            <strong>{inboxCards.length}</strong>
            <small>{activeQuarterReport.quarter_reference || READINESS_DEMO_REPORT.quarter_reference}</small>
          </div>
          <div className="inbox-mobile-stat">
            <small>Critical</small>
            <strong>{highSeverityCount}</strong>
            <small>High-severity blockers</small>
          </div>
          <div className="inbox-mobile-stat">
            <small>Ready now</small>
            <strong>{readyToExportCount}</strong>
            <small>Transactions already export-safe</small>
          </div>
        </div>
        <div className="hero-actions">
          <button className="hero-action-main" onClick={() => setCurrentTab('quarter')}>
            <ArrowRight size={16} />
            Review quarter readiness
          </button>
          <button className="hero-action-secondary" onClick={undoLastInboxAction} disabled={inboxBusyId === 'undo-last'}>
            {inboxBusyId === 'undo-last' ? <RefreshCcw size={16} className="spinner" /> : <ArchiveRestore size={16} />}
            Undo last action
          </button>
        </div>
      </section>

      {inboxMessage && (
        <div className={`readiness-panel inbox-message ${inboxMessage.type}`}>
          {inboxMessage.text}
        </div>
      )}

      <section className="readiness-panel">
        <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
          <div>
            <h5 style={{ marginBottom: 4 }}>Queue filters</h5>
            <small className="small-muted">Keep the mobile pass focused on one blocker type at a time.</small>
          </div>
          <div className="status-pill">{activeQuarterReport.readiness_pct ?? READINESS_DEMO_REPORT.readiness_pct}% ready</div>
        </div>
        <div className="inbox-filter-row">
          {INBOX_FILTERS.map((filter) => {
            const count = filter.key === 'all'
              ? inboxCards.length
              : inboxCards.filter((card) => card.issue_types.includes(filter.key)).length;
            return (
              <button
                key={filter.key}
                type="button"
                className={`inbox-filter-chip ${inboxFilter === filter.key ? 'active' : ''}`}
                onClick={() => setInboxFilter(filter.key)}
              >
                <span>{filter.label}</span>
                <small>{count}</small>
              </button>
            );
          })}
        </div>
      </section>

      {filteredInboxCards.length === 0 ? (
        <div className="inbox-empty">
          No blockers match this filter. Reset to All blockers or return to the quarter screen to confirm readiness.
        </div>
      ) : (
        <div className="inbox-card-list">
          {filteredInboxCards.map((card) => {
            const draft = inboxDrafts[card.id] || buildInboxDraft(card);
            const saving = inboxBusyId === card.id;
            const isSplit = draft.business_personal === 'SPLIT' || draft.is_split;
            return (
              <section
                key={card.id}
                className={`inbox-action-card ${activeVoiceContextId === card.id ? 'voice-target' : ''}`}
                onClick={() => setActiveVoiceContextId(card.id)}
              >
                <div className="inbox-card-top">
                  <div>
                    <strong>{card.merchant}</strong>
                    <div className="inbox-card-subline">
                      {card.txn_date ? String(card.txn_date).slice(0, 10) : 'Date pending'} · {formatIssueAmount(card.amount, card.direction)}
                    </div>
                  </div>
                  <span className={`inbox-issue-chip ${card.severity}`}>
                    <TriangleAlert size={14} />
                    {INBOX_REASON_LABELS[card.blocker_reason] || card.blocker_reason.replace(/_/g, ' ')}
                  </span>
                </div>

                <div className="inbox-chip-row">
                  {card.issue_labels.map((label) => (
                    <span key={`${card.id}-${label}`} className={`inbox-issue-chip ${card.severity}`}>
                      {label}
                    </span>
                  ))}
                  {activeVoiceContextId === card.id && (
                    <span className="voice-context-pill active">Voice target</span>
                  )}
                  {card.suggested_category?.category_name && (
                    <button type="button" className="inbox-suggestion-chip" onClick={() => applySuggestedInboxCategory(card)}>
                      <CheckCircle2 size={14} />
                      Suggested: {card.suggested_category.category_name}
                    </button>
                  )}
                </div>

                <p className="inbox-explainer">{card.explanation || 'Resolve the blocking fields to clear this transaction from the queue.'}</p>

                {(card.supports_category || card.supports_business_personal || card.supports_split) && (
                  <div className="inbox-action-grid">
                    <div className="inbox-field">
                      <label>Category code</label>
                      <input
                        value={draft.category_code}
                        onChange={(event) => setInboxDraftField(card.id, 'category_code', event.target.value)}
                        placeholder="MATERIALS"
                      />
                    </div>
                    <div className="inbox-field">
                      <label>Category label</label>
                      <input
                        value={draft.category_name}
                        onChange={(event) => setInboxDraftField(card.id, 'category_name', event.target.value)}
                        placeholder="Materials"
                      />
                    </div>
                  </div>
                )}

                {(card.supports_business_personal || card.supports_split) && (
                  <div>
                    <div className="inbox-field">
                      <label>Business treatment</label>
                    </div>
                    <div className="inbox-toggle-row">
                      {[
                        { value: 'BUSINESS', label: 'Business' },
                        { value: 'PERSONAL', label: 'Personal' },
                        { value: 'SPLIT', label: 'Split' },
                      ].map((option) => (
                        <button
                          key={option.value}
                          type="button"
                          className={`inbox-toggle ${draft.business_personal === option.value ? 'active' : ''}`}
                          onClick={() => setInboxDraftField(card.id, 'business_personal', option.value)}
                        >
                          {option.label}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {(card.supports_split || isSplit) && (
                  <div className="inbox-field">
                    <label>Business split %</label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      value={draft.split_business_pct}
                      onChange={(event) => setInboxDraftField(card.id, 'split_business_pct', event.target.value)}
                      placeholder="80"
                    />
                  </div>
                )}

                {card.supports_duplicate && (
                  <>
                    <div>
                      <div className="inbox-field">
                        <label>Duplicate action</label>
                      </div>
                      <div className="inbox-duplicate-row">
                        {[
                          { value: 'dismiss', label: 'Dismiss duplicate' },
                          { value: 'merge', label: 'Merge to original' },
                        ].map((option) => (
                          <button
                            key={option.value}
                            type="button"
                            className={`inbox-toggle ${draft.duplicate_action === option.value ? 'active' : ''}`}
                            onClick={() => setInboxDraftField(card.id, 'duplicate_action', option.value)}
                          >
                            {option.label}
                          </button>
                        ))}
                      </div>
                    </div>
                    {draft.duplicate_action === 'merge' && (
                      <div className="inbox-field">
                        <label>Original transaction id</label>
                        <input
                          value={draft.duplicate_of_txn_id}
                          onChange={(event) => setInboxDraftField(card.id, 'duplicate_of_txn_id', event.target.value)}
                          placeholder="txn-9001"
                        />
                      </div>
                    )}
                  </>
                )}

                <div className="inbox-footer-row">
                  <div className="inbox-inline-status">
                    Route: {card.resolution_target?.route || `/api/v1/inbox/${card.id}`}
                  </div>
                  <div className="inbox-footer-actions">
                    <button className="secondary-action" onClick={clearInboxMessage} disabled={saving}>
                      Clear banner
                    </button>
                    <button className="primary-action" onClick={() => submitInboxAction(card)} disabled={saving}>
                      {saving ? <RefreshCcw size={16} className="spinner" /> : <CheckCircle2 size={16} />}
                      Save and clear blocker
                    </button>
                  </div>
                </div>
              </section>
            );
          })}
        </div>
      )}
    </div>
    );
  };
  const renderControlCentre = () => {
    const policyLabels = {
      vat_scheme: 'VAT scheme',
      invoice_number_prefix: 'Invoice prefix',
      readiness_enforce_active_period: 'Active period lock',
      large_transaction_threshold_gbp: 'Large transaction threshold',
      feature_control_centre_enabled: 'Control centre feature',
      auto_commit_enabled: 'Auto-commit enabled',
      auto_commit_daily_cap_gbp: 'Auto-commit daily cap',
      auto_commit_single_txn_cap_gbp: 'Auto-commit single cap',
    };

    return (
      <div className="control-centre-layout">
        <div className="control-centre-stack">
          <section className="control-hero">
            <div className="d-flex justify-content-between align-items-center flex-wrap gap-2">
              <div className="readiness-kicker">
                <ShieldAlert size={14} />
                Dedicated admin surface
              </div>
              <div className={`mode-badge ${autoCommitVisibility.headerTone}`}>{autoCommitVisibility.modeBadge}</div>
            </div>
            <h3 style={{ marginTop: 14, marginBottom: 10 }}>Control Centre</h3>
            <p>
              Governance, role access, sync telemetry, queue backlog, and risky-mode visibility stay separate from the day-to-day operator cockpit.
            </p>
            <div className="control-hero-grid" style={{ marginTop: 18 }}>
              <div className="control-stat">
                <small>Policy posture</small>
                <strong>{autoCommitVisibility.enabled ? 'Governed auto-commit' : 'Manual review only'}</strong>
                <small>{formatPolicyDisplayValue('auto_commit_daily_cap_gbp', getPolicyValue(policyRecords, 'auto_commit_daily_cap_gbp', 0))} daily cap</small>
              </div>
              <div className="control-stat">
                <small>Sync health</small>
                <strong>{syncTelemetry.health}</strong>
                <small>{syncTelemetry.workerState}</small>
              </div>
              <div className="control-stat">
                <small>Live sessions</small>
                <strong>{activeSessions.length}</strong>
                <small>{controlCentreSummary.queue.headline}</small>
              </div>
            </div>
          </section>

          <section className={`auto-commit-banner ${autoCommitVisibility.bannerTone}`}>
            <div>
              <strong>{autoCommitVisibility.bannerTitle}</strong>
              <div className="small-muted">{autoCommitVisibility.bannerDetail}</div>
            </div>
            <div className={`mode-badge ${autoCommitVisibility.headerTone}`}>{autoCommitVisibility.headerBadge}</div>
          </section>

          <section className="readiness-panel">
            <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Role Management</h5>
                <small className="small-muted">Who is signed in, what they can do, and where they are working right now.</small>
              </div>
              <div className="status-pill">{currentRoleLabel}</div>
            </div>
            <div className="control-grid-two">
              <div className="toggle-card">
                <strong>Current actor</strong>
                <div className="small-muted">{currentUser.name}</div>
                <div className="small-muted">{currentUser.email}</div>
                <div className="small-muted">Permissions: {currentPermissions.length}</div>
              </div>
              <div className="toggle-card">
                <strong>Available governed actions</strong>
                <div className="d-flex flex-wrap gap-2 mt-2">
                  {currentPermissions.map((permission) => (
                    <span key={permission} className="meta-chip">{permission}</span>
                  ))}
                </div>
              </div>
            </div>
            <div className="control-list mt-3">
              {activeSessions.map((session) => (
                <div key={session.sessionId} className="session-card">
                  <strong>{session.actorName} · {ROLE_LABELS[session.role] || session.role}</strong>
                  <div className="small-muted">{session.surface} · {session.state}</div>
                  <div className="small-muted">Last seen {toDisplayTimestamp(session.lastSeenAt)}</div>
                </div>
              ))}
            </div>
          </section>

          <section className="readiness-panel">
            <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Policy Caps And Feature Toggles</h5>
                <small className="small-muted">Owner and admin policy controls with auditable mutation hooks.</small>
              </div>
              {!canManageGovernance && <div className="status-pill">Read only</div>}
            </div>
            <div className="governance-action-grid mb-3">
              {!canManageGovernance && (
                <div className="readiness-note">
                  Policy mutation is blocked for {currentRoleLabel}. Attempts still create denied audit records.
                </div>
              )}
              <button className="primary-action" onClick={tightenAutoCommitCaps}>
                Tighten auto-commit caps
              </button>
              <button className="secondary-action" onClick={disableAutoCommit}>
                Disable auto-commit
              </button>
              <button className="secondary-action" onClick={setFlatRateVatPolicy}>
                Set flat-rate VAT
              </button>
              <button className="secondary-action" onClick={requestAutoCommitOverride}>
                Request override
              </button>
            </div>
            <div className="policy-record-list">
              {policyRecords.map((record) => (
                <div key={record.policy_key} className="policy-record">
                  <strong>{policyLabels[record.policy_key] || record.policy_key}</strong>
                  <div className="small-muted">Value: {formatPolicyDisplayValue(record.policy_key, record.policy_value)}</div>
                  <div className="small-muted">
                    Changed by {record.changed_by_name} ({ROLE_LABELS[record.changed_role] || record.changed_role}) at {record.changed_at}
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>

        <aside className="control-centre-stack">
          <section className="readiness-panel">
            <h5 style={{ marginBottom: 12 }}>System Health</h5>
            <div className="health-stat-grid">
              <div className="health-stat">
                <small>Sync mode</small>
                <strong>{syncTelemetry.mode}</strong>
                <small>{syncTelemetry.workerState}</small>
              </div>
              <div className="health-stat">
                <small>Queue backlog</small>
                <strong>{controlCentreSummary.health.backlogCount}</strong>
                <small>{controlCentreSummary.queue.high} high-severity blockers</small>
              </div>
              <div className="health-stat">
                <small>Average latency</small>
                <strong>{syncTelemetry.avgLatencyMs} ms</strong>
                <small>{controlCentreSummary.health.failedCount} failed sync events</small>
              </div>
            </div>
            <div className="control-list mt-3">
              <div className="control-row">
                <div>
                  <strong>Last successful sync</strong>
                  <div className="small-muted">{toDisplayTimestamp(syncTelemetry.lastSuccessfulSyncAt)}</div>
                </div>
                <span className="meta-chip">{syncTelemetry.health}</span>
              </div>
              <div className="control-row">
                <div>
                  <strong>Queue backlog headline</strong>
                  <div className="small-muted">{controlCentreSummary.queue.headline}</div>
                </div>
                <span className="meta-chip">{controlCentreSummary.queue.total} open</span>
              </div>
            </div>
          </section>

          <section className="readiness-panel">
            <h5 style={{ marginBottom: 12 }}>Queue Backlog</h5>
            <div className="control-list">
              {activeFinishNowQueue.slice(0, 4).map((item) => (
                <div key={item.id || item.affected_entity_id} className="control-row">
                  <div>
                    <strong>{item.merchant || 'Unknown merchant'}</strong>
                    <div className="small-muted">{item.blocker_reason || item.issue_type}</div>
                  </div>
                  <div className="text-end">
                    <div className="small-muted">{item.txn_date?.slice ? item.txn_date.slice(0, 10) : item.txn_date}</div>
                    <span className="meta-chip">{formatIssueAmount(item.amount, item.direction)}</span>
                  </div>
                </div>
              ))}
              {activeFinishNowQueue.length === 0 && (
                <div className="readiness-note">No finish-now blockers are queued.</div>
              )}
            </div>
          </section>

          <section className="readiness-panel">
            <h5 style={{ marginBottom: 12 }}>Session Visibility</h5>
            <div className="control-list">
              {activeSessions.map((session) => (
                <div key={`${session.sessionId}-visibility`} className="control-row">
                  <div>
                    <strong>{session.actorName}</strong>
                    <div className="small-muted">{session.surface} · {session.state}</div>
                  </div>
                  <span className="meta-chip">{toDisplayTimestamp(session.lastSeenAt)}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="readiness-panel">
            <h5 style={{ marginBottom: 12 }}>Governance Audit Feed</h5>
            {!canReadAudit && (
              <div className="readiness-note">
                Audit feed is restricted to owner, admin, and future accountant read-only roles.
              </div>
            )}
            {canReadAudit && (
              <div className="audit-event-list">
                {governanceAudit.length === 0 && (
                  <div className="readiness-note">No governance events recorded in this session yet.</div>
                )}
                {governanceAudit.map((event) => (
                  <div key={event.id} className="audit-event">
                    <strong>{event.action}</strong>
                    <div className="small-muted">
                      {event.actor_name} ({ROLE_LABELS[event.actor_role] || event.actor_role}) -> {event.outcome}
                    </div>
                    <div className="small-muted">{event.target_type}:{event.target_id || 'n/a'} at {event.changed_at}</div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </aside>
      </div>
    );
  };

  const tightenAutoCommitCaps = () => {
    const dailyCapUpdated = applyTenantPolicyChange({
      policyKey: 'auto_commit_daily_cap_gbp',
      policyValue: 250,
      reason: 'Tighten daily governed auto-commit cap before quarter close.',
    });
    if (!dailyCapUpdated) {
      return;
    }
    applyTenantPolicyChange({
      policyKey: 'auto_commit_single_txn_cap_gbp',
      policyValue: 75,
      reason: 'Tighten single-transaction auto-commit cap before quarter close.',
    });
  };

  const disableAutoCommit = () => {
    applyTenantPolicyChange({
      policyKey: 'auto_commit_enabled',
      policyValue: false,
      reason: 'Disable governed auto-commit pending manual review.',
    });
  };

  const setFlatRateVatPolicy = () => {
    applyTenantPolicyChange({
      policyKey: 'vat_scheme',
      policyValue: 'flat_rate',
      reason: 'Switch VAT policy for tenant-level review.',
    });
  };

  const requestAutoCommitOverride = () => {
    const result = runGovernedAction({
      actor: currentUser,
      tenantId: currentUser.tenant_id,
      permission: PERMISSIONS.AUTO_COMMIT_MANAGE,
      action: 'auto_commit.override_requested',
      targetType: 'tenant_policy',
      targetId: 'auto_commit_override',
      metadata: {
        daily_cap_gbp: getPolicyValue(policyRecords, 'auto_commit_daily_cap_gbp', 0),
        single_txn_cap_gbp: getPolicyValue(policyRecords, 'auto_commit_single_txn_cap_gbp', 0),
      },
      onAudit: appendAuditEvent,
      callback: () => ({
        auto_commit_enabled: getPolicyValue(policyRecords, 'auto_commit_enabled', false),
      }),
    });

    if (!result.allowed) {
      alert(result.reason);
      return;
    }

    alert(`Override request logged within today's cap of ${formatCurrency(getPolicyValue(policyRecords, 'auto_commit_daily_cap_gbp', 0), 2)}.`);
  };

  const exportQuarterlyPack = () => {
    const result = runGovernedAction({
      actor: currentUser,
      tenantId: currentUser.tenant_id,
      permission: PERMISSIONS.QUARTER_EXPORT,
      action: 'quarter.export_requested',
      targetType: 'quarter',
      targetId: `${quarterStart}:${quarterEnd}`,
      metadata: {
        period_start: quarterStart,
        period_end: quarterEnd,
      },
      onAudit: appendAuditEvent,
      callback: () => {
        const url = `${API_BASE_URL}/export/quarterly-pack?period_start=${quarterStart}&period_end=${quarterEnd}`;
        window.open(url, '_blank');
        return url;
      },
    });

    if (!result.allowed) {
      alert(result.reason);
    }
  };

  const openReadinessWorkflow = (issue) => {
    if (issue?.affected_entity_id) {
      setActiveVoiceContextId(String(issue.affected_entity_id));
    }
    if (issue?.resolution_target?.workflow === '/inbox/finish-now') {
      setCurrentTab('inbox');
      return;
    }
    setCurrentTab('inbox');
  };

  const renderVoiceContextBanner = () => {
    if (!(currentTab === 'inbox' || currentTab === 'quarter')) {
      return null;
    }

    return (
      <section className="voice-context-banner">
        <div>
          <strong>Voice triage</strong>
          <div className="small-muted">
            Use the mic against one selected finish-now item only. Supported commands here are category, business, personal, and split n%.
          </div>
        </div>
        <div className="voice-context-row">
          <span className={`voice-context-pill ${activeVoiceCard ? 'active' : ''}`}>
            {activeVoiceCard
              ? `Target: ${activeVoiceCard.merchant} (${activeVoiceCard.id})`
              : 'Select a blocker card to arm voice triage'}
          </span>
          {activeVoiceCard && (
            <button className="secondary-action" type="button" onClick={() => setCurrentTab('inbox')}>
              Edit target
            </button>
          )}
        </div>
        {voiceMicroDecisionChip && (
          <div className="voice-micro-chip">
            <div>
              <strong>{voiceMicroDecisionChip.confirmationChip}</strong>
              <div className="small-muted">
                {voiceMicroDecisionChip.targetLabel} ({voiceMicroDecisionChip.targetId})
              </div>
            </div>
            {voiceMicroDecisionChip.labels.length > 0 && (
              <div className="voice-chip-labels">
                {voiceMicroDecisionChip.labels.map((label) => (
                  <span key={`${voiceMicroDecisionChip.targetId}-${label}`} className="voice-action-pill">
                    {label}
                  </span>
                ))}
              </div>
            )}
            <div className="voice-chip-actions">
              <button
                className="secondary-action"
                type="button"
                onClick={() => {
                  setCurrentTab('inbox');
                  setActiveVoiceContextId(voiceMicroDecisionChip.targetId);
                }}
              >
                Edit
              </button>
              {voiceMicroDecisionChip.undoSupported && (
                <button
                  className="secondary-action"
                  type="button"
                  onClick={undoLastInboxAction}
                  disabled={inboxBusyId === 'undo-last'}
                >
                  Undo
                </button>
              )}
            </div>
          </div>
        )}
      </section>
    );
  };

  const selectedSnapshot = snapshotWorkspace?.snapshots?.find((snapshot) => snapshot.snapshot_id === selectedSnapshotId)
    || snapshotWorkspace?.snapshots?.[0]
    || null;

  const refreshQuarterWorkspace = async () => {
    const nextWorkspace = await loadQuarterWorkspace(activeQuarterReport || READINESS_DEMO_REPORT);
    setSnapshotWorkspace(nextWorkspace);
    return nextWorkspace;
  };

  const downloadSnapshotArtifact = (snapshot) => {
    if (!snapshot) {
      return;
    }
    if (!snapshot.snapshot_id || snapshotDemoEnabled || readinessDemoEnabled) {
      const blob = new Blob([JSON.stringify(snapshot, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${snapshot.quarter_reference || 'quarter'}_${formatSnapshotVersion(snapshot.version_number).replace(/\s+/g, '_').toLowerCase()}.json`;
      link.click();
      URL.revokeObjectURL(url);
      setQuarterActionMessage(`${formatSnapshotVersion(snapshot.version_number)} downloaded as a local JSON reference file.`);
      setQuarterActionError('');
      return;
    }

    const url = `${API_BASE_URL}/export/quarterly-pack?snapshot_id=${encodeURIComponent(snapshot.snapshot_id)}`;
    window.open(url, '_blank');
    setQuarterActionMessage(`${formatSnapshotVersion(snapshot.version_number)} download opened in a new tab.`);
    setQuarterActionError('');
  };

  const createSnapshotVersion = async () => {
    const quarterReference = snapshotWorkspace?.quarter_reference || activeQuarterReport?.quarter_reference || 'Q1-2026';
    const status = snapshotWorkspace?.snapshot_status;

    if (!status?.can_create_snapshot_version) {
      setQuarterActionError(status?.no_change_reason || `No changes detected for ${quarterReference}.`);
      setQuarterActionMessage('');
      return;
    }

    if (snapshotDemoEnabled || readinessDemoEnabled) {
      setQuarterActionError('Demo mode intentionally blocks redundant or simulated snapshot creation.');
      setQuarterActionMessage('');
      return;
    }

    setQuarterActionBusy(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/business-events/snapshots`, {
        quarter_reference: quarterReference,
        description: `Quarter snapshot generated from Quarter workspace`,
        metadata: {
          source_type: 'manual',
          readiness_pct: activeQuarterReport?.readiness_pct ?? null
        }
      });
      await refreshQuarterWorkspace();
      setQuarterActionMessage(`${formatSnapshotVersion(response.data.version_number)} created for ${quarterReference}.`);
      setQuarterActionError('');
    } catch (error) {
      setQuarterActionError(error.response?.data?.error || 'Failed to create snapshot version.');
      setQuarterActionMessage('');
    } finally {
      setQuarterActionBusy(false);
    }
  };

  const closeQuarterWorkspace = async () => {
    const quarterReference = snapshotWorkspace?.quarter_reference || activeQuarterReport?.quarter_reference || 'Q1-2026';
    if (!String(closeReason || '').trim()) {
      setQuarterActionError('Close reason is required.');
      setQuarterActionMessage('');
      return;
    }

    if (snapshotDemoEnabled || readinessDemoEnabled) {
      setSnapshotWorkspace((previous) => previous ? {
        ...previous,
        quarter_lifecycle: {
          ...previous.quarter_lifecycle,
          quarter_state: 'closed',
          status: 'closed',
          closed_at: new Date().toISOString()
        },
        integrity_warnings: buildIntegrityWarnings({
          snapshotStatus: previous.snapshot_status,
          lifecycle: {
            ...previous.quarter_lifecycle,
            quarter_state: 'closed',
            quarter_label: previous.quarter_reference
          },
          selectedSnapshot
        })
      } : previous);
      setQuarterActionMessage(`Quarter ${quarterReference} marked closed in demo mode.`);
      setQuarterActionError('');
      return;
    }

    setQuarterActionBusy(true);
    try {
      await axios.post(`${API_BASE_URL}/business-events/quarters/${quarterReference}/close`, {
        reason: closeReason,
        metadata: {
          screen: 'quarter-workspace'
        }
      });
      await refreshQuarterWorkspace();
      setQuarterActionMessage(`Quarter ${quarterReference} closed.`);
      setQuarterActionError('');
    } catch (error) {
      setQuarterActionError(error.response?.data?.error || 'Failed to close quarter.');
      setQuarterActionMessage('');
    } finally {
      setQuarterActionBusy(false);
    }
  };

  const reopenQuarterWorkspace = async () => {
    const quarterReference = snapshotWorkspace?.quarter_reference || activeQuarterReport?.quarter_reference || 'Q1-2026';
    if (!String(reopenReason || '').trim()) {
      setQuarterActionError('Reopen reason is required.');
      setQuarterActionMessage('');
      return;
    }
    if (!String(reopenConfirmation || '').trim()) {
      setQuarterActionError('Confirmation reference is required.');
      setQuarterActionMessage('');
      return;
    }

    if (snapshotDemoEnabled || readinessDemoEnabled) {
      setSnapshotWorkspace((previous) => previous ? {
        ...previous,
        quarter_lifecycle: {
          ...previous.quarter_lifecycle,
          quarter_state: 'open',
          status: 'open',
          reopened_at: new Date().toISOString(),
          reopen_reason: reopenReason,
          confirmation_reference: reopenConfirmation
        },
        integrity_warnings: buildIntegrityWarnings({
          snapshotStatus: previous.snapshot_status,
          lifecycle: {
            ...previous.quarter_lifecycle,
            quarter_state: 'open',
            quarter_label: previous.quarter_reference
          },
          selectedSnapshot
        })
      } : previous);
      setQuarterActionMessage(`Quarter ${quarterReference} reopened in demo mode with reference ${reopenConfirmation}.`);
      setQuarterActionError('');
      return;
    }

    setQuarterActionBusy(true);
    try {
      await axios.post(`${API_BASE_URL}/business-events/quarters/${quarterReference}/reopen`, {
        reason: reopenReason,
        confirmation_reference: reopenConfirmation,
        metadata: {
          screen: 'quarter-workspace'
        }
      });
      await refreshQuarterWorkspace();
      setQuarterActionMessage(`Quarter ${quarterReference} reopened.`);
      setQuarterActionError('');
    } catch (error) {
      setQuarterActionError(error.response?.data?.error || 'Failed to reopen quarter.');
      setQuarterActionMessage('');
    } finally {
      setQuarterActionBusy(false);
    }
  };

  const renderQuarter = () => {
    const report = activeQuarterReport || READINESS_DEMO_REPORT;
    const issueSummary = Array.isArray(report?.issue_summary) ? report.issue_summary : [];
    const issueList = activeFinishNowQueue;
    const severityBreakdown = buildSeverityBreakdown(issueSummary);
    const historicalSnapshots = buildHistoricalSnapshots(report);
    const quarterLabel = formatQuarterLabel(report?.quarter_reference, report?.period_start, report?.period_end);
    const workspace = snapshotWorkspace || buildDemoSnapshotWorkspace();
    const lifecycle = workspace?.quarter_lifecycle || {
      quarter_label: report?.quarter_reference,
      quarter_state: 'pending'
    };
    const snapshotStatus = workspace?.snapshot_status || null;
    const activityEvents = Array.isArray(workspace?.activity_events) ? workspace.activity_events : [];
    const integrityWarnings = Array.isArray(workspace?.integrity_warnings) ? workspace.integrity_warnings : [];
    const versionList = Array.isArray(workspace?.snapshots) ? workspace.snapshots : [];
    const activeSnapshot = selectedSnapshot || versionList[0] || null;
    const lifecycleBadgeClass = lifecycle?.quarter_state === 'closed'
      ? 'closed'
      : lifecycle?.quarter_state === 'open'
        ? 'open'
        : 'pending';
    const policyLabels = {
      vat_scheme: 'VAT scheme',
      invoice_number_prefix: 'Invoice prefix',
      readiness_enforce_active_period: 'Active period lock',
      large_transaction_threshold_gbp: 'Large transaction threshold',
      feature_control_centre_enabled: 'Control centre feature',
      auto_commit_enabled: 'Auto-commit enabled',
      auto_commit_daily_cap_gbp: 'Auto-commit daily cap',
      auto_commit_single_txn_cap_gbp: 'Auto-commit single cap',
    };

    return (
      <div className="readiness-layout">
        <div className="d-grid gap-3">
          <section className="readiness-hero">
            <div className="readiness-kicker">
              <Calendar size={14} />
              Active quarter readiness only
            </div>
            <h3>{`${report?.readiness_pct ?? 0}% ready \u2014 ${issueList.length} item${issueList.length === 1 ? '' : 's'} left`}</h3>
            <p>
              {quarterLabel}. Historical snapshots remain visible below as read-only reference and do not change this live score.
            </p>
            <div className="readiness-stat-grid">
              <div className="readiness-stat">
                <small>Quarter label</small>
                <strong>{report?.quarter_reference || 'Current quarter'}</strong>
                <small>{report?.period_start} to {report?.period_end}</small>
              </div>
              <div className="readiness-stat">
                <small>Issues remaining</small>
                <strong>{issueList.length}</strong>
                <small>{report?.total_txns_in_period ?? 0} transactions in active scope</small>
              </div>
              <div className="readiness-stat">
                <small>Export state</small>
                <strong>{report?.can_export ? 'Ready' : 'Blocked'}</strong>
                <small>{report?.active_period_enforced ? 'Active quarter enforced' : 'Scope not locked'}</small>
              </div>
            </div>
            <div className="readiness-actions">
              <button className="primary-action" onClick={() => setCurrentTab('inbox')}>
                {issueList.length > 0 ? `Finish now (${issueList.length})` : 'Finish now cleared'}
              </button>
              <button className="secondary-action readiness-secondary" onClick={exportQuarterlyPack} disabled={!report?.can_export}>
                {report?.can_export ? 'Export quarterly pack' : 'Export locked until blockers clear'}
              </button>
            </div>
            <div className="readiness-explainer">
              {(report?.explanation_lines || []).map((line) => (
                <div key={line} className="readiness-note">{line}</div>
              ))}
            </div>
          </section>

          <section className="readiness-panel">
            <div className="snapshot-card-head mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Finish Now Queue</h5>
                <small className="small-muted">The blocking queue is ordered by severity and date so the next fix is obvious.</small>
              </div>
              <div className={`status-pill ${report?.can_export ? 'status-pill-success' : ''}`}>
                {report?.can_export ? 'Export enabled' : `${issueList.length} blockers`}
              </div>
            </div>
            <div className="finish-now-list">
              {issueList.map((issue, index) => (
                <div key={`${issue.affected_entity_id}-${issue.issue_type}`} className="finish-now-card">
                  <div className="finish-now-order">{String(index + 1).padStart(2, '0')}</div>
                  <div className="finish-now-body">
                    <div className="issue-head">
                      <div>
                        <div className={`issue-pill ${issue.severity || 'low'}`}>{issue.severity || 'low'} severity</div>
                        <h6 style={{ marginTop: 10, marginBottom: 6 }}>{issue.resolution_target?.label || issue.issue_type}</h6>
                        <div className="small-muted">{issue.explanation}</div>
                      </div>
                      <div className="text-end">
                        <strong>{formatIssueAmount(issue.amount, issue.direction)}</strong>
                        <div className="small-muted">{issue.txn_date || 'Date pending'}</div>
                      </div>
                    </div>
                    <div className="issue-meta">
                      <span className="meta-chip">Merchant: {issue.merchant || 'Unknown'}</span>
                      <span className="meta-chip">Route: {issue.resolution_target?.workflow || issue.resolution_target?.route || 'n/a'}</span>
                      <span className="meta-chip">Weight: {issue.weight || 0}</span>
                    </div>
                  </div>
                  <div className="finish-now-actions">
                    <button
                      className="secondary-action"
                      type="button"
                      onClick={() => setActiveVoiceContextId(String(issue.affected_entity_id))}
                    >
                      {activeVoiceContextId === String(issue.affected_entity_id) ? 'Voice target set' : 'Arm voice'}
                    </button>
                    {(readinessDemoEnabled || snapshotDemoEnabled) ? (
                      <button className="primary-action" onClick={() => resolveQuarterIssue(issue.affected_entity_id)}>
                        Mark fixed
                      </button>
                    ) : (
                      <button className="primary-action" onClick={() => openReadinessWorkflow(issue)}>
                        Open fix
                      </button>
                    )}
                  </div>
                </div>
              ))}
              {issueList.length === 0 && (
                <div className="alert alert-success mb-0">
                  Finish Now is clear. Export enabled immediately for the active quarter.
                </div>
              )}
            </div>
          </section>

          <section className="readiness-panel">
            <div className="snapshot-toolbar mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Snapshot Versions</h5>
                <small className="small-muted">Immutable quarter baselines with diff review and re-download support.</small>
              </div>
              <div className="d-flex flex-wrap gap-2">
                <button className="secondary-action" onClick={refreshQuarterWorkspace} disabled={quarterActionBusy}>
                  <RefreshCcw size={16} />
                  Refresh status
                </button>
                <button
                  className="primary-action"
                  onClick={createSnapshotVersion}
                  disabled={quarterActionBusy || !snapshotStatus?.can_create_snapshot_version || lifecycle?.quarter_state === 'closed'}
                >
                  <Plus size={16} />
                  Create snapshot
                </button>
              </div>
            </div>
            {quarterActionError && <div className="panel-error">{quarterActionError}</div>}
            {quarterActionMessage && <div className="panel-warning">{quarterActionMessage}</div>}
            <div className="snapshot-version-list">
              {versionList.map((snapshot) => (
                <div
                  key={snapshot.snapshot_id}
                  className={`snapshot-version-card ${activeSnapshot?.snapshot_id === snapshot.snapshot_id ? 'selected' : ''}`}
                >
                  <button className="snapshot-version-button" onClick={() => setSelectedSnapshotId(snapshot.snapshot_id)}>
                    <div className="snapshot-label-row">
                      <div>
                        <div className="snapshot-version-code">{formatSnapshotVersion(snapshot.version_number)}</div>
                        <div className="snapshot-subline">{toDisplayTimestamp(snapshot.created_at)}</div>
                      </div>
                      <div className="timeline-pill archived">{snapshot.status}</div>
                    </div>
                    <div className="snapshot-subline" style={{ marginTop: 10 }}>{snapshot.description}</div>
                    <div className="snapshot-meta-row" style={{ marginTop: 10 }}>
                      <span className="meta-chip">{snapshot.snapshot_summary?.transaction_count || 0} transactions</span>
                      <span className="meta-chip">{formatCurrency(snapshot.snapshot_summary?.totals?.gross_amount || 0, 2)} gross</span>
                      <span className="meta-chip">{snapshot.readiness_pct}% readiness</span>
                    </div>
                  </button>
                  <div className="snapshot-download-row" style={{ marginTop: 12 }}>
                    <small className="small-muted">{snapshot.snapshot_id}</small>
                    <button className="download-link-button" onClick={() => downloadSnapshotArtifact(snapshot)}>
                      <span className="meta-chip"><Download size={14} /> Re-download</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="readiness-panel">
            <div className="snapshot-card-head mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Diff Review</h5>
                <small className="small-muted">Compare the selected snapshot against its prior baseline.</small>
              </div>
              {activeSnapshot && <div className="status-pill">{formatSnapshotVersion(activeSnapshot.version_number)}</div>}
            </div>
            {activeSnapshot ? (
              <div className="d-grid gap-3">
                <div className="diff-impact-grid">
                  <div className="diff-impact-stat">
                    <small>Revenue impact</small>
                    <strong>{formatCurrency(activeSnapshot.diff_summary?.revenue_impact || 0, 2)}</strong>
                    <small>Net change since prior version</small>
                  </div>
                  <div className="diff-impact-stat">
                    <small>VAT impact</small>
                    <strong>{formatCurrency(activeSnapshot.diff_summary?.vat_impact || 0, 2)}</strong>
                    <small>Tax movement captured in diff</small>
                  </div>
                </div>
                <div className="diff-columns">
                  <div className="diff-card">
                    <h6><Plus size={16} /> Added transactions</h6>
                    <div className="diff-list">
                      {(activeSnapshot.diff_summary?.added_transactions || []).map((entry) => (
                        <div key={entry.txn_id} className="diff-row">
                          <strong>{entry.merchant || entry.txn_id}</strong>
                          <div className="small-muted">{entry.entity_type} • {entry.date || 'Date pending'}</div>
                          <div className="small-muted">{formatCurrency(entry.gross_amount || entry.amount || entry.revenue_impact || 0, 2)}</div>
                        </div>
                      ))}
                      {!(activeSnapshot.diff_summary?.added_transactions || []).length && (
                        <div className="small-muted">No new transactions were introduced in this version.</div>
                      )}
                    </div>
                  </div>
                  <div className="diff-card">
                    <h6><ArchiveRestore size={16} /> Adjustments and removals</h6>
                    <div className="diff-list">
                      {(activeSnapshot.diff_summary?.adjustments || []).map((entry) => (
                        <div key={entry.txn_id} className="diff-row">
                          <strong>{entry.current_transaction?.merchant || entry.txn_id}</strong>
                          <div className="small-muted">Adjusted fields: {(entry.changed_fields || []).join(', ') || 'n/a'}</div>
                          <div className="small-muted">Revenue {formatCurrency(entry.revenue_impact || 0, 2)} • VAT {formatCurrency(entry.vat_impact || 0, 2)}</div>
                        </div>
                      ))}
                      {(activeSnapshot.diff_summary?.voided_transactions || []).map((entry) => (
                        <div key={entry.txn_id} className="diff-row">
                          <strong>{entry.merchant || entry.txn_id}</strong>
                          <div className="small-muted">Voided or removed • {entry.date || 'Date pending'}</div>
                          <div className="small-muted">Reversal {formatCurrency(entry.gross_amount || entry.amount || 0, 2)}</div>
                        </div>
                      ))}
                      {!(activeSnapshot.diff_summary?.adjustments || []).length && !(activeSnapshot.diff_summary?.voided_transactions || []).length && (
                        <div className="small-muted">No adjustments or removals were recorded in this version.</div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="readiness-note">No snapshots recorded yet for this quarter.</div>
            )}
          </section>

          <section className="readiness-panel">
            <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Issue Drill-Down</h5>
                <small className="small-muted">Every blocker shows severity, transaction context, and a direct corrective action.</small>
              </div>
              <div className="status-pill">{issueList.length} open issues</div>
            </div>
            <div className="issue-list">
              {issueList.map((issue) => (
                <div key={`${issue.affected_entity_id}-${issue.issue_type}`} className="issue-row">
                  <div className="issue-head">
                    <div>
                      <div className={`issue-pill ${issue.severity || 'low'}`}>{issue.severity || 'low'} severity</div>
                      <h6 style={{ marginTop: 10, marginBottom: 6 }}>{issue.resolution_target?.label || issue.issue_type}</h6>
                      <div className="small-muted">{issue.explanation}</div>
                    </div>
                    <div className="text-end">
                      <strong>{formatIssueAmount(issue.amount, issue.direction)}</strong>
                      <div className="small-muted">{issue.txn_date || 'Date pending'}</div>
                    </div>
                  </div>
                  <div className="issue-meta">
                    <span className="meta-chip">Merchant: {issue.merchant || 'Unknown'}</span>
                    <span className="meta-chip">Entity: {issue.affected_entity_type}</span>
                    <span className="meta-chip">Weight: {issue.weight || 0}</span>
                    <span className="meta-chip">Route: {issue.resolution_target?.route || 'n/a'}</span>
                  </div>
                  <div className="issue-links">
                    <button className="issue-link" onClick={() => openReadinessWorkflow(issue)}>
                      {issue.resolution_target?.label || 'Open fix'}
                    </button>
                    <button className="issue-link" onClick={() => setCurrentTab('activity')}>
                      View timeline context
                    </button>
                  </div>
                </div>
              ))}
              {issueList.length === 0 && (
                <div className="alert alert-success mb-0">No active blockers remain for this quarter.</div>
              )}
            </div>
          </section>
        </div>

        <aside className="readiness-side-stack">
          <section className="readiness-panel">
            <h5 style={{ marginBottom: 12 }}>Severity Breakdown</h5>
            <div className="severity-grid">
              {severityBreakdown.map((entry) => (
                <div key={entry.severity} className="severity-card">
                  <div className={`severity-pill ${entry.severity}`}>{entry.severity}</div>
                  <strong>{entry.count}</strong>
                  <small>{entry.weight} weighted points still open</small>
                </div>
              ))}
            </div>
          </section>

          <section className="readiness-panel">
            <div className="snapshot-card-head mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Integrity Warnings</h5>
                <small className="small-muted">Warnings stay visible here even when export readiness is already 100%.</small>
              </div>
              <div className="status-pill">{integrityWarnings.length} warning{integrityWarnings.length === 1 ? '' : 's'}</div>
            </div>
            <div className="warning-list">
              {integrityWarnings.map((warning, index) => (
                <div key={`${warning.title}-${index}`} className={`warning-card ${warning.level || 'info'}`}>
                  <div className="warning-head">
                    <div className="warning-title">{warning.title || 'Integrity note'}</div>
                    <ShieldAlert size={16} />
                  </div>
                  <div className="small-muted" style={{ marginTop: 8 }}>{warning.detail || warning.message || 'No extra detail recorded.'}</div>
                </div>
              ))}
              {!integrityWarnings.length && (
                <div className="readiness-note">No integrity warnings are active for the selected snapshot.</div>
              )}
            </div>
          </section>

          <section className="readiness-panel">
            <div className="snapshot-card-head mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Quarter State Controls</h5>
                <small className="small-muted">Close locks new monetary activity. Reopen requires a reason and confirmation reference.</small>
              </div>
              <div className={`quarter-state-badge ${lifecycleBadgeClass}`}>
                {lifecycle?.quarter_state === 'closed' ? <Lock size={14} /> : <LockOpen size={14} />}
                {lifecycle?.quarter_state || 'pending'}
              </div>
            </div>
            <div className="quarter-state-row" style={{ marginBottom: 12 }}>
              <span className="meta-chip">Closed at: {toDisplayTimestamp(lifecycle?.closed_at)}</span>
              <span className="meta-chip">Reopened at: {toDisplayTimestamp(lifecycle?.reopened_at)}</span>
            </div>
            <div className="lifecycle-form">
              <div>
                <label className="small-muted" htmlFor="quarter-close-reason">Close reason</label>
                <textarea id="quarter-close-reason" value={closeReason} onChange={(event) => setCloseReason(event.target.value)} />
              </div>
              <button className="danger-action" onClick={closeQuarterWorkspace} disabled={quarterActionBusy || lifecycle?.quarter_state === 'closed'}>
                <Lock size={16} />
                Close quarter
              </button>
              <div>
                <label className="small-muted" htmlFor="quarter-reopen-reason">Reopen reason</label>
                <textarea id="quarter-reopen-reason" value={reopenReason} onChange={(event) => setReopenReason(event.target.value)} />
              </div>
              <div>
                <label className="small-muted" htmlFor="quarter-reopen-confirmation">Confirmation reference</label>
                <input id="quarter-reopen-confirmation" value={reopenConfirmation} onChange={(event) => setReopenConfirmation(event.target.value)} />
              </div>
              <button className="secondary-action" onClick={reopenQuarterWorkspace} disabled={quarterActionBusy || lifecycle?.quarter_state !== 'closed'}>
                <LockOpen size={16} />
                Reopen quarter
              </button>
              {lifecycle?.reopen_reason && (
                <div className="readiness-note">
                  Last reopen reason: {lifecycle.reopen_reason}{lifecycle?.confirmation_reference ? ` (${lifecycle.confirmation_reference})` : ''}
                </div>
              )}
            </div>
          </section>

          <section className="readiness-panel">
            <h5 style={{ marginBottom: 12 }}>Current vs Historical</h5>
            <div className="history-grid">
              <div className="history-card">
                <div>
                  <div className="timeline-pill live">Live active quarter</div>
                  <h6 style={{ marginTop: 10, marginBottom: 4 }}>{report?.quarter_reference || 'Current quarter'}</h6>
                  <small className="small-muted">This score recalculates from active-quarter issues only.</small>
                </div>
                <div className="history-score">{report?.readiness_pct ?? 0}%</div>
              </div>
              {historicalSnapshots.map((snapshot) => (
                <div key={snapshot.quarter_reference} className="history-card">
                  <div>
                    <div className="timeline-pill archived">{snapshot.status}</div>
                    <h6 style={{ marginTop: 10, marginBottom: 4 }}>{snapshot.quarter_reference}</h6>
                    <small className="small-muted">{snapshot.detail}</small>
                  </div>
                  <div className="history-score">{snapshot.readiness_pct}%</div>
                </div>
              ))}
            </div>
          </section>

          <section className="readiness-panel">
            <h5 style={{ marginBottom: 12 }}>Quarter Context</h5>
            <div className="d-grid gap-2">
              <div className="readiness-note">
                Requested period: {report?.requested_period_start || 'n/a'} to {report?.requested_period_end || 'n/a'}
              </div>
              <div className="readiness-note">
                Active period enforced: {report?.active_period_enforced ? 'Yes - score is locked to the current quarter.' : 'No'}
              </div>
              <div className="readiness-note">
                Local readiness URL: {typeof window !== 'undefined' ? window.location.href : 'Unavailable'}
              </div>
              <div className="readiness-note">
                Snapshot UI URL: {typeof window !== 'undefined' ? `${window.location.origin}/?snapshotDemo=1&tab=quarter` : 'Unavailable'}
              </div>
            </div>
          </section>

          <section className="readiness-panel">
            <div className="snapshot-card-head mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Lifecycle Timeline</h5>
                <small className="small-muted">Recent quarter governance and snapshot events.</small>
              </div>
              <div className="status-pill"><History size={14} /> {activityEvents.length} events</div>
            </div>
            <div className="audit-event-list">
              {activityEvents.map((event) => {
                const metadata = normalizeEventMetadata(event.metadata);
                return (
                  <div key={event.event_id} className="audit-event">
                    <strong>{event.description || event.event_type}</strong>
                    <div className="small-muted">{event.event_type} • {toDisplayTimestamp(event.timestamp)}</div>
                    {metadata.reason && <div className="small-muted">Reason: {metadata.reason}</div>}
                    {metadata.reopen_reason && <div className="small-muted">Reopen: {metadata.reopen_reason}</div>}
                    {metadata.confirmation_reference && <div className="small-muted">Confirmation: {metadata.confirmation_reference}</div>}
                    {metadata.version_number && <div className="small-muted">Version: {formatSnapshotVersion(metadata.version_number)}</div>}
                  </div>
                );
              })}
              {!activityEvents.length && <div className="readiness-note">No lifecycle activity recorded yet.</div>}
            </div>
          </section>

          <section className="readiness-panel">
            <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
              <div>
                <h5 style={{ marginBottom: 4 }}>Governance Control</h5>
                <small className="small-muted">Tenant policy storage, role checks, and audit hooks for protected actions.</small>
              </div>
              <div className="status-pill">{currentRoleLabel}</div>
            </div>
            <div className="d-flex flex-wrap gap-2 mb-3">
              {currentPermissions.map((permission) => (
                <span key={permission} className="meta-chip">{permission}</span>
              ))}
            </div>
            <div className="governance-action-grid mb-3">
              {!canManageGovernance && (
                <div className="readiness-note">
                  Policy mutation is blocked for {currentRoleLabel}. Buttons below will record denied audit events for protected actions.
                </div>
              )}
              <button className="primary-action" onClick={tightenAutoCommitCaps}>
                Tighten auto-commit caps
              </button>
              <button className="secondary-action" onClick={disableAutoCommit}>
                Disable auto-commit
              </button>
              <button className="secondary-action" onClick={setFlatRateVatPolicy}>
                Set flat-rate VAT
              </button>
              <button className="secondary-action" onClick={requestAutoCommitOverride}>
                Request override
              </button>
            </div>
            <div className="policy-record-list">
              {policyRecords.map((record) => (
                <div key={record.policy_key} className="policy-record">
                  <strong>{policyLabels[record.policy_key] || record.policy_key}</strong>
                  <div className="small-muted">
                    Value: {formatPolicyDisplayValue(record.policy_key, record.policy_value)}
                  </div>
                  <div className="small-muted">
                    Changed by {record.changed_by_name} ({ROLE_LABELS[record.changed_role] || record.changed_role}) at {record.changed_at}
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="readiness-panel">
            <h5 style={{ marginBottom: 12 }}>Audit Hooks</h5>
            {!canReadAudit && (
              <div className="readiness-note">
                Audit feed is restricted to owner, admin, and future accountant read-only roles.
              </div>
            )}
            {canReadAudit && (
              <div className="audit-event-list">
                {governanceAudit.length === 0 && (
                  <div className="readiness-note">
                    No governance events recorded in this session yet.
                  </div>
                )}
                {governanceAudit.map((event) => (
                  <div key={event.id} className="audit-event">
                    <strong>{event.action}</strong>
                    <div className="small-muted">
                      {event.actor_name} ({ROLE_LABELS[event.actor_role] || event.actor_role}) -> {event.outcome}
                    </div>
                    <div className="small-muted">
                      {event.target_type}:{event.target_id || 'n/a'} at {event.changed_at}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </aside>
      </div>
    );
  };

  const renderPreviewPanel = () => {
    if (!previewDraft || !previewForm) {
      return (
        <div className="empty-panel">
          <h5>Preview Queue</h5>
          <p className="small-muted mb-0">
            Monetary capture stays in draft until you review it here. Save an invoice, receipt, payment, or quote to open the preview.
          </p>
        </div>
      );
    }

    const confidenceClass = previewDraft.preview?.confidence_indicator || 'unknown';

    return (
      <div className="preview-panel">
        <div className="preview-header">
          <div>
            <div className="status-pill">Draft {previewDraft.compositionId.slice(0, 8)}</div>
            <h5 className="mt-2" style={{ textTransform: 'capitalize' }}>
              {previewForm.entityType} preview
            </h5>
            <div className="preview-note">
              Review the structured fields before commit. Edit stays in draft. Cancel archives the draft.
            </div>
          </div>
          <div className={`preview-badge ${confidenceClass}`}>{confidenceClass} confidence</div>
        </div>

        {previewError && <div className="panel-error">{previewError}</div>}
        {previewDraft.preview?.confidence_indicator === 'low' && (
          <div className="panel-warning">
            Low-confidence capture detected. Edit the values before confirming.
          </div>
        )}

        <div className="preview-field-grid">
          <div className="preview-field">
            <label>Entity Type</label>
            {previewMode === 'edit' ? (
              <select value={previewForm.entityType} onChange={(event) => setPreviewField('entityType', event.target.value)}>
                {MONETARY_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            ) : (
              <div className="preview-value" style={{ textTransform: 'capitalize' }}>{previewForm.entityType}</div>
            )}
          </div>
          <div className="preview-field">
            <label>Counterparty</label>
            {previewMode === 'edit' ? (
              <input value={previewForm.counterparty} onChange={(event) => setPreviewField('counterparty', event.target.value)} />
            ) : (
              <div className="preview-value">{previewForm.counterparty || 'Pending'}</div>
            )}
          </div>
          <div className="preview-field">
            <label>Gross Amount</label>
            {previewMode === 'edit' ? (
              <input type="number" step="0.01" value={previewForm.grossAmount} onChange={(event) => setPreviewField('grossAmount', event.target.value)} />
            ) : (
              <div className="preview-value">{currencyValue(previewForm.grossAmount)}</div>
            )}
          </div>
          <div className="preview-field">
            <label>Net Amount</label>
            {previewMode === 'edit' ? (
              <input type="number" step="0.01" value={previewForm.netAmount} onChange={(event) => setPreviewField('netAmount', event.target.value)} />
            ) : (
              <div className="preview-value">{currencyValue(previewForm.netAmount)}</div>
            )}
          </div>
          <div className="preview-field">
            <label>VAT Amount</label>
            {previewMode === 'edit' ? (
              <input type="number" step="0.01" value={previewForm.vatAmount} onChange={(event) => setPreviewField('vatAmount', event.target.value)} />
            ) : (
              <div className="preview-value">{currencyValue(previewForm.vatAmount)}</div>
            )}
          </div>
          <div className="preview-field">
            <label>VAT Rate</label>
            {previewMode === 'edit' ? (
              <input type="number" step="0.01" value={previewForm.vatRate} onChange={(event) => setPreviewField('vatRate', event.target.value)} />
            ) : (
              <div className="preview-value">{previewForm.vatRate === '' ? 'Pending' : `${previewForm.vatRate}%`}</div>
            )}
          </div>
          <div className="preview-field">
            <label>Category</label>
            {previewMode === 'edit' ? (
              <input value={previewForm.category} onChange={(event) => setPreviewField('category', event.target.value)} />
            ) : (
              <div className="preview-value">{previewForm.category || 'Pending'}</div>
            )}
          </div>
          <div className="preview-field">
            <label>Relevant Date</label>
            {previewMode === 'edit' ? (
              <input type="date" value={previewForm.relevantDate} onChange={(event) => setPreviewField('relevantDate', event.target.value)} />
            ) : (
              <div className="preview-value">{previewForm.relevantDate || 'Pending'}</div>
            )}
          </div>
          <div className="preview-field" style={{ gridColumn: '1 / -1' }}>
            <label>Notes</label>
            {previewMode === 'edit' ? (
              <textarea value={previewForm.note} onChange={(event) => setPreviewField('note', event.target.value)} />
            ) : (
              <div className="preview-value" style={{ minHeight: 96 }}>{previewForm.note || 'No note captured.'}</div>
            )}
          </div>
        </div>

        <div className="preview-actions">
          <button className="primary-action" onClick={confirmPreviewDraft} disabled={previewBusy}>
            {previewBusy ? <RefreshCcw size={16} className="spinner" /> : null}
            Confirm
          </button>
          <button
            className="secondary-action"
            onClick={() => setPreviewMode((previous) => (previous === 'edit' ? 'review' : 'edit'))}
            disabled={previewBusy}
          >
            {previewMode === 'edit' ? 'Lock Review' : 'Edit Draft'}
          </button>
          <button className="danger-action" onClick={cancelPreviewDraft} disabled={previewBusy}>
            Cancel
          </button>
        </div>
      </div>
    );
  };

  const renderAdd = () => (
    <div>
      <section className={`capture-mode-panel ${autoCommitVisibility.bannerTone}`}>
        <div className="d-flex justify-content-between align-items-center flex-wrap gap-2">
          <div>
            <div className={`mode-badge ${autoCommitVisibility.headerTone}`}>{autoCommitVisibility.headerBadge}</div>
            <h4 style={{ marginTop: 12, marginBottom: 6 }}>{autoCommitVisibility.captureTitle}</h4>
            <div className="small-muted">{autoCommitVisibility.captureDetail}</div>
          </div>
          <button className="secondary-action" onClick={() => setCurrentTab('control')}>
            Open control centre
          </button>
        </div>
      </section>
      <div className="capture-grid">
        <div className="capture-panel">
          <h4>Monetary Capture</h4>
          <p className="small-muted mb-2">
            Capture the draft first, then review the preview card before committing the record.
          </p>
          <div className="capture-inline-meta">
            <span className="meta-chip">Local API: {API_BASE_URL}</span>
            <span className="meta-chip">Preview required for invoice, receipt, payment, quote</span>
          </div>
          {previewError && !previewDraft && <div className="panel-error">{previewError}</div>}
          <div className="capture-type-grid">
            {['invoice', 'receipt', 'payment', 'quote', 'booking', 'note'].map((type) => (
              <button
                key={type}
                className={`capture-type-btn ${manualForm.type === type ? 'active' : ''}`}
                onClick={() => {
                  setManualField('type', type);
                  if (!isMonetaryType(type)) {
                    setPreviewDraft(null);
                    setPreviewForm(null);
                  }
                }}
              >
                {type}
              </button>
            ))}
          </div>
          <div className="capture-field-grid">
            <div className="field-shell">
              <label>Counterparty</label>
              <input
                placeholder="Customer, supplier, or payer"
                value={manualForm.counterparty}
                onChange={(event) => setManualField('counterparty', event.target.value)}
              />
            </div>
            <div className="field-shell">
              <label>Relevant Date</label>
              <input
                type="date"
                value={manualForm.relevantDate}
                onChange={(event) => setManualField('relevantDate', event.target.value)}
              />
            </div>
            <div className="field-shell">
              <label>Gross Amount</label>
              <input
                type="number"
                step="0.01"
                placeholder="0.00"
                value={manualForm.grossAmount}
                onChange={(event) => setManualField('grossAmount', event.target.value)}
              />
            </div>
            <div className="field-shell">
              <label>VAT Rate (%)</label>
              <input
                type="number"
                step="0.01"
                placeholder="20"
                value={manualForm.vatRate}
                onChange={(event) => setManualField('vatRate', event.target.value)}
              />
            </div>
            <div className="field-shell">
              <label>Net Amount</label>
              <input
                type="number"
                step="0.01"
                placeholder="0.00"
                value={manualForm.netAmount}
                onChange={(event) => setManualField('netAmount', event.target.value)}
              />
            </div>
            <div className="field-shell">
              <label>VAT Amount</label>
              <input
                type="number"
                step="0.01"
                placeholder="0.00"
                value={manualForm.vatAmount}
                onChange={(event) => setManualField('vatAmount', event.target.value)}
              />
            </div>
            <div className="field-shell" style={{ gridColumn: '1 / -1' }}>
              <label>Category</label>
              <input
                placeholder="Materials, labour, fuel, subcontractor"
                value={manualForm.category}
                onChange={(event) => setManualField('category', event.target.value)}
              />
            </div>
            <div className="field-shell" style={{ gridColumn: '1 / -1' }}>
              <label>Description / Note</label>
              <textarea
                placeholder="What was captured?"
                value={manualForm.note}
                onChange={(event) => setManualField('note', event.target.value)}
              />
            </div>
          </div>
          <div className="preview-actions">
            <button className="primary-action" onClick={submitManualEntry} disabled={manualSaving}>
              {manualSaving ? <RefreshCcw size={16} className="spinner" /> : null}
              {isMonetaryType(manualForm.type) ? `Preview ${manualForm.type}` : `Save ${manualForm.type}`}
            </button>
            <button className="secondary-action" onClick={() => resetManualCapture(manualForm.type)} disabled={manualSaving || previewBusy}>
              Clear
            </button>
          </div>
        </div>
        {renderPreviewPanel()}
      </div>
    </div>
  );

  return (
    <div className="container py-3 shell">
      <style>{styles}</style>
      {onboardingRequired ? (
        <OnboardingGate
          busy={onboardingBusy}
          errorMessage={onboardingError}
          onSubmit={completeOnboarding}
        />
      ) : (
        <>
      <header className="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
        <div>
          <h2 onClick={() => setCurrentTab('home')} style={{ cursor: 'pointer', marginBottom: 0 }}>
            bizPA <span className="badge text-bg-warning" style={{ fontSize: '0.5rem' }}>v1.3.9</span>
          </h2>
          <div className="d-flex align-items-center flex-wrap gap-2 mt-1">
            <small className="small-muted">{currentUser.name} · {currentRoleLabel}</small>
            <div className={`mode-badge ${autoCommitVisibility.headerTone}`}>{autoCommitVisibility.headerBadge}</div>
          </div>
        </div>
        <div className="header-controls">
          <select className="header-select" value={currentUser.id} onChange={(event) => switchUser(event.target.value)}>
            {appUsers.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name} · {ROLE_LABELS[user.role] || user.role}
              </option>
            ))}
          </select>
          <button className="btn btn-light rounded-circle p-2 me-2" onClick={toggleListening} disabled={voiceStatus === 'processing'} title="Voice Log">
            {voiceStatus === 'processing' ? <RefreshCcw size={18} className="spinner" /> : <Mic size={18} />}
          </button>
          <button className="btn btn-light rounded-circle p-2 me-2" onClick={toggleTheme}>
            {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
          </button>
          <button className="btn btn-light rounded-circle p-2" onClick={fetchAllData}>
            <RefreshCcw size={18} className={loading ? 'spinner' : ''} />
          </button>
        </div>
      </header>

      {MVP_QUARTERLY_EXPORT_MODE && <div className="alert alert-warning py-2">{LEGAL_DISCLAIMER}</div>}
      <section className={`auto-commit-banner ${autoCommitVisibility.bannerTone}`}>
        <div>
          <strong>{autoCommitVisibility.bannerTitle}</strong>
          <div className="small-muted">{autoCommitVisibility.bannerDetail}</div>
        </div>
        <button className="secondary-action" onClick={() => setCurrentTab('control')}>
          Review control centre
        </button>
      </section>
      {connectionError && <div className="alert alert-danger">{connectionError}</div>}
      {renderVoiceContextBanner()}

      {loading ? (
        <div className="text-center py-5">Loading...</div>
      ) : (
        <div style={{ paddingBottom: '100px' }}>
          {currentTab === 'home' && renderDashboard()}
          {currentTab === 'add' && renderAdd()}
          {currentTab === 'control' && renderControlCentre()}
          {currentTab === 'inbox' && renderInbox()}
          {currentTab === 'quarter' && renderQuarter()}
          {currentTab === 'activity' && renderActivity()}
          {currentTab === 'quotes' && renderQuotes()}
          {currentTab === 'calendar' && renderCalendar()}
          {currentTab === 'clients' && renderClients()}
          {currentTab === 'diary' && renderDiary()}
          {currentTab === 'tax' && renderTax()}
        </div>
      )}

      <nav className="bottom-nav">
        {[
          { key: 'home', label: 'Home', icon: <LayoutGrid size={20} /> },
          { key: 'add', label: 'Capture', icon: <FileText size={20} /> },
          { key: 'control', label: 'Control', icon: <ShieldAlert size={20} /> },
          { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
          { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
          { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
          { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
          { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
          { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },
        ]
          .filter((navItem) => !MVP_QUARTERLY_EXPORT_MODE || navItem.key !== 'tax')
          .map((navItem) => (
            <div
              key={navItem.key}
              className={`nav-item ${currentTab === navItem.key ? 'active' : ''}`}
              onClick={() => setCurrentTab(navItem.key)}
            >
              {navItem.icon}
              <span>{navItem.label}</span>
            </div>
          ))}
      </nav>

      <div className="capture-btn-container">
        {isListening && transcript && <div className="voice-preview">"{transcript}"</div>}
        <button className="log-something-btn" onClick={toggleListening} disabled={voiceStatus === 'processing'}>
          {voiceStatus === 'processing' ? <RefreshCcw size={20} className="spinner" /> : <Mic size={20} />}
          <span>Log</span>
        </button>
      </div>
        </>
      )}
    </div>
  );
}

export default App;
