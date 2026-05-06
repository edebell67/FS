import {
  ROLE_LABELS,
  PERMISSIONS,
  applyPolicyUpdate,
  buildDefaultPolicyRecords,
  getPermissionsForRole,
  hasPermission,
  runGovernedAction,
} from './governance';

const tenantId = 'tenant-bizpa-demo';
const owner = { id: 'user-owner', name: 'Alice Owner', role: 'owner' };
const admin = { id: 'user-admin', name: 'Cara Admin', role: 'admin' };
const staff = { id: 'user-staff', name: 'Bob Staff', role: 'staff' };
const accountant = { id: 'user-accountant', name: 'Dana Accountant', role: 'accountant_readonly' };

describe('governance role model', () => {
  test('distinguishes owner, admin, staff, and accountant read-only capabilities', () => {
    expect(ROLE_LABELS.owner).toBe('Owner');
    expect(getPermissionsForRole(owner.role)).toContain(PERMISSIONS.GOVERNANCE_MANAGE);
    expect(getPermissionsForRole(admin.role)).toContain(PERMISSIONS.QUARTER_EXPORT);
    expect(getPermissionsForRole(staff.role)).not.toContain(PERMISSIONS.GOVERNANCE_MANAGE);
    expect(getPermissionsForRole(accountant.role)).toContain(PERMISSIONS.GOVERNANCE_AUDIT_READ);
    expect(hasPermission(accountant, PERMISSIONS.ACTIVITY_CAPTURE)).toBe(false);
  });

  test('policy changes are stored with audit metadata and actor attribution', () => {
    const records = buildDefaultPolicyRecords({
      tenantId,
      actor: owner,
      now: '2026-03-11T16:30:00.000Z',
    });
    const auditEvents = [];
    const result = applyPolicyUpdate({
      records,
      tenantId,
      actor: admin,
      policyKey: 'auto_commit_daily_cap_gbp',
      policyValue: 250,
      reason: 'Tighten exposure before quarter close',
      now: '2026-03-11T16:31:00.000Z',
      onAudit: (event) => auditEvents.push(event),
    });

    expect(result.allowed).toBe(true);
    expect(result.record.changed_by).toBe(admin.id);
    expect(result.record.changed_role).toBe('admin');
    expect(result.record.changed_at).toBe('2026-03-11T16:31:00.000Z');
    expect(result.record.tenant_id).toBe(tenantId);
    expect(result.record.policy_key).toBe('auto_commit_daily_cap_gbp');
    expect(result.record.policy_value).toBe(250);
    expect(auditEvents).toHaveLength(1);
    expect(auditEvents[0]).toMatchObject({
      actor_id: admin.id,
      actor_role: 'admin',
      target_type: 'tenant_policy',
      target_id: 'auto_commit_daily_cap_gbp',
      outcome: 'allowed',
    });
  });

  test('protected administrative actions are denied for unauthorized roles', () => {
    const auditEvents = [];
    let executed = false;

    const result = runGovernedAction({
      actor: staff,
      tenantId,
      permission: PERMISSIONS.QUARTER_EXPORT,
      action: 'quarter.export_requested',
      targetType: 'quarter',
      targetId: 'Q1-2026',
      now: '2026-03-11T16:32:00.000Z',
      onAudit: (event) => auditEvents.push(event),
      callback: () => {
        executed = true;
      },
    });

    expect(result.allowed).toBe(false);
    expect(executed).toBe(false);
    expect(auditEvents).toHaveLength(1);
    expect(auditEvents[0]).toMatchObject({
      actor_role: 'staff',
      action: 'quarter.export_requested',
      permission: PERMISSIONS.QUARTER_EXPORT,
      outcome: 'denied',
      target_id: 'Q1-2026',
    });
  });
});
