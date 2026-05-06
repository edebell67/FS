// src/logic/lifecycleEngine.js
// V1.1.8 - 2026-03-04
import { STATUS, ROLES } from '../constants/tradeStatus';

/**
 * Transition Matrix (Target Status -> Allowed Source Statuses)
 * This prevents "cheating" and ensures rigid workflow compliance.
 */
const TRANSITION_RULES = {
  [STATUS.SUBMITTED]: {
    allowedFrom: [STATUS.DRAFT, STATUS.REJECTED],
    allowedRoles: [ROLES.FO, ROLES.ADMIN]
  },
  [STATUS.VALIDATED]: {
    allowedFrom: [STATUS.SUBMITTED],
    allowedRoles: [ROLES.MO, ROLES.ADMIN]
  },
  [STATUS.CONFIRMED]: {
    allowedFrom: [STATUS.SUBMITTED, STATUS.VALIDATED],
    allowedRoles: [ROLES.MO, ROLES.ADMIN] // Workflow 2A: MO Confirm = Auto-Confirm
  },
  [STATUS.REJECTED]: {
    allowedFrom: [STATUS.SUBMITTED, STATUS.VALIDATED],
    allowedRoles: [ROLES.MO, ROLES.ADMIN]
  },
  [STATUS.CANCEL_REQUESTED]: {
    allowedFrom: [STATUS.CONFIRMED],
    allowedRoles: [ROLES.FO, ROLES.MO, ROLES.ADMIN]
  },
  [STATUS.CANCELLED]: {
    allowedFrom: [STATUS.CANCEL_REQUESTED],
    allowedRoles: [ROLES.MO, ROLES.ADMIN]
  }
};

/**
 * Validates if a status transition is allowed.
 * @param {number} currentStatus 
 * @param {number} targetStatus 
 * @param {string} userRole 
 * @returns {{ allowed: boolean, reason?: string }}
 */
export const validateTransition = (currentStatus, targetStatus, userRole) => {
  const rule = TRANSITION_RULES[targetStatus];
  
  if (!rule) return { allowed: false, reason: 'Invalid target status' };

  if (!rule.allowedFrom.includes(currentStatus)) {
    return { allowed: false, reason: `Cannot transition to this status from the current state.` };
  }

  if (!rule.allowedRoles.includes(userRole)) {
    return { allowed: false, reason: `Your role (${userRole}) does not have permission for this action.` };
  }

  return { allowed: true };
};

/**
 * Gets available actions for a deal based on its current status and the user's role.
 */
export const getAvailableActions = (currentStatus, userRole) => {
  const actions = [];

  Object.entries(TRANSITION_RULES).forEach(([targetStatus, rule]) => {
    if (rule.allowedFrom.includes(currentStatus) && rule.allowedRoles.includes(userRole)) {
      actions.push(parseInt(targetStatus));
    }
  });

  return actions;
};
