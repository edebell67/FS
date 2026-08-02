export type DateKind = "original_event" | "source_publication";
export type DateConfidence = "high" | "medium" | "low";

export type NewsDateEvidenceInput = {
  originalEventDate: string;
  sourcePublishedAt: string;
  dateProvenanceNote: string;
  dateConfidence: string;
  dateSelectionRationale: string;
  selectedDateKind: string;
};

export type NewsDateEvidenceAssessment = {
  readyForPublish: boolean;
  reviewReason: string | null;
  effectiveStoryDate: string | null;
  effectiveDateKind: DateKind | null;
  originalEventDate: string | null;
  sourcePublishedDate: string | null;
  dateProvenance: {
    extractionNote: string;
    confidence: DateConfidence | null;
    selectionRationale: string;
  };
};

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;

function asDate(value: string): string | null {
  const trimmed = value.trim();
  const parsed = Date.parse(`${trimmed}T00:00:00Z`);
  return ISO_DATE.test(trimmed) && !Number.isNaN(parsed) && new Date(parsed).toISOString().slice(0, 10) === trimmed
    ? trimmed
    : null;
}

export type DuplicateSaveAction = {
  save: boolean;
  duplicateState: "unique" | "review_required";
  reason: string | null;
};

export function chooseDuplicateSaveAction(input: { matchingStatus: string | null }): DuplicateSaveAction {
  if (input.matchingStatus === "published") {
    return { save: true, duplicateState: "review_required", reason: "matches_published_event" };
  }
  return input.matchingStatus
    ? { save: true, duplicateState: "review_required", reason: "matches_existing_event" }
    : { save: true, duplicateState: "unique", reason: null };
}

export function assessNewsDateEvidence(input: NewsDateEvidenceInput): NewsDateEvidenceAssessment {
  const originalEventDate = asDate(input.originalEventDate);
  const sourcePublishedDate = asDate(input.sourcePublishedAt);
  const selectedDateKind = input.selectedDateKind === "original_event" || input.selectedDateKind === "source_publication"
    ? input.selectedDateKind
    : null;
  const confidence = input.dateConfidence === "high" || input.dateConfidence === "medium" || input.dateConfidence === "low"
    ? input.dateConfidence
    : null;
  const extractionNote = input.dateProvenanceNote.trim();
  const selectionRationale = input.dateSelectionRationale.trim();
  const effectiveStoryDate = selectedDateKind === "original_event" ? originalEventDate : sourcePublishedDate;
  const missingEvidence = !sourcePublishedDate || !selectedDateKind || !effectiveStoryDate || !extractionNote || !confidence || !selectionRationale;

  return {
    readyForPublish: !missingEvidence,
    reviewReason: missingEvidence ? "missing_date_evidence" : null,
    effectiveStoryDate,
    effectiveDateKind: selectedDateKind,
    originalEventDate,
    sourcePublishedDate,
    dateProvenance: { extractionNote, confidence, selectionRationale },
  };
}
