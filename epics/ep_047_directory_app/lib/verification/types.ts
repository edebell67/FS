export const EDITABLE_FIELDS = [
  "businessName", "tradingName", "phone", "email", "website",
  "address", "town", "postcode", "category",
] as const;

export type EditableField = (typeof EDITABLE_FIELDS)[number];
export type SubmittedFields = Record<EditableField, string>;

export interface VerificationInput {
  fields: SubmittedFields;
  requesterName: string;
  relationship: "owner" | "employee" | "authorised_representative" | "other";
  accuracyConfirmed: boolean;
  contactEmail?: string;
  contactPhone?: string;
}
