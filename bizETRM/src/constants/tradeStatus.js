// src/constants/tradeStatus.js
// V1.1.8 - 2026-03-04

export const STATUS = {
  DRAFT: 100,
  SUBMITTED: 200,
  VALIDATED: 300,
  CONFIRMED: 400,
  CANCEL_REQUESTED: 500,
  CANCELLED: 600,
  REJECTED: 700
};

export const STATUS_LABELS = {
  [STATUS.DRAFT]: 'Draft',
  [STATUS.SUBMITTED]: 'Submitted',
  [STATUS.VALIDATED]: 'Validated',
  [STATUS.CONFIRMED]: 'Confirmed',
  [STATUS.CANCEL_REQUESTED]: 'Cancel Requested',
  [STATUS.CANCELLED]: 'Cancelled',
  [STATUS.REJECTED]: 'Rejected'
};

export const ROLES = {
  FO: 'FO', // Front Office
  MO: 'MO', // Middle Office
  BO: 'BO', // Back Office
  ADMIN: 'Admin'
};
