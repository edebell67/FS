import type {
  BusinessValidationValues, FieldValidationOutcome, ValidationResult, ValidationRule,
} from "./types";

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE = /^\+?[0-9][0-9\s().-]{6,24}$/;

export function normalizeValidationValue(value: unknown): string | null {
  if (value === null || value === undefined) return null;
  const normalized = String(value).trim();
  return normalized === "" ? null : normalized;
}

function testRule(rule: ValidationRule, value: string): Pick<FieldValidationOutcome, "passed" | "outcomeCode" | "message"> {
  switch (rule.ruleType) {
    case "presence":
      return { passed: true, outcomeCode: "passed", message: null };
    case "email":
      return EMAIL.test(value)
        ? { passed: true, outcomeCode: "passed", message: null }
        : { passed: false, outcomeCode: "invalid_format", message: `${rule.label} is not a valid email address.` };
    case "phone":
      return PHONE.test(value)
        ? { passed: true, outcomeCode: "passed", message: null }
        : { passed: false, outcomeCode: "invalid_format", message: `${rule.label} is not a valid phone number.` };
    case "url": {
      try {
        const url = new URL(value);
        const passed = url.protocol === "http:" || url.protocol === "https:";
        return passed ? { passed, outcomeCode: "passed", message: null }
          : { passed, outcomeCode: "invalid_format", message: `${rule.label} must use http or https.` };
      } catch {
        return { passed: false, outcomeCode: "invalid_format", message: `${rule.label} is not a valid URL.` };
      }
    }
    case "regex": {
      try {
        const passed = new RegExp(rule.parameters?.pattern ?? "").test(value);
        return passed ? { passed, outcomeCode: "passed", message: null }
          : { passed, outcomeCode: "invalid_format", message: `${rule.label} does not match the configured pattern.` };
      } catch {
        return { passed: false, outcomeCode: "invalid_format", message: `${rule.label} has an invalid configured pattern.` };
      }
    }
    case "number_range": {
      const numeric = Number(value);
      const min = rule.parameters?.min;
      const max = rule.parameters?.max;
      const passed = Number.isFinite(numeric) && (min === undefined || numeric >= min) && (max === undefined || numeric <= max);
      return passed ? { passed, outcomeCode: "passed", message: null }
        : { passed, outcomeCode: "out_of_range", message: `${rule.label} is outside the configured numeric range.` };
    }
  }
}

export function validateBusiness(values: BusinessValidationValues, rules: ValidationRule[]): ValidationResult {
  const outcomes = [...rules]
    .sort((a, b) => `${a.fieldName}:${a.ruleType}:${a.id ?? ""}`.localeCompare(`${b.fieldName}:${b.ruleType}:${b.id ?? ""}`))
    .map((rule): FieldValidationOutcome => {
      const sourceValue = values[rule.fieldName];
      const normalizedValue = normalizeValidationValue(sourceValue);
      if (normalizedValue === null) {
        const passed = !rule.mandatory;
        return {
          ruleId: rule.id, fieldName: rule.fieldName, sourceValue: sourceValue == null ? null : String(sourceValue),
          normalizedValue, passed, outcomeCode: passed ? "passed" : "missing",
          message: passed ? null : `${rule.label} is mandatory.`, mandatory: rule.mandatory,
          blocksVerification: rule.blocksVerification,
        };
      }
      return {
        ruleId: rule.id, fieldName: rule.fieldName, sourceValue: String(sourceValue), normalizedValue,
        ...testRule(rule, normalizedValue), mandatory: rule.mandatory,
        blocksVerification: rule.blocksVerification,
      };
    });
  const failed = outcomes.filter((outcome) => !outcome.passed);
  const status = failed.some((outcome) => outcome.mandatory || outcome.blocksVerification)
    ? "non_valid" : failed.length > 0 ? "partially_validated" : "validated";
  return {
    status,
    outcomes,
    outstandingFields: [...new Set(failed.map((outcome) => outcome.fieldName))],
  };
}
