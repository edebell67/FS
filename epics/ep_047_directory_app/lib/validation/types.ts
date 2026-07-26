export const VALIDATION_STATUSES = ["non_valid", "partially_validated", "validated"] as const;
export type ValidationStatus = (typeof VALIDATION_STATUSES)[number];

export const VALIDATABLE_FIELDS = [
  "businessName", "tradingName", "category", "subCategory", "email", "phone", "mobile",
  "website", "facebook", "instagram", "linkedin", "address", "town", "county", "postcode",
  "latitude", "longitude", "googleRating", "reviewCount", "description",
] as const;
export type ValidatableField = (typeof VALIDATABLE_FIELDS)[number];

export const RULE_TYPES = ["presence", "email", "phone", "url", "regex", "number_range"] as const;
export type RuleType = (typeof RULE_TYPES)[number];

export interface ValidationRule {
  id?: string;
  fieldName: ValidatableField;
  label: string;
  ruleType: RuleType;
  mandatory: boolean;
  blocksVerification: boolean;
  parameters?: { pattern?: string; min?: number; max?: number };
}

export type BusinessValidationValues = Partial<Record<ValidatableField, unknown>>;

export interface FieldValidationOutcome {
  ruleId?: string;
  fieldName: ValidatableField;
  sourceValue: string | null;
  normalizedValue: string | null;
  passed: boolean;
  outcomeCode: "passed" | "missing" | "invalid_format" | "out_of_range";
  message: string | null;
  mandatory: boolean;
  blocksVerification: boolean;
}

export interface ValidationResult {
  status: ValidationStatus;
  outcomes: FieldValidationOutcome[];
  outstandingFields: ValidatableField[];
}
