import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { assessNewsDateEvidence, chooseDuplicateSaveAction } from "./news-evidence";

test("selects a documented original event date over the source publication date", () => {
  const result = assessNewsDateEvidence({
    originalEventDate: "2026-07-20",
    sourcePublishedAt: "2026-07-22",
    dateProvenanceNote: "The council notice says the road closure began on 20 July.",
    dateConfidence: "high",
    dateSelectionRationale: "Use the original event date stated in the primary notice.",
    selectedDateKind: "original_event",
  });

  assert.deepEqual(result, {
    readyForPublish: true,
    reviewReason: null,
    effectiveStoryDate: "2026-07-20",
    effectiveDateKind: "original_event",
    originalEventDate: "2026-07-20",
    sourcePublishedDate: "2026-07-22",
    dateProvenance: {
      extractionNote: "The council notice says the road closure began on 20 July.",
      confidence: "high",
      selectionRationale: "Use the original event date stated in the primary notice.",
    },
  });
});

test("holds an impossible source date for editorial review", () => {
  const result = assessNewsDateEvidence({
    originalEventDate: "",
    sourcePublishedAt: "2026-02-31",
    dateProvenanceNote: "Publisher metadata date.",
    dateConfidence: "high",
    dateSelectionRationale: "No original event date was evidenced, so use publication date.",
    selectedDateKind: "source_publication",
  });

  assert.equal(result.readyForPublish, false);
  assert.equal(result.reviewReason, "missing_date_evidence");
  assert.equal(result.effectiveStoryDate, null);
});

test("routes a matching event identity to review without changing an existing published story", () => {
  assert.deepEqual(chooseDuplicateSaveAction({ matchingStatus: "published" }), {
    save: true,
    duplicateState: "review_required",
    reason: "matches_published_event",
  });
});

test("admin actions hold incomplete or duplicate evidence and gate publication", async () => {
  const actions = await readFile(new URL("./news-actions.ts", import.meta.url), "utf8");
  assert.match(actions, /assessNewsDateEvidence/);
  assert.match(actions, /chooseDuplicateSaveAction/);
  assert.match(actions, /WHERE news_articles\.status <> 'published'/);
  assert.match(actions, /duplicate_state = 'unique'/);
  assert.match(actions, /effective_date_kind = 'original_event'/);
});
