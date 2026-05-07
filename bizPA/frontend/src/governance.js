export const GOVERNANCE_ROLES = ['owner', 'admin', 'staff', 'accountant_readonly'];

export const ROLE_LABELS = {
  owner: 'Owner',
  admin: 'Admin',
  staff: 'Staff',
  accountant_readonly: 'Accountant (Read-only)',
};

export const PERMISSIONS = {
  GOVERNANCE_MANAGE: 'governance.manage',
  GOVERNANCE_AUDIT_READ: 'governance.audit.read',
  QUARTER_EXPORT: 'quarter.export',
  AUTO_COMMIT_MANAGE: 'auto_commit.manage',
  INBOX_RESOLVE: 'inbox.resolve',
  ACTIVITY_CAPTURE: 'activity.capture',
  ACTIVITY_READ: 'activity.read',
};

export const ROLE_PERMISSION_MATRIX = {
  owner: [
    PERMISSIONS.GOVERNANCE_MANAGE,
    PERMISSIONS.GOVERNANCE_AUDIT_READ,
    PERMISSIONS.QUARTER_EXPORT,
    PERMISSIONS.AUTO_COMMIT_MANAGE,
    PERMISSIONS.INBOX_RESOLVE,
    PERMISSIONS.ACTIVITY_CAPTURE,
    PERMISSIONS.ACTIVITY_READ,
  ],
  admin: [
    PERMISSIONS.GOVERNANCE_MANAGE,
    PERMISSIONS.GOVERNANCE_AUDIT_READ,
    PERMISSIONS.QUARTER_EXPORT,
    PERMISSIONS.AUTO_COMMIT_MANAGE,
    PERMISSIONS.INBOX_RESOLVE,
    PERMISSIONS.ACTIVITY_CAPTURE,
    PERMISSIONS.ACTIVITY_READ,
  ],
  staff: [
    PERMISSIONS.INBOX_RESOLVE,
    PERMISSIONS.ACTIVITY_CAPTURE,
    PERMISSIONS.ACTIVITY_READ,
  ],
  accountant_readonly: [
    PERMISSIONS.GOVERNANCE_AUDIT_READ,
    PERMISSIONS.ACTIVITY_READ,
  ],
};

export const DEFAULT_TENANT_POLICY_SETTINGS = [
  { policy_key: 'vat_scheme', policy_value: 'standard' },
  { policy_key: 'invoice_number_prefix', policy_value: 'INV-' },
  { policy_key: 'readiness_enforce_active_period', policy_value: true },
  { policy_key: 'large_transaction_threshold_gbp', policy_value: 1000 },
  { policy_key: 'feature_control_centre_enabled', policy_value: true },
  { policy_key: 'auto_commit_enabled', policy_value: true },
  { policy_key: 'auto_commit_daily_cap_gbp', policy_value: 500 },
  { policy_key: 'auto_commit_single_txn_cap_gbp', policy_value: 150 },
];

const buildAuditId = (timestamp, action, actorId) => {
  const normalizedAction = String(action || 'event').replace(/[^a-z0-9]+/gi, '-').toLowerCase();
  return `audit-${timestamp.replace(/[^0-9]/g, '').slice(0, 14)}-${actorId || 'system'}-${normalizedAction}`;
};

export const getRole = (actor) => {
  if (!actor?.role || !GOVERNANCE_ROLES.includes(actor.role)) {
    return 'staff';
  }
  return actor.role;
};

export const getPermissionsForRole = (role) => ROLE_PERMISSION_MATRIX[getRole({ role })] || [];

export const hasPermission = (actor, permission) => getPermissionsForRole(getRole(actor)).includes(permission);

export const createAuditEvent = ({
  tenantId,
  actor,
  action,
  permission = null,
  outcome = 'allowed',
  reason = null,
  targetType = 'system',
  targetId = null,
  metadata = {},
  now = new Date().toISOString(),
}) => ({
  id: buildAuditId(now, action, actor?.id),
  tenant_id: tenantId,
  action,
  permission,
  outcome,
  reason,
  actor_id: actor?.id || null,
  actor_name: actor?.name || 'Unknown actor',
  actor_role: getRole(actor),
  target_type: targetType,
  target_id: targetId,
  metadata,
  changed_at: now,
});

export const createPolicyRecord = ({
  tenantId,
  policyKey,
  policyValue,
  actor,
  now = new Date().toISOString(),
}) => ({
  tenant_id: tenantId,
  policy_key: policyKey,
  policy_value: policyValue,
  changed_by: actor?.id || null,
  changed_by_name: actor?.name || 'Unknown actor',
  changed_role: getRole(actor),
  changed_at: now,
});

export const buildDefaultPolicyRecords = ({
  tenantId,
  actor,
  now = new Date().toISOString(),
}) => DEFAULT_TENANT_POLICY_SETTINGS.map((setting) => createPolicyRecord({
  tenantId,
  policyKey: setting.policy_key,
  policyValue: setting.policy_value,
  actor,
  now,
}));

export const getPolicyRecord = (records, policyKey) => records.find((record) => record.policy_key === policyKey) || null;

export const getPolicyValue = (records, policyKey, fallbackValue = null) => {
  const record = getPolicyRecord(records, policyKey);
  return record ? record.policy_value : fallbackValue;
};

export const authorizePermission = ({
  actor,
  tenantId,
  permission,
  action,
  targetType,
  targetId,
  metadata = {},
  now = new Date().toISOString(),
}) => {
  if (hasPermission(actor, permission)) {
    return { allowed: true };
  }

  const role = ROLE_LABELS[getRole(actor)] || getRole(actor);
  const reason = `${role} cannot perform ${action}.`;
  return {
    allowed: false,
    reason,
    auditEvent: createAuditEvent({
      tenantId,
      actor,
      action,
      permission,
      outcome: 'denied',
      reason,
      targetType,
      targetId,
      metadata,
      now,
    }),
  };
};

export const runGovernedAction = ({
  actor,
  tenantId,
  permission,
  action,
  targetType,
  targetId,
  metadata = {},
  now = new Date().toISOString(),
  onAudit,
  callback,
}) => {
  const authorization = authorizePermission({
    actor,
    tenantId,
    permission,
    action,
    targetType,
    targetId,
    metadata,
    now,
  });

  if (!authorization.allowed) {
    onAudit?.(authorization.auditEvent);
    return authorization;
  }

  const result = callback ? callback() : null;
  const auditEvent = createAuditEvent({
    tenantId,
    actor,
    action,
    permission,
    outcome: 'allowed',
    targetType,
    targetId,
    metadata,
    now,
  });
  onAudit?.(auditEvent);

  return {
    allowed: true,
    result,
    auditEvent,
  };
};

export const applyPolicyUpdate = ({
  records,
  tenantId,
  actor,
  policyKey,
  policyValue,
  reason,
  now = new Date().toISOString(),
  onAudit,
}) => {
  const authorization = authorizePermission({
    actor,
    tenantId,
    permission: PERMISSIONS.GOVERNANCE_MANAGE,
    action: 'policy.update',
    targetType: 'tenant_policy',
    targetId: policyKey,
    metadata: { policy_key: policyKey, requested_value: policyValue, reason },
    now,
  });

  if (!authorization.allowed) {
    onAudit?.(authorization.auditEvent);
    return authorization;
  }

  const updatedRecord = createPolicyRecord({
    tenantId,
    policyKey,
    policyValue,
    actor,
    now,
  });
  const orderedKeys = DEFAULT_TENANT_POLICY_SETTINGS.map((setting) => setting.policy_key);
  const nextRecords = [...records.filter((record) => record.policy_key !== policyKey), updatedRecord]
    .sort((left, right) => {
      const leftIndex = orderedKeys.indexOf(left.policy_key);
      const rightIndex = orderedKeys.indexOf(right.policy_key);
      return leftIndex - rightIndex;
    });
  const auditEvent = createAuditEvent({
    tenantId,
    actor,
    action: 'policy.updated',
    permission: PERMISSIONS.GOVERNANCE_MANAGE,
    targetType: 'tenant_policy',
    targetId: policyKey,
    metadata: { policy_key: policyKey, policy_value: policyValue, reason },
    now,
  });
  onAudit?.(auditEvent);

  return {
    allowed: true,
    records: nextRecords,
    record: updatedRecord,
    auditEvent,
  };
};
